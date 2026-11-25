// classify.mjs — canonical form of a stone configuration up to lattice isometry
// (D4 x integer translation): normalize each of the 8 images to min-corner (0,0),
// sort cells, take lexicographic minimum. Also relative-side invariant fingerprints.
const K0320 = {
  n11: [[5,0],[8,0],[1,4],[6,4],[8,4],[0,5],[3,5],[8,5],[4,9],[5,10]],
  n12: [[6,0],[9,0],[2,4],[7,4],[9,4],[1,5],[4,5],[9,5],[5,9],[6,10],[5,11]],
  n13: [[7,0],[3,2],[2,3],[9,3],[10,3],[2,4],[6,4],[11,4],[6,6],[1,10],[2,10],[7,12]],
  n14: [[3,1],[7,1],[10,1],[9,2],[4,3],[11,4],[7,8],[2,9],[7,9],[9,9],[2,11],[3,12],[0,13]],
  n15: [[7,0],[6,1],[1,3],[0,4],[3,7],[5,7],[10,7],[6,8],[12,9],[7,11],[11,11],[14,11],[6,12],[14,12]],
};
const W_b = [[6,0],[5,1],[6,2],[2,6],[7,6],[10,6],[2,7],[4,7],[9,7],[2,11],[5,11]];
const W_c = [[5,1],[4,2],[5,4],[9,5],[0,6],[10,6],[4,7],[0,9],[4,9],[5,9],[11,11]];

function canon(cells) {
  let best = null;
  for (const f of [
    (x,y)=>[x,y], (x,y)=>[-x,y], (x,y)=>[x,-y], (x,y)=>[-x,-y],
    (x,y)=>[y,x], (x,y)=>[-y,x], (x,y)=>[y,-x], (x,y)=>[-y,-x],
  ]) {
    const img = cells.map(([x,y]) => f(x,y));
    const mnx = Math.min(...img.map(c=>c[0])), mny = Math.min(...img.map(c=>c[1]));
    const norm = img.map(([x,y])=>[x-mnx,y-mny]).sort((a,b)=>a[1]-b[1]||a[0]-b[0]);
    const key = JSON.stringify(norm);
    if (best === null || key < best) best = key;
  }
  return best;
}
function span(cells) { // bounding box of the normalized best image
  const c = JSON.parse(canon(cells));
  return `${Math.max(...c.map(p=>p[0]))+1}x${Math.max(...c.map(p=>p[1]))+1}`;
}
const sets = { 'K0320-n11': K0320.n11, 'K0320-n12': K0320.n12, 'K0320-n13': K0320.n13, 'K0320-n14': K0320.n14, 'K0320-n15': K0320.n15, 'W_b': W_b, 'W_c': W_c };
const out = {};
for (const [k, v] of Object.entries(sets)) out[k] = { canonical: canon(v), span: span(v) };
// pairwise equality tests among the three 11-stone 12x12 witnesses
const trio = ['K0320-n12', 'W_b', 'W_c'];
const eq = {};
for (let i = 0; i < trio.length; i++) for (let j = i+1; j < trio.length; j++)
  eq[`${trio[i]}~${trio[j]}`] = out[trio[i]].canonical === out[trio[j]].canonical;
console.log(JSON.stringify({ sets: out, pairwise11stone: eq }, null, 1));
