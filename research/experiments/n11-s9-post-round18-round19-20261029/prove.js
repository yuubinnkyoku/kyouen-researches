#!/usr/bin/env node
'use strict';
// Bounded round19 discovery for exactly 12 coordinator-selected S9 classes.
// WIN requires every legal S10 child; LOSS requires a verified S10 LOSS witness.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
function run(){
  const plan=read('../n11-s9-post-round18-replan-20261029/next-plan.json');
  const prior=read('../n11-s9-post-round17-round18-20261029/certificate.json');
  const preflight=read('../n11-s9-post-round18-replan-20261029/preflight.json');
  const keys=plan.newSelectedKeys;
  need(plan.schema==='n11-post-round18-proof-only-replan-v1'&&
    plan.emptyBoard==='UNKNOWN'&&plan.conditionalUnprovedEdges===44&&
    plan.proofOnlyWin8After===5803&&plan.eligibleUnprovedS9===93&&
    plan.undominatedS9===12&&plan.legal10Children===329&&
    plan.selectedCount===12&&plan.potentialCoverage===12&&
    plan.sourceSelectionSha256===prior.selectionSha256&&
    plan.sourceWitnessSha256===prior.witnessSha256&&
    prior.win9===1&&prior.loss9===13&&
    keys.length===12&&new Set(keys).size===12&&
    sha(keys.join('\n')+'\n')===plan.newSelectionSha256,
    'frozen upstream selection/certificate mismatch');
  need(preflight.schema==='n11-post-round18-independent-boundary-preflight-v1'&&
    preflight.emptyBoard==='UNKNOWN'&&
    preflight.selectionSha256===plan.newSelectionSha256&&
    preflight.roots===12&&preflight.legalS10Edges===329&&
    preflight.distinctS10Classes===329&&
    preflight.repeatedS10Classes===0&&
    preflight.crossRootSavings===0,
    'frozen independent S10 preflight mismatch');
  const leaves=new Map(),claims=[],wins=[],lossLeaves=[];
  let states=0,obligations=0,winEdges=0,childEdges=0;
  function terminal(h){
    if(leaves.has(h))return leaves.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.legal===b.legal&&a.states===b.states,
      'independent S10 terminal mismatch '+h);
    leaves.set(h,a);states+=a.states;return a;
  }
  for(const h of keys){
    const kids=g.children(g.board(h,9)),other=ind.children4(h);
    need(same(kids,other),'S9 child geometry mismatch '+h);
    const ordered=[...kids].sort();childEdges+=ordered.length;
    let witness=255;
    for(let i=0;i<ordered.length;i++){
      obligations++;
      if(!terminal(ordered[i]).win){witness=i;break;}
    }
    claims.push(witness);
    if(witness===255){
      wins.push(h);winEdges+=ordered.length;
      for(const par of g.reverse([h]))need(
        g.children(g.board(par,8)).has(h)&&ind.children4(par).has(h),
        'WIN9 reverse incidence mismatch '+h);
    }else lossLeaves.push(ordered[witness]);
  }
  need(childEdges===329,'frozen S10 child cost mismatch');
  const parents=new Set();
  for(const leaf of lossLeaves){
    const b=BigInt('0x'+leaf);
    for(const pt of g.pts(b)){
      const par=g.key(g.canonical(b^(1n<<BigInt(pt))));
      need(g.children(g.board(par,9)).has(leaf)&&
        ind.children4(par).has(leaf),
        'LOSS10 reverse incidence mismatch '+par);
      parents.add(par);
    }
  }
  need(wins.every(h=>!parents.has(h)),'WIN9/LOSS9 contradiction');
  const bytes=Buffer.from(claims);
  const result={
    format:'n11-s9-post-round18-round19-terminal-v1',
    board:11,perspective:'original-first-player',emptyBoard:'UNKNOWN',
    sourcePlanSha256:plan.newSelectionSha256,
    sourcePriorWitnessSha256:prior.witnessSha256,
    selectionSha256:sha(keys.join('\n')+'\n'),
    witnessBase64:bytes.toString('base64'),witnessSha256:sha(bytes),
    win9:wins.length,loss9:keys.length-wins.length,win9Keys:wins,
    orderedS10Children:childEdges,win10Edges:winEdges,
    firstLossSearchObligations:obligations,
    uniqueTerminalLeaves:leaves.size,terminalStatesPerGeometry:states,
    loss9ParentClosure:parents.size,
    loss9ParentSha256:sha([...parents].sort().join('\n')+'\n'),
    newTwoStoneClosures:0
  };
  const fixed=path.join(__dirname,'certificate.json');
  if(fs.existsSync(fixed))need(
    JSON.stringify(read('certificate.json'))===JSON.stringify(result),
    'frozen certificate replay mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
