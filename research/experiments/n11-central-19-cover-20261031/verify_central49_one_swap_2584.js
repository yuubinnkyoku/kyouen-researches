#!/usr/bin/env node
'use strict';
// Reproducible exhaustive one-for-one neighborhood audit of the repaired {49,60} cover.
// All verdicts are ORIGINAL-FIRST polarity; this constructs a proof plan, not a root verdict.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../../..');
const {canonical,points,maps,witnesses:cachedWIN4}=require('./audit_win4_exclusion');
// Revalidate the 2-for-2 repair, all six terminal-only receipts, and the 31-class lower bound.
require('./verify_central49_terminal_safe_repair');
function pinned(file,sha){
  const raw=fs.readFileSync(path.join(ROOT,file));
  const git=crypto.createHash('sha1').update(Buffer.from('blob '+raw.length+'\0')).update(raw).digest('hex');
  assert.equal(git,sha,'changed pinned source '+file);
  return raw.toString('utf8');
}
const original=JSON.parse(pinned('research/experiments/n11-central-19-cover-20261031/central49-terminal-win5-safe-repair.json','1f60bff453f727b9a2db1d53d248b528d75bf8f1'));
const next=JSON.parse(fs.readFileSync(path.join(__dirname,'central49-one-swap-2584.json'),'utf8'));
assert.equal(next.schema,'n11-central49-terminal-safe-one-swap-v1');
assert.equal(next.board,11);
assert.deepEqual(next.root_stones,[49,60]);
assert.equal(next.root_outcome,'UNKNOWN');
assert.equal(next.empty_board_outcome,'UNKNOWN');
assert.equal(next.source_certificate,'central49-terminal-win5-safe-repair.json');
assert.deepEqual(next.known_loss4_classes,original.known_loss4_classes);
const old=original.selected_s4_classes, selected=next.selected_s4_classes;
assert.equal(old.length,31);assert.equal(selected.length,31);
assert.deepEqual([...selected].sort(),selected);
assert.equal(new Set(selected).size,31);
assert(old.includes(next.removed_s4_class));
assert(!old.includes(next.added_s4_class));
assert(!selected.includes(next.removed_s4_class));
assert.deepEqual(selected,[...old.filter(k=>k!==next.removed_s4_class),next.added_s4_class].sort());
assert(!next.known_loss4_classes.includes(next.removed_s4_class));
const terminalRoots=[[5,45,49,53,60],[1,49,59,60,61],
  [37,49,59,60,61],[49,51,59,60,71],[2,49,59,60,61],[14,49,59,60,61]];
const terminalWIN4=new Set();
for(const p of terminalRoots)for(let i=0;i<5;i++)
  terminalWIN4.add(canonical(p.filter((_,j)=>i!==j)));
assert.equal(terminalWIN4.size,24);
const cacheText=pinned('research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache',
  '2dccf42b92337cbcbfb62ea5c77db487b1ad8ead');
const cache=new Map();
for(const line of cacheText.split(/\r?\n/)){
  if(!line||line.startsWith('#'))continue;
  const f=line.split(',');
  assert.equal(f.length,6);assert.equal(f[0],'s5verdict');assert.equal(f[3],'5');
  const key=(BigInt(f[1])+(BigInt(f[2])<<64n)).toString(16).padStart(32,'0');
  assert(!cache.has(key));assert([1,2].includes(Number(f[4])));
  cache.set(key,Number(f[4]));
}
assert.equal(cache.size,5851);
assert.equal([...cache.values()].filter(v=>v===1).length,159);
const win4=new Set([...cachedWIN4.keys(),...terminalWIN4]);
assert.equal(cachedWIN4.size,549);
assert.equal(win4.size,573);
function det4(p){
  const a=p.map(i=>{const x=i%11,y=Math.floor(i/11);return[x*x+y*y,x,y];});
  const b=a.slice(1).map(r=>r.map((v,j)=>v-a[0][j]));
  return b[0][0]*(b[1][1]*b[2][2]-b[1][2]*b[2][1])
    -b[0][1]*(b[1][0]*b[2][2]-b[1][2]*b[2][0])
    +b[0][2]*(b[1][0]*b[2][1]-b[1][1]*b[2][0]);
}
function safe5(p){return p.every((_,i)=>det4(p.filter((_,j)=>i!==j))!==0);}
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
    const p=[49,60,a,b];
    if(det4(p)===0)continue;
    const key=canonical(p);
    if(!classes.has(key))classes.set(key,coverage(p));
  }
