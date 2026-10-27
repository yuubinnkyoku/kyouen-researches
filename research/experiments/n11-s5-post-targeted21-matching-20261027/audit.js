#!/usr/bin/env node
'use strict';
// Proof-only conditional 14-root matching, following nine terminal S9 WIN proofs.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const prev=require('../n11-s5-post-n20-matching-20261027/audit.js');
const target=require('../n11-s9-targeted-gap266-20261027/verify.js');
const p14=require('../n11-s9-degree2-terminal-20261027/verify.js');
const p13=require('../n11-s9-degree2-short-terminal-20261027/verify.js');
const p46=require('../n11-s9-short46-terminal-20261027/verify.js');
const p12=require('../n11-s9-short18-terminal-20261027/verify.js');
const p55=require('../n11-s9-n19-terminal-20261027/verify.js');
const p80=require('../n11-s9-n20-terminal-20261027/verify.js');
const EXP=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8');
const need=(x,m)=>{if(!x)throw Error(m);};
const children=h=>g.children(g.board(h,7));
const better=(a,b)=>!b||a.cost<b.cost||(a.cost===b.cost&&
 (a.total<b.total||(a.total===b.total&&a.s7<b.s7)));
function audit(negative=false){
 const old=prev.audit(false);
 const rows=target.parse(read('n11-s9-targeted-gap266-20261027/certificate.tsv'));
 // A standalone audit must independently replay the new terminal certificate;
 // metadata-only checking cannot justify adding these WIN leaves to proof coverage.
 const cert=target.verify(rows);
 need(cert.independentGeometries===2&&cert.terminalStatesPerGeometry===25222,
  'targeted S9 terminal replay was not performed');
 const {missing,by7,win,loss}=base.inventory();
 need(old.proofOnlyWin8After===4011&&old.updated.missing===266&&
  cert.newS9Win===9&&cert.newS8Win===78&&cert.updated.missing===250&&
  missing.length===27&&by7.size===853&&win.size===2176&&loss.size===338,
  'upstream proof/candidate inventory changed');
 const c5=JSON.parse(read('n11-s9-shared-plan14-20261027/certificate.json'));
 const c11=JSON.parse(read('n11-s9-shared-plan14-eleven-win-20261027/certificate.json'));
 const old9=[...c5.witnesses,...c11.witnesses].map(x=>x.s9_win).concat(
  p14.parse(read('n11-s9-degree2-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  p13.parse(read('n11-s9-degree2-short-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  p46.parse(read('n11-s9-short46-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  p12.parse(read('n11-s9-short18-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  p55.parse(read('n11-s9-n19-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  p80.parse(read('n11-s9-n20-terminal-20261027/certificate.tsv')).map(x=>x.s9));
 need(new Set(old9).size===236,'old S9 witnesses changed');
 const before=new Set([...win,'00000000000000821090a00000000020',...g.reverse(old9)]);
 const derived=g.reverse(rows.map(r=>r.s9));
 const after=new Set([...before,...derived]);
 need(before.size===4011&&after.size===4089&&[...after].every(h=>!loss.has(h)),
  'S8 WIN/LOSS conflict or unexpected proof coverage');
 const valid=new Map(),pairs=new Map(),single=Array(27).fill(null);
 let excluded=0,affected=0;
 for(const [s7,cover] of by7){
  const cs=children(s7);
  if([...cs].some(h=>loss.has(h))){excluded++;continue;}
  const r={s7,cover:[...cover].sort((a,b)=>a-b),total:cs.size,
   secured:[...cs].filter(h=>after.has(h)).length};
  r.cost=r.total-r.secured;
  need(r.cost>=0&&r.cover.length>=1&&r.cover.length<=2,'bad S7 candidate');
  valid.set(s7,r);
  if([...cs].some(h=>derived.has(h)&&!before.has(h)))affected++;
  for(const i of r.cover)if(better(r,single[i]))single[i]=r;
  if(r.cover.length===2){
   const k=r.cover.join(':');
   if(better(r,pairs.get(k)))pairs.set(k,r);
  }
 }
 need(excluded===67&&valid.size===786&&pairs.size===343&&
  single.every(Boolean),'S7 candidate census changed');
 const oldPairs=new Map(old.pairOptions.map(r=>[r.i+':'+r.j,r.cost]));
 let reducedPairs=0,reducedSingles=0;
 for(const [k,r] of pairs){
  need(oldPairs.has(k)&&r.cost<=oldPairs.get(k),'pair cost increased');
  if(r.cost<oldPairs.get(k))reducedPairs++;
 }
 for(let i=0;i<27;i++){
  need(single[i].cost<=old.singleOptions[i].cost,'single cost increased');
  if(single[i].cost<old.singleOptions[i].cost)reducedSingles++;
 }
 const plan=read('n11-s5-pair-cover-20261026/s7-plan14-remaining.keys').trim().split(/\s+/);
 function evaluate(roots,proofs){
  need(roots.length===14&&new Set(roots).size===14,'invalid root set');
  let total=0,secured=0;const covered=new Set(),unproved=new Set();
  for(const h of roots){
   need(valid.has(h),'invalid root candidate');
   for(const i of valid.get(h).cover)covered.add(i);
   for(const c of children(h)){
    total++;
    if(proofs.has(c))secured++;else unproved.add(c);
   }
  }
  need(covered.size===27,'incomplete S6 coverage');
  return {total,secured,missing:total-secured,distinctMissing:unproved.size};
 }
 const previous=evaluate(plan,before),updated=evaluate(plan,after);
 need(previous.total===548&&previous.secured===282&&previous.missing===266&&
  updated.total===548&&updated.secured===298&&updated.missing===250&&
  updated.distinctMissing===250,'fixed plan proof census changed');
 if(negative){
  let rejected=false;try{evaluate(plan.slice(1),after);}catch(_){rejected=true;}
  need(rejected,'incomplete plan accepted');
  const witness=[...derived].find(h=>!before.has(h)&&plan.some(root=>children(root).has(h)));
  need(witness&&evaluate(plan,new Set([...after].filter(h=>h!==witness))).missing>250,
   'proof deletion not detected');
  const conflict=new Set(after);conflict.add([...loss][0]);
  need([...conflict].some(h=>loss.has(h)),'conflict control failed');
 }
 return {schema:'n11-s5-post-targeted21-matching-v1',missingS6:27,
  proofOnlyWin8Before:before.size,proofOnlyWin8After:after.size,
  newlyProvedS8:after.size-before.size,knownLoss8:loss.size,
  candidates:by7.size,excluded,allowed:valid.size,
  affectedValidS7:affected,reducedPairCosts:reducedPairs,
  reducedSingleCosts:reducedSingles,
  pairOptions:[...pairs].map(([k,r])=>{
   const [i,j]=k.split(':').map(Number);
   return {i,j,s7:r.s7,total:r.total,secured:r.secured,cost:r.cost};
  }).sort((a,b)=>a.i-b.i||a.j-b.j),
  singleOptions:single.map((r,i)=>({i,s7:r.s7,total:r.total,
   secured:r.secured,cost:r.cost})),
  savedPlan:plan,previous,updated,
  newS7Verdicts:0,newS5Verdicts:0,twoStoneClosures:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module)console.log(JSON.stringify(audit(process.argv.includes('--negative'))));
module.exports={audit};
