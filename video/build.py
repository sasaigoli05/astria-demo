#!/usr/bin/env python3
"""
Astria pitch-video scene builder.

Each scene is a standalone 1920x1080 HTML page whose animation runs purely from
CSS `animation-delay` — no JS clock, no requestAnimationFrame — so htmlrec can
render it frame-perfectly and deterministically.

    python3 build.py          # writes scenes/*.html, index.html, record.sh
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
NCDATA = os.path.join(HERE, "..", "docs", "assets", "ncdata.json")

# ---------------------------------------------------------------- NC map paths
def nc_paths(width=760, height=330, pad=6):
    with open(NCDATA) as f:
        D = json.load(f)
    C = D["counties"]
    lons, lats = [], []
    for c in C:
        for poly in c["polys"]:
            for x, y in poly[0]:
                lons.append(x); lats.append(y)
    minx, maxx = min(lons), max(lons)
    miny, maxy = min(lats), max(lats)
    import math
    k = math.cos(math.radians((miny + maxy) / 2))
    sx = (width - 2 * pad) / ((maxx - minx) * k)
    h = (maxy - miny) * sx + 2 * pad
    px = lambda l: pad + (l - minx) * k * sx
    py = lambda l: h - pad - (l - miny) * sx
    out = []
    for c in C:
        d = ""
        for poly in c["polys"]:
            for ring in poly:
                for i, (x, y) in enumerate(ring):
                    d += ("L" if i else "M") + f"{px(x):.1f} {py(y):.1f}"
                d += "Z"
        out.append((c["name"], d, px(c["cx"]), py(c["cy"]), c["fq"]))
    return out, width, h

MAP, MAP_W, MAP_H = nc_paths()

def counties_svg():
    return "".join(
        f'<path class="cty fade" style="--d:{300 + (i % 23) * 55}ms" d="{d}"/>'
        for i, (_, d, _, _, _) in enumerate(MAP))

def anchors_svg():
    """24-ish well-spread anchor counties, with their coverage radius blooming."""
    picks = [n for n in ["Buncombe","Henderson","Macon","Avery","Watauga","Caldwell",
                         "Lincoln","Cabarrus","Davidson","Guilford","Surry","Orange",
                         "Franklin","Harnett","Hoke","Anson","Bladen","Wayne",
                         "Edgecombe","Halifax","Craven","Jones","New Hanover","Pamlico"]]
    by = {m[0]: m for m in MAP}
    rings = dots = ""
    for i, nm in enumerate(picks):
        if nm not in by: continue
        _, _, cx, cy, _ = by[nm]
        d = 2300 + i * 95
        rings += (f'<circle class="pop" style="--d:{d}ms" cx="{cx:.1f}" cy="{cy:.1f}" r="38" '
                  f'fill="rgba(71,118,230,.17)" stroke="rgba(170,190,245,.5)" stroke-width="1"/>')
        dots  += (f'<circle class="pop" style="--d:{d+120}ms" cx="{cx:.1f}" cy="{cy:.1f}" r="4.6" '
                  f'fill="#E8B85B"/>')
    return rings + dots

# ---------------------------------------------------------------- scenes
S = []   # (id, label, seconds, body_classes, html)

S.append(("01-mortality", "Problem — mortality", 14, "", f"""
<div class="stage">
  <div class="eyebrow fx" style="--d:200ms">The first two weeks</div>
  <div style="display:flex;align-items:flex-end;gap:54px;margin-top:34px">
    <div class="huge fx" style="--d:600ms">12.7&times;</div>
    <div class="sub fx" style="--d:1100ms;margin-bottom:46px;max-width:19ch">higher risk of death
      after release from prison, compared with the general population</div>
  </div>
  <div style="display:flex;gap:26px;margin-top:86px">
    <div class="chip gold fx" style="--d:4200ms"><span class="dot"></span>An overdose</div>
    <div class="chip gold fx" style="--d:5600ms"><span class="dot"></span>Untreated blood pressure</div>
    <div class="chip gold fx" style="--d:7000ms"><span class="dot"></span>A prescription rationed between refills</div>
  </div>
  <div class="tiny fade" style="--d:9200ms;margin-top:76px">Binswanger et al., New England Journal of Medicine, 2007</div>
