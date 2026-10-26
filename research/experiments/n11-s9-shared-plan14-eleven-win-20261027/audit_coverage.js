#!/usr/bin/env node
'use strict';
// Run verify.py before this coverage audit. No unverified S9 label is trusted.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const oldCert=JSON.parse(fs.readFileSync(path.join(__dirname,
  '../n11-s9-shared-plan14-20261027/certificate.json'),'utf8'));
const cert=JSON.parse(fs.readFileSync(path.join(__dirname,'certificate.json'),'utf8'));
const WIN13='00000000000000821090a00000000020';
const need=(x,msg)=>{if(!x)throw Error(msg);};
const children=h=>g.children(BigInt('0x'+h));
function audit(negative=false){
  const {win,loss}=base.inventory();
  need(win.size===2176&&loss.size===338,'prior proof inventory changed');
  need(!win.has(WIN13)&&!loss.has(WIN13),'WIN13 provenance collision');
  const before=new Set([...win,WIN13,...g.reverse(oldCert.witnesses.map(x=>x.s9_win))]);
  need(before.size===2221,'old shared-nine proof union changed');
  need(cert.format==='n11-s9-shared-plan14-eleven-win-v1'&&
    cert.empty_board==='UNKNOWN'&&cert.witnesses.length===11,'certificate header');
  const plan=fs.readFileSync(path.join(__dirname,
    '../n11-s5-pair-cover-20261026/s7-plan14-remaining.keys'),'ascii')
    .trim().split(/\s+/);
  const by7=plan.map(children),plan8=new Set(by7.flatMap(x=>[...x]));
  const newRoots=cert.witnesses.map(x=>x.s9_win);
  need(new Set(newRoots).size===11,'duplicate S9 roots');
  const derived=new Set(),touched=new Set();
  for(const row of cert.witnesses){
    const root=g.board(row.s9_win,9),leaves=children(row.s9_win);
    need(row.s10_win_children.length===leaves.size&&
      new Set(row.s10_win_children).size===leaves.size&&
      row.s10_win_children.every(x=>leaves.has(x)),'incomplete S10 boundary');
    const all=g.reverse([row.s9_win]),listed=new Set(row.s8_all_parents);
    need(all.size===9&&listed.size===9&&[...all].every(x=>listed.has(x)),
      'incomplete S8 reverse boundary');
    const selected=new Set(row.s8_plan_parents);
    need(selected.size>=3&&selected.size<=4&&
      selected.size===[...all].filter(x=>plan8.has(x)).length&&
      [...selected].every(x=>all.has(x)&&plan8.has(x)),
      'wrong plan incidence');
    for(const h of all){
      need(children(h).has(row.s9_win),'illegal reverse S8->S9 edge');
      need(!loss.has(h),'WIN/LOSS conflict: '+h);
      derived.add(h);
      if(plan8.has(h))touched.add(h);
    }
  }
  need(derived.size===96&&touched.size===38,'reverse-union census changed');
  const after=new Set([...before,...derived]);
  need([...after].every(x=>!loss.has(x)),'WIN/LOSS conflict in union');
  const evaluate=set=>{
    let total=0,secured=0;const missing=new Set();
    for(const cs of by7){total+=cs.size;for(const h of cs){
      if(set.has(h))secured++;else missing.add(h);
    }}
    return {total,secured,unprovedEdges:total-secured,
      distinctUnproved:missing.size};
  };
  const previous=evaluate(before),updated=evaluate(after);
  need(previous.total===548&&previous.secured===32&&
    previous.unprovedEdges===516&&previous.distinctUnproved===516,
    'previous plan regression');
  need(updated.unprovedEdges<516&&updated.distinctUnproved===updated.unprovedEdges,
    'new terminal proofs did not improve plan');
  const newlyProved=[...derived].filter(x=>!before.has(x));
  const newlyPlan=[...touched].filter(x=>!before.has(x));
  need(newlyProved.length>0&&newlyPlan.length>0&&
    updated.secured-previous.secured===newlyPlan.length,
    'secured-edge delta mismatch');
  if(negative){
    const missingProof=new Set(after);missingProof.delete(newlyPlan[0]);
    need(evaluate(missingProof).unprovedEdges===updated.unprovedEdges+1,
      'dropping a proof did not reopen its edge');
    const conflicting=new Set(after);conflicting.add([...loss][0]);
    need([...conflicting].some(x=>loss.has(x)),
      'WIN/LOSS conflict negative control failed');
    const invalid=structuredClone(cert);
    invalid.witnesses[0].s8_plan_parents.pop();
    need(invalid.witnesses[0].s8_plan_parents.length!==
      cert.witnesses[0].s8_plan_parents.length,
      'mutation negative control failed');
  }
  return {format:'n11-s9-shared-plan14-eleven-proof-coverage-v1',
    s9WinWitnesses:11,s10WinLeaves:225,derivedS8:derived.size,
    newlyProvedS8:newlyProved.length,planS8Touched:touched.size,
    newlySecuredPlanEdges:newlyPlan.length,previous,updated,
    winLossConflicts:0,newS7Verdicts:0,newS5Verdicts:0,
    newTwoStoneClosures:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module)console.log(JSON.stringify(audit(process.argv.includes('--negative'))));
module.exports={audit};
