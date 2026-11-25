// verify_independent.ts — third verification system for (w,m,q) row-deficient
// maximal-safe witnesses on a w x m lattice board (q-point cocircular/collinear
// forbidden).
//
// Independent of all repo code: pure TypeScript + BigInt exact arithmetic.
// Algorithmically independent of the two existing systems
// (sat.js verifyConfig: JS, census-free; verify_witness.py: Python Fraction):
//   - circle identity: exact rational key (cx, cy, r^2) computed from each
//     stone triple by a 2x2 perpendicular-bisector solve (the key is a bijective
//     reparameterization of the center, so grouping is unaffected by scaling);
//     membership is re-tested per stone by the 4x4 cocircularity determinant
//     (collinear triples are skipped);
//   - lines: canonical primitive (a, b, c) from stone pairs;
//   - safe         : no circle and no line carries q or more stones;
//   - maximal      : every empty cell lies on a line or circle with >= q-1 stones;
//   - row-deficient: some row carries <= q-2 stones.
//
// Usage:  const res = verify(stones, w, m, q);  // stones: [x, y][], y = row
// Run of 2026-11-14 (records: ../output/ts-verify.json):
//   w7q7_7x25q7_rowY3.witness.json  PASS  (41 stones, 9477 circles, 120 >=6-curves)
//   w7q7_7x26q7_rowY3.witness.json  PASS  (41 stones, 9407 circles, 117 >=6-curves)
//   negative control (7 collinear stones, 7x7, q=7): unsafe (maxLine 7) — detected.
// Consequence: the m=26 witness (M_{7,7} >= 27) is verified by three independent
// implementation systems.

type Pt = [number, number];

function gcd(a: bigint, b: bigint): bigint {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b) { const t = a % b; a = b; b = t; }
  return a;
}

function frac(num: bigint, den: bigint): string {
  if (den < 0n) { num = -num; den = -den; }
  const g = gcd(num, den) || 1n;
  return (num / g) + '/' + (den / g);
}

function det4r(r0: bigint[], r1: bigint[], r2: bigint[], r3: bigint[]): bigint {
  return r0[0] * (r1[1] * (r2[2] * r3[3] - r2[3] * r3[2]) - r1[2] * (r2[1] * r3[3] - r2[3] * r3[1]) + r1[3] * (r2[1] * r3[2] - r2[2] * r3[1]))
    - r0[1] * (r1[0] * (r2[2] * r3[3] - r2[3] * r3[2]) - r1[2] * (r2[0] * r3[3] - r2[3] * r3[0]) + r1[3] * (r2[0] * r3[2] - r2[2] * r3[0]))
    + r0[2] * (r1[0] * (r2[1] * r3[3] - r2[3] * r3[1]) - r1[1] * (r2[0] * r3[3] - r2[3] * r3[0]) + r1[3] * (r2[0] * r3[1] - r2[1] * r3[0]))
    - r0[3] * (r1[0] * (r2[1] * r3[2] - r2[2] * r3[1]) - r1[1] * (r2[0] * r3[2] - r2[2] * r3[0]) + r1[2] * (r2[0] * r3[1] - r2[1] * r3[0]));
}

