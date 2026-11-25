// Independent checker for the 5x15 q=6 deficit-maximal witness (24 stones).
// Integer arithmetic only (4x4 Bareiss determinants). No external dependencies.
// Run with any TypeScript runner, e.g.: npx ts-node q56_witness_check.ts
// Exits 0 and prints a JSON summary when every check passes.
// 2026-11-10: every check PASS recorded (max stones on any curve = 5,
// 51/51 empty points blocked, H = 244, U = 249).
// Intended repo path on permission recovery:
//   research/experiments/q56-five-row-20261110/scripts/q56_witness_check.ts

const rows: number[][] = [
  [3, 6, 7, 8, 10],
  [3, 5, 6, 7, 11],
  [2, 3, 4, 10, 12],
  [2, 4, 5, 6, 9],
  [0, 2, 4, 12],
];
const W = 15, H = 5, r = 5, q = 6;

function det4(m: number[][]): number {
  const a = m.map(row => row.slice());
  let sign = 1, prev = 1;
  for (let k = 0; k < 3; k++) {
    if (a[k][k] === 0) {
      let p = -1;
      for (let i = k + 1; i < 4; i++) if (a[i][k] !== 0) { p = i; break; }
      if (p < 0) return 0;
      [a[k], a[p]] = [a[p], a[k]]; sign = -sign;
    }
    const piv = a[k][k];
    for (let i = k + 1; i < 4; i++) for (let j = k + 1; j < 4; j++)
      a[i][j] = (a[i][j] * piv - a[i][k] * a[k][j]) / prev;
    prev = piv;
  }
  return sign * a[3][3];
}

function det3(m: number[][]): number {
  return m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
    - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
    + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]);
}

const M4 = (p: [number, number]) => [p[0] * p[0] + p[1] * p[1], p[0], p[1], 1];
const onLine = (x1: number, y1: number, x2: number, y2: number, x: number, y: number) =>
  (x - x1) * (y2 - y1) === (y - y1) * (x2 - x1);
const gcd = (a: number, b: number): number => b === 0 ? Math.abs(a) : gcd(b, a % b);

function circleCoeff(p1: [number, number], p2: [number, number], p3: [number, number]) {
  const m = [M4(p1), M4(p2), M4(p3)];
  const A = det3([[m[0][1], m[0][2], m[0][3]], [m[1][1], m[1][2], m[1][3]], [m[2][1], m[2][2], m[2][3]]]);
  const B = -det3([[m[0][0], m[0][2], m[0][3]], [m[1][0], m[1][2], m[1][3]], [m[2][0], m[2][2], m[2][3]]]);
  const C = det3([[m[0][0], m[0][1], m[0][3]], [m[1][0], m[1][1], m[1][3]], [m[2][0], m[2][1], m[2][3]]]);
  const D = -det3([[m[0][0], m[0][1], m[0][2]], [m[1][0], m[1][1], m[1][2]], [m[2][0], m[2][1], m[2][2]]]);
  if (A === 0) return null; // collinear
  const g = [A, B, C, D].reduce((s, v) => gcd(s, v), 0);
  const s = A > 0 ? 1 : -1;
  return [A * s / g, B * s / g, C * s / g, D * s / g];
}

const onCircle = (c: number[], p: [number, number]) =>
  c[0] * (p[0] * p[0] + p[1] * p[1]) + c[1] * p[0] + c[2] * p[1] + c[3] === 0;

const stones: [number, number][] = [];
rows.forEach((xs, y) => xs.forEach(x => stones.push([x, y])));
const stoneSet = new Set(stones.map(([x, y]) => y * W + x));
const n = stones.length;

function fail(msg: string): never { throw new Error(msg); }

// 1. row capacity
for (const xs of rows) if (xs.length > r) fail("row capacity exceeded");
if (n !== 24) fail("expected 24 stones");

// 2. safety: no 6 stones on one curve (circle or line)
let maxOnCurve = 0;
for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
  let cnt = 0;
  for (const s of stones) if (onLine(stones[i][0], stones[i][1], stones[j][0], stones[j][1], s[0], s[1])) cnt++;
  if (cnt > maxOnCurve) maxOnCurve = cnt;
  for (let k = j + 1; k < n; k++) {
    if (onLine(stones[i][0], stones[i][1], stones[j][0], stones[j][1], stones[k][0], stones[k][1])) continue;
    let c2 = 0;
    for (const s of stones) if (det4([M4(stones[i]), M4(stones[j]), M4(stones[k]), M4(s)]) === 0) c2++;
    if (c2 > maxOnCurve) maxOnCurve = c2;
  }
}
if (maxOnCurve > r) fail("unsafe: " + maxOnCurve + " stones on one curve");

// 3. maximality: every empty point is blocked by a curve holding exactly 5 stones
const seen = new Map<string, number[]>();
for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) for (let k = j + 1; k < n; k++) {
  if (onLine(stones[i][0], stones[i][1], stones[j][0], stones[j][1], stones[k][0], stones[k][1])) continue;
  const c = circleCoeff(stones[i], stones[j], stones[k]);
  if (c) seen.set(c.join(","), c);
}
const blockerCircles: { coeff: number[]; stones: [number, number][] }[] = [];
for (const c of seen.values()) {
  const onS = stones.filter(s => onCircle(c, s));
  if (onS.length === 5) blockerCircles.push({ coeff: c, stones: onS });
}
let blockedCount = 0, emptyCount = 0; const unblocked: [number, number][] = [];
for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
  if (stoneSet.has(y * W + x)) continue;
  emptyCount++;
  let ok = rows[y].length === 5; // full row line blocks its own empty points
  if (!ok) for (const bc of blockerCircles) if (onCircle(bc.coeff, [x, y])) { ok = true; break; }
  if (ok) blockedCount++; else unblocked.push([x, y]);
}
if (unblocked.length) fail("unblocked empty points: " + JSON.stringify(unblocked));

// 4. upper bound: K0318 substitution for (w,q)=(5,6) with the cross-row pair improvement
const C = (nn: number, k: number) => { let out = 1; for (let i = 0; i < k; i++) out = out * (nn - i) / (i + 1); return out; };
const w = 5, r2 = q - 1, a = r2 - 1, N = r2 * (w - 1);
const Q = C(N, 3) - (w - 1) * C(r2, 3);
const d0 = C(r2, 3), d1 = C(r2 - 1, 3);
const e = C(r2 - 1, 2) - Math.floor((r2 - 1) / 2);
const P = C(N, 2) - (w - 1) * C(r2, 2);
const Y = a * Math.min(Math.floor(C(N, 2) / C(r2 - 1, 2)), Math.floor(P / e));
let Hmax = 0; const argmax: number[][] = [];
for (let x = 0; x * d0 <= Q; x++) {
  const ymax = Math.min(Y, Math.floor((Q - x * d0) / d1));
  if (2 * x + ymax > Hmax) { Hmax = 2 * x + ymax; argmax.length = 0; }
  if (2 * x + ymax === Hmax) argmax.push([x, ymax]);
}
const U = r2 + Hmax;
if (U !== 249) fail("upper bound recomputation differs: " + U);

console.log(JSON.stringify({
  stones: n, row_occupancy: rows.map(xs => xs.length),
  max_stones_on_any_curve: maxOnCurve, safe: true,
  empty_points: emptyCount, blocked: blockedCount, maximal: true,
  upper_bound: { r: r2, a, N, Q, d0, d1, e, P, Y, H: Hmax, argmax, U },
  bounds: { lower_M_5_6: 16, upper_M_5_6: 249 },
  status: "PASS",
}, null, 2));
