#!/usr/bin/env node
'use strict';
// Exact independent replay of the proposed three-for-three {49,60} cover.
// Does NOT claim optimality of the three-swap neighborhood or a game verdict.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../../..');
const {canonical,points,maps,witnesses:cachedWIN4}=require('./audit_win4_exclusion');
require('./verify_central49_two_swap_2542');
function pinned(file,sha){
 const raw=fs.readFileSync(path.join(ROOT,file));
 const git=crypto.createHash('sha1').update(Buffer.from('blob '+raw.length+'\0')).update(raw).digest('hex');
 assert.equal(git,sha,'pinned source changed: '+file);
 return raw.toString('utf8');
}
const before=JSON.parse(pinned('research/experiments/n11-central-19-cover-20261031/central49-two-swap-2542.json',
 'cd5c9b4eb0ec448cdf44bcf5c49265088595b299'));
const doc=JSON.parse(pinned('research/experiments/n11-central-19-cover-20261031/central49-three-swap-2501.json',
 '5db25c9c60fd9514e0f5078a47029e84ee9769ad'));
assert.equal(doc.schema,'n11-central49-terminal-safe-three-swap-v1');
assert.equal(doc.board,11);assert.deepEqual(doc.root_stones,[49,60]);
assert.equal(doc.root_outcome,'UNKNOWN');assert.equal(doc.empty_board_outcome,'UNKNOWN');
assert.equal(doc.source_certificate,'central49-two-swap-2542.json');
assert.deepEqual(doc.known_loss4_classes,before.known_loss4_classes);
const old=before.selected_s4_classes,selected=doc.selected_s4_classes;
const removed=doc.removed_s4_classes,added=doc.added_s4_classes;
assert.equal(old.length,31);assert.equal(selected.length,31);
assert.equal(new Set(selected).size,31);assert.deepEqual(selected,[...selected].sort());
assert.equal(removed.length,3);assert.equal(added.length,3);
assert.equal(new Set(removed).size,3);assert.equal(new Set(added).size,3);
assert(removed.every(k=>old.includes(k)&&!doc.known_loss4_classes.includes(k)));
assert(added.every(k=>!old.includes(k)));
assert.deepEqual(selected,[...old.filter(k=>!removed.includes(k)),...added].sort());
const cacheText=pinned('research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache',
 '2dccf42b92337cbcbfb62ea5c77db487b1ad8ead');
const cache=new Map();
for(const line of cacheText.split(/\r?\n/)){
 if(!line||line.startsWith('#'))continue;
 const f=line.split(',');assert.equal(f.length,6);
 assert.equal(f[0],'s5verdict');assert.equal(f[3],'5');assert(['1','2'].includes(f[4]));
 const key=(BigInt(f[1])+(BigInt(f[2])<<64n)).toString(16).padStart(32,'0');
 assert(!cache.has(key));cache.set(key,Number(f[4]));
}
assert.equal(cache.size,5851);
const terminalWIN5=[[5,45,49,53,60],[1,49,59,60,61],[37,49,59,60,61],
 [49,51,59,60,71],[2,49,59,60,61],[14,49,59,60,61]];
const win4=new Set(cachedWIN4.keys());
for(const p of terminalWIN5)for(let i=0;i<5;i++)
 win4.add(canonical(p.filter((_,j)=>j!==i)));
assert.equal(win4.size,573);
function det4(p){
 const a=p.map(i=>{const x=i%11,y=Math.floor(i/11);return[x*x+y*y,x,y];});
 const b=a.slice(1).map(row=>row.map((v,j)=>v-a[0][j]));
 return b[0][0]*(b[1][1]*b[2][2]-b[1][2]*b[2][1])
 -b[0][1]*(b[1][0]*b[2][2]-b[1][2]*b[2][0])
 +b[0][2]*(b[1][0]*b[2][1]-b[1][1]*b[2][0]);
}
function coverage(p){
 let bits=0n;
 for(const m of maps){
  const q=p.map(x=>m[x]);
  if(q.includes(49)&&q.includes(60))
   for(const x of q)if(x!==49&&x!==60)bits|=1n<<BigInt(x);
 }
 return bits;
}
const classes=new Map();
for(let a=0;a<121;a++)if(a!==49&&a!==60)
 for(let b=a+1;b<121;b++)if(b!==49&&b!==60){
  const p=[49,60,a,b];if(det4(p)===0)continue;
  const k=canonical(p);if(!classes.has(k))classes.set(k,coverage(p));
 }
assert.equal(classes.size,3374);
const target=((1n<<121n)-1n)^(1n<<49n)^(1n<<60n);
function checkCover(keys){
 let bits=0n;
 for(const k of keys){
  assert(classes.has(k),'not a legal S4 class: '+k);
  assert(!win4.has(k),'known WIN4 selected: '+k);
  bits|=classes.get(k);
 }
 assert.equal(bits,target,'third-move coverage incomplete');
}
checkCover(old);checkCover(selected);
const memo=new Map();
function children(k){
 if(memo.has(k))return memo.get(k);
 const p=points(k);assert.equal(p.length,4);assert.notEqual(det4(p),0);
 const out=new Set();
 for(let x=0;x<121;x++)if(!p.includes(x)){
  const q=[...p,x];
  let safe=true;
  for(let i=0;i<5;i++)if(det4(q.filter((_,j)=>i!==j))===0){safe=false;break;}
  if(safe)out.add(canonical(q));
 }
 memo.set(k,out);return out;
}
function score(keys){
 const all=new Set();
 for(const k of keys)for(const child of children(k))all.add(child);
 let knownLoss=0;
 for(const child of all)if(cache.has(child)){
  assert.equal(cache.get(child),2,'known WIN5 child under LOSS4 candidate: '+child);
  knownLoss++;
 }
 return {distinct:all.size,known_loss:knownLoss,unknown:all.size-knownLoss};
}
assert.deepEqual(score(old),{distinct:2857,known_loss:315,unknown:2542});
assert.deepEqual(score(selected),{distinct:2816,known_loss:315,unknown:2501});
assert.deepEqual(score(selected),doc.s5_dependency);
for(const k of doc.known_loss4_classes){
 assert(selected.includes(k));assert([...children(k)].every(c=>cache.get(c)===2),
  'pinned LOSS4 has unknown child: '+k);
}
assert.equal(doc.search.old_unknown_s5,2542);
assert.equal(doc.search.new_unknown_s5,2501);
assert.equal(doc.search.removed_unknown_s5,41);
assert.equal(doc.search.global_optimality_claim,false);
assert.equal(doc.search.three_swap_neighborhood_optimality_claim,false);
console.log(JSON.stringify({schema:doc.schema,root:[49,60],root_outcome:'UNKNOWN',
 selected_s4:31,known_loss4:3,unproved_s4:28,legal_s4_classes:3374,
 known_win4_exclusions:573,distinct_s5:2816,known_loss5:315,unknown_s5:2501,
 improvement_over_two_swap:41,geometric_coverage:119,
 caveat:'Three-swap candidate only; frozen S5 cache is solver-trusted. No new game verdict.'},null,2));
