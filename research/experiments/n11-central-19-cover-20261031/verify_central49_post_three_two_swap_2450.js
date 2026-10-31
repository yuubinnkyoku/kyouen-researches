#!/usr/bin/env node
'use strict';
// Exhaustive two-for-two replacement audit of the {49,60} 31-S4 cover.
// Every label is in ORIGINAL-FIRST polarity. This is a conditional plan, not a game verdict.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../../..');
const {canonical,points,maps,witnesses:cachedWIN4}=require('./audit_win4_exclusion');
// Revalidate the pinned source, terminal-only WIN5 exclusions, and single-swap boundary.
require('./verify_central49_three_swap_2501');
function pinned(file,sha){
  const raw=fs.readFileSync(path.join(ROOT,file));
  const git=crypto.createHash('sha1').update(Buffer.from('blob '+raw.length+'\0')).update(raw).digest('hex');
  assert.equal(git,sha,'changed pinned source '+file);
  return raw.toString('utf8');
}
const old=JSON.parse(pinned('research/experiments/n11-central-19-cover-20261031/central49-three-swap-2501.json',
  '5db25c9c60fd9514e0f5078a47029e84ee9769ad'));
const next=JSON.parse(pinned('research/experiments/n11-central-19-cover-20261031/central49-post-three-two-swap-2450.json','77ce6a7e2b1f4fd3d35143acede17da9f0595439'));
assert.equal(next.schema,'n11-central49-terminal-safe-post-three-two-swap-v1');
assert.equal(next.source_certificate,'central49-three-swap-2501.json');
assert.equal(next.board,11);
assert.deepEqual(next.root_stones,[49,60]);
assert.equal(next.root_outcome,'UNKNOWN');
assert.equal(next.empty_board_outcome,'UNKNOWN');
assert.equal(next.source_certificate,'central49-three-swap-2501.json');
assert.deepEqual(next.known_loss4_classes,old.known_loss4_classes);
const selected=old.selected_s4_classes, after=next.selected_s4_classes;
const removed=next.removed_s4_classes, added=next.added_s4_classes;
assert.equal(selected.length,31);assert.equal(after.length,31);
assert.equal(new Set(after).size,31);assert.deepEqual(after,[...after].sort());
assert.equal(removed.length,2);assert.equal(added.length,2);
assert.equal(new Set(removed).size,2);assert.equal(new Set(added).size,2);
assert(removed.every(k=>selected.includes(k)&&!old.known_loss4_classes.includes(k)));
assert(added.every(k=>!selected.includes(k)));
assert.deepEqual(after,[...selected.filter(k=>!removed.includes(k)),...added].sort());
const cacheText=pinned('research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache',
 '2dccf42b92337cbcbfb62ea5c77db487b1ad8ead');
const cache=new Map();
for(const line of cacheText.split(/\r?\n/)){
 if(!line||line.startsWith('#'))continue;
 const f=line.split(',');
 assert.equal(f.length,6);assert.equal(f[0],'s5verdict');assert.equal(f[3],'5');
 assert(['1','2'].includes(f[4]));
 const k=(BigInt(f[1])+(BigInt(f[2])<<64n)).toString(16).padStart(32,'0');
 assert(!cache.has(k));cache.set(k,Number(f[4]));
}
assert.equal(cache.size,5851);
const terminalWIN5=[[5,45,49,53,60],[1,49,59,60,61],[37,49,59,60,61],
 [49,51,59,60,71],[2,49,59,60,61],[14,49,59,60,61]];
const terminalWIN4=new Set();
for(const p of terminalWIN5)for(let i=0;i<5;i++)
 terminalWIN4.add(canonical(p.filter((_,j)=>j!==i)));
