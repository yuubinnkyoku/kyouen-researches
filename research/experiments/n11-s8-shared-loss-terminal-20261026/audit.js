#!/usr/bin/env node
'use strict';
// Proof-only reverse propagation of the independently terminal-certified S8
// original-first LOSS. Frozen caches are used only as conflict comparisons.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const previous=require('../n11-terminal-s7-s8-legacy187-union-20261025/audit.js');
const latest=require('../n11-s6-legacy3-loss-union-20261025/audit.js');
const EXP=path.resolve(__dirname,'..');
const ROOT='000000100010a0011000000001004000';
const need=(v,m)=>{if(!v)throw Error(m);};
const keys=p=>fs.readFileSync(path.join(EXP,p),'utf8').trim().split(/\s+/);
function audit(){
 const root=g.board(ROOT,8);
 const old8=new Set([...previous.certifiedLoss8(),...latest.source().cert.roots]);
 need(old8.size===76&&!old8.has(ROOT),'S8 LOSS source overlap/regression');
 const frozenLoss8=new Set(keys('n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'));
 const frozenWin8=new Set(keys('n11-targeted-terminal-lift-20261015/data/lifted_s8_win_51571.txt'));
 need(frozenLoss8.size===294&&frozenWin8.size===13501&&
   !frozenLoss8.has(ROOT)&&!frozenWin8.has(ROOT),
   'frozen S8 conflict or old label');
 const old7=g.reverse(old8),new7=g.reverse([ROOT]);
 const fresh7=new Set([...new7].filter(h=>!old7.has(h)));
 const all7=new Set([...old7,...new7]);
 need(old7.size===554&&new7.size===8,'S7 LOSS witness boundary changed');
 const frozenWin7=new Set(keys('n11-targeted-terminal-lift-20261015/data/all_s7_win_17.txt'));
 const frozenLoss7=new Set(keys('n11-targeted-terminal-lift-20261015/data/all_s7_loss_2232.txt'));
 need(frozenWin7.size===17&&frozenLoss7.size===2232&&
   [...new7].every(h=>!frozenWin7.has(h))&&
   [...fresh7].every(h=>!frozenLoss7.has(h)),
   'S7 WIN/LOSS conflict or frozen overlap');
 for(const h of new7){
   const b=g.board(h,7);
   need(g.children(b).has(ROOT),'S7 parent lacks legal S8 LOSS witness');
 }
 const old6=g.reverse(old7),all6=g.reverse(all7),new6=g.reverse(fresh7);
 need(old6.size===1710&&[...old6].every(h=>all6.has(h)),
   'previous S6 WIN reverse coverage changed');
 for(const h of new6){
   const b=g.board(h,6);
   need([...g.children(b)].some(c=>fresh7.has(c)),
     'S6 WIN parent lacks legal S7 LOSS witness');
 }
 return {s8LossRoot:ROOT,priorCertifiedS8Loss:old8.size,newCertifiedS8Loss:1,
   certifiedS8Loss:old8.size+1,
   previousS7Loss:old7.size,newS7LossWitnessParents:new7.size,
   addedS7Loss:fresh7.size,totalS7Loss:all7.size,
   previousS6Win:old6.size,affectedS6Win:new6.size,
   addedS6Win:all6.size-old6.size,totalS6Win:all6.size,
   s7LossParents:[...new7].sort(),newS6WinParents:[...all6].filter(h=>!old6.has(h)).sort(),
   frozenConflicts:0,emptyBoard:'UNKNOWN'};
}
module.exports={audit};
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
