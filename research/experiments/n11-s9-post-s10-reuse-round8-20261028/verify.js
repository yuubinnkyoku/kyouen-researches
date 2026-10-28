#!/usr/bin/env node
'use strict';
// Exact, independently cross-checked S10 terminal proof; original-first viewpoint.
// The 32 S9 roots are LOSS. This is not an S8 or empty-board verdict.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const plan=JSON.parse(fs.readFileSync(path.join(__dirname,
  '../n11-s10-cross-batch-reuse-20261028/plan.json'),'utf8'));
const cert=JSON.parse(fs.readFileSync(path.join(__dirname,'certificate.json'),'utf8'));
function run({full=false,negative=false}={}){
  const keys=plan.selectedKeys;
  const claims=Buffer.from(cert.witnessBase64,'base64');
  need(cert.format==='n11-s9-post-s10-reuse-round8-terminal-v1'&&
    cert.board===11&&cert.perspective==='original-first-player'&&
    cert.emptyBoard==='UNKNOWN'&&plan.emptyBoard!=='WIN'&&
    plan.emptyBoard!=='LOSS','invalid scope');
  need(keys.length===32&&new Set(keys).size===32&&claims.length===32&&
    sha(keys.join('\n')+'\n')===cert.selectionSha256&&
    cert.selectionSha256===plan.selectionSha256&&
    sha(claims)===cert.witnessSha256,'selection/witness identity changed');
  const verdicts=new Map(),parents=new Set();
  let states=0,obligations=0;
  function terminal(h){
    if(verdicts.has(h))return verdicts.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.legal===b.legal&&a.states===b.states,
      '3x3/4x4 terminal disagreement '+h);
    verdicts.set(h,a);states+=a.states;return a;
  }
  function claim(row,index){
    const b=g.board(row,9),kids=g.children(b),other=ind.children4(row);
    need(same(kids,other),'3x3/4x4 S9 boundary mismatch '+row);
    const ordered=[...kids].sort();
    need(Number.isInteger(index)&&index>=0&&index<ordered.length,
      'out-of-range LOSS9 witness');
    if(full){
      for(let j=0;j<index;j++){
        obligations++;
        need(terminal(ordered[j]).win,'earlier LOSS10 invalidates first-loss order');
      }
    }
    obligations++;
    const leaf=ordered[index];
    need(!terminal(leaf).win,'false LOSS9 witness '+row);
    return leaf;
  }
  const selected=new Set(keys);
  for(let i=0;i<keys.length;i++){
    const leaf=claim(keys[i],claims[i]);
    const b=BigInt('0x'+leaf);
    for(const p of g.pts(b)){
      const parent=g.key(g.canonical(b^(1n<<BigInt(p))));
      const pb=g.board(parent,9);
      need(g.children(pb).has(leaf)&&ind.children4(parent).has(leaf),
        'invalid S9->LOSS10 parent incidence '+parent);
      parents.add(parent);
    }
  }
  need([...selected].every(x=>parents.has(x))&&
    parents.size===cert.derivedLoss9ParentClosure&&
    sha([...parents].sort().join('\n')+'\n')===cert.derivedLoss9ParentSha256,
    'LOSS9 parent closure mismatch');
  need(cert.win9===0&&cert.loss9===32&&cert.newProofOnlyWin8===0&&
    cert.conditionalUnprovedEdges===100&&cert.twoStoneClosures===0,
    'false upper-layer claim');
  if(full){
    const wins=[...verdicts.values()].filter(x=>x.win).length;
    need(obligations===cert.firstLossSearchObligations&&
      verdicts.size===cert.uniqueTerminalLeaves&&
      wins===cert.distinctWin10&&verdicts.size-wins===cert.distinctLoss10&&
      states===cert.terminalStatesPerGeometry,
      'full first-loss terminal replay differs');
  }else need(obligations===32&&verdicts.size===32,
    'minimal LOSS9 witness count changed');
  const positiveLeaves=verdicts.size,positiveStates=states;
  if(negative){
    // Root zero's first two children are terminal WIN; index 2 is LOSS.
    need(claims[0]===2,'negative-control precondition changed');
    let rejected=false;
    try{claim(keys[0],0);}catch(_){rejected=true;}
    need(rejected,'forged LOSS9 witness accepted');
    rejected=false;
    try{claim(keys[0],255);}catch(_){rejected=true;}
    need(rejected,'out-of-range witness accepted');
  }
  return {verified:true,full,roots:keys.length,win9:0,loss9:32,
    uniqueTerminalLeaves:positiveLeaves,terminalStatesPerGeometry:positiveStates,
    derivedLoss9ParentClosure:parents.size,independentGeometries:2,
    newProofOnlyWin8:0,conditionalUnprovedEdges:100,emptyBoard:'UNKNOWN'};
}
if(require.main===module)console.log(JSON.stringify(run({
  full:process.argv.includes('--full'),negative:process.argv.includes('--negative')}),null,2));
module.exports={run};
