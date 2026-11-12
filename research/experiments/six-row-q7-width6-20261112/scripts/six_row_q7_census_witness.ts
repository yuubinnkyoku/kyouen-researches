// six_row_q7_census_witness.ts
// Width-6 seed of the fixed-width q=7 occupancy program (6 x m integer grid,
// forbidden: 7 co-circular or 7 co-linear stones).
//
// What this script does (all exact integer arithmetic):
//   1. Controls:
//      a. 5x19 danger-curve census must reproduce K0726: 95 circles
//         (8 of size 7, 87 of size 8), and K0745 witness W1 must have
//         worst census-circle stone count 5.
//      b. 6x13 chord census must equal a brute-force 3-point
//         circumcenter census (independent method), circle sets identical.
//   2. Census of circles with >= 7 lattice points in 6 x m for the m values
//      in CENSUS_M_LIST (chord/center method, complete because a circle
//      meets a row in <= 2 points, so any >=7-point circle has >= 2 rows
//      with exactly 2 points whose column sums are equal).
//   3. Full-capacity witness search (6 stones in each of the 6 rows,
//      36 stones): safety against the census circles, whole-configuration
//      column-mirror canonicalization, then INDEPENDENT verification via
//      stone-triple circumcircle enumeration (no census involved: a circle
//      with >= 7 stones would contain a stone triple; the max stone count
//      on any stone-triple circle must be <= 6). Rows have exactly 6
//      stones and any non-horizontal line meets the 6-row grid in <= 6
//      points, so maximality follows from row lines alone (proof).
//
// Execution note (2026-11-12): run in batches by editing CENSUS_M_LIST /
// WITNESS_M_LIST per run_typescript call (sandbox process-safety deadline
// allows ~2 census points per call; see log). Every number in
// ../output/six_row_q7_census_witness.json was produced by this exact code.

const CENSUS_M_LIST = [13, 16, 19, 22, 25, 28, 31, 34, 40, 46, 52, 58];
const WITNESS_M_LIST = [19, 25, 31, 40, 46, 52, 58];
const WITNESS_SAMPLES = 200;

