const pptxgen = require("pptxgenjs");
const A = "/private/tmp/claude-501/-Users-suhanasaigoli-Desktop-Projects-Astria/d2e3bd46-8980-434f-ba94-01d6e71bac34/scratchpad/assets/";
const p = new pptxgen();
p.layout = "LAYOUT_WIDE";                 // 13.333 x 7.5
p.author = "Astria"; p.title = "Astria — Every point of care. One path forward.";

/* ---------- brand tokens ---------- */
const MID="101B2D", IVORY="F7F5EF", WHITE="FFFFFF", BLUE="4776E6",
      HORIZON="AABEF5", RENEWAL="91B5A2", GOLD="E8B85B", SLATE="687386",
      MID_SOFT="2A3A54", IVORY_DIM="E7E3D8", INK_ON_DARK="E8EBF2";
const DISP="Manrope", BODY="Inter";
const W=13.333, H=7.5, M=0.95;            // generous margins per brand

/* ---------- helpers ---------- */
const bg=(s,c)=>{ s.background={color:c}; };
const T=(s,t,o)=>s.addText(t, Object.assign({isTextBox:true,margin:0,valign:"top"},o));
const node=(s,x,y,d,c)=>s.addShape(p.ShapeType.ellipse,{x:x-d/2,y:y-d/2,w:d,h:d,fill:{color:c},line:{type:"none"}});
const ring=(s,x,y,d,c)=>s.addShape(p.ShapeType.ellipse,{x:x-d/2,y:y-d/2,w:d,h:d,fill:{color:"FFFFFF"},line:{color:c,width:1.25}});
const seg=(s,x1,y1,x2,y2,c,w)=>s.addShape(p.ShapeType.line,{x:x1,y:y1,w:x2-x1,h:y2-y1,line:{color:c||BLUE,width:w||1.25}});
const star=(s,x,y,d,c)=>s.addShape(p.ShapeType.star4,{x:x-d/2,y:y-d/2,w:d,h:d,fill:{color:c||GOLD},line:{type:"none"}});
const card=(s,x,y,w,h,f,ln)=>s.addShape(p.ShapeType.roundRect,{x,y,w,h,rectRadius:0.07,
  fill:{color:f||WHITE},line:ln?{color:ln,width:1}:{type:"none"}});

const eyebrow=(s,t,c)=>T(s,t.toUpperCase(),{x:M,y:0.72,w:W-2*M,h:0.26,fontFace:BODY,fontSize:10.5,
  bold:true,charSpacing:2.6,color:c||SLATE});
const h1=(s,t,o)=>{o=o||{};T(s,t,{x:M,y:o.y===undefined?1.12:o.y,w:o.w||(W-2*M),h:o.h||1.3,
  fontFace:DISP,fontSize:o.size||32,bold:true,color:o.color||MID,lineSpacing:o.ls||38,charSpacing:-0.4});};
const lede=(s,t,o)=>{o=o||{};T(s,t,{x:M,y:o.y||2.35,w:o.w||8.6,h:o.h||0.9,fontFace:BODY,
  fontSize:o.size||14,color:o.color||SLATE,lineSpacing:o.ls||22});};
const foot=(s,t,c)=>T(s,t,{x:M,y:6.74,w:W-2*M,h:0.3,fontFace:BODY,fontSize:9,color:c||"9AA3B2"});

