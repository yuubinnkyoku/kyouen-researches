#!/usr/bin/env node
'use strict';
// Proof-only upward propagation of independently certified round15 WIN9.
// No partial search statistic or prospective edge is a verdict.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const verify=require('./verify_compact.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
function run(){
  const originalLog=console.log;
  let audited;
  try{console.log=()=>{};audited=verify.verify({negative:true});}
  finally{console.log=originalLog;}
  need(audited.verified&&audited.win9===3&&audited.loss9===29,
    'round15 independent terminal proof failed');
  const plan=read('../n11-s9-post-round14-replan-20261029/next-plan.json');
  const cert=read('certificate.json');
  const priorLift=read('../n11-s9-post-round13-round14-20261029/lift.json');
  const r9=read('../n11-s9-post-round8-round9-20261028/certificate.json');
  const r10=read('../n11-s9-post-round9-round10-20261028/certificate.json');
  const r11=read('../n11-s9-post-round10-round11-20261028/certificate.json');
  const r12=read('../n11-s9-post-round11-round12-20261028/certificate.json');
  const r13=read('../n11-s9-post-round12-round13-20261029/certificate.json');
  const r14=read('../n11-s9-post-round13-round14-20261029/certificate.json');
  need(plan.emptyBoard==='UNKNOWN'&&cert.emptyBoard==='UNKNOWN'&&
    cert.format==='n11-s9-post-round14-round15-terminal-v1'&&
    cert.sourcePlanSha256===plan.newSelectionSha256&&
    cert.sourcePriorWitnessSha256===r14.witnessSha256&&
    plan.proofOnlyWin8After===5715&&plan.conditionalUnprovedEdges===55&&
    cert.win9===3&&cert.loss9===29&&cert.newTwoStoneClosures===0&&
    r9.win9===5&&r10.win9===8&&r11.win9===4&&r12.win9===12&&r13.win9===4&&r14.win9===5,
    'terminal certificate chain mismatch');
  const inv=r7.inventory(),{s,secured}=inv;
  need(inv.missing.length===100&&secured.size===5407,'round7 inventory changed');
  const after9=new Set([...secured,...g.reverse(r9.win9Keys)]);
  const after10=new Set([...after9,...g.reverse(r10.win9Keys)]);
  const after11=new Set([...after10,...g.reverse(r11.win9Keys)]);
  const after12=new Set([...after11,...g.reverse(r12.win9Keys)]);
  const after13=new Set([...after12,...g.reverse(r13.win9Keys)]);
  const after14=new Set([...after13,...g.reverse(r14.win9Keys)]);
  const before=r7.coverage(s.plan,after14);
  need(after9.size===5449&&after10.size===5513&&
    after11.size===5545&&after12.size===5643&&after13.size===5675&&
    after14.size===5715&&before.total===548&&before.secured===493&&before.missing===55&&
    priorLift.proofOnlyWIN8After===5715&&priorLift.updated.missing===55,
    'round14 proof-only frontier mismatch');
  const derived=g.reverse(cert.win9Keys);
  for(const h of derived)need(!s.loss.has(h),'WIN8/LOSS8 conflict '+h);
  for(const h of cert.win9Keys)for(const par of g.reverse([h]))
    need(g.children(g.board(par,8)).has(h),'illegal WIN8 witness '+h);
  const after15=new Set([...after14,...derived]);
  const updated=r7.coverage(s.plan,after15);
  need(updated.total===548&&updated.missing<=before.missing,
    'conditional coverage regression');
  const result={schema:'n11-round15-terminal-win8-lift-v1',
    emptyBoard:'UNKNOWN',verifiedWin9:cert.win9,verifiedLoss9:cert.loss9,
    distinctWIN8ParentsFromRound15:derived.size,
    newProofOnlyWIN8:after15.size-after14.size,
    proofOnlyWIN8Before:after14.size,proofOnlyWIN8After:after15.size,
    previous:before,updated,
    newlySecuredConditionalEdges:before.missing-updated.missing,
    winLossConflicts:0,newS7Verdicts:0,newS5Verdicts:0,
    newTwoStoneClosures:0};
  const frozen=path.join(__dirname,'lift.json');
  if(fs.existsSync(frozen))need(
    JSON.stringify(read('lift.json'))===JSON.stringify(result),
    'frozen lift mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
