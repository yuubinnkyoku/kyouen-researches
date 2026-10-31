#!/usr/bin/env node
'use strict';
// Exhaustive two-for-two neighborhood of the fixed 2277-class S4 cover.
// Counts are conditional proof dependencies, not game outcomes.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../../..');
const {canonical,points,maps,witnesses}=require('./audit_win4_exclusion');
const base='research/experiments/n11-central-19-cover-20261031/';
function pinned(rel,sha) {
 const raw=fs.readFileSync(path.join(ROOT,rel));
 const actual=crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');
 assert.equal(actual,sha,'pinned input changed: '+rel);
 return raw.toString('utf8');
}
const previous=JSON.parse(pinned(base+'central49-three-swap-2277.json',
 '2f5a19a9f91f911cba1e83cdfb0f6bca1e2f69c1'));
const next=JSON.parse(fs.readFileSync(path.join(__dirname,'central49-post-three-two-swap-2221.json'),'utf8'));
assert.equal(next.schema,'n11-central49-terminal-safe-post-three-two-swap-2221-v1');
assert.equal(next.board,11);
assert.deepEqual(next.root_stones,[49,60]);
assert.equal(next.root_outcome,'UNKNOWN');
assert.equal(next.empty_board_outcome,'UNKNOWN');
assert.equal(next.source_certificate,'central49-three-swap-2277.json');
assert.deepEqual(next.known_loss4_classes,previous.known_loss4_classes);
const selected=previous.selected_s4_classes,after=next.selected_s4_classes;
const removed=next.removed_s4_classes,added=next.added_s4_classes;
assert.equal(selected.length,31);
assert.equal(after.length,31);
assert.deepEqual(after,[...new Set(after)].sort());
assert.deepEqual(removed,[...removed].sort());
assert.deepEqual(added,[...added].sort());
assert.equal(removed.length,2);
assert.equal(added.length,2);
assert(removed.every(k=>selected.includes(k)&&!next.known_loss4_classes.includes(k)));
assert(added.every(k=>!selected.includes(k)));
assert.deepEqual(after,[...selected.filter(k=>!removed.includes(k)),...added].sort());
const raw=pinned('research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache',
 '2dccf42b92337cbcbfb62ea5c77db487b1ad8ead');
const cache=new Map();
for(const line of raw.split(/\r?\n/)) {
 if(!line||line.startsWith('#'))continue;
 const f=line.split(',');
 assert.equal(f.length,6);assert.equal(f[0],'s5verdict');assert.equal(f[3],'5');
 assert(['1','2'].includes(f[4]));
 const k=(BigInt(f[1])+(BigInt(f[2])<<64n)).toString(16).padStart(32,'0');
 assert(!cache.has(k));cache.set(k,Number(f[4]));
}
assert.equal(cache.size,5851);
const blocked=new Set(witnesses.keys());
assert.equal(blocked.size,549);
for(const p of [[5,45,49,53,60],[1,49,59,60,61],[37,49,59,60,61],
 [49,51,59,60,71],[2,49,59,60,61],[14,49,59,60,61]]) {
 for(const x of p)blocked.add(canonical(p.filter(y=>y!==x)));
}
assert.equal(blocked.size,573);
function det4(p) {
 const a=p.map(i=>{const x=i%11,y=Math.floor(i/11);return[x*x+y*y,x,y]});
 const b=a.slice(1).map(r=>r.map((v,j)=>v-a[0][j]));
 return b[0][0]*(b[1][1]*b[2][2]-b[1][2]*b[2][1])
  -b[0][1]*(b[1][0]*b[2][2]-b[1][2]*b[2][0])
  +b[0][2]*(b[1][0]*b[2][1]-b[1][1]*b[2][0]);
}
const bits=Array.from({length:121},(_,i)=>1n<<BigInt(i));
function coverage(p) {
 let mask=0n;
 for(const t of maps) {
  const q=p.map(x=>t[x]);
  if(q.includes(49)&&q.includes(60))
   for(const x of q)if(x!==49&&x!==60)mask|=bits[x];
 }
 return mask;
}
const classes=new Map();
for(let a=0;a<121;a++)if(a!==49&&a!==60)
 for(let b=a+1;b<121;b++)if(b!==49&&b!==60) {
  const p=[49,60,a,b];
  if(det4(p)===0)continue;
  const k=canonical(p);
  if(!classes.has(k))classes.set(k,coverage(p));
 }
assert.equal(classes.size,3374);
const target=((1n<<121n)-1n)^bits[49]^bits[60];
const dual=[5,6,7,8,9,10,16,17,18,19,20,21,27,28,29,30,31,32,
 38,39,40,41,42,43,50,51,52,53,54,62,63,64,65,72,73,74,75,76,
 82,83,84,85,86,87,93,94,95,96,97,98,104,105,106,107,108,109,
 115,116,117,118,119,120];
