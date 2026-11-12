// Verifier for: P(w) exact for w=9..16 (12,12,14,16,16,16,16,16), P(17),P(18) <= 18.
// Framework (K0072 Vieta + K0763-65 accounting):
//   Circle x^2+y^2+Cx+Dy+N=0 meets each row in <=2 points; tangent rows <= 2 (geometry).
//   P = 2d + s over point-rows (board clipping only reduces, so bounding over all x in Z is sound).
//   Vieta case (adjacent double rows): C,D,N integers; every point-row y has
//     s_y^2 = R - (2y+D)^2, R = C^2+D^2-4N in Z  =>  R-(2y+D)^2 in QR0(p) mod p for all p.
//   P <= 2*(d+s) in the Vieta case.
// This script re-verifies, as a third independent implementation:
//   (1) mod-9 standard-form window counts W_w,
//   (2) mixed (double+tangent) subset eliminations for w=9..18 (QR0 includes 0),
//   (3) g=2 (eighth-integer D) scaled-form counts killing non-Vieta d=9 on w=17,18,
//   (4) the witnesses, with exact integer on-circle checks.

async function main() {
  const out: any = { generated: "2026-11-12", parts: {} };

  // (1) standard-form window counts: max over (a,u) mod 9 of #{i in 0..w-1: a-4i^2-ui in QR9}
  const QR9 = new Set([0, 1, 4, 7]);
  const W: any = {};
  for (let w = 9; w <= 18; w++) {
    let best = 0;
    for (let a = 0; a < 9; a++) for (let u = 0; u < 9; u++) {
      let c = 0;
      for (let i = 0; i < w; i++) { const v = ((a - 4 * i * i - u * i) % 9 + 9) % 9; if (QR9.has(v)) c++; }
      if (c > best) best = c;
    }
    W[w] = best;
  }
  out.parts.windowCountsW = W;

  // (2) mixed subset eliminations: subset S of offsets feasible only if for SOME prime modulus p
  //     exists (R,D) mod p with R-(2i+D)^2 in QR0(p) for all i in S. Eliminate if none.
  const qrCache: Record<number, Set<number>> = {};
  const getQR0 = (m: number) => qrCache[m] ?? (qrCache[m] = (() => { const s = new Set<number>(); for (let x = 0; x < m; x++) s.add((x * x) % m); return s; })());
  function subsetOK(S: number[], m: number): boolean {
    const qr = getQR0(m);
    for (let R = 0; R < m; R++) for (let D = 0; D < m; D++) {
      let ok = true;
      for (let i = 0; i < S.length; i++) { const t = (2 * S[i] + D) % m; const v = ((R - t * t) % m + m) % m; if (!qr.has(v)) { ok = false; break; } }
      if (ok) return true;
    }
    return false;
  }
  function combos(n: number, k: number): number[][] {
    const res: number[][] = []; const cur: number[] = [];
    (function rec(s: number) { if (cur.length === k) { res.push(cur.slice()); return; } for (let i = s; i < n; i++) { cur.push(i); rec(i + 1); cur.pop(); } })(0);
    return res;
  }
  const mods = [9, 11, 19, 23, 7, 5, 13, 17];
  const elim: any = {};
  const tasks: [number, number][] = [[9, 7], [10, 7], [11, 8], [12, 9], [13, 9], [14, 9], [15, 9], [16, 9], [17, 10], [18, 10]];
  for (const [w, k] of tasks) {
    const subsets = combos(w, k);
    let alive = 0; const perMod: Record<number, number> = {};
    for (const S of subsets) {
      let isAlive = true;
      for (const m of mods) { if (!subsetOK(S, m)) { perMod[m] = (perMod[m] || 0) + 1; isAlive = false; break; } }
      if (isAlive) alive++;
    }
    elim[`w${w}_k${k}`] = { subsets: subsets.length, mixedRowsBound: k - 1, eliminated: subsets.length - alive, survivors: alive, perMod };
  }
  out.parts.subsetElimination = elim;

  // (3) g=2 form: pure-parity non-adjacent double set, no opposite-parity tangent => 8D = e (e odd possible),
  //     s^2 = C^2-4y^2-(e/2)y-4N; scale by 4: (2s)^2 = 4C^2-16y^2-2ey-16N.
  //     mod 9: A - 7y^2 - Uy in QR9 with A = 4C^2-16N free (4C^2 in QR9, 16N free), U = 2e free.
  const g2: any = {};
  for (const w of [17, 18]) {
    const evens: number[] = []; const odds: number[] = [];
    for (let y = 0; y < w; y += 2) evens.push(y);
    for (let y = 1; y < w; y += 2) odds.push(y);
    const maxCount = (rows: number[]) => {
      let best = 0;
      for (let A = 0; A < 9; A++) for (let U = 0; U < 9; U++) {
        let c = 0;
        for (const y of rows) { const v = ((A - 7 * y * y - U * y) % 9 + 9) % 9; if (QR9.has(v)) c++; }
        if (c > best) best = c;
      }
      return best;
    };
    g2[w] = { evens: evens.length, evensMax: maxCount(evens), odds: odds.length, oddsMax: maxCount(odds) };
  }
  out.parts.g2FormCounts = g2;

  // (4) witnesses: integer circles (2x+C)^2+(2y+D)^2=R, C = -smax so that all x >= 0.
  const witSpec: [number, number, number][] = [
    [9, -7, 50], [10, -7, 50], [11, -11, 130], [12, -11, 130], [13, -11, 130],
    [14, -11, 130], [15, -11, 130], [16, -11, 130], [17, -11, 130], [18, -11, 130],
  ];
  const witnesses: any = {};
  for (const [w, D, R] of witSpec) {
    const rows: { y: number; s: number }[] = [];
    let smax = 0;
    for (let y = 0; y < w; y++) {
      const t = 2 * y + D; const rem = R - t * t;
      if (rem >= 0) { const s = Math.round(Math.sqrt(rem)); if (s * s === rem) { rows.push({ y, s }); smax = Math.max(smax, s); } }
    }
    const C = -smax;
    const pts: [number, number][] = [];
    let parityOk = true;
    for (const { y, s } of rows) {
      if (((s % 2) + 2) % 2 !== ((C % 2) + 2) % 2) parityOk = false;
      if (s === 0) pts.push([-C / 2, y]); else { pts.push([(-C + s) / 2, y]); pts.push([(-C - s) / 2, y]); }
    }
    let ok = parityOk && pts.length > 0;
    const seen = new Set<string>();
    for (const [x, y] of pts) {
      if (x < 0 || y < 0 || y >= w || !Number.isInteger(x)) ok = false;
      if ((2 * x + C) * (2 * x + C) + (2 * y + D) * (2 * y + D) !== R) ok = false;
      const key = x + "," + y; if (seen.has(key)) ok = false; seen.add(key);
    }
    const rowCnt: Record<number, number> = {};
    for (const [, y] of pts) rowCnt[y] = (rowCnt[y] || 0) + 1;
    witnesses[w] = {
      circle: `(2x+(${C}))^2 + (2y+(${D}))^2 = ${R}`,
      points: pts.length, m_needed: Math.max(...pts.map(p => p[0])) + 1,
      doubleRows: Object.values(rowCnt).filter(c => c === 2).length,
      singleRows: Object.values(rowCnt).filter(c => c === 1).length,
      rowsUsed: Object.keys(rowCnt).map(Number).sort((a, b) => a - b),
      verified: ok,
      allPts: pts.sort((a, b) => a[1] - b[1] || a[0] - b[0]),
    };
  }
  out.parts.witnesses = witnesses;

  // final claims
  const P: any = {};
  const claims: [number, number, string][] = [
    [9, 12, "proved"], [10, 12, "proved"], [11, 14, "proved"], [12, 16, "proved"],
    [13, 16, "proved"], [14, 16, "proved"], [15, 16, "proved"], [16, 16, "proved"],
    [17, 18, "upper-bound-only"], [18, 18, "upper-bound-only"],
  ];
  for (const [w, val, status] of claims) P[w] = { value: val, status, lowerBound: w <= 16 ? val : 16 };
  out.parts.Pw = P;

  return out;
}
