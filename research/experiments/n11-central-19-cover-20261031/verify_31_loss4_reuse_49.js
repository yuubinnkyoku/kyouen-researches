#!/usr/bin/env node
'use strict';
// Independent audit of the 31-class {49,60} geometric cover.
// The three reused LOSS4 outcomes are solver-trusted S5 boundaries,
// NOT new terminal-to-root proofs; n11 empty-board outcome is UNKNOWN.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const zlib=require('node:zlib'),assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../../..');
const SOURCES=[
 ['research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache','2dccf42b92337cbcbfb62ea5c77db487b1ad8ead'],
 ['research/experiments/n11-boundary-recovery-20261006/output/post-23b52acf-after-round4-s6-escalation-s5-cache-corpus-union.cache','9887a18c0788d26507be7e8e191c26817634a6b6']
];
const PROOF=['research/experiments/n11-s4-boundary-direct-20261012/output/root-60-27-loss-proof.json','b52b6e2829f960e93393eac8fb930d415c37ac33'];
const hex=n=>n.toString(16).padStart(32,'0');
function pinned([file,expected]){
 const raw=fs.readFileSync(path.join(ROOT,file));
 const hash=crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');
 assert.equal(hash,expected,'source blob changed: '+file);
 return raw.toString('utf8');
}
function pairKey(lo,hi){
 const a=BigInt(lo),b=BigInt(hi);
 assert(a>=0n&&a<1n<<64n&&b>=0n&&b<1n<<64n);
 return hex(a+(b<<64n));
}
function parseCache(raw){
 const m=new Map();
 for(const line of raw.split(/\r?\n/)){
  if(!line||line.startsWith('#'))continue;
  const a=line.split(',');
  assert(a.length===6&&a[0]==='s5verdict'&&a[3]==='5');
  assert(['1','2'].includes(a[4])&&/^\d+$/.test(a[5]));
  const k=pairKey(a[1],a[2]);
  assert(!m.has(k),'duplicate verdict key');
  m.set(k,Number(a[4]));
 }
 return m;
}
function merge(a,b){
 const m=new Map(a);
 for(const [k,v] of b){
  if(m.has(k))assert.equal(m.get(k),v,'WIN/LOSS CONFLICT: '+k);
  else m.set(k,v);
 }
 return m;
}
const frozen=parseCache(pinned(SOURCES[0])),corpus=parseCache(pinned(SOURCES[1]));
assert.equal(frozen.size,5851);assert.equal(corpus.size,5700);
const cache=merge(frozen,corpus);assert.equal(cache.size,5853);
const shared=[...corpus].find(([k])=>frozen.has(k));assert(shared);
const forged=new Map(corpus);forged.set(shared[0],3-shared[1]);
assert.throws(()=>merge(frozen,forged),/WIN\/LOSS CONFLICT/);
const maps=Array.from({length:8},(_,j)=>Array.from({length:121},(_,i)=>{
 const x=i%11,y=Math.floor(i/11);
 const [u,v]=[[x,y],[10-y,x],[10-x,10-y],[y,10-x],
  [10-x,y],[10-y,10-x],[x,10-y],[y,x]][j];
 return 11*v+u;
}));
function points(k){
 assert.match(k,/^[0-9a-f]{32}$/);
 const n=BigInt('0x'+k);assert.equal(n>>121n,0n);
 const p=[];for(let i=0;i<121;i++)if(n&(1n<<BigInt(i)))p.push(i);
 return p;
}
function canonical(p){
 let best=null;
 for(const m of maps){
  let n=0n;for(const i of p)n|=1n<<BigInt(m[i]);
  if(best===null||n<best)best=n;
 }
 return hex(best);
}
// 3x3 difference determinant; the older geometric-cover verifier uses
// a separate full 4x4 permutation expansion.
function det4(p){
 const a=p.map(i=>{const x=i%11,y=Math.floor(i/11);return[x*x+y*y,x,y]});
 const b=a.slice(1).map(r=>r.map((v,j)=>v-a[0][j]));
 return b[0][0]*(b[1][1]*b[2][2]-b[1][2]*b[2][1])
  -b[0][1]*(b[1][0]*b[2][2]-b[1][2]*b[2][0])
  +b[0][2]*(b[1][0]*b[2][1]-b[1][1]*b[2][0]);
}
function coverage(p,first){
 const out=new Set();
 for(const m of maps){
  const q=p.map(i=>m[i]);
  if(q.includes(first)&&q.includes(60))
   for(const x of q)if(x!==first&&x!==60)out.add(x);
 }
 return out;
}
const proofRaw=pinned(PROOF).replace(
 /("(?:key|s4_class)"\s*:\s*\[\s*)(\d+)(\s*,\s*)(\d+)(\s*\])/g,
 '$1"$2"$3"$4"$5');