</div>"""))

dots = "".join(
    f'<i class="pop" style="--d:{900 + i*26}ms;background:{"#E8B85B" if i < 80 else "#2A3A54"}"></i>'
    for i in range(100))
S.append(("02-chronic", "Problem — chronic conditions", 8, "", f"""
<div class="stage">
  <div class="eyebrow fx" style="--d:150ms">Who is leaving</div>
  <h2 class="fx" style="--d:500ms;max-width:20ch;margin-top:26px">Nearly 80% have a chronic
    medical, psychiatric, or substance-use condition</h2>
  <div style="display:grid;grid-template-columns:repeat(20,1fr);gap:15px;width:900px;margin-top:62px">
    {dots}
  </div>
  <style>.stage i{{width:26px;height:26px;border-radius:50%;display:block}}</style>
  <div class="tiny fade" style="--d:4600ms;margin-top:60px">ASPE Report to Congress, 2023</div>
</div>"""))

rails = ""
for i, (who, ends, t) in enumerate([
        ("A jail's responsibility", "ends at release", 0),
        ("A health plan's", "can end at disenrollment", 2600),
        ("A clinic loses someone", "when they disappear from its panel", 5200)]):
    rails += f"""
  <div style="margin-bottom:74px">
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:20px">
      <span class="label fx" style="--d:{300+t}ms;font-size:28px;color:#E8EBF2">{who}</span>
      <span class="label fx" style="--d:{900+t}ms">{ends}</span>
    </div>
    <div class="rail" style="width:1180px">
      <div class="fill grow" style="--d:{500+t}ms;--dur:1500ms;width:62%"></div>
      <div class="stop pop" style="--d:{1900+t}ms;left:62%"></div>
      <div class="node blue" style="top:-8px;left:0;animation:travel 1500ms var(--ease) {500+t}ms forwards,
           drop 1100ms cubic-bezier(.5,0,.75,0) {2000+t}ms forwards;--to:718px"></div>
    </div>
  </div>"""
S.append(("03-ownership", "Problem — nobody owns the transition", 22, "", f"""
<div class="stage">
  <div class="eyebrow fx" style="--d:150ms">The real problem</div>
  <h2 class="fx" style="--d:450ms;margin:24px 0 70px">It isn't that nobody provides care.<br>
    It's that nobody owns the transition.</h2>
  {rails}
  <h2 class="fx" style="--d:9000ms;font-size:46px;color:#AABEF5;max-width:34ch">
    Every system can work exactly as designed — and the patient can still fall through the cracks.</h2>
</div>"""))

S.append(("04-astria", "Astria — logo reveal", 12, "", """
<div class="stage center">
  <div style="position:relative;width:760px">
    <img class="logo" src="../assets/logo-reversed.png" alt=""
         style="width:760px;clip-path:inset(0 100% 0 0);animation:wipe 2200ms var(--ease) 500ms forwards">
    <div class="bloom" style="--d:2500ms;position:absolute;right:92px;top:28px;width:150px;height:150px;
         background:radial-gradient(circle,rgba(232,184,91,.55) 0%,transparent 68%)"></div>
  </div>
  <style>@keyframes wipe{to{clip-path:inset(0 0 0 0)}}</style>
  <div class="sub fx" style="--d:3800ms;margin-top:58px;max-width:40ch;text-align:center">
    A care-navigation platform that makes sure there is continuity of care after release.</div>