function mulberry32(a: number) {
  return function () {
    a |= 0; a = a + 0x6d2b79f5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

// Chord/center census: circle through two same-row pairs with equal column
// sum s has centre (s/2, cy). u = y1 - cy, v = y2 - cy satisfy
// u^2 - v^2 = w2^2 - w1^2 (w_i = half chord width) and u - v = y1 - y2.
function censusChordB(H: number, m: number): { size: number, pts: number[] }[] {
  const gcd2 = (p: number, q: number) => { while (q) { const t = p % q; p = q; q = t; } return p; };
  const kept = new Map<string, { size: number, pts: number[] }>();
  const buckets: number[][][][] = [];
  for (let y = 0; y < H; y++) {
    const bs: number[][][] = Array.from({ length: 2 * m }, () => []);
    for (let a = 0; a < m - 1; a++) for (let b = a + 1; b < m; b++) bs[a + b].push([a, b]);
    buckets.push(bs);
  }
  for (let y1 = 0; y1 < H - 1; y1++) for (let y2 = y1 + 1; y2 < H; y2++) {
    const D = y1 - y2;
    for (let s = 1; s < 2 * m; s++) {
      for (const p1 of buckets[y1][s]) for (const p2 of buckets[y2][s]) {
        const W1 = p1[1] - p1[0], W2 = p2[1] - p2[0];
        const num = W2 * W2 - W1 * W1, den = 4 * D;
        const cyN = y1 * 2 * den - (num + D * den), cyD = 2 * den;
        const uN = y1 * cyD - cyN;
        const r2N = 4 * uN * uN + W1 * W1 * cyD * cyD;
        // canonical circumcenter form dd*x - (ux,uy), nr2 = r^2 * dd^2,
        // normalized by gcd and sign (identical keys to the brute method)
        let dd = 2 * cyD, ux = s * cyD, uy = 2 * cyN, nr2 = r2N;
        const g = (gcd2(gcd2(Math.abs(dd), Math.abs(ux)), Math.abs(uy)) || 1);
        dd /= g; ux /= g; uy /= g; nr2 /= g * g;
        if (dd < 0) { dd = -dd; ux = -ux; uy = -uy; }
        const key = dd + ',' + ux + ',' + uy + ',' + nr2;
        if (kept.has(key)) continue;
        const list: number[] = [];
        for (let y = 0; y < H; y++) {
          const dy = y * dd - uy;
          for (let x = 0; x < m; x++) {
            const dx = x * dd - ux;
            if (dx * dx + dy * dy === nr2) list.push(x, y);
          }
        }
        if (list.length / 2 >= 7) kept.set(key, { size: list.length / 2, pts: list });
      }
    }
  }
  return [...kept.values()];
}

// Brute-force control census: every 3-point circumcenter, gcd/sign
// normalized keys.
function censusBrute(H: number, m: number): { size: number, pts: number[] }[] {
  const pts: number[] = [];
  for (let y = 0; y < H; y++) for (let x = 0; x < m; x++) pts.push(x, y);
  const n = pts.length / 2;
  const gcd2 = (p: number, q: number) => { while (q) { const t = p % q; p = q; q = t; } return p; };
  const kept = new Map<string, { size: number, pts: number[] }>();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) for (let k = j + 1; k < n; k++) {
    const x1 = pts[2 * i], y1 = pts[2 * i + 1], x2 = pts[2 * j], y2 = pts[2 * j + 1], x3 = pts[2 * k], y3 = pts[2 * k + 1];
    const d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2));
    if (d === 0) continue;
    const s1 = x1 * x1 + y1 * y1, s2 = x2 * x2 + y2 * y2, s3 = x3 * x3 + y3 * y3;
    let ux = s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2);
    let uy = s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1);
    let dd = d;
    const g = (gcd2(gcd2(Math.abs(dd), Math.abs(ux)), Math.abs(uy)) || 1);
    dd /= g; ux /= g; uy /= g;
    if (dd < 0) { dd = -dd; ux = -ux; uy = -uy; }
    const ux0 = ux * g, uy0 = uy * g, d0 = dd * g;
    const vx0 = x1 * d0 - ux0, vy0 = y1 * d0 - uy0;
    const nr2 = (vx0 * vx0 + vy0 * vy0) / (g * g);
    const key = dd + ',' + ux + ',' + uy + ',' + nr2;
    if (kept.has(key)) continue;
    const list: number[] = [];
    for (let idx = 0; idx < n; idx++) {
      const dx = pts[2 * idx] * dd - ux, dy = pts[2 * idx + 1] * dd - uy;
      if (dx * dx + dy * dy === nr2) list.push(pts[2 * idx], pts[2 * idx + 1]);
    }
    if (list.length / 2 >= 7) kept.set(key, { size: list.length / 2, pts: list });
  }
  return [...kept.values()];
}

// Independent witness verification (no census): enumerate circles through
// stone triples; max stone count on any such circle must be <= 6.
function verifyIndependent(rows: number[][], H: number) {
  const stones: number[] = [];
  for (let y = 0; y < H; y++) for (const x of rows[y]) stones.push(x, y);
  const n = stones.length / 2;
  if (n !== 6 * H) return { ok: false, worst: -1 };
  for (const r of rows) if (r.length !== 6) return { ok: false, worst: -1 };
  let worst = 0;
  const seen = new Set<string>();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) for (let k = j + 1; k < n; k++) {
    const x1 = stones[2 * i], y1 = stones[2 * i + 1], x2 = stones[2 * j], y2 = stones[2 * j + 1], x3 = stones[2 * k], y3 = stones[2 * k + 1];
    const d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2));
    if (d === 0) continue; // collinear triples: rows hold 6 stones, other
    // lines meet the 6-row grid in <= 6 points, so no 7-point line exists.
    const s1 = x1 * x1 + y1 * y1, s2 = x2 * x2 + y2 * y2, s3 = x3 * x3 + y3 * y3;
    const ux = s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2);
    const uy = s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1);
    const key = ux + ',' + uy + ',' + d;
    if (seen.has(key)) continue;
    seen.add(key);
    let cnt = 0;
    for (let idx = 0; idx < n; idx++) {
      const dx = stones[2 * idx] * d - ux, dy = stones[2 * idx + 1] * d - uy;
      const vx = x1 * d - ux, vy = y1 * d - uy;
      if (dx * dx + dy * dy === vx * vx + vy * vy) cnt++;
    }
    if (cnt > worst) worst = cnt;
  }
  return { ok: worst <= 6, worst };
}

