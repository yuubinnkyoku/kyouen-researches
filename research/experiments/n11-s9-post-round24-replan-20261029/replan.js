#!/usr/bin/env node
'use strict';
// Replan the conditional N11 fourteen-root S8 frontier after round24.
// Only independently verified certificates count as proven coverage.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const planner=require('../n11-s9-n24-round2-20261028/plan_next.js');
const verify24=require('../n11-s9-post-round23-round24-20261029/verify_compact.js');
const need=(v,m)=>{if(!v)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const pop=rows=>planner.popcount(rows.reduce((m,x)=>m|x.mask,0n));
const cost=rows=>rows.reduce((n,x)=>n+x.children,0);
const better=(a,b)=>pop(a)>pop(b)||(pop(a)===pop(b)&&cost(a)<cost(b));
const planDirs=[
  'n11-s9-post-s10-reuse-round8-20261028',
  ...Array.from({length:15},(_,i)=>{
    const n=i+9,day=n<=11?'20261028':'20261029';
    return 'n11-s9-post-round'+n+'-replan-'+day;
  })
];
const certDirs=[
  'n11-s9-post-round8-round9-20261028',
  ...Array.from({length:15},(_,i)=>{
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
  const prior=read('../n11-s9-post-round23-replan-20261029/next-plan.json');
  const cert24=read('../n11-s9-post-round23-round24-20261029/certificate.json');
  const lift24=read('../n11-s9-post-round23-round24-20261029/lift.json');
  need(prior.schema==='n11-post-round23-proof-only-replan-v1'&&
    prior.emptyBoard==='UNKNOWN'&&prior.conditionalUnprovedEdges===38&&
    prior.proofOnlyWin8After===5851&&prior.selectedCount===3&&
    prior.newSelectionSha256==='b0631fd96ba1f5c71b1b47aa6a8c9970bfc5dbe70f8e2e8c4072c2c4aa719785'&&
    cert24.sourcePlanSha256===prior.newSelectionSha256&&
    cert24.win9===1&&cert24.loss9===2&&
    cert24.loss9ParentClosure===20&&cert24.newTwoStoneClosures===0&&
    lift24.proofOnlyWIN8Before===5851&&lift24.proofOnlyWIN8After===5859&&
    lift24.newProofOnlyWIN8===8&&lift24.updated.missing===37&&
    lift24.winLossConflicts===0,
    'frozen round23 plan / round24 certificate / lift mismatch');
  let checked24;
  const originalLog=console.log;
  try{console.log=()=>{};checked24=verify24.verify({negative:true});}
  finally{console.log=originalLog;}
  need(checked24.verified&&checked24.win9===1&&checked24.loss9===2&&
    checked24.emptyBoard==='UNKNOWN','round24 independent terminal replay failed');
  const plans=planDirs.map(d=>read('../'+d+'/next-plan.json'));
  const certs=certDirs.map(d=>read('../'+d+'/certificate.json'));
  need(plans.length===16&&certs.length===16&&
    plans[15].newSelectionSha256===prior.newSelectionSha256&&
    certs[15].witnessSha256===cert24.witnessSha256&&
    cert24.sourcePriorWitnessSha256===certs[14].witnessSha256,
    'round24 chain input mismatch');
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
  const after23=new Set(secured);
  for(let i=0;i<15;i++)for(const h of g.reverse(certs[i].win9Keys))after23.add(h);
  const derived24=g.reverse(cert24.win9Keys);
  need(derived24.size===9,'round24 WIN9 parent count mismatch');
  const after24=new Set([...after23,...derived24]);
  need(after23.size===5851&&after24.size===5859&&
    [...after24].every(h=>!s.loss.has(h))&&
    r7.coverage(s.plan,after23).missing===38&&
    r7.coverage(s.plan,after24).missing===37,
    'WIN8 frontier mismatch');
  const p8=plans[0];
  const oldLoss=read('../n11-s10-cross-batch-reuse-20261028/derived-loss9.json');
  const priorExcluded=new Set([...p8.excludedKeys,...oldLoss.map(x=>x.h)]);
  const used7=new Set(inv.selected.map(x=>x.h));
  const selectedBefore24=new Set(plans.slice(0,15).flatMap(p=>p.newSelectedKeys));
  const lossBefore24=new Set(parents.slice(0,15).flatMap(p=>[...p]));
  const missing23=new Set([...s.plan8].filter(h=>!after23.has(h)));
  const eligible23=inv.options.filter(x=>!used7.has(x.h)&&
    !priorExcluded.has(x.h)&&!selectedBefore24.has(x.h)&&
    !lossBefore24.has(x.h)&&x.hits.some(h=>missing23.has(h)));
  need(eligible23.length===12&&prior.selectedCount===3&&
    prior.newSelectedKeys.every(h=>eligible23.some(x=>x.h===h)),
    'round23 candidate census mismatch');
  const selected24=new Set(prior.newSelectedKeys),parents24=parents[15];
  const excludedByProof=eligible23.filter(x=>
    selected24.has(x.h)||parents24.has(x.h));
  need([...selected24].every(h=>excludedByProof.some(x=>x.h===h)),
    'round24 selected candidates not excluded');
  const remaining=eligible23.filter(x=>
    !selected24.has(x.h)&&!parents24.has(x.h));
  const missing24=[...s.plan8].filter(h=>!after24.has(h)).sort();
  need(missing24.length===37,'round24 missing edge mismatch');
  const index=new Map(missing24.map((h,i)=>[h,i]));
  const eligible=remaining.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index.has(h))mask|=1n<<BigInt(index.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  need(eligible.length>0,'no eligible round25 candidate');
  const reduced=planner.pruneDominated(eligible);
  const baseline=planner.greedy(eligible,32);
  const rg=planner.greedy(reduced,32);
  const optimized=planner.improve(reduced,better(rg,baseline)?rg:baseline);
  const chosen=optimized.picked;
  need(chosen.length>0&&chosen.length<=32&&
    new Set(chosen.map(x=>x.h)).size===chosen.length&&
    !better(baseline,chosen)&&
    chosen.every(x=>!selected24.has(x.h)&&!parents24.has(x.h)),
    'round25 candidate selection invalid');
  const result={
    schema:'n11-post-round24-proof-only-replan-v1',emptyBoard:'UNKNOWN',
    sourceSelectionSha256:cert24.selectionSha256,
    sourceWitnessSha256:cert24.witnessSha256,
    independentlyVerifiedTerminalLeaves:checked24.uniqueTerminalLeaves,
    terminalStatesPerGeometry:checked24.terminalStatesPerGeometry,
    verifiedWin9:cert24.win9,verifiedLoss9:cert24.loss9,
    derivedLoss9ParentClosure:parents24.size,
    proofOnlyWin8Before:after23.size,proofOnlyWin8After:after24.size,
    newProofOnlyWin8:after24.size-after23.size,
    conditionalUnprovedEdges:missing24.length,
    eligibleBeforeRound24:eligible23.length,
    excludedByRound24Proof:excludedByProof.length,
    excludedSelectedRound24:selected24.size,
    excludedAdditionalLoss9Parents:excludedByProof.length-selected24.size,
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
    'frozen round24 replan mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
