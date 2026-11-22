// classify.mjs — D4 orbit classification, integrity checks and structural
// features for a complete catalog of maximal safe configurations (enum JSONL).
//
// Checks performed (fail-closed, exit code 1 on any failure):
//  C1 shard-union integrity: parsed configs have strictly increasing stones,
//     k elements, and unique min-stone sharding (no duplicates).
//  C2 D4-closure: the full set of found configs is closed under the 8 board
//     symmetries (necessary since DFS enumerates ALL configurations).
//  C3 orbit classification: canonical form = lex-smallest of the 8 D4 images;
//     orbit size = number of distinct images; stabilizer order = 8/orbit size.
//  C4 features per configuration and per orbit (three-collinear directions,
//     row/column profiles, bbox span, corner/edge contact, stone-degree).
//
// Usage: node classify.mjs <in.jsonl>,...
//   (multiple inputs are concatenated; expected shard partition is not
//    re-verified against ranges, only uniqueness)
// Output: JSON to stdout (summary + orbits); per-config features embedded.

import * as fs from 'node:fs';

const files = process.argv.slice(2);
const n = parseInt(process.env.N ?? '7', 10);
const N = n * n;
const k = parseInt(process.env.K ?? '7', 10);

function key(a) { return a.join(','); }
function parseLine(l) { return JSON.parse(l); }

const cfgs = [];
for (const f of files) {
  const lines = fs.readFileSync(f, 'utf8').split('\n').filter(x => x.trim());
  for (const l of lines) {
    const r = parseLine(l);
    if (r.type === 'cfg') cfgs.push(r.stones);
  }
}
// sort configs lexicographically
cfgs.sort((a, b) => {
  for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return a[i] - b[i];
  return 0;
});

// C1
const seen = new Set();
for (const s of cfgs) {
  if (s.length !== k) { console.error('C1 FAIL length', s); process.exit(1); }
  for (let i = 1; i < k; i++) if (s[i] <= s[i - 1]) { console.error('C1 FAIL order', s); process.exit(1); }
  for (const c of s) if (!(c >= 0 && c < N)) { console.error('C1 FAIL range', s); process.exit(1); }
  const kk = key(s);
  if (seen.has(kk)) { console.error('C1 FAIL duplicate', s); process.exit(1); }
  seen.add(kk);
}

// D4 images on n x n board, cell c = x + n*y
function images(stones) {
  const out = [];
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
  for (const t of tf) {
    const img = pts.map(([x, y]) => { const [u, v] = t(x, y); return u + n * v; });
    img.sort((a, b) => a - b);
    out.push(img);
  }
  return out;
}

// C2 closure
const fullSet = new Set(cfgs.map(key));
let closureOK = true;
for (const s of cfgs) {
  for (const img of images(s)) if (!fullSet.has(key(img))) { closureOK = false; console.error('C2 FAIL not closed:', s, '->', img); }
}
if (!closureOK) process.exit(1);

// forbidden-catalog features (via census for curve counting)
const { census } = await import('../pinned/census.mjs');
const cen = census(n);

// rows/cols/corner/edge/bbox features + three-collinear direction census
function features(stones) {
  const xs = stones.map(c => c % n), ys = stones.map(c => Math.floor(c / n));
  const rowH = {}, colH = {};
  for (const y of ys) rowH[y] = (rowH[y] ?? 0) + 1;
  for (const x of xs) colH[x] = (colH[x] ?? 0) + 1;
  const rows = Object.values(rowH), cols = Object.values(colH);
  const bbox = [Math.max(...xs) - Math.min(...xs), Math.max(...ys) - Math.min(...ys)];
  const corners = stones.filter(c => (c % n === 0 || c % n === n - 1) && (Math.floor(c / n) === 0 || Math.floor(c / n) === n - 1)).length;
  const edges = stones.filter(c => c % n === 0 || c % n === n - 1 || Math.floor(c / n) === 0 || Math.floor(c / n) === n - 1).length;
  // three-collinear triples over stone triples using line grouping
  const dirCount = {}; // per primitive direction, number of 3-collinear stone triples
  let triples3 = 0;
  const pts = stones.map(c => [c % n, Math.floor(c / n)]);
  for (let i = 0; i < k; i++) for (let j = i + 1; j < k; j++) {
    const dx = pts[j][0] - pts[i][0], dy = pts[j][1] - pts[i][1];
    for (let m = j + 1; m < k; m++) {
      const ex = pts[m][0] - pts[i][0], ey = pts[m][1] - pts[i][1];
      if (dx * ey === dy * ex) {
        triples3++;
        const g = (function gg(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a || 1; })(dx, dy);
        const d = `${dx / g},${dy / g}`;
        dirCount[d] = (dirCount[d] ?? 0) + 1;
      }
    }
  }
  return {
    rows: rows.sort((a, b) => b - a), cols: cols.sort((a, b) => b - a),
    rowH, bbox, corners, edges,
    triples3, dirCount,
    dirs: Object.keys(dirCount).length,
  };
}

