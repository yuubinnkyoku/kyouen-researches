#!/usr/bin/env node
'use strict';
// Re-optimize conditional 14-S7 proof obligations after five independently
// terminal-proved S9 WIN witnesses. This is NOT an S7 or S5 verdict.
const fs=require('node:fs'),path=require('node:path');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const prior=require('../n11-s5-win13-reoptimization-20261027/audit.js');
const shared=require('../n11-s9-shared-plan14-20261027/audit_coverage.js');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const cert=JSON.parse(fs.readFileSync(path.join(__dirname,
  '../n11-s9-shared-plan14-20261027/certificate.json'),'utf8'));
const WIN13='00000000000000821090a00000000020';
const need=(x,m)=>{if(!x)throw Error(m);};
const children=h=>g.children(BigInt('0x'+h));
const pairId=(a,b)=>a+':'+b;
const better=(a,b)=>!b||a.cost<b.cost||
  (a.cost===b.cost&&(a.total<b.total||
  (a.total===b.total&&a.s7<b.s7)));
function audit(negative=false){
  const old=prior.audit(false);
  const previousShared=shared.audit(false);
  const {missing,by7,win,loss}=base.inventory();
  need(old.after.missing===535&&previousShared.updated.missing===516,
       'upstream fixed-plan coverage changed');
  need(win.size===2176&&loss.size===338&&missing.length===27,
       'upstream proof-only boundary changed');
  need(!win.has(WIN13)&&!loss.has(WIN13),'WIN13 source collision');
  const after13=new Set([...win,WIN13]);
  const roots=cert.witnesses.map(r=>r.s9_win);
  need(roots.length===5&&new Set(roots).size===5,'shared S9 witness count');
  const derived=g.reverse(roots);
  need(derived.size===45,'shared S9 reverse-parent boundary changed');
  need([...derived].every(h=>!loss.has(h)),'WIN/LOSS conflict in S9 parents');
  const newWin=new Set([...after13,...derived]);
  need(newWin.size===2221&&[...newWin].every(h=>!loss.has(h)),
       'proof-only WIN/LOSS union conflict');
  const valid=new Map(),pair=new Map(),single=Array(27).fill(null);
  let excluded=0,affected=0;
  for(const [s7,cover] of by7){
    const s8=children(s7);
    if([...s8].some(h=>loss.has(h))){excluded++;continue;}
    const row={s7,cover:[...cover].sort((a,b)=>a-b),
      total:s8.size,secured:[...s8].filter(h=>newWin.has(h)).length};
    row.cost=row.total-row.secured;
    need(row.cost>=0&&row.cover.length>=1&&row.cover.length<=2,
         'invalid candidate cost or coverage');
    valid.set(s7,row);
    if([...s8].some(h=>derived.has(h)&&!after13.has(h)))affected++;
    for(const i of row.cover)if(better(row,single[i]))single[i]=row;
    if(row.cover.length===2){
      const id=pairId(...row.cover);
      if(better(row,pair.get(id)))pair.set(id,row);
    }
  }
  need(by7.size===853&&excluded===67&&valid.size===786&&
       pair.size===343&&single.every(Boolean),'candidate census changed');
  const priorPairs=new Map(old.pairOptions.map(r=>[pairId(r.i,r.j),r.cost]));
  let pairReduced=0,singleReduced=0;
  for(const [id,row] of pair){
    need(priorPairs.has(id),'new pair option appeared');
    const d=priorPairs.get(id)-row.cost;
    need(d>=0&&d<=45,'invalid pair cost monotonicity');
    if(d)pairReduced++;
  }
  for(let i=0;i<27;i++){
    const d=old.singleOptions[i].cost-single[i].cost;
    need(d>=0&&d<=45,'invalid single cost monotonicity');
    if(d)singleReduced++;
  }
  const plan=fs.readFileSync(path.join(__dirname,
    '../n11-s5-pair-cover-20261026/s7-plan14-remaining.keys'),'ascii')
    .trim().split(/\s+/);
  function evaluate(keys,winSet){
    need(keys.length===14&&new Set(keys).size===14,'invalid 14-root plan');
    const covered=new Set(),unproved=new Set(),securedDistinct=new Set();
    let total=0,secured=0;
    for(const h of keys){
      need(valid.has(h),'refuted or missing S7 candidate: '+h);
      for(const i of valid.get(h).cover)covered.add(i);
      const cs=children(h);total+=cs.size;
      for(const c of cs){
        if(winSet.has(c)){secured++;securedDistinct.add(c);}
        else unproved.add(c);
      }
    }
    need(covered.size===27,'incomplete S6 coverage');
    return {total,secured,missing:total-secured,
      unprovedDistinct:unproved.size,securedDistinct:securedDistinct.size};
  }
  const before=evaluate(plan,after13),after=evaluate(plan,newWin);
  need(before.total===548&&before.secured===13&&before.missing===535,
       'post-WIN13 plan changed');
  need(after.total===548&&after.secured===32&&after.missing===516&&
       after.unprovedDistinct===516,'post-S9 fixed plan changed');
  if(negative){
    for(const bad of [plan.slice(1),[plan[0],...plan.slice(0,13)],
      plan.map((h,i)=>i?h:WIN13)]){
      let rejected=false;try{evaluate(bad,newWin);}catch(_){rejected=true;}
      need(rejected,'mutated plan accepted');
    }
    need(evaluate(plan,after13).missing===535,
         'dropping new proof did not restore previous obligations');
    const bad=new Set(newWin);bad.add([...loss][0]);
    need([...bad].some(h=>loss.has(h)),'conflict negative control failed');
  }
  return {schema:'n11-s5-post-shared9-matching-v1',
    sourceS5:old.sourceS5,missingS6:missing.length,
    proofOnlyWin8Before:after13.size,proofOnlyWin8After:newWin.size,
    knownLoss8:loss.size,derivedS8:derived.size,
    s7Candidates:by7.size,excluded,allowed:valid.size,
    affectedValidS7:affected,reducedPairCosts:pairReduced,
    reducedSingleCosts:singleReduced,
    pairOptions:[...pair].map(([id,r])=>{
      const [i,j]=id.split(':').map(Number);
      return {i,j,s7:r.s7,total:r.total,secured:r.secured,cost:r.cost};
    }).sort((a,b)=>a.i-b.i||a.j-b.j),
    singleOptions:single.map((r,i)=>({i,s7:r.s7,
      total:r.total,secured:r.secured,cost:r.cost})),
    savedPlan:plan,before,after,
    newS7Verdicts:0,newS5Verdicts:0,twoStoneClosures:0,
    emptyBoard:'UNKNOWN',
    trust:'Only independent-terminal S9 WIN lifts and existing terminal-proved S8 WINs secure S7->S8 edges; all S7 candidates UNKNOWN.'};
}
if(require.main===module)console.log(JSON.stringify(audit(process.argv.includes('--negative'))));
module.exports={audit};