/* Astria mark: geometric A + contiguous path through nodes + gold north star */
function mark(s,x,y,sc,onDark){
  const aFill = onDark ? WHITE : MID;
  const pathC = onDark ? HORIZON : BLUE;
  // the A — solid wedge with a counter notch
  s.addShape(p.ShapeType.triangle,{x:x,y:y,w:0.74*sc,h:0.78*sc,fill:{color:aFill},line:{type:"none"}});
  s.addShape(p.ShapeType.triangle,{x:x+0.235*sc,y:y+0.46*sc,w:0.27*sc,h:0.32*sc,
    fill:{color:onDark?MID:IVORY},line:{type:"none"}});
  // navigation path: one continuous stroke through waypoints to the star
  const px=[x-0.60*sc, x-0.30*sc, x+0.06*sc, x+0.44*sc, x+0.76*sc];
  const py=[y+0.70*sc, y+0.50*sc, y+0.22*sc, y+0.02*sc, y-0.16*sc];
  for(let i=0;i<px.length-1;i++) seg(s,px[i],py[i],px[i+1],py[i+1],pathC,1.25);
  node(s,px[0],py[0],0.11*sc,pathC);
  node(s,px[1],py[1],0.09*sc,pathC);
  node(s,px[3],py[3],0.08*sc,HORIZON);
  star(s,x+0.80*sc,y-0.20*sc,0.30*sc,GOLD);
}

/* service-node constellation used on the disconnected / connected pair */
const SERVICES=[
  ["Primary care",      9.10,2.73],
  ["Behavioral health", 7.05,3.27],
  ["Medication",        8.35,4.15],
  ["Housing",          10.60,3.10],
  ["Transportation",    7.55,4.97],
  ["Employment",       10.35,4.50],
  ["Benefits",          8.95,5.50]
];
function constellation(s,connected,onDark){
  const lab = onDark ? "B9C2D4" : SLATE;
  const dotC = onDark ? HORIZON : BLUE;
  if(connected){
    const order=[1,2,4,6,5,0,3];              // one contiguous, non-crossing route
    for(let i=0;i<order.length-1;i++){
      const a=SERVICES[order[i]], b=SERVICES[order[i+1]];
      seg(s,a[1],a[2],b[1],b[2],onDark?"3E5277":HORIZON,1.1);
    }
    const last=SERVICES[3];
    seg(s,last[1],last[2],11.52,2.30,onDark?"6C5A32":GOLD,1.1);
    star(s,11.60,2.22,0.42,GOLD);
    T(s,"Next step",{x:11.03,y:2.60,w:1.5,h:0.24,fontFace:BODY,fontSize:9,bold:true,
      color:GOLD,align:"center",charSpacing:0.6});
  }
  SERVICES.forEach(([t,x,y],i)=>{
    if(connected && (i===0||i===3)) node(s,x,y,0.17,dotC);
    else if(connected) node(s,x,y,0.15,dotC);
    else ring(s,x,y,0.15,onDark?"4A5A77":HORIZON);
    const above = connected && (i===0);
    T(s,t,{x:x-0.95,y:above?y-0.36:y+0.14,w:1.9,h:0.24,fontFace:BODY,fontSize:9,color:lab,align:"center"});
  });
}

/* =================================================================== 1 TITLE */
let s=p.addSlide(); bg(s,MID);
s.addImage({path:A+"logo-reversed.png",x:4.84,y:2.18,w:3.66,h:2.36});
T(s,"EVERY POINT OF CARE.   ONE PATH FORWARD.",{x:0,y:4.86,w:W,h:0.3,fontFace:BODY,
  fontSize:11,color:HORIZON,align:"center",charSpacing:3.4});
seg(s,5.55,5.42,7.78,5.42,"2E4068",1);
T(s,"Intelligent chronic-care navigation and reentry health infrastructure",
  {x:0,y:5.64,w:W,h:0.3,fontFace:BODY,fontSize:11.5,color:"7E8BA6",align:"center"});
s.addNotes("Speaker 1 opens on this slide. Hold it through the first two problem lines before advancing.");

/* =================================================================== 2 PROBLEM */
s=p.addSlide(); bg(s,IVORY);
eyebrow(s,"The problem");
h1(s,"The two weeks after release are\nthe most dangerous in American health care",{size:30,ls:40,h:1.6});

