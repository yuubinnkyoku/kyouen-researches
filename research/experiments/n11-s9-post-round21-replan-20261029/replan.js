#!/usr/bin/env node
'use strict';
// Replan the conditional N11 fourteen-root S8 frontier after round21.
// Only independently verified certificates count as proven coverage.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const planner=require('../n11-s9-n24-round2-20261028/plan_next.js');
const verify21=require('../n11-s9-post-round20-round21-20261029/verify_compact.js');
const need=(v,m)=>{if(!v)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const pop=rows=>planner.popcount(rows.reduce((m,x)=>m|x.mask,0n));
const cost=rows=>rows.reduce((n,x)=>n+x.children,0);
const better=(a,b)=>pop(a)>pop(b)||(pop(a)===pop(b)&&cost(a)<cost(b));
const planDirs=[
  'n11-s9-post-s10-reuse-round8-20261028',
  ...Array.from({length:12},(_,i)=>{
    const n=i+9,day=n<=11?'20261028':'20261029';
    return 'n11-s9-post-round'+n+'-replan-'+day;
  })
];
const certDirs=[
  'n11-s9-post-round8-round9-20261028',
  ...Array.from({length:12},(_,i)=>{
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
  // Audit the current terminal certificate; reuse the previous independently
  // audited fixed plan/lift rather than recursively rerunning every replan.
  const prior=read('../n11-s9-post-round20-replan-20261029/next-plan.json');
  const lift=read('../n11-s9-post-round20-round21-20261029/lift.json');
  const cert21=read('../n11-s9-post-round20-round21-20261029/certificate.json');
  need(prior.schema==='n11-post-round20-proof-only-replan-v1'&&
    prior.emptyBoard==='UNKNOWN'&&prior.conditionalUnprovedEdges===41&&
    prior.proofOnlyWin8After===5827&&prior.selectedCount===8&&
    prior.newSelectionSha256==='19e4e61fd96850a7f01aa64a5561e0f8d10ce81d3e9bbffe983b388d07a80bf0'&&
    lift.proofOnlyWIN8Before===5827&&lift.proofOnlyWIN8After===5835&&
    lift.updated.missing===40&&lift.newlySecuredConditionalEdges===1&&
    lift.winLossConflicts===0&&lift.newTwoStoneClosures===0,
    'frozen round20 plan / round21 lift mismatch');
  let checked21;
  const originalLog=console.log;
  try{console.log=()=>{};checked21=verify21.verify({negative:true});}
  finally{console.log=originalLog;}
  need(checked21.verified&&checked21.win9===1&&checked21.loss9===7&&
    checked21.emptyBoard==='UNKNOWN','round21 independent terminal replay failed');
  const plans=planDirs.map(d=>read('../'+d+'/next-plan.json'));
  const certs=certDirs.map(d=>read('../'+d+'/certificate.json'));
  need(plans.length===13&&certs.length===13&&
    plans[12].newSelectionSha256===prior.newSelectionSha256&&
    certs[12].witnessSha256===cert21.witnessSha256&&
    cert21.sourcePriorWitnessSha256===certs[11].witnessSha256,
    'round21 chain input mismatch');
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
  const after20=new Set(secured);
  for(let i=0;i<12;i++)for(const h of g.reverse(certs[i].win9Keys))after20.add(h);
  const derived21=g.reverse(cert21.win9Keys);
  for(const h of cert21.win9Keys)for(const par of g.reverse([h]))
    need(g.children(g.board(par,8)).has(h)&&ind.children4(par).has(h),
      'illegal round21 WIN8 witness '+h);
  const after21=new Set([...after20,...derived21]);
  need(after20.size===5827&&after21.size===5835&&
    [...after21].every(h=>!s.loss.has(h))&&
    JSON.stringify(r7.coverage(s.plan,after21))===JSON.stringify(lift.updated),
    'WIN8 frontier mismatch');
  const p8=plans[0];
  const oldLoss=read('../n11-s10-cross-batch-reuse-20261028/derived-loss9.json');
  const priorExcluded=new Set([...p8.excludedKeys,...oldLoss.map(x=>x.h)]);
  const used7=new Set(inv.selected.map(x=>x.h));
  const selectedBefore21=new Set(plans.slice(0,12).flatMap(p=>p.newSelectedKeys));
  const lossBefore21=new Set(parents.slice(0,12).flatMap(p=>[...p]));
  const missing20=new Set([...s.plan8].filter(h=>!after20.has(h)));
  const eligible20=inv.options.filter(x=>!used7.has(x.h)&&
    !priorExcluded.has(x.h)&&!selectedBefore21.has(x.h)&&
    !lossBefore21.has(x.h)&&x.hits.some(h=>missing20.has(h)));
  need(eligible20.length===47&&prior.selectedCount===8&&
    prior.newSelectedKeys.every(h=>eligible20.some(x=>x.h===h)),
    'round20 candidate census mismatch');
  const selected21=new Set(prior.newSelectedKeys),parents21=parents[12];
  const excludedByProof=eligible20.filter(x=>
    selected21.has(x.h)||parents21.has(x.h));
  need([...selected21].every(h=>excludedByProof.some(x=>x.h===h)),
    'round21 selected candidates not excluded');
  const remaining=eligible20.filter(x=>
    !selected21.has(x.h)&&!parents21.has(x.h));
  const missing21=[...s.plan8].filter(h=>!after21.has(h)).sort();
  need(missing21.length===40,'round21 missing edge mismatch');
  const index=new Map(missing21.map((h,i)=>[h,i]));
  const eligible=remaining.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index.has(h))mask|=1n<<BigInt(index.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  need(eligible.length>0,'no eligible round22 candidate');
  const reduced=planner.pruneDominated(eligible);
  const baseline=planner.greedy(eligible,32);
  const rg=planner.greedy(reduced,32);
  const optimized=planner.improve(reduced,better(rg,baseline)?rg:baseline);
  const chosen=optimized.picked;
  need(chosen.length>0&&chosen.length<=32&&
    new Set(chosen.map(x=>x.h)).size===chosen.length&&
    !better(baseline,chosen)&&
    chosen.every(x=>!selected21.has(x.h)&&!parents21.has(x.h)),
    'round22 candidate selection invalid');
  const result={
    schema:'n11-post-round21-proof-only-replan-v1',emptyBoard:'UNKNOWN',
    sourceSelectionSha256:cert21.selectionSha256,
    sourceWitnessSha256:cert21.witnessSha256,
    independentlyVerifiedTerminalLeaves:checked21.uniqueTerminalLeaves,
    terminalStatesPerGeometry:checked21.terminalStatesPerGeometry,
    verifiedWin9:cert21.win9,verifiedLoss9:cert21.loss9,
    derivedLoss9ParentClosure:parents21.size,
    proofOnlyWin8Before:after20.size,proofOnlyWin8After:after21.size,
    newProofOnlyWin8:after21.size-after20.size,
    conditionalUnprovedEdges:missing21.length,
    eligibleBeforeRound21:eligible20.length,
    excludedByRound21Proof:excludedByProof.length,
    excludedSelectedRound21:selected21.size,
    excludedAdditionalLoss9Parents:excludedByProof.length-selected21.size,
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
    'frozen round21 replan mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
