#!/usr/bin/env node
'use strict';
// Bounded, proof-directed survey of 9-stone witnesses for the 266
// still-unproved 8-stone obligations in the saved conditional 14-root plan.
// This is a discovery experiment, NOT a certificate.
const fs=require('node:fs'),path=require('node:path');
const EXP=path.resolve(__dirname,'..');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const p14=require('../n11-s9-degree2-terminal-20261027/verify.js');
const p13=require('../n11-s9-degree2-short-terminal-20261027/verify.js');
const p46=require('../n11-s9-short46-terminal-20261027/verify.js');
const p12=require('../n11-s9-short18-terminal-20261027/verify.js');
const p55=require('../n11-s9-n19-terminal-20261027/verify.js');
const p80=require('../n11-s9-n20-terminal-20261027/verify.js');
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8');
const keys=p=>read(p).trim().split(/\s+/);
const assert=(ok,msg)=>{if(!ok)throw Error(msg);};
const plan=keys('n11-s5-pair-cover-20261026/s7-plan14-remaining.keys');
const plan8=new Set(plan.flatMap(h=>[...g.children(g.board(h,7))]));
const {win,loss}=base.inventory();
const c5=JSON.parse(read('n11-s9-shared-plan14-20261027/certificate.json'));
const c11=JSON.parse(read('n11-s9-shared-plan14-eleven-win-20261027/certificate.json'));
const old9=[...c5.witnesses,...c11.witnesses].map(x=>x.s9_win)
  .concat(p14.parse(read('n11-s9-degree2-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  p13.parse(read('n11-s9-degree2-short-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  p46.parse(read('n11-s9-short46-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  p12.parse(read('n11-s9-short18-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  p55.parse(read('n11-s9-n19-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  p80.parse(read('n11-s9-n20-terminal-20261027/certificate.tsv')).map(x=>x.s9));
const prior9=new Set(old9);
const before=new Set([...win,'00000000000000821090a00000000020',...g.reverse(old9)]);
const missing=new Set([...plan8].filter(h=>!before.has(h)));
assert(plan.length===14&&plan8.size===547&&before.size===4011&&
  missing.size===266&&[...before].every(h=>!loss.has(h)),
  'upstream certified frontier changed');
const candidates=new Map();
for(const parent of missing){
  for(const s9 of g.children(g.board(parent,8))){
    if(prior9.has(s9))continue;
    let parents=candidates.get(s9);
    if(!parents){parents=new Set();candidates.set(s9,parents);}
    parents.add(parent);
  }
}
const selected=[];
for(const [s9,parents] of candidates){
  if(parents.size<2)continue;
  const c=g.children(g.board(s9,9));
  if(c.size===21)selected.push({s9,parents:[...parents],children:[...c]});
}
selected.sort((a,b)=>b.parents.length-a.parents.length||
  a.s9.localeCompare(b.s9));
const limit=Math.min(300,selected.length);
const leafCache=new Map(),wins=[];
let tested=0,states=0;
for(const row of selected.slice(0,limit)){
  tested++;let sum=0,all=true;
  for(const leaf of row.children){
    let r=leafCache.get(leaf);
    if(!r){r=g.solve10(leaf);leafCache.set(leaf,r);states+=r.states;}
    if(!r.win){all=false;break;}
    sum+=r.states;
  }
  if(all)wins.push({s9:row.s9,leaves:21,states:sum,parents:row.parents});
}
const gained=new Set(wins.flatMap(x=>x.parents));
assert([...gained].every(h=>missing.has(h)),'invalid gain');
console.log(JSON.stringify({schema:'n11-targeted-21-child-survey-v1',
  initialUnprovedS8:missing.size,allS9Candidates:candidates.size,
  degree2PlusN21:selected.length,tested,winningS9:wins.length,
  provenS8Gain:gained.size,distinctS10LeavesSolved:leafCache.size,
  statesComputed:states,rootClosures:0,emptyBoard:'UNKNOWN'}));
console.log('CERT_BEGIN');
for(const w of wins)console.log(w.s9+' '+w.leaves+' '+w.states);
console.log('CERT_END');
