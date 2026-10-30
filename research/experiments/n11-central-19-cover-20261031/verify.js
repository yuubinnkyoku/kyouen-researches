#!/usr/bin/env node
'use strict';
// Independent integer-geometry audit of 19 central-reply S4 set-cover
// primal/dual certificates. No solver or S5 verdicts are trusted here.
const fs = require('node:fs');
const zlib = require('node:zlib');
const assert = require('node:assert/strict');
const data = JSON.parse(zlib.gunzipSync(Buffer.from(
  fs.readFileSync(__dirname + '/certificate.json.gz.b64','utf8').trim(),
  'base64')).toString('utf8'));
const REPS=[16,38,49,24,0,26,48,12,25,3,13,2,14,5,15,4,1,37,36];
const hex=n=>n.toString(16).padStart(32,'0');
const trans=Array.from({length:8},(_,j)=>Array.from({length:121},(_,i)=>{
  const x=i%11,y=Math.floor(i/11);
  const [u,v]=[[x,y],[10-y,x],[10-x,10-y],[y,10-x],
    [10-x,y],[10-y,10-x],[x,10-y],[y,x]][j];
  return 11*v+u;
}));
function points(k){
  assert.match(k,/^[0-9a-f]{32}$/);
  const n=BigInt('0x'+k); assert.equal(n>>121n,0n);
  const p=[];for(let i=0;i<121;i++)if(n&(1n<<BigInt(i)))p.push(i);
  return p;
}
function canonical(p){
  let best=null;
  for(const t of trans){let n=0n;for(const x of p)n|=1n<<BigInt(t[x]);
    if(best===null||n<best)best=n;}
  return hex(best);
}
// Full 4x4 determinant, independent of the 3x3-difference generator.
function det4(p){
  const a=p.map(i=>{const x=i%11,y=Math.floor(i/11);
    return [x*x+y*y,x,y,1];});
  let ans=0;
  function rec(row,used,sign,prod){
    if(row===4){ans+=sign*prod;return;}
    for(let c=0;c<4;c++)if(!(used&(1<<c))){
      let flips=0;for(let k=c+1;k<4;k++)if(used&(1<<k))flips++;
      rec(row+1,used|(1<<c),flips%2?-sign:sign,prod*a[row][c]);
    }
  }
  rec(0,0,1,1);return ans;
}
function cover(p,a,b){
  let mask=0n;
  for(const t of trans){
    const q=p.map(x=>t[x]);
    if(q.includes(a)&&q.includes(b))
      for(const x of q)if(x!==a&&x!==b)mask|=1n<<BigInt(x);
  }
  return mask;
}
function verifyRoot(row){
  const a=row.first,b=row.reply;
  assert.equal(b,60);assert.equal(row.third_moves,119);
  assert.equal(row.dual_denominator,2);
  const thirds=Array.from({length:121},(_,i)=>i).filter(i=>i!==a&&i!==b);
  const universe=thirds.reduce((m,i)=>m|(1n<<BigInt(i)),0n);
  const dual=new Map(Object.entries(row.dual_numerators).map(([k,v])=>[Number(k),v]));
  for(const [p,v] of dual){assert(thirds.includes(p));assert.equal(v,1);}
  assert.equal(dual.size,row.minimum_classes*2);
  const selected=new Set(row.primal_s4_classes);
  assert.equal(selected.size,row.minimum_classes);
  const classes=new Map();
  for(let c=0;c<121;c++)if(c!==a&&c!==b)
    for(let d=c+1;d<121;d++)if(d!==a&&d!==b){
      const p=[a,b,c,d];if(det4(p)===0)continue;
      const k=canonical(p);
      if(!classes.has(k))classes.set(k,cover(p,a,b));
    }
  assert.equal(classes.size,row.legal_s4_classes);
  let used=0n;
  for(const k of selected){
    const p=points(k);assert.equal(p.length,4);assert.equal(canonical(p),k);
    assert.notEqual(det4(p),0);assert(classes.has(k),'selected class unreachable');
    used|=classes.get(k);
  }
  assert.equal(used,universe,'primal misses a third move');
  let maxDual=0;
  for(const [k,m] of classes){
    let w=0;
    for(const p of dual.keys())if(m&(1n<<BigInt(p)))w++;
    if(w>maxDual)maxDual=w;
    assert(w<=2,'dual inequality violated for '+k);
  }
  assert.equal(maxDual,2);
  return {first:a,reply:b,classes:classes.size,minimum:row.minimum_classes,
    dualPositive:dual.size,checkedConstraints:classes.size};
}
assert.equal(data.schema,'n11-central-19-geometric-s4-cover-v1');
assert.equal(data.outcome,'UNKNOWN');assert.equal(data.board,11);
assert.deepEqual(data.roots.map(x=>x.first),REPS);
const results=data.roots.map(verifyRoot);
assert.equal(results.filter(x=>x.minimum===31).length,9);
assert.equal(results.filter(x=>x.minimum===56).length,10);
assert.equal(results.reduce((s,x)=>s+x.checkedConstraints,0),
  data.roots.reduce((s,x)=>s+x.legal_s4_classes,0));
// Negative controls must be rejected by the same verifier.
const missing={...data.roots[0],
  primal_s4_classes:data.roots[0].primal_s4_classes.slice(1)};
assert.throws(()=>verifyRoot(missing));
const badDual={...data.roots[0],dual_numerators:{
  ...data.roots[0].dual_numerators,
  [data.roots[0].first]:1}};
assert.throws(()=>verifyRoot(badDual));
console.log(JSON.stringify({schema:data.schema,roots:results.length,
  minimum31:9,minimum56:10,classesChecked:results.reduce((s,x)=>s+x.checkedConstraints,0),
  allPrimalAndDualCertificatesVerified:true,negativeControlsPassed:true,
  note:'Geometry-only S4 class covers, not S4 LOSS proofs; n11 empty board UNKNOWN'},null,2));