card(s,M,3.02,3.42,2.62,WHITE);
T(s,"12.7×",{x:M+0.38,y:3.34,w:2.7,h:0.95,fontFace:DISP,fontSize:48,bold:true,color:MID,charSpacing:-0.3});
T(s,"higher risk of death in the first two weeks after release, compared with the general population",
  {x:M+0.38,y:4.34,w:2.66,h:1.0,fontFace:BODY,fontSize:11.5,color:SLATE,lineSpacing:16});

card(s,M+3.68,3.02,3.42,2.62,WHITE);
T(s,"80%",{x:M+4.06,y:3.34,w:2.7,h:0.95,fontFace:DISP,fontSize:48,bold:true,color:MID,charSpacing:-0.3});
T(s,"of people leaving incarceration have a chronic medical, psychiatric, or substance-use condition",
  {x:M+4.06,y:4.34,w:2.66,h:1.0,fontFace:BODY,fontSize:11.5,color:SLATE,lineSpacing:16});

card(s,M+7.36,3.02,3.42,2.62,MID);
T(s,"What that looks like",{x:M+7.74,y:3.32,w:2.7,h:0.3,fontFace:BODY,fontSize:10,bold:true,
  charSpacing:1.8,color:GOLD});
["An overdose.","Blood pressure nobody managed.","A prescription that ran out on day fifteen."]
  .forEach((t,i)=>T(s,t,{x:M+7.74,y:3.76+i*0.56,w:2.68,h:0.5,fontFace:BODY,fontSize:12.5,
    color:INK_ON_DARK,lineSpacing:17}));

foot(s,"Binswanger et al., New England Journal of Medicine, 2007  ·  ASPE Report to Congress, 2023");

/* =================================================================== 3 DISCONNECTED */
s=p.addSlide(); bg(s,MID);
eyebrow(s,"The gap","8A94AC");
h1(s,"The resources exist.\nThe system doesn’t.",{color:WHITE,size:34,ls:44,h:1.7,w:5.6});
lede(s,"Primary care, behavioral health, medication, housing, transport — all of it is already there. Nothing connects it across the moment of release.",
  {y:3.18,w:4.9,color:"9AA6BF",size:13.5});
constellation(s,false,true);
s.addNotes("Speaker 1: 'The problem isn't that nobody provides care. It's that nobody owns the transition.'");

/* =================================================================== 4 BOUNDARIES */
s=p.addSlide(); bg(s,IVORY);
eyebrow(s,"Why it keeps happening");
h1(s,"Nobody owns the transition",{size:34,h:0.9});
lede(s,"Three systems, three endpoints. Each one working exactly as designed.",{y:2.12,size:14});

const BND=[["A jail’s responsibility","ends at release"],
           ["A health plan’s","can end at disenrollment"],
           ["A clinic loses someone","when they disappear from its panel"]];
BND.forEach((b,i)=>{
  const x=M+i*3.72;
  card(s,x,2.92,3.42,1.86,WHITE);
  seg(s,x+0.38,3.34,x+1.52,3.34,HORIZON,1.1);
  node(s,x+0.38,3.34,0.13,BLUE);
  node(s,x+1.52,3.34,0.13,IVORY_DIM);
  T(s,b[0],{x:x+0.38,y:3.62,w:2.7,h:0.3,fontFace:DISP,fontSize:14,bold:true,color:MID});
  T(s,b[1],{x:x+0.38,y:3.96,w:2.72,h:0.56,fontFace:BODY,fontSize:12.5,color:SLATE,lineSpacing:17});
});
card(s,M,5.14,11.44,0.92,MID);
T(s,"Every system can work exactly as designed — and the patient can still fall through the middle.",
  {x:M+0.46,y:5.42,w:10.6,h:0.4,fontFace:DISP,fontSize:16,bold:true,color:WHITE});

