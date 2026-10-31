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
 assert(w>=3&&w<=4,'13-witness clique not complete');
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
console.log(JSON.stringify(report,null,2));
