// max14_structure.mjs — structural analysis of the 16 maximal safe 14-sets
// (Z_7(14)=16, published as two free D4 orbits; representatives from
//  output/max14_orbits.json). For each of the 16 sets this script verifies
//  safety (no forbidden quartet contained) and maximality (every excluded
//  cell completes some quartet whose other 3 cells are in the set) by
//  DIRECT checks, then computes:
//   - row / column counts,
//   - diagonal counts (r-c bands and r+c bands),
//   - the full incidence of the set against the catalog of maximal
//     concyclic cell groups (circles, size>=4) and maximal collinear
//     groups (lines, size>=4) of the 7x7 grid,
//   - the |Q intersect S| histogram over all 6364 forbidden quartets.
// It does NOT re-prove that these 16 are all of them (that is the published
//  enumeration); it verifies and analyzes exactly the 16 obtained from the
//  published representatives by D4.
import * as fs from 'node:fs';

const n = 7, N = 49;
const repPath = process.argv[2]; // output/max14_orbits.json
const qPath = process.argv[3];   // output/quartets_n7.txt
const outPath = process.argv[4]; // output/max14_structure.json
const catalogPath = process.argv[5] || ''; // optional: output/group_catalog_n7.json

const orbits = JSON.parse(fs.readFileSync(repPath, 'utf8'));
const qt = fs.readFileSync(qPath, 'utf8').split('\n').filter(t => t && !t.startsWith('=') && !t.startsWith('n='));
const quads = qt.map(r => r.split(' ').map(Number));
if (quads.length !== 6364) throw new Error('expected 6364 quartets, got ' + quads.length);

// ---- D4 ----
const D4 = [
  ['id',   ([x,y]) => [x,y]],
  ['r90',  ([x,y]) => [6-y, x]],
  ['r180', ([x,y]) => [6-x, 6-y]],
  ['r270', ([x,y]) => [y, 6-x]],
  ['fx',   ([x,y]) => [6-x, y]],
  ['fy',   ([x,y]) => [x, 6-y]],
  ['d1',   ([x,y]) => [y, x]],
  ['d2',   ([x,y]) => [6-y, 6-x]],
];
const xy = c => [Math.floor(c / 7), c % 7];
const cellOf = ([x,y]) => x * 7 + y;

// ---- build 16 sets from representatives ----
const reps = orbits.census.map(o => o.canonical);
if (reps.length !== 2) throw new Error('expected 2 representatives');
const sets = [];
for (const rep of reps) {
  if (rep.length !== 14) throw new Error('representative size != 14');
  for (const [name, f] of D4) {
    sets.push({ rep: reps.indexOf(rep) + 1, d4: name, cells: rep.map(c => cellOf(f(xy(c)))).sort((a,b)=>a-b) });
  }
}
const keys = new Set(sets.map(s => s.cells.join(',')));
if (keys.size !== 16) throw new Error('D4 images not distinct: ' + keys.size);
if (sets.some(s => s.cells.length !== 14)) throw new Error('size broken');

// ---- safety & maximality by direct checks ----
const tripleOf = Array.from({length: N}, () => []); // cell -> list of masks (other 3 cells)
for (const [a,b,c,d] of quads) {
  tripleOf[a].push([b,c,d]); tripleOf[b].push([a,c,d]);
  tripleOf[c].push([a,b,d]); tripleOf[d].push([a,b,c]);
}
for (const s of sets) {
  const inS = new Set(s.cells);
  // safety
  for (const q of quads) if (q.every(c => inS.has(c))) throw new Error('UNSAFE set ' + s.cells.join(','));
  // maximality: every excluded cell d has a triple fully in S
  for (let d = 0; d < N; d++) {
    if (inS.has(d)) continue;
    if (!tripleOf[d].some(t => t.every(c => inS.has(c)))) throw new Error('NOT MAXIMAL, missing cell ' + d + ' in set ' + s.cells.join(','));
  }
}
// every excluded cell blocked; and 14+35=49 accounting
if (sets.some(s => !s.cells.every(c => c >= 0 && c < 49))) throw new Error('cell range');

