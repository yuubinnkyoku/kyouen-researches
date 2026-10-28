#!/usr/bin/env node
'use strict';
// Replan only; never promote potential coverage to WIN8.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const planner=require('../n11-s9-n24-round2-20261028/plan_next.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const dir=__dirname;
const plan=JSON.parse(fs.readFileSync(path.join(dir,'../n11-s10-cross-batch-reuse-20261028/plan.json')));
const cert=JSON.parse(fs.readFileSync(path.join(dir,'certificate.json')));
const oldLoss=JSON.parse(fs.readFileSync(path.join(dir,'../n11-s10-cross-batch-reuse-20261028/derived-loss9.json')));
function run(){
  const inv=r7.inventory();
  need(inv.missing.length===100&&inv.secured.size===5407&&inv.options.length===1478,
    'upstream S8 frontier changed');
  const used=new Set(inv.selected.map(x=>x.h));
  const priorLoss=new Set(oldLoss.map(x=>x.h));
  need(priorLoss.size===383,'upstream LOSS9 reuse changed');
  const initial=inv.options.filter(x=>!used.has(x.h)&&!priorLoss.has(x.h));
  need(initial.length===1063,'old eligible census changed');
  const claims=Buffer.from(cert.witnessBase64,'base64');
  need(claims.length===32&&plan.selectedKeys.length===32&&
    sha(plan.selectedKeys.join('\n')+'\n')===cert.selectionSha256&&
    sha(claims)===cert.witnessSha256,'fixed round8 identity mismatch');
  const parents=new Set();
  for(let i=0;i<32;i++){
    const h=plan.selectedKeys[i],kids=[...g.children(g.board(h,9))].sort();
    need(claims[i]<kids.length,'bad LOSS10 witness');
    const b=BigInt('0x'+kids[claims[i]]);
    for(const p of g.pts(b))parents.add(g.key(g.canonical(b^(1n<<BigInt(p)))));
  }
  need(parents.size===320&&sha([...parents].sort().join('\n')+'\n')===
    cert.derivedLoss9ParentSha256,'LOSS9 parent closure changed');
  const removed=initial.filter(x=>parents.has(x.h));
  const remaining=initial.filter(x=>!parents.has(x.h));
  need(removed.length>=32&&plan.selectedKeys.every(h=>removed.some(x=>x.h===h)),
    'selected round8 roots not excluded');
  const reduced=planner.pruneDominated(remaining);
  const baseline=planner.greedy(remaining,32),alternate=planner.greedy(reduced,32);
  const count=rows=>planner.popcount(rows.reduce((m,x)=>m|x.mask,0n));
  const cost=rows=>rows.reduce((n,x)=>n+x.children,0);
  const better=(a,b)=>count(a)>count(b)||(count(a)===count(b)&&cost(a)<cost(b));
  const start=better(alternate,baseline)?alternate:baseline;
  const optimized=planner.improve(reduced,start),chosen=optimized.picked;
  need(chosen.length===32&&new Set(chosen.map(x=>x.h)).size===32&&
    !better(baseline,chosen),'invalid next selection');
  const report={schema:'n11-post-reuse-round8-replan-v1',emptyBoard:'UNKNOWN',
    oldEligible:initial.length,excludedByRound8Loss10:removed.length,
    beyondSelected32:removed.length-32,remainingEligible:remaining.length,
    undominated:reduced.length,baselinePotentialCoverage:count(baseline),
    potentialCoverage:count(chosen),legal10Children:cost(chosen),
    exchanges:optimized.swaps,newSelectedKeys:chosen.map(x=>x.h),
    newSelectionSha256:sha(chosen.map(x=>x.h).join('\n')+'\n'),
    excludedKeys:removed.map(x=>x.h).sort(),newS8Win:0,
    conditionalUnprovedEdges:100,twoStoneClosures:0};
  if(process.env.N11_REPLAN_OUTPUT)fs.writeFileSync(process.env.N11_REPLAN_OUTPUT,
    JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report,null,2));return report;
}
if(require.main===module)run();
module.exports={run};
