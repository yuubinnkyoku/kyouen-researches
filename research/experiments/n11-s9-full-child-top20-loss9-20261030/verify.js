#!/usr/bin/env node
'use strict';
// Exact N11 top20 LOSS9 replay: independent 3x3/4x4 terminal geometries.
// No unfinished search, pn/dn, or heuristic score is accepted as proof.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function verify(negative=false){
  const audit=read('../n11-s8-complete-child-audit-20261030/incidence.json');
  const cert=read('certificate.json');
  need(audit.schema==='n11-fixed14-complete-s8-s9-incidence-v1'&&
    audit.emptyBoard==='UNKNOWN'&&audit.proofOnlyWin8===5859&&
    audit.fixedPlanUnprovedS8===37&&audit.distinctUnknown9===799&&
    audit.unknown9Edges===829&&audit.certifiedLoss9Edges===259,
    'source incidence audit changed');
  need(cert.format==='n11-fixed14-s8-full-child-top20-loss9-v1'&&
    cert.board===11&&cert.emptyBoard==='UNKNOWN'&&
    cert.sourceIncidence==='research/experiments/n11-s8-complete-child-audit-20261030/incidence.json'&&
    cert.proofOnlyWin8Before===5859&&cert.fixedPlanUnprovedS8Before===37&&
    cert.s9LossCount===20&&cert.s9LossWitnesses.length===20&&
    cert.newTwoStoneClosures===0,'certificate header changed');
  const selected=audit.topUnknown9ByPotentialWIN8Coverage;
  need(selected.length===20&&new Set(selected.map(x=>x.h)).size===20,
    'source top20 changed');
  const newLoss=new Set(),leaves=new Set();let states=0;
  function check(row,i){
    const h=selected[i].h;
    need(row.s9===h&&selected[i].missing8Parents===2,
      'selected S9 mismatch '+i);
    const a=g.children(g.board(h,9)),b=ind.children4(h);
    need(same(a,b)&&a.size===selected[i].legal10,
      'S9 children differ '+h);
    const ordered=[...a].sort();
    need(Number.isInteger(row.index)&&row.index>=0&&row.index<ordered.length&&
      row.s10LossWitness===ordered[row.index],
      'illegal LOSS10 witness '+h);
    const first=g.solve10(row.s10LossWitness);
    const second=ind.solve4(row.s10LossWitness);
    need(!first.win&&!second.win&&first.legal===second.legal&&
      first.states===second.states&&
      first.states===row.s10TerminalStates&&
      first.legal===row.s10LegalMoves,'false LOSS10 witness '+h);
    return first;
  }
  for(let i=0;i<20;i++){
    const row=cert.s9LossWitnesses[i],a=check(row,i);
    need(!leaves.has(row.s10LossWitness),'duplicate LOSS10 witness');
    leaves.add(row.s10LossWitness);states+=a.states;
    const leaf=BigInt('0x'+row.s10LossWitness);
    for(const pt of g.pts(leaf)){
      const parent=g.key(g.canonical(leaf^(1n<<BigInt(pt))));
      need(g.children(g.board(parent,9)).has(row.s10LossWitness)&&
        ind.children4(parent).has(row.s10LossWitness),
        'invalid LOSS9 parent closure '+parent);
      newLoss.add(parent);
    }
  }
  need(newLoss.size===cert.s9LossParentClosure&&
    sha([...newLoss].sort().join('\n')+'\n')===cert.s9LossParentSha256,
    'LOSS9 parent closure digest changed');
  const oldWin=new Set(),oldLoss=new Set();
  for(let n=9;n<=27;n++){
    const day=n<=12?'20261028':'20261029';
    const p=n===9?'../n11-s9-post-s10-reuse-round8-20261028/next-plan.json':
      '../n11-s9-post-round'+(n-1)+'-replan-'+day+'/next-plan.json';
    const c='../n11-s9-post-round'+(n-1)+'-round'+n+'-'+day+'/certificate.json';
    const plan=read(p),prior=read(c);
    const claims=Buffer.from(prior.witnessBase64,'base64');
    need(claims.length===plan.newSelectedKeys.length&&
      sha(plan.newSelectedKeys.join('\n')+'\n')===prior.selectionSha256&&
      sha(claims)===prior.witnessSha256,'prior identity mismatch '+n);
    for(let i=0;i<claims.length;i++){
      const h=plan.newSelectedKeys[i],w=claims[i];
      if(w===255){oldWin.add(h);continue;}
      const kids=[...g.children(g.board(h,9))].sort();
      need(w<kids.length,'prior witness out of range '+n);
      const leaf=BigInt('0x'+kids[w]);
      for(const pt of g.pts(leaf))oldLoss.add(
        g.key(g.canonical(leaf^(1n<<BigInt(pt)))));
    }
  }
  need([...oldWin].every(h=>!oldLoss.has(h)&&!newLoss.has(h)),
    'cross-batch WIN9/LOSS9 conflict');
  const fresh=new Set([...newLoss].filter(h=>!oldLoss.has(h)));
  const s8Rows=[];let oldLossEdges=0,newLossEdges=0,unknownEdges=0;
  const distinctNewUnknown=new Set();
  for(const row of audit.s8Rows){
    const kids=g.children(g.board(row.h,8));
    const old=[...kids].filter(h=>oldLoss.has(h));
    const added=[...kids].filter(h=>fresh.has(h));
    need(kids.size===row.legal9&&old.length===row.certifiedLoss9,
      'prior audit S8 count mismatch '+row.h);
    for(const h of added)distinctNewUnknown.add(h);
    const remain=kids.size-old.length-added.length;
    oldLossEdges+=old.length;newLossEdges+=added.length;unknownEdges+=remain;
    s8Rows.push({h:row.h,added:added.length,unknownAfter:remain});
  }
  need(oldLossEdges===259&&unknownEdges===829-newLossEdges&&
    distinctNewUnknown.size<=fresh.size&&
    s8Rows.every(x=>x.unknownAfter>0),'S8 audit regression');
  if(negative){
    let rejected=false;
    try{check({...cert.s9LossWitnesses[0],s10LossWitness:cert.s9LossWitnesses[1].s10LossWitness},0)}
    catch(_){rejected=true}
    need(rejected,'tampered LOSS10 witness accepted');
    rejected=false;
    try{check({...cert.s9LossWitnesses[0],index:255},0)}
    catch(_){rejected=true}
    need(rejected,'invalid witness index accepted');
  }
  const result={verified:true,emptyBoard:'UNKNOWN',independentGeometries:2,
    s9Loss:20,s10LossLeaves:leaves.size,terminalStatesPerGeometry:states,
    newLoss9ParentClosure:newLoss.size,distinctNewLoss9:fresh.size,
    distinctNewUnknown9:distinctNewUnknown.size,
    oldUnknown9:audit.distinctUnknown9,unknown9After:audit.distinctUnknown9-distinctNewUnknown.size,
    oldUnknownEdges:829,newlyCertifiedLossEdges:newLossEdges,unknownEdgesAfter:unknownEdges,
    fullyClosedS8:0,proofOnlyWin8:5859,fixedPlanUnprovedS8:37,
    newTwoStoneClosures:0,winLossConflicts:0};
  need(JSON.stringify(result)===JSON.stringify(read('result.json')),
    'frozen proof-only result mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)verify(process.argv.includes('--negative'));
module.exports={verify};