</div>"""))

fields = ""
for i, (k, v) in enumerate([("Identity", "Confirmed"), ("Conditions", "3 chronic, 1 substance-use"),
                            ("Medications", "4, with days of supply"), ("Coverage", "Medicaid application assembled"),
                            ("Care pathway", "Primary care + behavioral health"), ("Gaps", "2 flagged for follow-up")]):
    fields += f"""<div class="fx" style="--d:{6200+i*900}ms;display:flex;justify-content:space-between;
      gap:30px;padding:19px 0;border-bottom:1px solid #22314C">
      <span class="label" style="font-size:22px">{k}</span>
      <span style="font-size:23px;font-weight:600;color:#E8EBF2">{v}</span></div>"""
S.append(("05-argo", "Argo — intake", 22, "", f"""
<div class="stage">
  <div class="eyebrow fx" style="--d:150ms">Onboarding</div>
  <h2 class="fx" style="--d:450ms;margin:24px 0 18px">Argo meets facilities where they are</h2>
  <div class="sub fx" style="--d:900ms;max-width:46ch">Fewer than 5% of state corrections departments
    can exchange structured medical data.</div>
  <div style="display:flex;align-items:center;gap:60px;margin-top:62px">
    <div style="display:flex;flex-direction:column;gap:20px;width:400px">
      <div class="chip fx" style="--d:2400ms"><span class="dot"></span>A fax</div>
      <div class="chip fx" style="--d:3100ms"><span class="dot"></span>A scan</div>
      <div class="chip fx" style="--d:3800ms"><span class="dot"></span>A spreadsheet</div>
      <div class="chip fx" style="--d:4500ms"><span class="dot"></span>A discharge record</div>
    </div>
    <svg width="230" height="300" style="overflow:visible">
      <path class="draw" style="--d:5000ms;--len:260;--dur:1400ms" d="M0 150 C 90 150, 120 150, 210 150"
            stroke="#AABEF5" stroke-width="2.4" fill="none"/>
      <circle class="pop" style="--d:6000ms" cx="214" cy="150" r="9" fill="#4776E6"/>
    </svg>
    <div class="card" style="width:720px;padding:34px 40px">
      <div class="label fade" style="--d:5600ms;font-size:20px;letter-spacing:.14em;text-transform:uppercase;
        color:#E8B85B;margin-bottom:8px">Patient record</div>
      {fields}
    </div>
  </div>
</div>"""))

ids = ""
for i, (k, v) in enumerate([("Correctional", "Booking number"), ("Coverage", "Medicaid ID"), ("Clinical", "Clinic record")]):
    ids += f"""<div class="chip fx" style="--d:{900+i*650}ms;justify-content:space-between;width:430px">
      <span style="color:#9AA6BF;font-size:21px">{k}</span><span>{v}</span></div>"""
events = ""
for i, e in enumerate(["Coverage lapses", "Moves county", "Returns to custody"]):
    events += f"""<div class="chip gold fx" style="--d:{8200+i*1500}ms"><span class="dot"></span>{e}</div>"""
S.append(("06-id", "The Astria ID", 18, "", f"""
<div class="stage">
  <div class="eyebrow fx" style="--d:150ms">Continuity</div>
  <h2 class="fx" style="--d:450ms;margin:24px 0 58px">One identifier that survives the gaps</h2>
  <div style="display:flex;align-items:center;gap:70px">
    <div style="display:flex;flex-direction:column;gap:20px">{ids}</div>
    <svg width="220" height="300" style="overflow:visible">
      <path class="draw" style="--d:2900ms;--len:300;--dur:1300ms" d="M0 62 C 110 62, 110 150, 206 150"
            stroke="#AABEF5" stroke-width="2.2" fill="none"/>
      <path class="draw" style="--d:3100ms;--len:240;--dur:1300ms" d="M0 150 L 206 150"
            stroke="#AABEF5" stroke-width="2.2" fill="none"/>
      <path class="draw" style="--d:3300ms;--len:300;--dur:1300ms" d="M0 238 C 110 238, 110 150, 206 150"
            stroke="#AABEF5" stroke-width="2.2" fill="none"/>
    </svg>
    <div class="card pop" style="--d:4400ms;text-align:center;padding:50px 60px;background:#16233A">
      <svg width="52" height="52" class="bloom" style="--d:4900ms;margin:0 auto 16px;display:block">
        <path d="M26 2 L30 20 L48 24 L30 28 L26 46 L22 28 L4 24 L22 20 Z" fill="#E8B85B"/></svg>
      <div class="wordmark" style="font-size:40px">ASTRIA ID</div>
      <div style="font-family:ui-monospace,monospace;font-size:24px;color:#AABEF5;margin-top:12px">AST&ndash;7Q4M&ndash;2XB9</div>
    </div>
  </div>
  <div style="display:flex;gap:24px;margin-top:70px;align-items:center">
    {events}
    <div class="fx" style="--d:12600ms;font-size:27px;font-weight:600;color:#91B5A2;margin-left:16px">
      &rarr;&nbsp; the ID does not change</div>
  </div>
