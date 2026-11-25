#!/usr/bin/env node
'use strict';
// Exhaustive fixed-cover three-for-three neighborhood and independent S5 dependency audit.
// All verdict labels use original-first polarity; the cover is conditional, not a game proof.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../../..');
const {canonical,points,maps,witnesses}=require('./audit_win4_exclusion');
require('./verify_central49_post_three_two_swap_2345');
function pinned(rel,sha){
 const raw=fs.readFileSync(path.join(ROOT,rel));
 const actual=crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');
 assert.equal(actual,sha,'changed pinned input: '+rel);
 return raw.toString('utf8');
}
const base='research/experiments/n11-central-19-cover-20261031/';
const previous=JSON.parse(pinned(base+'central49-post-three-two-swap-2345.json',
 '72415276c55528dfa83b7a151363cf4a662807b5'));
const next=JSON.parse(pinned(base+'central49-three-swap-2277.json','2f5a19a9f91f911cba1e83cdfb0f6bca1e2f69c1'));
assert.equal(next.schema,'n11-central49-terminal-safe-three-swap-2277-v1');
assert.equal(next.board,11);
assert.deepEqual(next.root_stones,[49,60]);
assert.equal(next.root_outcome,'UNKNOWN');
assert.equal(next.empty_board_outcome,'UNKNOWN');
assert.equal(next.source_certificate,'central49-post-three-two-swap-2345.json');
assert.deepEqual(next.known_loss4_classes,previous.known_loss4_classes);
const selected=previous.selected_s4_classes,after=next.selected_s4_classes;
const removed=next.removed_s4_classes,added=next.added_s4_classes;
assert.equal(selected.length,31);
assert.equal(after.length,31);
assert.equal(new Set(after).size,31);
assert.deepEqual(after,[...after].sort());
assert.equal(removed.length,3);
assert.equal(added.length,3);
assert.deepEqual(removed,[...removed].sort());
assert.deepEqual(added,[...added].sort());
assert(removed.every(k=>selected.includes(k)&&!next.known_loss4_classes.includes(k)));
assert(added.every(k=>!selected.includes(k)));
assert.deepEqual(after,[...selected.filter(k=>!removed.includes(k)),...added].sort());
const raw=pinned('research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache',
 '2dccf42b92337cbcbfb62ea5c77db487b1ad8ead');
const cache=new Map();
for(const line of raw.split(/\r?\n/)){
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
 [49,51,59,60,71],[2,49,59,60,61],[14,49,59,60,61]]){
 for(const x of p)blocked.add(canonical(p.filter(y=>y!==x)));
}
assert.equal(blocked.size,573);
function det4(p){
 const a=p.map(i=>{const x=i%11,y=Math.floor(i/11);return[x*x+y*y,x,y]});
 const b=a.slice(1).map(r=>r.map((v,j)=>v-a[0][j]));
 return b[0][0]*(b[1][1]*b[2][2]-b[1][2]*b[2][1])
  -b[0][1]*(b[1][0]*b[2][2]-b[1][2]*b[2][0])
  +b[0][2]*(b[1][0]*b[2][1]-b[1][1]*b[2][0]);
}
const bits=Array.from({length:121},(_,i)=>1n<<BigInt(i));
function coverage(p){
 let mask=0n;
 for(const t of maps){
  const q=p.map(x=>t[x]);
  if(q.includes(49)&&q.includes(60))
   for(const x of q)if(x!==49&&x!==60)mask|=bits[x];
 }
 return mask;
}
const classes=new Map();
for(let a=0;a<121;a++)if(a!==49&&a!==60)
 for(let b=a+1;b<121;b++)if(b!==49&&b!==60){
  const p=[49,60,a,b];
  if(det4(p)===0)continue;
  const k=canonical(p);
  if(!classes.has(k))classes.set(k,coverage(p));
 }
assert.equal(classes.size,3374);
const target=((1n<<121n)-1n)^bits[49]^bits[60];
function checkCover(keys){
 let mask=0n;
 for(const k of keys){
  assert(classes.has(k),'invalid S4: '+k);
  assert(!blocked.has(k),'known WIN4 selected: '+k);
  mask|=classes.get(k);
 }
 assert.equal(mask,target,'incomplete third-move cover');
}
checkCover(selected);checkCover(after);
const dual=[5,6,7,8,9,10,16,17,18,19,20,21,27,28,29,30,31,32,
 38,39,40,41,42,43,50,51,52,53,54,62,63,64,65,72,73,74,75,76,
 82,83,84,85,86,87,93,94,95,96,97,98,104,105,106,107,108,109,
 115,116,117,118,119,120];
