#!/usr/bin/env node
'use strict';
// Original-first-player verdicts: at S9 the opponent plays, so a certified
// LOSS10 child proves LOSS9. No S8 or empty-board verdict is inferred.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {execFileSync}=require('node:child_process');
const {parentsOfLoss10}=require('./expand.js');
const p=require('../n11-s9-n24-round2-20261028/plan_next.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const base=path.join(__dirname,'../n11-s10-cross-batch-reuse-20261028');
const data=JSON.parse(execFileSync(process.execPath,
  [path.join(base,'reuse.js'),'--export-loss10'],
  {encoding:'utf8',maxBuffer:32*1024*1024,timeout:1200000}));
need(data.schema==='n11-certified-loss10-export-v1'&&
  data.emptyBoard==='UNKNOWN'&&data.conflicts===0&&
  data.distinctS10===5085&&data.loss10.length===1306,'LOSS10 export regression');
const win9=new Set(data.knownWin9);
need(win9.size===data.knownWin9.length,'duplicate certified WIN9');
const all=new Map();
for(const row of data.loss10){
  need(typeof row.h==='string'&&typeof row.source==='string','bad LOSS10 record');
  for(const parent of parentsOfLoss10(row.h)){
    need(!win9.has(parent),'WIN/LOSS CONFLICT at S9 '+parent);
    if(!all.has(parent)||row.h<all.get(parent))all.set(parent,row.h);
  }
}
const prior=new Set(fs.readFileSync(path.join(__dirname,'expanded-loss9.keys'),'ascii')
  .trim().split(/\s+/));
need(prior.size===3250,'prior closure regression');
for(const h of prior)need(all.has(h),'previous certified LOSS9 missing '+h);
const frozen=JSON.parse(fs.readFileSync(path.join(base,'derived-loss9.json')));
need(frozen.length===383&&frozen.every(x=>all.has(x.h)),'prior witnesses missing');
const oldPlan=JSON.parse(fs.readFileSync(path.join(base,'plan.json')));
need(oldPlan.remainingEligible===1063&&oldPlan.selectedKeys.length===32,'old plan changed');
let inv;const log=console.log;
try{console.log=()=>{};inv=r7.inventory();}finally{console.log=log;}
need(inv.missing.length===100&&inv.secured.size===5407&&inv.options.length===1478,
  'certified S8 frontier changed');
const selected=new Set(inv.selected.map(x=>x.h)),previous=new Set(frozen.map(x=>x.h));
const eligible=inv.options.filter(x=>!selected.has(x.h)&&!previous.has(x.h));
need(eligible.length===1063,'eligible census changed');
const excluded=eligible.filter(x=>all.has(x.h));
const remaining=eligible.filter(x=>!all.has(x.h));
const reduced=p.pruneDominated(remaining);
const count=rows=>p.popcount(rows.reduce((s,x)=>s|x.mask,0n));
const cost=rows=>rows.reduce((s,x)=>s+x.children,0);
const better=(a,b)=>count(a)>count(b)||(count(a)===count(b)&&cost(a)<cost(b));
const baseline=p.greedy(remaining,32),alternative=p.greedy(reduced,32);
const start=better(alternative,baseline)?alternative:baseline;
const improved=p.improve(reduced,start),chosen=improved.picked;
need(chosen.length===32&&new Set(chosen.map(x=>x.h)).size===32&&
  chosen.every(x=>!all.has(x.h))&&!better(baseline,chosen),'invalid new plan');
const keys=[...all.keys()].sort(),manifest=keys.join('\n')+'\n';
const result={schema:'n11-all-loss10-parent-closure-v1',emptyBoard:'UNKNOWN',
  trust:'previously terminal-verified LOSS10 leaves, independent 3x3/4x4 and D4 parent audit; no new terminal replay',
  distinctLoss10:data.loss10.length,certifiedWin9Checked:win9.size,
  loss9Parents:all.size,previousLoss9Parents:prior.size,
  additionalLoss9Parents:all.size-prior.size,conflicts:0,
  eligibleBefore:eligible.length,eligibleNewlyExcluded:excluded.length,
  eligibleAfter:remaining.length,undominatedAfter:reduced.length,
  previous32Excluded:oldPlan.selectedKeys.filter(h=>all.has(h)),
  newSelection:chosen.map(x=>x.h),
  newSelectionSha256:sha(chosen.map(x=>x.h).join('\n')+'\n'),
  potentialCoverage:count(chosen),legal10ChildCount:cost(chosen),
  exchanges:improved.swaps,manifestSha256:sha(manifest),
  conditionalUnprovedEdges:100,newS8Win:0,twoStoneClosures:0};
const fixed=JSON.parse(fs.readFileSync(path.join(__dirname,'full-closure-report.json'),'utf8'));
need(JSON.stringify(fixed)===JSON.stringify(result),'frozen full-closure report differs');
if(process.env.N11_OUTPUT_DIR){
  fs.mkdirSync(process.env.N11_OUTPUT_DIR,{recursive:true});
  fs.writeFileSync(path.join(process.env.N11_OUTPUT_DIR,'report.json'),
    JSON.stringify(result,null,2)+'\n');
  fs.writeFileSync(path.join(process.env.N11_OUTPUT_DIR,'all-loss9.keys'),manifest);
  fs.writeFileSync(path.join(process.env.N11_OUTPUT_DIR,'newly-excluded.keys'),
    excluded.map(x=>x.h).sort().join('\n')+'\n');
}
console.log(JSON.stringify(result,null,2));
