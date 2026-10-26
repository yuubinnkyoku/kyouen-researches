#!/usr/bin/env node
'use strict';
// Independently terminal-verified S10 WIN leaves -> S9 WIN -> S8 WIN.
// No incomplete df-pn, frozen WIN labels, or cache verdicts as proof leaves.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const prior=require('../n11-s9-degree2-terminal-20261027/verify.js');
const lossCert=require('../n11-s9-shared-loss-pruning-20261027/verify.js');
const EXP=path.resolve(__dirname,'..');
const need=(ok,msg)=>{if(!ok)throw Error(msg);};
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8');
const keys=p=>read(p).trim().split(/\s+/);
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function parse(raw){
 const lines=raw.trimEnd().split(/\r?\n/);
 need(lines[0]==='# n11-s9-degree2-short-terminal-v1'&&
  lines[1]==='# board=11 perspective=original-first-player'&&
  lines[2]==='# empty_board=UNKNOWN'&&
  lines[3]==='# s9_win canonical_s10_children terminal_states_per_geometry',
  'invalid certificate header');
 return lines.slice(4).map(line=>{
  const m=/^([0-9a-f]{32}) ([0-9]+) ([0-9]+)$/.exec(line);
  need(m,'invalid certificate row');
  return {s9:m[1],leaves:Number(m[2]),states:Number(m[3])};
 });
}
function verify(rows,{terminal=true}={}){
 need(rows.length===13,'wrong number of roots');
 const plan=keys('n11-s5-pair-cover-20261026/s7-plan14-remaining.keys');
 need(plan.length===14&&new Set(plan).size===14,'plan changed');
 const plan8=new Set(plan.flatMap(h=>[...g.children(g.board(h,7))]));
 need(plan8.size===547,'plan S8 boundary changed');
 const {win,loss}=base.inventory();
 need(win.size===2176&&loss.size===338,'previous proof inventory changed');
 const old5=JSON.parse(read('n11-s9-shared-plan14-20261027/certificate.json'));
 const old11=JSON.parse(read('n11-s9-shared-plan14-eleven-win-20261027/certificate.json'));
 const old14=prior.parse(read('n11-s9-degree2-terminal-20261027/certificate.tsv'));
 const old9=[...old5.witnesses,...old11.witnesses].map(x=>x.s9_win)
  .concat(old14.map(x=>x.s9));
 need(new Set(old9).size===30,'prior S9 WIN roots changed');
 const before=new Set([...win,'00000000000000821090a00000000020',...g.reverse(old9)]);
 need(before.size===2433&&[...before].every(h=>!loss.has(h)),
  'prior proof-only S8 WIN union changed');
 const oldS7=JSON.parse(read('n11-s7-terminal-loss12-20261024/certificate.json'));
 const loss10=new Set([...keys('n11-s8-to-s7-lift238-20261020/selected385.txt'),
  ...oldS7.s10_loss_cover39,...oldS7.s10_loss_cover12,
  ...keys('n11-s9-loss12-frontier-20261024/s10-loss12.keys'),
  ...lossCert.load().map(x=>x.s10)]);
 need(loss10.size===494,'previous terminal S10 LOSS inventory changed');
 const loss9=g.reverse([...loss10]);
 need(loss9.size===4807,'previous proof-only S9 LOSS closure changed');
 const roots=new Set(),derived=new Set(),touched=new Set(),leaves10=new Set();
 let edges10=0,states=0;
 for(const row of rows){
  need(!roots.has(row.s9)&&!old9.includes(row.s9),'duplicate S9 WIN root');
  roots.add(row.s9);
  need(Number.isSafeInteger(row.leaves)&&row.leaves>0&&
   Number.isSafeInteger(row.states)&&row.states>0,'invalid numeric field');
  need(!loss9.has(row.s9),'S9 WIN/LOSS conflict: '+row.s9);
  const b=g.board(row.s9,9);
  const child=g.children(b),other=ind.children4(row.s9);
  need(same(child,other)&&child.size===row.leaves,
   'incomplete S9 AND boundary: '+row.s9);
  const parents=g.reverse([row.s9]);
  need(parents.size===9,'S8 reverse boundary changed');
  const selected=[...parents].filter(h=>plan8.has(h));
  need(selected.length===2,'S9 root not degree-two in selected plan');
  for(const h of parents){
   need(!loss.has(h),'S8 WIN/LOSS conflict: '+h);
   need(g.children(g.board(h,8)).has(row.s9),'illegal S8->S9 edge');
   derived.add(h);
   if(plan8.has(h)){
    need(ind.children4(h).has(row.s9),'independent S8->S9 geometry mismatch');
    touched.add(h);
   }
  }
  let subtotal=0;
  for(const h of child){
   need(!loss10.has(h),'S10 WIN/LOSS conflict: '+h);
   leaves10.add(h);edges10++;
   if(terminal){
    const a=g.solve10(h),c=ind.solve4(h);
    need(a.win&&c.win,'false S10 WIN leaf: '+h);
    need(a.states===c.states&&a.legal===c.legal,
     'independent terminal disagreement: '+h);
    subtotal+=a.states;
   }
  }
  if(terminal)need(subtotal===row.states,'terminal state count changed: '+row.s9);
  states+=row.states;
 }
 need(edges10===187&&leaves10.size===183&&states===8318&&
  derived.size===113&&touched.size===22,'certificate census changed');
 const after=new Set([...before,...derived]);
 need([...after].every(h=>!loss.has(h)),'S8 WIN/LOSS union conflict');
 function evaluate(set){
  let total=0,secured=0;const missing=new Set();
  for(const h of plan)for(const c of g.children(g.board(h,7))){
   total++;if(set.has(c))secured++;else missing.add(c);
  }
  return {total,secured,missing:total-secured,distinctMissing:missing.size};
 }
 const previous=evaluate(before),updated=evaluate(after);
 need(previous.total===548&&previous.secured===88&&previous.missing===460&&
  previous.distinctMissing===460,'previous 14-root coverage changed');
 need(updated.missing<=460&&updated.distinctMissing===updated.missing,
  'updated 14-root coverage inconsistent');
 return {schema:'n11-s9-degree2-short-terminal-v1',
  newS9WinCertificates:roots.size,s10WinLeafEdges:edges10,
  distinctS10WinLeaves:leaves10.size,
  terminalStatesPerGeometry:terminal?states:null,
  independentGeometries:terminal?2:0,
  s8WinDerived:derived.size,newS8WinProofs:after.size-before.size,
  plan8Touched:touched.size,newlySecuredPlanEdges:updated.secured-previous.secured,
  previous,updated,winLossConflicts:0,newS7Verdicts:0,newS5Verdicts:0,
  newTwoStoneClosures:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module){
 const raw=fs.readFileSync(path.join(__dirname,'certificate.tsv'),'utf8');
 const rows=parse(raw),report=verify(rows);
 console.log(JSON.stringify(report,null,2));
 if(process.argv.includes('--negative')){
  const reject=(mutate,full=false)=>{
   const altered=structuredClone(rows);mutate(altered);let failed=false;
   try{verify(altered,{terminal:full});}catch(_){failed=true;}
   need(failed,'tampered certificate accepted');
  };
  reject(r=>r.pop());
  reject(r=>r[1].s9=r[0].s9);
  reject(r=>r[0].leaves++);
  reject(r=>r[0].states++,true);
  reject(r=>r[0].s9='00000000000000000000000000000000');
  let rejected=false;
  try{parse(raw.replace('empty_board=UNKNOWN','empty_board=WIN'));}
  catch(_){rejected=true;}
  need(rejected,'tampered header accepted');
  console.error('PASS six certificate mutation rejections');
 }
}
module.exports={parse,verify};
