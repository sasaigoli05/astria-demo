# Astria — pitch video production plan

Fourteen animated scenes, 1920×1080, built to the Brand Toolkit's motion rule:
**nodes appear → one continuous line draws between them → the North Star
illuminates**, 700–1200ms per beat. Calm and subtle, never sci-fi.

Everything is CSS animation driven by `animation-delay` — no JS clock — so
`htmlrec` renders it frame-perfectly and the same file looks identical every time.

---

## 1 · Scene map

Timings are the *animation* length. Narration should land slightly inside each
scene so the graphic resolves a beat before the voice moves on.

| # | Scene | Len | Speaker | The line it carries |
|---|---|---|---|---|
| 01 | `01-mortality` | 14s | 1 | "…the risk of death is 12.7 times higher… an overdose, untreated blood pressure, a prescription rationed between refills." |
| 02 | `02-chronic` | 8s | 1 | "Nearly 80% of people leaving incarceration have a chronic medical, psychiatric, or substance-use condition." |
| 03 | `03-ownership` | 22s | 1 | "It isn't that nobody provides care… a jail's responsibility ends at release… every system can work exactly as designed." |
| 04 | `04-astria` | 12s | 2 | "That's why we built Astria: a care-navigation platform…" |
| 05 | `05-argo` | 22s | 2 | "Onboarding begins with Argo… fewer than 5%… Argo takes off the load." |
| 06 | `06-id` | 18s | 2 | "Each enrollee receives an Astria ID… nobody starts over." |
| 07 | `07-evidence` | 14s | 3 | "Research from the Transitions Clinic Network found… 39% to 25%." |
| 08 | `08-promoter` | 20s | 3 | "Those insights shape Astria's Care Promoter model…" |
| 09 | `09-network` | 14s | 3 | "Argo handles the administrative burden. The community network… Care Promoters…" |
| 10 | `10-implementation` | 20s | 4 | "Our initial customer base is established transitional-care programs…" |
| 11 | `11-outcome` | 12s | 4 | "Our primary pilot outcome is simple: was someone connected to care within 30 days?" |
| 12 | `12-map` | 20s | 5 | "North Carolina is our first market… mapping safety-net health infrastructure statewide." |
| 13 | `13-pathway` | 16s | 5 | "Start with one established network. Validate… Then expand." |
| 14 | `14-close` | 18s | 5 | "Astraea is a constellation… Leaving incarceration should never mean leaving care." |

**Total animation: 3:50.**

### If you need a 3:00 cut

Drop these four and the rest still tells the whole story:

| Cut | Why it survives without it |
|---|---|
| `02-chronic` (−8s) | Fold "nearly 80%" into the 01 voiceover; the dot grid is a nice-to-have |
| `09-network` (−14s) | Scene 08 already shows the three-way relationship visually |
| `11-outcome` (−12s) | Say the 30-day metric over the tail of scene 10 |
| `13-pathway` (−16s) | Say the three steps over the map in scene 12 as the anchors bloom |

That lands at **3:00** exactly, with no scene feeling truncated.

---

## 2 · Rendering

Install once:

```bash
npm install -g htmlrec
```

Render everything:

```bash
cd video
bash record.sh          # 14 MP4s into ./out, 1920×1080 @ 60fps
```

Budget roughly **5× real time** — the full set takes about 20 minutes. Render one
scene while you're iterating:

```bash
hrec render scenes/05-argo.html -o out/05-argo.mp4 -d 22 -f 60 --width 1920 --height 1080
```

### Transparent versions for overlays

If you want a scene to sit over footage in your editor:

```bash
hrec render scenes/04-astria.html -o out/04-astria.webm -d 12 -f 60 \
  --width 1920 --height 1080 --transparent
```

You'd need to remove the `background` from `body` in `shared.css` first — the
scenes are currently opaque by design.

### Fast composition checks

Each scene has a snapshot mode that collapses every delay so one frame shows the
finished composition — useful when you're adjusting layout and don't want to wait
for a full render:

