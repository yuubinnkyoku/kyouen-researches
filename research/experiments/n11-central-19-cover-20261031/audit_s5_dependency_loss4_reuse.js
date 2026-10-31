#!/usr/bin/env node
'use strict';
// Audit 19 central-reply covers against pinned S5 verdicts, and certify
// three substitutions of already-proven LOSS4 classes in the 56-class covers.
// Geometric minima are NOT proofs of the selected unknown S4 outcomes.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const zlib=require('node:zlib'),assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../../..');
const SOURCES=[
  ['research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache',
   '2dccf42b92337cbcbfb62ea5c77db487b1ad8ead'],
  ['research/experiments/n11-boundary-recovery-20261006/output/post-23b52acf-after-round4-s6-escalation-s5-cache-corpus-union.cache',
   '9887a18c0788d26507be7e8e191c26817634a6b6']
];
const PROOF=['research/experiments/n11-s4-boundary-direct-20261012/output/root-60-27-loss-proof.json',
 'b52b6e2829f960e93393eac8fb930d415c37ac33'];
function pinned([file,expected]){
  const raw=fs.readFileSync(path.join(ROOT,file));
  const sha=crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');
  assert.equal(sha,expected,'source changed: '+file);
  return raw.toString('utf8');
}
const hex=n=>n.toString(16).padStart(32,'0');
function pairKey(a){
  assert(Array.isArray(a)&&a.length===2&&a.every(x=>typeof x==='string'&&/^\d+$/.test(x)));
  const lo=BigInt(a[0]),hi=BigInt(a[1]);
  assert(lo>=0n&&lo<1n<<64n&&hi>=0n&&hi<1n<<64n);
  return hex(lo+(hi<<64n));
}
function parseCache(raw){
  const out=new Map();
  for(const line of raw.split(/\r?\n/)){
    if(!line||line.startsWith('#'))continue;
    const f=line.split(',');
    assert(f.length===6&&f[0]==='s5verdict'&&f[3]==='5'&&
      ['1','2'].includes(f[4])&&/^\d+$/.test(f[5]));
    const k=pairKey([f[1],f[2]]);
    assert(!out.has(k),'duplicate S5 cache key');
    out.set(k,Number(f[4]));
  }
  return out;
}
function merge(a,b){
  const out=new Map(a);
  for(const [k,v] of b){
    if(out.has(k))assert.equal(out.get(k),v,'WIN/LOSS CONFLICT: '+k);
    else out.set(k,v);
  }
  return out;
}
const frozen=parseCache(pinned(SOURCES[0])),corpus=parseCache(pinned(SOURCES[1]));
assert.equal(frozen.size,5851);assert.equal(corpus.size,5700);
const cache=merge(frozen,corpus);assert.equal(cache.size,5853);
const common=[...corpus].find(([k])=>frozen.has(k));assert(common);
const forged=new Map(corpus);forged.set(common[0],3-common[1]);
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
    let n=0n;for(const x of p)n|=1n<<BigInt(m[x]);
    if(best===null||n<best)best=n;
  }
  return hex(best);
}
// Integer 3x3 difference determinant, independent of the 4x4 cover verifiers.
function det4(p){
  const a=p.map(i=>{const x=i%11,y=Math.floor(i/11);return[x*x+y*y,x,y]});
  const b=a.slice(1).map(r=>r.map((v,j)=>v-a[0][j]));
  return b[0][0]*(b[1][1]*b[2][2]-b[1][2]*b[2][1])
    -b[0][1]*(b[1][0]*b[2][2]-b[1][2]*b[2][0])
    +b[0][2]*(b[1][0]*b[2][1]-b[1][1]*b[2][0]);
}
function coverage(k,first){
  const p=points(k),out=new Set();
  for(const m of maps){
    const q=p.map(i=>m[i]);
    if(q.includes(first)&&q.includes(60))
      for(const x of q)if(x!==first&&x!==60)out.add(x);
  }
  return out;
}
const childMemo=new Map();
function children(k){
  if(childMemo.has(k))return childMemo.get(k);
  const p=points(k);assert.equal(p.length,4);
  assert.equal(canonical(p),k);assert.notEqual(det4(p),0);
  const out=new Set();
  for(let x=0;x<121;x++)if(!p.includes(x)){
    const q=[...p,x];
    let legal=true;
    for(let omit=0;omit<4;omit++)
      if(det4(q.filter((_,j)=>j!==omit))===0){legal=false;break;}
    if(legal)out.add(canonical(q));
  }
  childMemo.set(k,out);return out;
}
const rawProof=pinned(PROOF).replace(
  /("(?:key|s4_class)"\s*:\s*\[\s*)(\d+)(\s*,\s*)(\d+)(\s*\])/g,
  '$1"$2"$3"$4"$5');