assert.equal(classes.size,3374);
const target=((1n<<121n)-1n)^(1n<<49n)^(1n<<60n);
function checkCover(keys){
  let union=0n;
  for(const k of keys){
    assert(classes.has(k),'invalid S4: '+k);
    assert(!win4.has(k),'known WIN4 selected: '+k);
    union|=classes.get(k);
  }
  assert.equal(union,target,'third-move coverage incomplete');
}
checkCover(old);checkCover(selected);
const memo=new Map();
function children(key){
  if(memo.has(key))return memo.get(key);
  const p=points(key);assert.equal(p.length,4);assert.notEqual(det4(p),0);
  const out=new Set();
  for(let x=0;x<121;x++)if(!p.includes(x)&&safe5([...p,x]))
    out.add(canonical([...p,x]));
  memo.set(key,out);return out;
}
function score(keys){
  const all=new Set();
  for(const k of keys)for(const c of children(k))all.add(c);
  let known=0,win=0;
  for(const k of all)if(cache.has(k)){known++;if(cache.get(k)===1)win++;}
  return {distinct:all.size,known_loss:known,unknown:all.size-known,known_win:win};
}
const before=score(old),after=score(selected);
assert.deepEqual(before,{distinct:2942,known_loss:315,unknown:2627,known_win:0});
assert.deepEqual(after,{distinct:2899,known_loss:315,unknown:2584,known_win:0});
assert.deepEqual(next.s5_dependency,{distinct:2899,known_loss:315,unknown:2584});
for(const k of next.known_loss4_classes){
  assert(selected.includes(k));
  assert([...children(k)].every(c=>cache.get(c)===2),'incomplete pinned LOSS4 '+k);
}
function scanOneSwap(keys){
  const fixed=new Set(next.known_loss4_classes),present=new Set(keys);
  const options=[];
  for(let i=0;i<keys.length;i++){
    if(fixed.has(keys[i]))continue;
    let union=0n;
    for(let j=0;j<keys.length;j++)if(i!==j)union|=classes.get(keys[j]);
    for(const [k,bits] of classes){
      if(present.has(k)||win4.has(k)||(union|bits)!==target)continue;
      const value=score(keys.map((x,j)=>i===j?k:x));
      assert.equal(value.known_win,0,'WIN5 under swap candidate');
      options.push({remove:keys[i],add:k,...value});
    }
  }
  options.sort((a,b)=>a.unknown-b.unknown||a.remove.localeCompare(b.remove)||a.add.localeCompare(b.add));
  return options;
}
const originalOptions=scanOneSwap(old);
assert.equal(originalOptions.length,34);
assert.equal(originalOptions.filter(x=>x.unknown<before.unknown).length,1);
assert.deepEqual({remove:originalOptions[0].remove,add:originalOptions[0].add,unknown:originalOptions[0].unknown},
  {remove:next.removed_s4_class,add:next.added_s4_class,unknown:2584});
const finalOptions=scanOneSwap(selected);
assert(finalOptions.every(x=>x.unknown>=2584),'another improving single swap exists');
assert.deepEqual(next.one_swap_search,{
  fixed_source_witnesses:31,known_loss4_held:3,eligible_single_swaps:34,
  strict_improvements:1,old_unknown_s5:2627,new_unknown_s5:2584,
  removed_unknown_s5:43,locally_best_single_swap:true,global_optimality_claim:false
});
console.log(JSON.stringify({schema:next.schema,root:[49,60],root_outcome:'UNKNOWN',
  geometric_classes:classes.size,known_WIN4_exclusions:win4.size,
  original_one_swaps:originalOptions.length,strict_improvements:1,
  new_one_swaps:finalOptions.length,new_improving_one_swaps:finalOptions.filter(x=>x.unknown<2584).length,
  before,after,removed_unknown_s5:43,known_loss4:3,unproved_s4:28,
  trust:'One-swap neighborhood only; S5 labels are pinned solver-trusted evidence. No S2 or empty-board verdict.'},null,2));