</div>"""))

S.append(("07-evidence", "Evidence — the human model", 14, "", """
<div class="stage">
  <div class="eyebrow fx" style="--d:150ms">The evidence</div>
  <h2 class="fx" style="--d:450ms;margin:24px 0 10px">Intelligent software isn't the full solution</h2>
  <div class="sub fx" style="--d:900ms;max-width:52ch">Adding a community health worker reduced
    emergency-department use — against a group that already had expedited primary care.</div>
  <div style="display:flex;align-items:flex-end;gap:120px;margin-top:70px;height:330px">
    <div style="text-align:center">
      <div class="huge fx" style="--d:2600ms;font-size:118px">39%</div>
      <div class="riseBar" style="--d:2200ms;--dur:1300ms;width:190px;height:230px;background:#2A3A54;
        border-radius:12px 12px 0 0;margin-top:22px"></div>
      <div class="label fade" style="--d:3400ms;margin-top:22px">Without a CHW</div>
    </div>
    <svg width="180" height="80" style="margin-bottom:150px;overflow:visible">
      <path class="draw" style="--d:4400ms;--len:200;--dur:1200ms" d="M0 40 L150 40"
            stroke="#E8B85B" stroke-width="2.6" fill="none"/>
      <path class="pop" style="--d:5400ms" d="M148 32 L168 40 L148 48 Z" fill="#E8B85B"/>
    </svg>
    <div style="text-align:center">
      <div class="huge fx" style="--d:6000ms;font-size:118px;color:#91B5A2">25%</div>
      <div class="riseBar" style="--d:5600ms;--dur:1300ms;width:190px;height:148px;background:#91B5A2;
        border-radius:12px 12px 0 0;margin-top:22px"></div>
      <div class="label fade" style="--d:6800ms;margin-top:22px">With a CHW</div>
    </div>
  </div>
  <div class="tiny fade" style="--d:8400ms;margin-top:54px">Transitions Clinic Network &middot; Wang et al., AJPH, 2012</div>
</div>"""))

LEFT  = ["Behavioral health", "Substance-use treatment", "Housing"]
RIGHT = ["Transportation", "Food access", "Primary care"]
def col(items, side, x0):
    out = ""
    for i, p in enumerate(items):
        d = 6400 + (i * 2 + (0 if side == "l" else 1)) * 520
        out += (f'<div class="chip green fx" style="--d:{d}ms;font-size:23px;padding:16px 26px">'
                f'<span class="dot"></span>{p}</div>')
    return out
links = ""
for i in range(3):
    y = 92 + i * 148
    links += (f'<path class="draw" style="--d:{6200+i*1040}ms;--len:360;--dur:900ms" '
              f'd="M0 {y} C 90 {y}, 110 240, 200 240" stroke="#2E4068" stroke-width="2" fill="none"/>')
    links += (f'<path class="draw" style="--d:{6700+i*1040}ms;--len:360;--dur:900ms" '
              f'd="M560 {y} C 470 {y}, 450 240, 360 240" stroke="#2E4068" stroke-width="2" fill="none"/>')

S.append(("08-promoter", "The Care Promoter", 20, "", f"""
<div class="stage">
  <div class="eyebrow fx" style="--d:150ms">The human model</div>
  <h2 class="fx" style="--d:450ms;margin:24px 0 12px">Every member gets a Care Promoter</h2>
  <div class="sub fx" style="--d:900ms;max-width:52ch">A community health worker who knows each member,
    their care plan, and the realities shaping their health.</div>

  <div style="position:relative;display:flex;align-items:center;justify-content:center;gap:0;
       margin-top:54px;height:520px">
    <div style="display:flex;flex-direction:column;gap:42px;align-items:flex-end;width:430px">
      {col(LEFT,"l",0)}
    </div>

    <svg width="560" height="520" style="overflow:visible;margin:0 10px">
      {links}
    </svg>

    <div style="display:flex;flex-direction:column;gap:42px;align-items:flex-start;width:430px">
      {col(RIGHT,"r",0)}
    </div>

    <div class="pop" style="--d:2600ms;position:absolute;left:50%;top:46%;transform:translate(-50%,-50%);
         text-align:center">
      <div class="card" style="padding:30px 44px;background:#16233A;border:1px solid #2E4068">
        <div style="font-size:29px;font-weight:700;color:#fff;font-family:var(--display)">Care Promoter</div>
        <div class="label" style="font-size:20px;margin-top:6px">knows the member</div>
      </div>
    </div>
    <svg style="position:absolute;left:50%;top:46%;transform:translateX(-50%);width:8px;height:170px;
         overflow:visible;pointer-events:none">
      <path class="draw" style="--d:4200ms;--len:160;--dur:900ms" d="M4 54 L4 150"
            stroke="#2E4068" stroke-width="2" fill="none"/>
    </svg>
    <div class="pop" style="--d:4900ms;position:absolute;left:50%;top:calc(46% + 160px);
         transform:translate(-50%,0)">
      <div class="chip" style="font-size:23px"><span class="dot"></span>Member</div>
    </div>
  </div>
