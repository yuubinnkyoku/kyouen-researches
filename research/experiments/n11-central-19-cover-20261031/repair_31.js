'use strict';
// Deterministic exact-size local repair of the five 31-class covers containing
// known WIN4. This is a search for geometry-only replacements, not LOSS proofs.
const fs=require('node:fs'),zlib=require('node:zlib'),assert=require('node:assert/strict');
const {witnesses,canonical,maps}=require('./audit_win4_exclusion');
const data=JSON.parse(zlib.gunzipSync(Buffer.from(
  fs.readFileSync(__dirname+'/certificate.json.gz.b64','utf8').trim(),'base64')));
const ROOTS=[16,49,24,48,12];
function det4(p){
  const a=p.map(i=>{const x=i%11,y=Math.floor(i/11);return[x*x+y*y,x,y]});
  const b=a.slice(1).map(row=>row.map((v,j)=>v-a[0][j]));
  return b[0][0]*(b[1][1]*b[2][2]-b[1][2]*b[2][1])
    -b[0][1]*(b[1][0]*b[2][2]-b[1][2]*b[2][0])
    +b[0][2]*(b[1][0]*b[2][1]-b[1][1]*b[2][0]);
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
function pop(n){let c=0;while(n){n&=n-1n;c++}return c}
function classesFor(a){
  const m=new Map();
  for(let c=0;c<121;c++)if(c!==a&&c!==60)
    for(let d=c+1;d<121;d++)if(d!==a&&d!==60){
      const p=[a,60,c,d];if(det4(p)===0)continue;
      const k=canonical(p);if(!m.has(k))m.set(k,cover(p,a));
    }
  return m;
}
const out=[];
for(const a of ROOTS){
  const row=data.roots.find(x=>x.first===a);assert(row&&row.minimum_classes===31);
  const classes=classesFor(a),selected=row.primal_s4_classes;
  const remove=selected.filter(k=>witnesses.has(k)),fixed=selected.filter(k=>!witnesses.has(k));
  const universe=((1n<<121n)-1n)&~(1n<<BigInt(a))&~(1n<<60n);
  const dual=Object.keys(row.dual_numerators).reduce((m,k)=>m|1n<<BigInt(k),0n);
  const fixedCover=fixed.reduce((m,k)=>m|classes.get(k),0n);
  const missingDual=dual&~fixedCover,missingFull=universe&~fixedCover;
  assert.equal(pop(missingDual),2*remove.length);
  const opts=[];
  for(const [k,m] of classes){
    if(witnesses.has(k)||fixed.includes(k))continue;
    const d=m&dual;
    if(pop(d)!==2||(d&~missingDual)!==0n)continue;
    opts.push({k,m,d});
  }
  const byPoint=new Map();
  for(let x=0;x<121;x++)if(missingDual&(1n<<BigInt(x)))
    byPoint.set(x,opts.filter(z=>z.d&(1n<<BigInt(x))));
  let nodes=0,solution=null;
  function dfs(remDual,covered,chosen){
    nodes++;
    if(remDual===0n){
      if((covered&missingFull)===missingFull){solution=[...chosen];return true}
      return false;
    }
    let pivot=-1,choices=null;
    for(const [x,ls] of byPoint)if(remDual&(1n<<BigInt(x))){
      const valid=ls.filter(z=>(z.d&remDual)===z.d);
      if(choices===null||valid.length<choices.length){choices=valid;pivot=x}
    }
    if(pivot<0||!choices.length)return false;
    choices.sort((a,b)=>pop(b.m&missingFull&~covered)-pop(a.m&missingFull&~covered)||a.k.localeCompare(b.k));
    for(const z of choices)if(dfs(remDual&~z.d,covered|z.m,[...chosen,z.k]))return true;
    return false;
  }
  const found=dfs(missingDual,0n,[]);
  if(found){
    const after=[...fixed,...solution],cov=after.reduce((m,k)=>m|classes.get(k),0n);
    assert.equal(after.length,31);assert.equal(cov,universe);
    assert(after.every(k=>!witnesses.has(k)));
  }
  out.push({first:a,remove,add:solution,found,nodes,candidates:opts.length,
    uncoveredThirds:pop(missingFull),uncoveredDual:pop(missingDual)});
}
console.log(JSON.stringify({schema:'n11-central-31-local-repair-v1',outcome:'UNKNOWN',roots:out},null,2));
