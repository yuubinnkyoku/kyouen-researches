#!/usr/bin/env node
'use strict';
// Independently reconstruct S5 sharing for the fixed {49,60} cover.
// This is a scheduling/certificate-dependency audit, not a game verdict.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const here=__dirname;
const cert=JSON.parse(fs.readFileSync(path.join(here,'win4-safe-31-loss4-reuse-49.json'),'utf8'));
const frontier=JSON.parse(fs.readFileSync(path.join(here,'central49-frontier-ownership.json'),'utf8'));
assert.deepEqual(cert.root_stones,[49,60]);
assert.equal(cert.root_outcome,'UNKNOWN');
assert.equal(frontier.rootOutcome,'UNKNOWN');
const keys=cert.selected_s4_classes;
assert.equal(keys.length,31);
assert.deepEqual(keys,frontier.witnesses.map(w=>w.s4));
const maps=Array.from({length:8},(_,j)=>Array.from({length:121},(_,i)=>{
 const x=i%11,y=Math.floor(i/11);
 const [u,v]=[[x,y],[10-y,x],[10-x,10-y],[y,10-x],
  [10-x,y],[10-y,10-x],[x,10-y],[y,x]][j];
 return 11*v+u;
}));
function points(k){
 assert.match(k,/^[0-9a-f]{32}$/);
 const n=BigInt('0x'+k);
 assert.equal(n>>121n,0n);
 const p=[];for(let i=0;i<121;i++)if(n&(1n<<BigInt(i)))p.push(i);
 return p;
}
function canonical(p){
 let best=null;
 for(const m of maps){
  let n=0n;for(const i of p)n|=1n<<BigInt(m[i]);
  if(best===null||n<best)best=n;
 }
 return best.toString(16).padStart(32,'0');
}
function det4(p){
 const a=p.map(i=>{const x=i%11,y=Math.floor(i/11);return[x*x+y*y,x,y]});
 const b=a.slice(1).map(r=>r.map((v,j)=>v-a[0][j]));
 return b[0][0]*(b[1][1]*b[2][2]-b[1][2]*b[2][1])
  -b[0][1]*(b[1][0]*b[2][2]-b[1][2]*b[2][0])
  +b[0][2]*(b[1][0]*b[2][1]-b[1][1]*b[2][0]);
}
const owners=new Map();
for(let i=0;i<keys.length;i++){
 const p=points(keys[i]);
 assert.equal(p.length,4);
 assert.equal(canonical(p),keys[i]);
 assert.notEqual(det4(p),0);
 const children=new Set();
 for(let x=0;x<121;x++)if(!p.includes(x)){
  const q=[...p,x];
  let legal=true;
  for(let j=0;j<4;j++)if(det4(q.filter((_,k)=>k!==j))===0){legal=false;break;}
  if(legal)children.add(canonical(q));
 }
 assert.equal(children.size,frontier.witnesses[i].legalS5Children);
 for(const c of children){
  if(!owners.has(c))owners.set(c,[]);
  owners.get(c).push(i);
 }
}
assert.equal(owners.size,2840);
const pair=Array.from({length:31},()=>Array(31).fill(0));
let shared=0;
for(const indices of owners.values()){
 assert(indices.length<=2,'three-way S5 overlap');
 if(indices.length===2){
  const [i,j]=indices;
  pair[i][j]++;pair[j][i]++;shared++;
 }
}
assert.equal(shared,301);
const unknown=frontier.witnesses.map((w,i)=>w.status==='UNKNOWN'?i:null).filter(i=>i!==null);
assert.equal(unknown.length,28);
const known=frontier.witnesses.map((w,i)=>w.status!=='UNKNOWN'?i:null).filter(i=>i!==null);
assert.equal(known.length,3);
for(const i of known)assert(pair[i].every(x=>x===0),'known S5 overlap');
for(let i=0;i<31;i++){
 const degree=pair[i].reduce((a,b)=>a+b,0);
 assert.equal(degree,frontier.witnesses[i].sharedUnknownS5,
  'unexpected known shared S5 or incorrect frontier degree');
}
assert.equal(unknown.reduce((s,i)=>s+frontier.witnesses[i].unknownS5,0),2826);
assert.equal(frontier.summary.unknownS5,2525);
assert.equal(frontier.summary.unknownS5Incidences,2826);
const visited=new Set(),components=[];
for(const i of unknown)if(!visited.has(i)){
 const stack=[i],group=[];visited.add(i);
 while(stack.length){
  const u=stack.pop();group.push(u);
  for(const v of unknown)if(pair[u][v]&&!visited.has(v)){
   visited.add(v);stack.push(v);
  }
 }
 components.push(group.sort((a,b)=>a-b));
}
const shapes=components.map(g=>g.length).sort((a,b)=>a-b);
assert.deepEqual(shapes,[1,1,1,1,1,1,1,1,1,1,1,1,1,2,13]);
const clique=components.find(g=>g.length===13);
assert.deepEqual(clique,Array.from({length:13},(_,i)=>i+11));
let cliquePairs=0,cliqueOverlap=0;
for(let a=0;a<clique.length;a++)for(let b=a+1;b<clique.length;b++){
 const w=pair[clique[a]][clique[b]];
 assert(w>=2&&w<=4,'13-witness clique not complete');
 cliquePairs++;cliqueOverlap+=w;
}
assert.equal(cliquePairs,78);
assert.equal(cliqueOverlap,300);
assert.deepEqual(components.find(g=>g.length===2),[3,27]);
assert.equal(pair[3][27],1);
const uniqueFor=indices=>{
 let sum=indices.reduce((s,i)=>s+frontier.witnesses[i].unknownS5,0);
 for(let a=0;a<indices.length;a++)for(let b=a+1;b<indices.length;b++)
  sum-=pair[indices[a]][indices[b]];
 return sum;
};
assert.equal(uniqueFor(clique),1042);
const schedules={
 // No S5 duplication between workers: optimal peak under this restriction.
 noDuplication:[
  [11,12,13,14,15,16,17,18,19,20,21,22,23],
  [7,8,10,26,30],
  [0,1,24,25,28],
  [2,3,5,27,29]
 ],
 // Deterministic, independently checked four-worker tradeoff; not proven optimal.
 balanced:[
  [2,3,10,24,27,28,29],
  [1,5,7,8,25,26,30],
  [0,11,13,15,17,19,20],
  [12,14,16,18,21,22,23]
 ]
};
function auditSchedule(groups){
 assert.equal(groups.length,4);
 const assigned=groups.flat();
 assert.equal(assigned.length,28);
 assert.deepEqual([...assigned].sort((a,b)=>a-b),unknown);
 const loads=groups.map(uniqueFor);
 const duplication=loads.reduce((a,b)=>a+b,0)-2525;
 let cuts=0;
 for(const i of unknown)for(const j of unknown)if(j>i&&pair[i][j]){
  if(groups.findIndex(g=>g.includes(i))!==groups.findIndex(g=>g.includes(j)))cuts+=pair[i][j];
 }
 assert.equal(duplication,cuts);
 return {loads,peak:Math.max(...loads),crossWorkerDuplicatedS5:duplication};
}
const zero=auditSchedule(schedules.noDuplication);
const balanced=auditSchedule(schedules.balanced);
assert.deepEqual(zero,{loads:[1042,495,494,494],peak:1042,crossWorkerDuplicatedS5:0});
assert.deepEqual(balanced,{loads:[685,689,669,639],peak:689,crossWorkerDuplicatedS5:157});
assert.equal(components.reduce((s,g)=>s+uniqueFor(g),0),2525);
// Any duplication-free partition must place all 13 connected clique witnesses
// on one worker; therefore its peak is at least 1042. The first schedule
// attains that lower bound and is optimal under the zero-duplication condition.
const report={
 schema:'n11-central49-s5-overlap-worker-partition-v1',
 root:[49,60],outcome:'UNKNOWN',
 selectedS4:31,unresolvedS4:28,distinctUnknownS5:2525,
 sharedUnknownS5:301,overlapEdges:79,
 components:{isolated:13,pair:1,clique13:1},
 clique:{witnessIndices:clique,edges:78,sharedUnknownS5:300,distinctUnknownS5:1042},
 schedules:{
  noDuplication:{groups:schedules.noDuplication,...zero,zeroDuplicationPeakOptimal:true},
  balanced:{groups:schedules.balanced,...balanced,optimality:'not established'}
 },
 caveat:'All 28 unresolved S4 are UNKNOWN; child counts are not solve times; shared cache may avoid redundant work.'
};
// Child-level scheduling: the same S5 class is solved by exactly one worker,
// then all dependent S4 witnesses may reuse its verdict. This is a worklist
// partition, NOT a claim of a solved S5, S4, S2, or empty-board position.
const crypto=require('node:crypto');
const ROOT=path.resolve(here,'../../..');
const CACHE_SOURCES=[
 ['research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache',
  '2dccf42b92337cbcbfb62ea5c77db487b1ad8ead'],
 ['research/experiments/n11-boundary-recovery-20261006/output/post-23b52acf-after-round4-s6-escalation-s5-cache-corpus-union.cache',
  '9887a18c0788d26507be7e8e191c26817634a6b6']
];
const cache=new Map();
for(const [relative,expected] of CACHE_SOURCES){
 const raw=fs.readFileSync(path.join(ROOT,relative));
 const actual=crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');
 assert.equal(actual,expected,'S5 source blob changed: '+relative);
 const local=new Map();
 for(const line of raw.toString('utf8').split(/\r?\n/)){
  if(!line||line.startsWith('#'))continue;
  const cols=line.split(',');
  assert.equal(cols.length,6);
  assert.equal(cols[0],'s5verdict');
  assert.equal(cols[3],'5');
  assert(['1','2'].includes(cols[4]));
  assert(/^\d+$/.test(cols[1])&&/^\d+$/.test(cols[2]));
  const lo=BigInt(cols[1]),hi=BigInt(cols[2]);
  assert(lo>=0n&&lo<1n<<64n&&hi>=0n&&hi<1n<<64n);
  const key=(lo+(hi<<64n)).toString(16).padStart(32,'0');
  assert(!local.has(key),'duplicate verdict in one source');
  local.set(key,Number(cols[4]));
 }
 for(const [key,outcome] of local){
  if(cache.has(key))assert.equal(cache.get(key),outcome,'WIN/LOSS CONFLICT: '+key);
  else cache.set(key,outcome);
 }
}
assert.equal(cache.size,5853);
const unresolvedSet=new Set(unknown);
const neededOwners=[...owners].filter(([,indices])=>indices.some(i=>unresolvedSet.has(i)));
assert.equal(neededOwners.length,2528);
const cachedNeeded=neededOwners.filter(([key])=>cache.has(key));
assert.equal(cachedNeeded.length,3);
assert(cachedNeeded.every(([key])=>cache.get(key)===2),'known WIN5 under an unresolved S4');
const pending=neededOwners.filter(([key])=>!cache.has(key)).map(([key])=>key).sort();
assert.equal(pending.length,2525);
const shards=Array.from({length:4},()=>[]);
const assigned=new Map();
for(let rank=0;rank<pending.length;rank++){
 const key=pending[rank],worker=rank%4;
 assert(!assigned.has(key),'duplicate S5 assignment');
 assigned.set(key,worker);shards[worker].push(key);
}
assert.deepEqual(shards.map(s=>s.length),[632,631,631,631]);
assert.equal(new Set(shards.flat()).size,2525);
for(const [key,indices] of neededOwners){
 if(cache.has(key))continue;
 assert(assigned.has(key),'unassigned S5');
 assert(indices.every(i=>unresolvedSet.has(i)),'S5 child also belongs to known LOSS4');
}
const digest=keys=>crypto.createHash('sha256').update(keys.join('\n')+'\n').digest('hex');
const shardHashes=shards.map(digest);
const expectedManifest='18749cc4083357d31c622a8e337cb867bd5700530d0677a9e27dec8197e30e70';
const expectedWorkerHashes=[
 '287d3771d1d15bafd48ec9fa021ceb2a5256dda0c30eedece8029b80faa0795a',
 '5b05d0af10932ca718c2ed960e350dfda4ae25756f6a96431a25dd92bd74e0fe',
 'cce0a24bce8838f33ffaf5f882216a46ab4b8934224a7258151e91ed8177ab18',
 '086f86af2b117ad5f1a6c7e4e5d7fbcae647c85a313e9e3f3771f37298891845'
];
assert.equal(digest(pending),expectedManifest,'pending S5 manifest changed');
assert.deepEqual(shardHashes,expectedWorkerHashes,'S5 worker assignments changed');
assert.notEqual(digest([...pending].reverse()),expectedManifest,'hash negative control');
const witnessShards=unknown.map(i=>{
 const keys=neededOwners.filter(([key,indices])=>!cache.has(key)&&indices.includes(i));
 assert.equal(keys.length,frontier.witnesses[i].unknownS5);
 const counts=Array(4).fill(0);
 for(const [key] of keys)counts[assigned.get(key)]++;
 assert.equal(counts.reduce((a,b)=>a+b,0),frontier.witnesses[i].unknownS5);
 return {witness:i,workerChildCounts:counts};
});
report.childLevelSharding={
 policy:'sorted canonical UNKNOWN S5 keys, zero-based rank modulo 4',
 distinctPendingS5:pending.length,sourceCacheClasses:cache.size,
 knownLOSS5UnderUnresolvedS4:cachedNeeded.length,
 workerLoads:shards.map(s=>s.length),peak:632,crossWorkerDuplicatedS5:0,
 totalChildWork:2525,manifestSha256:digest(pending),workerSha256:shardHashes,
 witnessShards,
 caveat:'Worklist count, not solve-time balance; each S4 remains UNKNOWN until every legal S5 child has verified LOSS evidence.'
};
// An equal-cost, four-worker schedule can prioritize the cheapest unresolved
// S4 witness without changing the 2525-class frontier or duplicating work.
// The original --worker schedule remains byte-for-byte stable for replay.
const priorityS4='00000000000000401002010000000000';
const priorityIndex=keys.indexOf(priorityS4);
assert.equal(priorityIndex,25,'priority witness changed');
assert.equal(frontier.witnesses[priorityIndex].status,'UNKNOWN');
assert.equal(frontier.witnesses[priorityIndex].unknownS5,91);
assert.equal(frontier.witnesses[priorityIndex].knownLossS5,1);
assert.equal(frontier.witnesses[priorityIndex].sharedUnknownS5,0);
assert.equal(Math.min(...unknown.map(i=>frontier.witnesses[i].unknownS5)),91);
const priorityKeys=pending.filter(k=>owners.get(k).includes(priorityIndex));
assert.equal(priorityKeys.length,91);
assert(priorityKeys.every(k=>owners.get(k).length===1),
 'priority witness unexpectedly shares pending S5');