</div>"""))

S.append(("09-network", "Network — not parallel", 14, "light", """
<div class="stage">
  <div class="eyebrow fx" style="--d:150ms">The network</div>
  <h2 class="fx" style="--d:450ms;margin:24px 0 58px">Astria enrolls the partners who are already there</h2>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:26px;max-width:1380px">
    <div class="card fx" style="--d:1200ms"><div style="font-size:30px;font-weight:700">Argo</div>
      <div class="sub" style="font-size:24px;margin-top:10px">handles the administrative burden.</div></div>
    <div class="card fx" style="--d:2400ms"><div style="font-size:30px;font-weight:700">The community network</div>
      <div class="sub" style="font-size:24px;margin-top:10px">gives Care Promoters somewhere to turn.</div></div>
    <div class="card fx" style="--d:3600ms;border-color:#E8B85B"><div style="font-size:30px;font-weight:700">Care Promoters</div>
      <div class="sub" style="font-size:24px;margin-top:10px">make sure members don't get lost between the two.</div></div>
  </div>
  <svg width="1380" height="90" style="margin-top:44px;overflow:visible">
    <path class="draw" style="--d:5000ms;--len:1400;--dur:2000ms"
          d="M230 18 C 460 18, 460 62, 690 62 C 920 62, 920 18, 1150 18"
          stroke="#AABEF5" stroke-width="2.6" fill="none"/>
    <circle class="pop" style="--d:5200ms" cx="230" cy="18" r="9" fill="#4776E6"/>
    <circle class="pop" style="--d:6000ms" cx="690" cy="62" r="9" fill="#4776E6"/>
    <circle class="pop" style="--d:6800ms" cx="1150" cy="18" r="9" fill="#E8B85B"/>
  </svg>
</div>"""))

S.append(("10-implementation", "How it gets implemented", 20, "light", """
<div class="stage">
  <div class="eyebrow fx" style="--d:150ms">Implementation</div>
  <h2 class="fx" style="--d:450ms;margin:24px 0 16px">We start with the programs that already exist</h2>
  <div class="sub fx" style="--d:900ms;max-width:56ch">Our initial customers are established
    transitional-care programs. A pilot gives them an automation and navigation layer.</div>
  <div style="display:flex;gap:28px;margin-top:66px">
    <div class="card fx" style="--d:2600ms;flex:1"><div class="chip gold" style="font-size:20px;padding:10px 18px">
      <span class="dot"></span>Lower</div>
      <div style="font-size:30px;font-weight:700;margin-top:20px">administrative cost</div></div>
    <div class="card fx" style="--d:3800ms;flex:1"><div class="chip gold" style="font-size:20px;padding:10px 18px">
      <span class="dot"></span>Expand</div>
      <div style="font-size:30px;font-weight:700;margin-top:20px">care-coordination capacity</div></div>
    <div class="card fx" style="--d:5000ms;flex:1"><div class="chip gold" style="font-size:20px;padding:10px 18px">
      <span class="dot"></span>Connect</div>
      <div style="font-size:30px;font-weight:700;margin-top:20px">members to community resources</div></div>
  </div>
  <div class="fx" style="--d:9000ms;margin-top:64px;display:flex;align-items:center;gap:32px">
    <div style="font-size:34px;font-weight:700;color:#101B2D">Toward value-based payment</div>
    <svg width="420" height="40" style="overflow:visible">
      <path class="draw" style="--d:9600ms;--len:420;--dur:1600ms" d="M0 20 L380 20"
            stroke="#91B5A2" stroke-width="3" fill="none"/>
      <path class="pop" style="--d:11000ms" d="M378 11 L402 20 L378 29 Z" fill="#91B5A2"/>
    </svg>
    <div class="label" style="font-size:24px">prevention becomes financially sustainable</div>
  </div>
