#!/usr/bin/env node
'use strict';
// Next bounded S9 plan after reusing certified S10 LOSS witnesses.
// Potential coverage is NOT a verdict or an empty-root proof.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
// Memoize the expensive nested certificate inventories before importing r7.
require('./reuse.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const p=require('../n11-s9-n24-round2-20261028/plan_next.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const count=rows=>p.popcount(rows.reduce((s,x)=>s|x.mask,0n));
const cost=rows=>rows.reduce((n,x)=>n+x.children,0);
const better=(a,b)=>count(a)>count(b)||(count(a)===count(b)&&cost(a)<cost(b));
function run(){
  const original=console.log;let inv;
  try{console.log=()=>{};inv=r7.inventory();}finally{console.log=original;}
  const frozen=JSON.parse(fs.readFileSync(path.join(__dirname,'derived-loss9.json')));
  need(Array.isArray(frozen)&&frozen.length===383,'derived LOSS9 witness list');
  const keys=new Set(frozen.map(x=>x.h));
  need(keys.size===383,'duplicate LOSS9 key');
  const options=new Map(inv.options.map(x=>[x.h,x]));
  const prior=new Set(inv.selected.map(x=>x.h));
  need(inv.missing.length===100&&inv.secured.size===5407&&inv.options.length===1478,
    'upstream proof-only frontier changed');
  need(frozen.every(x=>options.has(x.h)&&!prior.has(x.h)),
    'derived LOSS9 outside current eligible frontier');
  const eligible=inv.options.filter(x=>!prior.has(x.h)&&!keys.has(x.h));
  need(eligible.length===1063,'remaining candidate count');
  const reduced=p.pruneDominated(eligible);
  const baseline=p.greedy(eligible,32),alternate=p.greedy(reduced,32);
  const start=better(alternate,baseline)?alternate:baseline;
  const improved=p.improve(reduced,start);
  const chosen=improved.picked;
  need(chosen.length===32&&new Set(chosen.map(x=>x.h)).size===32,
    'selected S9 count/uniqueness');
  need(!better(baseline,chosen)&&chosen.every(x=>!keys.has(x.h)&&!prior.has(x.h)),
    'planner regression or certified LOSS9 selected');
  const result={schema:'n11-s9-post-s10-reuse-plan-v1',
    emptyBoard:'UNKNOWN',certifiedLoss9Excluded:383,
    alreadyProvedRound7Excluded:32,initialEligible:1478,
    remainingEligible:eligible.length,undominated:reduced.length,
    baselinePotentialCoverage:count(baseline),
    selectedPotentialCoverage:count(chosen),
    baselineChildCount:cost(baseline),selectedChildCount:cost(chosen),
    exchanges:improved.swaps,selected:chosen.length,
    selectedKeys:chosen.map(x=>x.h),
    selectionSha256:sha(chosen.map(x=>x.h).join('\n')+'\n'),
    newlyProvedS8:0,conditionalUnprovedEdges:100,
    twoStoneClosures:0};
  const f=path.join(__dirname,'plan.json');
  if(fs.existsSync(f))need(JSON.stringify(JSON.parse(fs.readFileSync(f)))===
    JSON.stringify(result),'frozen plan mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