const proof=JSON.parse(rawProof);
assert.equal(proof.schema,'n11-reply27-root-loss-move-certificate-v1');
assert.equal(proof.root_outcome,'LOSS');
assert.deepEqual(proof.root_stones,[60,27]);
assert.equal(proof.legal_root_moves,119);
assert.equal(proof.used_s4_loss_classes.length,32);
const loss4=new Map(proof.used_s4_loss_classes.map(r=>[pairKey(r.key),r.s5_children]));
assert.equal(loss4.size,32);
function verifyLoss4(k,c=cache){
  assert(loss4.has(k),'S4 is not in pinned LOSS4 proof: '+k);
  const ch=children(k);assert.equal(ch.size,loss4.get(k));
  for(const x of ch)assert.equal(c.get(x),2,'S4 LOSS boundary not certified: '+x);
  return ch.size;
}
const win4=new Set();
for(const [k,v] of cache)if(v===1){
  const p=points(k);assert.equal(p.length,5);
  for(const x of p)win4.add(canonical(p.filter(y=>y!==x)));
}
assert.equal(win4.size,555);
for(const k of loss4.keys())assert(!win4.has(k),'WIN4/LOSS4 conflict');
const base=JSON.parse(zlib.gunzipSync(Buffer.from(
  fs.readFileSync(path.join(__dirname,'certificate.json.gz.b64'),'utf8').trim(),'base64')));
