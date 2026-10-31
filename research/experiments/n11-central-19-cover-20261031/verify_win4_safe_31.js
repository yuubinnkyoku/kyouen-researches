'use strict';
// Independent 4x4 audit of four untouched and one repaired 31-class covers.
// These are geometric covers avoiding known WIN4, NOT S4 LOSS certificates.
const fs=require('node:fs'),zlib=require('node:zlib'),assert=require('node:assert/strict');
const {witnesses,canonical,points,maps}=require('./audit_win4_exclusion');
const data=JSON.parse(zlib.gunzipSync(Buffer.from(
  fs.readFileSync(__dirname+'/certificate.json.gz.b64','utf8').trim(),'base64')));
const patch=JSON.parse(fs.readFileSync(__dirname+'/win4-safe-31-repair.json','utf8'));
const REPS=[38,0,5,36,48],EXCLUDED=[30,3,21,21,112];
function det4(p){
  const a=p.map(i=>{const x=i%11,y=Math.floor(i/11);return[x*x+y*y,x,y,1]});
  let sum=0;
  function go(r,used,sign,prod){
    if(r===4){sum+=sign*prod;return}
    for(let c=0;c<4;c++)if(!(used&(1<<c))){
      let flips=0;for(let k=c+1;k<4;k++)if(used&(1<<k))flips++;
      go(r+1,used|(1<<c),flips%2?-sign:sign,prod*a[r][c]);
    }
  }
  go(0,0,1,1);return sum;
}
function cover(p,a){
  let mask=0n;
  for(const t of maps){
    const q=p.map(x=>t[x]);
    if(q.includes(a)&&q.includes(60))
      for(const x of q)if(x!==a&&x!==60)mask|=1n<<BigInt(x);
  }
  return mask;
}
function classesFor(a){
  const out=new Map();
  for(let c=0;c<121;c++)if(c!==a&&c!==60)
    for(let d=c+1;d<121;d++)if(d!==a&&d!==60){
      const p=[a,60,c,d];if(det4(p)===0)continue;
      const k=canonical(p);if(!out.has(k))out.set(k,cover(p,a));
    }
  return out;
}
function verifyCover(a,selected,classes){
  assert.equal(selected.length,31);assert.equal(new Set(selected).size,31);
  let used=0n;
  for(const k of selected){
    const p=points(k);assert.equal(p.length,4);
    assert.equal(canonical(p),k);assert.notEqual(det4(p),0);
    assert(classes.has(k),'unreachable class');
    assert(!witnesses.has(k),'known WIN4 used: '+k);
    used|=classes.get(k);
  }
  const universe=((1n<<121n)-1n)&~(1n<<BigInt(a))&~(1n<<60n);
  assert.equal(used,universe,'uncovered third move');
}
function verifyDual(row,classes){
  assert.equal(row.minimum_classes,31);assert.equal(row.dual_denominator,2);
  const dual=Object.entries(row.dual_numerators).map(([x,v])=>[Number(x),v]);
  assert.equal(dual.length,62);
  for(const [x,v] of dual){
    assert(Number.isInteger(x)&&x>=0&&x<121&&x!==row.first&&x!==60);
    assert.equal(v,1);
  }
  for(const [k,m] of classes){
    let w=0;for(const [x] of dual)if(m&(1n<<BigInt(x)))w++;
    assert(w<=2,'dual inequality: '+k);
  }
}
assert.equal(patch.schema,'n11-central-win4-safe-s4-31-patch-v1');
assert.equal(patch.board,11);assert.equal(patch.outcome,'UNKNOWN');
assert.equal(patch.first,48);assert.equal(patch.reply,60);
assert.equal(patch.base_certificate,'certificate.json.gz.b64');
assert.equal(patch.remove.length,3);assert.equal(patch.add.length,3);
const results=[];
for(let i=0;i<REPS.length;i++){
  const a=REPS[i],row=data.roots.find(r=>r.first===a);
  assert(row);assert.equal(row.reply,60);assert.equal(row.third_moves,119);
  const classes=classesFor(a);
  assert.equal(classes.size,row.legal_s4_classes);
  const blocked=[...classes.keys()].filter(k=>witnesses.has(k));
  assert.equal(blocked.length,EXCLUDED[i]);
  let selected=[...row.primal_s4_classes];
  if(a===48){
    for(const k of patch.remove){
      assert(witnesses.has(k));assert(selected.includes(k));
    }
    for(const k of patch.add){
      assert(!witnesses.has(k));assert(classes.has(k));assert(!selected.includes(k));
    }
    selected=selected.filter(k=>!patch.remove.includes(k)).concat(patch.add);
  }else{
    assert(selected.every(k=>!witnesses.has(k)));
  }
  verifyCover(a,selected,classes);verifyDual(row,classes);
  const forged=[blocked[0],...selected.slice(1)];
  assert.throws(()=>verifyCover(a,forged,classes),/known WIN4/);
  assert.throws(()=>verifyCover(a,selected.slice(1),classes));
  results.push({first:a,selected:31,excluded:blocked.length,thirdMovesCovered:119,
    repaired:a===48});
}
console.log(JSON.stringify({schema:'n11-central-win4-safe-31-audit-v1',
  roots:results,verifiedRoots:5,geometricConstrainedOptimum31:true,
  negativeControlsPassed:true,emptyBoard:'UNKNOWN',
  note:'No selected S4 LOSS is proved.'},null,2));
