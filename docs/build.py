#!/usr/bin/env python3
"""
Astria site builder.
Writes plain static HTML into this folder. No dependencies, no build chain —
run `python3 build.py` and push. Edit the PAGES dict below, not the output.
"""
import os, json, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))

NAV = [
    ("index.html",          "Home"),
    ("how-it-works.html",   "How it works"),
    ("argo.html",           "Argo"),
    ("astria-id.html",      "Astria ID"),
    ("care-promoter.html",  "Care team"),
    ("network.html",        "Network"),
    ("coverage.html",       "Coverage"),
    ("financing.html",      "Financing"),
    ("implementation.html", "Rollout"),
    ("team.html",           "Team"),
]

def mark(on_dark=False):
    """Brand logo lockup: icon PNG + wordmark set in Knockout Sumo."""
    src = "assets/img/logo-icon-light.png" if on_dark else "assets/img/logo-icon.png"
    cls = " on-dark" if on_dark else ""
    return (f'<img class="mark" src="{src}" alt="">'
            f'<span class="wordmark{cls}">ASTRIA</span>')

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Astria</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600;650;700&display=swap">
<link rel="stylesheet" href="assets/astria.css">
</head>
<body>

<header class="masthead">
  <div class="wrap">
    <a class="brand" href="index.html">{mark}</a>
    <nav class="primary" aria-label="Primary">{nav}</nav>
  </div>
</header>

{body}

<footer class="site">
  <div class="wrap">
    <div class="cols">
      <div>
        <div class="footer-lockup">
          <img class="mark" src="assets/img/logo-icon-light.png" alt="">
          <span class="wordmark on-dark">ASTRIA</span>
        </div>
        <p style="margin-top:14px;max-width:40ch">Every point of care. One path forward.</p>
        <p class="caption" style="color:#6E7C99">Intelligent chronic-care navigation and reentry health infrastructure.</p>
      </div>
      <div>
        <h4>Platform</h4>
        <a href="how-it-works.html">How it works</a>
        <a href="argo.html">Argo — onboarding</a>
        <a href="astria-id.html">The Astria ID</a>
        <a href="care-promoter.html">Care Promoters</a>
        <a href="network.html">Community network</a>
      </div>
      <div>
        <h4>Operating model</h4>
        <a href="coverage.html">Coverage analysis</a>
        <a href="financing.html">Financing</a>
        <a href="implementation.html">Rollout</a>
        <a href="team.html">Team</a>
      </div>
    </div>
    <p class="fine">Working draft, built by a student team at the University of North Carolina. Figures are sourced
    on the page where they appear. Coverage analysis is our own, derived from the NC DSH &amp; FQHC Locations 2022
    workbook and US Census county geography; distances are straight-line county-centroid and should be read as a
    floor, not drive time. Astria is not yet a deployed service.</p>
  </div>
</footer>

{scripts}
</body>
</html>
"""

def nav_html(current):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        out.append(f'<a href="{href}"{cur}>{label}</a>')
    return "".join(out)

def pagenav(prev, nxt):
    def blk(item, lbl):
        if not item: return '<span></span>'
        href, title = item
        return f'<a href="{href}"><div class="lbl">{lbl}</div><div class="t">{title}</div></a>'
    return f'<section class="tight"><div class="wrap"><div class="pagenav">{blk(prev,"Previous")}{blk(nxt,"Next")}</div></div></section>'

# ===========================================================================
PAGES = {}

# --------------------------------------------------------------- INDEX
PAGES["index.html"] = dict(
title="Every point of care. One path forward.",
desc="Astria is a care-navigation platform that follows people across the boundaries between corrections, coverage, and community care.",
body=f"""
<div class="hero">
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <div class="tagline">Every point of care. One path forward.</div>
        <h1>Leaving incarceration should never mean leaving care.</h1>
        <p class="lede">Astria is a care-navigation platform that follows a person across the boundaries
        between corrections, coverage, and community care — and keeps checking that someone is still
        holding on.</p>
        <div class="btn-row">
          <a class="btn" href="how-it-works.html">See how it works</a>
          <a class="btn ghost" href="coverage.html">Read the coverage analysis</a>
        </div>
      </div>
      <div>
        <img src="assets/img/logo-reversed.png" alt="Astria — a continuous path through waypoints to a north star" class="hero-lockup">
      </div>
    </div>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">The problem</span>
      <h2>The resources exist. The system doesn't.</h2>
      <p class="lede">Primary care, behavioral health, medication, housing, transport — all of it is already
      there. Nothing connects it across the moment of release.</p>
    </div>
    <div class="grid g3">
      <div class="stat">
        <div class="v mono-num">12.7&times;</div>
        <div class="k">higher risk of death in the first two weeks after release, compared with the general population</div>
        <div class="src">Binswanger et al., <em>NEJM</em>, 2007</div>
      </div>
      <div class="stat">
        <div class="v mono-num">80%</div>
        <div class="k">of people leaving incarceration have a chronic medical, psychiatric, or substance-use condition</div>
        <div class="src">ASPE Report to Congress, 2023</div>
      </div>
      <div class="stat">
        <div class="v mono-num">7.9M</div>
        <div class="k">jail admissions in a single year — every one of them eventually a release</div>
        <div class="src">Bureau of Justice Statistics, 2024</div>
      </div>
    </div>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow on-dark">Why it keeps happening</span>
      <h2>Nobody owns the transition</h2>
    </div>
    <div class="grid g3">
      <div class="card dark"><h3>A jail's responsibility</h3><p>ends at release.</p></div>
      <div class="card dark"><h3>A health plan's</h3><p>can end at disenrollment.</p></div>
      <div class="card dark"><h3>A clinic loses someone</h3><p>when they disappear from its panel.</p></div>
    </div>
    <p class="lede" style="margin-top:28px;max-width:72ch;color:#C6D0E4">Every system can work exactly as
    designed — and the patient can still fall through the middle.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">The platform</span>
      <h2>Four pieces, one path</h2>
    </div>
    <div class="grid g2">
      <a class="card" href="argo.html" style="text-decoration:none;color:inherit">
        <div class="pill blue" style="margin-bottom:12px">Onboarding</div>
        <h3>Argo</h3>
        <p>An AI system with a human in the loop. Give it a fax, a scan, a spreadsheet — it extracts what
        matters, assembles the Medicaid application, and produces a usable starting record.</p>
      </a>
      <a class="card" href="astria-id.html" style="text-decoration:none;color:inherit">
        <div class="pill blue" style="margin-bottom:12px">Continuity</div>
        <h3>The Astria ID</h3>
        <p>An encrypted identifier that resolves a booking number, a Medicaid ID, and clinic records back to
        the same person — so losing coverage or returning to custody doesn't mean starting over.</p>
      </a>
      <a class="card" href="care-promoter.html" style="text-decoration:none;color:inherit">
        <div class="pill green" style="margin-bottom:12px">The human</div>
        <h3>Care Promoters</h3>
        <p>A community health worker who knows a member's name, their plan, and what happened last week.
        Software isn't the intervention — the relationship is.</p>
      </a>
      <a class="card" href="network.html" style="text-decoration:none;color:inherit">
        <div class="pill green" style="margin-bottom:12px">The network</div>
        <h3>Community network</h3>
        <p>We don't build a parallel system. Astria connects the primary care, behavioral health, housing,
        transport and referral infrastructure already doing this work.</p>
      </a>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Proof of concept</span>
      <h2>We mapped North Carolina</h2>
      <p class="lede">Every federally qualified health center and safety-net hospital in the state, joined to
      county geography and population.</p>
    </div>
    <div class="grid g4">
      <div class="stat"><div class="v mono-num">288</div><div class="k">facilities mapped statewide</div></div>
      <div class="stat"><div class="v mono-num">18</div><div class="k">counties with no FQHC</div></div>
      <div class="stat"><div class="v mono-num">6</div><div class="k">counties with neither an FQHC nor a safety-net hospital</div></div>
      <div class="stat accent"><div class="v mono-num">24</div><div class="k">anchor sites would put all 100 counties within a 35-mile radius</div></div>
    </div>
    <div class="btn-row"><a class="btn" href="coverage.html">Explore the map</a></div>
  </div>