</div>"""))

S.append(("11-outcome", "The pilot outcome", 12, "", """
<div class="stage center">
  <div class="eyebrow fx" style="--d:150ms">Our primary pilot outcome</div>
  <h1 class="fx" style="--d:600ms;margin-top:30px;max-width:22ch">Was someone connected to care
    within 30 days of release?</h1>
  <div style="position:relative;width:1180px;margin-top:88px">
    <div class="rail" style="width:1180px;height:8px">
      <div class="fill grow" style="--d:3000ms;--dur:2400ms;width:100%;background:#4776E6"></div>
    </div>
    <div class="bloom" style="--d:5300ms;position:absolute;right:-26px;top:-28px">
      <svg width="64" height="64"><path d="M32 3 L37 25 L59 30 L37 35 L32 57 L27 35 L5 30 L27 25 Z" fill="#E8B85B"/></svg>
    </div>
    <div class="label fade" style="--d:3200ms;position:absolute;left:0;top:30px">Release</div>
    <div class="label fade" style="--d:5600ms;position:absolute;right:0;top:30px;color:#E8B85B">Day 30 &middot; connected</div>
  </div>
  <div style="display:flex;gap:24px;margin-top:104px">
    <div class="chip fx" style="--d:7000ms"><span class="dot"></span>Medicaid enrollment</div>
    <div class="chip fx" style="--d:7900ms"><span class="dot"></span>Medication access</div>
    <div class="chip fx" style="--d:8800ms"><span class="dot"></span>Completed community referrals</div>
  </div>
</div>"""))

S.append(("12-map", "Proof — North Carolina", 20, "", f"""
<div class="stage">
  <div class="eyebrow fx" style="--d:150ms">Proof of concept</div>
  <h2 class="fx" style="--d:450ms;margin:24px 0 10px">North Carolina is our first market</h2>
  <div class="sub fx" style="--d:900ms;max-width:54ch">We mapped safety-net health infrastructure
    statewide — every federally qualified health center and safety-net hospital.</div>
  <svg viewBox="0 0 {MAP_W} {MAP_H:.0f}" style="width:1500px;margin:38px auto 0;overflow:visible"
       fill="#1E2E49" stroke="#101B2D" stroke-width=".5">
    {counties_svg()}
    <g stroke="none">{anchors_svg()}</g>
  </svg>
  <div style="display:flex;gap:70px;justify-content:center;margin-top:30px">
    <div class="fx" style="--d:1800ms;text-align:center"><div class="huge" style="font-size:72px">288</div>
      <div class="label" style="margin-top:8px">facilities mapped</div></div>
    <div class="fx" style="--d:2300ms;text-align:center"><div class="huge" style="font-size:72px">100</div>
      <div class="label" style="margin-top:8px">counties</div></div>
    <div class="fx" style="--d:4600ms;text-align:center"><div class="huge gold" style="font-size:72px">24</div>
      <div class="label" style="margin-top:8px">anchor sites to reach them all</div></div>
  </div>
