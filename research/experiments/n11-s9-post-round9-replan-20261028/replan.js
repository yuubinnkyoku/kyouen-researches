#!/usr/bin/env node
'use strict';
// All round9 claims are independently checked before planning. Potential hits are not proofs.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const planner=require('../n11-s9-n24-round2-20261028/plan_next.js');
const need=(v,m)=>{if(!v)throw Error(m)};
const sha=v=>crypto.createHash('sha256').update(v).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const count=a=>planner.popcount(a.reduce((v,x)=>v|x.mask,0n));
const cost=a=>a.reduce((v,x)=>v+x.children,0);
const better=(a,b)=>count(a)>count(b)||(count(a)===count(b)&&cost(a)<cost(b));
function run(){
  const inv=r7.inventory(),{s,secured}=inv;
  need(inv.missing.length===100&&secured.size===5407&&inv.options.length===1478,
    'upstream proof-only inventory changed');
  const p8=read('../n11-s9-post-s10-reuse-round8-20261028/next-plan.json');
  const cert=read('../n11-s9-post-round8-round9-20261028/certificate.json');
  const oldLoss=read('../n11-s10-cross-batch-reuse-20261028/derived-loss9.json');
  const keys=p8.newSelectedKeys,claims=Buffer.from(cert.witnessBase64,'base64');
  need(p8.schema==='n11-post-reuse-round8-replan-v1'&&p8.remainingEligible===1011&&
    p8.conditionalUnprovedEdges===100&&p8.emptyBoard==='UNKNOWN'&&
    keys.length===32&&new Set(keys).size===32&&claims.length===32&&
    sha(keys.join('\n')+'\n')===p8.newSelectionSha256&&
    cert.format==='n11-s9-post-round8-round9-terminal-v1'&&
    cert.emptyBoard==='UNKNOWN'&&cert.perspective==='original-first-player'&&
    cert.selectionSha256===p8.newSelectionSha256&&
    cert.sourcePlanSha256===p8.newSelectionSha256&&
    sha(claims)===cert.witnessSha256,'round9 frozen certificate identity mismatch');
  const wins=[],losses=[],parents=new Set(),leaves=new Map();
  let states=0,winEdges=0;
  function terminal(h){
    if(leaves.has(h))return leaves.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.legal===b.legal&&a.states===b.states,
      '3x3/4x4 terminal disagreement '+h);
    leaves.set(h,a);states+=a.states;return a;
  }
  for(let i=0;i<32;i++){
    const h=keys[i],children=g.children(g.board(h,9));
    need(same(children,ind.children4(h)),'S9 boundary disagreement '+h);
    const ordered=[...children].sort(),w=claims[i];
    if(w===255){
      for(const child of ordered)need(terminal(child).win,'false WIN9 '+h);
      wins.push(h);winEdges+=ordered.length;
    }else{
      need(w<ordered.length,'invalid LOSS9 witness index '+h);
      const leaf=ordered[w];need(!terminal(leaf).win,'false LOSS9 '+h);
      losses.push(h);
      const b=BigInt('0x'+leaf);
      for(const pt of g.pts(b)){
        const parent=g.key(g.canonical(b^(1n<<BigInt(pt))));
        need(g.children(g.board(parent,9)).has(leaf)&&
          ind.children4(parent).has(leaf),'invalid LOSS9 parent '+parent);
        parents.add(parent);
      }
    }
  }
  need(wins.length===5&&losses.length===27&&
    JSON.stringify(wins)===JSON.stringify(cert.win9Keys)&&
    winEdges===cert.win10Edges&&parents.size===cert.loss9ParentClosure&&
    sha([...parents].sort().join('\n')+'\n')===cert.loss9ParentSha256&&
    wins.every(h=>!parents.has(h)),'frozen round9 terminal proof mismatch');
  const derived=g.reverse(wins);
  need([...derived].every(h=>!s.loss.has(h)),'WIN8/LOSS8 conflict');
  const after=new Set([...secured,...derived]),coverage=r7.coverage(s.plan,after);
  need(after.size===5449&&after.size-secured.size===42&&
    coverage.total===548&&coverage.missing===93&&
    JSON.stringify(coverage)===JSON.stringify(cert.updated),
    '93-edge proof-only frontier mismatch');
  const used7=new Set(inv.selected.map(x=>x.h));
  const priorLoss=new Set(oldLoss.map(x=>x.h)),excluded8=new Set(p8.excludedKeys);
  need(priorLoss.size===383&&excluded8.size===52,'old LOSS9 closure changed');
  const prior=inv.options.filter(x=>!used7.has(x.h)&&
    !priorLoss.has(x.h)&&!excluded8.has(x.h));
  need(prior.length===1011,'prior eligible census mismatch');
  const selected9=new Set(keys);
  const proofExcluded=prior.filter(x=>selected9.has(x.h)||parents.has(x.h));
  need(keys.every(h=>proofExcluded.some(x=>x.h===h)),'round9 exclusion incomplete');
  const remaining=prior.filter(x=>!selected9.has(x.h)&&!parents.has(x.h));
  const missing=[...s.plan8].filter(h=>!after.has(h)).sort();
  need(missing.length===93,'unproved S8 class count mismatch');
  const index=new Map(missing.map((h,i)=>[h,i]));
  const eligible=remaining.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index.has(h))mask|=1n<<BigInt(index.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  const reduced=planner.pruneDominated(eligible);
  const baseline=planner.greedy(eligible,32),redGreedy=planner.greedy(reduced,32);
  const start=better(redGreedy,baseline)?redGreedy:baseline;
  const opt=planner.improve(reduced,start),chosen=opt.picked;
  need(chosen.length===32&&new Set(chosen.map(x=>x.h)).size===32&&
    !better(baseline,chosen)&&chosen.every(x=>
      !selected9.has(x.h)&&!parents.has(x.h)&&!priorLoss.has(x.h)&&
      !excluded8.has(x.h)&&!used7.has(x.h)),'invalid next candidate selection');
  const result={
    schema:'n11-post-round9-proof-only-replan-v1',emptyBoard:'UNKNOWN',
    sourceSelectionSha256:cert.selectionSha256,sourceWitnessSha256:cert.witnessSha256,
    verifiedWin9:wins.length,verifiedLoss9:losses.length,
    independentlyVerifiedTerminalLeaves:leaves.size,
    terminalStatesPerGeometry:states,derivedLoss9ParentClosure:parents.size,
    proofOnlyWin8Before:secured.size,proofOnlyWin8After:after.size,
    newProofOnlyWin8:after.size-secured.size,conditionalUnprovedEdges:coverage.missing,
    eligibleBeforeRound9:prior.length,excludedByRound9Proof:proofExcluded.length,
    excludedSelectedRound9:keys.length,
    excludedAdditionalLoss9Parents:proofExcluded.length-keys.length,
    remainingAfterProofExclusions:remaining.length,
    noLongerTouchesUnprovedS8:remaining.length-eligible.length,
    eligibleUnprovedS9:eligible.length,undominatedS9:reduced.length,
    baselinePotentialCoverage:count(baseline),potentialCoverage:count(chosen),
    legal10Children:cost(chosen),exchanges:opt.swaps,
    newSelectedKeys:chosen.map(x=>x.h),
    newSelectionSha256:sha(chosen.map(x=>x.h).join('\n')+'\n'),
    winLossConflicts:0,newS7Verdicts:0,newS5Verdicts:0,newTwoStoneClosures:0
  };
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
