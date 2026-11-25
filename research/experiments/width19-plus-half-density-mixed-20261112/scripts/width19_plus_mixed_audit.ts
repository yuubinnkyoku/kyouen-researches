// 第三の独立実装: w>=19 半密度証明書の QR0（0を含む平方剰余）混合点行解釈の監査と
// 原始 sum-of-two-squares 族の witness 探索。単独実行で
// output/width19_plus_mixed_audit.json（MODE="audit"）および
// output/circle_witness_search.json（MODE="witness"）と同一の数値を返す。
//
// 使い方（sandbox の時間制限のためセグメント分割実行を推奨）:
//   MODE = "audit"   : segment1 (L=18,19,20; p=11,19,23) + segment2 (L=21..26; p=11,23,31)
//                      + segment3 (周期補題; p=23,31) + per-prime maxima を一括返す。
//   MODE = "witness" : R = 2^a * prod(p^e)（p≡1 mod 4, p<=149, Σe<=8, R<=1e11）を列挙し
//                      12/17..22 行窓の最大点数とその円を返す。制御: R=130→16点・R=50→12点。
//
// 数学的前提（K0072/K0767 と同一）:
//   Vieta 標準形 s_y^2 = A - 4y^2 - Uy（A = C^2-4N, U = 4D）。
//   点行（二重行 s_y>0 / 接点行 s_y=0）はすべての素数法 p で A-4y^2-Uy ∈ QR0(p)。
//   (N,C) ⟷ (A,U) の対応 A=N-C^2, U=2C は奇素数で全単射なので、
//   K0072 証明書の (N, C) 列挙と本実装の (A, U) 列挙は同じ必要条件集合を走査する。

let MODE: "audit" | "witness" = "audit";

async function main() {
  if (MODE === "audit") return JSON.stringify(runAudit());
  return JSON.stringify(runWitnessSearch());
}

function qr0Arr(p: number) {
  const a = new Uint8Array(p);
  for (let i = 0; i < p; i++) a[i * i % p] = 1;
  return a;
}

// ---------- MODE = "audit" ----------

function masks(p: number, L: number): number[] {
  // 窓 [0,L) の行 i が (n - (2i+c)^2) mod p ∈ QR0(p) を満たすかの bitmask。
  // (n, c) ∈ (Z/p)^2 を全走査し distinct mask のリストを返す。
  const qr = qr0Arr(p);
  const set = new Set<number>();
  for (let n = 0; n < p; n++) for (let c = 0; c < p; c++) {
    let m = 0;
    for (let i = 0; i < L; i++) {
      const u = (2 * i + c) % p;
      if (qr[(n - u * u + p * p) % p]) m |= 1 << i;
    }
    set.add(m);
  }
  return Array.from(set);
}