</div>"""))

steps = ""
for i, (n, t, s2) in enumerate([("01", "Start with one established network", "where the model already works"),
                                ("02", "Validate in communities with the greatest need", "rural and under-served counties"),
                                ("03", "Expand across North Carolina", "and eventually beyond it")]):
    steps += f"""
  <div class="fx" style="--d:{1400+i*1700}ms;display:flex;gap:34px;align-items:flex-start;max-width:1180px">
    <div class="wordmark" style="font-size:40px;color:#E8B85B;min-width:80px">{n}</div>
    <div><div style="font-size:40px;font-weight:700;color:#fff;font-family:var(--display)">{t}</div>
      <div class="label" style="margin-top:8px">{s2}</div></div>
  </div>"""
S.append(("13-pathway", "The pathway", 16, "", f"""
<div class="stage">
  <div class="eyebrow fx" style="--d:150ms">Our pathway is deliberate</div>
  <div style="display:flex;flex-direction:column;gap:62px;margin-top:62px">{steps}</div>
  <svg width="1180" height="60" style="margin-top:56px;overflow:visible">
    <path class="draw" style="--d:7000ms;--len:1250;--dur:2600ms"
          d="M40 40 C 340 40, 420 14, 620 14 C 840 14, 920 -10, 1130 -10"
          stroke="#AABEF5" stroke-width="2.6" fill="none"/>
    <circle class="pop" style="--d:7200ms" cx="40" cy="40" r="9" fill="#4776E6"/>
    <circle class="pop" style="--d:8400ms" cx="620" cy="14" r="9" fill="#4776E6"/>
    <circle class="bloom" style="--d:9600ms" cx="1130" cy="-10" r="11" fill="#E8B85B"/>
  </svg>
</div>"""))

S.append(("14-close", "Close", 18, "", """
<div class="stage center">
  <svg width="1080" height="260" style="overflow:visible;margin-bottom:10px">
    <path class="draw" style="--d:400ms;--len:1150;--dur:2600ms"
          d="M70 210 L250 158 L430 186 L610 112 L790 140 L930 62"
          stroke="#2E4068" stroke-width="2" fill="none"/>
    <circle class="pop" style="--d:700ms"  cx="70"  cy="210" r="8" fill="#AABEF5"/>
    <circle class="pop" style="--d:1200ms" cx="250" cy="158" r="7" fill="#AABEF5"/>
    <circle class="pop" style="--d:1700ms" cx="430" cy="186" r="7" fill="#AABEF5"/>
    <circle class="pop" style="--d:2200ms" cx="610" cy="112" r="8" fill="#AABEF5"/>
    <circle class="pop" style="--d:2700ms" cx="790" cy="140" r="7" fill="#AABEF5"/>
    <g class="bloom" style="--d:3200ms">
      <path d="M930 22 L943 54 L975 62 L943 70 L930 102 L917 70 L885 62 L917 54 Z" fill="#E8B85B"/></g>
  </svg>
  <div class="sub fade" style="--d:4200ms;max-width:58ch;text-align:center;font-size:27px">
    Astraea is a constellation associated with balance and justice — a reminder that where someone has
    been should not determine whether they receive care.</div>
  <h1 class="fx" style="--d:8000ms;margin-top:70px;max-width:24ch">Leaving incarceration should
    never mean leaving care.</h1>
  <img class="fade" src="../assets/logo-reversed.png" alt="Astria"
       style="--d:11000ms;width:360px;margin-top:76px">
</div>"""))

# ---------------------------------------------------------------- emit
PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{label} — Astria</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="../shared.css">
<meta name="duration" content="{secs}">
<script>if(location.search.indexOf("snap")>-1)document.documentElement.className="snap";</script>
</head><body class="{cls}">
{html}
</body></html>
"""

def build():
    os.makedirs(os.path.join(HERE, "scenes"), exist_ok=True)
    for sid, label, secs, cls, html in S:
        with open(os.path.join(HERE, "scenes", sid + ".html"), "w") as f:
            f.write(PAGE.format(label=label, secs=secs, cls=cls, html=html))
        print(f"  scenes/{sid}.html   {secs:>2}s   {label}")

    total = sum(s[2] for s in S)
    # preview player
    rows = "".join(
        f'<button data-s="{sid}" data-d="{secs}"><b>{i+1:02d}</b> {label}'
        f'<span>{secs}s</span></button>' for i, (sid, label, secs, _, _) in enumerate(S))
    with open(os.path.join(HERE, "index.html"), "w") as f:
        f.write(PLAYER.format(rows=rows, total=f"{total//60}:{total%60:02d}",
                              first=S[0][0], n=len(S)))
    # record script
    lines = ["#!/usr/bin/env bash",
             "# Render every scene to MP4 with htmlrec (npm i -g htmlrec).",
             "# Run from this folder:  bash record.sh",
             "set -euo pipefail",
             'cd "$(dirname "$0")"',
             "mkdir -p out", ""]
    for sid, label, secs, _, _ in S:
        lines.append(f'echo "→ {sid} ({secs}s)"')
        lines.append(f'hrec render scenes/{sid}.html -o out/{sid}.mp4 '
                     f'-d {secs} -f 60 --width 1920 --height 1080')
    lines += ["", 'echo "Done. MP4s are in ./out"']
    p = os.path.join(HERE, "record.sh")
    with open(p, "w") as f: f.write("\n".join(lines) + "\n")
    os.chmod(p, 0o755)
    print(f"\n  index.html   preview player")
    print(f"  record.sh    htmlrec batch ({len(S)} scenes, {total//60}:{total%60:02d} total)")