// ---- maximal concyclic (circles) and collinear (lines) cell groups ----
const C4 = k => k*(k-1)*(k-2)*(k-3)/24;
const collinear3 = (p,q,r) => (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0]) === 0;
const groups = new Map(); // key -> {type, cells}
for (const q of quads) {
  const pts = q.map(xy);
  if (collinear3(pts[0], pts[1], pts[2]) && collinear3(pts[0], pts[1], pts[3])) {
    // collinear quartet: find the full maximal collinear set through the line
    const [p, u] = [pts[0], [pts[1][0]-pts[0][0], pts[1][1]-pts[0][1]]];
    const gcd = (a, b) => b ? gcd(b, a % b) : a;
    const g = Math.abs(u[0]) && Math.abs(u[1]) ? gcd(Math.abs(u[0]), Math.abs(u[1])) : Math.max(Math.abs(u[0]), Math.abs(u[1]));
    const du = [u[0]/g, u[1]/g];
    const cells = [];
    for (let t = -8; t <= 8; t++) {
      const x = p[0] + t*du[0], y = p[1] + t*du[1];
      if (x >= 0 && x <= 6 && y >= 0 && y <= 6) cells.push(x*7+y);
    }
    cells.sort((a,b)=>a-b);
    const key = 'L' + cells.join(',');
    if (!groups.has(key)) groups.set(key, { type: 'line', cells });
  } else {
    // circle through pts[0..2]; collect all grid cells on it
    const det = (a, b, c, d) => {
      const m = [[a[0],a[1],a[0]*a[0]+a[1]*a[1],1],[b[0],b[1],b[0]*b[0]+b[1]*b[1],1],[c[0],c[1],c[0]*c[0]+c[1]*c[1],1],[d[0],d[1],d[0]*d[0]+d[1]*d[1],1]];
      let v = 0;
      const perm=(arr)=>arr;
      // cofactor expansion along row 4
      const minor=(r, cIdx)=>{ const rows=[0,1,2,3].filter(r2=>r2!==r).map(r2=>m[r2].filter((_,j)=>j!==cIdx)); return rows[0][0]*(rows[1][1]*rows[2][2]-rows[1][2]*rows[2][1]) - rows[0][1]*(rows[1][0]*rows[2][2]-rows[1][2]*rows[2][0]) + rows[0][2]*(rows[1][0]*rows[2][1]-rows[1][1]*rows[2][0]); };
      v = m[3][0]*minor(3,0) - m[3][1]*minor(3,1) + m[3][2]*minor(3,2) - m[3][3]*minor(3,3);
      return v;
    };
    const cells = [];
    for (let x = 0; x <= 6; x++) for (let y = 0; y <= 6; y++) {
      if ([pts[0],pts[1],pts[2]].some(p2 => p2[0]===x && p2[1]===y)) { cells.push(x*7+y); continue; }
      if (det(pts[0], pts[1], pts[2], [x,y]) === 0) cells.push(x*7+y);
    }
    cells.sort((a,b)=>a-b);
    if (cells.length < 4) continue;
    const key = 'C' + cells.join(',');
    if (!groups.has(key)) groups.set(key, { type: 'circle', cells });
  }
}
const groupList = [...groups.values()].sort((a,b)=> (a.type+a.cells.join(',')) < (b.type+b.cells.join(',')) ? -1 : 1);
const circleList = groupList.filter(g => g.type === 'circle');
const lineList = groupList.filter(g => g.type === 'line');

// cross-check: every quartet must be inside exactly one group of its type
for (const q of quads) {
  const qs = [...q].sort((a,b)=>a-b).join(',');
  const pts = q.map(xy);
  const isLine = collinear3(pts[0], pts[1], pts[2]) && collinear3(pts[0], pts[1], pts[3]);
  const cand = (isLine ? lineList : circleList).filter(g => q.every(c => g.cells.includes(c)));
  if (cand.length !== 1) throw new Error('quartet group coverage fail at ' + qs);
}

// ---- per-set structure ----
function analyze(cells) {
  const inS = new Set(cells);
  const rows = Array(7).fill(0), cols = Array(7).fill(0);
  const d1 = {}, d2 = {}; // r-c, r+c counts
  for (const c of cells) { const [x,y] = xy(c); rows[x]++; cols[y]++; d1[x-y] = (d1[x-y]||0)+1; d2[x+y] = (d2[x+y]||0)+1; }
  const circleHist = {}, lineHist = {};
  for (const g of circleList) { const k = g.cells.filter(c => inS.has(c)).length; if (k) circleHist[k] = (circleHist[k]||0)+1; }
  for (const g of lineList)   { const k = g.cells.filter(c => inS.has(c)).length; if (k) lineHist[k]   = (lineHist[k]||0)+1; }
  const qHist = {0:0,1:0,2:0,3:0};
  for (const q of quads) { const k = q.filter(c => inS.has(c)).length; if (k > 3) throw new Error('unsafe?'); qHist[k]++; }
  const blockedBy = Array(N).fill(0); // for excluded cells: number of quartets completed
  for (let d = 0; d < N; d++) if (!inS.has(d)) blockedBy[d] = tripleOf[d].filter(t => t.every(c => inS.has(c))).length;
  // per-stone degrees: blocking-quartet degree (|Q intersect S| = 3 quartets containing the stone)
  const blockDeg = {};
  for (const q of quads) {
    const inside = q.filter(c => inS.has(c));
    if (inside.length === 3) for (const c of inside) blockDeg[c] = (blockDeg[c] || 0) + 1;
  }
  // per-stone degrees: carrying-circle degree (circles meeting S in exactly 3, containing the stone)
  const carryDeg = {};
  for (const g of circleList) {
    const t = g.cells.filter(c => inS.has(c));
    if (t.length === 3) for (const c of t) carryDeg[c] = (carryDeg[c] || 0) + 1;
  }
  // triples-on-circles broken down by circle size
  const circleTriplesBySize = {};
  for (const g of circleList) { const k = g.cells.filter(c => inS.has(c)).length; if (k === 3) circleTriplesBySize[g.cells.length] = (circleTriplesBySize[g.cells.length] || 0) + 1; }
  const lineTriplesBySize = {};
  for (const g of lineList) { const k = g.cells.filter(c => inS.has(c)).length; if (k === 3) lineTriplesBySize[g.cells.length] = (lineTriplesBySize[g.cells.length] || 0) + 1; }
  return { rows, cols, diag_rd: Object.fromEntries(Object.entries(d1).sort((a,b)=>a[0]-b[0]).map(([k,v])=>[k,v])), diag_sum: d2,
    circle_hist: circleHist, line_hist: lineHist, quartet_hist: qHist, blocked_by: blockedBy,
    block_degree: blockDeg, carry_degree: carryDeg,
    circle_triples_by_size: circleTriplesBySize, line_triples_by_size: lineTriplesBySize };
}

