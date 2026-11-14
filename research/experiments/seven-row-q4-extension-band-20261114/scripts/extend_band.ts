// extend_band.ts — constructive extension and exact verification of the
// 7xm q=4 row-deficient witness band, widths m=22..35 (M_{7,4} >= 36).
// High-speed lane, run 9, batch 5 (2026-11-14).
// Pure TypeScript + BigInt exact rational arithmetic. No repo code, no SAT solver.
// Extends K0827 / seven-row-q4-q6-witness-search-20261114 (band m=4..21).
//
// Blocking-coverage lemma:
//  - cell (x,y) is BLOCKED iff some circle or line through >= 3 stones contains it
//    (adding a stone there completes a 4-stone curve => violation => maximality kept);
//  - a row with exactly q-1 = 3 stones blocks its whole horizontal line;
//  - if all 7 rows are covered contiguously on x in [0,W) and all stones have x < W,
//    the config is a row-deficient maximal safe witness for every width
//    maxX < w <= W (subset argument on cells; safety/deficiency width-independent).
//
// How the configs were found (deterministic, no randomness):
//  C22 = the m=21 frontier witness itself; its rows 5,6 blocking coverage is
//        contiguous through x=21, so w=22 is a free empty-column extension.
//  CA  = m=21 witness + adds (22,5),(22,6) + hill-climb move (13,5)->(14,5)
//        (width-capped search, cap 23); maxX=22, coverage W=31 -> m=23..31.
//  CB  = m=21 witness + greedy adds (25,5),(23,6) (W=27) + hill-climb moves
//        (13,5)->(14,5), (11,3)->(20,3), (16,4)->(14,4), (19,5)->(26,5);
//        maxX=26, coverage W=35 -> m=27..35 (used for m=32..35).
//  Search primitives as run: greedy candidates = the gap cell itself plus all integer
//  points (rows 5,6) on circles/lines through two stones and a gap cell, scored by the
//  resulting contiguous coverage; hill-climb accepts a same-row move only if W strictly
//  increases and W > maxX (validity). Verification below is independent of the search.

type Pt = [number, number];
type F = { n: bigint; d: bigint };
function gcd(a: bigint, b: bigint): bigint { while (b) { const t = a % b; a = b; b = t; } return a || 1n; }
function mk(n: bigint, d: bigint): F { if (d < 0n) { n = -n; d = -d; } const g = gcd(n < 0n ? -n : n, d); return { n: n / g, d: d / g }; }
const B = (x: number) => BigInt(x);
const collinear = (x1: number, y1: number, x2: number, y2: number, x3: number, y3: number) =>
  (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1) === 0;
function circle3(x1: number, y1: number, x2: number, y2: number, x3: number, y3: number) {
  const A = 2n * B(x2 - x1), Bp = 2n * B(y2 - y1), C = B(x2 * x2 - x1 * x1 + y2 * y2 - y1 * y1);
  const D = 2n * B(x3 - x1), E = 2n * B(y3 - y1), Fc = B(x3 * x3 - x1 * x1 + y3 * y3 - y1 * y1);
  const dd = A * E - D * Bp;
  const cx = mk(C * E - Fc * Bp, dd), cy = mk(A * Fc - D * C, dd);
  const dxn = B(x1) * cx.d - cx.n, dyn = B(y1) * cy.d - cy.n;
  const r2 = mk(dxn * dxn * cy.d * cy.d + dyn * dyn * cx.d * cx.d, cx.d * cx.d * cy.d * cy.d);
  return { cx, cy, r2 };
}
function onCirc(x: number, y: number, cx: F, cy: F, r2: F): boolean {
  const dxn = B(x) * cx.d - cx.n, dyn = B(y) * cy.d - cy.n;
  const ln = dxn * dxn * cy.d * cy.d + dyn * dyn * cx.d * cx.d;
  const ld = cx.d * cx.d * cy.d * cy.d;
  return ln * r2.d === r2.n * ld;
}

