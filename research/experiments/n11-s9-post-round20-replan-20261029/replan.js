#!/usr/bin/env node
'use strict';
// Replan the conditional N11 fourteen-root S8 frontier after round20.
// Only independently verified certificates count as proven coverage.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const planner=require('../n11-s9-n24-round2-20261028/plan_next.js');
const previous=require('../n11-s9-post-round19-replan-20261029/replan.js');
const verify20=require('../n11-s9-post-round19-round20-20261029/verify_compact.js');
const lift20=require('../n11-s9-post-round19-round20-20261029/lift.js');
const need=(v,m)=>{if(!v)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const pop=rows=>planner.popcount(rows.reduce((m,x)=>m|x.mask,0n));
const cost=rows=>rows.reduce((n,x)=>n+x.children,0);
const better=(a,b)=>pop(a)>pop(b)||(pop(a)===pop(b)&&cost(a)<cost(b));
const planDirs=[
  'n11-s9-post-s10-reuse-round8-20261028',
  ...Array.from({length:11},(_,i)=>{
    const n=i+9,day=n<=11?'20261028':'20261029';
    return 'n11-s9-post-round'+n+'-replan-'+day;
  })
];
const certDirs=[
  'n11-s9-post-round8-round9-20261028',
  ...Array.from({length:11},(_,i)=>{
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
  let checkedPrior,checked20,lift;
  const saved=console.log;
  try{
    console.log=()=>{};
    checkedPrior=previous.run();
    checked20=verify20.verify({negative:true});
    lift=lift20.run();
  }finally{console.log=saved;}
  const p19=read('../n11-s9-post-round19-replan-20261029/next-plan.json');
  need(JSON.stringify(checkedPrior)===JSON.stringify(p19)&&
    checked20.verified&&checked20.win9===1&&checked20.loss9===8&&
    checked20.emptyBoard==='UNKNOWN'&&
    lift.proofOnlyWIN8Before===5819&&lift.proofOnlyWIN8After===5827&&
    lift.updated.missing===41&&lift.newlySecuredConditionalEdges===1&&
    lift.winLossConflicts===0&&lift.newTwoStoneClosures===0,
    'round19/20 proof chain mismatch');
  const plans=planDirs.map(d=>read('../'+d+'/next-plan.json'));
  const certs=certDirs.map(d=>read('../'+d+'/certificate.json'));
  need(plans.length===12&&certs.length===12&&
    plans[11].newSelectionSha256===p19.newSelectionSha256&&
    certs[11].witnessSha256===
      read('../n11-s9-post-round19-round20-20261029/certificate.json').witnessSha256,
    'round20 chain input mismatch');
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
  let after19=new Set(secured);
  for(let i=0;i<11;i++)for(const h of g.reverse(certs[i].win9Keys))after19.add(h);
  const after20=new Set([...after19,...g.reverse(certs[11].win9Keys)]);
  need(after19.size===5819&&after20.size===5827&&
    [...after20].every(h=>!s.loss.has(h))&&
    JSON.stringify(r7.coverage(s.plan,after20))===JSON.stringify(lift.updated),
    'WIN8 frontier mismatch');
  const p8=plans[0];
  const oldLoss=read('../n11-s10-cross-batch-reuse-20261028/derived-loss9.json');
  const priorExcluded=new Set([...p8.excludedKeys,...oldLoss.map(x=>x.h)]);
  const used7=new Set(inv.selected.map(x=>x.h));
  const selectedBefore20=new Set(plans.slice(0,11).flatMap(p=>p.newSelectedKeys));
  const lossBefore20=new Set(parents.slice(0,11).flatMap(p=>[...p]));
  const missing19=new Set([...s.plan8].filter(h=>!after19.has(h)));
  const eligible19=inv.options.filter(x=>!used7.has(x.h)&&
    !priorExcluded.has(x.h)&&!selectedBefore20.has(x.h)&&
    !lossBefore20.has(x.h)&&x.hits.some(h=>missing19.has(h)));
  need(eligible19.length===64&&p19.selectedCount===9&&
    p19.newSelectedKeys.every(h=>eligible19.some(x=>x.h===h)),
    'round19 candidate census mismatch');
  const selected20=new Set(p19.newSelectedKeys),parents20=parents[11];
  const excludedByProof=eligible19.filter(x=>
    selected20.has(x.h)||parents20.has(x.h));
  need([...selected20].every(h=>excludedByProof.some(x=>x.h===h)),
    'round20 selected candidates not excluded');
  const remaining=eligible19.filter(x=>
    !selected20.has(x.h)&&!parents20.has(x.h));
  const missing20=[...s.plan8].filter(h=>!after20.has(h)).sort();
  need(missing20.length===41,'round20 missing edge mismatch');
  const index=new Map(missing20.map((h,i)=>[h,i]));
  const eligible=remaining.map(x=>{
    let mask=0n;
    for(const h of x.hits)if(index.has(h))mask|=1n<<BigInt(index.get(h));
    return {...x,mask};
  }).filter(x=>x.mask!==0n);
  need(eligible.length>0,'no eligible round21 candidate');
  const reduced=planner.pruneDominated(eligible);
  const baseline=planner.greedy(eligible,32);
  const rg=planner.greedy(reduced,32);
  const optimized=planner.improve(reduced,better(rg,baseline)?rg:baseline);
  const chosen=optimized.picked;
  need(chosen.length>0&&chosen.length<=32&&
    new Set(chosen.map(x=>x.h)).size===chosen.length&&
    !better(baseline,chosen)&&
    chosen.every(x=>!selected20.has(x.h)&&!parents20.has(x.h)),
    'round21 candidate selection invalid');
  const cert20=certs[11];
  const result={
    schema:'n11-post-round20-proof-only-replan-v1',emptyBoard:'UNKNOWN',
    sourceSelectionSha256:cert20.selectionSha256,
    sourceWitnessSha256:cert20.witnessSha256,
    independentlyVerifiedTerminalLeaves:checked20.uniqueTerminalLeaves,
    terminalStatesPerGeometry:checked20.terminalStatesPerGeometry,
    verifiedWin9:cert20.win9,verifiedLoss9:cert20.loss9,
    derivedLoss9ParentClosure:parents20.size,
    proofOnlyWin8Before:after19.size,proofOnlyWin8After:after20.size,
    newProofOnlyWin8:after20.size-after19.size,
    conditionalUnprovedEdges:missing20.length,
    eligibleBeforeRound20:eligible19.length,
    excludedByRound20Proof:excludedByProof.length,
    excludedSelectedRound20:selected20.size,
    excludedAdditionalLoss9Parents:excludedByProof.length-selected20.size,
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
    'frozen round20 replan mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
