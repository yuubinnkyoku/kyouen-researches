#!/usr/bin/env node
'use strict';
// Exact proof-only conditional matching costs after the complete n22 terminal batch.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const previous=require('../n11-s5-post-targeted21-matching-20261027/audit.js');
const n22=require('../n11-s9-n22-complete-20261027/verify.js');
const need=(x,m)=>{if(!x)throw Error(m);};
const better=(a,b)=>!b||a.cost<b.cost||
 (a.cost===b.cost&&(a.total<b.total||(a.total===b.total&&a.s7<b.s7)));
function audit(negative=false){
 const cert=n22.verify({negative});
 need(cert.win9===115&&cert.loss9===775&&cert.newProofOnlyWin8===855&&
  cert.updated.missing===174,'n22 terminal certificate changed');
 const {candidates}=n22.inventory();
 const bytes=Buffer.from(JSON.parse(fs.readFileSync(path.join(__dirname,
  '../n11-s9-n22-complete-20261027/compact-certificate.json'),'utf8')).witnessBase64,'base64');
 const roots=candidates.filter((_,i)=>bytes[i]===255);
 need(roots.length===115,'WIN9 root reconstruction changed');
 const {before,loss}=n22.priorProofs();
 const after=new Set([...before,...g.reverse(roots)]);
 need(before.size===4089&&after.size===4944&&[...after].every(h=>!loss.has(h)),
  'proof-only WIN/LOSS conflict or census changed');
 const {by7}=base.inventory();
 const valid=new Map(),pairs=new Map(),single=Array(27).fill(null);
 let excluded=0,affected=0;
 for(const [s7,cover] of by7){
  const cs=g.children(g.board(s7,7));
  if([...cs].some(h=>loss.has(h))){excluded++;continue;}
  const r={s7,cover:[...cover].sort((a,b)=>a-b),total:cs.size,
   secured:[...cs].filter(h=>after.has(h)).length};
  r.cost=r.total-r.secured;
  need(r.cost>=0&&r.cover.length>=1&&r.cover.length<=2,'bad S7 candidate');
  valid.set(s7,r);
  if([...cs].some(h=>after.has(h)&&!before.has(h)))affected++;
  for(const i of r.cover)if(better(r,single[i]))single[i]=r;
  if(r.cover.length===2){
   const k=r.cover.join(':');
   if(better(r,pairs.get(k)))pairs.set(k,r);
  }
 }
 need(by7.size===853&&excluded===67&&valid.size===786&&pairs.size===343&&
  single.every(Boolean),'S7 candidate inventory changed');
 const old=previous.audit(false);
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
 const plan=fs.readFileSync(path.join(__dirname,
  '../n11-s5-pair-cover-20261026/s7-plan14-remaining.keys'),'utf8').trim().split(/\s+/);
 function evaluate(roots){
  need(roots.length===14&&new Set(roots).size===14,'invalid plan cardinality');
  let total=0,secured=0;const covered=new Set(),missing=new Set();
  for(const h of roots){
   need(valid.has(h),'invalid root candidate');
   for(const i of valid.get(h).cover)covered.add(i);
   for(const c of g.children(g.board(h,7))){
    total++;if(after.has(c))secured++;else missing.add(c);
   }
  }
  need(covered.size===27,'incomplete S6 coverage');
  return {total,secured,missing:total-secured,distinctMissing:missing.size};
 }
 const saved=evaluate(plan);
 need(saved.total===548&&saved.secured===374&&saved.missing===174&&
  saved.distinctMissing===174,'saved plan progress changed');
 if(negative){
  let rejected=false;try{evaluate(plan.slice(1));}catch(_){rejected=true;}
  need(rejected,'incomplete plan accepted');
  const witness=[...after].find(h=>!before.has(h)&&
   plan.some(root=>g.children(g.board(root,7)).has(h)));
  need(witness,'no newly secured saved-plan witness');
  const mutated=new Set(after);mutated.delete(witness);
  need([...plan].some(root=>[...g.children(g.board(root,7))].some(h=>h===witness&&
   !mutated.has(h))),'deleted WIN witness not detected');
 }
 return {schema:'n11-s5-post-n22-matching-v1',
  missingS6:27,proofOnlyWin8Before:4089,proofOnlyWin8After:4944,
  newlyProvedS8:855,knownLoss8:loss.size,
  candidates:by7.size,excluded,allowed:valid.size,
  affectedValidS7:affected,reducedPairCosts:reducedPairs,
  reducedSingleCosts:reducedSingles,
  pairOptions:[...pairs].map(([k,r])=>{
   const [i,j]=k.split(':').map(Number);
   return {i,j,s7:r.s7,total:r.total,secured:r.secured,cost:r.cost};
  }).sort((a,b)=>a.i-b.i||a.j-b.j),
  singleOptions:single.map((r,i)=>({i,s7:r.s7,total:r.total,
   secured:r.secured,cost:r.cost})),
  savedPlan:plan,saved,newS7Verdicts:0,newS5Verdicts:0,
  twoStoneClosures:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module)console.log(JSON.stringify(audit(process.argv.includes('--negative'))));
module.exports={audit};
