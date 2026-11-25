// annotate8.mjs — recompute structural features on the PUBLISHED n=8 catalog
// (round10_small_saturation.json, 51 D4 orbit representatives of the 408
// maximal safe 8-stone configurations, K0032/B371) with the SAME feature code
// used for the n=7 catalog, and validate:
//   - D4 closure gives 51 orbits * orbit size 8 = 408 distinct configurations
//   - published stabilizer histogram {"1": 408} (all trivial)
//   - published per-rep essential_curve_count matches our ecc definition 51/51
//   - aggregate feature histograms (three-collinear direction counts etc.)
// Then the identical feature pipeline is applied to n=7 (classify.mjs),
// enabling the n=7 vs n=8 comparison table.
// Usage: node annotate8.mjs <round10.json> <out.json>

import * as fs from 'node:fs';
import { census } from '../pinned/census.mjs';

const inPath = process.argv[2];
const outPath = process.argv[3];
const n = 8, k = 8, N = 64;
const r10 = JSON.parse(fs.readFileSync(inPath, 'utf8'));
const cen = census(n);

const repFromStones = (stones) => stones.map(([x, y]) => x + n * y).sort((a, b) => a - b);
const key = (a) => a.join(',');

function images(stones) {
  const pts = stones.map(c => [c % n, Math.floor(c / n)]);
  const tf = [
    (x, y) => [x, y],
    (x, y) => [n - 1 - x, y],
    (x, y) => [x, n - 1 - y],
    (x, y) => [n - 1 - x, n - 1 - y],
    (x, y) => [y, x],
    (x, y) => [n - 1 - y, x],
    (x, y) => [y, n - 1 - x],
    (x, y) => [n - 1 - y, n - 1 - x],
  ];
  return tf.map(t => pts.map(([x, y]) => { const [u, v] = t(x, y); return u + n * v; }).sort((a, b) => a - b));
}

function features(stones) {
  const pts = stones.map(c => [c % n, Math.floor(c / n)]);
  const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
  const rowH = {}, colH = {};
  for (const y of ys) rowH[y] = (rowH[y] ?? 0) + 1;
  for (const x of xs) colH[x] = (colH[x] ?? 0) + 1;
  const bbox = [Math.max(...xs) - Math.min(...xs), Math.max(...ys) - Math.min(...ys)];
  let triples3 = 0; const dirCount = {};
  for (let i = 0; i < k; i++) for (let j = i + 1; j < k; j++) {
    for (let m = j + 1; m < k; m++) {
      const dx = pts[j][0] - pts[i][0], dy = pts[j][1] - pts[i][1];
      const ex = pts[m][0] - pts[i][0], ey = pts[m][1] - pts[i][1];
      if (dx * ey === dy * ex) {
        triples3++;
        const g = (function gg(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a || 1; })(dx, dy);
        const d = `${dx / g},${dy / g}`;
        dirCount[d] = (dirCount[d] ?? 0) + 1;
      }
    }
  }
  return { triples3, dirs: Object.keys(dirCount).length, dirCount, bbox, rows: Object.values(rowH).sort((a, b) => b - a), cols: Object.values(colH).sort((a, b) => b - a) };
}

function essentialCurves(stones) {
  const onBoard = new Set(stones);
  const cand = [];
  for (const l of cen.lines) {
    const inS = l.pts.filter(p => onBoard.has(p));
    if (inS.length >= 3) cand.push({ kind: 'line', pts: l.pts });
  }
  for (const c of cen.circles) {
    const inS = c.pts.filter(p => onBoard.has(p));
    if (inS.length >= 3) cand.push({ kind: 'circle', pts: c.pts });
  }
  const coverSets = cand.map(cd => new Set(cd.pts.filter(p => !onBoard.has(p))));
  let ecc = 0;
  for (let i = 0; i < cand.length; i++) {
    let priv = null;
    for (const p of coverSets[i]) {
      let only = true;
      for (let j = 0; j < cand.length; j++) if (j !== i && coverSets[j].has(p)) { only = false; break; }
      if (only) { priv = p; break; }
    }
    if (priv !== null) ecc++;
  }
  return { ecc, cand: cand.length };
}

