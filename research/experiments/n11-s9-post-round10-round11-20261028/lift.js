#!/usr/bin/env node
'use strict';
// Proof-only lift of round11 terminal WIN9 into the conditional 14-root S7 plan.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
function run(){
  const plan=read('../n11-s9-post-round10-replan-20261028/next-plan.json');
  const r9=read('../n11-s9-post-round8-round9-20261028/certificate.json');
  const r10=read('../n11-s9-post-round9-round10-20261028/certificate.json');
  const priorLift=read('../n11-s9-post-round9-round10-20261028/lift.json');
  const cert=read('certificate.json');
  need(plan.emptyBoard==='UNKNOWN'&&cert.emptyBoard==='UNKNOWN'&&
    cert.format==='n11-s9-post-round10-round11-terminal-v1'&&
    cert.sourcePlanSha256===plan.newSelectionSha256&&
    cert.sourcePriorWitnessSha256===r10.witnessSha256&&
    r9.win9===5&&r10.win9===8&&cert.win9===4&&cert.loss9===28&&
    plan.proofOnlyWin8After===5513&&plan.conditionalUnprovedEdges===83,
    'terminal certificate chain mismatch');
  const inv=r7.inventory(),{s,secured}=inv;
  need(inv.missing.length===100&&secured.size===5407,
    'upstream round7 inventory changed');
  const after9=new Set([...secured,...g.reverse(r9.win9Keys)]);
  const after10=new Set([...after9,...g.reverse(r10.win9Keys)]);
  const before=r7.coverage(s.plan,after10);
  need(after9.size===5449&&after10.size===5513&&
    before.total===548&&before.missing===83&&before.secured===465&&
    priorLift.proofOnlyWIN8After===5513&&priorLift.updated.missing===83,
    'round10 proof-only frontier mismatch');
  const derived=g.reverse(cert.win9Keys);
  for(const h of derived)need(!s.loss.has(h),'WIN8/LOSS8 conflict '+h);
  for(const h of cert.win9Keys)for(const par of g.reverse([h]))
    need(g.children(g.board(par,8)).has(h),'illegal WIN8 witness '+h);
  const after11=new Set([...after10,...derived]);
  const updated=r7.coverage(s.plan,after11);
  need(updated.total===548&&updated.missing<=before.missing,
    'conditional coverage regression');
  const result={schema:'n11-round11-terminal-win8-lift-v1',
    emptyBoard:'UNKNOWN',verifiedWin9:cert.win9,verifiedLoss9:cert.loss9,
    distinctWIN8ParentsFromRound11:derived.size,
    newProofOnlyWIN8:after11.size-after10.size,
    proofOnlyWIN8Before:after10.size,proofOnlyWIN8After:after11.size,
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