const cert56=JSON.parse(fs.readFileSync(path.join(__dirname,'win4-safe-56-certificate.json')));
const repair31=JSON.parse(fs.readFileSync(path.join(__dirname,'win4-safe-31-repair.json')));
const patch=JSON.parse(fs.readFileSync(path.join(__dirname,'win4-safe-56-loss4-reuse.json')));
assert.equal(base.schema,'n11-central-19-geometric-s4-cover-v1');
assert.equal(cert56.schema,'n11-central-win4-safe-s4-cover-v1');
assert.equal(repair31.schema,'n11-central-win4-safe-s4-31-patches-v2');
assert.equal(patch.schema,'n11-central-win4-safe-56-loss4-reuse-v1');
assert.equal(patch.board,11);assert.equal(patch.outcome,'UNKNOWN');
assert.equal(patch.base_certificate,'win4-safe-56-certificate.json');
assert.equal(patch.loss4_proof,PROOF[0]);
assert.deepEqual(patch.swaps.map(s=>s.first),[4,1,37]);
assert.equal(new Set(patch.swaps.map(s=>s.add)).size,3);
const selected31=new Map();
for(const row of base.roots)if(row.minimum_classes===31){
  const repair=repair31.repairs.find(r=>r.first===row.first);
  let chosen=[...row.primal_s4_classes];
  if(repair){
    assert.equal(repair.remove.length,repair.add.length);
    for(const k of repair.remove)assert(chosen.includes(k));
    chosen=chosen.filter(k=>!repair.remove.includes(k)).concat(repair.add);
  }
  selected31.set(row.first,chosen);
}
function checkCover(first,chosen,expected){
  assert.equal(chosen.length,expected);
  assert.equal(new Set(chosen).size,expected);
  const seen=new Set();
  for(const k of chosen){
    assert(!win4.has(k),'selected S4 is already WIN4: '+k);
    assert(coverage(k,first).size>0,'unreachable S4: '+k);
    children(k); // independent legality and canonicality check
    for(const x of coverage(k,first))seen.add(x);
  }
  assert.equal(seen.size,119,'incomplete third-move cover: '+first);
  assert(!seen.has(first)&&!seen.has(60));
}
const before=[],after=[];
for(const row of base.roots){
  const first=row.first;
  const is56=row.minimum_classes===56;
  const original=is56?cert56.roots.find(r=>r.first===first)?.primal_s4_classes:selected31.get(first);
  assert(original,'missing root '+first);
  const swap=patch.swaps.find(s=>s.first===first);
  let updated=[...original];
  if(swap){
    assert(is56);assert(original.includes(swap.remove));
    assert(!original.includes(swap.add));
    assert(!win4.has(swap.add));
    verifyLoss4(swap.add);
    updated=updated.map(k=>k===swap.remove?swap.add:k);
  }
  checkCover(first,original,row.minimum_classes);
  checkCover(first,updated,row.minimum_classes);
  before.push({first,selected:original,minimum:row.minimum_classes});
  after.push({first,selected:updated,minimum:row.minimum_classes});
}
assert.equal(before.length,19);
assert.equal(after.reduce((n,r)=>n+r.selected.length,0),839);
for(const s of patch.swaps){
  assert(!after.some(r=>r.minimum===56&&r.selected.includes(s.remove)),'removed S4 still selected in a 56-root');
  assert.throws(()=>verifyLoss4(s.remove),/not in pinned LOSS4 proof/);
  const ch=children(s.add),bad=new Map(cache);
  bad.set([...ch][0],1);
  assert.throws(()=>verifyLoss4(s.add,bad),/S4 LOSS boundary not certified/);
}
assert.throws(()=>checkCover(4,after.find(r=>r.first===4).selected.slice(1),56));
function summary(rows){
  const allS4=new Set(rows.flatMap(r=>r.selected));
  const allS5=new Set([...allS4].flatMap(k=>[...children(k)]));
  const known=[...allS5].filter(k=>cache.has(k)).length;
  const roots=rows.map(r=>{
    const c=new Set(r.selected.flatMap(k=>[...children(k)]));
    const hits=[...c].filter(k=>cache.has(k)).length;
    return {first:r.first,selected:r.selected.length,
      alreadyLOSS4:r.selected.filter(k=>loss4.has(k)).length,
      distinctS5:c.size,knownS5:hits,unknownS5:c.size-hits};
  });
  return {selectedIncidences:rows.reduce((n,r)=>n+r.selected.length,0),
    uniqueS4:allS4.size,alreadyLOSS4:[...allS4].filter(k=>loss4.has(k)).length,
    distinctS5:allS5.size,knownS5:known,unknownS5:allS5.size-known,roots};
}
const old56=summary(before.filter(r=>r.minimum===56));
const new56=summary(after.filter(r=>r.minimum===56));
const old19=summary(before),new19=summary(after);
assert.equal(old56.uniqueS4,555);
assert.equal(old56.unknownS5,46639);
assert.equal(old56.knownS5,198);
assert.equal(new56.uniqueS4,555);
assert.equal(new56.alreadyLOSS4,3);
assert.equal(new56.unknownS5,46529);
assert.equal(new56.knownS5,493);
assert.equal(new56.unknownS5-old56.unknownS5,-110);
assert(new19.unknownS5<=old19.unknownS5,'19-root unknown dependency increased');
console.log(JSON.stringify({
  schema:'n11-central-19-s5-dependency-loss4-reuse-v1',
  existingLOSS4Source:'{60,27} certificate (solver-trusted S5 labels)',
  patchedRoots:[4,1,37],newLOSS4Proven:0,
  ten56:{before:{uniqueS4:old56.uniqueS4,alreadyLOSS4:old56.alreadyLOSS4,
      distinctS5:old56.distinctS5,knownS5:old56.knownS5,unknownS5:old56.unknownS5},
    after:{uniqueS4:new56.uniqueS4,alreadyLOSS4:new56.alreadyLOSS4,
      distinctS5:new56.distinctS5,knownS5:new56.knownS5,unknownS5:new56.unknownS5},
    reducedDistinctUnknownS5:old56.unknownS5-new56.unknownS5},
  all19:{before:{uniqueS4:old19.uniqueS4,alreadyLOSS4:old19.alreadyLOSS4,
      unknownS5:old19.unknownS5},
    after:{uniqueS4:new19.uniqueS4,alreadyLOSS4:new19.alreadyLOSS4,
      unknownS5:new19.unknownS5},
    reducedDistinctUnknownS5:old19.unknownS5-new19.unknownS5,
    rootCosts:new19.roots.sort((a,b)=>a.unknownS5-b.unknownS5||a.first-b.first)},
  negativeControlsPassed:true,emptyBoard:'UNKNOWN',
  note:'The 3 reused LOSS4 labels depend on the pinned exact S5 solver results. Other selected S4 remain unproved.'
},null,2));


