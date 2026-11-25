// Five-row (5 x m), q=7 deficit-maximal witness search: m=19 campaign.
// Self-contained TypeScript, integer arithmetic only, deterministic (mulberry32).
// Reproduces every number in research/log/2026-11-10-five-row-q7-m19-search.md:
//   1. Dangerous-curve census by row-pair enumeration (100 curves incl. 5 row lines).
//   2. Independent census by all-triples enumeration (verify {7:8, 8:87, >=9:0}).
//   3. Independent witness checker (all stone-triple circles + all pair lines, det4).
//   4. SA search (from scratch and from the extended 5x18 witness of K0332).
//   5. Exhaustive 1- and 2-move local search from a cost-1 state.
// Run with any TypeScript runner, e.g.: npx ts-node five_row_q7_m19_search.ts
// 2026-11-10/11 session result: no m=19 witness found (best cost 1 of 14*100+14 scale).

const W = 19, H = 5, NP = W * H;

// ---------- integer geometry ----------
const gcd = (a: number, b: number): number => b === 0 ? Math.abs(a) : gcd(b, a % b);
const det3 = (m: number[][]): number =>
  m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]);
function circleCoeff(p1: [number, number], p2: [number, number], p3: [number, number]): number[] | null {
  // primitive integer coefficients A,B,C,D of A(x^2+y^2)+Bx+Cy+D=0, A>0, gcd 1
  const f = (p: [number, number]) => [p[0] * p[0] + p[1] * p[1], p[0], p[1], 1];
  const m = [f(p1), f(p2), f(p3)];
  const A = det3([[m[0][1], m[0][2], m[0][3]], [m[1][1], m[1][2], m[1][3]], [m[2][1], m[2][2], m[2][3]]]);
  if (A === 0) return null; // collinear
  const B = -det3([[m[0][0], m[0][2], m[0][3]], [m[1][0], m[1][2], m[1][3]], [m[2][0], m[2][2], m[2][3]]]);
  const C = det3([[m[0][0], m[0][1], m[0][3]], [m[1][0], m[1][1], m[1][3]], [m[2][0], m[2][1], m[2][3]]]);
  const D = -det3([[m[0][0], m[0][1], m[0][2]], [m[1][0], m[1][1], m[1][2]], [m[2][0], m[2][1], m[2][2]]]);
  const g = [A, B, C, D].reduce((s, v) => gcd(s, v), 0) || 1;
  const s = A > 0 ? 1 : -1;
  return [A * s / g, B * s / g, C * s / g, D * s / g];
}
const on = (c: number[], x: number, y: number) => c[0] * (x * x + y * y) + c[1] * x + c[2] * y + c[3] === 0;
const onLine = (x1: number, y1: number, x2: number, y2: number, x: number, y: number) => (x - x1) * (y2 - y1) === (y - y1) * (x2 - x1);
function det4(m: number[][]): number {
  const a = m.map(row => row.slice());
  let sign = 1, prev = 1;
  for (let k = 0; k < 3; k++) {
    if (a[k][k] === 0) { let p = -1; for (let i = k + 1; i < 4; i++) if (a[i][k] !== 0) { p = i; break; } if (p < 0) return 0; [a[k], a[p]] = [a[p], a[k]]; sign = -sign; }
    const piv = a[k][k];
    for (let i = k + 1; i < 4; i++) for (let j = k + 1; j < 4; j++) a[i][j] = (a[i][j] * piv - a[i][k] * a[k][j]) / prev;
    prev = piv;
  }
  return sign * a[3][3];
}
const M4 = (p: [number, number]) => [p[0] * p[0] + p[1] * p[1], p[0], p[1], 1];