assert.equal(dual.length,62);
assert.equal(new Set(dual).size,62);
function dualPair(mask){
 const result=[];
 for(let i=0;i<dual.length;i++)if(mask&bits[dual[i]])result.push(i);
 return result;
}
for(const mask of classes.values())assert(dualPair(mask).length<=2,'dual lower bound invalid');
function checkTight(keys){
 const covered=new Set();
 for(const k of keys){
  const pair=dualPair(classes.get(k));
  assert.equal(pair.length,2,'selected class is not dual-tight');
  for(const x of pair){assert(!covered.has(x),'dual overlap');covered.add(x);}
 }
 assert.equal(covered.size,62);
}
checkTight(selected);checkTight(after);
const fixed=new Set(next.known_loss4_classes),selectedSet=new Set(selected);
const byPair=new Map();
for(const [k,mask] of classes){
 const pair=dualPair(mask);
 if(pair.length!==2||blocked.has(k)||selectedSet.has(k))continue;
 const id=pair[0]*62+pair[1];
 if(!byPair.has(id))byPair.set(id,[]);
 byPair.get(id).push({k,mask});
}
const idOf=new Map(),counter=new Uint16Array(1000000),seen=new Uint32Array(1000000);
const memo=new Map();let nextID=0,epoch=0;
function children(k){
 if(memo.has(k))return memo.get(k);
 const p=points(k);assert.equal(p.length,4);assert.notEqual(det4(p),0);
 const all=new Set(),unknown=[];
 for(let x=0;x<121;x++)if(!p.includes(x)){
  let safe=true;
  for(let i=0;i<4;i++)
   if(det4([...p.filter((_,j)=>i!==j),x])===0){safe=false;break;}
  if(!safe)continue;
  all.add(canonical([...p,x]));
 }
 for(const child of all){
  assert.notEqual(cache.get(child),1,'WIN5 under candidate LOSS4: '+k);
  if(cache.has(child))continue;
  if(!idOf.has(child))idOf.set(child,nextID++);
  assert(nextID<counter.length,'S5 ID capacity exceeded');
  unknown.push(idOf.get(child));
 }
 const out={all,unknown};
 memo.set(k,out);return out;
}
for(const k of selected)for(const id of children(k).unknown)counter[id]++;
let baseline=0;
for(let i=0;i<nextID;i++)if(counter[i])baseline++;
assert.equal(baseline,2345);
const free=selected.map((k,i)=>fixed.has(k)?-1:i).filter(i=>i>=0);
assert.equal(free.length,28);
let triples=0,matchings=0,combos=0,feasible=0,improvements=0;
let minimum=baseline,minCount=0,best=null;
for(let ii=0;ii<free.length;ii++)
 for(let jj=ii+1;jj<free.length;jj++)
  for(let kk=jj+1;kk<free.length;kk++){
   triples++;
   const rem=[free[ii],free[jj],free[kk]];
   let kept=0n;
   for(let i=0;i<31;i++)if(!rem.includes(i))kept|=classes.get(selected[i]);
   const missing=target&~kept;
   const vertices=rem.flatMap(i=>dualPair(classes.get(selected[i])));
   assert.equal(new Set(vertices).size,6);
   let keptCount=baseline;
   for(const i of rem)for(const id of children(selected[i]).unknown){
    counter[id]--;
    if(counter[id]===0)keptCount--;
   }
   function match(pairs,remaining){
    if(remaining.length===0){
     matchings++;
     const choices=pairs.map(([a,b])=>byPair.get(Math.min(a,b)*62+Math.max(a,b))||[]);
     if(choices.some(a=>a.length===0))return;
     for(const a of choices[0])for(const b of choices[1])for(const c of choices[2]){
      combos++;
      if(((a.mask|b.mask|c.mask)&missing)!==missing)continue;
      feasible++;epoch++;
      let cost=keptCount;
      for(const item of [a,b,c])for(const id of children(item.k).unknown){
       if(counter[id]===0&&seen[id]!==epoch){seen[id]=epoch;cost++;}
      }
      if(cost<baseline)improvements++;
      if(cost<minimum){
       minimum=cost;minCount=1;
       best={removed:rem.map(i=>selected[i]),added:[a.k,b.k,c.k].sort()};
      }else if(cost===minimum)minCount++;
     }
     return;
    }
    const a=remaining[0];
    for(let j=1;j<remaining.length;j++)
     match([...pairs,[a,remaining[j]]],remaining.filter((_,i)=>i!==0&&i!==j));
   }
   match([],vertices);
   for(const i of rem)for(const id of children(selected[i]).unknown)counter[id]++;
  }
assert.equal(triples,3276);
assert.equal(matchings,49140);
assert.equal(combos,237342);
assert.equal(feasible,223218);
assert.equal(improvements,74);
assert.equal(minimum,2277);
assert.equal(minCount,1);
assert.deepEqual(best,{removed,added});
const allS5=new Set(),unknownS5=new Set();
for(const k of after){
 const c=children(k);
 for(const x of c.all)allS5.add(x);
 for(const id of c.unknown)unknownS5.add(id);
}
assert.deepEqual(next.s5_dependency,{
 distinct:allS5.size,known_loss:allS5.size-unknownS5.size,unknown:unknownS5.size
});
assert.deepEqual(next.s5_dependency,{distinct:2591,known_loss:314,unknown:2277});
for(const k of fixed)assert.equal(children(k).unknown.length,0,'pinned LOSS4 incomplete');
assert.deepEqual(next.search,{
 method:'exhaustive three-for-three replacement of fixed 2345-class cover using a verified 62-point half-dual',
 old_unknown_s5:2345,new_unknown_s5:2277,removed_unknown_s5:68,
 removed_triples:3276,dual_pair_matchings:49140,candidate_triples:237342,
 feasible_three_swaps:223218,strict_improvements:74,best_count:1,
 exact_three_swap_neighborhood_optimum:true,global_optimality_claim:false
});
console.log(JSON.stringify({
 schema:next.schema,root:[49,60],root_outcome:'UNKNOWN',
 prior_unknown_s5:2345,new_unknown_s5:2277,known_loss4:3,unproved_s4:28,
 dual_points:62,removed_triples:triples,candidate_triples:combos,
 feasible_three_swaps:feasible,improvements,best_count:minCount,
 trust:'Conditional certificate plan, not a game verdict.'
},null,2));
