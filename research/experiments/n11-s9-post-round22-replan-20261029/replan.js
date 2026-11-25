#!/usr/bin/env node
'use strict';
// Replan the conditional N11 fourteen-root S8 frontier after round22.
// Only independently verified certificates count as proven coverage.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const planner=require('../n11-s9-n24-round2-20261028/plan_next.js');
const verify22=require('../n11-s9-post-round21-round22-20261029/verify_compact.js');
const need=(v,m)=>{if(!v)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const pop=rows=>planner.popcount(rows.reduce((m,x)=>m|x.mask,0n));
const cost=rows=>rows.reduce((n,x)=>n+x.children,0);
const better=(a,b)=>pop(a)>pop(b)||(pop(a)===pop(b)&&cost(a)<cost(b));
const planDirs=[
  'n11-s9-post-s10-reuse-round8-20261028',
  ...Array.from({length:13},(_,i)=>{
    const n=i+9,day=n<=11?'20261028':'20261029';
    return 'n11-s9-post-round'+n+'-replan-'+day;
  })
];
const certDirs=[
  'n11-s9-post-round8-round9-20261028',
  ...Array.from({length:13},(_,i)=>{
    const n=i+9,day=n<=11?'20261028':'20261029';
    return 'n11-s9-post-round'+n+'-round'+(n+1)+'-'+day;
  })
];
function lossClosure(plan,cert){
  const keys=plan.newSelectedKeys,claims=Buffer.from(cert.witnessBase64,'base64');
  need(keys.length===claims.length&&keys.length===cert.win9+cert.loss9&&
    sha(keys.join('\n')+'\n')===cert.selectionSha256&&
    sha(claims)===cert.witnessSha256&&
    plan.newSelectionSha256===cert.sourcePlanSha256,'certificate identity');
  const parents=new Set(),wins=[];
  for(let i=0;i<keys.length;i++){
    const h=keys[i],kids=g.children(g.board(h,9));
    need(same(kids,ind.children4(h)),'geometry boundary mismatch '+h);
    const ordered=[...kids].sort(),w=claims[i];
    if(w===255){wins.push(h);continue;}
    need(w<ordered.length,'LOSS witness out of range');
    const leaf=ordered[w],b=BigInt('0x'+leaf);
    for(const pt of g.pts(b)){
      const par=g.key(g.canonical(b^(1n<<BigInt(pt))));
      need(g.children(g.board(par,9)).has(leaf)&&
        ind.children4(par).has(leaf),'invalid LOSS parent '+par);
      parents.add(par);
    }
  }
  need(wins.length===cert.win9&&
    JSON.stringify(wins)===JSON.stringify(cert.win9Keys)&&
    parents.size===cert.loss9ParentClosure&&
    sha([...parents].sort().join('\n')+'\n')===cert.loss9ParentSha256,
    'LOSS parent closure mismatch');
  return parents;
}
function run(){
  // Recheck the latest terminal certificate, then reuse independently audited
  // fixed older plans and certificates. No unfinished solver states count.
  const prior=read('../n11-s9-post-round21-replan-20261029/next-plan.json');
  const cert22=read('../n11-s9-post-round21-round22-20261029/certificate.json');
  need(prior.schema==='n11-post-round21-proof-only-replan-v1'&&
    prior.emptyBoard==='UNKNOWN'&&prior.conditionalUnprovedEdges===40&&
    prior.proofOnlyWin8After===5835&&prior.selectedCount===5&&
    prior.newSelectionSha256==='f42aed3692d2f50de7f0c2a3633c50d3f9f5c662e6d29469371b8f502e4eae17'&&
    cert22.sourcePlanSha256===prior.newSelectionSha256&&
    cert22.win9===0&&cert22.loss9===5&&
    cert22.loss9ParentClosure===50&&cert22.newTwoStoneClosures===0,
    'frozen round21 plan / round22 certificate mismatch');
  let checked22;
  const originalLog=console.log;
  try{console.log=()=>{};checked22=verify22.verify({negative:true});}
  finally{console.log=originalLog;}
  need(checked22.verified&&checked22.win9===0&&checked22.loss9===5&&
    checked22.emptyBoard==='UNKNOWN','round22 independent terminal replay failed');
  const plans=planDirs.map(d=>read('../'+d+'/next-plan.json'));
  const certs=certDirs.map(d=>read('../'+d+'/certificate.json'));
  need(plans.length===14&&certs.length===14&&
    plans[13].newSelectionSha256===prior.newSelectionSha256&&
    certs[13].witnessSha256===cert22.witnessSha256&&
    cert22.sourcePriorWitnessSha256===certs[12].witnessSha256,
    'round22 chain input mismatch');
  const parents=certs.map((c,i)=>lossClosure(plans[i],c));
  const allWin9=new Set(),allLoss9=new Set();
  for(let i=0;i<certs.length;i++){
    for(const h of certs[i].win9Keys)allWin9.add(h);
    for(const h of parents[i])allLoss9.add(h);
  }
  need([...allWin9].every(h=>!allLoss9.has(h)),
    'cross-batch WIN9/LOSS9 contradiction');
  const inv=r7.inventory(),{s,secured}=inv;
  need(secured.size===5407&&inv.missing.length===100,'round7 inventory mismatch');
  const after21=new Set(secured);
  for(let i=0;i<13;i++)for(const h of g.reverse(certs[i].win9Keys))after21.add(h);
  const derived22=g.reverse(cert22.win9Keys);
  need(derived22.size===0,'round22 unexpectedly has WIN9 parents');
  const after22=new Set([...after21,...derived22]);
  need(after21.size===5835&&after22.size===5835&&
    [...after22].every(h=>!s.loss.has(h))&&
    r7.coverage(s.plan,after22).missing===40,
    'WIN8 frontier mismatch');
  const p8=plans[0];
  const oldLoss=read('../n11-s10-cross-batch-reuse-20261028/derived-loss9.json');
  const priorExcluded=new Set([...p8.excludedKeys,...oldLoss.map(x=>x.h)]);
  const used7=new Set(inv.selected.map(x=>x.h));
  const selectedBefore22=new Set(plans.slice(0,13).flatMap(p=>p.newSelectedKeys));
  const lossBefore22=new Set(parents.slice(0,13).flatMap(p=>[...p]));
  const missing21=new Set([...s.plan8].filter(h=>!after21.has(h)));
  const eligible21=inv.options.filter(x=>!used7.has(x.h)&&
    !priorExcluded.has(x.h)&&!selectedBefore22.has(x.h)&&
    !lossBefore22.has(x.h)&&x.hits.some(h=>missing21.has(h)));
  need(eligible21.length===32&&prior.selectedCount===5&&
    prior.newSelectedKeys.every(h=>eligible21.some(x=>x.h===h)),
    'round21 candidate census mismatch');
  const selected22=new Set(prior.newSelectedKeys),parents22=parents[13];
  const excludedByProof=eligible21.filter(x=>
    selected22.has(x.h)||parents22.has(x.h));
  need([...selected22].every(h=>excludedByProof.some(x=>x.h===h)),
    'round21 selected candidates not excluded');
  const remaining=eligible21.filter(x=>
    !selected22.has(x.h)&&!parents22.has(x.h));
  const missing22=[...s.plan8].filter(h=>!after22.has(h)).sort();
  need(missing22.length===40,'round21 missing edge mismatch');
  const index=new Map(missing22.map((h,i)=>[h,i]));
  const eligible=remaining.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index.has(h))mask|=1n<<BigInt(index.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  need(eligible.length>0,'no eligible round23 candidate');
  const reduced=planner.pruneDominated(eligible);
  const baseline=planner.greedy(eligible,32);
  const rg=planner.greedy(reduced,32);
  const optimized=planner.improve(reduced,better(rg,baseline)?rg:baseline);
  const chosen=optimized.picked;
  need(chosen.length>0&&chosen.length<=32&&
    new Set(chosen.map(x=>x.h)).size===chosen.length&&
    !better(baseline,chosen)&&
    chosen.every(x=>!selected22.has(x.h)&&!parents22.has(x.h)),
    'round23 candidate selection invalid');
  const result={
    schema:'n11-post-round22-proof-only-replan-v1',emptyBoard:'UNKNOWN',
    sourceSelectionSha256:cert22.selectionSha256,
    sourceWitnessSha256:cert22.witnessSha256,
    independentlyVerifiedTerminalLeaves:checked22.uniqueTerminalLeaves,
    terminalStatesPerGeometry:checked22.terminalStatesPerGeometry,
    verifiedWin9:cert22.win9,verifiedLoss9:cert22.loss9,
    derivedLoss9ParentClosure:parents22.size,
    proofOnlyWin8Before:after21.size,proofOnlyWin8After:after22.size,
    newProofOnlyWin8:after22.size-after21.size,
    conditionalUnprovedEdges:missing22.length,
    eligibleBeforeRound22:eligible21.length,
    excludedByRound22Proof:excludedByProof.length,
    excludedSelectedRound22:selected22.size,
    excludedAdditionalLoss9Parents:excludedByProof.length-selected22.size,
    remainingAfterProofExclusions:remaining.length,
    noLongerTouchesUnprovedS8:remaining.length-eligible.length,
    eligibleUnprovedS9:eligible.length,undominatedS9:reduced.length,
    baselinePotentialCoverage:pop(baseline),potentialCoverage:pop(chosen),
    legal10Children:cost(chosen),exchanges:optimized.swaps,
    selectedCount:chosen.length,newSelectedKeys:chosen.map(x=>x.h),
    newSelectionSha256:sha(chosen.map(x=>x.h).join('\n')+'\n'),
    winLossConflicts:0,newS7Verdicts:0,newS5Verdicts:0,newTwoStoneClosures:0
  };
  const fixed=path.join(__dirname,'next-plan.json');
  if(fs.existsSync(fixed))need(
    JSON.stringify(read('next-plan.json'))===JSON.stringify(result),
    'frozen round22 replan mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