const perSet = sets.map(s => ({ rep: s.rep, d4: s.d4, cells: s.cells, ...analyze(s.cells) }));

// ---- aggregate facts ----
const repAnalyses = [1,2].map(i => perSet.find(s => s.rep === i && s.d4 === 'id'));

// circle/line groups maximally meeting S in exactly 3 (the "arcs/lines carrying triples")
const triplesOn = (cells) => {
  const inS = new Set(cells);
  const out = { circles: [], lines: [] };
  for (const g of circleList) { const t = g.cells.filter(c => inS.has(c)); if (t.length >= 3) out.circles.push({ size: g.cells.length, shared: t }); }
  for (const g of lineList)   { const t = g.cells.filter(c => inS.has(c)); if (t.length >= 3) out.lines.push({ size: g.cells.length, shared: t }); }
  out.circles.sort((a,b)=>a.shared[0]-b.shared[0]);
  out.lines.sort((a,b)=>a.shared[0]-b.shared[0]);
  return out;
};
const tripleStructure = {};
for (const s of sets) tripleStructure[s.rep + '|' + s.d4] = triplesOn(s.cells);

{
  const sL = lineList.reduce((a,g)=>a+C4(g.cells.length),0), sC = circleList.reduce((a,g)=>a+C4(g.cells.length),0);
  if (sL !== 660 || sC !== 5704 || sL + sC !== quads.length) throw new Error('group sums mismatch: lines ' + sL + ' circles ' + sC);
}
const result = {
  n: 7, N: 49,
  source: { representatives: repPath, quartets: qPath, quartets_count: quads.length },
  verified: {
    d4_images_distinct: keys.size === 16,
    all_safe_no_quartet_contained: true,
    all_maximal_every_excluded_cell_blocked: true,
    note: 'direct checks on the 16 sets obtained from the published representatives; NOT a re-proof that no other maximal set exists (published enumeration: Z_7(14)=16)',
  },
  catalog: { distinct_circles_size_ge4: circleList.length, distinct_lines_size_ge4: lineList.length,
    line_sizes: lineList.reduce((a,g)=>{a[g.cells.length]=(a[g.cells.length]||0)+1;return a;},{}),
    circle_sizes: circleList.reduce((a,g)=>{a[g.cells.length]=(a[g.cells.length]||0)+1;return a;},{}) },
  per_set: perSet,
  triple_structure: tripleStructure,
};
if (catalogPath) {
  const cat = {
    n: 7, N: 49,
    description: 'maximal collinear and concyclic grid-point groups of the 7x7 board (size >= 4); every forbidden quartet lies in exactly one group of its type (cross-checked)',
    verified_sums: {
      lines_sum_C_len4: lineList.reduce((a,g)=>a+C4(g.cells.length),0),
      circles_sum_C_len4: circleList.reduce((a,g)=>a+C4(g.cells.length),0),
      published_collinear_F7: 660, published_circular_F7: 5704,
      matches_published: true,
    },
    lines: lineList.map(g => g.cells), circles: circleList.map(g => g.cells),
  };
  fs.writeFileSync(catalogPath, JSON.stringify(cat) + '\n');
}
fs.writeFileSync(outPath, JSON.stringify(result) + '\n');
console.log(JSON.stringify({ sets: perSet.length, circles: circleList.length, lines: lineList.length,
  circle_sizes: result.catalog.circle_sizes, line_sizes: result.catalog.line_sizes,
  rep1_rows: repAnalyses[0].rows, rep1_cols: repAnalyses[0].cols, rep1_circlehist: repAnalyses[0].circle_hist, rep1_linehist: repAnalyses[0].line_hist, rep1_qhist: repAnalyses[0].quartet_hist,
  rep2_rows: repAnalyses[1].rows, rep2_cols: repAnalyses[1].cols, rep2_circlehist: repAnalyses[1].circle_hist, rep2_linehist: repAnalyses[1].line_hist, rep2_qhist: repAnalyses[1].quartet_hist }));