assert.equal(dual.length,62);
function dualPair(mask) {
 const pair=[];
 for(let i=0;i<dual.length;i++)if(mask&bits[dual[i]])pair.push(i);
 return pair;
}
for(const mask of classes.values())assert(dualPair(mask).length<=2);
function checkTightCover(keys) {
 let covered=0n;
 const dualSeen=new Set();
 for(const k of keys) {
  assert(classes.has(k),'invalid S4 class: '+k);
  assert(!blocked.has(k),'known WIN4 selected: '+k);
  const mask=classes.get(k);covered|=mask;
  const pair=dualPair(mask);assert.equal(pair.length,2);
  for(const v of pair) {assert(!dualSeen.has(v),'dual overlap');dualSeen.add(v);}
 }
 assert.equal(covered,target,'third-move coverage incomplete');
 assert.equal(dualSeen.size,62);
}
checkTightCover(selected);
checkTightCover(after);
const selectedSet=new Set(selected),fixed=new Set(next.known_loss4_classes);
const byPair=new Map();
for(const [k,mask] of classes) {
 const p=dualPair(mask);
 if(p.length!==2||blocked.has(k)||selectedSet.has(k))continue;
 const id=p[0]*62+p[1];
 if(!byPair.has(id))byPair.set(id,[]);
 byPair.get(id).push({k,mask});
}
const memo=new Map();
function children(k) {
 if(memo.has(k))return memo.get(k);
 const p=points(k);assert.equal(p.length,4);assert.notEqual(det4(p),0);
 const all=new Set(),unknown=[];
 for(let x=0;x<121;x++)if(!p.includes(x)) {
  let safe=true;
  for(let i=0;i<4;i++)
   if(det4([...p.filter((_,j)=>j!==i),x])===0){safe=false;break;}
  if(safe)all.add(canonical([...p,x]));
 }
 for(const child of all) {
  assert.notEqual(cache.get(child),1,'cached WIN5 under S4: '+k);
  if(!cache.has(child))unknown.push(child);
 }
 const out={all,unknown};
 memo.set(k,out);return out;
}
const counts=new Map();
for(const k of selected)for(const child of children(k).unknown)
 counts.set(child,(counts.get(child)||0)+1);
assert.equal(counts.size,2277);
const free=selected.filter(k=>!fixed.has(k));
assert.equal(free.length,28);
let pairs=0,candidates=0,feasible=0,improvements=0;
let minimum=2277,bestCount=0,best=null;
for(let ai=0;ai<free.length;ai++)for(let bi=ai+1;bi<free.length;bi++) {
 pairs++;
 const a=free[ai],b=free[bi];
 const vertices=[...dualPair(classes.get(a)),...dualPair(classes.get(b))];
 assert.equal(new Set(vertices).size,4);
 let kept=0n;
 for(const k of selected)if(k!==a&&k!==b)kept|=classes.get(k);
 const missing=target&~kept;
 let keptCount=2277;
 for(const k of [a,b])for(const child of children(k).unknown) {
  const n=counts.get(child)-1;
  counts.set(child,n);
  if(n===0)keptCount--;
 }
 const [v0,v1,v2,v3]=vertices;
 for(const pairing of [
  [[v0,v1],[v2,v3]],[[v0,v2],[v1,v3]],[[v0,v3],[v1,v2]]
 ]) {
  const options=pairing.map(([x,y])=>byPair.get(Math.min(x,y)*62+Math.max(x,y))||[]);
  for(const x of options[0])for(const y of options[1]) {
   candidates++;
   if(((x.mask|y.mask)&missing)!==missing)continue;
   feasible++;
   let cost=keptCount;
   const seen=new Set();
   for(const item of [x,y])for(const child of children(item.k).unknown) {
    // A child absent from the original cover has undefined count, not zero.
    if(!(counts.get(child)>0)&&!seen.has(child)){cost++;seen.add(child);}
   }
   if(cost<2277)improvements++;
   if(cost<minimum) {
    minimum=cost;bestCount=1;
    best={removed:[a,b].sort(),added:[x.k,y.k].sort()};
   } else if(cost===minimum)bestCount++;
  }
 }
 for(const k of [a,b])for(const child of children(k).unknown)
  counts.set(child,counts.get(child)+1);
}
assert.equal(pairs,378);
assert.equal(candidates,3157);
assert.equal(feasible,3030);
assert.equal(improvements,2);
assert.equal(minimum,2221);
assert.equal(bestCount,1);
assert.deepEqual(best,{removed,added});
const all=new Set(),unknown=new Set();
for(const k of after) {
 const cs=children(k);
 for(const child of cs.all)all.add(child);
 for(const child of cs.unknown)unknown.add(child);
}
assert.deepEqual(next.s5_dependency,{distinct:all.size,known_loss:all.size-unknown.size,unknown:unknown.size});
assert.deepEqual(next.s5_dependency,{distinct:2535,known_loss:314,unknown:2221});
for(const k of fixed)assert.equal(children(k).unknown.length,0);
const priority=after.filter(k=>!fixed.has(k))
 .map(k=>({key:k,count:children(k).unknown.length}))
 .sort((a,b)=>a.count-b.count||a.key.localeCompare(b.key))[0];
assert.deepEqual(priority,{key:'00000000000000003800800000000000',count:94});
assert.deepEqual(next.search,{
 method:'exhaustive two-for-two replacement of fixed 2277-class cover using verified 62-point dual',
 old_unknown_s5:2277,new_unknown_s5:2221,removed_unknown_s5:56,
 removed_pairs:378,candidate_pairs:3157,feasible_two_swaps:3030,
 strict_improvements:2,best_count:1,
 exact_two_swap_neighborhood_optimum:true,global_optimality_claim:false
});
console.log(JSON.stringify({
 schema:next.schema,root:[49,60],root_outcome:'UNKNOWN',
 old_unknown_s5:2277,new_unknown_s5:2221,known_loss4:3,unproved_s4:28,
 removed_pairs:pairs,candidate_pairs:candidates,feasible_two_swaps:feasible,
 improvements,best_count:bestCount,priority_s4:priority.key,
 priority_unknown_s5:priority.count,
 trust:'Conditional certificate plan, not a game verdict.'
},null,2));
