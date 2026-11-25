#!/usr/bin/env node
'use strict';
// Independently enumerate central-reply S4 classes and remove classes
// disproved as LOSS by saved exact S5 WIN witnesses. No S4 LOSS is inferred.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const zlib = require('node:zlib');
const assert = require('node:assert/strict');
const {excludeQuarantined}=require('./quarantine_s5');
const ROOT = path.resolve(__dirname, '../../..');
const SOURCES = [
  ['research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache',
    '2dccf42b92337cbcbfb62ea5c77db487b1ad8ead'],
  ['research/experiments/n11-boundary-recovery-20261006/output/post-23b52acf-after-round4-s6-escalation-s5-cache-corpus-union.cache',
    '9887a18c0788d26507be7e8e191c26817634a6b6'],
];
const REPS = [16,38,49,24,0,26,48,12,25,3,13,2,14,5,15,4,1,37,36];
const EXPECTED = [
  [3402,100],[3400,30],[3374,66],[3384,63],[3396,3],
  [6542,35],[3377,112],[3389,120],[6585,9],[6612,47],
  [6586,21],[6594,29],[6577,15],[3385,21],[6590,43],
  [6588,16],[6615,11],[6546,32],[3388,21],
];
const hex = n => n.toString(16).padStart(32, '0');
const maps = Array.from({length:8}, (_,j) => Array.from({length:121}, (_,i) => {
  const x=i%11,y=Math.floor(i/11);
  const [u,v]=[[x,y],[10-y,x],[10-x,10-y],[y,10-x],
    [10-x,y],[10-y,10-x],[x,10-y],[y,x]][j];
  return 11*v+u;
}));
function canonical(p) {
  let best=null;
  for(const t of maps) {
    let b=0n;
    for(const x of p) b|=1n<<BigInt(t[x]);
    if(best===null || b<best) best=b;
  }
  return hex(best);
}
function points(k) {
  assert.match(k,/^[0-9a-f]{32}$/);
  const b=BigInt('0x'+k);
  assert.equal(b>>121n,0n);
  const p=[];
  for(let i=0;i<121;i++) if(b&(1n<<BigInt(i))) p.push(i);
  return p;
}
// Independent of the 4x4 permutation determinant in verify.js:
// translate the first row to zero, then expand the resulting 3x3.
function det4(p) {
  const rows=p.map(i=>{
    const x=i%11,y=Math.floor(i/11);
    return [x*x+y*y,x,y];
  });
  const a=rows.slice(1).map(r=>r.map((v,j)=>v-rows[0][j]));
  return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
    -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
    +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]);
}
function safe(p) {
  for(let a=0;a<p.length;a++)for(let b=a+1;b<p.length;b++)
    for(let c=b+1;c<p.length;c++)for(let d=c+1;d<p.length;d++)
      if(det4([p[a],p[b],p[c],p[d]])===0) return false;
  return true;
}
function pinned(file,expected) {
  const raw=fs.readFileSync(path.join(ROOT,file));
  const sha=crypto.createHash('sha1')
    .update(Buffer.from('blob '+raw.length+'\0')).update(raw).digest('hex');
  assert.equal(sha,expected,'source blob changed: '+file);
  return raw.toString('utf8');
}
function parseCache(raw) {
  const out=new Map();
  for(const line of raw.split(/\r?\n/)) {
    if(!line || line.startsWith('#')) continue;
    const f=line.split(',');
    assert.equal(f.length,6);
    assert.equal(f[0],'s5verdict');
    assert.equal(f[3],'5');
    assert(['1','2'].includes(f[4]));
    assert(/^\d+$/.test(f[5]));
    const lo=BigInt(f[1]),hi=BigInt(f[2]);
    assert(lo>=0n && lo<1n<<64n && hi>=0n && hi<1n<<64n);
    const k=hex(lo+(hi<<64n));
    const p=points(k);
    assert.equal(p.length,5);
    assert.equal(canonical(p),k);
    assert(safe(p));
    assert(!out.has(k),'duplicate cache key: '+k);
    out.set(k,Number(f[4]));
  }
  return out;
}
function merge(a,b) {
  const out=new Map(a);
  for(const [k,v] of b) {
    if(out.has(k)) assert.equal(out.get(k),v,'WIN/LOSS CONFLICT: '+k);
    else out.set(k,v);
  }
  return out;
}
const frozen=parseCache(pinned(...SOURCES[0]));
const corpus=parseCache(pinned(...SOURCES[1]));
assert.equal(frozen.size,5851);
assert.equal(corpus.size,5700);
const merged=merge(frozen,corpus);
assert.equal(merged.size,5853);
excludeQuarantined(merged);
assert.equal(merged.size,5851);
const win5=[...merged].filter(([,v])=>v===1).map(([k])=>k);
assert.equal(win5.length,159);
const witnesses=new Map();
for(const k of win5) {
  const p=points(k);
  for(const x of p) {
    const parent=canonical(p.filter(y=>y!==x));
    if(!witnesses.has(parent)) witnesses.set(parent,k);
  }
}
assert.equal(witnesses.size,549);
for(const [parent,child] of witnesses) {
  const pp=points(parent),cp=points(child);
  assert.equal(pp.length,4);
  assert(safe(pp));
  assert(cp.some(x=>canonical(cp.filter(y=>y!==x))===parent));
}
const rootStats=[];
const uniqueBlocked=new Set();
let classIncidences=0,blockedIncidences=0;
for(let j=0;j<REPS.length;j++) {
  const first=REPS[j],classes=new Set();
  for(let c=0;c<121;c++) if(c!==first && c!==60)
    for(let d=c+1;d<121;d++) if(d!==first && d!==60) {
      const p=[first,60,c,d];
      if(det4(p)!==0) classes.add(canonical(p));
    }
  const blocked=[...classes].filter(k=>witnesses.has(k));
  assert.deepEqual([classes.size,blocked.length],EXPECTED[j],
    'root '+first+' geometric or WIN4 incidence changed');
  blocked.forEach(k=>uniqueBlocked.add(k));
  classIncidences+=classes.size;
  blockedIncidences+=blocked.length;
  rootStats.push({first,legalClasses:classes.size,win4Excluded:blocked.length,
    remainingCandidates:classes.size-blocked.length});
}
assert.equal(classIncidences,96330);
assert.equal(blockedIncidences,794);
assert.equal(uniqueBlocked.size,389);
// Audit how many of the earlier geometry-only optimal witnesses need repair.
// This is not an assertion that the minimum 31/56 remains achievable.
const certRaw=fs.readFileSync(path.join(__dirname,'certificate.json.gz.b64'),'utf8');
const cert=JSON.parse(zlib.gunzipSync(Buffer.from(certRaw.trim(),'base64')));
assert.equal(cert.schema,'n11-central-19-geometric-s4-cover-v1');
assert.deepEqual(cert.roots.map(r=>r.first),REPS);
const selectedWitnessConflicts=cert.roots.map(r=>({
  first:r.first,
  selected:r.primal_s4_classes.length,
  knownWin4:r.primal_s4_classes.filter(k=>witnesses.has(k)).length
}));
assert(selectedWitnessConflicts.every(r=>r.knownWin4<=r.selected));
const shared=[...corpus].find(([k])=>frozen.has(k));
assert(shared);
const forged=new Map(corpus);
forged.set(shared[0],3-shared[1]);
assert.throws(()=>merge(frozen,forged),/WIN\/LOSS CONFLICT/);
console.log(JSON.stringify({
  board:11,emptyBoard:'UNKNOWN',
  frozenS5:frozen.size,corpusS5:corpus.size,mergedS5:merged.size,
  quarantinedUnsupportedWIN5:2,
  exactWin5:win5.length,derivedWin4:witnesses.size,
  centralRoots:REPS.length,legalS4ClassIncidences:classIncidences,
  excludedWIN4Incidences:blockedIncidences,
  uniqueExcludedWIN4Classes:uniqueBlocked.size,
  remainingS4ClassIncidences:classIncidences-blockedIncidences,
  rootStats,selectedWitnessConflicts,
  note:'Existing solver-trusted S5 WIN labels; geometry audited. No S4 LOSS or root verdict added.'
},null,2));

// Reuse the pinned-cache, conflict-checked WIN4 set in an independent
// 4x4-determinant audit of the constrained geometric cover certificate.
module.exports={witnesses,REPS,canonical,points,maps};