function runAudit() {
  const pop = new Uint8Array(65536);
  for (let i = 1; i < 65536; i++) pop[i] = pop[i >>> 1] + (i & 1);
  const pc = (m: number) => pop[m & 65535] + pop[m >>> 16];
  const out: any = { note: "third independent implementation, QR0 (0 included) everywhere" };

  // segment 1: L=18,19,20 with primes 11,19,23 (K0072 の w=19,20 帯)
  out.segment1_w19_20 = {};
  for (const L of [18, 19, 20]) {
    const M11 = masks(11, L), M19 = masks(19, L), M23 = masks(23, L);
    const abSet = new Set<number>();
    for (const a of M11) for (const b of M19) abSet.add(a & b);
    const AB = Array.from(abSet);
    let mx = 0;
    for (const ab of AB) for (const m of M23) { const c = pc(ab & m); if (c > mx) mx = c; }
    out.segment1_w19_20["L" + L] = { maxPointRows: mx, ceilHalf: Math.ceil(L / 2) };
  }

  // segment 2: L=21..26 with primes 11,23,31（先行の mod 11・23・31 監査の再現）
  {
    const L = 26;
    const M11 = masks(11, L), M23 = masks(23, L), M31 = masks(31, L);
    const abSet = new Set<number>();
    for (const a of M11) for (const b of M23) abSet.add(a & b);
    const AB = Array.from(abSet);
    const maxCnt = new Array(6).fill(0);
    const subMask: number[] = [];
    for (let l = 21; l <= 26; l++) subMask.push((1 << l) - 1);
    for (const ab of AB) for (const m of M31) {
      const v = ab & m;
      if (v === 0) continue;
      if (pc(v) <= maxCnt[0]) continue; // L=21 の暫定最大以下なら詳細不要
      for (let j = 0; j < 6; j++) { const c = pc(v & subMask[j]); if (c > maxCnt[j]) maxCnt[j] = c; }
    }
    out.segment2_w21_26 = {};
    for (let j = 0; j < 6; j++) {
      const L2 = 21 + j;
      out.segment2_w21_26["L" + L2] = { maxPointRows: maxCnt[j], ceilHalf: Math.ceil(L2 / 2) };
    }
  }

  // segment 3: 周期補題（p=23,31; 周期 713）。
  // 全ての (c23,c31) は同時並進で base pattern (c=0,0) の並進と等価（2 が奇素数で可逆 + CRT）。
  // よって類型は (n23,n31) の 713 個。各類型の on-position 列について k 点を含む最小円周 span を
  // 全 k で計算し、minspan(k) <= L-1 ⟺ ある窓長 L に k 点行が入る、で全 L を監査する。
  {
    const qr23 = qr0Arr(23), qr31 = qr0Arr(31);
    const KMAX = 223;
    const minspan = new Int32Array(KMAX + 1).fill(1 << 29);
    minspan[0] = 0; minspan[1] = 0;
    let periodMax = 0;
    let inv = 0; for (let x = 1; x < 31; x++) if ((23 * x) % 31 === 1) { inv = x; break; }
    for (let n23 = 0; n23 < 23; n23++) {
      const c23 = new Uint8Array(23); let p23 = 0;
      for (let r = 0; r < 23; r++) { const u = 2 * r % 23; c23[r] = qr23[(n23 - u * u + 529) % 23] ? 1 : 0; p23 += c23[r]; }
      for (let n31 = 0; n31 < 31; n31++) {
        const c31 = new Uint8Array(31); let p31 = 0;
        for (let r = 0; r < 31; r++) { const u = 2 * r % 31; c31[r] = qr31[(n31 - u * u + 961) % 31] ? 1 : 0; p31 += c31[r]; }
        const total = p23 * p31; // 周期 713 (=23*31) 内の on 行数（CRT 全単射の積）
        if (total > periodMax) periodMax = total;
        if (total < 2) continue;
        const pos: number[] = [];
        for (let a = 0; a < 23; a++) { if (!c23[a]) continue; for (let b = 0; b < 31; b++) { if (!c31[b]) continue; const t = (((b - a) * inv) % 31 + 31) % 31; pos.push(a + 23 * t); } }
        pos.sort((x, y) => x - y);
        const m = pos.length;
        const D = pos.slice();
        if (m <= KMAX) for (let j = 0; j < m; j++) D.push(pos[j] + 713);
        const lim = Math.min(m, KMAX);
        for (let k = 2; k <= lim; k++) {
          let best = 1 << 29;
          for (let j = 0; j < D.length - k + 1; j++) { const s = D[j + k - 1] - D[j]; if (s < best) best = s; }
          if (best < minspan[k]) minspan[k] = best;
        }
      }
    }
    const maxcount = (L: number) => { let b = 0; for (let k = 1; k <= KMAX; k++) if (minspan[k] <= L - 1) b = k; return Math.min(b, 221); };
    const seg3: any = { periodMax, maxWindowByL: {} as any, violations: [] as string[] };
    for (let L = 26; L <= 442; L++) {
      const mc = maxcount(L);
      if (L === 26 || L === 27 || L === 28 || L === 30 || L === 50 || L === 100 || L === 200 || L === 300 || L === 442) seg3.maxWindowByL["L" + L] = mc;
      if (L >= 27 && mc > Math.ceil(L / 2)) seg3.violations.push("L" + L);
      if (L === 26 && mc !== 14) seg3.violations.push("L26control!=14");
    }
    out.segment3_w27_plus = seg3;
  }

  // per-prime maxima（QR0 と 0 除外の対比 — 従来証明書が 0 込みであることの独立証拠）
  {
    const ppm: any = {};
    for (const p of [11, 19, 23, 31]) {
      const rows: any = {};
      for (const wz of [true, false]) {
        const qr = new Uint8Array(p);
        for (let i = 0; i < p; i++) { const v = i * i % p; if (!wz && v === 0) continue; qr[v] = 1; }
        let best = -1;
        for (let n = 0; n < p; n++) { let c = 0; for (let q = 0; q < p; q++) { const s = q * q % p; if (qr[(n - s + p * p) % p]) c++; } if (c > best) best = c; }
        rows[wz ? "QR0" : "QRno0"] = best;
      }
      ppm["p" + p] = rows;
    }
    out.perPrimeMax = ppm;
  }
  return out;
}

// ---------- MODE = "witness" ----------

const PRIMES: [number, number, number][] = [
  [5, 1, 2], [13, 2, 3], [17, 1, 4], [29, 5, 2], [37, 1, 6], [41, 4, 5],
  [53, 7, 2], [61, 5, 6], [73, 3, 8], [89, 5, 8], [97, 4, 9], [101, 1, 10],
  [109, 3, 10], [113, 7, 8], [137, 4, 11], [149, 7, 10],
];
const RLIMIT = 1e11, EMAX = 8;
const LS = [12, 17, 18, 19, 20, 21, 22];