</section>
""",
scripts="")

# --------------------------------------------------------------- HOW IT WORKS
PAGES["how-it-works.html"] = dict(
title="How it works",
desc="From ninety days before release to a year after — who does what, and when.",
body="""
<section>
  <div class="wrap">
    <span class="eyebrow">How it works</span>
    <h1>From ninety days before release to a year after</h1>
    <p class="lede" style="margin-top:18px">Three stages. The balance of software and human effort shifts
    deliberately as you move through them — automated at the front, human at the back.</p>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="grid g3">
      <div class="card">
        <div class="pill blue" style="margin-bottom:12px">Mostly automated</div>
        <h3>1 &middot; Onboard</h3>
        <p>The facility uploads whatever it has. Argo extracts it, assigns an Astria ID, resolves coverage,
        and produces a usable record — even an incomplete one.</p>
      </div>
      <div class="card">
        <div class="pill blue" style="margin-bottom:12px">Assisted matching</div>
        <h3>2 &middot; Assemble</h3>
        <p>Match to a clinic that takes Medicaid and takes this population, plus behavioral health where
        indicated. Where a county has nothing, we record the gap rather than hide it.</p>
      </div>
      <div class="card">
        <div class="pill green" style="margin-bottom:12px">Human, supported</div>
        <h3>3 &middot; Hold on</h3>
        <p>A Care Promoter makes contact and keeps it. The schedule relaxes as the connection proves durable
        and tightens the moment a signal breaks.</p>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">The journey</span>
      <h2>One person, step by step</h2>
    </div>
    <div class="rail">
      <div class="pt done"><div class="when">Day &minus;90 to &minus;14</div><h4>Enrollment begins inside the facility</h4>
        <p>A reentry coordinator or jail health nurse uploads what exists. Argo extracts conditions, medications
        and days of supply, release date and contacts. Missing fields become tasks with an owner, not blanks.</p></div>
      <div class="pt done"><div class="when">Day &minus;90 to &minus;14</div><h4>Coverage resolved</h4>
        <p>Medicaid status checked; where coverage is inactive, Argo assembles the application so a certified
        assister can submit it. The goal is coverage active on release day.</p></div>
      <div class="pt done"><div class="when">Day &minus;14</div><h4>A care team is assembled</h4>
        <p>A clinic of record accepts the referral and puts the person on a panel. Behavioral health or
        substance-use treatment is added where clinically indicated.</p></div>
      <div class="pt active"><div class="when">Day 0 &middot; release</div><h4>A Care Promoter makes contact</h4>
        <p>In person where we have local staff, by phone or video where we don't. A working phone number and a
        backup contact are confirmed — the two things most likely to break in month one.</p></div>
      <div class="pt"><div class="when">Day 1&ndash;30</div><h4>Weekly contact</h4>
        <p>First community visit inside thirty days. Medications reconciled and continued before the release
        supply runs out.</p></div>
      <div class="pt"><div class="when">Month 2&ndash;6</div><h4>Monthly, as things hold</h4>
        <p>Cadence relaxes once prescriptions are filling, visits are happening, and the clinic confirms the
        person is on its panel.</p></div>
      <div class="pt"><div class="when">Month 7&ndash;12</div><h4>Quarterly &mdash; and quiet</h4>
        <p>The goal is an ordinary established patient: named care team, active coverage, seen within the year.
        Graduation, not permanent membership.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">The checking</span>
      <h2>Silence is the trigger</h2>
      <p class="lede">Most care systems react to events. The people who fall out of care stop generating
      events — that is what falling out means. So the check runs top-down, and only absence escalates.</p>
    </div>
    <div class="steps">
      <div class="step"><div><h4>Data we already have</h4>
        <p>Prescription filled, visit attended, coverage still active. Nobody is contacted at all.</p></div></div>
      <div class="step"><div><h4>Ask the clinic</h4>
        <p>One click to confirm the person is on the panel and was seen. About five seconds of someone's time.</p></div></div>
      <div class="step"><div><h4>Text the member</h4>
        <p>A plain SMS from their Care Promoter. No app, no password, works on a borrowed phone.</p></div></div>
      <div class="step"><div><h4>A task for a human</h4>
        <p>If nothing has come back, it becomes a task that week — with everything already assembled.</p></div></div>
    </div>
    <div class="note" style="margin-top:26px">
      <strong>An open question we take seriously</strong>
      <p>A tapering schedule needs a floor — a minimum contact frequency no confidence score can drop below.
      Setting that floor, and naming who is accountable when it fails, is a design decision we are working
      through with practitioners rather than assuming.</p>
    </div>
  </div>