/* =================================================================== 5 CONNECTED */
s=p.addSlide(); bg(s,MID);
eyebrow(s,"The solution","8A94AC");
h1(s,"Astria connects\nthe points.",{color:WHITE,size:34,ls:44,h:1.7,w:5.2});
lede(s,"One intelligent navigation system for the entire journey — before release, through the first year, and across whatever happens next.",
  {y:3.18,w:4.9,color:"9AA6BF",size:13.5});
constellation(s,true,true);
foot(s,"Point → Path → Star","5E6B86");

/* =================================================================== 6 ARGO */
s=p.addSlide(); bg(s,IVORY);
eyebrow(s,"Onboarding");
h1(s,"Argo meets facilities where they are",{size:32,h:0.9});
lede(s,"Fewer than 5% of state corrections departments can exchange structured medical data. So Astria doesn’t require interoperability that doesn’t exist.",
  {y:2.10,w:9.4,size:14});

const STEPS=[["Any format in","A fax, a scan, a spreadsheet, a discharge record — whatever the facility actually has."],
             ["Argo extracts","Conditions, medications and days of supply, release date, contacts. Missing fields become tasks, not blanks."],
             ["Coverage assembled","Argo assembles the Medicaid application so a certified assister can submit in minutes."],
             ["A usable record","A baseline the care team can act on from day one."]];
STEPS.forEach((st,i)=>{
  const x=M+i*2.90;
  card(s,x,3.10,2.62,2.44,WHITE);
  node(s,x+0.44,3.56,0.30,i===3?RENEWAL:BLUE);
  T(s,String(i+1),{x:x+0.29,y:3.44,w:0.3,h:0.26,fontFace:BODY,fontSize:11,bold:true,color:WHITE,align:"center"});
  T(s,st[0],{x:x+0.30,y:3.92,w:2.1,h:0.3,fontFace:DISP,fontSize:13.5,bold:true,color:MID});
  T(s,st[1],{x:x+0.30,y:4.26,w:2.06,h:1.14,fontFace:BODY,fontSize:11,color:SLATE,lineSpacing:15});
  if(i<3) seg(s,x+2.66,4.32,x+2.86,4.32,HORIZON,1.25);
});
card(s,M,5.78,11.44,0.72,"EFECE2");
T(s,"AI with a human in the loop. Argo compresses the paperwork so the care team spends its time on people.",
  {x:M+0.44,y:5.98,w:10.6,h:0.36,fontFace:BODY,fontSize:12.5,color:MID});

/* =================================================================== 7 ASTRIA ID */
s=p.addSlide(); bg(s,IVORY);
eyebrow(s,"Continuity");
h1(s,"One identifier that survives the gaps",{size:32,h:0.9});
lede(s,"An encrypted Astria ID resolves a person’s booking number, Medicaid ID, and clinic records back to the same human being.",
  {y:2.10,w:9.0,size:14});

const IDS=[["Booking number","Corrections"],["Medicaid ID","Coverage"],["Clinic record","Care"]];
IDS.forEach((d,i)=>{
  const y=3.46+i*0.78;
  card(s,M,y,3.30,0.62,WHITE);
  T(s,d[0],{x:M+0.34,y:y+0.13,w:2.2,h:0.26,fontFace:DISP,fontSize:12.5,bold:true,color:MID});
  T(s,d[1],{x:M+2.30,y:y+0.15,w:0.92,h:0.24,fontFace:BODY,fontSize:9.5,color:SLATE,align:"right"});
  seg(s,M+3.36,y+0.31,M+4.74,4.26,HORIZON,1.1);
});
card(s,M+4.78,3.40,3.00,1.72,MID);
star(s,M+6.28,3.82,0.30,GOLD);
T(s,"ASTRIA ID",{x:M+4.90,y:4.14,w:2.76,h:0.3,fontFace:DISP,fontSize:16,bold:true,
  color:WHITE,align:"center",charSpacing:2.2});
T(s,"Encrypted. Internal. Never visible to corrections, courts, probation or parole.",
  {x:M+4.98,y:4.50,w:2.6,h:0.5,fontFace:BODY,fontSize:9.5,color:"9AA6BF",align:"center",lineSpacing:13});