const proof=JSON.parse(proofRaw);
assert.equal(proof.schema,'n11-reply27-root-loss-move-certificate-v1');
assert.deepEqual(proof.root_stones,[60,27]);
assert.equal(proof.root_outcome,'LOSS');
assert.equal(proof.used_s4_loss_classes.length,32);
const loss4=new Map(proof.used_s4_loss_classes.map(r=>[pairKey(...r.key),r.s5_children]));
assert.equal(loss4.size,32);
const win4=new Set();
for(const [k,v] of cache)if(v===1){
 const p=points(k);assert.equal(p.length,5);
 for(const x of p)win4.add(canonical(p.filter(y=>y!==x)));
}
assert.equal(win4.size,555);
for(const k of loss4.keys())assert(!win4.has(k),'WIN4/LOSS4 contradiction');
const cert=JSON.parse(fs.readFileSync(path.join(__dirname,'win4-safe-31-loss4-reuse-49.json'),'utf8'));
assert.equal(cert.schema,'n11-central-49-win4-safe-loss4-reuse-v1');
assert.equal(cert.board,11);assert.deepEqual(cert.root_stones,[49,60]);
assert.equal(cert.root_outcome,'UNKNOWN');assert.equal(cert.minimum_geometric_classes,31);
const base=JSON.parse(zlib.gunzipSync(Buffer.from(
 fs.readFileSync(path.join(__dirname,'certificate.json.gz.b64'),'utf8').trim(),'base64')));
const row=base.roots.find(r=>r.first===49);
assert(row&&row.reply===60&&row.minimum_classes===31&&row.third_moves===119);
const repair=JSON.parse(fs.readFileSync(path.join(__dirname,'win4-safe-31-repair.json'),'utf8'))
 .repairs.find(r=>r.first===49);
assert(repair&&repair.remove.length===2&&repair.add.length===2);
assert(repair.remove.every(k=>row.primal_s4_classes.includes(k)));
const old=row.primal_s4_classes.filter(k=>!repair.remove.includes(k)).concat(repair.add);
const selected=cert.selected_s4_classes;
const required=cert.known_loss4_classes;
assert.equal(required.length,3);
assert.deepEqual(required,[...required].sort());
assert.equal(new Set(required).size,3);
assert(required.every(k=>loss4.has(k)));
assert.equal(selected.length,31);assert.equal(new Set(selected).size,31);
assert(required.every(k=>selected.includes(k)));
assert.equal(selected.filter(k=>loss4.has(k)).length,3);
const legalClasses=new Map();
for(let a=0;a<121;a++)if(a!==49&&a!==60)
 for(let b=a+1;b<121;b++)if(b!==49&&b!==60){
  const p=[49,60,a,b];
  if(det4(p)===0)continue;
  const k=canonical(p);
  if(!legalClasses.has(k))legalClasses.set(k,coverage(p,49));
 }