PLAYER = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Astria — pitch video scenes</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Inter:wght@400;500;600&display=swap">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0B1322;color:#E8EBF2;font-family:Inter,sans-serif;display:grid;
  grid-template-columns:330px 1fr;height:100vh;overflow:hidden}}
aside{{background:#101B2D;border-right:1px solid #1E2E49;overflow-y:auto;padding:22px 16px}}
h1{{font-family:Manrope;font-size:16px;letter-spacing:.2em;margin:4px 10px 4px;color:#fff}}
.meta{{font-size:12px;color:#6E7C99;margin:0 10px 18px}}
button{{display:flex;align-items:center;gap:10px;width:100%;background:none;border:0;color:#9AA6BF;
  font:inherit;font-size:13.5px;text-align:left;padding:11px 12px;border-radius:9px;cursor:pointer}}
button b{{font-family:Manrope;color:#4D6490;font-size:12px}}
button span{{margin-left:auto;font-size:11.5px;color:#4D6490}}
button:hover{{background:#16233A;color:#fff}}
button[aria-current]{{background:#16233A;color:#fff}}
button[aria-current] b{{color:#E8B85B}}
main{{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;padding:22px}}
.frame{{width:min(100%,1280px);aspect-ratio:16/9;border-radius:12px;overflow:hidden;
  box-shadow:0 30px 80px -40px #000;background:#101B2D}}
iframe{{width:1920px;height:1080px;border:0;transform-origin:top left}}
.bar{{display:flex;align-items:center;gap:14px;font-size:13px;color:#6E7C99}}
.bar button{{width:auto;background:#1B2A42;color:#E8EBF2;padding:8px 16px;border-radius:9px}}
.prog{{width:320px;height:4px;background:#1E2E49;border-radius:3px;overflow:hidden}}
.prog i{{display:block;height:100%;background:#4776E6;width:0}}
</style></head><body>
<aside>
  <h1>ASTRIA</h1><p class="meta">{n} scenes · {total} total</p>
  {rows}
</aside>
<main>
  <div class="frame"><iframe id="f" src="scenes/{first}.html"></iframe></div>
  <div class="bar">
    <button id="replay">Replay</button>
    <div class="prog"><i id="p"></i></div>
    <span id="t">0.0s</span>
  </div>
</main>
<script>
var f=document.getElementById('f'), prog=document.getElementById('p'), tt=document.getElementById('t');
var cur=null, dur=0, t0=0, raf;
function fit(){{var w=f.parentElement.clientWidth; f.style.transform='scale('+(w/1920)+')';}}
addEventListener('resize',fit); fit();
function tick(){{
  var e=(performance.now()-t0)/1000;
  prog.style.width=Math.min(100,e/dur*100)+'%';
  tt.textContent=e.toFixed(1)+'s / '+dur+'s';
  if(e<dur+0.4) raf=requestAnimationFrame(tick);
}}
function play(btn){{
  document.querySelectorAll('aside button').forEach(function(b){{b.removeAttribute('aria-current');}});
  btn.setAttribute('aria-current','true');
  cur=btn.dataset.s; dur=+btn.dataset.d;
  f.src='scenes/'+cur+'.html?'+Date.now();
  cancelAnimationFrame(raf); t0=performance.now(); tick(); fit();
}}
document.querySelectorAll('aside button').forEach(function(b){{
  b.addEventListener('click',function(){{play(b);}});
}});
document.getElementById('replay').addEventListener('click',function(){{
  var b=document.querySelector('aside button[aria-current]')||document.querySelector('aside button');
  play(b);
}});
play(document.querySelector('aside button'));
</script></body></html>
"""

if __name__ == "__main__":
    build()
