#!/usr/bin/env node
'use strict';
// Replan the conditional N11 fourteen-root S8 frontier after round26.
// Only independently verified certificates count as proven coverage.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const planner=require('../n11-s9-n24-round2-20261028/plan_next.js');
const verify26=require('../n11-s9-post-round25-round26-20261029/verify_compact.js');
const need=(v,m)=>{if(!v)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const pop=rows=>planner.popcount(rows.reduce((m,x)=>m|x.mask,0n));
const cost=rows=>rows.reduce((n,x)=>n+x.children,0);
const better=(a,b)=>pop(a)>pop(b)||(pop(a)===pop(b)&&cost(a)<cost(b));
const planDirs=[
  'n11-s9-post-s10-reuse-round8-20261028',
  ...Array.from({length:17},(_,i)=>{
    const n=i+9,day=n<=11?'20261028':'20261029';
    return 'n11-s9-post-round'+n+'-replan-'+day;
  })
];
const certDirs=[
  'n11-s9-post-round8-round9-20261028',
  ...Array.from({length:17},(_,i)=>{
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
  const prior=read('../n11-s9-post-round25-replan-20261029/next-plan.json');
  const cert26=read('../n11-s9-post-round25-round26-20261029/certificate.json');
  const lift24=read('../n11-s9-post-round23-round24-20261029/lift.json');
  need(prior.schema==='n11-post-round25-proof-only-replan-v1'&&
    prior.emptyBoard==='UNKNOWN'&&prior.conditionalUnprovedEdges===37&&
    prior.proofOnlyWin8After===5859&&prior.selectedCount===1&&
    prior.eligibleUnprovedS9===7&&
    prior.newSelectionSha256==='b94d401cdc0fe573c5a58f7a2a98b0b03856f10e7c3fb815cb8ac9d82b2001cb'&&
    cert26.sourcePlanSha256===prior.newSelectionSha256&&
    cert26.win9===0&&cert26.loss9===1&&
    cert26.loss9ParentClosure===10&&cert26.newTwoStoneClosures===0&&
    lift24.proofOnlyWIN8Before===5851&&lift24.proofOnlyWIN8After===5859&&
    lift24.newProofOnlyWIN8===8&&lift24.updated.missing===37&&
    lift24.winLossConflicts===0,'frozen preceding proofs mismatch');
  let checked26;
  const originalLog=console.log;
  try{console.log=()=>{};checked26=verify26.verify({negative:true});}
  finally{console.log=originalLog;}
  need(checked26.verified&&checked26.win9===0&&checked26.loss9===1&&
    checked26.uniqueTerminalLeaves===1&&
    checked26.terminalStatesPerGeometry===439&&
    checked26.emptyBoard==='UNKNOWN','round26 independent terminal replay failed');
  const plans=planDirs.map(d=>read('../'+d+'/next-plan.json'));
  const certs=certDirs.map(d=>read('../'+d+'/certificate.json'));
  need(plans.length===18&&certs.length===18&&
    plans[17].newSelectionSha256===prior.newSelectionSha256&&
    certs[17].witnessSha256===cert26.witnessSha256&&
    cert26.sourcePriorWitnessSha256===certs[16].witnessSha256,
    'round26 chain input mismatch');
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
  const after25=new Set(secured);
  for(let i=0;i<17;i++)for(const h of g.reverse(certs[i].win9Keys))after25.add(h);
  const derived26=g.reverse(cert26.win9Keys);
  need(derived26.size===0,'round26 WIN9 parent count mismatch');
  const after26=new Set([...after25,...derived26]);
  need(after25.size===5859&&after26.size===5859&&
    [...after26].every(h=>!s.loss.has(h))&&
    r7.coverage(s.plan,after25).missing===37&&
    r7.coverage(s.plan,after26).missing===37,
    'WIN8 frontier mismatch');
  const p8=plans[0];
  const oldLoss=read('../n11-s10-cross-batch-reuse-20261028/derived-loss9.json');
  const priorExcluded=new Set([...p8.excludedKeys,...oldLoss.map(x=>x.h)]);
  const used7=new Set(inv.selected.map(x=>x.h));
  const selectedBefore26=new Set(plans.slice(0,17).flatMap(p=>p.newSelectedKeys));
  const lossBefore26=new Set(parents.slice(0,17).flatMap(p=>[...p]));
  const missing25=new Set([...s.plan8].filter(h=>!after25.has(h)));
  const eligible25=inv.options.filter(x=>!used7.has(x.h)&&
    !priorExcluded.has(x.h)&&!selectedBefore26.has(x.h)&&
    !lossBefore26.has(x.h)&&x.hits.some(h=>missing25.has(h)));
  need(eligible25.length===7&&
    prior.newSelectedKeys.every(h=>eligible25.some(x=>x.h===h)),
    'round25 candidate census mismatch');
  const selected26=new Set(prior.newSelectedKeys),parents26=parents[17];
  const excludedByProof=eligible25.filter(x=>
    selected26.has(x.h)||parents26.has(x.h));
  need([...selected26].every(h=>excludedByProof.some(x=>x.h)),
    'round26 selected candidates not excluded');
  const remaining=eligible25.filter(x=>
    !selected26.has(x.h)&&!parents26.has(x.h));
  const missing26=[...s.plan8].filter(h=>!after26.has(h)).sort();
  need(missing26.length===37,'round26 missing edge mismatch');
  const index=new Map(missing26.map((h,i)=>[h,i]));
  const eligible=remaining.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index.has(h))mask|=1n<<BigInt(index.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  const reduced=eligible.length?planner.pruneDominated(eligible):[];
  const baseline=eligible.length?planner.greedy(eligible,32):[];
  const rg=reduced.length?planner.greedy(reduced,32):[];
  const optimized=reduced.length?
    planner.improve(reduced,better(rg,baseline)?rg:baseline):
    {picked:[],swaps:0};
  const chosen=optimized.picked;
  need(chosen.length<=32&&new Set(chosen.map(x=>x.h)).size===chosen.length&&
    !better(baseline,chosen)&&
    chosen.every(x=>!selected26.has(x.h)&&!parents26.has(x.h)),
    'round27 candidate selection invalid');
  const result={
    schema:'n11-post-round26-proof-only-replan-v1',emptyBoard:'UNKNOWN',
    sourceSelectionSha256:cert26.selectionSha256,
    sourceWitnessSha256:cert26.witnessSha256,
    independentlyVerifiedTerminalLeaves:checked26.uniqueTerminalLeaves,
    terminalStatesPerGeometry:checked26.terminalStatesPerGeometry,
    verifiedWin9:cert26.win9,verifiedLoss9:cert26.loss9,
    derivedLoss9ParentClosure:parents26.size,
    proofOnlyWin8Before:after25.size,proofOnlyWin8After:after26.size,
    newProofOnlyWin8:after26.size-after25.size,
    conditionalUnprovedEdges:missing26.length,
    eligibleBeforeRound26:eligible25.length,
    excludedByRound26Proof:excludedByProof.length,
    excludedSelectedRound26:selected26.size,
    excludedAdditionalLoss9Parents:excludedByProof.length-selected26.size,
    remainingAfterProofExclusions:remaining.length,
    noLongerTouchesUnprovedS8:remaining.length-eligible.length,
    eligibleUnprovedS9:eligible.length,undominatedS9:reduced.length,
    baselinePotentialCoverage:pop(baseline),potentialCoverage:pop(chosen),
    legal10Children:cost(chosen),exchanges:optimized.swaps,
    selectedCount:chosen.length,newSelectedKeys:chosen.map(x=>x.h),
    newSelectionSha256:sha(chosen.map(x=>x.h).join('\n')+'\n'),
    exhaustedCandidatePool:eligible.length===0,
    winLossConflicts:0,newS7Verdicts:0,newS5Verdicts:0,newTwoStoneClosures:0
  };
  const fixed=path.join(__dirname,'next-plan.json');
  if(fs.existsSync(fixed))need(
    JSON.stringify(read('next-plan.json'))===JSON.stringify(result),
    'frozen round26 replan mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