</section>
""",
scripts="")

# --------------------------------------------------------------- ARGO
PAGES["argo.html"] = dict(
title="Argo — onboarding",
desc="Argo turns a fax, a scan or a spreadsheet into a usable care record, and assembles the Medicaid application.",
body="""
<section>
  <div class="wrap">
    <span class="eyebrow">Onboarding</span>
    <h1>Argo meets facilities where they are</h1>
    <p class="lede" style="margin-top:18px">Fewer than five percent of state corrections departments can
    exchange structured medical data. So Astria does not require interoperability that does not exist.
    Give Argo whatever the facility actually has.</p>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="demo">
      <div class="demo-bar">
        <span class="dot"></span><span class="title">Argo &mdash; intake</span>
        <span class="right"><span class="pill blue" id="argo-state">Awaiting upload</span></span>
      </div>
      <div class="demo-body">
        <div class="grid g2" style="gap:26px">
          <div>
            <div class="caption" style="margin-bottom:10px">What the facility sent</div>
            <div class="filecard">
              <span class="ico"></span>
              <span>
                <span class="nm">alamance_release_packet.pdf</span>
                <span class="mt">Scanned fax &middot; 6 pages &middot; mixed handwriting</span>
              </span>
            </div>
            <div class="btn-row" style="margin-top:18px">
              <button class="btn" id="argo-run">Process with Argo</button>
              <button class="btn ghost" id="argo-reset">Reset</button>
            </div>
            <p class="caption" style="margin-top:16px">Illustrative demo with sample data. No real patient
            information is used anywhere on this site.</p>
          </div>
          <div>
            <div class="caption" style="margin-bottom:10px">Structured record</div>
            <div id="argo-fields">
              <div class="field" data-f><span class="k">Name</span><span class="v pending">&mdash;</span></div>
              <div class="field" data-f><span class="k">Release date</span><span class="v pending">&mdash;</span></div>
              <div class="field" data-f><span class="k">Conditions</span><span class="v pending">&mdash;</span></div>
              <div class="field" data-f><span class="k">Medications</span><span class="v pending">&mdash;</span></div>
              <div class="field" data-f><span class="k">Days of supply</span><span class="v pending">&mdash;</span></div>
              <div class="field" data-f><span class="k">Coverage</span><span class="v pending">&mdash;</span></div>
              <div class="field" data-f><span class="k">Contact</span><span class="v pending">&mdash;</span></div>
              <div class="field" data-f><span class="k">Discharge summary</span><span class="v pending">&mdash;</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">What Argo does</span>
      <h2>Four moves, in order</h2>
    </div>
    <div class="steps">
      <div class="step"><div><h4>Any format in</h4>
        <p>A fax, a scan, a spreadsheet, a discharge record. No schema, no integration, no minimum quality bar.</p></div></div>
      <div class="step"><div><h4>Extract to structure</h4>
        <p>Conditions, medications with days of supply, release date, contacts. Every extracted field keeps a
        link back to the page it came from, so a clinician can check the source.</p></div></div>
      <div class="step"><div><h4>Assemble coverage</h4>
        <p>Argo verifies Medicaid status or assembles the application so a certified assister can submit it.
        Astria does not submit applications itself — assisting with enrolment is a regulated role.</p></div></div>
      <div class="step done"><div><h4>Name the gaps</h4>
        <p>Missing discharge summary, no contact number, release date unconfirmed. Each becomes a chase task
        with an owner, rather than an empty field somebody discovers later.</p></div></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="grid g2" style="gap:24px">
      <div class="card">
        <h3>Why this matters commercially</h3>
        <p>A Michigan state analysis found community health workers spend <strong>8.7 hours a week</strong>
        tracking down resources and making referrals — separate from the 18.5 hours they spend with clients.
        Across a caseload of twenty-five, that is roughly eighteen hours per client per year on coordination
        before any care is delivered.</p>
        <p class="caption">Michigan DHHS / MiCHWA Community Health Worker Caseload Analysis, 2023.</p>
      </div>
      <div class="card">
        <h3>What Argo does not do</h3>
        <p>It does not contact members directly, make clinical decisions, or appear as a person. It reduces
        the administrative load — it does not absorb it. Somebody still has to call the housing program and
        ask whether there is a bed.</p>
        <p>Every message that reaches a member is sent by a named human who can be reached back.</p>
      </div>
    </div>
  </div>
</section>
""",
scripts="""<script>
(function(){
  var DATA=[["Name","James T. (sample)"],["Release date","22 September &middot; confirmed"],
    ["Conditions","Hypertension, type 2 diabetes, opioid use disorder"],
    ["Medications","Buprenorphine/naloxone, lisinopril, metformin"],
    ["Days of supply","30 days issued at release"],
    ["Coverage","Medicaid inactive &mdash; application assembled","flag"],
    ["Contact","(336) 555&ndash;0148 &middot; backup contact captured"],
    ["Discharge summary","Not provided &mdash; chase task created","flag"]];
  var rows=document.querySelectorAll('#argo-fields [data-f]');
  var state=document.getElementById('argo-state');
  var t=[];
  function reset(){
    t.forEach(clearTimeout); t=[];
    rows.forEach(function(r){ var v=r.querySelector('.v'); v.className='v pending'; v.innerHTML='&mdash;'; });
    state.textContent='Awaiting upload'; state.className='pill blue';
  }
  document.getElementById('argo-reset').addEventListener('click',reset);
  document.getElementById('argo-run').addEventListener('click',function(){
    reset();
    state.textContent='Reading 6 pages\\u2026'; state.className='pill gold';
    DATA.forEach(function(d,i){
      t.push(setTimeout(function(){
        var v=rows[i].querySelector('.v');
        v.className='v'+(d[2]?' '+d[2]:''); v.innerHTML=d[1];
        if(i===DATA.length-1){ state.textContent='Record ready \\u00b7 2 gaps flagged'; state.className='pill green'; }
      }, 420+i*260));
    });
  });
})();
</script>""")

# --------------------------------------------------------------- ASTRIA ID
PAGES["astria-id.html"] = dict(
title="The Astria ID",
desc="An encrypted identifier that resolves a booking number, a Medicaid ID and clinic records to the same person.",
body="""
<section>
  <div class="wrap">
    <span class="eyebrow">Continuity</span>
    <h1>One identifier that survives the gaps</h1>
    <p class="lede" style="margin-top:18px">People who cycle between custody, coverage and community care
    acquire a new identifier at every door. The Astria ID is the key that resolves them back to the same
    human being.</p>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="demo">
      <div class="demo-bar">
        <span class="dot gold"></span><span class="title">Astria ID &mdash; continuity across events</span>
        <span class="right"><span class="pill" id="id-ctx">Baseline</span></span>
      </div>
      <div class="demo-body">
        <div class="ctrl" style="margin-bottom:22px">
          <label>Simulate an event:</label>
          <div class="seg" id="id-seg">
            <button data-e="0" aria-pressed="true">Baseline</button>
            <button data-e="1" aria-pressed="false">Loses coverage</button>
            <button data-e="2" aria-pressed="false">Moves county</button>
            <button data-e="3" aria-pressed="false">Returns to custody</button>
          </div>
        </div>
        <div class="grid g2" style="gap:26px">
          <div>
            <div class="caption" style="margin-bottom:10px">Institutional identifiers</div>
            <div id="id-list">
              <div class="field"><span class="k">Booking number</span><span class="v" data-i="0">AL-2291847</span></div>
              <div class="field"><span class="k">Medicaid ID</span><span class="v" data-i="1">NC 9042118833</span></div>
              <div class="field"><span class="k">Clinic MRN</span><span class="v" data-i="2">PHS-004512</span></div>
              <div class="field"><span class="k">Pharmacy record</span><span class="v" data-i="3">GW-88107</span></div>
            </div>
          </div>
          <div>
            <div class="card dark" style="text-align:center;padding:30px 26px">
              <svg viewBox="0 0 34 34" style="width:30px;height:30px;margin:0 auto 10px;display:block" aria-hidden="true">
                <path d="M17 2 L19 12 L29 14 L19 16 L17 26 L15 16 L5 14 L15 12 Z" fill="#E8B85B"/>
              </svg>
              <div style="font-family:var(--display);font-weight:800;letter-spacing:.14em;font-size:19px;color:#fff">ASTRIA ID</div>
              <div class="mono-num" style="font-size:14px;color:#AABEF5;margin-top:6px">AST&ndash;7Q4M&ndash;2XB9</div>
              <p style="font-size:13.5px;margin-top:14px;color:#9AA6BF">Unchanged across every event on the
              left. Encrypted, internal, and never visible to corrections, courts, probation or parole.</p>
            </div>
            <div class="callout gold" style="margin-top:18px">
              <p id="id-msg" style="font-size:15px">All four identifiers currently resolve to one person and one
              continuous record.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="grid g2" style="gap:24px">
      <div class="card" style="border-color:var(--celestial)">
        <h3 style="color:var(--celestial-dk)">What it is</h3>
        <ul class="small" style="margin:12px 0 0;padding-left:20px;line-height:1.9">
          <li>A private, commercial, system-level identifier, encrypted at rest and in transit</li>
          <li>A resolver: the same person across a booking number, a Medicaid ID, and clinic records</li>
          <li>The mechanism that lets a record survive reincarceration, relocation, or a coverage lapse</li>
          <li>Queryable only by organisations the member has consented to</li>
        </ul>
      </div>
      <div class="card" style="border-color:#D8A99A">
        <h3 style="color:#A8512F">What it is not</h3>
        <ul class="small" style="margin:12px 0 0;padding-left:20px;line-height:1.9">
          <li>Not a personal health record, and not a replacement for an EHR</li>
          <li>Not a government identifier &mdash; federal appropriations language has blocked HHS from issuing one since 1999</li>
          <li>Not visible or useful to corrections, courts, probation or parole</li>
          <li>Not a score, a risk tier, or anything that ranks a person</li>
        </ul>
      </div>
    </div>
    <div class="note" style="margin-top:26px">
      <strong>A design constraint we hold to</strong>
      <p>For someone who has just left custody, a permanent identifier that follows you is the precise shape
      of the thing they have reason to fear. The same object reads as infrastructure or as surveillance
      depending entirely on who can query it and who controls consent. If we cannot explain that difference
      to a member in one sentence, we have designed it wrong.</p>
    </div>
  </div>
