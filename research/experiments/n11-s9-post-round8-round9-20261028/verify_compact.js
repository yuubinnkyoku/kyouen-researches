#!/usr/bin/env node
'use strict';
// Independently recheck every proof obligation in the frozen round9 certificate.
// LOSS9 needs one certified LOSS10 child; WIN9 needs every legal WIN10 child.
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
  const cert=JSON.parse(fs.readFileSync(path.join(dir,'certificate.json'),'utf8'));
  const keys=plan.newSelectedKeys,claims=Buffer.from(cert.witnessBase64,'base64');
  need(cert.format==='n11-s9-post-round8-round9-terminal-v1'&&
    cert.board===11&&cert.emptyBoard==='UNKNOWN'&&
    cert.perspective==='original-first-player'&&
    plan.emptyBoard==='UNKNOWN'&&plan.conditionalUnprovedEdges===100&&
    keys.length===32&&claims.length===32&&new Set(keys).size===32&&
    sha(keys.join('\n')+'\n')===plan.newSelectionSha256&&
    cert.selectionSha256===plan.newSelectionSha256&&
    cert.sourcePlanSha256===plan.newSelectionSha256&&
    sha(claims)===cert.witnessSha256,'frozen plan/certificate identity mismatch');
  const inv=r7.inventory(),{s,secured}=inv;
  need(inv.missing.length===100&&secured.size===5407&&
    keys.every(h=>inv.options.some(x=>x.h===h)),'upstream S8 proof changed');
  const leaves=new Map(),wins=[],parents=new Set();
  let states=0,obligations=0,winEdges=0;
  function terminal(h){
    if(leaves.has(h))return leaves.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.legal===b.legal&&a.states===b.states,
      'independent terminal disagreement '+h);
    leaves.set(h,a);states+=a.states;return a;
  }
  function check(h,witness){
    const kids=g.children(g.board(h,9)),other=ind.children4(h);
    need(same(kids,other),'independent S9 boundary disagreement '+h);
    const ordered=[...kids].sort();
    if(witness===255){
      for(const leaf of ordered){
        obligations++;
        need(terminal(leaf).win,'false WIN9 universal child '+h);
      }
      return {win:true,children:ordered.length};
    }
    need(Number.isInteger(witness)&&witness>=0&&witness<ordered.length,
      'invalid LOSS9 witness index');
    const leaf=ordered[witness];
    obligations++;
    need(!terminal(leaf).win,'false LOSS9 witness '+h);
    return {win:false,leaf};
  }
  for(let i=0;i<keys.length;i++){
    const h=keys[i],res=check(h,claims[i]);
    if(res.win){
      wins.push(h);winEdges+=res.children;
      for(const parent of g.reverse([h]))need(
        g.children(g.board(parent,8)).has(h)&&ind.children4(parent).has(h),
        'invalid WIN8 parent incidence '+h);
    }else{
      const b=BigInt('0x'+res.leaf);
      for(const pt of g.pts(b)){
        const parent=g.key(g.canonical(b^(1n<<BigInt(pt))));
        need(g.children(g.board(parent,9)).has(res.leaf)&&
          ind.children4(parent).has(res.leaf),
          'invalid LOSS9 parent incidence '+parent);
        parents.add(parent);
      }
    }
  }
  const derived=g.reverse(wins),after=new Set([...secured,...derived]);
  need([...derived].every(h=>!s.loss.has(h))&&
    wins.every(h=>!parents.has(h)),'WIN/LOSS contradiction');
  const previous=r7.coverage(s.plan,secured),updated=r7.coverage(s.plan,after);
  need(cert.win9===wins.length&&cert.loss9===32-wins.length&&
    JSON.stringify(cert.win9Keys)===JSON.stringify(wins)&&
    cert.win10Edges===winEdges&&cert.derivedWin8===derived.size&&
    cert.newProofOnlyWin8===after.size-secured.size&&
    cert.proofOnlyWin8Before===secured.size&&
    cert.proofOnlyWin8After===after.size&&
    JSON.stringify(cert.previous)===JSON.stringify(previous)&&
    JSON.stringify(cert.updated)===JSON.stringify(updated)&&
    cert.loss9ParentClosure===parents.size&&
    cert.loss9ParentSha256===sha([...parents].sort().join('\n')+'\n')&&
    cert.winLossConflicts===0&&cert.twoStoneClosures===0,
    'frozen upper-layer/parent claim mismatch');
  const positiveLeaves=leaves.size,positiveStates=states,positiveObligations=obligations;
  if(negative){
    const wi=claims.indexOf(255),li=claims.findIndex(x=>x!==255);
    if(wi>=0){
      let rejected=false;try{check(keys[wi],0)}catch(_){rejected=true}
      need(rejected,'forged LOSS9 witness accepted');
    }
    if(li>=0){
      let rejected=false;try{check(keys[li],255)}catch(_){rejected=true}
      need(rejected,'forged WIN9 witness accepted');
    }
    let rejected=false;try{check(keys[0],254)}catch(_){rejected=true}
    need(rejected,'out-of-range witness accepted');
  }
  const result={verified:true,win9:wins.length,loss9:32-wins.length,
    proofOnlyWin8After:after.size,conditionalUnprovedEdges:updated.missing,
    obligations:positiveObligations,uniqueTerminalLeaves:positiveLeaves,
    terminalStatesPerGeometry:positiveStates,independentGeometries:2,
    emptyBoard:'UNKNOWN'};
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run({negative:process.argv.includes('--negative')});
module.exports={run};