const prioritySet=new Set(priorityKeys);
const priorityOrder=priorityKeys.concat(pending.filter(k=>!prioritySet.has(k)));
assert.equal(priorityOrder.length,2525);
assert.equal(new Set(priorityOrder).size,2525);
assert.deepEqual([...priorityOrder].sort(),pending);
const priorityShards=Array.from({length:4},()=>[]);
for(let rank=0;rank<priorityOrder.length;rank++)
 priorityShards[rank%4].push(priorityOrder[rank]);
assert.deepEqual(priorityShards.map(s=>s.length),[632,631,631,631]);
const priorityLoads=priorityShards.map(s=>s.filter(k=>prioritySet.has(k)).length);
assert.deepEqual(priorityLoads,[23,23,23,22]);
for(const s of priorityShards){
 const firstNonPriority=s.findIndex(k=>!prioritySet.has(k));
 assert(s.slice(firstNonPriority<0?s.length:firstNonPriority)
  .every(k=>prioritySet.has(k)),'priority work not at shard head');
 assert(s.slice(firstNonPriority<0?s.length:firstNonPriority)
  .every(k=>!prioritySet.has(k)),'priority work interleaved');
}
const oldRanks=new Map(pending.map((k,i)=>[k,i]));
const oldFinishRound=Math.max(...priorityKeys.map(k=>Math.floor(oldRanks.get(k)/4)+1));
const priorityFinishRound=Math.max(...priorityLoads);
assert.equal(oldFinishRound,551,'baseline worklist order changed');
assert.equal(priorityFinishRound,23);
assert.equal(priorityFinishRound,Math.ceil(priorityKeys.length/4),
 'priority completion round not optimal in equal-cost model');
