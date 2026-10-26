#!/usr/bin/env node
'use strict';
// Correct a recurring fixed-first parity error in the historical
// S8 LOSS -> S7 LOSS -> S6 'WIN' -> S5 'secured WIN' reverse census.
// Geometry-only parent sets are not certified verdict sets.
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const previous=require('../n11-terminal-s7-s8-legacy187-union-20261025/audit.js');
const latest=require('../n11-s6-legacy3-loss-union-20261025/audit.js');
const need=(v,m)=>{if(!v)throw Error(m);};
const S8_LOSS='000000100010a0011000000001004000';
const S7_WIN='00000000000100001000000042401008';
function fixedFirst(layer,children){
 if(layer%2===0){
   if(children.includes('WIN'))return 'WIN';
   return children.every(v=>v==='LOSS')?'LOSS':'UNKNOWN';
 }
 if(children.includes('LOSS'))return 'LOSS';
 return children.every(v=>v==='WIN')?'WIN':'UNKNOWN';
}
function audit(){
 need(fixedFirst(7,['LOSS','UNKNOWN'])==='LOSS'&&
   fixedFirst(6,['LOSS','UNKNOWN'])==='UNKNOWN'&&
   fixedFirst(6,['WIN','UNKNOWN'])==='WIN'&&
   fixedFirst(5,['WIN','UNKNOWN'])==='UNKNOWN'&&
   fixedFirst(5,['WIN','WIN'])==='WIN',
   'fixed-first AND/OR parity regression');
 const old8=new Set([...previous.certifiedLoss8(),...latest.source().cert.roots]);
 const all8=new Set([...old8,S8_LOSS]);
 const loss7=g.reverse(all8),candidate6=g.reverse(loss7);
 need(old8.size===76&&all8.size===77&&loss7.size===562&&
   candidate6.size===1737,'historical geometry-only census changed');
 // These are geometric edges, not secured WIN edges: S6 is OR over S7 WIN.
 const candidateEdges=new Set();
 for(const h of candidate6){
   const b=g.board(h,6);
   for(const p of g.pts(b))candidateEdges.add(
     g.key(g.canonical(b^(1n<<BigInt(p))))+':'+h);
 }
 need(candidateEdges.size===10422,'historical S5 incidence census changed');
 const certified6=g.reverse([S7_WIN]);
 need(certified6.size===7&&[...certified6].every(h=>
   g.children(g.board(h,6)).has(S7_WIN)),
   'new independently certified S7 WIN does not support S6 WIN');
 return {s8Loss:all8.size,certifiedS7LossFromS8:loss7.size,
   s6GeometricParentsOfS7Loss:candidate6.size,
   s6WinCertifiedByThatLossOnly:0,
   s5GeometricEdgesFromUncertifiedS6:candidateEdges.size,
   s5WinEdgesCertifiedByThatLossOnly:0,
   s6WinCertifiedByNewS7Win:certified6.size,
   overlapWithHistoricalUncertifiedS6:[...certified6].filter(h=>
     candidate6.has(h)).length,
   correctedRule:'even S6 WIN requires a legal S7 WIN child; S7 LOSS is not a WIN witness',
   source:'K0371 fixed-player propagation; historical audit counts are geometry-only',
   newlyClosedTwoStoneRoots:0,emptyBoard:'UNKNOWN'};
}
module.exports={fixedFirst,audit};
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
