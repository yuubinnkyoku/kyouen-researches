// census.mjs — forbidden-quartet census of the n x n standard kyouen board.
// Exact integer arithmetic (all intermediate products bounded << 2^53 for n <= 16).
// Lines: primitive-direction maximal line enumeration, C(m,4) decomposition.
// Circles: every non-collinear triple -> unique circle equation x^2+y^2+Dx+Ey+F=0
// with rational (D,E,F) reduced to a canonical coprime integer key; grouped, then
// the group point set IS the board intersection of the circle (forbidden-ness is
// intrinsic to points, so every cocircular quartet lies on some >=4-point circle
// and is generated exactly once from it).
// Anchors (published, K0057): F_1..F_16, D/C splits for n=9..13, line/circle
// catalog sizes for n=10..12.
// Changelog: gcd(0,0)=0 fix (non-canonical keys when D=E=0), primitive-only
// horizontal directions (a==1 for b==0), F-array indexing fix.

export function gcd(a, b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { [a, b] = [b, a % b]; } return a; }

export function C4(m) { // C(m,4)
  if (m < 4) return 0;
  return m * (m - 1) * (m - 2) * (m - 3) / 24;
}

export function census(n) {
  const N = n * n;
  // ---- lines ----
  const lineList = [];
  let D = 0;
  const seenDirs = new Set();
  for (let a = -(n - 1); a <= n - 1; a++) {
    for (let b = 0; b <= n - 1; b++) {
      const canon = b === 0 ? (a === 1 ? `${a},0` : null) : (gcd(a, b) === 1 ? `${a},${b}` : null);
      if (canon === null || seenDirs.has(canon)) continue;
      seenDirs.add(canon);
      const groups = new Map(); // key a*y-b*x -> list
      for (let x = 0; x < n; x++) for (let y = 0; y < n; y++) {
        const k = a * y - b * x;
        let g = groups.get(k);
        if (!g) { g = []; groups.set(k, g); }
        g.push(x + n * y);
      }
      for (const g of groups.values()) {
        if (g.length >= 4) { lineList.push({ dir: [a, b], pts: g }); D += C4(g.length); }
      }
    }
  }
  // ---- circles via triples ----
  const circleMap = new Map(); // key -> {n: Set, triples: count}
  let tripleCount = 0;
  for (let p1 = 0; p1 < N; p1++) {
    const x1 = p1 % n, y1 = (p1 / n) | 0, s1 = x1 * x1 + y1 * y1;
    for (let p2 = p1 + 1; p2 < N; p2++) {
      const x2 = p2 % n, y2 = (p2 / n) | 0, s2 = x2 * x2 + y2 * y2;
      for (let p3 = p2 + 1; p3 < N; p3++) {
        const x3 = p3 % n, y3 = (p3 / n) | 0, s3 = x3 * x3 + y3 * y3;
        const det = x1 * (y2 - y3) - y1 * (x2 - x3) + (x2 * y3 - x3 * y2);
        if (det === 0) continue; // collinear triple: lines already counted
        tripleCount++;
        const Dn = -(s1 * (y2 - y3) - y1 * (s2 - s3) + (s2 * y3 - s3 * y2));
        const En = -(x1 * (s2 - s3) - s1 * (x2 - x3) + (x2 * s3 - x3 * s2));
        const Fn = -(x1 * (y2 * s3 - y3 * s2) - y1 * (x2 * s3 - x3 * s2) + s1 * (x2 * y3 - x3 * y2));
        const g = gcd(gcd(gcd(Math.abs(Dn), Math.abs(En)), Math.abs(Fn)), Math.abs(det));
        let Dn2 = Dn / g, En2 = En / g, Fn2 = Fn / g, det2 = det / g;
        if (det2 < 0) { Dn2 = -Dn2; En2 = -En2; Fn2 = -Fn2; det2 = -det2; }
        const key = `${Dn2}/${det2}|${En2}/${det2}|${Fn2}/${det2}`;
        let e = circleMap.get(key);
        if (!e) { e = { pts: new Set(), triples: 0 }; circleMap.set(key, e); }
        e.pts.add(p1); e.pts.add(p2); e.pts.add(p3);
        e.triples++;
      }
    }
  }
  let circleConsistency = true;
  const circleList = [];
  let C = 0;
  for (const e of circleMap.values()) {
    const m = e.pts.size;
    if (m * (m - 1) * (m - 2) / 6 !== e.triples) circleConsistency = false;
    if (m < 4) continue;
    circleList.push({ pts: [...e.pts].sort((a, b) => a - b) });
    C += C4(m);
  }
  return {
    n, N,
    D, C, F: D + C,
    lines: lineList, circles: circleList,
    tripleCount, circleConsistency,
    lineHist: hist(lineList.map(l => l.pts.length)),
    circleHist: hist(circleList.map(c => c.pts.length)),
  };
}

