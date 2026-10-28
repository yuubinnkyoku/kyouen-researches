#!/usr/bin/env node
'use strict';
// Independent geometry-only preflight of the frozen post-round10 batch.
// Counts are planning obligations, not terminal WIN/LOSS evidence.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
function structural(p){
  need(p.schema==='n11-post-round10-proof-only-replan-v1'&&
    p.emptyBoard==='UNKNOWN'&&p.conditionalUnprovedEdges===83&&
    p.proofOnlyWin8After===5513,'wrong proof-only scope');
  const keys=p.newSelectedKeys;
  need(Array.isArray(keys)&&keys.length===32&&new Set(keys).size===32,
    'wrong or duplicate S9 selection');
  need(keys.every(h=>typeof h==='string'&&/^[0-9a-f]{32}$/.test(h)),
    'malformed S9 key');
  need(sha(keys.join('\n')+'\n')===p.newSelectionSha256,
    'selection hash mismatch');
  return keys;
}
function audit(p){
  const keys=structural(p),children=new Map(),parents=new Map();
  let edges=0,reverseEdges=0;
  for(let i=0;i<keys.length;i++){
    const h=keys[i],b=g.board(h,9),pp=g.pts(b);
    need(pp.length===9,'incorrect S9 popcount '+h);
    for(let a=0;a<6;a++)for(let c=a+1;c<7;c++)
      for(let d=c+1;d<8;d++)for(let e=d+1;e<9;e++)
        need(ind.det4([pp[a],pp[c],pp[d],pp[e]])!==0,
          'independent S9 safety failure '+h);
    const a=g.children(b),v=ind.children4(h);
    need(same(a,v),'independent S10 boundary mismatch '+h);
    edges+=a.size;
    for(const leaf of a){
      if(!children.has(leaf))children.set(leaf,[]);
      children.get(leaf).push(i);
    }
    const pp8=g.reverse([h]);
    reverseEdges+=pp8.size;
    for(const par of pp8){
      need(g.children(g.board(par,8)).has(h)&&
        ind.children4(par).has(h),'independent S8->S9 incidence '+par);
      if(!parents.has(par))parents.set(par,[]);
      parents.get(par).push(i);
    }
  }
  need(edges===p.legal10Children&&edges===822,
    'S10 child cost mismatch');
  const shared10=[...children].filter(([,owners])=>owners.length>1);
  const shared8=[...parents].filter(([,owners])=>owners.length>1);
  return {schema:'n11-round11-preflight-v1',emptyBoard:'UNKNOWN',
    selectionSha256:p.newSelectionSha256,
    checkedS9:keys.length,independentGeometries:2,
    orderedS10Edges:edges,distinctS10Children:children.size,
    sharedS10Children:shared10.length,
    savedWithinBatchTerminalLeaves:edges-children.size,
    orderedS8PredecessorEdges:reverseEdges,
    distinctS8Predecessors:parents.size,
    sharedS8Predecessors:shared8.length,
    potentialS8Hits:p.potentialCoverage,
    newS9Verdicts:0,newS8Verdicts:0,newTwoStoneClosures:0};
}
function negative(p){
  const reject=(change,label)=>{
    const q=structuredClone(p);change(q);let failed=false;
    try{structural(q)}catch(_){failed=true}
    need(failed,'forged '+label+' accepted');
  };
  reject(q=>q.newSelectedKeys[0]=q.newSelectedKeys[1],'duplicate');
  reject(q=>q.newSelectedKeys[0]='0'.repeat(32),'key');
  reject(q=>q.newSelectionSha256='0'.repeat(64),'hash');
  reject(q=>q.emptyBoard='WIN','empty-board verdict');
}
function run(){
  const p=read('next-plan.json');
  negative(p);
  const result=audit(p);
  const fixed=path.join(__dirname,'preflight.json');
  if(fs.existsSync(fixed))need(
    JSON.stringify(read('preflight.json'))===JSON.stringify(result),
    'frozen independent preflight mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run,audit,structural};
