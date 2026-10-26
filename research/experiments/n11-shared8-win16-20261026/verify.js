#!/usr/bin/env node
'use strict';
// Independent of saved verdict caches. Geometry: existing 3x3 determinant.
const fs = require('node:fs');
const path = require('node:path');
const g = require('../n11-gap6-terminal-20261019/verify_js.js');
const ROOT = '00020000000000821090200000000020';
const S9 = '00020000000000821090200000400020';
const PLAN_PARENTS = [
 '00000000000000821090200000000020',
 '00020000000000821080200000000020'
];
const need = (ok,msg) => {if (!ok) throw Error(msg);};
const read = () => fs.readFileSync(path.join(__dirname,'s10-win16.keys'),'ascii').trim().split(/\s+/);
function verify(leaves, root=ROOT, witness=S9, {terminal=true}={}) {
 need(Array.isArray(leaves)&&leaves.length===16&&
      new Set(leaves).size===16&&leaves.every(h=>/^[0-9a-f]{32}$/.test(h)),
      'malformed or incomplete 16-leaf certificate');
 const r = g.board(root,8), w = g.board(witness,9);
 need(g.children(r).has(witness),'illegal S8->S9 witness');
 const actual = g.children(w);
 need(actual.size===16&&leaves.every(h=>actual.has(h)),
      'S9 universal boundary missing/altered');
 let states=0;
 for (const h of leaves) {
  g.board(h,10);
  if (terminal) {
   const result = g.solve10(h);
   need(result.win,'false terminal S10 WIN: '+h);
   states+=result.states;
  }
 }
 for (const p of PLAN_PARENTS) {
  need(g.children(g.board(p,7)).has(root),
       'shared S8 root is not a legal S7 child: '+p);
 }
 need(!PLAN_PARENTS.includes(root),'invalid parent/root levels');
 if (terminal) need(states===914,'3x3 terminal-state regression');
 return {s8:root,verdict:'WIN',s9WinWitness:witness,
         allS10WinLeaves:16,terminalStates:terminal?states:null,
         conditionalS7ParentsWithOneMoreSecuredEdge:2,
         newS7Verdicts:0,newS5Verdicts:0,twoStoneClosures:0,emptyBoard:'UNKNOWN'};
}
if (require.main===module) {
 const leaves=read();
 console.log(JSON.stringify(verify(leaves),null,2));
 if (process.argv.includes('--negative')) {
  const tests=[
   [leaves.slice(1),ROOT,S9],
   [[leaves[0],...leaves.slice(0,-1)],ROOT,S9],
   [[ROOT,...leaves.slice(1)],ROOT,S9],
   [leaves,ROOT,ROOT],
  ];
  for(const [bad,r,w] of tests) {
   let rejected=false;
   try {verify(bad,r,w,{terminal:false});} catch (_) {rejected=true;}
   need(rejected,'altered S8 WIN certificate was accepted');
  }
  console.error('PASS four mutation rejections');
 }
}
module.exports={verify};
