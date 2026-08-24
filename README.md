# dimitrismallis.github.io

Personal academic website of **Dr. Dimitrios Mallis** — Postdoctoral Researcher in 3D
Computer Vision at [SnT](https://www.uni.lu/snt-en/), University of Luxembourg.

Live at <https://dimitrismallis.github.io>.

## Structure

Built with [al-folio](https://github.com/alshedivat/al-folio) **v1.x**, which is a *thin
Jekyll starter, not a theme* — all layouts, includes, Sass and Liquid tags come from
versioned gems (`al_folio_core` and friends, pinned in the `Gemfile`). This repo owns only
content and configuration:

| Path | Contents |
| --- | --- |
| `_config.yml` | Site configuration |
| `_data/socials.yml` | Social links, Google Scholar ID |
| `_data/repositories.yml` | GitHub repos shown as cards |
| `_data/citations.yml` | Google Scholar citation counts (generated) |
| `_bibliography/papers.bib` | Publications |
| `_news/` | News items shown on the landing page |
| `_pages/` | About, Publications, News, external nav links |
| `assets/` | Images, PDFs, publication previews |

There are **no local overrides** of gem-owned files, so upgrades are just a dependency
bump. Keep it that way where possible.

## Local development

```bash
bundle install
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 bundle exec jekyll serve
```

The `LANG`/`LC_ALL` exports matter: without a UTF-8 locale, Ruby reads the site's
non-ASCII content (emoji, `CVI²`) as US-ASCII and the build dies with
`invalid byte sequence in US-ASCII`.

Optional: `brew install imagemagick` to generate the responsive `.webp` image variants
locally. Without it the build logs `convert: command not found` and images fall back to
their original format — harmless, and CI installs ImageMagick anyway.

## Upgrading

```bash
bundle update
bundle exec al-folio upgrade audit          # flags breaking/deprecated patterns
bundle exec al-folio upgrade overrides audit # flags local files shadowing gem files
bundle exec al-folio upgrade report
```

If a local override is ever added, run `overrides accept <path>` and commit
`.al-folio-overrides.yml` so future gem updates can flag drift on the shadowed file.

## Deployment

Pushing to `master` triggers `.github/workflows/deploy.yml`, which builds the site and
publishes `_site` to the `gh-pages` branch.