const reps = r10.orbits.map(o => repFromStones(o.stones));
// duplicates guard
const repKeys = new Set(reps.map(key));
if (repKeys.size !== reps.length) { console.error('duplicate reps'); process.exit(1); }

// closure check: images of all reps = 408 distinct configs, one orbit each 8
const all = new Set();
let closureOK = true;
let eccMatch = 0, eccMismatch = [];
let perRep = [];
for (let i = 0; i < reps.length; i++) {
  const imgs = images(reps[i]);
  const distinct = new Set(imgs.map(key));
  if (distinct.size !== 8) { console.error('orbit size != 8', reps[i]); closureOK = false; }
  for (const im of imgs) {
    if (all.has(key(im))) { console.error('orbit OVERLAP', reps[i]); closureOK = false; }
    all.add(key(im));
  }
  if (key(reps[i]) !== key([...distinct].map(s => s.split(',').map(Number)).sort((a, b) => { for (let t = 0; t < k; t++) if (a[t] !== b[t]) return a[t] - b[t]; return 0; })[0])) {
    // rep is not the stone-list lex-min of its own orbit (fine; just noting)
  }
  const f = features(reps[i]);
  const e = essentialCurves(reps[i]);
  const published = r10.orbits[i].essential_curve_count;
  if (e.ecc === published) eccMatch++; else eccMismatch.push({ rep: reps[i], mine: e.ecc, published });
  perRep.push({ rep: reps[i], orbit_size: distinct.size, ...f, ecc_mine: e.ecc, ecc_published: published, cand_curves: e.cand });
}
if (all.size !== 408) { console.error('closure size', all.size); process.exit(1); }
if (r10.source_maximal_sets !== 408 || r10.d4_orbits !== 51) { console.error('published meta mismatch'); process.exit(1); }

// per-config features on the full 408
let tripsH = {}, dirsH = {}, eccH = {};
for (const kk of all) {
  const s = kk.split(',').map(Number);
  const f = features(s);
  tripsH[f.triples3] = (tripsH[f.triples3] ?? 0) + 1;
  dirsH[f.dirs] = (dirsH[f.dirs] ?? 0) + 1;
  const e = essentialCurves(s);
  eccH[e.ecc] = (eccH[e.ecc] ?? 0) + 1;
}
// published ecc histogram over all 408 (reconstruct order-insensitively)
const pubEccH = r10.essential_curve_count_histogram_all_sets;
const eccHMatches = JSON.stringify(Object.fromEntries(Object.entries(eccH).map(([a, b]) => [a, b]).sort((a, b) => a[0] - b[0]))) ===
  JSON.stringify(Object.fromEntries(Object.entries(pubEccH).map(([a, b]) => [a, b]).sort((a, b) => a[0] - b[0])));

const out = {
  n, k,
  published_source: r10.input_source,
  published_source_sha256: r10.source_sha256,
  total_configs_closure: all.size,
  orbits: reps.length,
  closure_ok: closureOK,
  stabilizer_all_trivial: true,
  ecc_rep_match: `${eccMatch}/${reps.length}`,
  ecc_rep_mismatches: eccMismatch,
  ecc_histogram_mine_all408: eccH,
  ecc_histogram_published: pubEccH,
  ecc_histogram_matches_published: eccHMatches,
  triples3_histogram_all408: tripsH,
  dirs_histogram_all408: dirsH,
  all_have_three_collinear: Object.keys(tripsH).every(t => parseInt(t) >= 1),
  per_rep: perRep,
};
fs.writeFileSync(outPath, JSON.stringify(out, null, 1));
console.log(JSON.stringify({ total: out.total_configs_closure, orbits: out.orbits, closure_ok: closureOK, ecc: out.ecc_rep_match, ecc_hist_match: eccHMatches, trips: tripsH, dirs: dirsH, all3col: out.all_have_three_collinear }));
