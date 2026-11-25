#!/usr/bin/env node
'use strict';
// Lift only independently verified round21 WIN9 to proof-only WIN8.
// Prospective coverage, partial search and pn/dn are not verdicts.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const verify=require('./verify_compact.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
function run(){
  const originalLog=console.log;let audited;
  try{console.log=()=>{};audited=verify.verify({negative:true});}
  finally{console.log=originalLog;}
  need(audited.verified&&audited.win9===1&&audited.loss9===7&&
    audited.emptyBoard==='UNKNOWN','round21 independent terminal proof failed');
  const plan=read('../n11-s9-post-round20-replan-20261029/next-plan.json');
  const cert=read('certificate.json');
  const priorLift=read('../n11-s9-post-round19-round20-20261029/lift.json');
  const r9=read('../n11-s9-post-round8-round9-20261028/certificate.json');
  const r10=read('../n11-s9-post-round9-round10-20261028/certificate.json');
  const r11=read('../n11-s9-post-round10-round11-20261028/certificate.json');
  const r12=read('../n11-s9-post-round11-round12-20261028/certificate.json');
  const r13=read('../n11-s9-post-round12-round13-20261029/certificate.json');
  const r14=read('../n11-s9-post-round13-round14-20261029/certificate.json');
  const r15=read('../n11-s9-post-round14-round15-20261029/certificate.json');
  const r16=read('../n11-s9-post-round15-round16-20261029/certificate.json');
  const r17=read('../n11-s9-post-round16-round17-20261029/certificate.json');
  const r18=read('../n11-s9-post-round17-round18-20261029/certificate.json');
  const r19=read('../n11-s9-post-round18-round19-20261029/certificate.json');
  const r20=read('../n11-s9-post-round19-round20-20261029/certificate.json');
  need(plan.emptyBoard==='UNKNOWN'&&cert.emptyBoard==='UNKNOWN'&&
    cert.format==='n11-s9-post-round20-round21-terminal-v1'&&
    cert.sourcePlanSha256===plan.newSelectionSha256&&
    cert.sourcePriorWitnessSha256===r20.witnessSha256&&
    plan.proofOnlyWin8After===5827&&plan.conditionalUnprovedEdges===41&&
    cert.win9===1&&cert.loss9===7&&cert.newTwoStoneClosures===0&&
    r9.win9===5&&r10.win9===8&&r11.win9===4&&
    r12.win9===12&&r13.win9===4&&r14.win9===5&&
    r15.win9===3&&r16.win9===3&&r17.win9===4&&r18.win9===1&&
    r19.win9===2&&r19.loss9===10&&
    r20.win9===1&&r20.loss9===8,'terminal certificate chain mismatch');
  const inv=r7.inventory(),{s,secured}=inv;
  need(inv.missing.length===100&&secured.size===5407,'round7 inventory changed');
  const after9=new Set([...secured,...g.reverse(r9.win9Keys)]);
  const after10=new Set([...after9,...g.reverse(r10.win9Keys)]);
  const after11=new Set([...after10,...g.reverse(r11.win9Keys)]);
  const after12=new Set([...after11,...g.reverse(r12.win9Keys)]);
  const after13=new Set([...after12,...g.reverse(r13.win9Keys)]);
  const after14=new Set([...after13,...g.reverse(r14.win9Keys)]);
  const after15=new Set([...after14,...g.reverse(r15.win9Keys)]);
  const after16=new Set([...after15,...g.reverse(r16.win9Keys)]);
  const after17=new Set([...after16,...g.reverse(r17.win9Keys)]);
  const after18=new Set([...after17,...g.reverse(r18.win9Keys)]);
  const after19=new Set([...after18,...g.reverse(r19.win9Keys)]);
  const after20=new Set([...after19,...g.reverse(r20.win9Keys)]);
  const before=r7.coverage(s.plan,after20);
  need(after9.size===5449&&after10.size===5513&&
    after11.size===5545&&after12.size===5643&&after13.size===5675&&
    after14.size===5715&&after15.size===5739&&after16.size===5763&&
    after17.size===5795&&after18.size===5803&&after19.size===5819&&
    after20.size===5827&&
    before.total===548&&before.secured===507&&before.missing===41&&
    priorLift.proofOnlyWIN8After===5827&&priorLift.updated.missing===41,
    'round19 proof-only frontier mismatch');
  const derived=g.reverse(cert.win9Keys);
  for(const h of derived)need(!s.loss.has(h),'WIN8/LOSS8 conflict '+h);
  for(const h of cert.win9Keys)for(const par of g.reverse([h]))
    need(g.children(g.board(par,8)).has(h)&&ind.children4(par).has(h),
      'illegal WIN8 witness '+h);
  const after21=new Set([...after20,...derived]);
  const updated=r7.coverage(s.plan,after21);
  need(updated.total===548&&updated.missing<=before.missing,
    'conditional coverage regression');
  const result={schema:'n11-round21-terminal-win8-lift-v1',
    emptyBoard:'UNKNOWN',verifiedWin9:cert.win9,verifiedLoss9:cert.loss9,
    distinctWIN8ParentsFromRound21:derived.size,
    newProofOnlyWIN8:after21.size-after20.size,
    proofOnlyWIN8Before:after20.size,proofOnlyWIN8After:after21.size,
    previous:before,updated,
    newlySecuredConditionalEdges:before.missing-updated.missing,
    winLossConflicts:0,newS7Verdicts:0,newS5Verdicts:0,
    newTwoStoneClosures:0};
  const fixed=path.join(__dirname,'lift.json');
  if(fs.existsSync(fixed))need(
    JSON.stringify(read('lift.json'))===JSON.stringify(result),
    'frozen lift mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
