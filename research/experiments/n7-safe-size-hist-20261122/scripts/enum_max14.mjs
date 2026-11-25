// enum_max14.mjs — enumerate ALL safe 14-subsets of the n=7 board (Z_7(14)=16,
// cross-verified by three histogram implementations), canonicalize under the
// D4 symmetry group of the square (8 elements), and report the orbit census.
// Uses the mask reachability test (same machinery as safehist_mask.mjs).
import * as fs from 'node:fs';
const n = 7, N = 49;
const qt = fs.readFileSync('/home/user/knowledge/kyouen-research/_n7-hist-kit/outputs/quartets_n7.txt', 'utf8').split('\n').filter(t => t && !t.startsWith('n='));
const cellTriples = Array.from({length: N}, () => ({los: [], his: []}));
for (const row of qt) {
  const [a,b,c,d] = row.split(' ').map(Number);
  for (const e of [a,b,c,d]) {
    let lo=0, hi=0;
    for (const o of [a,b,c,d]) if (o!==e) { if(o<32) lo|=1<<o; else hi|=1<<(o-32); }
    cellTriples[e].los.push(lo); cellTriples[e].his.push(hi);
  }
}
let curLo=0, curHi=0, out=[];
function placeable(c){const ts=cellTriples[c];for(let i=0;i<ts.los.length;i++){const l=ts.los[i],h=ts.his[i];if((curLo&l)===l&&(curHi&h)===h)return false;}return true;}
function dfs(start,depth){
  if (depth===14){ const cells=[]; for(let c=0;c<N;c++) if(c<32?(curLo>>c)&1:(curHi>>(c-32))&1) cells.push(c); out.push(cells); return; }
  for(let c=start;c<N;c++){
    if(!placeable(c))continue;
    if(c<32)curLo|=1<<c;else curHi|=1<<(c-32);
    dfs(c+1,depth+1);
    if(c<32)curLo&=~(1<<c);else curHi&=~(1<<(c-32));
  }
}
dfs(0,0);
const perms = [];
for (const [name,f] of [
  ['id', ([x,y]) => [x,y]],
  ['r90', ([x,y]) => [6-y, x]],
  ['r180', ([x,y]) => [6-x, 6-y]],
  ['r270', ([x,y]) => [y, 6-x]],
  ['fx', ([x,y]) => [6-x, y]],
  ['fy', ([x,y]) => [x, 6-y]],
  ['d1', ([x,y]) => [y, x]],
  ['d2', ([x,y]) => [6-y, 6-x]],
]) perms.push({name, f});
const canon = s => {
  const pts = s.map(c => [c%7, Math.floor(c/7)]);
  let best = null, stab = [];
  for (const p of perms) {
    const t = pts.map(pt => { const [x,y]=p.f(pt); return x + 7*y; }).sort((a,b)=>a-b);
    const key = t.join(',');
    if (best === null || key < best) best = key;
  }
  for (const p of perms) {
    const t = pts.map(pt => { const [x,y]=p.f(pt); return x + 7*y; }).sort((a,b)=>a-b);
    if (t.join(',') === best) stab.push(p.name);
  }
  return { canonical: best, stabilizer: stab };
};
const orbits = new Map();
for (const s of out) {
  const { canonical, stabilizer } = canon(s);
  if (!orbits.has(canonical)) orbits.set(canonical, { stabilizer, members: 0 });
  orbits.get(canonical).members++;
}
let orbitSum = 0;
const orbList = [];
for (const [k, v] of orbits) { orbitSum += v.members; orbList.push({ canonical: k.split(',').map(Number), orbit_size: v.members, stabilizer_size: v.stabilizer.length, stabilizer: v.stabilizer }); }
orbList.sort((a,b)=>{
  for (let i=0;i<14;i++){ if(a.canonical[i]!==b.canonical[i]) return a.canonical[i]-b.canonical[i]; }
  return 0;
});
console.log(JSON.stringify({ total_safe_sets: out.length, orbits: orbList.length, orbit_sum: orbitSum, orbit_sizes: orbList.map(o=>o.orbit_size), stab_sizes: orbList.map(o=>o.stabilizer_size) }));
const fd = fs.openSync('/home/user/knowledge/kyouen-research/_n7-hist-kit/outputs/max14_orbits.json','w');
fs.writeSync(fd, JSON.stringify({ n, lambda: 14, total_safe_sets: out.length, orbits: orbList.length, orbit_sum: orbitSum, census: orbList }, null, 1) + '\n');
fs.closeSync(fd);
