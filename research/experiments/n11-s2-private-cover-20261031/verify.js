#!/usr/bin/env node
'use strict';
// Geometric minimality audit of the 32 S4 LOSS classes in the {60,27} certificate.
// This proves minimality only relative to these 32 classes, not all possible S4s.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../../..');
const SRC='research/experiments/n11-s4-boundary-direct-20261012/output/root-60-27-loss-proof.json';
const PIN='b52b6e2829f960e93393eac8fb930d415c37ac33';
const raw=fs.readFileSync(path.join(ROOT,SRC));
const blob=crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');
assert.equal(blob,PIN,'pinned proof changed');
// Quote 64-bit key halves before JSON.parse, preventing Number precision loss.
const precise=raw.toString('utf8').replace(
  /("(?:key|s4_class)"\s*:\s*\[\s*)(\d+)(\s*,\s*)(\d+)(\s*\])/g,
  '$1"$2"$3"$4"$5');
const proof=JSON.parse(precise);
assert.equal(proof.schema,'n11-reply27-root-loss-move-certificate-v1');
assert.deepEqual(proof.root_stones,[60,27]);
assert.equal(proof.legal_root_moves,119);
assert.equal(proof.root_outcome,'LOSS');
const maps=Array.from({length:8},(_,m)=>Array.from({length:121},(_,i)=>{
  const x=i%11,y=Math.floor(i/11);
  const [u,v]=[[x,y],[10-y,x],[10-x,10-y],[y,10-x],
    [10-x,y],[10-y,10-x],[x,10-y],[y,x]][m];
  return 11*v+u;
}));
function points(pair){
  assert(Array.isArray(pair)&&pair.length===2);
  assert(pair.every(x=>typeof x==='string'&&/^\d+$/.test(x)));
  const lo=BigInt(pair[0]),hi=BigInt(pair[1]);
  assert(lo>=0n&&lo<(1n<<64n)&&hi>=0n&&hi<(1n<<64n));
  const n=lo+(hi<<64n);
  assert.equal(n>>121n,0n);
  return Array.from({length:121},(_,i)=>i).filter(i=>(n>>BigInt(i))&1n);
}
function canon(p){
  let best=null;
  for(const map of maps){
    let n=0n;for(const i of p)n|=1n<<BigInt(map[i]);
    if(best===null||n<best)best=n;
  }
  return best.toString(16).padStart(32,'0');
}
function det4(p){
  const a=p.map(i=>{const x=i%11,y=Math.floor(i/11);return [x*x+y*y,x,y]});
  const b=a.slice(1).map(row=>row.map((v,j)=>v-a[0][j]));
  return b[0][0]*(b[1][1]*b[2][2]-b[1][2]*b[2][1])
       - b[0][1]*(b[1][0]*b[2][2]-b[1][2]*b[2][0])
       + b[0][2]*(b[1][0]*b[2][1]-b[1][1]*b[2][0]);
}
function coverage(p){
  const out=new Set();
  for(const map of maps){
    const a=p.map(i=>map[i]);
    if(a.includes(27)&&a.includes(60))
      for(const i of a)if(i!==27&&i!==60)out.add(i);
  }
  return out;
}
assert.equal(proof.used_s4_loss_classes.length,32);
const classes=proof.used_s4_loss_classes.map(row=>{
  const p=points(row.key);
  assert.equal(p.length,4);assert.notEqual(det4(p),0,'unsafe S4');
  let n=0n;for(const i of p)n|=1n<<BigInt(i);
  const k=n.toString(16).padStart(32,'0');
  assert.equal(canon(p),k,'noncanonical S4');
  assert(Number.isSafeInteger(row.s5_children)&&row.s5_children>0);
  return {key:k,s5:row.s5_children,third:coverage(p)};
});
const byKey=new Map(classes.map(c=>[c.key,c]));
assert.equal(byKey.size,32,'duplicate S4');
const freq=Array(121).fill(0);
for(const c of classes)for(const i of c.third)freq[i]++;
assert.equal(freq[27],0);assert.equal(freq[60],0);
for(let i=0;i<121;i++)if(i!==27&&i!==60)
  assert(freq[i]>0,'uncovered root third move '+i);
assert.equal(proof.third_move_witnesses.length,119);
const seen=new Set();
for(const w of proof.third_move_witnesses){
  const t=w.root_move,f=w.s4_reply_move;
  assert(Number.isInteger(t)&&t>=0&&t<121&&t!==27&&t!==60);
  assert(Number.isInteger(f)&&f>=0&&f<121);
  assert(!seen.has(t),'duplicate third move');seen.add(t);
  const k=canon(points(w.s4_class));
  assert(byKey.has(k)&&byKey.get(k).third.has(t),'bad witness class');
  const a=[60,27,t,f];
  assert.equal(new Set(a).size,4);assert.notEqual(det4(a),0);
  assert.equal(canon(a),k,'bad fourth reply');
}
assert.equal(seen.size,119);
const priv=classes.map(c=>[...c.third].filter(i=>freq[i]===1).length);
assert(priv.every(n=>n>=1),'nonessential class');
for(let skip=0;skip<32;skip++){
  const covered=new Set(classes.flatMap((c,i)=>i===skip?[]:[...c.third]));
  assert(covered.size<119,'deletion did not break coverage');
}
const histogram={};
for(const n of freq)histogram[n]=(histogram[n]||0)+1;
assert.deepEqual(histogram,{'0':2,'1':114,'2':2,'3':2,'13':1});
assert.deepEqual([57,63,93,110,120].map(i=>[i,freq[i]]),
  [[57,2],[63,2],[93,13],[110,3],[120,3]]);
assert.equal(classes.reduce((n,c)=>n+c.s5,0),3297);
console.log(JSON.stringify({
  schema:'n11-s2-private-cover-v1',root:[60,27],
  s4Classes:32,rootThirdMoves:119,privateThirdMoves:114,
  frequencyHistogram:histogram,essentialClasses:32,
  privatePerClassMin:Math.min(...priv),privatePerClassMax:Math.max(...priv),
  fixedClassSetMinCover:32,s4S5BoundaryEdges:3297,
  trust:'solver-trusted S4 LOSS labels; geometric set cover audited independently',
  emptyBoard:'UNKNOWN'
},null,2));