</section>
""",
scripts="""<script>
(function(){
  var EV=[
    {ctx:"Baseline", cls:"pill",
     vals:["AL-2291847","NC 9042118833","PHS-004512","GW-88107"], dim:[],
     msg:"All four identifiers currently resolve to one person and one continuous record."},
    {ctx:"Coverage lapsed", cls:"pill gold",
     vals:["AL-2291847","Inactive at redetermination","PHS-004512","GW-88107"], dim:[1],
     msg:"Coverage lapsed at redetermination. The Astria ID is unchanged, so the care team sees it the week it happens rather than at the pharmacy counter."},
    {ctx:"Moved county", cls:"pill gold",
     vals:["AL-2291847","NC 9042118833","New MRN at receiving clinic","New pharmacy record"], dim:[2,3],
     msg:"New county, new clinic, new pharmacy &mdash; two new institutional identifiers. The Astria ID resolves them to the same person, so the history travels."},
    {ctx:"Returned to custody", cls:"pill gold",
     vals:["New booking number","Suspended during custody","PHS-004512","GW-88107"], dim:[0,1],
     msg:"A new booking number and suspended coverage. Intake starts from the real history instead of from zero &mdash; which is the single largest source of avoidable harm in this population."}
  ];
  var vals=document.querySelectorAll('#id-list .v');
  var ctx=document.getElementById('id-ctx'), msg=document.getElementById('id-msg');
  function render(i){
    var e=EV[i];
    vals.forEach(function(v,k){
      v.innerHTML=e.vals[k];
      v.className='v'+(e.dim.indexOf(k)>-1?' flag':'');
    });
    ctx.textContent=e.ctx; ctx.className=e.cls; msg.innerHTML=e.msg;
  }
  document.getElementById('id-seg').addEventListener('click',function(ev){
    var b=ev.target.closest('[data-e]'); if(!b) return;
    this.querySelectorAll('[data-e]').forEach(function(x){x.setAttribute('aria-pressed','false');});
    b.setAttribute('aria-pressed','true'); render(+b.dataset.e);
  });
})();
</script>""")

# --------------------------------------------------------------- CARE PROMOTER
PAGES["care-promoter.html"] = dict(
title="Care Promoters",
desc="A community health worker who knows a member's name, their plan, and what happened last week.",
body="""
<section>
  <div class="wrap">
    <span class="eyebrow">The human model</span>
    <h1>Software isn't the intervention</h1>
    <p class="lede" style="margin-top:18px">The Transitions Clinic Network found that adding a community
    health worker to a primary care team reduced emergency-department use from 39.2% to 25.5% &mdash; measured
    against a comparison group that already received expedited primary care. Access was not the constraint.
    The relationship was.</p>
    <p class="caption">Wang et al., <em>American Journal of Public Health</em>, 2012.</p>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="grid g2" style="gap:24px;align-items:start">
      <div class="card" style="padding:0;overflow:hidden">
        <div class="demo-bar"><span class="dot g"></span><span class="title">Today &mdash; Marcus R., Care Promoter</span>
          <span class="right"><span class="pill green">18 members</span></span></div>
        <div class="worklist">
          <div class="wl urgent"><span class="av gold">JT</span>
            <span><span class="nm">James T.</span><span class="why">Day 3 &middot; no first visit booked</span></span>
            <span class="pill gold">Today</span></div>
          <div class="wl urgent"><span class="av gold">MB</span>
            <span><span class="nm">Michael B.</span><span class="why">Medication runs out Saturday</span></span>
            <span class="pill gold">3 days</span></div>
          <div class="wl"><span class="av">TJ</span>
            <span><span class="nm">Tanya J.</span><span class="why">Releases Saturday &middot; handoff incomplete</span></span>
            <span class="pill blue">Prep</span></div>
          <div class="wl"><span class="av g">DW</span>
            <span><span class="nm">Derrick W.</span><span class="why">Day 12 &middot; first visit completed</span></span>
            <span class="pill green">On track</span></div>
          <div class="wl"><span class="av g">RC</span>
            <span><span class="nm">Rosa C.</span><span class="why">Day 8 &middot; behavioral health intake Friday</span></span>
            <span class="pill green">On track</span></div>
        </div>
      </div>
      <div>
        <h3>Ordered by risk, not by date</h3>
        <p>A Care Promoter opens a list sorted by who is closest to falling out of care. Argo has already done
        the documents, the matching and the notes, so her time goes to the person rather than the paperwork.</p>
        <h3 style="margin-top:26px">Hired from the population served</h3>
        <p>Where we can, Care Promoters have lived experience of incarceration. This is the design feature with
        the strongest evidence behind it, and the one we are least willing to compromise.</p>
        <h3 style="margin-top:26px">Reachable where there is no local programme</h3>
        <p>In person where we have staff on the ground; by phone or video where we don't. Eighteen North
        Carolina counties have no federally qualified health center &mdash; a remote Care Promoter is often the
        difference between a programme existing and not.</p>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Cadence</span>
      <h2>The schedule relaxes. It doesn't end.</h2>
      <p class="lede">Contact frequency is set by signals, not by self-report: prescriptions filled, visits
      attended, coverage active, and whether the clinic confirms the member is on its panel.</p>
    </div>
    <div class="cadence">
      <div class="cad"><div class="dots"><i style="height:26px"></i><i style="height:26px"></i><i style="height:26px"></i><i style="height:26px"></i></div>
        <h4>Week 1&ndash;4</h4><p>Weekly. Fresh out, and the overdose-risk window is open.</p></div>
      <div class="cad"><div class="dots"><i style="height:19px"></i><i style="height:19px"></i></div>
        <h4>Month 2&ndash;6</h4><p>Monthly. Filling prescriptions, attending visits, answering texts.</p></div>
      <div class="cad"><div class="dots"><i style="height:12px"></i></div>
        <h4>Month 7&ndash;12</h4><p>Quarterly. An established patient. We get quiet on purpose.</p></div>
      <div class="cad alert"><div class="dots"><i style="height:26px"></i><i style="height:26px"></i><i style="height:26px"></i><i style="height:26px"></i></div>
        <h4>A signal breaks</h4><p>Missed refill, ED admission, bounced text, redetermination approaching &mdash; back to weekly.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="grid g2" style="gap:24px">
      <div class="callout">
        <h3>What AI does</h3>
        <p class="small" style="margin-top:10px">Watches the data and decides what matters today. Drafts the
        message at the right reading level. Fills the forms and writes the encounter note. Prioritises a
        caseload.</p>
      </div>
      <div class="callout" style="border-left-color:#C9705A">
        <h3>What AI never does</h3>
        <p class="small" style="margin-top:10px">Appear as a person, or sign as one. Originate the
        relationship. Make a clinical decision. Score a person as a risk. Send anything nobody is accountable
        for.</p>
      </div>
    </div>
    <p class="lede" style="margin-top:26px;max-width:74ch">The scarce resource is a Care Promoter's attention,
    not her typing. Automation is there to buy attention back so the real connection happens more often &mdash;
    not fewer times.</p>
  </div>
