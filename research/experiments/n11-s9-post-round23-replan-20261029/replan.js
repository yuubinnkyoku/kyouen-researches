#!/usr/bin/env node
'use strict';
// Replan the conditional N11 fourteen-root S8 frontier after round23.
// Only independently verified certificates count as proven coverage.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const planner=require('../n11-s9-n24-round2-20261028/plan_next.js');
const verify23=require('../n11-s9-post-round22-round23-20261029/verify_compact.js');
const need=(v,m)=>{if(!v)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const pop=rows=>planner.popcount(rows.reduce((m,x)=>m|x.mask,0n));
const cost=rows=>rows.reduce((n,x)=>n+x.children,0);
const better=(a,b)=>pop(a)>pop(b)||(pop(a)===pop(b)&&cost(a)<cost(b));
const planDirs=[
  'n11-s9-post-s10-reuse-round8-20261028',
  ...Array.from({length:14},(_,i)=>{
    const n=i+9,day=n<=11?'20261028':'20261029';
    return 'n11-s9-post-round'+n+'-replan-'+day;
  })
];
const certDirs=[
  'n11-s9-post-round8-round9-20261028',
  ...Array.from({length:14},(_,i)=>{
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
  const prior=read('../n11-s9-post-round22-replan-20261029/next-plan.json');
  const cert23=read('../n11-s9-post-round22-round23-20261029/certificate.json');
  const lift23=read('../n11-s9-post-round22-round23-20261029/lift.json');
  need(prior.schema==='n11-post-round22-proof-only-replan-v1'&&
    prior.emptyBoard==='UNKNOWN'&&prior.conditionalUnprovedEdges===40&&
    prior.proofOnlyWin8After===5835&&prior.selectedCount===5&&
    prior.newSelectionSha256==='f1c6e9763fa9b13daf42d8b71147d4e230c3dc1de45cace72888a6428db7046d'&&
    cert23.sourcePlanSha256===prior.newSelectionSha256&&
    cert23.win9===2&&cert23.loss9===3&&
    cert23.loss9ParentClosure===30&&cert23.newTwoStoneClosures===0&&
    lift23.proofOnlyWIN8Before===5835&&lift23.proofOnlyWIN8After===5851&&
    lift23.newProofOnlyWIN8===16&&lift23.updated.missing===38&&
    lift23.winLossConflicts===0,
    'frozen round22 plan / round23 certificate / lift mismatch');
  let checked23;
  const originalLog=console.log;
  try{console.log=()=>{};checked23=verify23.verify({negative:true});}
  finally{console.log=originalLog;}
  need(checked23.verified&&checked23.win9===2&&checked23.loss9===3&&
    checked23.emptyBoard==='UNKNOWN','round23 independent terminal replay failed');
  const plans=planDirs.map(d=>read('../'+d+'/next-plan.json'));
  const certs=certDirs.map(d=>read('../'+d+'/certificate.json'));
  need(plans.length===15&&certs.length===15&&
    plans[14].newSelectionSha256===prior.newSelectionSha256&&
    certs[14].witnessSha256===cert23.witnessSha256&&
    cert23.sourcePriorWitnessSha256===certs[13].witnessSha256,
    'round23 chain input mismatch');
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
  const after22=new Set(secured);
  for(let i=0;i<14;i++)for(const h of g.reverse(certs[i].win9Keys))after22.add(h);
  const derived23=g.reverse(cert23.win9Keys);
  need(derived23.size===18,'round23 WIN9 parent count mismatch');
  const after23=new Set([...after22,...derived23]);
  need(after22.size===5835&&after23.size===5851&&
    [...after23].every(h=>!s.loss.has(h))&&
    r7.coverage(s.plan,after22).missing===40&&
    r7.coverage(s.plan,after23).missing===38,
    'WIN8 frontier mismatch');
  const p8=plans[0];
  const oldLoss=read('../n11-s10-cross-batch-reuse-20261028/derived-loss9.json');
  const priorExcluded=new Set([...p8.excludedKeys,...oldLoss.map(x=>x.h)]);
  const used7=new Set(inv.selected.map(x=>x.h));
  const selectedBefore23=new Set(plans.slice(0,14).flatMap(p=>p.newSelectedKeys));
  const lossBefore23=new Set(parents.slice(0,14).flatMap(p=>[...p]));
  const missing22=new Set([...s.plan8].filter(h=>!after22.has(h)));
  const eligible22=inv.options.filter(x=>!used7.has(x.h)&&
    !priorExcluded.has(x.h)&&!selectedBefore23.has(x.h)&&
    !lossBefore23.has(x.h)&&x.hits.some(h=>missing22.has(h)));
  need(eligible22.length===27&&prior.selectedCount===5&&
    prior.newSelectedKeys.every(h=>eligible22.some(x=>x.h===h)),
    'round22 candidate census mismatch');
  const selected23=new Set(prior.newSelectedKeys),parents23=parents[14];
  const excludedByProof=eligible22.filter(x=>
    selected23.has(x.h)||parents23.has(x.h));
  need([...selected23].every(h=>excludedByProof.some(x=>x.h===h)),
    'round23 selected candidates not excluded');
  const remaining=eligible22.filter(x=>
    !selected23.has(x.h)&&!parents23.has(x.h));
  const missing23=[...s.plan8].filter(h=>!after23.has(h)).sort();
  need(missing23.length===38,'round23 missing edge mismatch');
  const index=new Map(missing23.map((h,i)=>[h,i]));
  const eligible=remaining.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index.has(h))mask|=1n<<BigInt(index.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  need(eligible.length>0,'no eligible round24 candidate');
  const reduced=planner.pruneDominated(eligible);
  const baseline=planner.greedy(eligible,32);
  const rg=planner.greedy(reduced,32);
  const optimized=planner.improve(reduced,better(rg,baseline)?rg:baseline);
  const chosen=optimized.picked;
  need(chosen.length>0&&chosen.length<=32&&
    new Set(chosen.map(x=>x.h)).size===chosen.length&&
    !better(baseline,chosen)&&
    chosen.every(x=>!selected23.has(x.h)&&!parents23.has(x.h)),
    'round24 candidate selection invalid');
  const result={
    schema:'n11-post-round23-proof-only-replan-v1',emptyBoard:'UNKNOWN',
    sourceSelectionSha256:cert23.selectionSha256,
    sourceWitnessSha256:cert23.witnessSha256,
    independentlyVerifiedTerminalLeaves:checked23.uniqueTerminalLeaves,
    terminalStatesPerGeometry:checked23.terminalStatesPerGeometry,
    verifiedWin9:cert23.win9,verifiedLoss9:cert23.loss9,
    derivedLoss9ParentClosure:parents23.size,
    proofOnlyWin8Before:after22.size,proofOnlyWin8After:after23.size,
    newProofOnlyWin8:after23.size-after22.size,
    conditionalUnprovedEdges:missing23.length,
    eligibleBeforeRound23:eligible22.length,
    excludedByRound23Proof:excludedByProof.length,
    excludedSelectedRound23:selected23.size,
    excludedAdditionalLoss9Parents:excludedByProof.length-selected23.size,
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
    'frozen round23 replan mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