assert.equal(terminalWIN4.size,24);
const win4=new Set([...cachedWIN4.keys(),...terminalWIN4]);
assert.equal(cachedWIN4.size,549);assert.equal(win4.size,573);
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
 let covered=0n;
 for(const k of keys){
  assert(classes.has(k),'invalid S4 '+k);
  assert(!win4.has(k),'known WIN4 selected '+k);
  covered|=classes.get(k);
 }
 assert.equal(covered,target,'incomplete third-move cover');
}
checkCover(selected);checkCover(after);
assert.throws(()=>checkCover(after.slice(1)),/incomplete third-move cover/);
const memo=new Map();
function children(key){
 if(memo.has(key))return memo.get(key);
 const p=points(key);assert.equal(p.length,4);assert.notEqual(det4(p),0);
 const all=new Set(),unknown=new Set();
 for(let x=0;x<121;x++)if(!p.includes(x)){
  let safe=true;
  for(let i=0;i<4;i++)if(det4([...p.filter((_,j)=>i!==j),x])===0){safe=false;break;}
  if(!safe)continue;
  const k=canonical([...p,x]);all.add(k);
  assert.notEqual(cache.get(k),1,'known WIN5 child under LOSS4 candidate '+key);
  if(!cache.has(k))unknown.add(k);
 }
 const result={all,unknown};memo.set(key,result);return result;
}
function score(keys){
 const all=new Set(),unknown=new Set();
 for(const k of keys){const c=children(k);for(const x of c.all)all.add(x);for(const x of c.unknown)unknown.add(x);}
 return {distinct:all.size,known_loss:all.size-unknown.size,unknown:unknown.size};
}
assert.deepEqual(score(selected),{distinct:2816,known_loss:315,unknown:2501});
assert.deepEqual(score(after),{distinct:2765,known_loss:315,unknown:2450});
assert.deepEqual(next.s5_dependency,score(after));
for(const k of next.known_loss4_classes){
 assert(after.includes(k));
 assert.equal(children(k).unknown.size,0,'incomplete pinned LOSS4 '+k);
}
const fixed=new Set(next.known_loss4_classes),present=new Set(selected);
const eligible=[...classes].filter(([k])=>!win4.has(k)&&!present.has(k));
assert.equal(eligible.length,3260);
const byPoint=Array.from({length:121},()=>[]);
for(const entry of eligible)for(let i=0;i<121;i++)
 if(entry[1]&(1n<<BigInt(i)))byPoint[i].push(entry);
let singleFeasible=0,singleImprovements=0;
for(let i=0;i<selected.length;i++)if(!fixed.has(selected[i])){
 const kept=selected.filter((_,j)=>i!==j);
 const missing=target&~kept.reduce((v,k)=>v|classes.get(k),0n);
 for(const [k,m] of eligible)if((m&missing)===missing){
  singleFeasible++;
  if(score([...kept,k]).unknown<2501)singleImprovements++;
 }
}
assert.equal(singleFeasible,35);
assert.equal(singleImprovements,0);
let pairs=0,solutions=0,improvements=0,best=null,minimum=Infinity,minCount=0;
for(let i=0;i<selected.length;i++)if(!fixed.has(selected[i]))
 for(let j=i+1;j<selected.length;j++)if(!fixed.has(selected[j])){
  pairs++;
  let kept=0n;
  for(let h=0;h<selected.length;h++)if(h!==i&&h!==j)kept|=classes.get(selected[h]);
  const missing=target&~kept;
  const pivots=[];
  for(let t=0;t<121;t++)if(missing&(1n<<BigInt(t)))pivots.push(t);
  assert(pivots.length>0);
  const pivot=pivots.reduce((a,b)=>byPoint[a].length<byPoint[b].length?a:b);
  const keptUnknown=new Set();
  for(let h=0;h<selected.length;h++)if(h!==i&&h!==j)
   for(const x of children(selected[h]).unknown)keptUnknown.add(x);
  const seen=new Set();
  for(const [ak,am] of byPoint[pivot]){
   const remaining=missing&~am;
   assert(remaining!==0n,'unexpected 30-class geometric cover');
   for(const [bk,bm] of eligible){
    if(ak===bk||(bm&remaining)!==remaining)continue;
    const pair=[ak,bk].sort(),signature=pair.join(':');
    if(seen.has(signature))continue;
    seen.add(signature);solutions++;
    const union=new Set(keptUnknown);
    for(const x of children(pair[0]).unknown)union.add(x);
    for(const x of children(pair[1]).unknown)union.add(x);
    const cost=union.size;
    if(cost<2501)improvements++;
    if(cost<minimum){
     minimum=cost;minCount=1;best={removed:[selected[i],selected[j]],added:pair};
    }else if(cost===minimum)minCount++;
   }
  }
 }
assert.equal(pairs,378);
assert.equal(solutions,2817);
assert.equal(improvements,12);
assert.equal(minimum,2450);
assert.equal(minCount,1);
assert.deepEqual(best,{removed,added});
assert.deepEqual(next.search,{
  "method": "exhaustive one- and two-for-two replacement of the fixed 2501-class cover",
  "old_unknown_s5": 2501,
  "new_unknown_s5": 2450,
  "removed_unknown_s5": 51,
  "one_swap_feasible": 35,
  "one_swap_improvements": 0,
  "two_swap_feasible": 2817,
  "two_swap_improvements": 12,
  "exact_two_swap_neighborhood_optimum": true,
  "global_optimality_claim": false
});
console.log(JSON.stringify({schema:next.schema,root:[49,60],root_outcome:'UNKNOWN',old_unknown_s5:2501,new_unknown_s5:2450,removed_unknown_s5:51,geometric_classes:3374,eligible:3260,removed_pairs:378,feasible_two_swaps:solutions,strict_improvements:improvements,best_count:minCount,known_loss4:3,unproved_s4:28,distinct_s5:2765,known_loss5:315,trust:'Conditional plan, not a verdict.'},null,2));
