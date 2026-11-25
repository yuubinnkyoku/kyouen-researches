#!/usr/bin/env node
'use strict';
// Certificate-only N11 S9 replan after round14. Potential hits are not proofs.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const verify14=require('../n11-s9-post-round13-round14-20261029/verify_compact.js');
const planner=require('../n11-s9-n24-round2-20261028/plan_next.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const count=a=>planner.popcount(a.reduce((m,x)=>m|x.mask,0n));
const cost=a=>a.reduce((n,x)=>n+x.children,0);
const better=(a,b)=>count(a)>count(b)||(count(a)===count(b)&&cost(a)<cost(b));
function closure(plan,cert,win,loss,expected){
  const keys=plan.newSelectedKeys,claims=Buffer.from(cert.witnessBase64,'base64');
  need(keys.length===32&&claims.length===32&&
    sha(keys.join('\n')+'\n')===cert.selectionSha256&&
    sha(claims)===cert.witnessSha256&&
    cert.sourcePlanSha256===plan.newSelectionSha256&&
    cert.win9===win&&cert.loss9===loss,'certificate identity mismatch');
  const parents=new Set(),wins=[];
  for(let i=0;i<32;i++){
    const h=keys[i],kids=g.children(g.board(h,9));
    need(same(kids,ind.children4(h)),'independent boundary mismatch '+h);
    const ordered=[...kids].sort(),w=claims[i];
    if(w===255){wins.push(h);continue;}
    need(w<ordered.length,'invalid LOSS witness '+h);
    const leaf=ordered[w],b=BigInt('0x'+leaf);
    for(const pt of g.pts(b)){
      const par=g.key(g.canonical(b^(1n<<BigInt(pt))));
      need(g.children(g.board(par,9)).has(leaf)&&
        ind.children4(par).has(leaf),'invalid LOSS parent '+par);
      parents.add(par);
    }
  }
  need(wins.length===win&&parents.size===expected&&
    parents.size===cert.loss9ParentClosure&&
    sha([...parents].sort().join('\n')+'\n')===cert.loss9ParentSha256&&
    JSON.stringify(wins)===JSON.stringify(cert.win9Keys)&&
    wins.every(h=>!parents.has(h)),'LOSS closure mismatch');
  return parents;
}
function run(){
  const log=console.log;let checked;
  try{console.log=()=>{};checked=verify14.verify({negative:true});}
  finally{console.log=log;}
  need(checked.verified&&checked.win9===5&&checked.loss9===27&&
    checked.emptyBoard==='UNKNOWN','round14 independent terminal audit failed');
  const p8=read('../n11-s9-post-s10-reuse-round8-20261028/next-plan.json');
  const p9=read('../n11-s9-post-round9-replan-20261028/next-plan.json');
  const p10=read('../n11-s9-post-round10-replan-20261028/next-plan.json');
  const p11=read('../n11-s9-post-round11-replan-20261028/next-plan.json');
  const p12=read('../n11-s9-post-round12-replan-20261029/next-plan.json');
  const p13=read('../n11-s9-post-round13-replan-20261029/next-plan.json');
  const c9=read('../n11-s9-post-round8-round9-20261028/certificate.json');
  const c10=read('../n11-s9-post-round9-round10-20261028/certificate.json');
  const c11=read('../n11-s9-post-round10-round11-20261028/certificate.json');
  const c12=read('../n11-s9-post-round11-round12-20261028/certificate.json');
  const c13=read('../n11-s9-post-round12-round13-20261029/certificate.json');
  const c14=read('../n11-s9-post-round13-round14-20261029/certificate.json');
  const l10=read('../n11-s9-post-round9-round10-20261028/lift.json');
  const l11=read('../n11-s9-post-round10-round11-20261028/lift.json');
  const l12=read('../n11-s9-post-round11-round12-20261028/lift.json');
  const l13=read('../n11-s9-post-round12-round13-20261029/lift.json');
  const l14=read('../n11-s9-post-round13-round14-20261029/lift.json');
  const oldLoss=read('../n11-s10-cross-batch-reuse-20261028/derived-loss9.json');
  need(p9.eligibleUnprovedS9===890&&p10.eligibleUnprovedS9===709&&
    p10.conditionalUnprovedEdges===83&&p10.newSelectionSha256===c11.sourcePlanSha256&&
    c11.sourcePriorWitnessSha256===c10.witnessSha256&&
    p11.eligibleUnprovedS9===638&&p11.conditionalUnprovedEdges===79&&
    p11.newSelectionSha256===c12.sourcePlanSha256&&
    c12.sourcePriorWitnessSha256===c11.witnessSha256&&
    l10.proofOnlyWIN8After===5513&&l11.proofOnlyWIN8After===5545&&
    l11.updated.missing===79&&l11.winLossConflicts===0&&
    l12.proofOnlyWIN8After===5643&&l12.updated.missing===64&&
    l12.winLossConflicts===0&&
    p12.eligibleUnprovedS9===423&&p12.conditionalUnprovedEdges===64&&
    p12.newSelectionSha256===c13.sourcePlanSha256&&
    c13.sourcePriorWitnessSha256===c12.witnessSha256&&
    l13.proofOnlyWIN8Before===5643&&l13.verifiedWin9===4&&
    l13.verifiedLoss9===28&&l13.winLossConflicts===0&&
    p13.eligibleUnprovedS9===338&&p13.conditionalUnprovedEdges===60&&
    p13.newSelectionSha256===c14.sourcePlanSha256&&
    c14.sourcePriorWitnessSha256===c13.witnessSha256&&
    l14.proofOnlyWIN8Before===5675&&l14.proofOnlyWIN8After===5715&&
    l14.updated.missing===55&&l14.newlySecuredConditionalEdges===5&&
    l14.winLossConflicts===0&&
    p10.emptyBoard==='UNKNOWN'&&p11.emptyBoard==='UNKNOWN'&&
    l11.emptyBoard==='UNKNOWN'&&l12.emptyBoard==='UNKNOWN',
    'frozen prior evidence mismatch');
  const parents9=closure(p8,c9,5,27,270);
  const parents10=closure(p9,c10,8,24,240);
  const parents11=closure(p10,c11,4,28,280);
  const parents12=closure(p11,c12,12,20,200);
  const parents13=closure(p12,c13,4,28,280);
  const parents14=closure(p13,c14,5,27,270);
  // A newly derived LOSS9 parent must never contradict a WIN9 proven in
  // another batch; same-batch checks alone are insufficient.
  const allWin9=new Set([...c9.win9Keys,...c10.win9Keys,
    ...c11.win9Keys,...c12.win9Keys,...c13.win9Keys,...c14.win9Keys]);
  const allLoss9=new Set([...parents9,...parents10,...parents11,
    ...parents12,...parents13,...parents14]);
  need([...allWin9].every(h=>!allLoss9.has(h)),
    'cross-batch WIN9/LOSS9 contradiction');
  const inv=r7.inventory(),{s,secured}=inv;
  need(secured.size===5407&&inv.missing.length===100,
    'round7 inventory mismatch');
  const after9=new Set([...secured,...g.reverse(c9.win9Keys)]);
  const after10=new Set([...after9,...g.reverse(c10.win9Keys)]);
  const after11=new Set([...after10,...g.reverse(c11.win9Keys)]);
  const after12=new Set([...after11,...g.reverse(c12.win9Keys)]);
  const after13=new Set([...after12,...g.reverse(c13.win9Keys)]);
  const after14=new Set([...after13,...g.reverse(c14.win9Keys)]);
  need(after9.size===5449&&after10.size===5513&&after11.size===5545&&
    after12.size===5643&&after13.size===l13.proofOnlyWIN8After&&
    after14.size===5715&&[...after14].every(h=>!s.loss.has(h))&&
    [...after13].every(h=>!s.loss.has(h))&&
    JSON.stringify(r7.coverage(s.plan,after10))===JSON.stringify(l10.updated)&&
    JSON.stringify(r7.coverage(s.plan,after11))===JSON.stringify(l11.updated)&&
    JSON.stringify(r7.coverage(s.plan,after12))===JSON.stringify(l12.updated)&&
    JSON.stringify(r7.coverage(s.plan,after13))===JSON.stringify(l13.updated)&&
    JSON.stringify(r7.coverage(s.plan,after14))===JSON.stringify(l14.updated),
    'certified WIN8 frontier mismatch');
  const used7=new Set(inv.selected.map(x=>x.h));
  const oldExcluded=new Set(p8.excludedKeys),priorLoss=new Set(oldLoss.map(x=>x.h));
  const before9=inv.options.filter(x=>!used7.has(x.h)&&
    !priorLoss.has(x.h)&&!oldExcluded.has(x.h));
  need(before9.length===1011,'1011 candidate census mismatch');
  const selected9=new Set(p8.newSelectedKeys);
  const missing9=new Set([...s.plan8].filter(h=>!after9.has(h)));
  const eligible9=before9.filter(x=>!selected9.has(x.h)&&
    !parents9.has(x.h)&&x.hits.some(h=>missing9.has(h)));
  need(eligible9.length===890,'890 candidate census mismatch');
  const selected10=new Set(p9.newSelectedKeys);
  const missing10=new Set([...s.plan8].filter(h=>!after10.has(h)));
  const eligible10=eligible9.filter(x=>!selected10.has(x.h)&&
    !parents10.has(x.h)&&x.hits.some(h=>missing10.has(h)));
  need(eligible10.length===709&&
    p10.newSelectedKeys.every(h=>eligible10.some(x=>x.h===h)),
    '709 candidate census mismatch');
  const selected11=new Set(p10.newSelectedKeys);
  const missing11=new Set([...s.plan8].filter(h=>!after11.has(h)));
  const eligible11=eligible10.filter(x=>!selected11.has(x.h)&&
    !parents11.has(x.h)&&x.hits.some(h=>missing11.has(h)));
  need(eligible11.length===638&&
    p11.newSelectedKeys.every(h=>eligible11.some(x=>x.h===h)),
    '638 candidate census mismatch');
  const selected12=new Set(p11.newSelectedKeys);
  const excludedByProof=eligible11.filter(x=>
    selected12.has(x.h)||parents12.has(x.h));
  need(p11.newSelectedKeys.every(h=>excludedByProof.some(x=>x.h===h)),
    'round12 selection exclusion incomplete');
  const remaining=eligible11.filter(x=>
    !selected12.has(x.h)&&!parents12.has(x.h));
  const missing=[...s.plan8].filter(h=>!after12.has(h)).sort();
  need(missing.length===64,'64-edge frontier mismatch');
  const index=new Map(missing.map((h,i)=>[h,i]));
  const eligible=remaining.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index.has(h))mask|=1n<<BigInt(index.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  need(eligible.length===423&&
    p12.newSelectedKeys.every(h=>eligible.some(x=>x.h===h)),
    '423 candidate census mismatch');
  const selected13=new Set(p12.newSelectedKeys);
  const excludedByProof13=eligible.filter(x=>
    selected13.has(x.h)||parents13.has(x.h));
  need(p12.newSelectedKeys.every(h=>excludedByProof13.some(x=>x.h===h)),
    'round13 selection exclusion incomplete');
  const remaining13=eligible.filter(x=>
    !selected13.has(x.h)&&!parents13.has(x.h));
  const missing13=[...s.plan8].filter(h=>!after13.has(h)).sort();
  need(missing13.length===l13.updated.missing,
    'round13 conditional frontier mismatch');
  const index13=new Map(missing13.map((h,i)=>[h,i]));
  const eligible13=remaining13.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index13.has(h))mask|=1n<<BigInt(index13.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  need(eligible13.length>=32,'fewer than 32 eligible round14 candidates');
  need(eligible13.length===338&&
    p13.newSelectedKeys.every(h=>eligible13.some(x=>x.h===h)),
    '338 candidate census mismatch');
  const selected14=new Set(p13.newSelectedKeys);
  const excludedByProof14=eligible13.filter(x=>
    selected14.has(x.h)||parents14.has(x.h));
  need(p13.newSelectedKeys.every(h=>excludedByProof14.some(x=>x.h===h)),
    'round14 selection exclusion incomplete');
  const remaining14=eligible13.filter(x=>
    !selected14.has(x.h)&&!parents14.has(x.h));
  const missing14=[...s.plan8].filter(h=>!after14.has(h)).sort();
  need(missing14.length===55,'round14 conditional frontier mismatch');
  const index14=new Map(missing14.map((h,i)=>[h,i]));
  const eligible14=remaining14.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index14.has(h))mask|=1n<<BigInt(index14.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  need(eligible14.length>=32,'fewer than 32 eligible round15 candidates');
  const reduced=planner.pruneDominated(eligible14);
  const baseline=planner.greedy(eligible14,32);
  const rg=planner.greedy(reduced,32);
  const optimized=planner.improve(reduced,better(rg,baseline)?rg:baseline);
  const chosen=optimized.picked;
  need(chosen.length===32&&new Set(chosen.map(x=>x.h)).size===32&&
    !better(baseline,chosen)&&
    chosen.every(x=>!selected14.has(x.h)&&!parents14.has(x.h)),
    'candidate selection invalid');
  const result={
    schema:'n11-post-round14-proof-only-replan-v1',emptyBoard:'UNKNOWN',
    sourceSelectionSha256:c14.selectionSha256,
    sourceWitnessSha256:c14.witnessSha256,
    independentlyVerifiedTerminalLeaves:checked.uniqueTerminalLeaves,
    terminalStatesPerGeometry:checked.terminalStatesPerGeometry,
    verifiedWin9:5,verifiedLoss9:27,
    derivedLoss9ParentClosure:parents14.size,
    proofOnlyWin8Before:after13.size,proofOnlyWin8After:after14.size,
    newProofOnlyWin8:after14.size-after13.size,
    conditionalUnprovedEdges:missing14.length,
    eligibleBeforeRound14:eligible13.length,
    excludedByRound14Proof:excludedByProof14.length,
    excludedSelectedRound14:selected14.size,
    excludedAdditionalLoss9Parents:excludedByProof14.length-selected14.size,
    remainingAfterProofExclusions:remaining14.length,
    noLongerTouchesUnprovedS8:remaining14.length-eligible14.length,
    eligibleUnprovedS9:eligible14.length,undominatedS9:reduced.length,
    baselinePotentialCoverage:count(baseline),potentialCoverage:count(chosen),
    legal10Children:cost(chosen),exchanges:optimized.swaps,
    newSelectedKeys:chosen.map(x=>x.h),
    newSelectionSha256:sha(chosen.map(x=>x.h).join('\n')+'\n'),
    winLossConflicts:0,newS7Verdicts:0,newS5Verdicts:0,newTwoStoneClosures:0
  };
  const frozen=path.join(__dirname,'next-plan.json');
  if(fs.existsSync(frozen))need(
    JSON.stringify(read('next-plan.json'))===JSON.stringify(result),
    'frozen round14 replan mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
