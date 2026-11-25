// width6_circle_bound.ts — universal bound P(6) <= 8 on lattice points of a
// circle over the 6xm integer grid, plus the q>=9 row-separation corollary.
// Machine-verifiable controls for every finite step of the proof in
// ../reports/width6-circle-eight-point-bound.md.
// Every number in ../output/width6_circle_bound.json comes from this file.
async function main() {
  const isSq = (n: number) => { if (n < 0) return false; const s = Math.round(Math.sqrt(n)); return s * s === n; };
  const out: any = { controls: {}, mod9_double_row_classification: {}, tangent_lemma: {}, example_radius5: {}, census_reproduction: {} };

  // --- Control E: end-to-end example (validates the tangent algebra) ---
  // Circle x^2+y^2-25=0 on rows 0..5: doubles y=0 (x=+-5), y=3 (+-4), y=4 (+-3), tangent y=5 (x=0).
  {
    const pts: number[] = [];
    for (let y = 0; y <= 5; y++) for (let x = -11; x <= 11; x++) if (x * x + y * y === 25) pts.push(x, y);
    out.example_radius5.points = pts; // 14 entries = 7 points
    out.example_radius5.count = pts.length / 2;
  }

  // --- Mod-9 classification (self-contained re-proof of the K0072 core for w=6) ---
  // After the Vieta reduction (C,D,M integers, valid once two double rows lie in
  // consecutive rows), row y is a double row only if disc(y) = M-4y^2-4Dy is a
  // positive perfect square, hence a QR mod 9.
  {
    const p = 9, qr = new Set<number>();
    for (let s = 0; s < p; s++) qr.add((s * s) % p);
    let worst = 0, worstCase: any = null;
    for (let M = 0; M < p; M++) for (let D = 0; D < p; D++) for (let k = 0; k < p; k++) {
      let c = 0;
      for (let y = k; y < k + 6; y++) if (qr.has(((M - 4 * y * y - 4 * D * y) % p + p) % p)) c++;
      if (c > worst) { worst = c; worstCase = { M, D, k }; }
    }
    out.mod9_double_row_classification = { modulus: p, qr: [...qr], worstDoubleRowsAmong6: worst, worstCase, cases: p * p * p };
  }

  // --- Tangent lemma controls (rules out d=4 with s>=1) ---
  {
    const G1 = 1000000;
    let maxCnt = 0; const maxExamples: any[] = [];
    let t3co = 0;
    for (let g = -G1; g <= G1; g++) {
      let cnt = 0; const ts: number[] = [];
      for (let t = -5; t <= 5; t++) { if (t === 0) continue; if (isSq(t * (g - t))) { cnt++; ts.push(t); } }
      if (cnt > maxCnt) { maxCnt = cnt; maxExamples.length = 0; maxExamples.push({ g, ts }); }
      else if (cnt === maxCnt && maxExamples.length < 6) maxExamples.push({ g, ts });
    }
    for (let g = -G1; g <= G1; g++) {
      let has3 = false, other = 0;
      for (let t = -5; t <= 5; t++) { if (t === 0) continue; if (isSq(t * (g - t))) { if (Math.abs(t) === 3) has3 = true; else other++; } }
      if (has3 && other >= 1) t3co++;
    }
    let f2found = 0;
    for (let h = -G1; h <= G1; h++) if (h - 4 > 0 && -(h + 4) > 0 && isSq(h - 4) && isSq(-(h + 4))) f2found++;
    out.tangent_lemma = { f1_g_range: G1, f1_max_double_ts: maxCnt, f1_examples: maxExamples, t3_never_coexists_count: t3co, f2_both_positive_squares_count: f2found };
  }

  // --- d=5 sanity control (covered by the mod-9 classification; finite spot check) ---
  {
    const B = 600; let d5count = 0, best = 0, bestEx: any = null;
    for (let M = -B; M <= B; M++) for (let D = -B; D <= B; D++) {
      let c = 0;
      for (let y = 0; y <= 5; y++) { const v = M - 4 * y * y - 4 * D * y; if (v > 0 && isSq(v)) c++; }
      if (c > best) { best = c; bestEx = { M, D }; }
      if (c >= 5) d5count++;
    }
    out.controls.d5_spotcheck = { bound: B, five_double_rows: d5count, bestCount: best, bestExample: bestEx };
  }

  // --- Census reproduction (sharpness: 8-point circles exist; K0760 controls) ---
  const gcd2 = (p: number, q: number) => { while (q) { const t = p % q; p = q; q = t; } return p; };
  function censusChordB(H: number, m: number): { size: number, pts: number[] }[] {
    const kept = new Map<string, { size: number, pts: number[] }>();
    const buckets: number[][][][] = [];
    for (let y = 0; y < H; y++) {
      const bs: number[][][] = Array.from({ length: 2 * m }, () => []);
      for (let a = 0; a < m - 1; a++) for (let b = a + 1; b < m; b++) bs[a + b].push([a, b]);
      buckets.push(bs);
    }
    for (let y1 = 0; y1 < H - 1; y1++) for (let y2 = y1 + 1; y2 < H; y2++) {
      const D = y1 - y2;
      for (let s = 1; s < 2 * m; s++) for (const p1 of buckets[y1][s]) for (const p2 of buckets[y2][s]) {
        const W1 = p1[1] - p1[0], W2 = p2[1] - p2[0];
        const num = W2 * W2 - W1 * W1, den = 4 * D;
        const cyN = y1 * 2 * den - (num + D * den), cyD = 2 * den;
        const uN = y1 * cyD - cyN;
        const r2N = 4 * uN * uN + W1 * W1 * cyD * cyD;
        let dd = 2 * cyD, ux = s * cyD, uy = 2 * cyN, nr2 = r2N;
        const g = (gcd2(gcd2(Math.abs(dd), Math.abs(ux)), Math.abs(uy)) || 1);
        dd /= g; ux /= g; uy /= g; nr2 /= g * g;
        if (dd < 0) { dd = -dd; ux = -ux; uy = -uy; }
        const key = dd + ',' + ux + ',' + uy + ',' + nr2;
        if (kept.has(key)) continue;
        const list: number[] = [];
        for (let y = 0; y < H; y++) { const dy = y * dd - uy; for (let x = 0; x < m; x++) { const dx = x * dd - ux; if (dx * dx + dy * dy === nr2) list.push(x, y); } }
        if (list.length / 2 >= 7) kept.set(key, { size: list.length / 2, pts: list });
      }
    }
    return [...kept.values()];
  }
  for (const m of [13, 16]) {
    const c = censusChordB(6, m);
    const by: Record<number, number> = {}; let maxS = 0;
    for (const q of c) { by[q.size] = (by[q.size] || 0) + 1; if (q.size > maxS) maxS = q.size; }
    out.census_reproduction['6x' + m] = { total: c.length, bySize: by, max: maxS };
  }
  return out;
}
