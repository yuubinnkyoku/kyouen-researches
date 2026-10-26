#!/usr/bin/env node
'use strict';
// This structural audit NEVER trusts an S9 label: run verify.py first.
// Only independent-terminal S8 WINs enter the secured-coverage count.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const cert=JSON.parse(fs.readFileSync(path.join(__dirname,'certificate.json'),'utf8'));
const need=(x,m)=>{if(!x)throw Error(m);};
const WIN13='00000000000000821090a00000000020';
const PLAN='../n11-s5-pair-cover-20261026/s7-plan14-remaining.keys';
const children=h=>g.children(BigInt('0x'+h));
function audit(negative=false){
  const {win,loss}=base.inventory();
  need(win.size===2176&&loss.size===338,'proof-only source counts changed');
  need(!win.has(WIN13)&&!loss.has(WIN13),'WIN13 source conflict');
  const before=new Set([...win,WIN13]);
  need(before.size===2177,'previous WIN13 union changed');
  const roots=cert.witnesses.map(r=>r.s9_win);
  need(roots.length===5&&new Set(roots).size===5,'invalid S9 roots');
  const derived=new Set(),planHit=new Set();
  const plan=fs.readFileSync(path.join(__dirname,PLAN),'ascii').trim().split(/\s+/);
  need(plan.length===14&&new Set(plan).size===14,'invalid plan');
  const by7=new Map(plan.map(h=>[h,children(h)]));
  const plan8=new Set([...by7.values()].flatMap(s=>[...s]));
  for(const row of cert.witnesses){
    const all=g.reverse([row.s9_win]);
    need(all.size===9,'unexpected reverse S8 boundary');
    const listed=new Set(row.s8_all_parents),selected=new Set(row.s8_plan_parents);
    need(listed.size===9&&[...listed].every(h=>all.has(h)),
         'invalid all-parent manifest');
    need(selected.size===4&&[...selected].every(h=>all.has(h)&&plan8.has(h)),
         'invalid plan-parent manifest');
    need([...all].filter(h=>plan8.has(h)).length===4,
         'missing plan-parent incidence');
    for(const h of all){
      need(!derived.has(h),'S8 witness overlap');
      need(!loss.has(h),'WIN/LOSS conflict: '+h);
      derived.add(h);
      if(plan8.has(h))planHit.add(h);
    }
  }
  need(derived.size===45&&planHit.size===20,'S8 union changed');
  const after=new Set([...before,...derived]);
  const evaluate=winSet=>{
    let total=0,secured=0;const open=new Set();
    for(const cs of by7.values()){
      total+=cs.size;
      for(const h of cs)if(winSet.has(h))secured++;else open.add(h);
    }
    return {total,secured,missing:total-secured,distinctMissing:open.size};
  };
  const old=evaluate(before),now=evaluate(after);
  need(old.total===548&&old.secured===13&&old.missing===535&&
       old.distinctMissing===535,'previous matching baseline changed');
  need(now.total===548&&now.missing<535&&now.distinctMissing===now.missing,
       'no secured-coverage improvement or overlap regression');
  const newlyProved=[...derived].filter(h=>!before.has(h));
  const newlyPlan=[...planHit].filter(h=>!before.has(h));
  need(now.secured-old.secured===newlyPlan.length,
       'newly secured edge count mismatch');
  if(negative){
    const bad=new Set([...after]);bad.delete(newlyPlan[0]);
    need(evaluate(bad).missing===now.missing+1,'proof removal did not reopen edge');
    need([...derived].every(h=>!loss.has(h)),'WIN/LOSS conflict');
  }
  return {format:'n11-s9-shared-plan14-proof-only-coverage-v1',
    s9WinWitnesses:5,s10WinLeaves:85,derivedS8Win:45,
    newlyDerivedS8Win:newlyProved.length,planS8Touched:20,
    newlySecuredPlanEdges:newlyPlan.length,previous:old,updated:now,
    winLossConflicts:0,newS7Verdicts:0,newS5Verdicts:0,
    newTwoStoneClosures:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module)console.log(JSON.stringify(audit(process.argv.includes('--negative'))));
module.exports={audit};
