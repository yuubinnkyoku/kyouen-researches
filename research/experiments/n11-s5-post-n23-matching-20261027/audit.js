#!/usr/bin/env node
'use strict';
// Re-optimize conditional 14-root obligations only after replaying n23 terminal evidence.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const previous=require('../n11-s5-post-n22-matching-20261027/audit.js');
const n22=require('../n11-s9-n22-complete-20261027/verify.js');
const n23=require('../n11-s9-n23-priority-20261027/prove.js');
const need=(x,m)=>{if(!x)throw Error(m);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const better=(a,b)=>!b||a.cost<b.cost||
 (a.cost===b.cost&&(a.total<b.total||(a.total===b.total&&a.s7<b.s7)));
function audit(negative=false){
 // This replays every selected n23 9->10 child through both integer geometries.
 const terminal=n23.run();
 need(terminal.win9===21&&terminal.loss9===235&&
  terminal.proofOnlyWin8Before===4944&&terminal.proofOnlyWin8After===5120&&
  terminal.updated.total===548&&terminal.updated.secured===404&&
  terminal.updated.missing===144,'n23 terminal boundary changed');
 const {by9,plan,plan8,candidates}=n22.inventory();
 const {before,loss}=n22.priorProofs();
 const oldCert=JSON.parse(fs.readFileSync(path.join(__dirname,
  '../n11-s9-n22-complete-20261027/compact-certificate.json'),'utf8'));
 const oldBytes=Buffer.from(oldCert.witnessBase64,'base64');
 need(oldBytes.length===candidates.length,'n22 candidate certificate changed');
 const oldWin9=candidates.filter((_,i)=>oldBytes[i]===255);
 const secured=new Set([...before,...g.reverse(oldWin9)]);
 need(secured.size===4944,'n22 proof-only WIN8 count changed');
 const choices=[];
 for(const [h,parents] of by9){
  if(parents.size<2||g.children(g.board(h,9)).size!==23)continue;
  const gaps=[...parents].filter(p=>plan8.has(p)&&!secured.has(p)).length;
  choices.push({h,degree:parents.size,gaps});
 }
 choices.sort((a,b)=>b.gaps-a.gaps||b.degree-a.degree||
  (a.h<b.h?-1:a.h>b.h?1:0));
 const positive=choices.filter(x=>x.gaps>0);
 const selected=positive.slice(0,256);
 need(choices.length===terminal.candidates&&
  positive.length===terminal.positiveGapCandidates&&
  selected.length===terminal.selected&&
  sha(selected.map(x=>x.h).join('\n')+'\n')===terminal.selectionSha256,
  'n23 frozen candidate order changed');
 const cert=JSON.parse(fs.readFileSync(path.join(__dirname,
  '../n11-s9-n23-priority-20261027/compact-certificate.json'),'utf8'));
 const bytes=Buffer.from(cert.witnessBase64,'base64');
 need(bytes.length===selected.length&&bytes.toString('base64')===cert.witnessBase64&&
  sha(bytes)===cert.witnessSha256,'n23 witness bytes changed');
 const win9=selected.filter((_,i)=>bytes[i]===255).map(x=>x.h);
 need(win9.length===21,'n23 WIN9 count changed');
 const derived=g.reverse(win9);
 need(derived.size===terminal.derivedWin8,'n23 reverse-parent count changed');
 const after=new Set([...secured,...derived]);
 need(after.size===5120&&[...after].every(h=>!loss.has(h)),
  'proof-only WIN8 conflict or census changed');
 const {by7}=base.inventory();
 const valid=new Map(),pairs=new Map(),single=Array(27).fill(null);
 let excluded=0,affected=0;
 for(const [s7,cover] of by7){
  const cs=g.children(g.board(s7,7));
  if([...cs].some(h=>loss.has(h))){excluded++;continue;}
  const r={s7,cover:[...cover].sort((a,b)=>a-b),total:cs.size,
   secured:[...cs].filter(h=>after.has(h)).length};
  r.cost=r.total-r.secured;
  need(r.cost>=0&&r.cover.length>=1&&r.cover.length<=2,'invalid S7 option');
  valid.set(s7,r);
  if([...cs].some(h=>after.has(h)&&!secured.has(h)))affected++;
  for(const i of r.cover)if(better(r,single[i]))single[i]=r;
  if(r.cover.length===2){
   const k=r.cover.join(':');
   if(better(r,pairs.get(k)))pairs.set(k,r);
  }
 }
 need(by7.size===853&&excluded===67&&valid.size===786&&pairs.size===343&&
  single.every(Boolean),'S7 inventory changed');
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
 function evaluate(roots){
  need(roots.length===14&&new Set(roots).size===14,'invalid plan cardinality');
  let total=0,securedEdges=0;const covered=new Set(),missing=new Set();
  for(const h of roots){
   need(valid.has(h),'invalid S7 candidate');
   for(const i of valid.get(h).cover)covered.add(i);
   for(const c of g.children(g.board(h,7))){
    total++;if(after.has(c))securedEdges++;else missing.add(c);
   }
  }
  need(covered.size===27,'incomplete S6 coverage');
  return {total,secured:securedEdges,missing:total-securedEdges,
   distinctMissing:missing.size};
 }
 const saved=evaluate(plan);
 need(saved.total===548&&saved.secured===404&&saved.missing===144&&
  saved.distinctMissing===144,'fixed 14-root frontier changed');
 if(negative){
  let rejected=false;try{evaluate(plan.slice(1));}catch(_){rejected=true;}
  need(rejected,'incomplete plan accepted');
  const witness=[...derived].find(h=>!secured.has(h)&&
   plan.some(root=>g.children(g.board(root,7)).has(h)));
  need(witness,'no new plan-covered WIN8 witness');
  const mutated=new Set(after);mutated.delete(witness);
  need(plan.some(root=>[...g.children(g.board(root,7))].some(h=>
   h===witness&&!mutated.has(h))),'removed WIN8 witness undetected');
 }
 return {schema:'n11-s5-post-n23-matching-v1',missingS6:27,
  proofOnlyWin8Before:4944,proofOnlyWin8After:5120,newlyProvedS8:176,
  knownLoss8:loss.size,candidates:by7.size,excluded,allowed:valid.size,
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