assert.equal(legalClasses.size,3374);
const dual=new Set(Object.entries(row.dual_numerators).map(([k,v])=>{
 assert.equal(v,1);return Number(k);
}));
assert.equal(row.dual_denominator,2);assert.equal(dual.size,62);
for(const [k,c] of legalClasses){
 let n=0;for(const x of c)if(dual.has(x))n++;
 assert(n<=2,'dual lower bound fails for '+k);
}
const childMemo=new Map();
function children(k){
 if(childMemo.has(k))return childMemo.get(k);
 const p=points(k);
 assert.equal(p.length,4);assert.equal(canonical(p),k);assert.notEqual(det4(p),0);
 const out=new Set();
 for(let x=0;x<121;x++)if(!p.includes(x)){
  const q=[...p,x];
  let safe=true;
  for(let j=0;j<4;j++)if(det4(q.filter((_,i)=>i!==j))===0){safe=false;break;}
  if(safe)out.add(canonical(q));
 }
 childMemo.set(k,out);return out;
}
function checkCover(keys){
 assert.equal(keys.length,31);assert.equal(new Set(keys).size,31);
 const covered=new Set(),all5=new Set();
 for(const k of keys){
  assert(legalClasses.has(k),'S4 not reachable from root');
  assert(!win4.has(k),'known WIN4 selected');
  children(k);
  for(const x of legalClasses.get(k))covered.add(x);
  for(const x of children(k))all5.add(x);
 }
 assert.equal(covered.size,119,'third-move coverage incomplete');
 assert(!covered.has(49)&&!covered.has(60));
 const known=[...all5].filter(k=>cache.has(k)).length;
 return {distinctS5:all5.size,knownS5:known,unknownS5:all5.size-known,
  alreadyLOSS4:keys.filter(k=>loss4.has(k)).length};
}
const before=checkCover(old),after=checkCover(selected);
assert.equal(before.unknownS5,3330);
assert.equal(before.alreadyLOSS4,0);
assert.deepEqual(after,{distinctS5:2840,knownS5:315,unknownS5:2525,alreadyLOSS4:3});
assert.deepEqual(cert.s5_dependency,{distinct:2840,known:315,unknown:2525});
for(const k of required){
 const ch=children(k);
 assert.equal(ch.size,loss4.get(k),'LOSS4 manifest child count mismatch');
 for(const c of ch)assert.equal(cache.get(c),2,'LOSS4 child verdict not proven');
}
assert.throws(()=>checkCover(selected.slice(1)));
const blocked=[...legalClasses.keys()].find(k=>win4.has(k));assert(blocked);
assert.throws(()=>checkCover([...selected.slice(1),blocked]),/known WIN4/);
const altered=new Map(cache),firstChild=[...children(required[0])][0];
altered.set(firstChild,1);
assert.throws(()=>{for(const c of children(required[0]))
 assert.equal(altered.get(c),2,'LOSS4 child verdict not proven');},/LOSS4 child verdict/);
console.log(JSON.stringify({schema:cert.schema,first:49,reply:60,
 geometricMinimum:31,allThirdMovesCovered:119,dualClassesChecked:legalClasses.size,
 reusedLOSS4:3,unknownS4:28,
 before,after,reducedUnknownS5:before.unknownS5-after.unknownS5,
 negativeControlsPassed:true,emptyBoard:'UNKNOWN',
 trust:'Three LOSS4 classes rely on pinned solver-trusted S5 verdicts; other S4 outcomes UNKNOWN.'},null,2));