</section>
""",
scripts="")

# --------------------------------------------------------------- NETWORK
PAGES["network.html"] = dict(
title="Community network",
desc="Astria connects the primary care, behavioral health, housing, transport and referral infrastructure already doing this work.",
body="""
<section>
  <div class="wrap">
    <span class="eyebrow">The network</span>
    <h1>Astria doesn't build a parallel system</h1>
    <p class="lede" style="margin-top:18px">Reentry is never one problem. A person needs primary care and
    housing and transport and a prescription that doesn't lapse. All of that infrastructure already exists.
    What's missing is the layer that routes between it.</p>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="grid g4">
      <div class="card flat"><div class="nodeline"><span class="dot"></span> Primary care</div></div>
      <div class="card flat"><div class="nodeline"><span class="dot"></span> Behavioral health</div></div>
      <div class="card flat"><div class="nodeline"><span class="dot"></span> Substance-use treatment</div></div>
      <div class="card flat"><div class="nodeline"><span class="dot"></span> Pharmacy</div></div>
      <div class="card flat"><div class="nodeline"><span class="dot renewal"></span> Housing</div></div>
      <div class="card flat"><div class="nodeline"><span class="dot renewal"></span> Transportation</div></div>
      <div class="card flat"><div class="nodeline"><span class="dot renewal"></span> Food &amp; benefits</div></div>
      <div class="card flat"><div class="nodeline"><span class="dot renewal"></span> Employment</div></div>
    </div>
    <div class="callout" style="margin-top:24px">
      <p>Where a state already runs a closed-loop referral network &mdash; NCCARE360 in North Carolina &mdash;
      Astria routes through it rather than around it. Building a competing referral network would put us in a
      fight we could not win and should not pick.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Why it's different from a directory</span>
      <h2>A plan, not a list of phone numbers</h2>
    </div>
    <div class="grid g3">
      <div class="card">
        <h3>Context-aware</h3>
        <p>A plan reflects what is genuinely near that person &mdash; their county, their transport situation,
        whether they have a phone that works this week.</p>
      </div>
      <div class="card">
        <h3>Tracked to delivery</h3>
        <p>We distinguish <em>sent</em> from <em>accepted</em> from <em>actually delivered</em>. The gap between
        the second and third is where most referral systems quietly fail.</p>
      </div>
      <div class="card">
        <h3>Honest about absence</h3>
        <p>Where a service does not exist locally, Astria records the unmet need against that county instead of
        issuing a referral nobody can use. The gap becomes evidence.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="note">
      <strong>The open question on this one</strong>
      <p>Community programmes have no obvious incentive to log into another platform and maintain availability
      data. Every referral network in the country has struggled with exactly this. Our working answer is that
      the Care Promoter maintains it as a by-product of the work she is already doing &mdash; but it is a real
      adoption risk, and we would rather name it than pretend it is solved.</p>
    </div>
  </div>