T(s,"So losing coverage, changing counties, or returning to custody doesn’t mean starting over.",
  {x:M+8.14,y:3.66,w:3.30,h:0.9,fontFace:DISP,fontSize:15,bold:true,color:MID,lineSpacing:21});
T(s,"The record follows the person, not the institution.",
  {x:M+8.14,y:4.70,w:3.26,h:0.6,fontFace:BODY,fontSize:12,color:SLATE,lineSpacing:17});

/* =================================================================== 8 CARE PROMOTER */
s=p.addSlide(); bg(s,IVORY);
eyebrow(s,"The human model");
h1(s,"Software isn’t the intervention",{size:32,h:0.9});

card(s,M,2.36,5.34,3.54,WHITE);
T(s,"Evidence",{x:M+0.44,y:2.68,w:3,h:0.28,fontFace:BODY,fontSize:10,bold:true,charSpacing:1.8,color:SLATE});
T(s,"39.2%  →  25.5%",{x:M+0.44,y:3.04,w:4.6,h:0.8,fontFace:DISP,fontSize:36,bold:true,color:MID,charSpacing:-0.3});
T(s,"Emergency-department use, after adding a community health worker to the care team — measured against a comparison group that already received expedited primary care.",
  {x:M+0.44,y:4.00,w:4.5,h:1.3,fontFace:BODY,fontSize:12,color:SLATE,lineSpacing:17});
T(s,"Transitions Clinic Network · Wang et al., AJPH, 2012",
  {x:M+0.44,y:5.30,w:4.5,h:0.26,fontFace:BODY,fontSize:9,color:"9AA3B2"});

card(s,M+5.70,2.36,5.74,3.54,MID);
star(s,M+6.16,2.84,0.26,GOLD);
T(s,"Every Astria member gets a Care Promoter",{x:M+6.42,y:2.68,w:4.9,h:0.38,
  fontFace:DISP,fontSize:17,bold:true,color:WHITE});
T(s,"A community health worker who knows their name, their plan, and what happened last week.",
  {x:M+6.14,y:3.20,w:5.1,h:0.6,fontFace:BODY,fontSize:12.5,color:INK_ON_DARK,lineSpacing:17});
["In person where we have local staff, by phone or video where we don’t",
 "A care team built around what they actually need — chronic disease, behavioral health, substance-use treatment, maternal care",
 "Argo takes the administrative load so this person can spend time building trust"]
 .forEach((t,i)=>{
   const y=3.92+i*0.58;
   node(s,M+6.14,y+0.10,0.09,HORIZON);
   T(s,t,{x:M+6.36,y:y,w:4.9,h:0.52,fontFace:BODY,fontSize:11,color:"A9B5CC",lineSpacing:15});
 });
foot(s,"Technology can do the paperwork. It cannot do the trust.");

/* =================================================================== 9 NETWORK */
s=p.addSlide(); bg(s,IVORY);
eyebrow(s,"The network");
h1(s,"Astria doesn’t build a parallel system",{size:32,h:0.9});
lede(s,"It connects the infrastructure already doing this work, so a plan reflects what is genuinely available near that person.",
  {y:2.10,w:9.0,size:14});

const NET=[["Primary care",BLUE],["Behavioral health",BLUE],["Substance-use treatment",BLUE],
           ["Transportation",RENEWAL],["Housing",RENEWAL],["Food & benefits",RENEWAL],
           ["Employment",RENEWAL],["Existing referral networks",SLATE]];