async function main() {
  const out: any = { controls: {}, census: {}, span: {}, witnesses: {} };

  // Control a: 5x19 census + K0745 W1
  const c5 = censusChordB(5, 19);
  const by5: Record<number, number> = {};
  for (const q of c5) by5[q.size] = (by5[q.size] || 0) + 1;
  const W1 = [[0, 2, 15, 16, 17, 18], [2, 8, 11, 12, 15, 16], [1, 4, 12, 16, 17, 18], [4, 5, 6, 7, 9, 12], [1, 2, 9, 10, 14, 18]];
  const occ5 = new Set<number>();
  for (let y = 0; y < 5; y++) for (const x of W1[y]) occ5.add(x * 8 + y);
  let w5 = 0;
  for (const q of c5) { let cnt = 0; for (let i = 0; i < q.pts.length; i += 2) if (occ5.has(q.pts[i] * 8 + q.pts[i + 1])) cnt++; if (cnt > w5) w5 = cnt; }
  out.controls.five_x19 = { total: c5.length, bySize: by5, W1worst: w5 };

  // Control b: 6x13 brute cross-check
  const a13 = censusChordB(6, 13), b13 = censusBrute(6, 13);
  const ka = new Set(a13.map(q => q.pts.join(',')));
  let missing = 0;
  for (const q of b13) if (!ka.has(q.pts.join(','))) missing++;
  out.controls.six_x13_crosscheck = { chord: a13.length, brute: b13.length, chordMissing: missing };

  // Census table + span distributions
  for (const m of CENSUS_M_LIST) {
    const c = censusChordB(6, m);
    const by: Record<number, number> = {};
    let maxS = 0;
    for (const q of c) { by[q.size] = (by[q.size] || 0) + 1; if (q.size > maxS) maxS = q.size; }
    out.census[m] = { total: c.length, bySize: by, max: maxS };
    if (m === 19 || m === 31) {
      const d: Record<number, number> = {};
      for (const q of c) {
        let lo = 99, hi = -1;
        for (let i = 0; i < q.pts.length; i += 2) { lo = Math.min(lo, q.pts[i + 1]); hi = Math.max(hi, q.pts[i + 1]); }
        d[hi - lo + 1] = (d[hi - lo + 1] || 0) + 1;
      }
      out.span[m] = d;
    }
  }

  // Witness search + canonicalization + independent verification
  for (const m of WITNESS_M_LIST) {
    const circles = censusChordB(6, m);
    const cpts = circles.map(q => q.pts);
    const rnd = mulberry32(20261112 + m * 7 + 1);
    let found: number[][] | null = null;
    let safe = 0;
    for (let t = 0; t < WITNESS_SAMPLES; t++) {
      const occ = new Array(6).fill(0).map(() => new Uint8Array(m));
      for (let y = 0; y < 6; y++) {
        const cols = new Set<number>();
        while (cols.size < 6) cols.add(Math.floor(rnd() * m));
        for (const c of cols) occ[y][c] = 1;
      }
      let bad = false;
      for (const P of cpts) {
        let cnt = 0;
        for (let i = 0; i < P.length; i += 2) { if (occ[P[i + 1]][P[i]]) cnt++; if (cnt >= 7) { bad = true; break; } }
        if (bad) break;
      }
      if (!bad) {
        safe++;
        if (!found) found = occ.map(r => { const l: number[] = []; for (let x = 0; x < m; x++) if (r[x]) l.push(x); return l; });
      }
    }
    if (found) {
      const A = found.map(r => [...r].sort((x, y2) => x - y2));
      const mir = A.map(r => r.map(x => m - 1 - x).sort((x, y2) => x - y2));
      const canon = JSON.stringify(A) <= JSON.stringify(mir) ? A : mir;
      out.witnesses[m] = {
        rows: canon, safeRate: safe + '/' + WITNESS_SAMPLES,
        verify: verifyIndependent(canon, 6),
      };
    } else {
      out.witnesses[m] = { rows: null, safeRate: safe + '/' + WITNESS_SAMPLES };
    }
  }
  return out;
}