// ---------- census method A: row-pair enumeration ----------
function censusRowPair() {
  const curveMap = new Map<string, number>();
  const curvePts: number[][] = [];
  const addCurve = (key: string, pts: number[]) => { if (curveMap.has(key)) return; curveMap.set(key, curvePts.length); curvePts.push(pts); };
  let constructions = 0;
  // Any circle with >=7 points in a 5-row grid has two rows with >=2 points each
  // (7 points / max 2 per row forces it), so enumerating circles through
  // 2 points of row a and 1 point of row b, testing row b for a second point, is complete.
  for (let a = 0; a < H; a++) for (let b = 0; b < H; b++) {
    if (a === b) continue;
    for (let x1 = 0; x1 < W; x1++) for (let x2 = x1 + 1; x2 < W; x2++) for (let u = 0; u < W; u++) {
      const c = circleCoeff([x1, a], [x2, a], [u, b]);
      constructions++;
      if (!c) continue;
      let cntB = 0; for (let v = 0; v < W; v++) if (on(c, v, b)) cntB++;
      if (cntB < 2) continue;
      const pts: number[] = [];
      for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (on(c, x, y)) pts.push(y * W + x);
      if (pts.length >= 7) addCurve(c.join(','), pts);
    }
  }
  for (let y = 0; y < H; y++) { const pts: number[] = []; for (let x = 0; x < W; x++) pts.push(y * W + x); addCurve('row' + y, pts); }
  const dist: Record<number, number> = {};
  for (const pts of curvePts) dist[pts.length] = (dist[pts.length] || 0) + 1;
  return { constructions, curves: curvePts.length, dist, curvePts, curveMap };
}

// ---------- census method B: all triples (independent) ----------
function censusTriples() {
  const pts: [number, number][] = [];
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) pts.push([x, y]);
  const keys = new Set<string>();
  let triples = 0, collinear = 0;
  for (let i = 0; i < NP; i++) for (let j = i + 1; j < NP; j++) for (let k = j + 1; k < NP; k++) {
    if (onLine(pts[i][0], pts[i][1], pts[j][0], pts[j][1], pts[k][0], pts[k][1])) { collinear++; continue; }
    triples++;
    const c = circleCoeff(pts[i], pts[j], pts[k]);
    if (c) keys.add(c.join(','));
  }
  let seven = 0, eight = 0, more = 0;
  for (const key of keys) {
    const c = key.split(',').map(Number);
    let n = 0;
    for (const p of pts) if (on(c, p[0], p[1])) n++;
    if (n === 7) seven++; else if (n === 8) eight++; else if (n > 8) more++;
  }
  return { triples, collinear, unique: keys.size, seven, eight, more };
}

// ---------- independent witness checker ----------
function checkWitness(rows: number[][], q: number): { safe: boolean; maximal: boolean; unblocked: [number, number][] } {
  const stones: [number, number][] = [];
  rows.forEach((xs, y) => xs.forEach(x => stones.push([x, y])));
  const stoneSet = new Set(stones.map(([x, y]) => y * W + x));
  const n = stones.length, r = q - 1;
  let maxLine = 0, maxCirc = 0;
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    let c = 0;
    for (const s of stones) if (onLine(stones[i][0], stones[i][1], stones[j][0], stones[j][1], s[0], s[1])) c++;
    if (c > maxLine) maxLine = c;
  }
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) for (let k = j + 1; k < n; k++) {
    if (onLine(stones[i][0], stones[i][1], stones[j][0], stones[j][1], stones[k][0], stones[k][1])) continue;
    let c = 0;
    for (const s of stones) if (det4([M4(stones[i]), M4(stones[j]), M4(stones[k]), M4(s)]) === 0) c++;
    if (c > maxCirc) maxCirc = c;
  }
  const occ = rows.map(r2 => r2.length);
  const unblocked: [number, number][] = [];
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    if (stoneSet.has(y * W + x)) continue;
    if (occ[y] === r) continue; // full row line blocks
    const p: [number, number] = [x, y];
    let best = 0;
    outer:
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
      if (onLine(p[0], p[1], stones[i][0], stones[i][1], stones[j][0], stones[j][1])) continue;
      let c = 0;
      for (const s of stones) if (det4([M4(p), M4(stones[i]), M4(stones[j]), M4(s)]) === 0) c++;
      if (c > best) best = c;
      if (best >= r) break outer;
    }
    if (best < r) unblocked.push([x, y]);
  }
  return { safe: maxLine <= r && maxCirc <= r, maximal: unblocked.length === 0, unblocked };
}

// ---------- SA search (deterministic) ----------
let seed = 2718281;
const rnd = () => { seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };

function saSearch(curvePts: number[][], defRow: number, inits: number[][][], restarts: number, iters: number) {
  const pointCurves: number[][] = Array.from({ length: NP }, () => []);
  curvePts.forEach((pts, i) => pts.forEach(p => pointCurves[p].push(i)));
  const NC = curvePts.length;
  const cnt = new Int32Array(NC);
  const occRow: number[][] = Array.from({ length: H }, () => Array(W).fill(0));
  let violTotal = 0;
  const f = (c: number) => c > 6 ? c - 6 : 0;
  const changePoint = (p: number, dir: number) => {
    occRow[(p / W) | 0][p % W] += dir;
    for (const i of pointCurves[p]) { const o = cnt[i]; cnt[i] = o + dir; violTotal += f(o + dir) - f(o); }
  };
  const unblockedCount = () => {
    let un = 0;
    for (let x = 0; x < W; x++) {
      if (occRow[defRow][x]) continue;
      let ok = false;
      for (const i of pointCurves[defRow * W + x]) if (cnt[i] >= 6) { ok = true; break; }
      if (!ok) un++;
    }
    return un;
  };
  let bestCost = Infinity, bestRows: number[][] | null = null, witness: number[][] | null = null;
  for (let rs = 0; rs < restarts && !witness; rs++) {
    const rows: number[][] = [];
    if (rs < inits.length) { for (let y = 0; y < H; y++) rows.push(inits[rs][y].slice()); }
    else {
      const src = bestRows ?? inits[rs % inits.length];
      for (let y = 0; y < H; y++) rows.push(src[y].slice());
      for (let m2 = 0; m2 < 4; m2++) { const r = Math.floor(rnd() * H); const si = Math.floor(rnd() * rows[r].length); const nx = Math.floor(rnd() * W); if (!rows[r].includes(nx)) rows[r][si] = nx; }
    }
    cnt.fill(0); for (let y = 0; y < H; y++) occRow[y].fill(0);
    violTotal = 0;
    for (let y = 0; y < H; y++) for (const x of rows[y]) changePoint(y * W + x, 1);
    let c = 100 * violTotal + unblockedCount();
    for (let it = 0; it < iters; it++) {
      const T = 12 * (1 - it / iters) + 0.08;
      let r: number, ox: number, nx: number, si: number;
      if (rnd() < 0.6) {
        let x = -1;
        for (let t = 0; t < 6; t++) { const x2 = Math.floor(rnd() * W); if (!occRow[defRow][x2]) { x = x2; break; } }
        if (x < 0) continue;
        const cs = pointCurves[defRow * W + x];
        if (cs.length === 0) continue;
        const i = cs[Math.floor(rnd() * cs.length)];
        const cand = curvePts[i].filter(p => !occRow[(p / W) | 0][p % W] && ((p / W) | 0) !== defRow);
        if (cand.length === 0) continue;
        const pn = cand[Math.floor(rnd() * cand.length)];
        r = (pn / W) | 0; nx = pn % W;
        si = Math.floor(rnd() * rows[r].length);
        ox = rows[r][si];
      } else {
        r = Math.floor(rnd() * H);
        si = Math.floor(rnd() * rows[r].length);
        nx = Math.floor(rnd() * W);
        if (occRow[r][nx]) continue;
        ox = rows[r][si];
      }
      if (occRow[r][nx]) continue;
      changePoint(r * W + ox, -1); changePoint(r * W + nx, 1);
      rows[r][si] = nx;
      const c2 = 100 * violTotal + unblockedCount();
      const d = c2 - c;
      if (d <= 0 || rnd() < Math.exp(-d / T)) {
        c = c2;
        if (c < bestCost) { bestCost = c; bestRows = rows.map(r2 => r2.slice()); }
        if (c === 0) { witness = rows.map(r2 => r2.slice().sort((a, b) => a - b)); break; }
      } else {
        changePoint(r * W + nx, -1); changePoint(r * W + ox, 1);
        rows[r][si] = ox;
      }
    }
  }
  return { witness, bestCost, bestRows };
}

