#!/usr/bin/env python3
"""Refresh _data/citations.yml from Google Scholar.

al_folio_core's bib layout renders the scholar badge by looking up
'<scholar_userid>:<google_scholar_id>' in site.data.citations.papers and baking the
count into a shields.io URL at build time. Google publishes no embed widget or API
for citation counts, so they have to be fetched out of band and committed.

Reads scholar_userid from _data/socials.yml. Writes _data/citations.yml.

Google throttles datacenter IPs hard, so this is expected to fail sometimes. On any
failure it leaves the existing citations.yml untouched and exits non-zero; the site
then keeps rendering the last known counts rather than regressing to zeros.

Usage:  python3 bin/update_scholar_citations.py
"""

from __future__ import annotations

import html
import re
import sys
import urllib.error
import urllib.request
from datetime import date, timezone, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOCIALS = ROOT / "_data" / "socials.yml"
OUTPUT = ROOT / "_data" / "citations.yml"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
ROW_RE = re.compile(
    r'citation_for_view=(?P<uid>[\w-]+):(?P<pid>[\w-]+)"[^>]*>(?P<title>.*?)</a>'
    r'.*?gsc_a_c">.*?>(?P<cites>\d*)</a>.*?gsc_a_y">.*?>(?P<year>\d*)<',
    re.S,
)


def scholar_userid() -> str:
    if not SOCIALS.exists():
        sys.exit(f"{SOCIALS} not found")
    uid = (yaml.safe_load(SOCIALS.read_text(encoding="utf-8")) or {}).get("scholar_userid")
    if not uid:
        sys.exit(f"no 'scholar_userid' in {SOCIALS}")
    return str(uid)


def fetch(uid: str) -> str:
    url = f"https://scholar.google.com/citations?user={uid}&hl=en&cstart=0&pagesize=100"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError) as exc:
        sys.exit(f"could not reach Google Scholar: {exc}")
    if re.search(r"unusual traffic|not a robot|/sorry/", body, re.I):
        sys.exit("Google Scholar served a bot check; leaving citations.yml unchanged")
    if f"citation_for_view={uid}:" not in body:
        sys.exit("no publications found in the profile page; layout may have changed")
    return body


def strip_tags(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]*>", "", text)).strip()


def main() -> None:
    uid = scholar_userid()
    papers = {}
    for m in ROW_RE.finditer(fetch(uid)):
        if m.group("uid") != uid:
            continue
        papers[f"{uid}:{m.group('pid')}"] = {
            "citations": int(m.group("cites") or 0),
            "title": strip_tags(m.group("title")),
            "year": m.group("year") or "Unknown Year",
        }
    if not papers:
        sys.exit("parsed zero publications; leaving citations.yml unchanged")

    header = (
        "# Google Scholar citation counts, consumed by al_folio_core's bib layout.\n"
        "# Regenerate with: python3 bin/update_scholar_citations.py\n"
        "# Keys are '<scholar_userid>:<google_scholar_id>' and must match the\n"
        "# google_scholar_id fields in _bibliography/papers.bib.\n"
    )
    doc = {
        "metadata": {
            "last_updated": date.today().isoformat(),
            "scholar_userid": uid,
        },
        "papers": dict(
            sorted(papers.items(), key=lambda kv: -kv[1]["citations"])
        ),
    }
    OUTPUT.write_text(
        header + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=1000),
        encoding="utf-8",
    )
    total = sum(p["citations"] for p in papers.values())
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(papers)} papers, {total} total citations")


if __name__ == "__main__":
    main()
