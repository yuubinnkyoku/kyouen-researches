#!/usr/bin/env node
'use strict';
// Forty-six new S9 WIN witnesses, independently checked to terminal positions.
// No truncated search, frozen verdict cache or pn/dn is accepted as a leaf.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const degree2=require('../n11-s9-degree2-terminal-20261027/verify.js');
const short=require('../n11-s9-degree2-short-terminal-20261027/verify.js');
const lossCert=require('../n11-s9-shared-loss-pruning-20261027/verify.js');
const EXP=path.resolve(__dirname,'..');
const need=(x,msg)=>{if(!x)throw Error(msg);};
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8');
const keys=p=>read(p).trim().split(/\s+/);
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function parse(raw){
 const lines=raw.trimEnd().split(/\r?\n/);
 need(lines[0]==='# n11-s9-short46-terminal-v1'&&
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
 need(rows.length===46,'wrong number of roots');
 const plan=keys('n11-s5-pair-cover-20261026/s7-plan14-remaining.keys');
 need(plan.length===14&&new Set(plan).size===14,'plan changed');
 const plan8=new Set(plan.flatMap(h=>[...g.children(g.board(h,7))]));
 need(plan8.size===547,'plan S8 boundary changed');
 const {win,loss}=base.inventory();
 need(win.size===2176&&loss.size===338,'base proof inventory changed');
 const old5=JSON.parse(read('n11-s9-shared-plan14-20261027/certificate.json'));
 const old11=JSON.parse(read('n11-s9-shared-plan14-eleven-win-20261027/certificate.json'));
 const old14=degree2.parse(read('n11-s9-degree2-terminal-20261027/certificate.tsv'));
 const old13=short.parse(read('n11-s9-degree2-short-terminal-20261027/certificate.tsv'));
 const prior9=[...old5.witnesses,...old11.witnesses].map(x=>x.s9_win)
  .concat(old14.map(x=>x.s9),old13.map(x=>x.s9));
 const priorSet=new Set(prior9);
 need(priorSet.size===43,'prior S9 WIN root inventory changed');
 const before=new Set([...win,'00000000000000821090a00000000020',
  ...g.reverse(prior9)]);
 need(before.size===2516&&[...before].every(h=>!loss.has(h)),
  'prior S8 proof-only WIN union changed');
 const oldS7=JSON.parse(read('n11-s7-terminal-loss12-20261024/certificate.json'));
 const loss10=new Set([...keys('n11-s8-to-s7-lift238-20261020/selected385.txt'),
  ...oldS7.s10_loss_cover39,...oldS7.s10_loss_cover12,
  ...keys('n11-s9-loss12-frontier-20261024/s10-loss12.keys'),
  ...lossCert.load().map(x=>x.s10)]);
 need(loss10.size===494,'S10 LOSS proof inventory changed');
 const loss9=g.reverse([...loss10]);
 need(loss9.size===4807,'S9 LOSS proof-only closure changed');
 const roots=new Set(),derived=new Set(),touched=new Set(),leaves10=new Set();
 let edges=0,states=0;
 for(const row of rows){
  need(!roots.has(row.s9)&&!priorSet.has(row.s9),'duplicate or old S9 WIN root');
  roots.add(row.s9);
  need(Number.isSafeInteger(row.leaves)&&row.leaves>0&&
   Number.isSafeInteger(row.states)&&row.states>0,'invalid numeric field');
  need(!loss9.has(row.s9),'S9 WIN/LOSS conflict: '+row.s9);
  const children=g.children(g.board(row.s9,9));
  need(same(children,ind.children4(row.s9))&&children.size===row.leaves,
   'incomplete or incorrect S9 AND boundary: '+row.s9);
  const parents=g.reverse([row.s9]);
  need(parents.size===9,'S8 reverse boundary changed');
  const degree=[...parents].filter(h=>plan8.has(h)).length;
  need(degree===2||degree===3,'unexpected S9 plan-parent degree');
  for(const h of parents){
   need(!loss.has(h),'S8 WIN/LOSS conflict: '+h);
   need(g.children(g.board(h,8)).has(row.s9)&&
    ind.children4(h).has(row.s9),'S8->S9 edge disagreement: '+h);
   derived.add(h);
   if(plan8.has(h))touched.add(h);
  }
  let subtotal=0;
  for(const h of children){
   need(!loss10.has(h),'S10 WIN/LOSS conflict: '+h);
   leaves10.add(h);edges++;
   if(terminal){
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win&&b.win&&a.states===b.states&&a.legal===b.legal,
     'independent terminal WIN disagreement: '+h);
    subtotal+=a.states;
   }
  }
  if(terminal)need(subtotal===row.states,'terminal states changed: '+row.s9);
  states+=row.states;
 }
 need(roots.size===46&&edges===766&&leaves10.size===755&&
  states===52401&&derived.size===395&&touched.size===74,
  'certificate census changed');
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
 need(previous.total===548&&previous.secured===101&&previous.missing===447&&
  previous.distinctMissing===447,'prior plan proof coverage changed');
 need(updated.secured>previous.secured&&updated.missing<447&&
  updated.distinctMissing===updated.missing,'no verified plan progress');
 return {schema:'n11-s9-short46-terminal-v1',newS9Win:46,
  s10WinLeafEdges:edges,distinctS10WinLeaves:leaves10.size,
  terminalStatesPerGeometry:terminal?states:null,
  independentGeometries:terminal?2:0,
  derivedS8Win:derived.size,newS8Win:after.size-before.size,
  proofOnlyS8WinAfter:after.size,plan8Touched:touched.size,
  newlySecuredPlanEdges:updated.secured-previous.secured,
  previous,updated,winLossConflicts:0,newS7Verdicts:0,
  newS5Verdicts:0,newTwoStoneClosures:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module){
 const raw=fs.readFileSync(path.join(__dirname,'certificate.tsv'),'utf8');
 const rows=parse(raw),result=verify(rows);
 console.log(JSON.stringify(result,null,2));
 if(process.argv.includes('--negative')){
  const reject=(mutate,full=false)=>{
   const altered=structuredClone(rows);mutate(altered);let rejected=false;
   try{verify(altered,{terminal:full});}catch(_){rejected=true;}
   need(rejected,'tampered certificate accepted');
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