// ---------- exhaustive 1/2-move local search ----------
function localSearch(curvePts: number[][], start: number[][][]) {
  const pointCurves: number[][] = Array.from({ length: NP }, () => []);
  curvePts.forEach((pts, i) => pts.forEach(p => pointCurves[p].push(i)));
  const NC = curvePts.length;
  const f = (c: number) => c > 6 ? c - 6 : 0;
  const evalRows = (rows: number[][]): number => {
    const cnt = new Int32Array(NC);
    const occ: number[][] = Array.from({ length: H }, () => Array(W).fill(0));
    for (let y = 0; y < H; y++) for (const x of rows[y]) occ[y][x] = 1;
    for (let y = 0; y < H; y++) for (const x of rows[y]) for (const i of pointCurves[y * W + x]) cnt[i]++;
    let viol = 0;
    for (let i = 0; i < NC; i++) viol += f(cnt[i]);
    let un = 0;
    for (let x = 0; x < W; x++) {
      if (occ[0][x]) continue;
      let ok = false;
      for (const i of pointCurves[x]) if (cnt[i] >= 6) { ok = true; break; }
      if (!ok) un++;
    }
    return 100 * viol + un;
  };
  const results: any[] = [];
  for (const s0 of start) {
    let found: number[][] | null = null;
    const moves: [number, number, number][] = [];
    for (let y = 0; y < H; y++) for (let si = 0; si < s0[y].length; si++) for (let nx = 0; nx < W; nx++) if (!s0[y].includes(nx)) moves.push([y, si, nx]);
    // 1-move exhaustive
    outer1:
    for (const [y1, si1, nx1] of moves) {
      const rows = s0.map(r => r.slice());
      rows[y1][si1] = nx1;
      if (evalRows(rows) === 0) { found = rows.map(r => r.slice().sort((a, b) => a - b)); break outer1; }
    }
    // 2-move exhaustive (distinct stones)
    if (!found) {
      outer:
      for (let m1 = 0; m1 < moves.length; m1++) for (let m2 = m1 + 1; m2 < moves.length; m2++) {
        const [y1, si1, nx1] = moves[m1];
        const [y2, si2, nx2] = moves[m2];
        if (y1 === y2 && si1 === si2) continue;
        const rows = s0.map(r => r.slice());
        rows[y1][si1] = nx1;
        if (rows[y2].includes(nx2)) continue;
        rows[y2][si2] = nx2;
        if (evalRows(rows) === 0) { found = rows.map(r => r.slice().sort((a, b) => a - b)); break outer; }
      }
    }
    results.push({ c0: evalRows(s0), found: !!found, witness: found });
  }
  return results;
}

// ---------- main ----------
export function main() {
  const A = censusRowPair();
  const circles = A.curvePts.filter(pts => pts.length < W); // the 95 circles (row lines have W points)
  const B = censusTriples();
  console.log(JSON.stringify({
    censusRowPair: { constructions: A.constructions, dist: A.dist },
    censusTriples: B,
    agree: (A.dist[7] || 0) === B.seven && (A.dist[8] || 0) === B.eight,
  }, null, 2));
  // SA from scratch + extended 5x18 witness warm starts (K0332 witness, deficit row 0)
  const base: number[][] = [[5, 8, 12, 14, 17], [1, 3, 6, 7, 8, 10], [1, 3, 6, 7, 10, 12], [2, 4, 7, 9, 11, 14], [4, 6, 7, 9, 11, 12]];
  const inits: number[][][] = [];
  for (const mirror of [false, true]) for (const shift of [0, 1]) {
    const tf = (x: number) => (mirror ? 17 - x : x) + shift;
    inits.push(base.map((xs, y) => xs.map(tf).sort((a, b) => a - b)));
  }
  const sa = saSearch(circles, 0, inits, 48, 25000);
  console.log(JSON.stringify({ saBestCost: sa.bestCost, witness: sa.witness, best: sa.bestRows }, null, 2));
  if (sa.witness) {
    const chk = checkWitness(sa.witness, 7);
    console.log(JSON.stringify({ independentCheck: chk }, null, 2));
  }
  // exhaustive local search from best states
  if (sa.bestRows) {
    const ls = localSearch(circles, [sa.bestRows]);
    console.log(JSON.stringify({ localSearch: ls }, null, 2));
  }
}
main();
