#!/usr/bin/env node
'use strict';
// Independently recheck 9 newly discovered original-first WIN S9 roots:
// every legal S10 child is a terminal WIN by two different integer geometries.
// No truncated search, pn/dn, or cached verdict is a proof leaf.
const fs=require('node:fs'),path=require('node:path');
const EXP=path.resolve(__dirname,'..');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const p14=require('../n11-s9-degree2-terminal-20261027/verify.js');
const p13=require('../n11-s9-degree2-short-terminal-20261027/verify.js');
const p46=require('../n11-s9-short46-terminal-20261027/verify.js');
const p12=require('../n11-s9-short18-terminal-20261027/verify.js');
const p55=require('../n11-s9-n19-terminal-20261027/verify.js');
const p80=require('../n11-s9-n20-terminal-20261027/verify.js');
const lossCert=require('../n11-s9-shared-loss-pruning-20261027/verify.js');
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8');
const keys=p=>read(p).trim().split(/\s+/);
const need=(ok,msg)=>{if(!ok)throw Error(msg);};
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function parse(raw){
 const lines=raw.trimEnd().split(/\r?\n/);
 need(lines.length===13&&lines[0]==='# n11-s9-targeted-gap266-terminal-v1'&&
  lines[1]==='# board=11 perspective=original-first-player'&&
  lines[2]==='# empty_board=UNKNOWN'&&
  lines[3]==='# s9_win canonical_s10_children terminal_states_per_geometry',
  'invalid certificate header/count');
 return lines.slice(4).map(line=>{
  const m=/^([0-9a-f]{32}) (21) ([0-9]+)$/.exec(line);
  need(m,'invalid certificate row');
  return {s9:m[1],leaves:Number(m[2]),states:Number(m[3])};
 });
}
function verify(rows,{terminal=true}={}){
 need(Array.isArray(rows)&&rows.length===9,'wrong root count');
 const plan=keys('n11-s5-pair-cover-20261026/s7-plan14-remaining.keys');
 const plan8=new Set(plan.flatMap(h=>[...g.children(g.board(h,7))]));
 const {win,loss}=base.inventory();
 need(plan.length===14&&plan8.size===547&&win.size===2176&&loss.size===338,
  'upstream plan/candidate inventory changed');
 const c5=JSON.parse(read('n11-s9-shared-plan14-20261027/certificate.json'));
 const c11=JSON.parse(read('n11-s9-shared-plan14-eleven-win-20261027/certificate.json'));
 const old9=[...c5.witnesses,...c11.witnesses].map(x=>x.s9_win)
  .concat(p14.parse(read('n11-s9-degree2-terminal-20261027/certificate.tsv')).map(x=>x.s9),
   p13.parse(read('n11-s9-degree2-short-terminal-20261027/certificate.tsv')).map(x=>x.s9),
   p46.parse(read('n11-s9-short46-terminal-20261027/certificate.tsv')).map(x=>x.s9),
   p12.parse(read('n11-s9-short18-terminal-20261027/certificate.tsv')).map(x=>x.s9),
   p55.parse(read('n11-s9-n19-terminal-20261027/certificate.tsv')).map(x=>x.s9),
   p80.parse(read('n11-s9-n20-terminal-20261027/certificate.tsv')).map(x=>x.s9));
 const prior9=new Set(old9);
 need(prior9.size===236,'upstream S9 witness inventory changed');
 const before=new Set([...win,'00000000000000821090a00000000020',
  ...g.reverse(old9)]);
 const missing=new Set([...plan8].filter(h=>!before.has(h)));
 need(before.size===4011&&missing.size===266&&
  [...before].every(h=>!loss.has(h)),'upstream proof-only S8 frontier changed');
 const old7=JSON.parse(read('n11-s7-terminal-loss12-20261024/certificate.json'));
 const loss10=new Set([...keys('n11-s8-to-s7-lift238-20261020/selected385.txt'),
  ...old7.s10_loss_cover39,...old7.s10_loss_cover12,
  ...keys('n11-s9-loss12-frontier-20261024/s10-loss12.keys'),
  ...lossCert.load().map(x=>x.s10)]);
 need(loss10.size===494,'known terminal LOSS inventory changed');
 const loss9=g.reverse([...loss10]);
 need(loss9.size===4807,'known S9 LOSS inventory changed');
 const roots=new Set(),derived=new Set(),touched=new Set(),leaves10=new Set();
 let edges=0,states=0;
 for(const row of rows){
  need(!roots.has(row.s9)&&!prior9.has(row.s9),'duplicate/previous S9 WIN');
  roots.add(row.s9);
  need(!loss9.has(row.s9),'S9 WIN/LOSS conflict: '+row.s9);
  need(Number.isSafeInteger(row.states)&&row.states>0&&row.leaves===21,
   'invalid certificate metadata');
  const actual=g.children(g.board(row.s9,9));
  need(actual.size===21&&same(actual,ind.children4(row.s9)),
   'incomplete/incorrect 9-to-10 AND boundary: '+row.s9);
  const parents=g.reverse([row.s9]);
  need(parents.size===9,'incorrect S8 reverse boundary');
  const unknownParents=[...parents].filter(h=>missing.has(h));
  need(unknownParents.length>=2,'not a targeted shared unknown witness');
  let subtotal=0;
  for(const h of parents){
   need(!loss.has(h),'S8 WIN/LOSS conflict: '+h);
   need(g.children(g.board(h,8)).has(row.s9)&&
    ind.children4(h).has(row.s9),'illegal S8-to-S9 witness: '+h);
   derived.add(h);
  }
  for(const h of unknownParents)touched.add(h);
  for(const h of actual){
   need(!loss10.has(h),'S10 WIN/LOSS conflict: '+h);
   leaves10.add(h);edges++;
   if(terminal){
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win&&b.win&&a.states===b.states&&a.legal===b.legal,
     'independent terminal WIN disagreement: '+h);
    subtotal+=a.states;
   }
  }
  if(terminal)need(subtotal===row.states,'terminal states mismatch: '+row.s9);
  states+=row.states;
 }
 need(roots.size===9&&edges===189&&states===25222&&touched.size===16,
  'terminal/coverage census changed');
 const after=new Set([...before,...derived]);
 need([...after].every(h=>!loss.has(h)),'S8 WIN/LOSS union conflict');
 function evaluate(proofs){
  let total=0,secured=0;const unknown=new Set();
  for(const h of plan)for(const c of g.children(g.board(h,7))){
   total++;if(proofs.has(c))secured++;else unknown.add(c);
  }
  return {total,secured,missing:total-secured,distinctMissing:unknown.size};
 }
 const previous=evaluate(before),updated=evaluate(after);
 need(previous.total===548&&previous.secured===282&&previous.missing===266&&
  updated.total===548&&updated.secured===298&&updated.missing===250&&
  updated.distinctMissing===250,'certified conditional coverage changed');
 return {schema:'n11-s9-targeted-gap266-terminal-v1',newS9Win:9,
  s10WinLeafEdges:edges,distinctS10WinLeaves:leaves10.size,
  terminalStatesPerGeometry:terminal?states:null,
  independentGeometries:terminal?2:0,derivedS8Win:derived.size,
  newS8Win:after.size-before.size,proofOnlyS8WinAfter:after.size,
  newlySecuredPlanEdges:16,previous,updated,winLossConflicts:0,
  newS7Verdicts:0,newS5Verdicts:0,twoStoneClosures:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module){
 const raw=fs.readFileSync(path.join(__dirname,'certificate.tsv'),'utf8');
 const rows=parse(raw),r=verify(rows);
 console.log(JSON.stringify(r,null,2));
 if(process.argv.includes('--negative')){
  const reject=(fn,terminal=false)=>{
   const bad=structuredClone(rows);fn(bad);let failed=false;
   try{verify(bad,{terminal});}catch(_){failed=true;}
   need(failed,'tampered certificate accepted');
  };
  reject(x=>x.pop());
  reject(x=>x[1].s9=x[0].s9);
  reject(x=>x[0].leaves++);
  reject(x=>x[0].states++,true);
  reject(x=>x[0].s9='00000000000000000000000000000000');
  let failed=false;try{parse(raw.replace('empty_board=UNKNOWN','empty_board=WIN'));}
  catch(_){failed=true;}
  need(failed,'tampered header accepted');
  console.error('PASS six certificate mutation rejections');
 }
}
module.exports={parse,verify};
