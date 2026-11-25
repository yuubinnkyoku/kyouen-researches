'use strict';
// Exact 2-for-2 repair of the refuted {49,60} 31-class geometric cover.
// No S4 LOSS or S2/empty-board verdict is inferred.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../../..');
const {witnesses:cachedWIN4,canonical,points,maps}=require('./audit_win4_exclusion');
require('./audit_central49_terminal_win5_conflicts');
require('./verify_31_loss4_reuse_49');
function pinned(file,sha){
 const raw=fs.readFileSync(path.join(ROOT,file));
 const blob=Buffer.concat([Buffer.from('blob '+raw.length),Buffer.from([0]),raw]);
 assert.equal(crypto.createHash('sha1').update(blob).digest('hex'),sha,'changed source: '+file);
 return raw.toString('utf8');
}
const receipts=[
 [144095,[5,45,49,53,60],'research/experiments/n11-adaptive-verify-20261013/output/pilot-144095-receipt.json','e89aa0a088ca694faabfb390b22c1f14f8d6b4ae'],
 [126017,[1,49,59,60,61],'research/experiments/n11-night-batch1-20261014/output/nightb10m-126017-receipt.json','a16a89e94f6e18d18191284d3489b9c2b78662a5'],
 [197665,[37,49,59,60,61],'research/experiments/n11-night-batch2-20261014/output/nighta25m-197665-receipt.json','79329811653738a0e213aebef75f0176d0c9472b'],
 [206386,[49,51,59,60,71],'research/experiments/n11-night-batch3-20261014/output/nighta25m-206386-receipt.json','93d7d1f09fb9807f2f77c74795f75572703d39db'],
 [131631,[2,49,59,60,61],'research/experiments/n11-night-batch4-20261014/output/nighta25m-131631-receipt.json','ca0d1d5e6698481e1de7c2543e47a2a09fba77c0'],
 [162106,[14,49,59,60,61],'research/experiments/n11-night-batch5-20261014/output/nighta25m-162106-receipt.json','9e687e5ec961254d6ea8dc2f33e1c62291bfe19b']
];
function verifyReceipt(r,index,p){
 assert.equal(r.board_size,11);assert.equal(r.s5_index,index);
 assert.equal(r.verdict,1);assert.equal(r.trusted_leaves,0);
 assert.equal(r.evidence_class,'independent-terminal-only-verification');
 assert.equal(BigInt(r.root_mask),p.reduce((b,x)=>b|(1n<<BigInt(x)),0n));
 assert.match(r.certificate_sha256,/^[a-f0-9]{64}$/);
 assert.equal(r.checker_source_sha256,'0f890cb49e806880bb56de2147163dc3fcfb0d5eae44835d602160c16008cd96');
}
const terminalWIN4=new Set();
for(const [index,p,file,sha] of receipts){
 const r=JSON.parse(pinned(file,sha));verifyReceipt(r,index,p);
 for(const x of p)terminalWIN4.add(canonical(p.filter(y=>y!==x)));
}
const receipt0=JSON.parse(pinned(receipts[0][2],receipts[0][3]));
assert.throws(()=>verifyReceipt({...receipt0,verdict:2},144095,receipts[0][1]));
assert.throws(()=>verifyReceipt({...receipt0,trusted_leaves:1},144095,receipts[0][1]));
assert.equal(terminalWIN4.size,24);
// Independent 4x4 determinant (the cache audit uses a 3x3 difference determinant).
const perms=[];
function permute(a,sign){
 if(a.length===4){perms.push([a,sign]);return;}
 for(let j=0;j<4;j++)if(!a.includes(j))
  permute([...a,j],sign*((a.filter(k=>k>j).length%2)?-1:1));
}
permute([],1);assert.equal(perms.length,24);
function det4(p){
 const a=p.map(i=>{const x=i%11,y=Math.floor(i/11);return[x*x+y*y,x,y,1];});
 return perms.reduce((sum,[q,sign])=>sum+sign*a[0][q[0]]*a[1][q[1]]*a[2][q[2]]*a[3][q[3]],0);
}
function safe5(p){for(let i=0;i<5;i++)if(det4(p.filter((_,j)=>i!==j))===0)return false;return true;}
function coverage(p){
 const out=new Set();
 for(const m of maps){const q=p.map(x=>m[x]);if(q.includes(49)&&q.includes(60))
  for(const x of q)if(x!==49&&x!==60)out.add(x);}
 return out;
}
const classes=new Map();
for(let a=0;a<121;a++)if(a!==49&&a!==60)
 for(let b=a+1;b<121;b++)if(b!==49&&b!==60){
  const p=[49,60,a,b];if(det4(p)===0)continue;
  const k=canonical(p);if(!classes.has(k))classes.set(k,coverage(p));
 }
