#!/usr/bin/env node
'use strict';
// Provenance/conflict and historical-gap audit, NOT terminal minimax.
// The independent terminal proof is verify.py and uses no frozen caches.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const historical=require('../n11-s9-neighbor23-s7-union-20261026/audit.js');
const loss=require('../n11-s8-shared-loss-terminal-20261026/audit.js');
const previous=require('../n11-terminal-s7-s8-legacy187-union-20261025/audit.js');
const latest=require('../n11-s6-legacy3-loss-union-20261025/audit.js');
const ROOT='00000000000100001000000042401008';
const need=(v,m)=>{if(!v)throw Error(m);};
function audit(){
 const rows=fs.readFileSync(path.join(__dirname,'s8-witness.tsv'),'utf8').trim()
   .split('\n').map(x=>x.trim().split(/\s+/));
 const roots=new Set(fs.readFileSync(path.join(__dirname,'s9-roots.keys'),'utf8')
   .trim().split(/\s+/));
 need(rows.length===34&&roots.size===17,'certificate manifest count');
 const s8=new Set(rows.map(r=>r[0]));
 need(s8.size===34&&[...g.children(g.board(ROOT,7))].every(h=>s8.has(h)),
   'S7 all-child boundary changed');
 for(const [h,w] of rows){
   need(roots.has(w)&&g.children(g.board(h,8)).has(w),
     'illegal or missing S8->S9 witness');
 }
 const history=historical.audit();
 const row=history.proofOnlyFrontier.closestS7.find(x=>x.s7===ROOT);
 need(row&&row.legal===34&&row.secured===13&&row.uncovered===21,
   'historical 13/34 secured S8 boundary changed');
 const gaps=new Set(row.missingS8);
 need(gaps.size===21&&[...gaps].every(h=>s8.has(h)),
   'old S8 gap list does not match complete S7 certificate');
 const oldLoss8=new Set([...previous.certifiedLoss8(),
   ...latest.source().cert.roots]);
 const allLoss8=new Set([...oldLoss8,loss.audit().s8LossRoot]);
 need(oldLoss8.size===76&&allLoss8.size===77&&
   [...s8].every(h=>!allLoss8.has(h))&&
   !g.reverse(allLoss8).has(ROOT),
   'certified S8/S7 WIN/LOSS conflict');
 const frozenLoss8=new Set(fs.readFileSync(path.resolve(__dirname,
   '../n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'),
   'utf8').trim().split(/\s+/));
 need(frozenLoss8.size===294&&[...s8].every(h=>!frozenLoss8.has(h)),
   'frozen S8 WIN/LOSS conflict');
 const parents6=g.reverse([ROOT]);
 need(parents6.size===7&&[...parents6].every(h=>
   g.children(g.board(h,6)).has(ROOT)),'S6 reverse witness incomplete');
 return {s7Root:ROOT,s7Outcome:'original-first WIN',
   fullLegalS8:34,previouslySecuredS8:13,previouslyMissingS8:21,
   newlyTerminalCoveredS8:[...gaps].sort(),
   distinctS9Witnesses:roots.size,
   s6WinWitnessParents:[...parents6].sort(),
   certifiedS8LossConflicts:0,frozenS8LossConflicts:0,
   newlyClosedS7:1,newlyClosedTwoStoneRoots:0,emptyBoard:'UNKNOWN',
   terminalVerifier:'n11-s7-complete-terminal-20261026/verify.py'};
}
module.exports={audit};
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
