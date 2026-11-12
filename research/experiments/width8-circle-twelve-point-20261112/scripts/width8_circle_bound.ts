// width8_circle_bound.ts — universal structure of circle lattice points over the
// 8xm integer grid: P(8) = 12, possible sizes {7, 8, 10, 12}, and every size >= 9
// is even (no odd circle size >= 9 exists for any m). Proof in
// ../reports/width8-circle-twelve-point.md.
// Run in batches by editing CENSUS_M_LIST per call; every number in
// ../output/width8_circle_bound.json comes from this file.
const CENSUS_M_LIST = [11];

async function main() {
  const isSq = (n: number) => { if (n < 0) return false; const s = Math.round(Math.sqrt(n)); return s * s === n; };
  const out: any = {};

  // Witness: (2x-7)^2+(2y-7)^2=50 has 12 lattice points on rows 0..7 (6 double rows 0,1,3,4,6,7).
  {
    const pts: number[] = [];
    for (let y = 0; y <= 7; y++) for (let x = 0; x <= 7; x++) {
      const dx = 2 * x - 7, dy = 2 * y - 7;
      if (dx * dx + dy * dy === 50) pts.push(x, y);
    }
    const rows: number[][] = Array.from({ length: 8 }, () => []);
    for (let i = 0; i < pts.length; i += 2) rows[pts[i + 1]].push(pts[i]);
    out.witness = { equation: '(2x-7)^2+(2y-7)^2=50', count: pts.length / 2, rows, fitsM: 8 };
  }

  // Mod-9 classification for 8 consecutive rows (double-row upper bound d <= 6).
  {
    const p = 9, qr = new Set<number>();
    for (let s = 0; s < p; s++) qr.add((s * s) % p);
    let worst = 0, worstCase: any = null;
    for (let M = 0; M < p; M++) for (let D = 0; D < p; D++) for (let k = 0; k < p; k++) {
      let c = 0;
      for (let y = k; y < k + 8; y++) if (qr.has(((M - 4 * y * y - 4 * D * y) % p + p) % p)) c++;
      if (c > worst) { worst = c; worstCase = { M, D, k }; }
    }
    out.mod9_8rows = { worstDoubleRowsAmong8: worst, worstCase, cases: p * p * p };
  }

  // Prime-offset lemma control: t=7 never coexists with any other double offset.
  {
    const G = 1000000;
    let maxCnt = 0; const ex: any[] = []; let t7co = 0;
    for (let g = -G; g <= G; g++) {
      let cnt = 0; const ts: number[] = [];
      for (let t = -7; t <= 7; t++) { if (t === 0) continue; const v = t * (g - t); if (v > 0 && isSq(v)) { cnt++; ts.push(t); } }
      if (cnt > maxCnt) { maxCnt = cnt; ex.length = 0; ex.push({ g, ts }); }
      else if (cnt === maxCnt && ex.length < 6) ex.push({ g, ts });
    }
    for (let g = -G; g <= G; g++) {
      let h7 = false, o = 0;
      for (let t = -7; t <= 7; t++) { if (t === 0) continue; const v = t * (g - t); if (v > 0 && isSq(v)) { if (Math.abs(t) === 7) h7 = true; else o++; } }
      if (h7 && o >= 1) t7co++;
    }
    out.tangent_f1 = { range: G, maxDoubleTs: maxCnt, examples: ex, t7_coexists: t7co };
  }

  // f=2 control (t in {+-2,+-4,+-6}, t*(h-2t)/2 positive square).
  {
    const G = 1000000;
    let maxCnt = 0;
    for (let h = -G; h <= G; h++) {
      let cnt = 0;
      for (const t of [2, -2, 4, -4, 6, -6]) { const v = t * (h - 2 * t) / 2; if (v > 0 && isSq(v)) cnt++; }
      if (cnt > maxCnt) maxCnt = cnt;
    }
    out.tangent_f2 = { range: G, maxDoubleTs: maxCnt };
  }

  // Two-tangent control for w=8: tangents at t=0 and t=g, |g| <= 7; doubles strictly between.
  {
    const res: any = {};
    for (const g of [6, 7, -6, -7]) {
      let cnt = 0; const ts: number[] = [];
      for (let t = 1; t < Math.abs(g); t++) { const tt = g > 0 ? t : -t; const v = tt * (g - tt); if (v > 0 && isSq(v)) { cnt++; ts.push(tt); } }
      res['g=' + g] = { count: cnt, ts };
    }
    out.two_tangent = res;
  }

  // Census.
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
  out.census = {};
  for (const m of CENSUS_M_LIST) {
    const c = censusChordB(8, m);
    const by: Record<number, number> = {}; let maxS = 0;
    for (const q of c) { by[q.size] = (by[q.size] || 0) + 1; if (q.size > maxS) maxS = q.size; }
    out.census['8x' + m] = { total: c.length, bySize: by, max: maxS };
  }
  return out;
}
