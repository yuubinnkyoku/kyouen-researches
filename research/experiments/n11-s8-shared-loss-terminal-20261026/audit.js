#!/usr/bin/env node
'use strict';
// Proof-only reverse propagation of the independently terminal-certified S8
// original-first LOSS. Frozen caches are used only as conflict comparisons.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const previous=require('../n11-terminal-s7-s8-legacy187-union-20261025/audit.js');
const latest=require('../n11-s6-legacy3-loss-union-20261025/audit.js');
const s7Coverage=require('../n11-s9-neighbor23-s7-union-20261026/audit.js');
const EXP=path.resolve(__dirname,'..');
const ROOT='000000100010a0011000000001004000';
const need=(v,m)=>{if(!v)throw Error(m);};
const keys=p=>fs.readFileSync(path.join(EXP,p),'utf8').trim().split(/\s+/);
function audit(){
 const root=g.board(ROOT,8);
 const old8=new Set([...previous.certifiedLoss8(),...latest.source().cert.roots]);
 need(old8.size===76&&!old8.has(ROOT),'S8 LOSS source overlap/regression');
 const frozenLoss8=new Set(keys('n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'));
 const frozenWin8=new Set(keys('n11-targeted-terminal-lift-20261015/data/lifted_s8_win_51571.txt'));
 need(frozenLoss8.size===294&&frozenWin8.size===13501&&
   !frozenLoss8.has(ROOT)&&!frozenWin8.has(ROOT),
   'frozen S8 conflict or old label');
 const old7=g.reverse(old8),new7=g.reverse([ROOT]);
 const fresh7=new Set([...new7].filter(h=>!old7.has(h)));
 const all7=new Set([...old7,...new7]);
 need(old7.size===554&&new7.size===8,'S7 LOSS witness boundary changed');
 const frozenWin7=new Set(keys('n11-targeted-terminal-lift-20261015/data/all_s7_win_17.txt'));
 const frozenLoss7=new Set(keys('n11-targeted-terminal-lift-20261015/data/all_s7_loss_2232.txt'));
 need(frozenWin7.size===17&&frozenLoss7.size===2232&&
   [...new7].every(h=>!frozenWin7.has(h))&&
   [...fresh7].every(h=>!frozenLoss7.has(h)),
   'S7 WIN/LOSS conflict or frozen overlap');
 for(const h of new7){
   const b=g.board(h,7);
   need(g.children(b).has(ROOT),'S7 parent lacks legal S8 LOSS witness');
 }
 const old6=g.reverse(old7),all6=g.reverse(all7),new6=g.reverse(fresh7);
 const fresh6=new Set([...all6].filter(h=>!old6.has(h)));
 // A certified S6 WIN witnesses one secured S5 -> S6 edge. S5 WIN
 // would require ALL legal S6 children to be WIN: partial coverage is
 // never promoted to a verdict.
 const old5=g.reverse(old6),all5=g.reverse(all6),affected5=g.reverse(fresh6);
 const reverseEdges=roots=>{
   const edges=new Set();
   for(const h of roots){
     const b=g.board(h,6);
     for(const p of g.pts(b)){
       const parent=g.key(g.canonical(b^(1n<<BigInt(p))));
       edges.add(parent+':'+h);
     }
   }
   return edges;
 };
 const oldEdges=reverseEdges(old6),allEdges=reverseEdges(all6);
 need(old5.size===2896&&all5.size===2946&&affected5.size===56&&
   fresh6.size===27&&oldEdges.size===10260&&allEdges.size===10422&&
   [...oldEdges].every(e=>allEdges.has(e))&&
   allEdges.size-oldEdges.size===162,
   'S5 reverse proof-only coverage regression');
 // Forward legal-move enumeration must match the independent
 // reverse-deletion edge census on the newly affected S5 positions.
 const forwardEdges=new Set(),s5Frontier=[];
 let affectedLegal=0,affectedSecured=0,affectedRawSecured=0;
 for(const h of affected5){
   const b=g.board(h,5),classes=g.children(b);
   const secured=[...classes].filter(c=>all6.has(c));
   affectedLegal+=classes.size;
   affectedSecured+=secured.length;
   for(const c of secured)forwardEdges.add(h+':'+c);
   for(const p of g.legal(b)){
     const c=g.key(g.canonical(b|(1n<<BigInt(p))));
     if(all6.has(c))affectedRawSecured++;
   }
   s5Frontier.push({s5:h,legal:classes.size,secured:secured.length,
     uncovered:classes.size-secured.length});
 }
 s5Frontier.sort((a,b)=>a.uncovered-b.uncovered||
   b.secured-a.secured||a.s5.localeCompare(b.s5));
 const reverseAffected=new Set([...allEdges].filter(e=>affected5.has(e.slice(0,32))));
 need(affectedLegal===5328&&affectedSecured===271&&
   affectedRawSecured===271&&forwardEdges.size===271&&
   forwardEdges.size===reverseAffected.size&&
   [...forwardEdges].every(e=>reverseAffected.has(e))&&
   s5Frontier[0].s5==='00000000000100001000000042001000'&&
   s5Frontier[0].uncovered===53&&
   !s5Frontier.some(row=>row.uncovered===0),
   'S5 forward/reverse coverage or near-closure regression');
 // Recompute the full S6 universal boundary. One already certified S6
 // LOSS remains closed; the new S6 WIN roots are existential witnesses.
 let s6Legal=0,s6Secured=0;
 const closed6=[];
 for(const h of all6){
   const children=g.children(g.board(h,6));
   const secured=[...children].filter(c=>all7.has(c)).length;
   s6Legal+=children.size;s6Secured+=secured;
   if(secured===children.size)closed6.push(h);
 }
 need(s6Legal===134640&&s6Secured===3934&&
   closed6.length===1&&
   closed6[0]==='00000000040004001004000004010000',
   'S6 full-child proof-only coverage regression');
 need(old6.size===1710&&[...old6].every(h=>all6.has(h)),
   'previous S6 WIN reverse coverage changed');
 need(fresh7.size===8&&all7.size===562&&new6.size===28&&
   all6.size===1737&&all6.size-old6.size===27,
   'new S7 LOSS / S6 WIN proof-only union regression');
 for(const h of new6){
   const b=g.board(h,6);
   need([...g.children(b)].some(c=>fresh7.has(c)),
     'S6 WIN parent lacks legal S7 LOSS witness');
 }
 // The older S7 near-closure list was assembled BEFORE this S8 LOSS was
 // terminal-certified. Any S7 parent with a proven S8 LOSS child is itself
 // proven LOSS (original-first viewpoint) and cannot be an S7 WIN target.
 // Keep the original S7 audit immutable; derive a new proof-only worklist.
 const historical=s7Coverage.audit().proofOnlyFrontier;
 const near7=historical.closestS7.filter(row=>
   row.uncovered<=historical.nearGapThreshold);
 need(near7.length===historical.nearS7Parents&&near7.length===5,
   'historical S7 near frontier incomplete');
 const newlyRefutedNear=near7.filter(row=>row.missingS8.includes(ROOT));
 need(newlyRefutedNear.length===2&&
   newlyRefutedNear.every(row=>all7.has(row.s7)),
   'new S8 LOSS did not refute the expected two S7 WIN targets');
 const refutedNear=near7.filter(row=>all7.has(row.s7));
 const actionableNear=near7.filter(row=>!all7.has(row.s7));
 need(refutedNear.length>=2&&actionableNear.length>0,
   'S7 near frontier pruning regression');
 const knownLoss8=new Set([...old8,ROOT]);
 const frequencies=new Map();
 for(const row of actionableNear){
   const legal=g.children(g.board(row.s7,7));
   for(const h of row.missingS8){
     need(legal.has(h)&&!knownLoss8.has(h),
       'S7 actionable target illegal or already proven S8 LOSS');
     const parents=frequencies.get(h)||[];
     parents.push(row.s7);frequencies.set(h,parents);
   }
 }
 const nextS8Targets=[...frequencies].sort((a,b)=>
   b[1].length-a[1].length||a[0].localeCompare(b[0]))
   .slice(0,15).map(([s8,parents])=>({s8,nearS7Parents:parents.length,
     parents:parents.sort()}));
 need(nextS8Targets.length>0&&
   nextS8Targets.every(row=>!knownLoss8.has(row.s8)),
   'proven S8 LOSS leaked into actionable S7 worklist');
 const s7ProofOnlyWorklist={
   scope:'historical newly affected S7 parents with gap <=26 only',
   historicalNearS7:near7.length,
   refutedNearS7:refutedNear.map(row=>row.s7).sort(),
   newlyRefutedBySharedS8: new Set(newlyRefutedNear.map(row=>row.s7)).size,
   remainingNearS7:actionableNear.map(row=>({
     s7:row.s7,legal:row.legal,secured:row.secured,
     uncovered:row.uncovered})),
   nextS8Targets,
   proofRule:'S7 with a certified S8 LOSS child is LOSS, not a WIN-coverage target'
 };
 return {s8LossRoot:ROOT,priorCertifiedS8Loss:old8.size,newCertifiedS8Loss:1,
   certifiedS8Loss:old8.size+1,
   previousS7Loss:old7.size,newS7LossWitnessParents:new7.size,
   addedS7Loss:fresh7.size,totalS7Loss:all7.size,
   previousS6Win:old6.size,affectedS6Win:new6.size,
   addedS6Win:all6.size-old6.size,totalS6Win:all6.size,
   s7LossParents:[...new7].sort(),newS6WinParents:[...all6].filter(h=>!old6.has(h)).sort(),
   previousS5Parents:old5.size,addedS5Parents:all5.size-old5.size,
   totalS5Parents:all5.size,affectedS5Parents:affected5.size,
   previousSecuredS5ClassEdges:oldEdges.size,
   addedSecuredS5ClassEdges:allEdges.size-oldEdges.size,
   securedS5ClassEdges:allEdges.size,
   affectedS5LegalClasses:affectedLegal,
   affectedS5SecuredClasses:affectedSecured,
   affectedS5SecuredRawMoves:affectedRawSecured,
   closestAffectedS5:s5Frontier.slice(0,5),
   newlyClosedS5:0,previousS6LegalClasses:132573,
   totalS6LegalClasses:s6Legal,previousSecuredS6Classes:3878,
   securedS6Classes:s6Secured,addedSecuredS6Classes:s6Secured-3878,
   closedS6:closed6.sort(),newlyClosedS6:0,
   s7ProofOnlyWorklist,frozenConflicts:0,emptyBoard:'UNKNOWN'};
}
module.exports={audit};
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
