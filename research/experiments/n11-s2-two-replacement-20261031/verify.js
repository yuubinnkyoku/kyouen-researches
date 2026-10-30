#!/usr/bin/env node
'use strict';
// Exhaustive 2-new/3-old S4 cover substitution audit for root {60,27}.
// Geometry is exact; S5 cache labels are solver-trusted, not terminal proofs.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../../..');
const SOURCES={
  proof:['research/experiments/n11-s4-boundary-direct-20261012/output/root-60-27-loss-proof.json','b52b6e2829f960e93393eac8fb930d415c37ac33'],
  frozen:['research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache','2dccf42b92337cbcbfb62ea5c77db487b1ad8ead'],
  corpus:['research/experiments/n11-boundary-recovery-20261006/output/post-23b52acf-after-round4-s6-escalation-s5-cache-corpus-union.cache','9887a18c0788d26507be7e8e191c26817634a6b6']
};
function pinned([file,sha]){
  const b=fs.readFileSync(path.join(ROOT,file));
  const got=crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
  assert.equal(got,sha,'source blob changed: '+file);
  return b.toString('utf8');
}
const hex=n=>n.toString(16).padStart(32,'0');
const maps=Array.from({length:8},(_,m)=>Array.from({length:121},(_,i)=>{
  const x=i%11,y=Math.floor(i/11);
  const [u,v]=[[x,y],[10-y,x],[10-x,10-y],[y,10-x],
    [10-x,y],[10-y,10-x],[x,10-y],[y,x]][m];
  return 11*v+u;
}));
function points(k){
  assert.match(k,/^[0-9a-f]{32}$/);
  const n=BigInt('0x'+k);
  assert.equal(n>>121n,0n);
  return Array.from({length:121},(_,i)=>i).filter(i=>Boolean((n>>BigInt(i))&1n));
}
function canon(p){
  let best=null;
  for(const m of maps){
    let n=0n;for(const i of p)n|=1n<<BigInt(m[i]);
    if(best===null||n<best)best=n;
  }
  return hex(best);
}
function det4(p){
  const a=p.map(i=>{const x=i%11,y=Math.floor(i/11);return [x*x+y*y,x,y]});
  const b=a.slice(1).map(row=>row.map((v,j)=>v-a[0][j]));
  return b[0][0]*(b[1][1]*b[2][2]-b[1][2]*b[2][1])
       - b[0][1]*(b[1][0]*b[2][2]-b[1][2]*b[2][0])
       + b[0][2]*(b[1][0]*b[2][1]-b[1][1]*b[2][0]);
}
function safe(p){
  for(let a=0;a<p.length;a++)for(let b=a+1;b<p.length;b++)
    for(let c=b+1;c<p.length;c++)for(let d=c+1;d<p.length;d++)
      if(det4([p[a],p[b],p[c],p[d]])===0)return false;
  return true;
}
function cover(p){
  let mask=0n;
  for(const m of maps){
    const a=p.map(i=>m[i]);
    if(a.includes(27)&&a.includes(60))
      for(const i of a)if(i!==27&&i!==60)mask|=1n<<BigInt(i);
  }
  return mask;
}
function parseCache(raw){
  const out=new Map();
  for(const line of raw.split(/\r?\n/)){
    if(!line||line.startsWith('#'))continue;
    const f=line.split(',');
    assert.equal(f.length,6);assert.equal(f[0],'s5verdict');
    assert.equal(f[3],'5');assert(['1','2'].includes(f[4]));
    assert.match(f[5],/^\d+$/);
    const lo=BigInt(f[1]),hi=BigInt(f[2]);
    assert(lo>=0n&&lo<2n**64n&&hi>=0n&&hi<2n**64n);
    const k=hex(lo+(hi<<64n));
    assert.equal(points(k).length,5);
    assert(!out.has(k),'duplicate S5 key '+k);
    out.set(k,Number(f[4]));
  }
  return out;
}
function main(){
  const raw=pinned(SOURCES.proof);
  // JSON decimal 64-bit halves must be quoted before JSON.parse.
  const precise=raw.replace(/("(?:key|s4_class)"\s*:\s*\[\s*)(\d+)(\s*,\s*)(\d+)(\s*\])/g,
    '$1"$2"$3"$4"$5');
  const proof=JSON.parse(precise);
  assert.deepEqual(proof.root_stones,[60,27]);
  assert.equal(proof.root_outcome,'LOSS');
  assert.equal(proof.used_s4_loss_classes.length,32);
  const known=proof.used_s4_loss_classes.map(row=>{
    const pair=row.key;
    assert(pair.length===2&&pair.every(x=>typeof x==='string'));
    const lo=BigInt(pair[0]),hi=BigInt(pair[1]);
    assert(lo>=0n&&lo<2n**64n&&hi>=0n&&hi<2n**64n);
    const k=hex(lo+(hi<<64n)),p=points(k);
    assert.equal(p.length,4);assert(safe(p));assert.equal(canon(p),k);
    return {k,c:cover(p)};
  });
  const knownKeys=new Set(known.map(x=>x.k));
  assert.equal(knownKeys.size,32);
  const full=known.reduce((a,x)=>a|x.c,0n);
  assert.equal(full.toString(2).replace(/0/g,'').length,119);
  const priv=known.map((x,i)=>x.c&~known.reduce((a,y,j)=>i===j?a:a|y.c,0n));
  assert(priv.every(x=>x!==0n),'known S4 class is not essential');
  const all=new Map();
  for(let t=0;t<121;t++){
    if(t===27||t===60)continue;
    for(let f=t+1;f<121;f++){
      if(f===27||f===60)continue;
      const p=[60,27,t,f];
      if(det4(p)===0)continue;
      const k=canon(p);
      if(!all.has(k))all.set(k,cover(p));
    }
  }
  assert.equal(all.size,3384);
  const cand=[...all].filter(([k])=>!knownKeys.has(k)).map(([k,c])=>({k,c}));
  assert.equal(cand.length,3352);
  // Reuse a precomputed cover of the other 29 known classes for each triple.
  const remain=new Map();
  for(let i=0;i<32;i++)for(let j=i+1;j<32;j++)for(let k=j+1;k<32;k++){
    let mask=0n;
    for(let a=0;a<32;a++)if(a!==i&&a!==j&&a!==k)mask|=known[a].c;
    remain.set(i+','+j+','+k,mask);
  }
  const pairs=[];let prechecked=0;
  for(let i=0;i<cand.length;i++)for(let j=i+1;j<cand.length;j++){
    const c=cand[i].c|cand[j].c;
    const eligible=[];
    for(let a=0;a<32;a++)if((priv[a]&~c)===0n)eligible.push(a);
    if(eligible.length<3)continue;
    prechecked++;
    for(let a=0;a<eligible.length;a++)for(let b=a+1;b<eligible.length;b++)
      for(let d=b+1;d<eligible.length;d++){
        const x=eligible[a],y=eligible[b],z=eligible[d];
        if((remain.get(x+','+y+','+z)|c)===full)
          pairs.push({i,j,removed:[x,y,z]});
      }
  }
  assert.equal(prechecked,875);
  assert.equal(pairs.length,548);
  const frozen=parseCache(pinned(SOURCES.frozen));
  const corpus=parseCache(pinned(SOURCES.corpus));
  assert.equal(frozen.size,5851);assert.equal(corpus.size,5700);
  const merged=new Map(frozen);
  for(const [k,v] of corpus){
    if(merged.has(k))assert.equal(merged.get(k),v,'WIN/LOSS conflict '+k);
    else merged.set(k,v);
  }
  const selected=new Set(pairs.flatMap(x=>[x.i,x.j]));
  assert.equal(selected.size,313);
  const statuses=new Map();
  for(const idx of selected){
    const p=points(cand[idx].k),children=new Set();
    for(let t=0;t<121;t++)if(!p.includes(t)&&safe([...p,t]))
      children.add(canon([...p,t]));
    let win=0,loss=0,unknown=0;
    for(const k of children){
      const v=merged.get(k);
      if(v===1)win++;else if(v===2)loss++;else unknown++;
    }
    assert.equal(win+loss+unknown,children.size);
    statuses.set(idx,{win,loss,unknown,children});
  }
  const eligiblePairs=pairs.filter(x=>statuses.get(x.i).win===0&&statuses.get(x.j).win===0);
  const ranked=eligiblePairs.map(x=>{
    const a=statuses.get(x.i),b=statuses.get(x.j);
    const unknown=new Set([...a.children,...b.children].filter(k=>!merged.has(k)));
    return {new:[cand[x.i].k,cand[x.j].k],removed:x.removed.map(i=>known[i].k),
      unknownUnion:unknown.size,unknownEach:[a.unknown,b.unknown],
      childrenEach:[a.children.size,b.children.size]};
  }).sort((a,b)=>a.unknownUnion-b.unknownUnion||a.new.join('').localeCompare(b.new.join('')));
  assert.equal([...selected].filter(i=>statuses.get(i).win>0).length,97);
  assert.equal(eligiblePairs.length,174);
  assert.equal(ranked[0].unknownUnion,185);
  assert.deepEqual(ranked[0].new,
    ['00000000000000009100000000000400','00000000000000001200000018000000']);
  // Every emitted candidate really covers all 119 third moves after the swap.
  for(const row of ranked.slice(0,10)){
    let m=0n;
    for(const k of row.new)m|=all.get(k);
    for(const x of known)if(!row.removed.includes(x.k))m|=x.c;
    assert.equal(m,full,'invalid suggested cover');
  }

  // Count *all distinct S5 dependency roots*, not just the unclassified new
  // children. This is a conditional proof-plan cost, not a terminal proof.
  const knownChildren=new Map(known.map(({k})=>{
    const p=points(k),out=new Set();
    for(let t=0;t<121;t++)if(!p.includes(t)&&safe([...p,t]))
      out.add(canon([...p,t]));
    return [k,out];
  }));
  const originalS5=new Set([...knownChildren.values()].flatMap(x=>[...x]));
  assert.equal(originalS5.size,2995);
  for(const k of originalS5)
    assert.equal(merged.get(k),2,'baseline S5 must be cached LOSS: '+k);
  const candidateIndex=new Map(cand.map((x,i)=>[x.k,i]));
  function candidateStatus(k){
    const idx=candidateIndex.get(k);
    assert.notEqual(idx,undefined);
    if(!statuses.has(idx)){
      const p=points(k),children=new Set();
      for(let t=0;t<121;t++)if(!p.includes(t)&&safe([...p,t]))
        children.add(canon([...p,t]));
      let win=0,loss=0,unknown=0;
      for(const c of children){
        const v=merged.get(c);
        if(v===1)win++;else if(v===2)loss++;else unknown++;
      }
      statuses.set(idx,{win,loss,unknown,children});
    }
    return statuses.get(idx);
  }
  function dependencyCost(row){
    const removed=new Set(row.removed),final=new Set(),newChildren=new Set();
    for(const [k,children] of knownChildren)if(!removed.has(k))
      for(const child of children)final.add(child);
    for(const k of row.new){
      const st=candidateStatus(k);
      assert.equal(st.win,0,'known WIN child refutes candidate LOSS');
      for(const child of st.children){newChildren.add(child);final.add(child);}
    }
    const unknownUnion=[...newChildren].filter(k=>!merged.has(k)).length;
    return {...row,unknownUnion,distinctS5:final.size,
      removedOldS5:[...originalS5].filter(k=>!final.has(k)).length,
      introducedS5:[...final].filter(k=>!originalS5.has(k)).length};
  }
  // Earlier one-new/two-old alternatives are re-enumerated, rather than
  // trusting the 2026-10-17 report's best value.
  const oneNew=[];
  for(let i=0;i<cand.length;i++){
    const eligible=[];
    for(let a=0;a<32;a++)if((priv[a]&~cand[i].c)===0n)
      eligible.push(a);
    for(let a=0;a<eligible.length;a++)for(let b=a+1;b<eligible.length;b++){
      const x=eligible[a],y=eligible[b];
      let mask=cand[i].c;
      for(let j=0;j<32;j++)if(j!==x&&j!==y)mask|=known[j].c;
      if(mask===full)
        oneNew.push({new:[cand[i].k],removed:[known[x].k,known[y].k]});
    }
  }
  assert.equal(oneNew.length,4);
  const viableOne=oneNew.filter(row=>candidateStatus(row.new[0]).win===0)
    .map(dependencyCost).sort((a,b)=>a.distinctS5-b.distinctS5);
  assert.equal(viableOne.length,1);
  assert.equal(viableOne[0].unknownUnion,94);
  assert.equal(viableOne[0].distinctS5,2939);
  const byDistinct=ranked.map(row=>{
    const x=dependencyCost(row);
    assert.equal(x.unknownUnion,row.unknownUnion);
    return x;
  }).sort((a,b)=>a.distinctS5-b.distinctS5||
      a.unknownUnion-b.unknownUnion||
      a.new.join('').localeCompare(b.new.join('')));
  assert.equal(byDistinct.length,174);
  assert.equal(byDistinct[0].distinctS5,2930);
  assert.equal(byDistinct[0].unknownUnion,189);
  assert.equal(byDistinct[0].removedOldS5,267);
  assert.equal(byDistinct[0].introducedS5,202);
  assert.deepEqual(byDistinct[0].new,[
    '00000000000000401000000008000400',
    '00000000000000009100000000000080']);
  assert.equal(byDistinct.filter(x=>x.distinctS5<2939).length,6);
  console.log(JSON.stringify({
    schema:'n11-s2-two-new-three-old-cover-audit-v1',root:[60,27],
    geometricS4Classes:all.size,knownLoss4:32,newCandidateClasses:cand.length,
    geometricPairsReplacingThree:548,distinctCandidatesInPairs:313,
    candidateClassesWithCachedWIN5:97,unrefutedCandidateClasses:216,
    pairsWithoutKnownWIN5:eligiblePairs.length,
    minimumUnclassifiedDistinctS5:ranked[0].unknownUnion,
    top:ranked.slice(0,10),
    conditionalDependencyComparison:{
      baselineDistinctS5:originalS5.size,
      geometricOneNewTwoOld:oneNew.length,
      viableOneNewTwoOld:viableOne.length,
      bestOneNewTwoOld:viableOne[0],
      viableTwoNewThreeOld:byDistinct.length,
      bestTwoNewThreeOld:byDistinct[0],
      twoNewPlansWithFewerDistinctS5ThanOneNew:byDistinct.filter(x=>x.distinctS5<viableOne[0].distinctS5).length,
      note:'Conditional only: new S4 LOSS and unknown S5 LOSS are unproved; distinct S5 roots are not terminal DAG size'
    },
    trust:'S5 verdicts solver-trusted; UNKNOWN is not LOSS',
    emptyBoard:'UNKNOWN'
  },null,2));
}
main();