NET.forEach((n,i)=>{
  const col=i%4, row=Math.floor(i/4);
  const x=M+col*2.90, y=3.06+row*1.12;
  card(s,x,y,2.62,0.86,WHITE);
  node(s,x+0.40,y+0.43,0.15,n[1]);
  T(s,n[0],{x:x+0.66,y:y+0.30,w:1.86,h:0.34,fontFace:BODY,fontSize:11.5,bold:true,color:MID,lineSpacing:14});
});
card(s,M,5.56,11.44,0.86,"EFECE2");
T(s,"We route through whatever a state already pays for — not around it.",
  {x:M+0.46,y:5.82,w:10.6,h:0.36,fontFace:DISP,fontSize:15,bold:true,color:MID});

/* =================================================================== 10 TIMING */
s=p.addSlide(); bg(s,MID);
eyebrow(s,"Why now","8A94AC");
h1(s,"States are already paying for the transition.\nThe challenge is delivering it.",
  {color:WHITE,size:28,ls:38,h:1.5});

const TIME=[["~19","states with approved Medicaid reentry demonstrations"],
            ["3","services CMS requires: case management, MAT when appropriate, and medication in hand at release"],
            ["$0","new policy or new funding required for Astria to operate inside them"]];
TIME.forEach((t,i)=>{
  const x=M+i*3.84;
  card(s,x,3.10,3.54,2.16,MID_SOFT);
  T(s,t[0],{x:x+0.40,y:3.38,w:2.8,h:0.8,fontFace:DISP,fontSize:40,bold:true,color:GOLD,charSpacing:-0.3});
  T(s,t[1],{x:x+0.40,y:4.28,w:2.76,h:0.84,fontFace:BODY,fontSize:11.5,color:INK_ON_DARK,lineSpacing:16});
});
T(s,"Astria contracts with health systems, county programs, and reentry partners per enrolled person — with a path to per-member reimbursement.",
  {x:M,y:5.62,w:11.3,h:0.6,fontFace:BODY,fontSize:12.5,color:"9AA6BF",lineSpacing:18});
foot(s,"CMS State Medicaid Director letter #23-003  ·  Medicaid.gov reentry demonstrations","5E6B86");

/* =================================================================== 11 PROOF */
s=p.addSlide(); bg(s,IVORY);
eyebrow(s,"Proof of concept — North Carolina");
h1(s,"We mapped the whole state",{size:32,h:0.9});
lede(s,"Every federally qualified health center and safety-net hospital in North Carolina, joined to county geography and population.",
  {y:2.10,w:9.0,size:14});

const PROOF=[["288","facilities mapped statewide",MID],
             ["18","counties with no FQHC",MID],
             ["6","counties with neither an FQHC nor a safety-net hospital",MID]];
PROOF.forEach((d,i)=>{
  const y=3.02+i*0.90;
  T(s,d[0],{x:M,y:y,w:1.3,h:0.6,fontFace:DISP,fontSize:30,bold:true,color:d[2],charSpacing:-0.2});
  T(s,d[1],{x:M+1.46,y:y+0.12,w:3.5,h:0.56,fontFace:BODY,fontSize:12,color:SLATE,lineSpacing:16});
});

card(s,M+5.42,2.92,6.02,2.86,MID);
star(s,M+5.92,3.40,0.30,GOLD);
T(s,"24",{x:M+5.80,y:3.74,w:1.8,h:0.9,fontFace:DISP,fontSize:52,bold:true,color:GOLD,charSpacing:-0.4});
T(s,"anchor sites would put all 100 North Carolina counties within a 35-mile radius of an FQHC county.",
  {x:M+7.40,y:3.78,w:3.80,h:1.1,fontFace:DISP,fontSize:15,bold:true,color:WHITE,lineSpacing:21});
T(s,"The infrastructure largely exists. What’s missing is the layer that holds onto someone when every other system lets go.",
  {x:M+5.86,y:4.92,w:5.3,h:0.66,fontFace:BODY,fontSize:11.5,color:"9AA6BF",lineSpacing:16});
foot(s,"Astria analysis · NC DSH & FQHC Locations 2022 workbook, US Census county geography. Straight-line county-centroid distances.");

