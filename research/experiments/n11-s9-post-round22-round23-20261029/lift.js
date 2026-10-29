#!/usr/bin/env node
'use strict';
// Lift independently verified round23 WIN9 only; no search statistics are verdicts.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const verify=require('./verify_compact.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
function run(){
  const saved=console.log;let audited;
  try{console.log=()=>{};audited=verify.verify({negative:true});}
  finally{console.log=saved;}
  need(audited.verified&&audited.win9===2&&audited.loss9===3&&
    audited.emptyBoard==='UNKNOWN','independent round23 terminal verification failed');
  const plan=read('../n11-s9-post-round22-replan-20261029/next-plan.json');
  const cert=read('certificate.json');
  const prior=read('../n11-s9-post-round21-round22-20261029/certificate.json');
  const prevLift=read('../n11-s9-post-round20-round21-20261029/lift.json');
  need(cert.sourcePlanSha256===plan.newSelectionSha256&&
    cert.sourcePriorWitnessSha256===prior.witnessSha256&&
    cert.win9===2&&cert.loss9===3&&cert.newTwoStoneClosures===0&&
    plan.proofOnlyWin8After===5835&&plan.conditionalUnprovedEdges===40&&
    prevLift.proofOnlyWIN8After===5835&&prevLift.updated.missing===40,
    'upstream certificate or proof-only frontier mismatch');
  const inv=r7.inventory(),{s,secured}=inv;
  need(inv.missing.length===100&&secured.size===5407,'round7 inventory changed');
  let priorSecured=new Set(secured);
  for(let n=9;n<=22;n++){
    const day=n<=12?'20261028':'20261029';
    const c=read('../n11-s9-post-round'+(n-1)+'-round'+n+'-'+day+'/certificate.json');
    need(c.emptyBoard==='UNKNOWN'&&Array.isArray(c.win9Keys)&&
      c.win9Keys.length===c.win9,'previous terminal batch mismatch '+n);
    for(const par of g.reverse(c.win9Keys))priorSecured.add(par);
  }
  const before=r7.coverage(s.plan,priorSecured);
  need(priorSecured.size===5835&&before.total===548&&
    before.secured===508&&before.missing===40,'round22 proof-only baseline mismatch');
  const derived=g.reverse(cert.win9Keys);
  for(const h of derived)need(!s.loss.has(h),'WIN8/LOSS8 conflict '+h);
  for(const h of cert.win9Keys)for(const par of g.reverse([h]))
    need(g.children(g.board(par,8)).has(h)&&ind.children4(par).has(h),
      'illegal WIN8 witness '+h);
  const afterSecured=new Set([...priorSecured,...derived]);
  const updated=r7.coverage(s.plan,afterSecured);
  need(updated.total===548&&updated.missing<=before.missing,
    'conditional coverage regression');
  const result={
    schema:'n11-round23-terminal-win8-lift-v1',emptyBoard:'UNKNOWN',
    verifiedWin9:cert.win9,verifiedLoss9:cert.loss9,
    distinctWIN8ParentsFromRound23:derived.size,
    newProofOnlyWIN8:afterSecured.size-priorSecured.size,
    proofOnlyWIN8Before:priorSecured.size,proofOnlyWIN8After:afterSecured.size,
    previous:before,updated,
    newlySecuredConditionalEdges:before.missing-updated.missing,
    winLossConflicts:0,newS7Verdicts:0,newS5Verdicts:0,newTwoStoneClosures:0
  };
  const fixed=path.join(__dirname,'lift.json');
  if(fs.existsSync(fixed))need(
    JSON.stringify(read('lift.json'))===JSON.stringify(result),
    'frozen lift replay mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
