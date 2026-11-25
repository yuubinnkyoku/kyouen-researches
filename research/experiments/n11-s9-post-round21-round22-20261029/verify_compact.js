#!/usr/bin/env node
'use strict';
// Independently replay the minimal terminal obligations of round22.
// No unfinished search count, cached verdict or discovery ordering is trusted.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
function verify({negative=false}={}){
  const plan=read('../n11-s9-post-round21-replan-20261029/next-plan.json');
  const cert=read('certificate.json'),keys=plan.newSelectedKeys;
  const prior=read('../n11-s9-post-round20-round21-20261029/certificate.json');
  const preflight=read('../n11-s9-post-round21-replan-20261029/preflight.json');
  const claims=Buffer.from(cert.witnessBase64,'base64');
  need(cert.format==='n11-s9-post-round21-round22-terminal-v1'&&
    cert.board===11&&cert.perspective==='original-first-player'&&
    cert.emptyBoard==='UNKNOWN'&&plan.emptyBoard==='UNKNOWN'&&
    plan.conditionalUnprovedEdges===40&&plan.proofOnlyWin8After===5835&&
    plan.eligibleUnprovedS9===32&&plan.undominatedS9===5&&
    cert.sourcePlanSha256===plan.newSelectionSha256&&
    cert.sourcePriorWitnessSha256===prior.witnessSha256&&
    plan.sourceWitnessSha256===prior.witnessSha256&&
    preflight.selectionSha256===plan.newSelectionSha256&&
    preflight.legalS10Edges===138&&preflight.distinctS10Classes===138&&
    cert.selectionSha256===plan.newSelectionSha256&&
    keys.length===5&&claims.length===5&&new Set(keys).size===5&&
    sha(keys.join('\n')+'\n')===plan.newSelectionSha256&&
    sha(claims)===cert.witnessSha256&&
    claims.toString('base64')===cert.witnessBase64,
    'frozen plan/certificate identity mismatch');
  const leaves=new Map(),wins=[],lossLeaves=[];
  let states=0,obligations=0,winEdges=0,allEdges=0;
  function terminal(h){
    if(leaves.has(h))return leaves.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.legal===b.legal&&a.states===b.states,
      'independent terminal disagreement '+h);
    leaves.set(h,a);states+=a.states;return a;
  }
  function check(h,w){
    const children=g.children(g.board(h,9));
    need(same(children,ind.children4(h)),'S9 boundary mismatch '+h);
    const ordered=[...children].sort();
    if(w===255){
      for(const child of ordered){
        obligations++;need(terminal(child).win,'forged WIN9 '+h);
      }
      return {win:true,children:ordered.length};
    }
    need(Number.isInteger(w)&&w>=0&&w<ordered.length,
      'invalid LOSS9 witness index '+h);
    obligations++;need(!terminal(ordered[w]).win,'forged LOSS9 '+h);
    return {win:false,leaf:ordered[w],children:ordered.length};
  }
  for(let i=0;i<keys.length;i++){
    const h=keys[i],c=check(h,claims[i]);
    allEdges+=c.children;
    if(c.win){
      wins.push(h);winEdges+=c.children;
      for(const par of g.reverse([h]))need(
        g.children(g.board(par,8)).has(h)&&ind.children4(par).has(h),
        'WIN8 parent incidence '+h);
    }else lossLeaves.push(c.leaf);
  }
  const parents=new Set();
  for(const leaf of lossLeaves){
    const b=BigInt('0x'+leaf);
    for(const pt of g.pts(b)){
      const par=g.key(g.canonical(b^(1n<<BigInt(pt))));
      need(g.children(g.board(par,9)).has(leaf)&&
        ind.children4(par).has(leaf),'LOSS9 parent incidence '+par);
      parents.add(par);
    }
  }
  need(wins.every(h=>!parents.has(h)),'WIN9/LOSS9 conflict');
  // Fail closed if a newly derived LOSS9 parent was certified WIN9 in
  // any earlier independently audited terminal batch.
  const earlierWins=new Set();
  for(let n=9;n<=21;n++){
    const day=n<=12?'20261028':'20261029';
    const c=read('../n11-s9-post-round'+(n-1)+'-round'+n+'-'+day+'/certificate.json');
    for(const h of c.win9Keys)earlierWins.add(h);
  }
  need([...parents].every(h=>!earlierWins.has(h)),
    'cross-batch WIN9/LOSS9 conflict');
  need(allEdges===138&&cert.orderedS10Children===138&&
    cert.win9===wins.length&&cert.loss9===5-wins.length&&
    JSON.stringify(cert.win9Keys)===JSON.stringify(wins)&&
    cert.win10Edges===winEdges&&cert.loss9ParentClosure===parents.size&&
    cert.loss9ParentSha256===sha([...parents].sort().join('\n')+'\n')&&
    cert.uniqueTerminalLeaves>=leaves.size&&
    cert.terminalStatesPerGeometry>=states&&
    cert.firstLossSearchObligations>=obligations&&
    cert.newTwoStoneClosures===0,
    'frozen terminal/reverse proof mismatch');
  const positive={verified:true,win9:wins.length,loss9:5-wins.length,
    terminalObligations:obligations,uniqueTerminalLeaves:leaves.size,
    terminalStatesPerGeometry:states,independentGeometries:2,
    newTwoStoneClosures:0,emptyBoard:'UNKNOWN'};
  if(negative){
    const wi=claims.indexOf(255),li=claims.findIndex(x=>x!==255);
    if(wi>=0){let fail=false;try{check(keys[wi],0)}catch(_){fail=true}
      need(fail,'forged LOSS9 accepted');}
    if(li>=0){let fail=false;try{check(keys[li],255)}catch(_){fail=true}
      need(fail,'forged WIN9 accepted');}
    let fail=false;try{check(keys[0],254)}catch(_){fail=true}
    need(fail,'out-of-range witness accepted');
  }
  console.log(JSON.stringify(positive,null,2));return positive;
}
if(require.main===module)verify({negative:process.argv.includes('--negative')});
module.exports={verify};