</section>
""",
scripts="")

# --------------------------------------------------------------- FINANCING
PAGES["financing.html"] = dict(
title="Financing",
desc="Astria is paid out of Medicaid reentry funding that already exists and is currently under-billed.",
body="""
<section>
  <div class="wrap">
    <span class="eyebrow">Financing</span>
    <h1>Paid out of money that already exists</h1>
    <p class="lede" style="margin-top:18px">The strongest position in Medicaid is not asking for new money.
    It is helping a payer deliver something it has already committed to buying.</p>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="grid g3">
      <div class="stat"><div class="v mono-num">~19</div><div class="k">states with approved Medicaid reentry Section 1115 demonstrations</div><div class="src">CMS</div></div>
      <div class="stat"><div class="v mono-num">90</div><div class="k">days before release during which states may cover pre-release services</div><div class="src">CMS SMD #23-003</div></div>
      <div class="stat accent"><div class="v mono-num">$0</div><div class="k">new policy or new funding required for Astria to operate inside those rules</div></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">What CMS requires</span>
      <h2>The services are already mandated</h2>
      <p class="lede">Every approved demonstration is bound to a minimum service package. These are not
      optional extras — they are conditions of the waiver.</p>
    </div>
    <div class="grid g3">
      <div class="card"><h3>Case management</h3><p>Needs assessment, a care plan, a warm handoff to the
      post-release care manager, appointment scheduling, and follow-up to ensure the plan is implemented.</p></div>
      <div class="card"><h3>Medication-assisted treatment</h3><p>For substance use disorder as clinically
      appropriate, with accompanying counselling.</p></div>
      <div class="card"><h3>A 30-day medication supply</h3><p>All prescribed medications, physical and
      behavioural, in hand at release.</p></div>
    </div>
    <div class="callout gold" style="margin-top:26px">
      <p><strong>The gap we work in:</strong> NASHP found that community health worker claim volume stays low
      even in states that have explicitly authorised the billing. The barrier is not policy. It is the
      documentation friction between doing the work and getting paid for it.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Revenue</span>
      <h2>How Astria is paid</h2>
    </div>
    <div class="tablewrap">
      <table>
        <thead><tr><th>Stage</th><th>What we charge</th><th>Where the money comes from</th></tr></thead>
        <tbody>
          <tr><td><strong>Pilot</strong></td><td>Implementation fee, one site</td>
              <td>Demonstration implementation funds; potentially the 90/10 enhanced federal match for reentry health IT, via a state partner</td></tr>
          <tr><td><strong>Scale</strong></td><td>Per enrolled person, per year</td>
              <td>The health system, county programme, or managed care plan</td></tr>
          <tr><td><strong>At maturity</strong></td><td>Per member per month, across a defined reentry episode</td>
              <td>Managed care contract, once the site is billing recurring chronic-care and behavioural-health codes it could not bill before</td></tr>
        </tbody>
      </table>
    </div>
    <div class="grid g2" style="margin-top:24px;gap:24px">
      <div class="card">
        <h3>The alignment</h3>
        <p>Revenue follows how long a member stays connected — ours and the site's. We are paid more for doing
        exactly the thing we exist to do, which is rare enough in health care to be worth stating plainly.</p>
      </div>
      <div class="card">
        <h3>A constraint we observe</h3>
        <p>We never price as a percentage of claims captured. Contingency arrangements on Medicaid billing are
        a compliance problem, not a clever business model.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="note">
      <strong>What we have not yet validated</strong>
      <p>We have not priced this with a payer. The reimbursement rate for a pre-release case management
      encounter is the single number that decides this model, and obtaining it from a state fee schedule is
      our immediate next step. Any figure we quote before then is an assumption, and we will say so.</p>
      <p>A second open question: in most states community health worker services are billable only when the
      worker is certified and supervised by an enrolled Medicaid provider. Whether Astria employs Care
      Promoters directly or contracts through the clinic materially changes the billing path.</p>
    </div>
  </div>
</section>
""",
scripts="")

# --------------------------------------------------------------- IMPLEMENTATION
PAGES["implementation.html"] = dict(
title="Rollout",
desc="Standing up one county: who has to say yes, what it takes, and what blocks it.",
body="""
<section>
  <div class="wrap">
    <span class="eyebrow">Rollout</span>
    <h1>Standing up one county</h1>
    <p class="lede" style="margin-top:18px">The established care model needs a host clinic, a clinical
    champion, grant funding and a new hire — all at once. That is why it reached 48 sites in twenty years.
    Astria needs four things a county already has.</p>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="grid g4">
      <div class="card"><div class="nodeline" style="margin-bottom:10px"><span class="dot"></span><strong>One facility</strong></div>
        <p class="small">A jail or prison willing to upload what it already has.</p></div>
      <div class="card"><div class="nodeline" style="margin-bottom:10px"><span class="dot"></span><strong>One clinic</strong></div>
        <p class="small">That takes Medicaid, and takes this population onto a panel.</p></div>
      <div class="card"><div class="nodeline" style="margin-bottom:10px"><span class="dot renewal"></span><strong>One Care Promoter</strong></div>
        <p class="small">Hired from the population served where possible.</p></div>
      <div class="card"><div class="nodeline" style="margin-bottom:10px"><span class="dot gold"></span><strong>A data agreement</strong></div>
        <p class="small">A business associate agreement, patient authorisation, or both.</p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Sequence</span>
      <h2>Eight weeks, and what blocks each step</h2>
    </div>
    <div class="tablewrap">
      <table>
        <thead><tr><th>Week</th><th>What happens</th><th>Who has to say yes</th><th>What it blocks on</th></tr></thead>
        <tbody>
          <tr><td class="num"><strong>0&ndash;2</strong></td><td>Legal: business associate agreement with the county or its jail health vendor; patient authorisation form drafted and reviewed</td><td>County attorney, jail health vendor</td><td>The longest pole. Start it first.</td></tr>
          <tr><td class="num"><strong>2&ndash;4</strong></td><td>Name the clinic of record and confirm it will accept these patients onto a panel</td><td>FQHC or clinic leadership</td><td>Willingness, not capacity. Some will say no.</td></tr>
          <tr><td class="num"><strong>3&ndash;5</strong></td><td>Identify who performs the upload inside the facility, and how they are compensated for it</td><td>Sheriff or jail administrator; health vendor</td><td>Five unpaid minutes is how adoption dies.</td></tr>
          <tr><td class="num"><strong>4&ndash;6</strong></td><td>Hire and train the Care Promoter</td><td>Astria</td><td>Finding the right person takes longer than the job posting suggests.</td></tr>
          <tr><td class="num"><strong>5&ndash;7</strong></td><td>Configure state billing rules, the local resource list, and the referral network the state already uses</td><td>Astria</td><td>Library work, not custom build.</td></tr>
          <tr><td class="num"><strong>6&ndash;8</strong></td><td>Go live: first upload, first enrolment, first encounter, first claim</td><td>Everyone above</td><td>&mdash;</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Tiers</span>
      <h2>Four levels Astria operates at</h2>
      <p class="lede">The same platform at different depths. Each tier makes the next one easier — a county
      pilot generates the outcome data a health system wants, which generates the volume a state will contract
      for.</p>
    </div>
    <div class="tablewrap">
      <table>
        <thead><tr><th>Tier</th><th>Buyer</th><th>What Astria provides</th><th>What it proves</th></tr></thead>
        <tbody>
          <tr><td><strong>County with no programme</strong></td><td>County health department, sheriff's office, local reentry council</td><td>Full stack: onboarding, matching, a Care Promoter we staff, remote routing where no local provider exists</td><td>That a programme can exist where none did</td></tr>
          <tr><td><strong>County with infrastructure</strong></td><td>FQHC, existing reentry programme</td><td>Onboarding, matching, the continuity watch, billing capture</td><td>That we make an existing programme measurably better</td></tr>
          <tr><td><strong>Health system</strong></td><td>Multi-county system or FQHC network</td><td>Multi-site deployment, cross-county matching, the Astria ID as the linkage layer</td><td>That continuity holds when people move between counties</td></tr>
          <tr><td><strong>State</strong></td><td>State Medicaid agency or managed care plan</td><td>Statewide onboarding, demonstration reporting, the ID as shared infrastructure</td><td>That this is infrastructure, not a programme</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="grid g3">
      <div class="card"><h3>What we bring</h3>
        <ul class="small" style="padding-left:20px;line-height:1.9;margin:10px 0 0">
          <li>The platform and the rules library</li><li>The Care Promoter, at county tiers</li>
          <li>Billing capture and demonstration reporting</li><li>The Astria ID and the continuity watch</li></ul></div>
      <div class="card"><h3>What the partner brings</h3>
        <ul class="small" style="padding-left:20px;line-height:1.9;margin:10px 0 0">
          <li>Facility access and the upload</li><li>A clinic willing to accept attribution</li>
          <li>The legal route for the data</li><li>Local relationships we do not have</li></ul></div>
      <div class="card"><h3>What we never bring</h3>
        <ul class="small" style="padding-left:20px;line-height:1.9;margin:10px 0 0">
          <li>A replacement for the existing programme</li><li>A parallel referral network</li>
          <li>Data to probation, parole or the courts</li><li>A promise that an app fixes transport</li></ul></div>
    </div>
  </div>
