#!/usr/bin/env node
'use strict';
// Independent 3x3 integer geometry, complete S9/S10 boundary and terminal check.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ROOT='00000000000040001000044400830000';
function need(x,msg){if(!x)throw Error(msg);}
function verify(keys,{terminal=true,full=false,dump=false}={}){
  need(keys.length===16&&new Set(keys).size===16,'wrong/duplicate leaf count');
  const root=g.board(ROOT,8);
  const obligations=g.children(root);need(obligations.size===31,'wrong S9 boundary');
  const boundary=new Map();
  for(const s9 of obligations){
    const b=g.board(s9,9);
    for(const h of g.children(b)){
      if(!boundary.has(h))boundary.set(h,new Set());boundary.get(h).add(s9);
    }
  }
  need(boundary.size===378,'wrong S10 boundary');
  need([...boundary.values()].every(s=>s.size===2),'leaf covers more/less than two');
  const covered=new Set();let states=0;
  for(const h of keys){
    need(/^[0-9a-f]{32}$/.test(h)&&boundary.has(h),'invalid S10 leaf');
    g.board(h,10);
    for(const s9 of boundary.get(h))covered.add(s9);
    if(terminal){const v=g.solve10(h);need(!v.win,'false LOSS '+h);states+=v.states;}
  }
  need(covered.size===31,'uncovered S9 obligation');
  if(terminal)need(states===11495,'terminal state regression');
  const out={s9Obligations:31,s10Boundary:378,maxCoveragePerLeaf:2,
    minimumLeaves:16,selectedLeaves:16,terminalVerified:terminal?16:0,
    terminalStates:terminal?states:null,emptyBoard:'UNKNOWN'};
  if(full||dump){let loss=0,win=0,allStates=0,rows=[];
    for(const h of boundary.keys()){
      const v=g.solve10(h);if(v.win)win++;else loss++;allStates+=v.states;
      if(dump)rows.push([h,v.win?'WIN':'LOSS',v.states,v.legal].join('\t'));
    }
    need(loss===81&&win===297&&allStates===175066,'full boundary regression');
    out.fullBoundary={loss,win,states:allStates};
    if(dump)out.rows=rows.sort();
  }
  return out;
}
module.exports={verify};
if(require.main===module){
  const keys=fs.readFileSync(path.join(__dirname,'leaves16.keys'),'utf8').trim().split(/\s+/);
  const dump=process.argv.includes('--dump');
  const result=verify(keys,{full:process.argv.includes('--full'),dump});
  if(dump)process.stdout.write(result.rows.join('\n')+'\n');
  else console.log(JSON.stringify(result,null,2));
  if(process.argv.includes('--negative')){
    const bad=[keys.slice(0,-1),[...keys.slice(0,-1),keys[0]],
      [...keys.slice(0,-1),'0'.repeat(32)],[...keys.slice(0,-1),ROOT]];
    for(const rows of bad){let rejected=false;
      try{verify(rows,{terminal:false});}catch(_){rejected=true;}
      need(rejected,'malformed proof accepted');
    }
    console.error('PASS four malformed certificates rejected');
  }
}
