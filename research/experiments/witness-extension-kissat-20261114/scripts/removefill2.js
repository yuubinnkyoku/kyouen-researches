// remove-fill: for a base witness on w x M0, extend to w x M (M>M0) allowing
// removal of up to rMax stones from the base and filling subset of new cells,
// subject to total <= w*(q-1)-1. Prefilter: cells not blocked by kept stones
// must be in the add-subset.
const S = require('./sat.js');
const fs = require('fs');
const [w, M, q, M0, rMax] = process.argv.slice(2, 7).map(Number);
const witFile = process.argv[7];
let st = JSON.parse(fs.readFileSync(witFile, 'utf8'));
if (Array.isArray(st)) st = st.find(e => e.w === w && e.q === q && (e.toM === M0 || e.m === M0));
const base = (st.stones || st).map(([x, y]) => [x, y]);
const capDef = w * (q - 1) - 1;
function combos(arr, k) {
  const res = [];
  const rec = (i, cur) => { if (cur.length === k) { res.push(cur.slice()); return; } if (i >= arr.length) return; cur.push(arr[i]); rec(i + 1, cur); cur.pop(); rec(i + 1, cur); };
  rec(0, []); return res;
}
function subsets(arr, cap) {
  const res = []; const n = arr.length;
  const rec = (i, cur, sz) => { if (i === n) { res.push(cur.slice()); return; } rec(i + 1, cur, sz); if (sz < cap) { cur.push(arr[i]); rec(i + 1, cur, sz + 1); cur.pop(); } };
  rec(0, [], 0); return res;
}
// blocking: is cell c on a curve with >= q-1 stones among kept?
function blockedBy(c, kept, q) {
  for (let i = 0; i < kept.length; i++) {
    const lo = S.lineABC(c, kept[i]);
    let cnt = 0; for (const p of kept) if (S.onLine(lo, p[0], p[1])) cnt++;
    if (cnt >= q - 1) return true;
    for (let j = i + 1; j < kept.length; j++) {
      const co = S.circleABC(c, kept[i], kept[j]);
      if (!co) continue;
      let cc = 0; for (const p of kept) if (S.onCircle(co, p[0], p[1])) cc++;
      if (cc >= q - 1) return true;
    }
  }
  return false;
}
let tries = 0, hits = 0;
const dm = M - M0;
for (let off = 0; off <= dm; off++) {
  const newCells = [];
  for (let x = 0; x < M; x++) for (let y = 0; y < w; y++) if (!(x >= off && x < off + M0)) newCells.push([x, y]);
  for (let r = 0; r <= rMax; r++) {
    for (const rem of combos(base.map((_, i) => i), r)) {
      const rm = new Set(rem);
      const kept = base.filter((_, i) => !rm.has(i)).map(([x, y]) => [x + off, y]);
      const spare = capDef - kept.length;
      if (spare < 0) continue;
      const required = [], optional = [];
      for (const c of newCells) { if (blockedBy(c, kept, q)) optional.push(c); else required.push(c); }
      if (required.length > spare) continue;
      for (const extras of subsets(optional, spare - required.length)) {
        const cand = kept.concat(required, extras);
        tries++;
        const v = S.verifyConfig(w, M, q, cand);
        if (v.ok) { hits++; console.log('HIT', JSON.stringify({ w, M, q, off, r, size: cand.length, rows: v.rows, stones: cand })); }
      }
    }
  }
}
console.log(JSON.stringify({ w, M, q, M0, rMax, tries, hits }));