</section>
""",
scripts="")

# --------------------------------------------------------------- TEAM
PAGES["team.html"] = dict(
title="Team",
desc="Five students at the University of North Carolina working at the intersection of health, medicine and innovation.",
body="""
<section>
  <div class="wrap">
    <span class="eyebrow">The team</span>
    <h1>Five students at the intersection of health, medicine, and innovation</h1>
    <p class="lede" style="margin-top:18px">We came to this because reentry is one of the few places in
    health care where the model is proven and almost nobody can run it.</p>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="team">
      <div class="person"><img src="assets/img/suhan.png" alt="Suhan Asaigoli">
        <div class="nm">Suhan Asaigoli &rsquo;27</div><div class="fo">Neuroscience</div><div class="sc">Morehead-Cain Scholar</div></div>
      <div class="person"><img src="assets/img/favor.png" alt="Favor Asabor">
        <div class="nm">Favor Asabor &rsquo;27</div><div class="fo">Health Policy &amp; Management</div><div class="sc">Honors Carolina</div></div>
      <div class="person"><img src="assets/img/aidan.png" alt="Aidan Gunn">
        <div class="nm">Aidan Gunn &rsquo;27</div><div class="fo">Communication Studies</div><div class="sc">Johnston Scholar</div></div>
      <div class="person"><img src="assets/img/niharika.png" alt="Niharika Koppolu">
        <div class="nm">Niharika Koppolu &rsquo;29</div><div class="fo">Biostatistics</div><div class="sc">Morehead-Cain Scholar</div></div>
      <div class="person"><img src="assets/img/amy.png" alt="Amy Okonkwo">
        <div class="nm">Amy Okonkwo &rsquo;28</div><div class="fo">Environmental Health Sciences</div><div class="sc">Morehead-Cain Scholar</div></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <span class="eyebrow">Experience across</span>
    <div class="afflogos">
      <img src="assets/img/aff_chai.png" alt="Clinton Health Access Initiative">
      <img src="assets/img/aff_uncsom.png" alt="UNC School of Medicine">
      <img src="assets/img/aff_ncdhhs.png" alt="North Carolina Department of Health and Human Services">
      <img src="assets/img/aff_heartland.png" alt="Heartland Whole Health Institute">
      <img src="assets/img/aff_phrii.png" alt="PHRII">
      <img src="assets/img/aff_campusy.png" alt="Campus Y">
      <img src="assets/img/aff_bme.png" alt="UNC/NC State Biomedical Engineering">
      <img src="assets/img/aff_ccn.png" alt="Campus Climate Network">
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="grid g2" style="gap:24px">
      <div class="card">
        <h3>Where we are</h3>
        <p>Astria is a working concept, not a deployed service. We have built the coverage analysis, specified
        the platform, and are moving into practitioner interviews and a first county partnership.</p>
      </div>
      <div class="card">
        <h3>What we're looking for</h3>
        <p>One county partner and one design partner. If you run a reentry programme, a health centre, or a
        Medicaid reentry initiative and this is a problem you recognise, we would like to hear where we have
        it wrong.</p>
      </div>
    </div>
  </div>
</section>
""",
scripts="")

# --------------------------------------------------------------- COVERAGE (map)
PAGES["coverage.html"] = dict(
title="Coverage analysis",
desc="Every FQHC and safety-net hospital in North Carolina, mapped against county geography and travel radius.",
body="""
<section>
  <div class="wrap">
    <span class="eyebrow">Proof of concept &mdash; North Carolina</span>
    <h1>We mapped the whole state</h1>
    <p class="lede" style="margin-top:18px">A matching engine is only as good as the supply it matches into.
    So before specifying the product, we mapped every federally qualified health center and safety-net
    hospital in North Carolina against county geography and population.</p>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="grid g4" id="cov-stats"></div>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="demo">
      <div class="demo-bar">
        <span class="dot"></span><span class="title">North Carolina &mdash; care access</span>
        <span class="right"><span class="pill blue" id="cov-mode">Health centres per county</span></span>
      </div>
      <div class="demo-body">
        <div class="ctrl">
          <div class="seg" id="cov-seg">
            <button data-m="fq" aria-pressed="true">Health centres</button>
            <button data-m="all" aria-pressed="false">All facilities</button>
            <button data-m="radius" aria-pressed="false">Travel radius</button>
          </div>
          <label for="cov-rad">Radius</label>
          <input type="range" id="cov-rad" min="5" max="60" step="5" value="15">
          <span class="mono-num" id="cov-radv" style="font-weight:700;min-width:58px">15 mi</span>
        </div>
        <svg id="map" role="img" aria-label="Map of North Carolina counties by health centre access"></svg>
        <div class="legend" id="cov-legend"></div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="grid g2" style="gap:24px">
      <div class="card">
        <h3>The finding that shaped the product</h3>
        <p>No county in North Carolina is more than <strong>31 miles</strong> from a county that has a federally
        qualified health center. We modelled the network: <strong>24 anchor sites</strong> would place all 100
        counties within a 35-mile radius.</p>
        <p>The infrastructure to reach the whole state largely exists. What is missing is the layer that
        connects it — which is why Astria is a navigation system rather than a clinic.</p>
      </div>
      <div class="card">
        <h3>And the finding that constrains it</h3>
        <p>At <strong>15 miles</strong> — a realistic limit for someone without a car in their first month out
        — fourteen counties and roughly <strong>734,000 people</strong> fall outside reach. Access in North
        Carolina is not primarily a facility problem. It is a transport problem wearing a facility problem's
        clothes.</p>
        <p>That is why a Care Promoter who can work by phone or video is a design requirement, not a
        convenience.</p>
      </div>
    </div>
    <div class="note" style="margin-top:26px">
      <strong>How to read these numbers</strong>
      <p>Distances are straight-line, county-centroid to county-centroid. Treat every one as a floor rather
      than a drive time — Dare County, on the Outer Banks, is the clearest case where the number flatters
      reality. We do not yet hold a population or vehicle-access layer, so a large rural county and a dense
      small one look alike here. Source data is the NC DSH &amp; FQHC Locations 2022 workbook; four county
      names were misspelled in the source and corrected on load.</p>
    </div>
  </div>
