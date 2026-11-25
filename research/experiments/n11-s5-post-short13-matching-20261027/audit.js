#!/usr/bin/env node
'use strict';
// Re-optimize the conditional 14-root plan after thirteen terminal-proved S9 WIN roots.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const previous=require('../n11-s5-post-degree2-matching-20261027/audit.js');
const short=require('../n11-s9-degree2-short-terminal-20261027/verify.js');
const EXP=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8');
const need=(ok,msg)=>{if(!ok)throw Error(msg);};
const children=h=>g.children(g.board(h,7));
const id=(a,b)=>a+':'+b;
const better=(a,b)=>!b||a.cost<b.cost||
  (a.cost===b.cost&&(a.total<b.total||
  (a.total===b.total&&a.s7<b.s7)));
function audit(negative=false){
 const old=previous.audit(false);
 const rows=short.parse(read('n11-s9-degree2-short-terminal-20261027/certificate.tsv'));
 const proof=short.verify(rows,{terminal:true});
 const {missing,by7,win,loss}=base.inventory();
 need(old.schema==='n11-s5-post-degree2-matching-v1'&&
  old.updated.missing===460&&old.proofOnlyWin8After===2433&&
  proof.newS8WinProofs===83&&proof.updated.missing===447&&
  missing.length===27&&by7.size===853&&win.size===2176&&loss.size===338,
  'upstream proof or candidate inventory changed');
 const cert5=JSON.parse(read('n11-s9-shared-plan14-20261027/certificate.json'));
 const cert11=JSON.parse(read('n11-s9-shared-plan14-eleven-win-20261027/certificate.json'));
 const cert14=require('../n11-s9-degree2-terminal-20261027/verify.js')
  .parse(read('n11-s9-degree2-terminal-20261027/certificate.tsv'));
 const prior9=[...cert5.witnesses,...cert11.witnesses].map(r=>r.s9_win)
  .concat(cert14.map(r=>r.s9));
 const before=new Set([...win,'00000000000000821090a00000000020',
  ...g.reverse(prior9)]);
 const derived=g.reverse(rows.map(r=>r.s9));
 const after=new Set([...before,...derived]);
 need(before.size===2433&&after.size===2516&&
  [...after].every(h=>!loss.has(h)),
  'proof-only S8 WIN union changed or WIN/LOSS conflict');
 const valid=new Map(),pairs=new Map(),single=Array(27).fill(null);
 let excluded=0,affected=0;
 for(const [s7,cover] of by7){
  const cs=children(s7);
  if([...cs].some(h=>loss.has(h))){excluded++;continue;}
  const row={s7,cover:[...cover].sort((a,b)=>a-b),total:cs.size,
   secured:[...cs].filter(h=>after.has(h)).length};
  row.cost=row.total-row.secured;
  need(row.cost>=0&&row.cover.length>=1&&row.cover.length<=2,
   'invalid candidate');
  valid.set(s7,row);
  if([...cs].some(h=>derived.has(h)&&!before.has(h)))affected++;
  for(const i of row.cover)if(better(row,single[i]))single[i]=row;
  if(row.cover.length===2){
   const k=id(...row.cover);
   if(better(row,pairs.get(k)))pairs.set(k,row);
  }
 }
 need(excluded===67&&valid.size===786&&pairs.size===343&&
  single.every(Boolean),'candidate census changed');
 const oldPairs=new Map(old.pairOptions.map(r=>[id(r.i,r.j),r.cost]));
 let reducedPairs=0,reducedSingles=0;
 for(const [k,r] of pairs){
  need(oldPairs.has(k)&&r.cost<=oldPairs.get(k),'pair cost increased');
  if(r.cost<oldPairs.get(k))reducedPairs++;
 }
 for(let i=0;i<27;i++){
  need(single[i].cost<=old.singleOptions[i].cost,'single cost increased');
  if(single[i].cost<old.singleOptions[i].cost)reducedSingles++;
 }
 const plan=read('n11-s5-pair-cover-20261026/s7-plan14-remaining.keys')
  .trim().split(/\s+/);
 function evaluate(roots,proofs){
  need(roots.length===14&&new Set(roots).size===14,'invalid plan roots');
  const covered=new Set(),unproved=new Set();let total=0,secured=0;
  for(const h of roots){
   need(valid.has(h),'invalid plan candidate');
   for(const i of valid.get(h).cover)covered.add(i);
   const cs=children(h);total+=cs.size;
   for(const c of cs)if(proofs.has(c))secured++;else unproved.add(c);
  }
  need(covered.size===27,'incomplete S6 coverage');
  return {total,secured,missing:total-secured,distinctMissing:unproved.size};
 }
 const prior=evaluate(plan,before),updated=evaluate(plan,after);
 need(prior.total===548&&prior.secured===88&&prior.missing===460&&
  updated.total===548&&updated.secured===101&&updated.missing===447&&
  updated.distinctMissing===447,'fixed-plan coverage changed');
 if(negative){
  let rejected=false;
  try{evaluate(plan.slice(1),after);}catch(_){rejected=true;}
  need(rejected,'incomplete plan accepted');
  const witness=[...derived].find(h=>!before.has(h)&&
   plan.some(p=>children(p).has(h)));
  need(witness&&evaluate(plan,new Set([...after].filter(h=>h!==witness))).missing===448,
   'removing proof failed to reopen an edge');
  const conflict=new Set(after);conflict.add([...loss][0]);
  need([...conflict].some(h=>loss.has(h)),'WIN/LOSS conflict negative control failed');
 }
 return {schema:'n11-s5-post-short13-matching-v1',missingS6:missing.length,
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
  savedPlan:plan,previous:prior,updated,
  newS7Verdicts:0,newS5Verdicts:0,twoStoneClosures:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module)console.log(JSON.stringify(audit(process.argv.includes('--negative'))));
module.exports={audit};
