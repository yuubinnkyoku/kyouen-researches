#!/usr/bin/env node
'use strict';
// Targeted 23-child S9 terminal census, prioritizing still-unsecured S8 parents.
// No df-pn, incomplete search, or cached verdict is used as terminal evidence.
const crypto=require('node:crypto'),fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const n22=require('../n11-s9-n22-complete-20261027/verify.js');
const need=(x,m)=>{if(!x)throw Error(m);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function run(){
  // The prior 890-root certificate must be terminal-replayed before its
  // propagated WIN8 set is admitted as evidence.
  const audited=n22.verify();
  need(audited.proofOnlyWin8After===4944&&audited.updated.missing===174,
    'upstream proof-only boundary changed');
  const {by9,plan,plan8}=n22.inventory();
  const {before,loss}=n22.priorProofs();
  const prevCert=JSON.parse(fs.readFileSync(path.join(__dirname,
    '../n11-s9-n22-complete-20261027/compact-certificate.json'),'utf8'));
  const prevBytes=Buffer.from(prevCert.witnessBase64,'base64');
  const prevCandidates=n22.inventory().candidates;
  const oldWin9=prevCandidates.filter((_,i)=>prevBytes[i]===255);
  const secured=new Set([...before,...g.reverse(oldWin9)]);
  need(secured.size===4944,'previous proof-only WIN8 census changed');
  const choices=[];
  for(const [h,parents] of by9){
    const boundary=g.children(g.board(h,9));
    if(parents.size<2||boundary.size!==23)continue;
    const gaps=[...parents].filter(p=>plan8.has(p)&&!secured.has(p)).length;
    choices.push({h,degree:parents.size,gaps});
  }
  choices.sort((a,b)=>b.gaps-a.gaps||b.degree-a.degree||
    (a.h<b.h?-1:a.h>b.h?1:0));
  const positive=choices.filter(x=>x.gaps>0).length;
  const selected=choices.filter(x=>x.gaps>0).slice(0,256);
  need(selected.length>0,'no unresolved S8 parent reachable through 23-child S9');
  const leafCache=new Map(),rootRows=[],winRoots=[],lossRoots=[];
  let edges=0,states=0;
  function terminal(h){
    if(leafCache.has(h))return leafCache.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
      'independent terminal geometry mismatch '+h);
    leafCache.set(h,a);return a;
  }
  for(const {h,gaps,degree} of selected){
    const children=g.children(g.board(h,9));
    need(children.size===23&&same(children,ind.children4(h)),
      'independent S9->S10 geometry mismatch '+h);
    const ordered=[...children].sort();
    let firstLoss=-1,subtotal=0;
    for(let i=0;i<ordered.length;i++){
      const r=terminal(ordered[i]);subtotal+=r.states;
      if(!r.win&&firstLoss<0)firstLoss=i;
    }
    const isWin=firstLoss<0;
    if(isWin){
      winRoots.push(h);edges+=ordered.length;
      for(const p of g.reverse([h])){
        need(g.children(g.board(p,8)).has(h)&&ind.children4(p).has(h),
          'independent S8->S9 reverse boundary mismatch '+h);
      }
    }else lossRoots.push(h);
    rootRows.push({h,degree,gaps,witness:isWin?255:firstLoss,states:subtotal});
    states+=subtotal;
  }
  const derived=new Set(g.reverse(winRoots));
  need([...derived].every(x=>!loss.has(x)),'S8 WIN/LOSS conflict');
  const after=new Set([...secured,...derived]);
  const evaluate=proof=>{
    let total=0,securedEdges=0;const missing=new Set();
    for(const h of plan)for(const c of g.children(g.board(h,7))){
      total++;if(proof.has(c))securedEdges++;else missing.add(c);
    }
    return {total,secured:securedEdges,missing:total-securedEdges,
      distinctMissing:missing.size};
  };
  const old=evaluate(secured),updated=evaluate(after);
  need(old.total===548&&old.missing===174&&updated.missing<=174,
    'conditional proof-only coverage regression');
  const witness=Buffer.from(rootRows.map(x=>x.witness));
  return {
    format:'n11-s9-n23-priority-terminal-probe-v1',board:11,
    perspective:'original-first-player',emptyBoard:'UNKNOWN',
    candidates:choices.length,positiveGapCandidates:positive,
    selected:rootRows.length,selectionSha256:sha(rootRows.map(x=>x.h).join('\n')+'\n'),
    witnessBase64:witness.toString('base64'),witnessSha256:sha(witness),
    win9:winRoots.length,loss9:lossRoots.length,win10Edges:edges,
    independentTerminalLeaves:leafCache.size,
    terminalStatesPerGeometry:states,
    derivedWin8:derived.size,newProofOnlyWin8:after.size-secured.size,
    proofOnlyWin8Before:secured.size,proofOnlyWin8After:after.size,
    knownLoss8:loss.size,previous:old,updated,
    firstFive:rootRows.slice(0,5),winLossConflicts:0,
    newS7Verdicts:0,newS5Verdicts:0,twoStoneClosures:0
  };
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};