</section>
""",
scripts="""<script>
fetch('assets/ncdata.json').then(function(r){return r.json();}).then(function(D){
  var C=D.counties, T=D.totals;
  C.forEach(function(c){ c.tot=c.fq+c.dsh; });

  var lons=[],lats=[];
  C.forEach(function(c){ c.polys.forEach(function(p){ p[0].forEach(function(pt){ lons.push(pt[0]); lats.push(pt[1]); }); }); });
  var minx=Math.min.apply(null,lons), maxx=Math.max.apply(null,lons),
      miny=Math.min.apply(null,lats), maxy=Math.max.apply(null,lats);
  var k=Math.cos((miny+maxy)/2*Math.PI/180), Wv=1000, pad=8;
  var sx=(Wv-2*pad)/((maxx-minx)*k), Hv=(maxy-miny)*sx+2*pad;
  function px(l){return pad+(l-minx)*k*sx;} function py(l){return Hv-pad-(l-miny)*sx;}
  var svg=document.getElementById('map');
  svg.setAttribute('viewBox','0 0 '+Wv+' '+Math.round(Hv));
  C.forEach(function(c){
    var d='';
    c.polys.forEach(function(poly){ poly.forEach(function(ring){
      ring.forEach(function(pt,i){ d+=(i?'L':'M')+px(pt[0]).toFixed(1)+' '+py(pt[1]).toFixed(1); }); d+='Z'; }); });
    c.d=d;
  });

  function hav(a,b,c2,d2){
    var R=3958.8,p1=b*Math.PI/180,p2=d2*Math.PI/180;
    var x=Math.pow(Math.sin((p2-p1)/2),2)+Math.cos(p1)*Math.cos(p2)*Math.pow(Math.sin((c2-a)*Math.PI/180/2),2);
    return 2*R*Math.asin(Math.sqrt(x));
  }
  var wf=C.filter(function(c){return c.fq>0;});
  C.forEach(function(a){ a.near = a.fq>0 ? 0 : Math.min.apply(null, wf.map(function(b){return hav(a.cx,a.cy,b.cx,b.cy);})); });

  var RAMP=['#DCE4FA','#AABEF5','#7E9BEF','#4776E6','#3862CB','#28478F'];
  var GAP='#C9705A';
  var metric='fq', radius=15;
  var MAXFQ=Math.max.apply(null,C.map(function(c){return c.fq;}));
  var MAXTOT=Math.max.apply(null,C.map(function(c){return c.tot;}));

  function fill(c){
    if(metric==='radius') return c.near<=radius ? RAMP[2] : GAP;
    var v = metric==='fq'? c.fq : c.tot;
    if(v===0) return GAP;
    var mx = metric==='fq'? MAXFQ : MAXTOT;
    return RAMP[Math.min(RAMP.length-1, 1+Math.floor(v/mx*(RAMP.length-2)))];
  }
  function draw(){
    svg.innerHTML = C.map(function(c,i){
      return '<path class="cty" d="'+c.d+'" fill="'+fill(c)+'" data-i="'+i+'"><title>'+c.name+'</title></path>';
    }).join('');
    var L=document.getElementById('cov-legend');
    if(metric==='radius'){
      L.innerHTML='<span><i style="background:'+RAMP[2]+'"></i>health centre county within '+radius+' mi</span>'
                 +'<span><i style="background:'+GAP+'"></i>none within '+radius+' mi</span>';
    } else {
      L.innerHTML='<span><i style="background:'+GAP+'"></i>none</span><span>then</span>'
        +RAMP.slice(1).map(function(c){return '<span><i style="background:'+c+'"></i></span>';}).join('')
        +'<span>fewer &rarr; more</span>';
    }
  }
  function stats(){
    var out=C.filter(function(c){return c.near>radius;});
    document.getElementById('cov-stats').innerHTML=[
      ['288','facilities mapped statewide','171 health centres &middot; 117 safety-net hospitals',''],
      ['18','counties with no health centre','of 100 &mdash; 6 have neither kind',''],
      [out.length,'counties outside '+radius+' miles','no health-centre county within range','accent'],
      ['24','anchor sites cover all 100 counties','within a 35-mile radius','accent']
    ].map(function(t){
      return '<div class="stat '+t[3]+'"><div class="v mono-num">'+t[0]+'</div><div class="k">'+t[1]
        +'</div><div class="src">'+t[2]+'</div></div>';
    }).join('');
  }

  var tip=document.createElement('div'); tip.id='tip'; document.body.appendChild(tip);
  svg.addEventListener('mousemove',function(e){
    var p=e.target.closest('.cty'); if(!p){ tip.style.opacity=0; return; }
    var c=C[+p.dataset.i];
    tip.innerHTML='<b>'+c.name+' County</b><br>'+c.fq+' health centres &middot; '+c.dsh+' hospitals'
      +(c.fq===0?'<br>nearest health-centre county '+c.near.toFixed(0)+' mi':'');
    tip.style.opacity=1;
    tip.style.left=Math.min(e.clientX+14, innerWidth-280)+'px';
    tip.style.top=(e.clientY+16)+'px';
  });
  svg.addEventListener('mouseleave',function(){ tip.style.opacity=0; });

  document.getElementById('cov-seg').addEventListener('click',function(e){
    var b=e.target.closest('[data-m]'); if(!b) return;
    this.querySelectorAll('[data-m]').forEach(function(x){x.setAttribute('aria-pressed','false');});
    b.setAttribute('aria-pressed','true'); metric=b.dataset.m;
    document.getElementById('cov-mode').textContent =
      {fq:'Health centres per county',all:'All facilities per county',radius:'Within '+radius+' miles'}[metric];
    draw();
  });
  var rad=document.getElementById('cov-rad');
  rad.addEventListener('input',function(){
    radius=+rad.value; document.getElementById('cov-radv').textContent=radius+' mi';
    if(metric==='radius') document.getElementById('cov-mode').textContent='Within '+radius+' miles';
    draw(); stats();
  });

  draw(); stats();
});
</script>""")

# ===========================================================================
ORDER = [h for h,_ in NAV]
TITLES = {h:t for h,t in NAV}

def build():
    for i, href in enumerate(ORDER):
        pg = PAGES[href]
        prev = (ORDER[i-1], TITLES[ORDER[i-1]]) if i > 0 else None
        nxt  = (ORDER[i+1], TITLES[ORDER[i+1]]) if i < len(ORDER)-1 else None
        body = pg["body"] + pagenav(prev, nxt)
        html = SHELL.format(title=pg["title"], desc=pg["desc"], mark=mark(False),
                            nav=nav_html(href), body=body, scripts=pg.get("scripts",""))
        with open(os.path.join(HERE, href), "w") as f:
            f.write(html)
        print("wrote", href)

if __name__ == "__main__":
    build()
