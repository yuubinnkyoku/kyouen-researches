#!/usr/bin/env node
'use strict';
// Re-optimize the 14-S7 conditional plan after the independently terminal-proved S8 WIN13.
// Every S7 candidate remains UNKNOWN. WIN8 is a secured AND edge, not a S7 verdict.
const fs=require('node:fs'),path=require('node:path');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const WIN8='00000000000000821090a00000000020';
const OLD_S7='00000000000000821090200000000020';
const need=(x,m)=>{if(!x)throw Error(m);};
const children=h=>g.children(BigInt('0x'+h));
const keyOf=(a,b)=>a+':'+b;
const better=(a,b)=>!b||a.cost<b.cost||(a.cost===b.cost&&
  (a.total<b.total||(a.total===b.total&&a.s7<b.s7)));
function audit(negative=false){
  const previous=base.audit(false);
  const {missing,by7,win,loss}=base.inventory();
  need(previous.improved.missing===536&&previous.improved.unprovedDistinct===536,
       'previous independently audited optimum changed');
  need(!win.has(WIN8)&&!loss.has(WIN8),'WIN13 proof provenance conflict');
  const newWin=new Set(win);newWin.add(WIN8);
  const parents=g.reverse([WIN8]);
  const candidateParents=[...parents].filter(h=>by7.has(h)).sort();
  need(parents.size===8&&candidateParents.length===3,
       'WIN13 S7 parent incidence changed');
  need(candidateParents.includes(OLD_S7),'selected S7 witness parent missing');
  const pair=new Map(),single=Array(27).fill(null),valid=new Map();
  let excluded=0,changed=0;
  for(const [s7,cover] of by7){
    const s8=children(s7);
    if([...s8].some(h=>loss.has(h))){excluded++;continue;}
    const row={s7,cover:[...cover].sort((a,b)=>a-b),
      total:s8.size,secured:[...s8].filter(h=>newWin.has(h)).length};
    row.cost=row.total-row.secured;
    need(row.cost>=0,'negative cost');
    valid.set(s7,row);
    if(s8.has(WIN8))changed++;
    for(const i of row.cover)if(better(row,single[i]))single[i]=row;
    if(row.cover.length===2){
      const id=keyOf(...row.cover);
      if(better(row,pair.get(id)))pair.set(id,row);
    }
  }
  need(excluded===67&&valid.size===786&&pair.size===343&&single.every(Boolean),
       'candidate census changed');
  need(changed>=1&&changed<=3,'unexpected affected valid candidates');
  const plan=fs.readFileSync(path.join(__dirname,
    '../n11-s5-pair-cover-20261026/s7-plan14-remaining.keys'),'ascii')
    .trim().split(/\s+/);
  function evaluate(keys,winSet){
    need(keys.length===14&&new Set(keys).size===14,'invalid plan');
    const covered=new Set(),unproved=new Set();
    let total=0,secured=0;
    for(const h of keys){
      need(valid.has(h),'invalid/refuted root '+h);
      const row=valid.get(h);
      for(const i of row.cover)covered.add(i);
      const cs=children(h);
      total+=cs.size;
      for(const c of cs)if(winSet.has(c))secured++;else unproved.add(c);
    }
    need(covered.size===27,'incomplete S6 coverage');
    return {total,secured,missing:total-secured,distinctUnproved:unproved.size};
  }
  const before=evaluate(plan,win),after=evaluate(plan,newWin);
  need(before.missing===536&&after.missing===535&&after.distinctUnproved===535,
       'WIN13 secured edge regression');
  need(after.secured===before.secured+1,'unexpected WIN13 selected multiplicity');
  // Every affected candidate is an actual S7 parent of the certified S8,
  // so the only possible cost change is exactly one per selected parent.
  for(const h of candidateParents)
    need(children(h).has(WIN8),'reverse incidence not a legal forward edge');
  if(negative){
    for(const bad of [plan.slice(1),plan.map((h,i)=>i?h:WIN8)]){
      let rejected=false;try{evaluate(bad,newWin);}catch(_){rejected=true;}
      need(rejected,'tampered plan accepted');
    }
    need(evaluate(plan,new Set([...newWin].filter(h=>h!==WIN8))).missing===536,
         'dropping new proof did not restore old cost');
  }
  return {schema:'n11-s5-win13-updated-matching-v1',win8:WIN8,
    sourceS5:previous.sourceS5,missingS6:missing.length,
    oldKnownWin8:win.size,newKnownWin8:newWin.size,knownLoss8:loss.size,
    s7Candidates:by7.size,excluded,allowed:valid.size,
    affectedS7Parents:candidateParents,affectedValidCandidates:changed,
    pairOptions:[...pair].map(([id,r])=>{
      const [i,j]=id.split(':').map(Number);
      return {i,j,s7:r.s7,total:r.total,secured:r.secured,cost:r.cost};
    }).sort((a,b)=>a.i-b.i||a.j-b.j),
    singleOptions:single.map((r,i)=>({i,s7:r.s7,total:r.total,
      secured:r.secured,cost:r.cost})),
    oldPlan:plan,before,after,emptyBoard:'UNKNOWN',
    trust:'WIN13 independently terminal-proved; S7 candidates remain UNKNOWN.'};
}
if(require.main===module)console.log(JSON.stringify(audit(process.argv.includes('--negative'))));
module.exports={audit};
