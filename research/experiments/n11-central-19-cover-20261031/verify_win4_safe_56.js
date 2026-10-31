'use strict';
// Verify WIN4-safe 56-class covers with independent 4x4 integer geometry.
// The imported audit fail-closes on pinned cache hashes and WIN/LOSS conflicts.
const fs=require('node:fs'),zlib=require('node:zlib'),assert=require('node:assert/strict');
const {witnesses,canonical,points,maps}=require('./audit_win4_exclusion');
const dir=__dirname;
const cert=JSON.parse(fs.readFileSync(dir+'/win4-safe-56-certificate.json','utf8'));
const prior=JSON.parse(zlib.gunzipSync(Buffer.from(
  fs.readFileSync(dir+'/certificate.json.gz.b64','utf8').trim(),'base64')));
const REPS=[26,25,3,13,2,14,15,4,1,37];
const EXCLUDED=[35,9,47,21,29,15,43,16,11,32];
// Full 4x4 determinant (the generator and cache audit use a 3x3 difference).
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
  for(const t of maps){
    const q=p.map(x=>t[x]);
    if(q.includes(a)&&q.includes(b))
      for(const x of q)if(x!==a&&x!==b)mask|=1n<<BigInt(x);
  }
  return mask;
}
function classesFor(a){
  const classes=new Map();
  for(let c=0;c<121;c++)if(c!==a&&c!==60)
    for(let d=c+1;d<121;d++)if(d!==a&&d!==60){
      const p=[a,60,c,d];if(det4(p)===0)continue;
      const k=canonical(p);
      if(!classes.has(k))classes.set(k,cover(p,a,60));
    }
  return classes;
}
function checkSelected(row,classes){
  assert.equal(row.reply,60);assert.equal(row.third_moves,119);
  assert.equal(row.minimum_classes,56);
  assert.equal(row.primal_s4_classes.length,56);
  const selected=new Set(row.primal_s4_classes);
  assert.equal(selected.size,56);
  let used=0n;
  for(const k of selected){
    const p=points(k);
    assert.equal(p.length,4);assert.equal(canonical(p),k);
    assert.notEqual(det4(p),0);assert(classes.has(k),'unreachable class');
    assert(!witnesses.has(k),'known WIN4 used: '+k);
    used|=classes.get(k);
  }
  const universe=((1n<<121n)-1n)&~(1n<<BigInt(row.first))&~(1n<<60n);
  assert.equal(used,universe,'uncovered third move');
}
function checkDual(primal,classes){
  assert.equal(primal.minimum_classes,56);
  assert.equal(primal.dual_denominator,2);
  const dual=Object.entries(primal.dual_numerators).map(([k,v])=>[Number(k),v]);
  assert.equal(dual.length,112);
  for(const [x,v] of dual){
    assert(Number.isInteger(x)&&x>=0&&x<121&&x!==primal.first&&x!==60);
    assert.equal(v,1);
  }
  for(const [k,m] of classes){
    let w=0;
    for(const [x] of dual)if(m&(1n<<BigInt(x)))w++;
    assert(w<=2,'dual inequality: '+k);
  }
}
assert.equal(cert.schema,'n11-central-win4-safe-s4-cover-v1');
assert.equal(cert.board,11);assert.equal(cert.outcome,'UNKNOWN');
assert.equal(prior.schema,'n11-central-19-geometric-s4-cover-v1');
assert.deepEqual(cert.roots.map(r=>r.first),REPS);
assert.equal(cert.cache_sources.length,2);
assert.equal(cert.cache_sources[0].blob_sha,'2dccf42b92337cbcbfb62ea5c77db487b1ad8ead');
assert.equal(cert.cache_sources[1].blob_sha,'9887a18c0788d26507be7e8e191c26817634a6b6');
assert.equal(witnesses.size,549);
const result=[];
for(let i=0;i<REPS.length;i++){
  const row=cert.roots[i],a=REPS[i];assert.equal(row.first,a);
  const classes=classesFor(a);
  assert.equal(classes.size,row.legal_s4_classes);
  const blocked=[...classes.keys()].filter(k=>witnesses.has(k));
  assert.equal(blocked.length,row.excluded_win4_classes);
  assert.equal(blocked.length,EXCLUDED[i]);
  checkSelected(row,classes);
  const old=prior.roots.find(x=>x.first===a);
  assert(old);checkDual(old,classes);
  // The same verifier must reject a known-WIN4 witness and an incomplete cover.
  const bad={...row,primal_s4_classes:[blocked[0],...row.primal_s4_classes.slice(1)]};
  assert.throws(()=>checkSelected(bad,classes),/known WIN4/);
  const missing={...row,primal_s4_classes:row.primal_s4_classes.slice(1)};
  assert.throws(()=>checkSelected(missing,classes));
  result.push({first:a,minimum:56,selected:56,excluded:blocked.length,
    legalClasses:classes.size,thirdMovesCovered:119});
}
console.log(JSON.stringify({schema:cert.schema,roots:result,verifiedRoots:10,
  selectedClasses:560,blockedWin4:549,geometryConstrainedOptimum56:true,
  negativeControlsPassed:true,emptyBoard:'UNKNOWN',
  note:'S4 LOSS verdicts are NOT proved by this geometric cover.'},null,2));