function hist(arr) {
  const h = {};
  for (const v of arr) h[v] = (h[v] || 0) + 1;
  return h;
}

// Quartet expansion: every forbidden quartet (4-subset of cells on a common line or circle).
export function quartetList(cen) {
  const out = [];
  const push = (pts) => {
    const m = pts.length;
    for (let a = 0; a < m; a++) for (let b = a + 1; b < m; b++) for (let c = b + 1; c < m; c++) for (let d = c + 1; d < m; d++) {
      out.push(pts[a], pts[b], pts[c], pts[d]);
    }
  };
  for (const l of cen.lines) push(l.pts);
  for (const c of cen.circles) push(c.pts);
  if (out.length / 4 !== cen.F) throw new Error(`quartet expansion mismatch: ${out.length / 4} vs F=${cen.F}`);
  return Uint16Array.from(out);
}

// Published anchors (K0057)
export const ANCHORS = {
  // F_n indexed by n (F_1..F_16); K0057: 0,1,14,194,826,2491,6364,14564,29152,54441,95670,158426,252362,383603,565948,816276
  F: [null, 0, 1, 14, 194, 826, 2491, 6364, 14564, 29152, 54441, 95670, 158426, 252362, 383603, 565948, 816276],
  D: { 9: 3156, 10: 5928, 11: 10428, 12: 17154, 13: 27340, 14: 41506, 15: 61176, 16: 87756 },
  C: { 9: 25996, 10: 48513, 11: 85242, 12: 141272, 13: 225022, 14: 342097, 15: 504772, 16: 728520 },
  lines: { 10: 154, 11: 232, 12: 326 },
  circles: { 10: 12170, 11: 20847, 12: 34031 },
};

export function verifyAgainstAnchors(cen) {
  const issues = [];
  if (ANCHORS.F[cen.n] !== undefined && cen.F !== ANCHORS.F[cen.n]) issues.push(`F_${cen.n}=${cen.F} published ${ANCHORS.F[cen.n]}`);
  if (ANCHORS.D[cen.n] !== undefined && cen.D !== ANCHORS.D[cen.n]) issues.push(`D_${cen.n}=${cen.D} published ${ANCHORS.D[cen.n]}`);
  if (ANCHORS.C[cen.n] !== undefined && cen.C !== ANCHORS.C[cen.n]) issues.push(`C_${cen.n}=${cen.C} published ${ANCHORS.C[cen.n]}`);
  if (ANCHORS.lines[cen.n] !== undefined && cen.lines.length !== ANCHORS.lines[cen.n]) issues.push(`lines_${cen.n}=${cen.lines.length} published ${ANCHORS.lines[cen.n]}`);
  if (ANCHORS.circles[cen.n] !== undefined && cen.circles.length !== ANCHORS.circles[cen.n]) issues.push(`circles_${cen.n}=${cen.circles.length} published ${ANCHORS.circles[cen.n]}`);
  if (!cen.circleConsistency) issues.push(`circle group triple-count consistency FAILED`);
  return issues;
}

// ---- CLI ----
if (process.argv[1] && process.argv[1].endsWith("census.mjs") && process.argv.length > 2) {
  const args = process.argv.slice(2);
  const ns = args.map(Number);
  const rows = [];
  for (const n of ns) {
    const t0 = Date.now();
    const cen = census(n);
    const issues = verifyAgainstAnchors(cen);
    rows.push({
      n, F: cen.F, D: cen.D, C: cen.C, lines: cen.lines.length, circles: cen.circles.length,
      triples: cen.tripleCount, circleConsistency: cen.circleConsistency,
      anchorIssues: issues, ms: Date.now() - t0,
      lineHist: cen.lineHist, circleHist: cen.circleHist,
    });
  }
  console.log(JSON.stringify(rows, null, 1));
}