// all blocking curves (>= 3 stones) of a config, plus max stone counts (safety)
function blockingCurves(stones: Pt[]) {
  const n = stones.length;
  const circles: { cx: F; cy: F; r2: F }[] = [];
  const seen = new Set<string>();
  let maxCirc = 0;
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) for (let k = j + 1; k < n; k++) {
    const [x1, y1] = stones[i], [x2, y2] = stones[j], [x3, y3] = stones[k];
    if (collinear(x1, y1, x2, y2, x3, y3)) continue;
    const c = circle3(x1, y1, x2, y2, x3, y3);
    const key = c.cx.n + "/" + c.cx.d + "|" + c.cy.n + "/" + c.cy.d + "|" + c.r2.n + "/" + c.r2.d;
    if (seen.has(key)) continue;
    seen.add(key);
    let cnt = 0;
    for (const [sx, sy] of stones) if (onCirc(sx, sy, c.cx, c.cy, c.r2)) cnt++;
    maxCirc = Math.max(maxCirc, cnt);
    if (cnt >= 3) circles.push(c);
  }
  const lineMap = new Map<string, { a: number; b: number; c: number; cnt: number }>();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    const [x1, y1] = stones[i], [x2, y2] = stones[j];
    let a = y2 - y1, b = x1 - x2; const c = a * x1 + b * y1;
    if (a === 0 && b === 0) continue;
    let ga = Number(gcd(BigInt(Math.abs(a) || 1), BigInt(Math.abs(b) || 1))); if (ga === 0) ga = 1;
    a /= ga; b /= ga; const cc = c / ga;
    const key = a + "," + b + "," + cc;
    if (!lineMap.has(key)) { let cnt = 0; for (const [sx, sy] of stones) if (a * sx + b * sy === cc) cnt++; lineMap.set(key, { a, b, c: cc, cnt }); }
  }
  let maxLine = 0;
  const lines3: { a: number; b: number; c: number }[] = [];
  for (const L of lineMap.values()) { maxLine = Math.max(maxLine, L.cnt); if (L.cnt >= 3) lines3.push(L); }
  return { circles, lines3, maxCirc, maxLine };
}

// exact verification at width m (q = 4): safety + maximality + deficiency + grid
function verifyWidth(stones: Pt[], curves: ReturnType<typeof blockingCurves>, m: number, q: number) {
  const stoneSet = new Set(stones.map(s => s.join(",")));
  let uncovered = 0;
  outer: for (let y = 0; y < 7; y++) for (let x = 0; x < m; x++) {
    if (stoneSet.has(x + "," + y)) continue;
    for (const L of curves.lines3) if (L.a * x + L.b * y === L.c) continue outer;
    for (const c of curves.circles) if (onCirc(x, y, c.cx, c.cy, c.r2)) continue outer;
    uncovered++;
  }
  const rows = [0, 1, 2, 3, 4, 5, 6].map(y => stones.filter(s => s[1] === y).length);
  let inGrid = true;
  for (const [x, y] of stones) if (x < 0 || x >= m || y < 0 || y >= 7) inGrid = false;
  return { pass: uncovered === 0 && curves.maxCirc < q && curves.maxLine < q && inGrid && rows.some(r => r <= q - 2), uncovered, rows, inGrid };
}

// contiguous blocking coverage over all 7 rows (cell occupied or blocked), x <= 60
function contiguousW(stones: Pt[]): number {
  const curves = blockingCurves(stones);
  const st: Set<number>[] = [0, 1, 2, 3, 4, 5, 6].map(y => new Set(stones.filter(s => s[1] === y).map(s => s[0])));
  const blockedAll: Set<number>[] = [0, 1, 2, 3, 4, 5, 6].map(() => new Set<number>());
  for (let y = 0; y < 7; y++) for (let x = 0; x <= 60; x++) {
    for (const L of curves.lines3) if (L.a * x + L.b * y === L.c) { blockedAll[y].add(x); break; }
    if (blockedAll[y].has(x)) continue;
    for (const c of curves.circles) if (onCirc(x, y, c.cx, c.cy, c.r2)) { blockedAll[y].add(x); break; }
  }
  let W = 0;
  while (W <= 60 && [0, 1, 2, 3, 4, 5, 6].every(y => blockedAll[y].has(W) || st[y].has(W))) W++;
  return W;
}

// the three found configs (see header for provenance and the found-by sequences)
const C22: Pt[] = [[0,0],[1,0],[2,0],[0,1],[4,1],[5,1],[1,2],[5,2],[6,2],[9,3],[10,3],[11,3],[9,4],[16,4],[18,4],[13,5],[19,5],[1,6]];
const CA: Pt[] = [[0,0],[1,0],[2,0],[0,1],[4,1],[5,1],[1,2],[5,2],[6,2],[9,3],[10,3],[11,3],[9,4],[16,4],[18,4],[19,5],[1,6],[22,5],[22,6],[14,5]];
const CB: Pt[] = [[0,0],[1,0],[2,0],[0,1],[4,1],[5,1],[1,2],[5,2],[6,2],[9,3],[10,3],[20,3],[9,4],[18,4],[14,4],[25,5],[1,6],[23,6],[14,5],[26,5]];

function main() {
  const configs: Record<string, Pt[]> = { C22, CA, CB };
  let allPass = true;
  for (let m = 22; m <= 35; m++) {
    const name = m === 22 ? "C22" : (m <= 31 ? "CA" : "CB");
    const curves = blockingCurves(configs[name]);
    const v = verifyWidth(configs[name], curves, m, 4);
    if (!v.pass) allPass = false;
    console.log("m=" + m + " config=" + name + " pass=" + v.pass + " uncovered=" + v.uncovered);
  }
  console.log("coverageW: C22=" + contiguousW(C22) + " CA=" + contiguousW(CA) + " CB=" + contiguousW(CB));
  console.log(allPass ? "ALL WIDTHS 22..35 PASS => M_{7,4} >= 36" : "FAIL");
}
main();