// Second-stage, matching-preserving two-edge substitutions. Each operation
// replaces one or two unknown S4s with one pinned LOSS4 and (when needed)
// one still-unknown S4. The entire 119-move cover is rechecked afterwards.
const patch2=JSON.parse(fs.readFileSync(path.join(__dirname,'win4-safe-56-loss4-reuse-v2.json')));
assert.equal(patch2.schema,'n11-central-win4-safe-56-loss4-reuse-v2');
assert.equal(patch2.board,11);assert.equal(patch2.outcome,'UNKNOWN');
assert.equal(patch2.base_certificate,'win4-safe-56-certificate.json');
assert.equal(patch2.loss4_proof,PROOF[0]);
assert.deepEqual(patch2.roots.map(r=>r.first),[26,25,3,13,2,14,15,4,1,37]);
const after2=before.map(row=>{
  const plan=patch2.roots.find(r=>r.first===row.first);
  if(!plan)return {...row,selected:[...row.selected]};
  assert.equal(row.minimum,56);
  let chosen=[...row.selected];
  const removed=new Set(),added=new Set();
  for(const op of plan.operations){
    assert(op.remove.length===op.add.length);
    assert([1,2].includes(op.remove.length));
    assert.equal(op.add.filter(k=>loss4.has(k)).length,1,
      'each operation must introduce exactly one certified LOSS4');
    for(const k of op.remove){
      assert(!removed.has(k)&&chosen.includes(k),'duplicate or missing removed class');
      removed.add(k);
    }
    for(const k of op.add){
      assert(!added.has(k)&&!chosen.includes(k),'duplicate or existing added class');
      assert(!win4.has(k),'known WIN4 added');
      added.add(k);
      if(loss4.has(k))verifyLoss4(k);
      else children(k);
    }
    chosen=chosen.filter(k=>!op.remove.includes(k)).concat(op.add);
  }
  assert.equal(new Set(chosen).size,56);
  checkCover(row.first,chosen,56);
  return {...row,selected:chosen};
});
assert.equal(after2.length,19);
assert.equal(after2.reduce((n,r)=>n+r.selected.length,0),839);
const final56=summary(after2.filter(r=>r.minimum===56));
const final19=summary(after2);
const loss4Incidences=final56.roots.reduce((n,r)=>n+r.alreadyLOSS4,0);
assert.equal(loss4Incidences,19);
assert(final56.roots.every(r=>r.alreadyLOSS4>=1),'one of ten roots still has no reusable LOSS4');
assert(final56.unknownS5<new56.unknownS5,'v2 did not improve v1');
assert(final19.unknownS5<new19.unknownS5,'v2 did not improve 19-root union');
for(const plan of patch2.roots){
  for(const op of plan.operations)
    for(const k of op.remove)
      assert(!after2.find(r=>r.first===plan.first).selected.includes(k));
}
console.log(JSON.stringify({
  schema:'n11-central-19-s5-dependency-loss4-reuse-v2',
  geometricCoversVerified:19,rootThirdMovesVerified:19*119,
  exactLoss4Incidences:loss4Incidences,
  ten56:{before:{unknownS5:old56.unknownS5,alreadyLOSS4:old56.alreadyLOSS4},
    v1:{unknownS5:new56.unknownS5,alreadyLOSS4:new56.alreadyLOSS4},
    v2:{uniqueS4:final56.uniqueS4,alreadyLOSS4:final56.alreadyLOSS4,
      knownS5:final56.knownS5,unknownS5:final56.unknownS5},
    reducedUnknownS5:old56.unknownS5-final56.unknownS5},
  all19:{before:{uniqueS4:old19.uniqueS4,unknownS5:old19.unknownS5},
    v1:{uniqueS4:new19.uniqueS4,unknownS5:new19.unknownS5},
    v2:{uniqueS4:final19.uniqueS4,alreadyLOSS4:final19.alreadyLOSS4,
      knownS5:final19.knownS5,unknownS5:final19.unknownS5},
    reducedUnknownS5:old19.unknownS5-final19.unknownS5,
    rootCosts:final19.roots.sort((a,b)=>a.unknownS5-b.unknownS5||a.first-b.first)},
  trust:'Reused S4 LOSS labels rely on pinned solver-trusted exact S5 verdicts; all geometry and S5 boundary edges rechecked.',
  newS4LOSSProved:0,newS2RootsClosed:0,emptyBoard:'UNKNOWN'
},null,2));