/* =================================================================== 12 CLOSE */
s=p.addSlide(); bg(s,MID);
// a quiet constellation across the upper field
const CST=[[2.30,1.70],[3.65,2.28],[5.10,1.92],[6.55,2.56],[8.00,2.10],[9.35,2.74]];
for(let i=0;i<CST.length-1;i++) seg(s,CST[i][0],CST[i][1],CST[i+1][0],CST[i+1][1],"32446A",1);
seg(s,CST[5][0],CST[5][1],10.72,1.98,"6C5A32",1);
CST.forEach(([x,y],i)=>node(s,x,y,i%2?0.09:0.12,i<3?"4A5E8A":HORIZON));
star(s,10.82,1.90,0.40,GOLD);

T(s,"Astraea is the constellation associated with balance and justice —",
  {x:M,y:3.46,w:11.3,h:0.42,fontFace:BODY,fontSize:14,color:"9AA6BF"});
T(s,"a reminder that where someone has been should not determine whether they receive care.",
  {x:M,y:3.86,w:10.6,h:0.5,fontFace:BODY,fontSize:14,color:"9AA6BF"});
T(s,"Leaving incarceration should\nnever mean leaving care.",
  {x:M,y:4.62,w:10.6,h:1.3,fontFace:DISP,fontSize:32,bold:true,color:WHITE,lineSpacing:42,charSpacing:-0.5});
s.addImage({path:A+"logo-reversed.png",x:10.94,y:5.04,w:1.74,h:1.12});

/* =================================================================== 13 TEAM */
s=p.addSlide(); bg(s,IVORY);
eyebrow(s,"The team");
h1(s,"Five students at the intersection of health, medicine, and innovation",{size:23,ls:30,h:0.8,w:11.4});

const TEAM=[["suhan","Suhan Asaigoli ’27","Neuroscience","Morehead-Cain Scholar"],
            ["favor","Favor Asabor ’27","Health Policy & Management","Honors Carolina"],
            ["aidan","Aidan Gunn ’27","Communication Studies","Johnston Scholar"],
            ["niharika","Niharika Koppolu ’29","Biostatistics","Morehead-Cain Scholar"],
            ["amy","Amy Okonkwo ’28","Environmental Health Sciences","Morehead-Cain Scholar"]];
TEAM.forEach((t,i)=>{
  const x=M+i*2.32;
  s.addImage({path:A+t[0]+".png",x:x+0.30,y:2.70,w:1.44,h:1.44});
  T(s,t[1],{x:x-0.06,y:4.32,w:2.16,h:0.3,fontFace:DISP,fontSize:12.5,bold:true,color:MID,align:"center"});
  T(s,t[2],{x:x-0.06,y:4.64,w:2.16,h:0.3,fontFace:BODY,fontSize:10.5,color:SLATE,align:"center"});
  T(s,t[3],{x:x-0.06,y:4.92,w:2.16,h:0.3,fontFace:BODY,fontSize:10,color:"9AA3B2",align:"center"});
});

seg(s,M,5.62,W-M,5.62,"DCD8CC",1);
T(s,"Experience across",{x:M,y:5.80,w:3,h:0.26,fontFace:BODY,fontSize:9.5,bold:true,
  charSpacing:1.8,color:"9AA3B2"});
const AFF=[["aff_chai",1.26],["aff_uncsom",0.96],["aff_ncdhhs",1.42],["aff_heartland",1.12],
           ["aff_phrii",0.66],["aff_campusy",0.62],["aff_bme",0.84],["aff_ccn",1.00]];
let ax=M;
AFF.forEach(a=>{ s.addImage({path:A+a[0]+".png",x:ax,y:6.12,w:a[1],h:0.52}); ax+=a[1]+0.42; });

p.writeFile({fileName:"/Users/suhanasaigoli/Desktop/Projects/Astria/Astria-Pitch-Deck.pptx"})
 .then(f=>console.log("written",f));
