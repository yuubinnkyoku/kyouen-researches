#!/usr/bin/env node
'use strict';
// Bounded independent preflight of the frozen post-round9 batch.
// Potential S8 hits and unfinished searches are not winning proofs.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need=(x,msg)=>{if(!x)throw Error(msg)};
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const file=path.join(__dirname,'next-plan.json');
const SHARED='00006000100020821080000000000030';

function structural(p){
  need(p.schema==='n11-post-round9-proof-only-replan-v1'&&
    p.emptyBoard==='UNKNOWN','wrong plan scope');
  const keys=p.newSelectedKeys;
  need(Array.isArray(keys)&&keys.length===32&&new Set(keys).size===32,
    'wrong/duplicate S9 selection');
  need(sha(keys.join('\n')+'\n')===p.newSelectionSha256,
    'S9 selection hash mismatch');
  need(keys.every(h=>typeof h==='string'&&/^[0-9a-f]{32}$/.test(h)),
    'malformed S9 key');
  return keys;
}
function audit(p){
  const keys=structural(p),children=new Map(),parents=new Map();
  let edges=0,reverseEdges=0;
  for(let i=0;i<keys.length;i++){
    const h=keys[i],b=g.board(h,9),pp=g.pts(b);
    // 4x4 Bareiss is independent of the 3x3 difference determinant.
    for(let a=0;a<6;a++)for(let c=a+1;c<7;c++)
      for(let d=c+1;d<8;d++)for(let e=d+1;e<9;e++)
        need(ind.det4([pp[a],pp[c],pp[d],pp[e]])!==0,
          'independent S9 safety failure '+h);
    const a=g.children(b),v=ind.children4(h);
    need(same(a,v),'3x3/4x4 S10 boundary mismatch '+h);
    edges+=a.size;
    for(const leaf of a){
      if(!children.has(leaf))children.set(leaf,[]);
      children.get(leaf).push(i);
    }
    const pp8=g.reverse([h]);
    need(pp8.size===9,'unexpected S8 predecessor count '+h);
    reverseEdges+=pp8.size;
    for(const par of pp8){
      need(g.children(g.board(par,8)).has(h)&&
        ind.children4(par).has(h),'independent S8->S9 incidence '+par);
      if(!parents.has(par))parents.set(par,[]);
      parents.get(par).push(i);
    }
  }
  const shared=[...children].filter(([,owners])=>owners.length>1);
  const shared8=[...parents].filter(([,owners])=>owners.length>1);
  need(edges===830&&p.legal10Children===830,'S10 child cost mismatch');
  need(children.size===829&&shared.length===1&&
    shared[0][0]===SHARED&&shared[0][1].length===2,
    'S10 sharing regression');
  need(reverseEdges===288&&parents.size===286&&
    shared8.length===2&&shared8.every(([,owners])=>owners.length===2),
    'S8 predecessor overlap regression');
  return {checkedS9:keys.length,independentGeometries:2,
    orderedS10Edges:edges,distinctS10Children:children.size,
    sharedS10Children:shared.length,sharedS10Key:shared[0][0],
    orderedS8PredecessorEdges:reverseEdges,distinctS8Predecessors:parents.size,
    sharedS8Predecessors:shared8.length,
    measuredWithinBatchLeafReuse:edges-children.size,
    certifiedNewWin9:0,certifiedNewWin8:0,newTwoStoneClosures:0,
    emptyBoard:'UNKNOWN'};
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
  reject(q=>q.emptyBoard='WIN','empty-board claim');
}
if(require.main===module){
  const p=JSON.parse(fs.readFileSync(file,'utf8'));
  negative(p);
  console.log(JSON.stringify(audit(p),null,2));
}
module.exports={audit,structural};
