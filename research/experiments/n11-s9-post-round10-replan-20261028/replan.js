#!/usr/bin/env node
'use strict';
// Proof-only replan after round10. Never treat potential incidence as a verdict.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const verify10=require('../n11-s9-post-round9-round10-20261028/verify_compact.js');
const planner=require('../n11-s9-n24-round2-20261028/plan_next.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const union=a=>a.reduce((m,x)=>m|x.mask,0n);
const count=a=>planner.popcount(union(a));
const cost=a=>a.reduce((n,x)=>n+x.children,0);
const better=(a,b)=>count(a)>count(b)||(count(a)===count(b)&&cost(a)<cost(b));
function run(){
  // Replay the round10 certificate with independent terminal solvers.
  // Round9 was separately certified; reconstruct its census below.
  const log=console.log;let checked;
  try{console.log=()=>{};checked=verify10.verify({negative:true});}
  finally{console.log=log;}
  need(checked.verified&&checked.win9===8&&checked.loss9===24&&
    checked.emptyBoard==='UNKNOWN','round10 terminal audit failed');
  const inv=r7.inventory(),{s,secured}=inv;
  const p8=read('../n11-s9-post-s10-reuse-round8-20261028/next-plan.json');
  const p9=read('../n11-s9-post-round9-replan-20261028/next-plan.json');
  const c9=read('../n11-s9-post-round8-round9-20261028/certificate.json');
  const c10=read('../n11-s9-post-round9-round10-20261028/certificate.json');
  const lift=read('../n11-s9-post-round9-round10-20261028/lift.json');
  const oldLoss=read('../n11-s10-cross-batch-reuse-20261028/derived-loss9.json');
  need(p9.eligibleUnprovedS9===890&&p9.conditionalUnprovedEdges===93&&
    p9.newSelectionSha256===c10.sourcePlanSha256&&
    c10.selectionSha256===c10.sourcePlanSha256&&
    c10.sourcePriorWitnessSha256===c9.witnessSha256&&
    c10.emptyBoard==='UNKNOWN'&&lift.emptyBoard==='UNKNOWN'&&
    lift.proofOnlyWIN8After===5513&&lift.updated.missing===83,
    'round10 source or fixed lift mismatch');
  const keys10=p9.newSelectedKeys,claims=Buffer.from(c10.witnessBase64,'base64');
  need(keys10.length===32&&claims.length===32&&
    sha(keys10.join('\n')+'\n')===c10.selectionSha256&&
    sha(claims)===c10.witnessSha256,'round10 selection or witness hash mismatch');
  const win10=[],parents10=new Set(),loss10=[];
  for(let i=0;i<32;i++){
    const h=keys10[i],kids=g.children(g.board(h,9));
    need(same(kids,ind.children4(h)),'independent S9 boundary mismatch '+h);
    const ordered=[...kids].sort(),w=claims[i];
    if(w===255){win10.push(h);continue;}
    need(w<ordered.length,'invalid LOSS9 witness index '+h);
    const leaf=ordered[w];loss10.push(h);
    const b=BigInt('0x'+leaf);
    for(const pt of g.pts(b)){
      const par=g.key(g.canonical(b^(1n<<BigInt(pt))));
      need(g.children(g.board(par,9)).has(leaf)&&
        ind.children4(par).has(leaf),'invalid LOSS10 parent '+par);
      parents10.add(par);
    }
  }
  need(win10.length===8&&loss10.length===24&&
    JSON.stringify(win10)===JSON.stringify(c10.win9Keys)&&
    parents10.size===240&&parents10.size===c10.loss9ParentClosure&&
    sha([...parents10].sort().join('\n')+'\n')===c10.loss9ParentSha256&&
    win10.every(h=>!parents10.has(h)),
    'round10 LOSS parent closure or WIN/LOSS conflict');
  const after9=new Set([...secured,...g.reverse(c9.win9Keys)]);
  const after10=new Set([...after9,...g.reverse(win10)]);
  need(after9.size===5449&&after10.size===5513&&
    [...after10].every(h=>!s.loss.has(h))&&
    JSON.stringify(r7.coverage(s.plan,after10))===JSON.stringify(lift.updated),
    'proof-only WIN8 frontier mismatch');
  const used7=new Set(inv.selected.map(x=>x.h));
  const priorLoss=new Set(oldLoss.map(x=>x.h));
  const excluded8=new Set(p8.excludedKeys);
  const before9=inv.options.filter(x=>!used7.has(x.h)&&
    !priorLoss.has(x.h)&&!excluded8.has(x.h));
  need(before9.length===1011,'old 1011-candidate census changed');
  const chosen9=new Set(p8.newSelectedKeys);
  const parents9=new Set();
  const claims9=Buffer.from(c9.witnessBase64,'base64');
  need(claims9.length===32&&sha(claims9)===c9.witnessSha256,
    'round9 witness hash mismatch');
  for(let i=0;i<32;i++){
    if(claims9[i]===255)continue;
    const ordered=[...g.children(g.board(p8.newSelectedKeys[i],9))].sort();
    need(claims9[i]<ordered.length,'round9 LOSS witness out of range');
    const b=BigInt('0x'+ordered[claims9[i]]);
    for(const pt of g.pts(b))parents9.add(
      g.key(g.canonical(b^(1n<<BigInt(pt)))));
  }
  need(parents9.size===270&&
    sha([...parents9].sort().join('\n')+'\n')===c9.loss9ParentSha256,
    'round9 parent closure mismatch');
  const missing9=new Set([...s.plan8].filter(h=>!after9.has(h)));
  const eligible9=before9.filter(x=>!chosen9.has(x.h)&&
    !parents9.has(x.h)&&x.hits.some(h=>missing9.has(h)));
  need(eligible9.length===890&&
    keys10.every(h=>eligible9.some(x=>x.h===h)),
    'round9 890-candidate inventory mismatch');
  const selected10=new Set(keys10);
  const excludedByProof=eligible9.filter(x=>
    selected10.has(x.h)||parents10.has(x.h));
  need(keys10.every(h=>excludedByProof.some(x=>x.h===h)),
    'round10 selection exclusion incomplete');
  const remaining=eligible9.filter(x=>
    !selected10.has(x.h)&&!parents10.has(x.h));
  const missing=[...s.plan8].filter(h=>!after10.has(h)).sort();
  need(missing.length===83,'83-edge frontier changed');
  const index=new Map(missing.map((h,i)=>[h,i]));
  const eligible=remaining.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index.has(h))mask|=1n<<BigInt(index.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  const reduced=planner.pruneDominated(eligible);
  const baseline=planner.greedy(eligible,32);
  const redGreedy=planner.greedy(reduced,32);
  const opt=planner.improve(reduced,better(redGreedy,baseline)?redGreedy:baseline);
  const chosen=opt.picked;
  need(chosen.length===32&&new Set(chosen.map(x=>x.h)).size===32&&
    !better(baseline,chosen)&&chosen.every(x=>
      !selected10.has(x.h)&&!parents10.has(x.h)),
    'next candidate plan invalid');
  const result={
    schema:'n11-post-round10-proof-only-replan-v1',emptyBoard:'UNKNOWN',
    sourceSelectionSha256:c10.selectionSha256,
    sourceWitnessSha256:c10.witnessSha256,
    verifiedWin9:win10.length,verifiedLoss9:loss10.length,
    independentlyVerifiedTerminalLeaves:checked.uniqueTerminalLeaves,
    terminalStatesPerGeometry:checked.terminalStatesPerGeometry,
    derivedLoss9ParentClosure:parents10.size,
    proofOnlyWin8Before:after9.size,proofOnlyWin8After:after10.size,
    newProofOnlyWin8:after10.size-after9.size,
    conditionalUnprovedEdges:missing.length,
    eligibleBeforeRound10:eligible9.length,
    excludedByRound10Proof:excludedByProof.length,
    excludedSelectedRound10:keys10.length,
    excludedAdditionalLoss9Parents:excludedByProof.length-keys10.length,
    remainingAfterProofExclusions:remaining.length,
    noLongerTouchesUnprovedS8:remaining.length-eligible.length,
    eligibleUnprovedS9:eligible.length,undominatedS9:reduced.length,
    baselinePotentialCoverage:count(baseline),potentialCoverage:count(chosen),
    legal10Children:cost(chosen),exchanges:opt.swaps,
    newSelectedKeys:chosen.map(x=>x.h),
    newSelectionSha256:sha(chosen.map(x=>x.h).join('\n')+'\n'),
    winLossConflicts:0,newS7Verdicts:0,newS5Verdicts:0,newTwoStoneClosures:0
  };
  const fixed=path.join(__dirname,'next-plan.json');
  if(fs.existsSync(fixed))need(
    JSON.stringify(JSON.parse(fs.readFileSync(fixed,'utf8')))===
      JSON.stringify(result),'frozen round10 replan mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