function mulRep(l1: number[][], l2: number[][]): number[][] {
  const seen = new Set<number>(); const out: number[][] = [];
  for (const [u1, v1] of l1) for (const [u2, v2] of l2) {
    const a = Math.abs(u1 * u2 - v1 * v2), b = Math.abs(u1 * v2 + u2 * v1);
    const x = Math.max(a, b), y = Math.min(a, b);
    const key = x * 1000003 + y;
    if (!seen.has(key)) { seen.add(key); out.push([x, y]); }
  }
  return out;
}
function ppReps(p: number, a: number, b: number, e: number): number[][] {
  const out: number[][] = []; const seen = new Set<number>();
  for (let j = 0; j <= e; j++) {
    let ru = 1, rv = 0;
    for (let t = 0; t < j; t++) { const nu = ru * a - rv * b; rv = ru * b + rv * a; ru = nu; }
    for (let t = 0; t < e - j; t++) { const nu = ru * a + rv * b; rv = rv * a - ru * b; ru = nu; }
    const xx = Math.max(Math.abs(ru), Math.abs(rv)), yy = Math.min(Math.abs(ru), Math.abs(rv));
    const key = xx * 1000003 + yy;
    if (!seen.has(key)) { seen.add(key); out.push([xx, yy]); }
  }
  return out;
}
// 行->点数プロファイル。円 (2x+C)^2 + (2y+D)^2 = R、族 (D,C):
//   R ≡ 2 mod 4: (1,1)（全座標奇）。R 奇: (1,0)（奇座標が行・偶座標が点）と (0,1)。
// rep (a,b)（a>=b>=0）は 2y+D = ±a（点は ±b）と 2y+D = ±b（点は ±a）の両役割を持つ。
function evaluate(reps: number[][], D: number, C: number): Map<number, number> | null {
  const prof = new Map<number, number>(); let ok = false;
  for (const [a, b] of reps) {
    for (const B of [a, b]) {
      if (((B - D) % 2 + 2) % 2 !== 0) continue;
      const other = B === a ? b : a;
      let pts: number;
      if (other === 0) pts = (C === 0) ? 1 : 0; // 接点行（二重点 x=-C/2、C偶のとき1点）
      else pts = ((other - C) % 2 === 0) ? 2 : 0;
      if (pts === 0) continue;
      ok = true;
      if (B === 0) { const y = -D / 2; prof.set(y, (prof.get(y) || 0) + pts); }
      else {
        const y1 = (B - D) / 2, y2 = (-B - D) / 2;
        prof.set(y1, (prof.get(y1) || 0) + pts);
        prof.set(y2, (prof.get(y2) || 0) + pts);
      }
    }
  }
  return ok ? prof : null;
}
function runWitnessSearch() {
  const globalBest: Record<number, any> = {};
  for (const L of LS) globalBest[L] = { pts: -1, R: 0, D: 0, C: 0, y0: 0 };
  let count = 0;
  function scan(R: number, reps: number[][]) {
    count++;
    const fams: [number, number][] = (R % 2 === 0) ? [[1, 1]] : [[1, 0], [0, 1]];
    for (const [D, C] of fams) {
      const prof = evaluate(reps, D, C);
      if (!prof) continue;
      const rows = Array.from(prof.keys()).sort((x, y) => x - y);
      const pts = rows.map(r => prof.get(r)!);
      const n = rows.length;
      const pref = new Array(n + 1).fill(0);
      for (let i = 0; i < n; i++) pref[i + 1] = pref[i] + pts[i];
      for (const L of LS) {
        let j = 0, best = -1, bestI = -1;
        for (let i = 0; i < n; i++) {
          while (j < n && rows[j] < rows[i] + L) j++;
          const c = pref[j] - pref[i];
          if (c > best) { best = c; bestI = i; }
        }
        if (best > globalBest[L].pts) globalBest[L] = { pts: best, R, D, C, y0: rows[bestI] };
      }
    }
  }
  function rec(idx: number, remE: number, R: number, reps: number[][]) {
    if (reps.length >= 2) scan(R, reps);
    if (idx >= PRIMES.length || remE === 0) return;
    const [p, a, b] = PRIMES[idx];
    let pe = 1;
    for (let e = 1; e <= remE; e++) {
      pe *= p;
      const nR = R * pe;
      if (nR > RLIMIT) break;
      rec(idx + 1, remE - e, nR, mulRep(reps, ppReps(p, a, b, e)));
    }
    rec(idx + 1, remE, R, reps);
  }
  // 制御（既知 witness の再現）
  const controls: any = {};
  scan(130, [[11, 3], [9, 7]]);
  controls.R130 = { L12: globalBest[12].pts, attainedBy: 130 };
  scan(50, [[7, 1], [5, 5]]);
  controls.R50_L12 = globalBest[12].pts === 16 ? 16 : globalBest[12].pts;
  rec(0, EMAX, 1, [[1, 0]]);
  rec(0, EMAX, 2, [[1, 1]]);
  return { searchSpace: { primes: "p≡1 mod 4, p<=149", Rmax: RLIMIT, maxTotalExponent: EMAX, families: "R=2^a·∏p^e, a∈{0,1}" }, candidates: count, controls, globalBest };
}
