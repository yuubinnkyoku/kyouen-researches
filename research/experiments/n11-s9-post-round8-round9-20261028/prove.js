#!/usr/bin/env node
'use strict';
// Fixed 32-class S9 terminal experiment after certified round8 exclusions.
// Every verdict is recomputed to terminal with two independent integer geometries.
// No incomplete search statistic is treated as a winner.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const dir=__dirname;
function run({negative=false}={}){
  const plan=JSON.parse(fs.readFileSync(path.join(dir,
    '../n11-s9-post-s10-reuse-round8-20261028/next-plan.json'),'utf8'));
  const keys=plan.newSelectedKeys;
  need(plan.schema==='n11-post-reuse-round8-replan-v1'&&
    plan.emptyBoard==='UNKNOWN'&&plan.remainingEligible===1011&&
    plan.undominated===156&&plan.conditionalUnprovedEdges===100&&
    keys.length===32&&new Set(keys).size===32&&
    sha(keys.join('\n')+'\n')===plan.newSelectionSha256,
    'upstream frozen round8 replan identity changed');
  const inv=r7.inventory(),{s,secured}=inv;
  need(inv.missing.length===100&&secured.size===5407&&
    keys.every(h=>inv.options.some(x=>x.h===h))&&
    keys.every(h=>!plan.excludedKeys.includes(h)),
    'round9 candidates not in certified S8 frontier');
  const leafCache=new Map(),claims=[],wins=[],lossLeaves=[];
  let states=0,obligations=0,winEdges=0;
  function terminal(h){
    if(leafCache.has(h))return leafCache.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.legal===b.legal&&a.states===b.states,
      '3x3/4x4 terminal mismatch '+h);
    leafCache.set(h,a);states+=a.states;return a;
  }
  function claim(h,index){
    const kids=g.children(g.board(h,9)),other=ind.children4(h);
    need(same(kids,other),'independent S9 boundary mismatch '+h);
    const ordered=[...kids].sort();
    if(index===255){
      for(const child of ordered)need(terminal(child).win,
        'forged WIN9 universal child '+h);
    }else{
      need(Number.isInteger(index)&&index>=0&&index<ordered.length,
        'out-of-range LOSS9 witness');
      need(!terminal(ordered[index]).win,'forged LOSS9 witness '+h);
    }
    return ordered;
  }
  for(const h of keys){
    const kids=[...g.children(g.board(h,9))].sort();
    need(same(new Set(kids),ind.children4(h)),'child geometry disagreement '+h);
    let witness=255;
    for(let i=0;i<kids.length;i++){
      obligations++;
      if(!terminal(kids[i]).win){witness=i;break;}
    }
    const ordered=claim(h,witness);
    claims.push(witness);
    if(witness===255){
      wins.push(h);winEdges+=ordered.length;
      for(const parent of g.reverse([h]))need(
        g.children(g.board(parent,8)).has(h)&&ind.children4(parent).has(h),
        'reverse WIN8 incidence mismatch '+h);
    }else lossLeaves.push(ordered[witness]);
  }
  const derived=g.reverse(wins);
  need([...derived].every(h=>!s.loss.has(h)),
    'WIN8/LOSS8 conflict');
  const after=new Set([...secured,...derived]);
  const previous=r7.coverage(s.plan,secured),updated=r7.coverage(s.plan,after);
  need(previous.total===548&&previous.missing===100&&
    updated.missing<=100,'conditional fourteen-root regression');
  const parents=new Set();
  for(const leaf of lossLeaves){
    const b=BigInt('0x'+leaf);
    for(const pt of g.pts(b)){
      const parent=g.key(g.canonical(b^(1n<<BigInt(pt))));
      need(g.children(g.board(parent,9)).has(leaf)&&
        ind.children4(parent).has(leaf),
        'invalid certified LOSS10 parent '+parent);
      parents.add(parent);
    }
  }
  need(wins.every(h=>!parents.has(h)),
    'WIN9/LOSS9 parent contradiction');
  const bytes=Buffer.from(claims);
  const result={
    format:'n11-s9-post-round8-round9-terminal-v1',
    board:11,perspective:'original-first-player',emptyBoard:'UNKNOWN',
    sourcePlanSha256:plan.newSelectionSha256,
    selectionSha256:sha(keys.join('\n')+'\n'),
    witnessBase64:bytes.toString('base64'),witnessSha256:sha(bytes),
    win9:wins.length,loss9:keys.length-wins.length,
    win9Keys:wins,win10Edges:winEdges,
    firstLossSearchObligations:obligations,
    uniqueTerminalLeaves:leafCache.size,terminalStatesPerGeometry:states,
    derivedWin8:derived.size,newProofOnlyWin8:after.size-secured.size,
    proofOnlyWin8Before:secured.size,proofOnlyWin8After:after.size,
    previous,updated,
    loss9ParentClosure:parents.size,
    loss9ParentSha256:sha([...parents].sort().join('\n')+'\n'),
    winLossConflicts:0,newS7Verdicts:0,newS5Verdicts:0,
    twoStoneClosures:0
  };
  const frozenPath=path.join(dir,'certificate.json');
  if(fs.existsSync(frozenPath)){
    const frozen=JSON.parse(fs.readFileSync(frozenPath,'utf8'));
    need(JSON.stringify(result)===JSON.stringify(frozen),
      'replay differs from frozen terminal certificate');
  }
  if(negative){
    const wi=claims.indexOf(255),li=claims.findIndex(x=>x!==255);
    if(wi>=0){
      let rejected=false;try{claim(keys[wi],0)}catch(_){rejected=true}
      need(rejected,'false LOSS9 claim accepted');
    }
    if(li>=0){
      let rejected=false;try{claim(keys[li],255)}catch(_){rejected=true}
      need(rejected,'false WIN9 claim accepted');
    }
    let rejected=false;try{claim(keys[0],254)}catch(_){rejected=true}
    need(rejected,'out-of-range claim accepted');
  }
  if(process.env.N11_ROUND9_OUTPUT)fs.writeFileSync(process.env.N11_ROUND9_OUTPUT,
    JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run({negative:process.argv.includes('--negative')});
module.exports={run};
