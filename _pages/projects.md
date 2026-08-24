---
# Nav dropdown of project pages. al_folio_core's header.liquid renders the parent as a
# non-navigating toggle (href="#") and links each child straight out when its permalink
# contains '://', so this needs no layout override.
layout: none
title: Projects
nav: true
nav_order: 2
dropdown: true
sitemap: false # the parent never navigates, so keep the stub out of the sitemap
children:
  - title: MiCADangelo
    permalink: https://cvi2snt.github.io/micadangelo/
  - title: CAD-Assistant
    permalink: https://cadassistant.github.io/
  - title: CAD-Recode
    permalink: https://cad-recode.github.io/
  - title: PICASSO
    permalink: https://cvi2snt.github.io/picasso/
  - title: DAVINCI
    permalink: https://cvi2snt.github.io/davinci/
  - title: TransCAD
    permalink: https://cvi2snt.github.io/transcad/
  - title: Morfis
    permalink: https://www.morfis.ai/
---