// Audited per-witness frontier for the *fixed* 31-class cover.
// This does not promote any of the 28 UNKNOWN S4 outcomes to LOSS.
const frontier=JSON.parse(fs.readFileSync(path.join(__dirname,'central49-frontier-ownership.json'),'utf8'));
assert.equal(frontier.schema,'n11-central49-s4-frontier-ownership-v1');
assert.deepEqual(frontier.rootStones,[49,60]);
assert.equal(frontier.rootOutcome,'UNKNOWN');
assert.equal(frontier.sourceCertificate,'win4-safe-31-loss4-reuse-49.json');
assert.deepEqual(frontier.sourceS5CacheBlobs,SOURCES.map(x=>x[1]));
const thirdFrequency=new Map(),unknownFrequency=new Map(),allChildren=new Set();
for(const k of selected){
 for(const x of legalClasses.get(k))thirdFrequency.set(x,(thirdFrequency.get(x)||0)+1);
 for(const x of children(k)){
  allChildren.add(x);
  if(!cache.has(x))unknownFrequency.set(x,(unknownFrequency.get(x)||0)+1);
 }
}
const auditedWitnesses=selected.map(k=>{
 const covered=[...legalClasses.get(k)].sort((a,b)=>a-b);
 const ch=[...children(k)],unknown=ch.filter(x=>!cache.has(x));
 assert(ch.every(x=>cache.get(x)!==1),'WIN5 under selected LOSS4 candidate');
 const dualOwned=covered.filter(x=>dual.has(x));
 assert.equal(dualOwned.length,2,'dual saturation broken: '+k);
 return {s4:k,status:loss4.has(k)?'LOSS4_PINNED_S5':'UNKNOWN',
  thirdMoves:covered,exclusiveThirdMoves:covered.filter(x=>thirdFrequency.get(x)===1),
  legalS5Children:ch.length,knownLossS5:ch.length-unknown.length,
  unknownS5:unknown.length,sharedUnknownS5:unknown.filter(x=>unknownFrequency.get(x)>1).length};
});
const dualOwnedAll=auditedWitnesses.flatMap(w=>w.thirdMoves.filter(x=>dual.has(x)));
assert.equal(new Set(dualOwnedAll).size,62,'dual points multiply covered');
const unresolved=auditedWitnesses.filter(w=>w.status==='UNKNOWN');
const auditedSummary={
 selectedS4:selected.length,reusedLoss4:selected.length-unresolved.length,unresolvedS4:unresolved.length,
 thirdMoves:thirdFrequency.size,
 onceCoveredThirdMoves:[...thirdFrequency.values()].filter(n=>n===1).length,
 multiplyCoveredThirdMove:[...thirdFrequency].find(([x,n])=>n>1)?.[0],
 multiplyCoveredMultiplicity:Math.max(...thirdFrequency.values()),
 eachWitnessHasExclusiveThirdMove:auditedWitnesses.every(w=>w.exclusiveThirdMoves.length>0),
 distinctS5:allChildren.size,knownLossS5:[...allChildren].filter(x=>cache.get(x)===2).length,
 unknownS5:unknownFrequency.size,
 unknownS5Incidences:[...unknownFrequency.values()].reduce((a,b)=>a+b,0),
 unknownS5SharedByTwo:[...unknownFrequency.values()].filter(n=>n===2).length,
 unknownS5SharedByThreeOrMore:[...unknownFrequency.values()].filter(n=>n>=3).length,
 minUnknownS5PerUnresolvedS4:Math.min(...unresolved.map(w=>w.unknownS5)),
 maxUnknownS5PerUnresolvedS4:Math.max(...unresolved.map(w=>w.unknownS5))
};
assert.deepEqual(frontier.witnesses,auditedWitnesses,'frontier witness mismatch');
assert.deepEqual(frontier.summary,auditedSummary,'frontier summary mismatch');
assert.deepEqual(
 [auditedSummary.thirdMoves,auditedSummary.onceCoveredThirdMoves,auditedSummary.multiplyCoveredThirdMove,
  auditedSummary.multiplyCoveredMultiplicity,auditedSummary.unknownS5,auditedSummary.unknownS5Incidences,
  auditedSummary.unknownS5SharedByTwo],
 [119,118,71,13,2525,2826,301]);
assert(auditedSummary.eachWitnessHasExclusiveThirdMove);
const tampered=JSON.parse(JSON.stringify(frontier));
tampered.witnesses[0].unknownS5++;
assert.throws(()=>assert.deepEqual(tampered.witnesses,auditedWitnesses));
console.log(JSON.stringify({schema:frontier.schema,summary:auditedSummary,
 lowestUnknownS5:unresolved.slice().sort((a,b)=>a.unknownS5-b.unknownS5||a.s4.localeCompare(b.s4))
  .slice(0,3).map(w=>({s4:w.s4,unknownS5:w.unknownS5,sharedUnknownS5:w.sharedUnknownS5})),
 negativeControlPassed:true,emptyBoard:'UNKNOWN'},null,2));