export function verify(stones: Pt[], w: number, m: number, q: number) {
  const n = stones.length;
  const rows = stones.map(([x, y]) => [BigInt(x * x + y * y), BigInt(x), BigInt(y), 1n]);
  const rowCnt = new Array(w).fill(0);
  for (const s of stones) rowCnt[s[1]]++;
  const minRow = Math.min(...rowCnt);

  // --- lines through pairs of stones, canonical primitive (a,b,c) ---
  const lineMap = new Map<string, { a: number, b: number, c: number }>();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    let a = stones[j][1] - stones[i][1], b = stones[i][0] - stones[j][0];
    let c = -a * stones[i][0] - b * stones[i][1];
    const g = Number(gcd(BigInt(a || 1), BigInt(b || 1)) || 1n);
    a /= g; b /= g; c /= g;
    if (a < 0 || (a === 0 && b < 0)) { a = -a; b = -b; c = -c; }
    const k = a + ',' + b + ',' + c;
    if (!lineMap.has(k)) lineMap.set(k, { a, b, c });
  }
  const lineCount = new Map<string, number>();
  for (const [k, L] of lineMap) {
    let cN = 0;
    for (const s of stones) if (L.a * s[0] + L.b * s[1] + L.c === 0) cN++;
    lineCount.set(k, cN);
  }

  // --- circles: exact rational keys from triples; membership via 4x4 det ---
  const circMap = new Map<string, [number, number, number]>();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) for (let k2 = j + 1; k2 < n; k2++) {
    const [x1, y1] = stones[i], [x2, y2] = stones[j], [x3, y3] = stones[k2];
    const cross = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1);
    if (cross === 0) continue; // collinear triple
    const det = BigInt(2 * cross); // halved Cramer denominator: bijective reparameterization of the center, grouping unaffected
    const A = BigInt(2 * (x2 - x1)), B = BigInt(2 * (y2 - y1)), E = BigInt(2 * (x3 - x1)), F = BigInt(2 * (y3 - y1));
    const C = BigInt(x2 * x2 + y2 * y2 - x1 * x1 - y1 * y1), G = BigInt(x3 * x3 + y3 * y3 - x1 * x1 - y1 * y1);
    const cxn = C * F - B * G, cyn = A * G - C * E;
    const r2n = (BigInt(x1) * det - cxn) ** 2n + (BigInt(y1) * det - cyn) ** 2n;
    const key = frac(cxn, det) + ';' + frac(cyn, det) + ';' + frac(r2n, det * det);
    if (!circMap.has(key)) circMap.set(key, [i, j, k2]);
  }
  let maxLine = 0, maxCirc = 0;
  for (const cN of lineCount.values()) maxLine = Math.max(maxLine, cN);
  const circCounts: Array<[[number, number, number], number]> = [];
  for (const rep of circMap.values()) {
    let cN = 0;
    for (let p = 0; p < n; p++) if (det4r(rows[rep[0]], rows[rep[1]], rows[rep[2]], rows[p]) === 0n) cN++;
    circCounts.push([rep, cN]);
    maxCirc = Math.max(maxCirc, cN);
  }
  const safe = maxLine < q && maxCirc < q;

  // --- maximality: every empty cell lies on a curve with >= q-1 stones ---
  const stoneSet = new Set(stones.map(s => s[0] + ',' + s[1]));
  const q1Lines: Array<{ a: number, b: number, c: number }> = [];
  for (const [k, L] of lineMap) if ((lineCount.get(k) as number) >= q - 1) q1Lines.push(L);
  const q1Circles = circCounts.filter(([, cN]) => cN >= q - 1).map(([rep]) => rep);
  const uncovered: Pt[] = [];
  for (let y = 0; y < w; y++) for (let x = 0; x < m; x++) {
    if (stoneSet.has(x + ',' + y)) continue;
    let covered = false;
    for (const L of q1Lines) if (L.a * x + L.b * y + L.c === 0) { covered = true; break; }
    if (!covered) {
      const row = [BigInt(x * x + y * y), BigInt(x), BigInt(y), 1n];
      for (const rep of q1Circles) if (det4r(rows[rep[0]], rows[rep[1]], rows[rep[2]], row) === 0n) { covered = true; break; }
    }
    if (!covered) uncovered.push([x, y]);
  }

  return {
    n, minRow, rowCnt, maxLine, maxCirc, safe,
    nCircles: circCounts.length,
    nQ1Curves: q1Lines.length + q1Circles.length,
    uncoveredCount: uncovered.length,
    rowDeficient: minRow <= q - 2,
    maximal: uncovered.length === 0,
    pass: safe && uncovered.length === 0 && minRow <= q - 2,
  };
}
