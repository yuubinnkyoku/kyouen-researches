#!/usr/bin/env node
'use strict';
// Re-optimize proof-only conditional S7 witness roots after eleven new S9 proofs.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const prior=require('../n11-s5-post-shared9-matching-20261027/audit.js');
const oldCert=JSON.parse(fs.readFileSync(path.join(__dirname,
  '../n11-s9-shared-plan14-20261027/certificate.json'),'utf8'));
const newCert=JSON.parse(fs.readFileSync(path.join(__dirname,
  '../n11-s9-shared-plan14-eleven-win-20261027/certificate.json'),'utf8'));
const WIN13='00000000000000821090a00000000020';
const need=(x,m)=>{if(!x)throw Error(m);};
const children=h=>g.children(BigInt('0x'+h));
const id=(a,b)=>a+':'+b;
const better=(a,b)=>!b||a.cost<b.cost||
  (a.cost===b.cost&&(a.total<b.total||
  (a.total===b.total&&a.s7<b.s7)));
function audit(negative=false){
  const old=prior.audit(false),{missing,by7,win,loss}=base.inventory();
  need(old.after.missing===516&&win.size===2176&&loss.size===338&&
    missing.length===27&&by7.size===853,'upstream proof inventory changed');
  const before=new Set([...win,WIN13,
    ...g.reverse(oldCert.witnesses.map(r=>r.s9_win))]);
  need(before.size===2221,'old proof-only WIN union changed');
  const derived=g.reverse(newCert.witnesses.map(r=>r.s9_win));
  need(derived.size===96,'new S9 proof reverse boundary changed');
  const after=new Set([...before,...derived]);
  need(after.size===2315&&[...after].every(h=>!loss.has(h)),
    'new proof-only WIN union conflict');
  const valid=new Map(),pair=new Map(),single=Array(27).fill(null);
  let excluded=0,affected=0;
  for(const [s7,cover] of by7){
    const cs=children(s7);
    if([...cs].some(h=>loss.has(h))){excluded++;continue;}
    const row={s7,cover:[...cover].sort((a,b)=>a-b),
      total:cs.size,secured:[...cs].filter(h=>after.has(h)).length};
    row.cost=row.total-row.secured;
    need(row.cost>=0&&row.cover.length>=1&&row.cover.length<=2,
      'invalid S7 candidate');
    valid.set(s7,row);
    if([...cs].some(h=>derived.has(h)&&!before.has(h)))affected++;
    for(const i of row.cover)if(better(row,single[i]))single[i]=row;
    if(row.cover.length===2){
      const k=id(...row.cover);
      if(better(row,pair.get(k)))pair.set(k,row);
    }
  }
  need(excluded===67&&valid.size===786&&pair.size===343&&
    single.every(Boolean),'S7 matching candidate census changed');
  const oldPair=new Map(old.pairOptions.map(r=>[id(r.i,r.j),r.cost]));
  let reducedPairs=0,reducedSingles=0;
  for(const [k,r] of pair){
    need(oldPair.has(k)&&r.cost<=oldPair.get(k),
      'pair cost increased or new option appeared');
    if(r.cost<oldPair.get(k))reducedPairs++;
  }
  for(let i=0;i<27;i++){
    need(single[i].cost<=old.singleOptions[i].cost,
      'single option cost increased');
    if(single[i].cost<old.singleOptions[i].cost)reducedSingles++;
  }
  const plan=fs.readFileSync(path.join(__dirname,
    '../n11-s5-pair-cover-20261026/s7-plan14-remaining.keys'),'ascii')
    .trim().split(/\s+/);
  function evaluate(keys,winSet){
    need(keys.length===14&&new Set(keys).size===14,'invalid plan');
    const covered=new Set(),unproved=new Set();let total=0,secured=0;
    for(const h of keys){
      need(valid.has(h),'refuted or missing candidate');
      for(const i of valid.get(h).cover)covered.add(i);
      const cs=children(h);total+=cs.size;
      for(const c of cs)if(winSet.has(c))secured++;else unproved.add(c);
    }
    need(covered.size===27,'incomplete S6 coverage');
    return {total,secured,missing:total-secured,distinctMissing:unproved.size};
  }
  const previous=evaluate(plan,before),updated=evaluate(plan,after);
  need(previous.total===548&&previous.secured===32&&previous.missing===516&&
    updated.total===548&&updated.secured===68&&updated.missing===480&&
    updated.distinctMissing===480,'fixed-plan proof coverage changed');
  if(negative){
    let rejected=false;
    try{evaluate(plan.slice(1),after);}catch(_){rejected=true;}
    need(rejected,'missing root accepted');
    const one=[...derived].find(h=>!before.has(h)&&
      plan.some(p=>children(p).has(h)));
    need(one&&evaluate(plan,new Set([...after].filter(h=>h!==one))).missing===481,
      'dropping proof did not reopen an edge');
    const conflict=new Set(after);conflict.add([...loss][0]);
    need([...conflict].some(h=>loss.has(h)),'conflict negative control failed');
  }
  return {schema:'n11-s5-post-eleven-s9-matching-v1',
    missingS6:missing.length,proofOnlyWin8Before:before.size,
    proofOnlyWin8After:after.size,knownLoss8:loss.size,
    newDerivedS8:derived.size,newlyProvedS8:after.size-before.size,
    candidates:by7.size,excluded,allowed:valid.size,
    affectedValidS7:affected,reducedPairCosts:reducedPairs,
    reducedSingleCosts:reducedSingles,
    pairOptions:[...pair].map(([k,r])=>{
      const [i,j]=k.split(':').map(Number);
      return {i,j,s7:r.s7,total:r.total,secured:r.secured,cost:r.cost};
    }).sort((a,b)=>a.i-b.i||a.j-b.j),
    singleOptions:single.map((r,i)=>({i,s7:r.s7,
      total:r.total,secured:r.secured,cost:r.cost})),
    savedPlan:plan,previous,updated,newS7Verdicts:0,newS5Verdicts:0,
    twoStoneClosures:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module)console.log(JSON.stringify(audit(process.argv.includes('--negative'))));
module.exports={audit};