// essential-curve feature (same semantics as round10_small_saturation via
// stone-triple curves with PRIVATE empty points; validated against the n=8
// published representatives separately in annotate8.mjs)
function essentialCurves(stones) {
  // candidate curves: every line with >=3 stones and every circle through
  // >=3 stones (census lines/circles restricted to the stone set)
  const onBoard = new Set(stones);
  const cand = [];
  for (const l of cen.lines) {
    const inS = l.pts.filter(p => onBoard.has(p));
    if (inS.length >= 3) cand.push({ kind: 'line', pts: l.pts, inS });
  }
  for (const c of cen.circles) {
    const inS = c.pts.filter(p => onBoard.has(p));
    if (inS.length >= 3) cand.push({ kind: 'circle', pts: c.pts, inS });
  }
  // covered-by sets: empty points of the board covered by each candidate
  const board = new Set(); for (let c2 = 0; c2 < N; c2++) board.add(c2);
  const coverSets = cand.map(cd => new Set(cd.pts.filter(p => board.has(p) && !onBoard.has(p))));
  // duplicate curves can occur only as line-vs-circle (impossible) so cand unique
  let ecc = 0;
  const certs = [];
  for (let i = 0; i < cand.length; i++) {
    // private point: covered by cand[i] and by no other candidate
    let priv = null;
    for (const p of coverSets[i]) {
      let only = true;
      for (let j = 0; j < cand.length; j++) if (j !== i && coverSets[j].has(p)) { only = false; break; }
      if (only) { priv = p; break; }
    }
    if (priv !== null) { ecc++; certs.push({ curve: cand[i].kind, triple_min_hint: cand[i].inS, private_empty_point: priv }); }
  }
  return { ecc, cand: cand.length, certs };
}

// C3 orbits
const lexcmp = (a, b) => { for (let i = 0; i < a.length; i++) { if (a[i] !== b[i]) return a[i] - b[i]; } return 0; };
const orbitMap = new Map(); // canonKey -> {rep, members(Set of cfgKeys), images}
for (const s of cfgs) {
  const imgsArr = images(s);
  const imgs = imgsArr.map(key);
  const canonArr = imgsArr.slice().sort(lexcmp)[0];
  const canon = key(canonArr);
  let o = orbitMap.get(canon);
  if (!o) { o = { rep: canonArr, lexmin: canonArr, members: new Set(), sizeDistinct: new Set() }; orbitMap.set(canon, o); }
  o.members.add(key(s));
  for (const ik of imgs) o.sizeDistinct.add(ik);
}
const orbits = [...orbitMap.values()].map(o => ({
  rep: o.rep,
  lexmin: o.rep, // canon is the index-lexicographic minimum of the orbit (== lex-leader rep)
  members: [...o.members].map(m => m.split(',').map(Number)),
  orbit_size: o.sizeDistinct.size,
  stabilizer_order: 8 / o.sizeDistinct.size,
}));

// consistency: sum of orbit sizes must equal total configs AND every orbit
// member must have been found by the enumeration (completeness within-orbit)
let tot = 0;
for (const o of orbits) tot += o.orbit_size;
if (tot !== cfgs.length) { console.error('C3 FAIL orbit-sum', tot, cfgs.length); process.exit(1); }
for (const o of orbits) {
  if (o.members.length !== o.orbit_size) { console.error('C3 FAIL orbit incomplete', o.rep, o.members.length, o.orbit_size); process.exit(1); }
}

// per-config features
const featuresByCfg = {};
for (const s of cfgs) featuresByCfg[key(s)] = features(s);
const eccByCfg = {};
for (const s of cfgs) eccByCfg[key(s)] = essentialCurves(s);

const out = {
  n, k, N,
  total: cfgs.length,
  orbits: orbits.length,
  stabilizer_histogram: (() => { const h = {}; for (const o of orbits) h[o.stabilizer_order] = (h[o.stabilizer_order] ?? 0) + 1; return h; })(),
  configs: cfgs,
  orbit_details: orbits.map(o => ({
    rep: o.rep,
    members: o.members,
    orbit_size: o.orbit_size,
    stabilizer_order: o.stabilizer_order,
    features: featuresByCfg[key(o.rep)],
    ecc: eccByCfg[key(o.rep)].ecc,
    ecc_candidate_curves: eccByCfg[key(o.rep)].cand,
    // one-stone-removal legality count is computed in Python verifier
  })),
  ecc_histogram_all_sets: (() => { const h = {}; for (const s of cfgs) { const e = eccByCfg[key(s)].ecc; h[e] = (h[e] ?? 0) + 1; } return h; })(),
  triples3_histogram_all_sets: (() => { const h = {}; for (const s of cfgs) { const t = featuresByCfg[key(s)].triples3; h[t] = (h[t] ?? 0) + 1; } return h; })(),
  dirs_histogram_all_sets: (() => { const h = {}; for (const s of cfgs) { const d = featuresByCfg[key(s)].dirs; h[d] = (h[d] ?? 0) + 1; } return h; })(),
  all_have_three_collinear: cfgs.every(s => featuresByCfg[key(s)].triples3 >= 1),
  checks: { C1_unique_sorted: true, C2_d4_closure: true, C3_orbit_sum: tot },
};
fs.writeFileSync(process.env.OUT ?? 'output/classify_n7.json', JSON.stringify(out, null, 1));
console.log(JSON.stringify({
  total: out.total, orbits: out.orbits, stab: out.stabilizer_histogram,
  ecc_hist: out.ecc_histogram_all_sets, checks: out.checks,
}));
