#!/usr/bin/env node
'use strict';
// Certificate-only N11 S9 replan after round19. Frozen witnesses are independently rechecked. Potential hits are not proofs.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const verify18=require('../n11-s9-post-round17-round18-20261029/verify_compact.js');
const lift18=require('../n11-s9-post-round17-round18-20261029/lift.js');
const verify19=require('../n11-s9-post-round18-round19-20261029/verify_compact.js');
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
  need(keys.length===win+loss&&claims.length===keys.length&&
    sha(keys.join('\n')+'\n')===cert.selectionSha256&&
    sha(claims)===cert.witnessSha256&&
    cert.sourcePlanSha256===plan.newSelectionSha256&&
    cert.win9===win&&cert.loss9===loss,'certificate identity mismatch');
  const parents=new Set(),wins=[];
  for(let i=0;i<keys.length;i++){
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
  try{console.log=()=>{};checked=verify18.verify({negative:true});}
  finally{console.log=log;}
  need(checked.verified&&checked.win9===1&&checked.loss9===13&&
    checked.emptyBoard==='UNKNOWN','round18 independent terminal audit failed');
  const p8=read('../n11-s9-post-s10-reuse-round8-20261028/next-plan.json');
  const p9=read('../n11-s9-post-round9-replan-20261028/next-plan.json');
  const p10=read('../n11-s9-post-round10-replan-20261028/next-plan.json');
  const p11=read('../n11-s9-post-round11-replan-20261028/next-plan.json');
  const p12=read('../n11-s9-post-round12-replan-20261029/next-plan.json');
  const p13=read('../n11-s9-post-round13-replan-20261029/next-plan.json');
  const p14=read('../n11-s9-post-round14-replan-20261029/next-plan.json');
  const p15=read('../n11-s9-post-round15-replan-20261029/next-plan.json');
  const p16=read('../n11-s9-post-round16-replan-20261029/next-plan.json');
  const p17=read('../n11-s9-post-round17-replan-20261029/next-plan.json');
  const c9=read('../n11-s9-post-round8-round9-20261028/certificate.json');
  const c10=read('../n11-s9-post-round9-round10-20261028/certificate.json');
  const c11=read('../n11-s9-post-round10-round11-20261028/certificate.json');
  const c12=read('../n11-s9-post-round11-round12-20261028/certificate.json');
  const c13=read('../n11-s9-post-round12-round13-20261029/certificate.json');
  const c14=read('../n11-s9-post-round13-round14-20261029/certificate.json');
  const c15=read('../n11-s9-post-round14-round15-20261029/certificate.json');
  const c16=read('../n11-s9-post-round15-round16-20261029/certificate.json');
  const c17=read('../n11-s9-post-round16-round17-20261029/certificate.json');
  const c18=read('../n11-s9-post-round17-round18-20261029/certificate.json');
  const p18=read('../n11-s9-post-round18-replan-20261029/next-plan.json');
  const c19=read('../n11-s9-post-round18-round19-20261029/certificate.json');
  const l19=read('../n11-s9-post-round18-round19-20261029/lift.json');
  const l10=read('../n11-s9-post-round9-round10-20261028/lift.json');
  const l11=read('../n11-s9-post-round10-round11-20261028/lift.json');
  const l12=read('../n11-s9-post-round11-round12-20261028/lift.json');
  const l13=read('../n11-s9-post-round12-round13-20261029/lift.json');
  const l14=read('../n11-s9-post-round13-round14-20261029/lift.json');
  const l15=read('../n11-s9-post-round14-round15-20261029/lift.json');
  const l16=read('../n11-s9-post-round15-round16-20261029/lift.json');
  const l17=read('../n11-s9-post-round16-round17-20261029/lift.json');
  const savedLog=console.log;let l18;
  try{console.log=()=>{};l18=lift18.run();}
  finally{console.log=savedLog;}
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
    p14.eligibleUnprovedS9===269&&p14.conditionalUnprovedEdges===55&&
    p14.newSelectionSha256===c15.sourcePlanSha256&&
    c15.sourcePriorWitnessSha256===c14.witnessSha256&&
    l15.proofOnlyWIN8Before===5715&&l15.proofOnlyWIN8After===5739&&
    l15.updated.missing===52&&l15.newProofOnlyWIN8===24&&
    l15.newlySecuredConditionalEdges===3&&l15.winLossConflicts===0&&
    p15.eligibleUnprovedS9===215&&p15.conditionalUnprovedEdges===52&&
    p15.newSelectionSha256===c16.sourcePlanSha256&&
    c16.sourcePriorWitnessSha256===c15.witnessSha256&&
    l16.proofOnlyWIN8Before===5739&&l16.proofOnlyWIN8After===5763&&
    l16.updated.missing===49&&l16.newProofOnlyWIN8===24&&
    l16.newlySecuredConditionalEdges===3&&l16.winLossConflicts===0&&
    p16.eligibleUnprovedS9===158&&p16.conditionalUnprovedEdges===49&&
    p16.newSelectionSha256===c17.sourcePlanSha256&&
    c17.sourcePriorWitnessSha256===c16.witnessSha256&&
    l17.proofOnlyWIN8Before===5763&&l17.proofOnlyWIN8After===5795&&
    l17.updated.missing===45&&l17.newProofOnlyWIN8===32&&
    l17.newlySecuredConditionalEdges===4&&l17.winLossConflicts===0&&
    p17.eligibleUnprovedS9===116&&p17.undominatedS9===14&&
    p17.conditionalUnprovedEdges===45&&
    p17.newSelectionSha256===c18.sourcePlanSha256&&
    c18.sourcePriorWitnessSha256===c17.witnessSha256&&
    l18.proofOnlyWIN8Before===5795&&l18.verifiedWin9===1&&
    l18.verifiedLoss9===13&&l18.updated.missing<=45&&
    l18.winLossConflicts===0&&
    p10.emptyBoard==='UNKNOWN'&&p11.emptyBoard==='UNKNOWN'&&
    l11.emptyBoard==='UNKNOWN'&&l12.emptyBoard==='UNKNOWN',
    'frozen prior evidence mismatch');
  const parents9=closure(p8,c9,5,27,270);
  const parents10=closure(p9,c10,8,24,240);
  const parents11=closure(p10,c11,4,28,280);
  const parents12=closure(p11,c12,12,20,200);
  const parents13=closure(p12,c13,4,28,280);
  const parents14=closure(p13,c14,5,27,270);
  const parents15=closure(p14,c15,3,29,289);
  const parents16=closure(p15,c16,3,25,249);
  const parents17=closure(p16,c17,4,16,160);
  const parents18=closure(p17,c18,1,13,130);
  // A newly derived LOSS9 parent must never contradict a WIN9 proven in
  // another batch; same-batch checks alone are insufficient.
  const allWin9=new Set([...c9.win9Keys,...c10.win9Keys,
    ...c11.win9Keys,...c12.win9Keys,...c13.win9Keys,...c14.win9Keys,
    ...c15.win9Keys,...c16.win9Keys,...c17.win9Keys,...c18.win9Keys]);
  const allLoss9=new Set([...parents9,...parents10,...parents11,
    ...parents12,...parents13,...parents14,...parents15,...parents16,
    ...parents17,...parents18]);
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
  const after15=new Set([...after14,...g.reverse(c15.win9Keys)]);
  const after16=new Set([...after15,...g.reverse(c16.win9Keys)]);
  const after17=new Set([...after16,...g.reverse(c17.win9Keys)]);
  const after18=new Set([...after17,...g.reverse(c18.win9Keys)]);
  need(after9.size===5449&&after10.size===5513&&after11.size===5545&&
    after12.size===5643&&after13.size===l13.proofOnlyWIN8After&&
    after14.size===5715&&after15.size===5739&&after16.size===5763&&
    after17.size===5795&&after18.size===l18.proofOnlyWIN8After&&
    [...after18].every(h=>!s.loss.has(h))&&
    [...after17].every(h=>!s.loss.has(h))&&
    [...after16].every(h=>!s.loss.has(h))&&
    [...after15].every(h=>!s.loss.has(h))&&
    [...after14].every(h=>!s.loss.has(h))&&
    [...after13].every(h=>!s.loss.has(h))&&
    JSON.stringify(r7.coverage(s.plan,after10))===JSON.stringify(l10.updated)&&
    JSON.stringify(r7.coverage(s.plan,after11))===JSON.stringify(l11.updated)&&
    JSON.stringify(r7.coverage(s.plan,after12))===JSON.stringify(l12.updated)&&
    JSON.stringify(r7.coverage(s.plan,after13))===JSON.stringify(l13.updated)&&
    JSON.stringify(r7.coverage(s.plan,after14))===JSON.stringify(l14.updated)&&
    JSON.stringify(r7.coverage(s.plan,after15))===JSON.stringify(l15.updated)&&
    JSON.stringify(r7.coverage(s.plan,after16))===JSON.stringify(l16.updated)&&
    JSON.stringify(r7.coverage(s.plan,after17))===JSON.stringify(l17.updated)&&
    JSON.stringify(r7.coverage(s.plan,after18))===JSON.stringify(l18.updated),
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
  need(eligible14.length===269&&p14.newSelectedKeys.every(h=>
    eligible14.some(x=>x.h===h)),'269 candidate census mismatch');
  const selected15=new Set(p14.newSelectedKeys);
  need(selected15.size===32,'round15 selection count mismatch');
  const excludedByProof15=eligible14.filter(x=>
    selected15.has(x.h)||parents15.has(x.h));
  need(p14.newSelectedKeys.every(h=>excludedByProof15.some(x=>x.h===h)),
    'round15 selection exclusion incomplete');
  const remaining15=eligible14.filter(x=>
    !selected15.has(x.h)&&!parents15.has(x.h));
  const missing15=[...s.plan8].filter(h=>!after15.has(h)).sort();
  need(missing15.length===52,'round15 conditional frontier mismatch');
  const index15=new Map(missing15.map((h,i)=>[h,i]));
  const eligible15=remaining15.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index15.has(h))mask|=1n<<BigInt(index15.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  need(eligible15.length===215&&p15.newSelectedKeys.every(h=>
    eligible15.some(x=>x.h===h)),'215 candidate census mismatch');
  const selected16=new Set(p15.newSelectedKeys);
  need(selected16.size===28,'round16 selection count mismatch');
  const excludedByProof16=eligible15.filter(x=>
    selected16.has(x.h)||parents16.has(x.h));
  need(p15.newSelectedKeys.every(h=>excludedByProof16.some(x=>x.h===h)),
    'round16 selection exclusion incomplete');
  const remaining16=eligible15.filter(x=>
    !selected16.has(x.h)&&!parents16.has(x.h));
  const missing16=[...s.plan8].filter(h=>!after16.has(h)).sort();
  need(missing16.length===49,'round16 conditional frontier mismatch');
  const index16=new Map(missing16.map((h,i)=>[h,i]));
  const eligible16=remaining16.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index16.has(h))mask|=1n<<BigInt(index16.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  need(eligible16.length===158&&p16.newSelectedKeys.every(h=>
    eligible16.some(x=>x.h===h)),'158 candidate census mismatch');
  const selected17=new Set(p16.newSelectedKeys);
  need(selected17.size===20,'round17 selection count mismatch');
  const excludedByProof17=eligible16.filter(x=>
    selected17.has(x.h)||parents17.has(x.h));
  need(p16.newSelectedKeys.every(h=>excludedByProof17.some(x=>x.h===h)),
    'round17 selection exclusion incomplete');
  const remaining17=eligible16.filter(x=>
    !selected17.has(x.h)&&!parents17.has(x.h));
  const missing17=[...s.plan8].filter(h=>!after17.has(h)).sort();
  need(missing17.length===45,'round17 conditional frontier mismatch');
  const index17=new Map(missing17.map((h,i)=>[h,i]));
  const eligible17=remaining17.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index17.has(h))mask|=1n<<BigInt(index17.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  need(eligible17.length===116&&p17.newSelectedKeys.every(h=>
    eligible17.some(x=>x.h===h)),'116 candidate census mismatch');
  const selected18=new Set(p17.newSelectedKeys);
  need(selected18.size===14,'round18 selection count mismatch');
  const excludedByProof18=eligible17.filter(x=>
    selected18.has(x.h)||parents18.has(x.h));
  need(p17.newSelectedKeys.every(h=>excludedByProof18.some(x=>x.h)),
    'round18 selection exclusion incomplete');
  const remaining18=eligible17.filter(x=>
    !selected18.has(x.h)&&!parents18.has(x.h));
  const missing18=[...s.plan8].filter(h=>!after18.has(h)).sort();
  need(missing18.length===l18.updated.missing,
    'round18 conditional frontier mismatch');
  const index18=new Map(missing18.map((h,i)=>[h,i]));
  const eligible18=remaining18.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index18.has(h))mask|=1n<<BigInt(index18.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  need(eligible18.length>0,'no remaining eligible candidate');
  const reduced=planner.pruneDominated(eligible18);
  const baseline=planner.greedy(eligible18,32);
  const rg=planner.greedy(reduced,32);
  const optimized=planner.improve(reduced,better(rg,baseline)?rg:baseline);
  const chosen=optimized.picked;
  need(chosen.length>0&&chosen.length<=32&&
    new Set(chosen.map(x=>x.h)).size===chosen.length&&
    !better(baseline,chosen)&&
    chosen.every(x=>!selected18.has(x.h)&&!parents18.has(x.h)),
    'candidate selection invalid');
  const result={
    schema:'n11-post-round18-proof-only-replan-v1',emptyBoard:'UNKNOWN',
    sourceSelectionSha256:c18.selectionSha256,
    sourceWitnessSha256:c18.witnessSha256,
    independentlyVerifiedTerminalLeaves:checked.uniqueTerminalLeaves,
    terminalStatesPerGeometry:checked.terminalStatesPerGeometry,
    verifiedWin9:1,verifiedLoss9:13,
    derivedLoss9ParentClosure:parents18.size,
    proofOnlyWin8Before:after17.size,proofOnlyWin8After:after18.size,
    newProofOnlyWin8:after18.size-after17.size,
    conditionalUnprovedEdges:missing18.length,
    eligibleBeforeRound18:eligible17.length,
    excludedByRound18Proof:excludedByProof18.length,
    excludedSelectedRound18:selected18.size,
    excludedAdditionalLoss9Parents:excludedByProof18.length-selected18.size,
    remainingAfterProofExclusions:remaining18.length,
    noLongerTouchesUnprovedS8:remaining18.length-eligible18.length,
    eligibleUnprovedS9:eligible18.length,undominatedS9:reduced.length,
    baselinePotentialCoverage:count(baseline),potentialCoverage:count(chosen),
    legal10Children:cost(chosen),exchanges:optimized.swaps,
    selectedCount:chosen.length,newSelectedKeys:chosen.map(x=>x.h),
    newSelectionSha256:sha(chosen.map(x=>x.h).join('\n')+'\n'),
    winLossConflicts:0,newS7Verdicts:0,newS5Verdicts:0,newTwoStoneClosures:0
  };
  const frozen=path.join(__dirname,'next-plan.json');
  if(fs.existsSync(frozen))need(
    JSON.stringify(read('next-plan.json'))===JSON.stringify(result),
    'frozen round18 replan mismatch');

  // Preserve the exact round18 plan as an audited stepping stone.
  need(JSON.stringify(result)===JSON.stringify(p18),
    'round18 plan reconstruction mismatch');
  const oldConsole=console.log;let checked19;
  try{console.log=()=>{};checked19=verify19.verify({negative:true});}
  finally{console.log=oldConsole;}
  need(checked19.verified&&checked19.win9===2&&checked19.loss9===10&&
    checked19.emptyBoard==='UNKNOWN','round19 independent terminal audit failed');
  need(p18.newSelectionSha256===c19.sourcePlanSha256&&
    c19.sourcePriorWitnessSha256===c18.witnessSha256&&
    l19.verifiedWin9===2&&l19.verifiedLoss9===10&&
    l19.proofOnlyWIN8Before===5803&&l19.proofOnlyWIN8After===5819&&
    l19.newProofOnlyWIN8===16&&l19.updated.missing===42&&
    l19.newlySecuredConditionalEdges===2&&
    l19.winLossConflicts===0&&l19.newTwoStoneClosures===0,
    'round19 frozen lift mismatch');
  const parents19=closure(p18,c19,2,10,100);
  const allWin19=new Set([...allWin9,...c19.win9Keys]);
  const allLoss19=new Set([...allLoss9,...parents19]);
  need([...allWin19].every(h=>!allLoss19.has(h)),
    'cross-batch round19 WIN9/LOSS9 contradiction');
  const after19=new Set([...after18,...g.reverse(c19.win9Keys)]);
  need(after19.size===5819&&[...after19].every(h=>!s.loss.has(h))&&
    JSON.stringify(r7.coverage(s.plan,after19))===JSON.stringify(l19.updated),
    'round19 certified WIN8 coverage mismatch');
  const selected19=new Set(p18.newSelectedKeys);
  need(selected19.size===12&&selected19.size===p18.selectedCount&&
    [...selected19].every(h=>eligible18.some(x=>x.h===h)),
    'round19 selected candidate mismatch');
  const excludedByProof19=eligible18.filter(x=>
    selected19.has(x.h)||parents19.has(x.h));
  const remaining19=eligible18.filter(x=>
    !selected19.has(x.h)&&!parents19.has(x.h));
  const missing19=[...s.plan8].filter(h=>!after19.has(h)).sort();
  need(missing19.length===42,'round19 missing-edge count mismatch');
  const index19=new Map(missing19.map((h,i)=>[h,i]));
  const eligible19=remaining19.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index19.has(h))mask|=1n<<BigInt(index19.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  need(eligible19.length>0,'no eligible round20 candidate');
  const reduced19=planner.pruneDominated(eligible19);
  const baseline19=planner.greedy(eligible19,32);
  const rg19=planner.greedy(reduced19,32);
  const optimized19=planner.improve(reduced19,
    better(rg19,baseline19)?rg19:baseline19);
  const chosen19=optimized19.picked;
  need(chosen19.length>0&&chosen19.length<=32&&
    new Set(chosen19.map(x=>x.h)).size===chosen19.length&&
    !better(baseline19,chosen19)&&
    chosen19.every(x=>!selected19.has(x.h)&&!parents19.has(x.h)),
    'round20 candidate selection invalid');
  const result19={
    schema:'n11-post-round19-proof-only-replan-v1',emptyBoard:'UNKNOWN',
    sourceSelectionSha256:c19.selectionSha256,
    sourceWitnessSha256:c19.witnessSha256,
    independentlyVerifiedTerminalLeaves:checked19.uniqueTerminalLeaves,
    terminalStatesPerGeometry:checked19.terminalStatesPerGeometry,
    verifiedWin9:2,verifiedLoss9:10,
    derivedLoss9ParentClosure:parents19.size,
    proofOnlyWin8Before:after18.size,proofOnlyWin8After:after19.size,
    newProofOnlyWin8:after19.size-after18.size,
    conditionalUnprovedEdges:missing19.length,
    eligibleBeforeRound19:eligible18.length,
    excludedByRound19Proof:excludedByProof19.length,
    excludedSelectedRound19:selected19.size,
    excludedAdditionalLoss9Parents:excludedByProof19.length-selected19.size,
    remainingAfterProofExclusions:remaining19.length,
    noLongerTouchesUnprovedS8:remaining19.length-eligible19.length,
    eligibleUnprovedS9:eligible19.length,undominatedS9:reduced19.length,
    baselinePotentialCoverage:count(baseline19),
    potentialCoverage:count(chosen19),legal10Children:cost(chosen19),
    exchanges:optimized19.swaps,selectedCount:chosen19.length,
    newSelectedKeys:chosen19.map(x=>x.h),
    newSelectionSha256:sha(chosen19.map(x=>x.h).join('\n')+'\n'),
    winLossConflicts:0,newS7Verdicts:0,newS5Verdicts:0,newTwoStoneClosures:0
  };
  const frozen19=path.join(__dirname,'next-plan.json');
  if(fs.existsSync(frozen19))need(
    JSON.stringify(read('next-plan.json'))===JSON.stringify(result19),
    'frozen round19 replan mismatch');
  console.log(JSON.stringify(result19,null,2));return result19;
}
if(require.main===module)run();
module.exports={run};