report.childLevelSharding.priorityFirst={
 witnessS4:priorityS4,unknownS5:91,alreadyKnownLossS5:1,
 oldFirstPossibleCompletionRound:oldFinishRound,
 newFirstPossibleCompletionRound:priorityFinishRound,
 lowerBoundRound:Math.ceil(priorityKeys.length/4),
 priorityWorkerLoads:priorityLoads,
 workerLoads:priorityShards.map(s=>s.length),
 distinctPendingS5:priorityOrder.length,crossWorkerDuplicatedS5:0,
 priorityManifestSha256:digest(priorityOrder),
 priorityWorkerSha256:priorityShards.map(digest),
 caveat:'Rounds assume one S5 per worker per round, equal cost and all 91 new verdicts LOSS. This is a conditional scheduling bound, not a game verdict or measured speedup.'
};
const args=process.argv.slice(2);
if(args.length===0)console.log(JSON.stringify(report,null,2));
else if(args.length===2&&args[0]==='--worker'&&/^[0-3]$/.test(args[1]))
 process.stdout.write(shards[Number(args[1])].join('\n')+'\n');
else if(args.length===2&&args[0]==='--priority-worker'&&/^[0-3]$/.test(args[1]))
 process.stdout.write(priorityShards[Number(args[1])].join('\n')+'\n');
else throw new Error('usage: node audit_central49_worker_partition.js [--worker 0|1|2|3 | --priority-worker 0|1|2|3]');
