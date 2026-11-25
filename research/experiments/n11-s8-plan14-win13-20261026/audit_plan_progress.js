#!/usr/bin/env node
'use strict';
// Independent terminal proof lives in verify.py. This audits only the
// proof-only inventory and the selected conditional S7 plan's coverage.
const fs=require('node:fs'),path=require('node:path');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const S8='00000000000000821090a00000000020';
const S7='00000000000000821090200000000020';
const need=(v,msg)=>{if(!v)throw Error(msg);};
const children=h=>g.children(BigInt('0x'+h));
function audit(negative=false){
 const {win,loss}=base.inventory();
 need(!win.has(S8),'new terminal S8 WIN already in old proof-only inventory');
 need(!loss.has(S8),'new terminal S8 WIN conflicts with known LOSS');
 const old=base.audit();
 need(old.improved.missing===536&&old.improved.unprovedDistinct===536,
  'old conditional baseline changed');
 const plan=fs.readFileSync(path.join(__dirname,
  '../n11-s5-pair-cover-20261026/s7-plan14-remaining.keys'),'ascii')
  .trim().split(/\s+/);
 need(plan.length===14&&new Set(plan).size===14,'invalid saved 14-root plan');
 const parents=plan.filter(h=>children(h).has(S8));
 need(parents.length===1&&parents[0]===S7,'new S8 not uniquely in selected plan');
 const now=new Set(win);now.add(S8);
 const remaining=plan.reduce((s,h)=>s+[...children(h)].filter(c=>!now.has(c)).length,0);
 const allMissing=new Set();
 for(const h of plan)for(const c of children(h))if(!now.has(c))allMissing.add(c);
 need(remaining===535&&allMissing.size===535,'new secured coverage regression');
 if(negative){
  for(const tampered of [plan.filter(h=>h!==S7),plan.map(h=>h===S7?S8:h)]){
   let rejected=false;
   try{
    need(tampered.length===14&&tampered.every(h=>h.length===32),
     'bad plan dimensions');
    need(tampered.includes(S7)&&tampered.filter(h=>children(h).has(S8)).length===1,
     'new witness missing or malformed');
   }catch(_){rejected=true;}
   need(rejected,'tampered plan accepted');
  }
 }
 return {schema:'n11-s8-win13-proof-only-coverage-v1',s8:S8,s7:S7,
  previously_secured:false,old_remaining_edges:536,new_remaining_edges:remaining,
  old_distinct_unproved_s8:536,new_distinct_unproved_s8:allMissing.size,
  new_s8_win_proofs:1,new_s7_win_proofs:0,new_two_stone_root_closures:0,
  empty_board:'UNKNOWN'};
}
if(require.main===module)console.log(JSON.stringify(audit(process.argv.includes('--negative'))));
module.exports={audit};
