# Astria

**Every point of care. One path forward.**

Astria is a care-navigation platform for people leaving incarceration. It onboards
someone before release from whatever records exist, assembles a care team around
them, and keeps checking that the connection holds.

This repository holds the public site, the pitch materials, and the research that
underpins them.

```
docs/                     the website (GitHub Pages serves from here)
  build.py                page content lives here — edit this, then run it
  assets/astria.css       brand tokens and all styling
  assets/img/             logos, team photos, affiliation marks
  assets/ncdata.json      NC county geography + facility counts
Research/                 (local only — not in the repo)
Astria-Pitch-Deck.pptx    13-slide deck (needs Manrope + Inter installed)
astria-deck-generator.js  the script that produces the deck
Astria_Brand_Toolkit_v1_1.pdf
```

## Working on the site

```bash
python3 docs/build.py                              # regenerate the HTML
python3 -m http.server 4173 --directory docs       # preview
```

Then open <http://localhost:4173>. A local server is required — the coverage map
fetches a JSON file, which browsers block over `file://`.

See `docs/README.md` for the full site notes.

## Publishing

The site is already in `docs/`, which is one of the two locations GitHub Pages can
serve from. After pushing:

**Settings → Pages → Source: _Deploy from a branch_ → `main` / `/docs` → Save**

It goes live at `https://<user>.github.io/<repo>/` in a minute or two. No Actions
workflow, no build step.

## Status

Working draft. Astria is not a deployed service. Figures on the site are sourced
where they appear; analysis we produced ourselves is labelled as such, and the
questions we have not resolved are stated rather than hidden.
