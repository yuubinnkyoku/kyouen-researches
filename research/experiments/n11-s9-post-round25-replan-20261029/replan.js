#!/usr/bin/env node
'use strict';
// Replan the conditional N11 fourteen-root S8 frontier after round25.
// Only independently verified certificates count as proven coverage.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const planner=require('../n11-s9-n24-round2-20261028/plan_next.js');
const verify25=require('../n11-s9-post-round24-round25-20261029/verify_compact.js');
const need=(v,m)=>{if(!v)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const pop=rows=>planner.popcount(rows.reduce((m,x)=>m|x.mask,0n));
const cost=rows=>rows.reduce((n,x)=>n+x.children,0);
const better=(a,b)=>pop(a)>pop(b)||(pop(a)===pop(b)&&cost(a)<cost(b));
const planDirs=[
  'n11-s9-post-s10-reuse-round8-20261028',
  ...Array.from({length:16},(_,i)=>{
    const n=i+9,day=n<=11?'20261028':'20261029';
    return 'n11-s9-post-round'+n+'-replan-'+day;
  })
];
const certDirs=[
  'n11-s9-post-round8-round9-20261028',
  ...Array.from({length:16},(_,i)=>{
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
  // Recheck the latest terminal certificate and all earlier fixed proof
  // identities. A search frontier alone never establishes a verdict.
  const prior=read('../n11-s9-post-round24-replan-20261029/next-plan.json');
  const cert25=read('../n11-s9-post-round24-round25-20261029/certificate.json');
  const lift24=read('../n11-s9-post-round23-round24-20261029/lift.json');
  need(prior.schema==='n11-post-round24-proof-only-replan-v1'&&
    prior.emptyBoard==='UNKNOWN'&&prior.conditionalUnprovedEdges===37&&
    prior.proofOnlyWin8After===5859&&prior.selectedCount===1&&
    prior.newSelectionSha256==='3a830c2fd7e01a99f613a6bab5f5e0e3ab5f38433203a28fc3a35573ae4def59'&&
    cert25.sourcePlanSha256===prior.newSelectionSha256&&
    cert25.win9===0&&cert25.loss9===1&&
    cert25.loss9ParentClosure===10&&cert25.newTwoStoneClosures===0&&
    lift24.proofOnlyWIN8Before===5851&&lift24.proofOnlyWIN8After===5859&&
    lift24.newProofOnlyWIN8===8&&lift24.updated.missing===37&&
    lift24.winLossConflicts===0,
    'frozen round24 plan / round25 certificate / preceding lift mismatch');
  let checked25;
  const originalLog=console.log;
  try{console.log=()=>{};checked25=verify25.verify({negative:true});}
  finally{console.log=originalLog;}
  need(checked25.verified&&checked25.win9===0&&checked25.loss9===1&&
    checked25.uniqueTerminalLeaves===1&&
    checked25.terminalStatesPerGeometry===499&&
    checked25.emptyBoard==='UNKNOWN','round25 independent terminal replay failed');
  const plans=planDirs.map(d=>read('../'+d+'/next-plan.json'));
  const certs=certDirs.map(d=>read('../'+d+'/certificate.json'));
  need(plans.length===17&&certs.length===17&&
    plans[16].newSelectionSha256===prior.newSelectionSha256&&
    certs[16].witnessSha256===cert25.witnessSha256&&
    cert25.sourcePriorWitnessSha256===certs[15].witnessSha256,
    'round25 chain input mismatch');
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
  const after24=new Set(secured);
  for(let i=0;i<16;i++)for(const h of g.reverse(certs[i].win9Keys))after24.add(h);
  const derived25=g.reverse(cert25.win9Keys);
  need(derived25.size===0,'round25 WIN9 parent count mismatch');
  const after25=new Set([...after24,...derived25]);
  need(after24.size===5859&&after25.size===5859&&
    [...after25].every(h=>!s.loss.has(h))&&
    r7.coverage(s.plan,after24).missing===37&&
    r7.coverage(s.plan,after25).missing===37,
    'WIN8 frontier mismatch');
  const p8=plans[0];
  const oldLoss=read('../n11-s10-cross-batch-reuse-20261028/derived-loss9.json');
  const priorExcluded=new Set([...p8.excludedKeys,...oldLoss.map(x=>x.h)]);
  const used7=new Set(inv.selected.map(x=>x.h));
  const selectedBefore25=new Set(plans.slice(0,16).flatMap(p=>p.newSelectedKeys));
  const lossBefore25=new Set(parents.slice(0,16).flatMap(p=>[...p]));
  const missing24=new Set([...s.plan8].filter(h=>!after24.has(h)));
  const eligible24=inv.options.filter(x=>!used7.has(x.h)&&
    !priorExcluded.has(x.h)&&!selectedBefore25.has(x.h)&&
    !lossBefore25.has(x.h)&&x.hits.some(h=>missing24.has(h)));
  need(eligible24.length===8&&prior.selectedCount===1&&
    prior.newSelectedKeys.every(h=>eligible24.some(x=>x.h===h)),
    'round24 candidate census mismatch');
  const selected25=new Set(prior.newSelectedKeys),parents25=parents[16];
  const excludedByProof=eligible24.filter(x=>
    selected25.has(x.h)||parents25.has(x.h));
  need([...selected25].every(h=>excludedByProof.some(x=>x.h)),
    'round25 selected candidates not excluded');
  const remaining=eligible24.filter(x=>
    !selected25.has(x.h)&&!parents25.has(x.h));
  const missing25=[...s.plan8].filter(h=>!after25.has(h)).sort();
  need(missing25.length===37,'round25 missing edge mismatch');
  const index=new Map(missing25.map((h,i)=>[h,i]));
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
    chosen.every(x=>!selected25.has(x.h)&&!parents25.has(x.h)),
    'round26 candidate selection invalid');
  const result={
    schema:'n11-post-round25-proof-only-replan-v1',emptyBoard:'UNKNOWN',
    sourceSelectionSha256:cert25.selectionSha256,
    sourceWitnessSha256:cert25.witnessSha256,
    independentlyVerifiedTerminalLeaves:checked25.uniqueTerminalLeaves,
    terminalStatesPerGeometry:checked25.terminalStatesPerGeometry,
    verifiedWin9:cert25.win9,verifiedLoss9:cert25.loss9,
    derivedLoss9ParentClosure:parents25.size,
    proofOnlyWin8Before:after24.size,proofOnlyWin8After:after25.size,
    newProofOnlyWin8:after25.size-after24.size,
    conditionalUnprovedEdges:missing25.length,
    eligibleBeforeRound25:eligible24.length,
    excludedByRound25Proof:excludedByProof.length,
    excludedSelectedRound25:selected25.size,
    excludedAdditionalLoss9Parents:excludedByProof.length-selected25.size,
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
    'frozen round25 replan mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