assert.equal(classes.size,3374);
const historical=JSON.parse(fs.readFileSync(path.join(__dirname,'win4-safe-31-loss4-reuse-49.json'),'utf8'));
const repaired=JSON.parse(fs.readFileSync(path.join(__dirname,'central49-terminal-win5-safe-repair.json'),'utf8'));
assert.equal(repaired.schema,'n11-central49-terminal-win5-safe-31-repair-v1');
assert.deepEqual(repaired.root_stones,[49,60]);
assert.equal(repaired.root_outcome,'UNKNOWN');assert.equal(repaired.empty_board_outcome,'UNKNOWN');
const removed=['00000000000000003800000000000002','00000000000000003800000000004000'];
assert.deepEqual(repaired.removed_s4_classes,removed);
assert(removed.every(k=>historical.selected_s4_classes.includes(k)&&terminalWIN4.has(k)));
const fixed=historical.selected_s4_classes.filter(k=>!removed.includes(k));
assert.equal(fixed.length,29);
assert(fixed.every(k=>!cachedWIN4.has(k)&&!terminalWIN4.has(k)));
assert.deepEqual(historical.known_loss4_classes,repaired.known_loss4_classes);
assert(repaired.known_loss4_classes.every(k=>fixed.includes(k)));
const covered=new Set(fixed.flatMap(k=>[...classes.get(k)]));
const missing=Array.from({length:121},(_,i)=>i).filter(x=>x!==49&&x!==60&&!covered.has(x));
assert.deepEqual(missing,[11,21,34,42,78,86,99,109]);
const candidates=[...classes].filter(([k,c])=>!fixed.includes(k)&&!removed.includes(k)&&[...c].some(x=>missing.includes(x)));
assert.equal(candidates.length,450);
const pairs=[];
for(let i=0;i<candidates.length;i++)for(let j=i+1;j<candidates.length;j++){
 const union=new Set([...candidates[i][1],...candidates[j][1]]);
 if(missing.every(x=>union.has(x)))pairs.push([candidates[i][0],candidates[j][0]]);
}
assert.equal(pairs.length,12);
const cacheText=pinned('research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache',
 '2dccf42b92337cbcbfb62ea5c77db487b1ad8ead');
const cache=new Map();
for(const line of cacheText.split(String.fromCharCode(10))){
 if(!line||line.startsWith('#'))continue;
 const f=line.trim().split(',');assert.equal(f[0],'s5verdict');assert.equal(f[3],'5');
 const k=(BigInt(f[1])+(BigInt(f[2])<<64n)).toString(16).padStart(32,'0');
 assert(!cache.has(k));cache.set(k,Number(f[4]));
}
assert.equal(cache.size,5851);assert.equal([...cache.values()].filter(x=>x===1).length,159);
const childMemo=new Map();
function children(k){
 if(childMemo.has(k))return childMemo.get(k);
 const p=points(k);assert.equal(p.length,4);assert.notEqual(det4(p),0);
 const out=new Set();
 for(let x=0;x<121;x++)if(!p.includes(x)&&safe5([...p,x]))out.add(canonical([...p,x]));
 childMemo.set(k,out);return out;
}
const fixedS5=new Set(fixed.flatMap(k=>[...children(k)]));
assert.equal(fixedS5.size,2721);
assert.equal([...fixedS5].filter(k=>!cache.has(k)).length,2406);
function score(pair){
 const all=new Set(fixedS5);
 for(const k of pair){
  assert(!cachedWIN4.has(k),'solver-trusted WIN4 selected');
  assert(!terminalWIN4.has(k),'terminal WIN4 selected');
  for(const child of children(k))all.add(child);
 }
 const known=[...all].filter(k=>cache.has(k));
 assert(known.every(k=>cache.get(k)===2),'known WIN5 under candidate');
 return {pair,distinct_s5:all.size,known_loss5:known.length,unknown_s5:all.size-known.length};
}
const options=pairs.map(score).sort((a,b)=>a.unknown_s5-b.unknown_s5||
 a.pair.join(',').localeCompare(b.pair.join(',')));
assert.equal(options.length,12);
assert(options.every(x=>x.unknown_s5>=2627&&x.unknown_s5<=2634));
assert.deepEqual(options,repaired.pair_options);
assert.deepEqual(repaired.added_s4_classes,options[0].pair);
assert.deepEqual(repaired.s5_dependency,{distinct:2942,known_loss:315,unknown:2627});
assert.deepEqual(repaired.s5_dependency,{distinct:options[0].distinct_s5,
 known_loss:options[0].known_loss5,unknown:options[0].unknown_s5});
const selected=[...fixed,...options[0].pair].sort();
assert.deepEqual(selected,repaired.selected_s4_classes);
assert.equal(selected.length,31);assert.equal(new Set(selected).size,31);
assert(selected.every(k=>classes.has(k)&&!cachedWIN4.has(k)&&!terminalWIN4.has(k)));
const third=new Set(selected.flatMap(k=>[...classes.get(k)]));
assert.equal(third.size,119);assert(!third.has(49)&&!third.has(60));
assert.equal(selected.filter(k=>historical.known_loss4_classes.includes(k)).length,3);
assert.equal(new Set([...fixed,options[0].pair[0]].flatMap(k=>[...classes.get(k)])).size<119,true);
assert.equal(new Set([...fixed,options[0].pair[1]].flatMap(k=>[...classes.get(k)])).size<119,true);
console.log(JSON.stringify({schema:repaired.schema,root:[49,60],root_outcome:'UNKNOWN',
 terminal_win5_receipts:6,legal_s4_classes:3374,missing_third_moves:missing,
 two_for_two_repairs:options.length,best_repair:options[0],reused_loss4:3,
 unknown_s4:28,refuted_historical_unknown_s5:2525,repaired_unknown_s5:2627,
 minimum_geometric_classes:31,empty_board:'UNKNOWN',
 trust:'Constrained geometric proof only; terminal receipts pinned but large terminal DAGs not replayed.'},null,2));