```bash
# add ?snap to the URL in a browser, or render the .snap copies:
hrec render .snap/05-argo.html -o /tmp/s.mp4 -d 0.4 -f 10 --width 1920 --height 1080
```

---

## 3 · Assembly

**Order:** straight sequence 01 → 14. No reordering needed; the scenes were built
to the script's order.

**Transitions:** cross-dissolve, 400–500ms, between every scene. The brand motion
is calm; hard cuts fight it. The two light scenes (09, 10) will flash if you hard
cut into them — dissolve is doing real work there.

**Audio bed:** something sparse and warm. Piano or soft strings, no percussion
driving a beat. The animations have no rhythm to sync to, and adding one makes the
whole thing feel like a product launch rather than a health pitch. Duck to about
−22dB under narration.

**Narration:** record each speaker separately, dry, then place. Leave 300–400ms of
air between speakers so the handoffs read as deliberate rather than rushed.

**Captions:** burn them in. A lot of people will watch this muted, and the
statistics are the thing you can least afford to have missed.

---

## 4 · Where the voice should sit inside each scene

The scenes have internal beats. Landing narration on them is most of what makes
this feel composed rather than slideshow-with-voiceover.

- **01** — say "12.7 times higher" as the number lands (0.6s), then pause. The
  three chips appear at 4.2s / 5.6s / 7.0s — one cause per chip, don't rush them.
- **03** — each rail fills and *stops* 2.6s apart. Say each system's name as its
  rail starts, and its ending as the red stop appears. The closing line arrives at
  9.0s; let the dots finish dropping before you say it.
- **04** — the logo wipes in over 2.2s. Say nothing until it completes. The star
  blooms at 2.5s; "Astria" should land there.
- **05** — the four input chips stagger 2.4–4.5s, the connector draws at 5.0s, the
  record fields build from 6.2s. "Fewer than 5%" goes over the input chips.
- **06** — the three identifiers, then the converging lines at 2.9s, then the ID
  card pops at 4.4s. The three events run 8.2–11.2s; "nobody starts over" lands on
  the green line at 12.6s.
- **07** — the 39% bar rises at 2.2s, the arrow draws at 4.4s, the 25% bar at 5.6s.
  Say the numbers as they appear, not before.
- **08** — the centre card at 2.6s, the member at 4.9s, then partners from 6.4s.
  "Those insights shape…" over the card; name the partner categories as they land.
- **12** — counties draw in over ~1.5s, stats at 1.8s and 2.3s, then the 24 anchor
  circles bloom from 2.3s. "24 anchor sites" lands at about 4.6s.
- **14** — the constellation draws over 2.6s, the star blooms at 3.2s, the Astraea
  line fades at 4.2s. **Hold silence from 6.5s to 8.0s.** The final line lands at
  8.0s. Don't fill that gap.

---

## 5 · Editing the scenes

Content lives in `build.py`. Change it there, then:

```bash
python3 build.py
```

That rewrites `scenes/*.html`, `index.html` and `record.sh` together, so timings
and the record script can't drift from the scenes.

Motion primitives are in `shared.css` — `.fx` (rise), `.fade`, `.pop`, `.draw`
(line draws itself), `.bloom` (star illuminates), `.grow`, `.riseBar`, `.travel`,
`.drop`. Every one takes `--d` for its delay and most take `--dur`.

To restyle globally, the brand tokens are at the top of `shared.css`. Gold is a
signal — it appears on milestones, the North Star, and single key figures. Keep it
that scarce.

---

## 6 · Preview

```bash
python3 -m http.server 4174 --directory video
```

`index.html` is a scene player with a timeline — click through, replay, check
pacing before you commit to a render.

---

## 7 · One thing to decide before you record narration

The script runs about four minutes read at a natural pace, which matches the
animation. If the submission caps at three, make the cut from §1 **before** you
record — re-cutting narration to fit is much worse than writing to length.
