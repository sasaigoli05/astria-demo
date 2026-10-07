# Astria — site

Plain static HTML. No framework, no build chain, no dependencies.

## Files

```
docs/
  build.py            ← edit page content HERE, then run it
  assets/astria.css   ← all styling; brand tokens at the top
  assets/ncdata.json  ← NC county geography + facility counts (coverage map)
  assets/img/         ← team photos, affiliation logos
  *.html              ← generated output — don't hand-edit, they get overwritten
```

## Editing

Page content lives in the `PAGES` dict in `build.py`. Change the copy, then:

```bash
python3 build.py
```

That restamps every page with the shared header, nav and footer, so the chrome
can never drift between pages. To add a page, add it to `NAV` and to `PAGES`.

If you'd rather hand-edit the HTML directly, that works too — just stop running
`build.py`, or it will overwrite your changes.

## Previewing locally

```bash
python3 -m http.server 4173 --directory docs
```

Then open http://localhost:4173. **A local server is required** — the coverage
map fetches `assets/ncdata.json`, which browsers block over `file://`.

## Publishing to GitHub Pages

GitHub Pages only serves from the repository root or from `/docs`. Two options:

**Option A — rename the folder** (least disruptive)
```bash
# already done — this folder IS docs/
```
Then: Settings → Pages → Source: *Deploy from a branch* → `main` / `/docs`.
Update the path in `.claude/launch.json` if you want local preview to keep working.

**Option B — move the contents to the repo root**
```bash
git mv docs/* .
git rm -r site
```
Then set Pages source to `main` / `/ (root)`.

Either way the site is live at `https://<user>.github.io/<repo>/` within a minute
or two. No Actions workflow needed.

## Fonts

Manrope (display) and Inter (body) load from Google Fonts via the `<link>` in the
page head — nothing to install for the website. The PowerPoint deck in the parent
folder specifies the same two faces and *does* need them installed locally.

## Brand tokens

All colours are CSS custom properties at the top of `astria.css`, named to match
the Brand Toolkit v1.1:

| Token | Hex | Use |
|---|---|---|
| `--midnight` | `#101B2D` | primary brand, headings, dark sections |
| `--northstar` | `#F7F5EF` | warm canvas |
| `--celestial` | `#4776E6` | actions, navigation, active states |
| `--horizon` | `#AABEF5` | secondary UI, diagram strokes |
| `--renewal` | `#91B5A2` | health, success, progress |
| `--gold` | `#E8B85B` | north star and milestones only — a signal, not a fill |
| `--slate` | `#687386` | secondary text |

Target ratio is roughly 45% ivory / 25% white / 20% midnight / 7% celestial /
3% accents. Gold appears on this site in exactly four places: the logo star, the
Astria ID card, the accent stat tiles, and milestone pills. Keep it that scarce.

## Interactive demos

- **argo.html** — upload → extraction. `#argo-run` staggers the structured fields
  in, flagging two gaps. Sample data lives in the `DATA` array in the page script.
- **astria-id.html** — four scenario buttons (baseline, coverage lapse, move
  county, return to custody) showing institutional identifiers changing while the
  Astria ID holds. Scenarios in the `EV` array.
- **coverage.html** — the real NC map. Three metrics plus a travel-radius slider.
  Data is genuine; distances are straight-line county-centroid.

## A note on the content

Every statistic on the site is sourced in the surrounding text. Figures derived
from our own analysis are labelled as such, and the open questions we haven't
resolved — the cadence floor, community-programme adoption, the CHW billing path,
the un-validated reimbursement rate — are stated on the relevant pages rather than
hidden. Please keep them there as the site grows; they're load-bearing for
credibility, not a weakness to edit out.
