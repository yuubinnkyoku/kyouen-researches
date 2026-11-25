/**
 * 26点円の最小行スパン（中心窓）— E/O/Z 3実現族の全数掃引機械
 * 実験: research/experiments/circle-26pt-min-rowspan-20261112/
 * 対応知識: K0785（この出力が本体の根拠）
 *
 * 定式化（詳細は reports/circle-26pt-min-rowspan.md）:
 *   R' = 奇・1mod4-smooth（3mod4素因数は平方でのみ現れ、その平方根部分 t は
 *   行オフセットを t 倍にスケールするだけなので W(t²r) = t(W(r)-1)+1 >= W(r)、
 *   最小円は常に t=1、すなわち 1mod4-smooth に限ってよい）。
 *   E族: (2x-A)^2+(2y-B)^2 = 2R' (A,B奇)  行オフセット = ±c/2, c in {X+Y, |X-Y|} (奇)
 *   O族: (2x-A)^2+(2y-B)^2 =  R' (A奇,B偶) 行オフセット = ±Y_even/2
 *   Z族: (2x-A)^2+(2y-B)^2 = 4R' (A,B偶)   行オフセット = ±X, ±Y
 *   ここで (X,Y) は R' のガウス整数因子 g = prod (a_j+ib_j)^k (a_j-ib_j)^(e_j-k)
 *   の (|Re|, |Im|)。各ペアは X^2+Y^2 = R' を機械検証（pairFail で計数）。
 *
 * bestK[K] = K二重行（2K点）を含み中心（オフセット0）を含む窓の最小幅:
 *   E: W = (c_max - c_min)/2 + 1（c は奇オフセットの2倍尺度）
 *   O/Z: W = span + 1
 *
 * 完備性（→ report）: E は W<=W0 で R' <= B_E(W0) = max(C², C²((C-2)²+16)/32),
 * C=2(W0-1)。Z は R' <= max(2C'², C'⁴/4+C'²), C'=W0-1。O は C''=2(W0-1) で
 * R' <= C''⁴/4+C''²。よって掃引上限が B を超えていれば bestK は全称。
 *
 * 実行方法: LO/HI を書き換えて段階実行（HI<=6.2e7 で実績、62M は
 * [1,11.3M] / (11.3,24] / (24,37] / (37,51.2] / (51.2,62] に分割推奨）。
 * 制御（期待値）:
 *   [1, 11,296,324]: c8 = 149,490 / c7 = 149,492 (D=7のみ 5⁶,13⁶)
 *     E 13:43@1105(一意) 14:44 15:46 16:48(@1105) 17..24 @5525, 25:211 26:214 @27625
 *     Z 13:58@1105(一意) 14:65 15:66 16:67(@1105) 17..24 @5525, 25:286 26:298 @27625
 *     O 13:149@27625
 *   R'<=20000 全円（118個）3族の行集合が素朴な整数点全列挙と完全一致（bruteFail=0）
 */

type Pair = [number, number];
const KMAX = 26;

// ---- 掃引区間 ----
const LO = 1;
const HI = 11296324;

// ---- ビット篩（奇数 >= 3; bit i = 数 2i+3）----
const nbits = (HI - 1) >> 1;
const sieve = new Uint8Array((nbits >> 3) + 1);
const isComp = (i: number) => (sieve[i >> 3] >> (i & 7)) & 1;
const setComp = (i: number) => { sieve[i >> 3] |= 1 << (i & 7); };
for (let n = 3; n * n <= HI; n += 2)
  if (!isComp((n - 3) >> 1)) for (let m = n * n; m <= HI; m += 2 * n) setComp((m - 3) >> 1);

function nextP14(from: number): number {
  let n = from < 3 ? 5 : from + ((from & 1) ? 0 : 1);
  if (n % 4 === 3) n += 2;
  if (n < 5) n = 5;
  while (n <= HI) { if (!isComp((n - 3) >> 1)) return n; n += 4; }
  return 0;
}

// D>=7 の R' に現れる素数は p <= HI/65（5·13·p パターンが最大）なので、
// (a,b) 表はその範囲のみ遅延計算
const REPMAX = Math.floor(HI / 65);
const repCache = new Map<number, Pair>();
function rep(p: number): Pair {
  let r = repCache.get(p);
  if (r) return r;
  r = [0, 0];
  for (let b = 0; 2 * b * b <= p; b++) {
    const a2 = p - b * b, a = Math.round(Math.sqrt(a2));
    if (a * a === a2) { r = [a, b]; break; }
  }
  repCache.set(p, r);
  return r;
}

// ---- 集計 ----
const mk = () => Array.from({ length: KMAX + 1 }, () => ({ w: Infinity, list: [] as number[] }));
const bestE = mk(), bestZ = mk(), bestO = mk();
let c7 = 0, c8 = 0, c14 = 0, pairFail = 0, repFail = 0, nodes = 0;
let bruteChecked = 0, bruteFail = 0;
const anomalies: string[] = [];
const facs: { a: number, b: number, e: number }[] = [];

function rowsFor(pairs: Pair[], fam: number): number[] {
  const s = new Set<number>();
  for (const [x, y] of pairs) {
    if (fam === 0) { s.add(x + y); s.add(-(x + y)); const d = Math.abs(x - y); s.add(d); s.add(-d); }
    else if (fam === 1) { s.add(x); s.add(-x); s.add(y); s.add(-y); }
    else { const e0 = x % 2 === 0 ? x : y; s.add(e0 / 2); s.add(-e0 / 2); }
  }
  return [...s].sort((a, b) => a - b);
}

function bestKW(rows: number[], scale: number): number[] {
  const n = rows.length, res = new Array(KMAX + 1).fill(Infinity);
  let first = n; for (let i = 0; i < n; i++) if (rows[i] >= 0) { first = i; break; }
  if (first === n) return res;
  for (let i = 0; i <= first; i++)
    for (let K = 13; K <= KMAX; K++) {
      const j = Math.max(i + K - 1, first); if (j >= n) break;
      const w = (rows[j] - rows[i]) / scale + 1;
      if (w < res[K]) res[K] = w;
    }
  return res;
}

// 素朴な整数点全列挙（独立検証用）
function bruteRows(Rp: number, fam: number): number[] {
  const s = new Set<number>();
  if (fam === 0) { // E: u,v 奇, u^2+v^2 = 2R', 行 = ±v/2 → c=±v
    const N = 2 * Rp;
    for (let v = 1; v * v <= N; v += 2) {
      const u2 = N - v * v, u = Math.round(Math.sqrt(u2));
      if (u * u === u2 && (u & 1) === 1) { s.add(v); s.add(-v); }
    }
  } else if (fam === 2) { // O: u 奇 v 偶, u^2+v^2 = R', 行 = ±v/2
    for (let t = 0; 4 * t * t <= Rp; t++) {
      const u2 = Rp - 4 * t * t, u = Math.round(Math.sqrt(u2));
      if (u * u === u2 && (u & 1) === 1) { s.add(t); s.add(-t); }
    }
  } else { // Z: U^2+V^2 = R', 行 = ±V
    for (let V = 0; V * V <= Rp; V++) {
      const U2 = Rp - V * V, U = Math.round(Math.sqrt(U2));
      if (U * U === U2) { s.add(V); s.add(-V); }
    }
  }
  return [...s].sort((a, b) => a - b);
}

function analyze(Rp: number) {
  const seen = new Set<number>();
  const pairs: Pair[] = [];
  const gen = (fi: number, X: number, Y: number) => {
    if (fi === facs.length) {
      const xx = Math.abs(X), yy = Math.abs(Y);
      const key = Math.min(xx, yy) * 16384 + Math.max(xx, yy);
      if (!seen.has(key)) { seen.add(key); pairs.push([xx, yy]); }
      return;
    }
    const { a, b, e } = facs[fi];
    const powA: Pair[] = [[1, 0]]; let ax = 1, ay = 0;
    for (let k = 1; k <= e; k++) { const nx = ax * a - ay * b, ny = ax * b + ay * a; powA.push([nx, ny]); ax = nx; ay = ny; }
    const powB: Pair[] = [[1, 0]]; let bx = 1, by = 0;
    for (let k = 1; k <= e; k++) { const nx = bx * a + by * b, ny = by * a - bx * b; powB.push([nx, ny]); bx = nx; by = ny; }
    for (let k = 0; k <= e; k++) {
      const A2 = powA[k], B2 = powB[e - k];
      const cx = A2[0] * B2[0] - A2[1] * B2[1], cy = A2[0] * B2[1] + A2[1] * B2[0];
      gen(fi + 1, X * cx - Y * cy, X * cy + Y * cx);
    }
  };
  gen(0, 1, 0);
  for (const [x, y] of pairs) if (x * x + y * y !== Rp) { pairFail++; return; }
  if (Rp <= 20000) {
    bruteChecked++;
    for (let fam = 0; fam < 3; fam++) {
      const pr = rowsFor(pairs, fam), br = bruteRows(Rp, fam);
      if (pr.length !== br.length || pr.some((v, i) => v !== br[i])) {
        bruteFail++; anomalies.push("BRUTE MISMATCH Rp=" + Rp + " fam=" + fam);
      }
    }
  }
  const tabs = [bestE, bestZ, bestO], scales = [2, 1, 1];
  for (let fam = 0; fam < 3; fam++) {
    const rows = rowsFor(pairs, fam);
    if (rows.length < 13) continue;
    const bk = bestKW(rows, scales[fam]);
    for (let K = 13; K <= KMAX; K++) {
      if (!isFinite(bk[K])) continue;
      const t = tabs[fam][K];
      if (bk[K] < t.w) { t.w = bk[K]; t.list = [Rp]; }
      else if (bk[K] === t.w && t.list.length < 12) t.list.push(Rp);
    }
    if (fam === 0 && bk[13] <= 52) anomalies.push("E b13=" + bk[13] + " Rp=" + Rp);
    if (fam === 1 && bk[13] <= 70) anomalies.push("Z b13=" + bk[13] + " Rp=" + Rp);
    if (fam === 2 && bk[13] <= 160) anomalies.push("O b13=" + bk[13] + " Rp=" + Rp);
  }
}

// ---- 枝刈り付き DFS（正しさの核心）----
// minUnits: D を >=7 まで持ち上げるのに必要な最小の追加素因数指数和。
// 同一素数の冪も許されるため、完了の価値の下界は p^(units) であり、
// p-loop の打ち切り条件は prod·p^(e+Fmin) の形で min を取る（詳細は report）。
const Emin = (D: number) => D >= 7 ? 0
  : (Math.ceil(7 / D) <= 2 ? 1 : Math.ceil(7 / D) <= 4 ? 2 : Math.ceil(7 / D) <= 6 ? 3 : 4);
const Fmin = (D: number) => {
  if (D >= 7) return 1;
  let m = Infinity;
  for (let e = 1; e <= 6; e++) m = Math.min(m, e + Emin(D * (e + 1)));
  return m;
};

function dfs(prod: number, D: number, minP: number) {
  nodes++;
  if (prod > 1 && D >= 7 && prod > LO) { c7++; if (D >= 8) c8++; if (D >= 14) c14++; analyze(prod); }
  const f = Fmin(D);
  for (let p = nextP14(minP); p !== 0; p = nextP14(p + 2)) {
    if (prod * Math.pow(p, f) > HI) break;
    if (p > REPMAX) break;
    const r = rep(p); if (r[0] === 0) { repFail++; break; }
    const [a, b] = r;
    let np = prod * p, e = 0;
    while (np <= HI) {
      e++; facs.push({ a, b, e });
      dfs(np, D * (e + 1), p + 2);
      facs.pop(); np *= p;
    }
  }
}

dfs(1, 1, 3);

const fmt = (t: ReturnType<typeof mk>) => {
  const r: string[] = [];
  for (let K = 13; K <= KMAX; K++)
    r.push(K + ":" + (isFinite(t[K].w) ? t[K].w + "@" + t[K].list.slice(0, 3).join(",") : "-"));
  return r.join(" ");
};
console.log(JSON.stringify({
  LO, HI, nodes, c7, c8, c14, d7only: c7 - c8, pairFail, repFail,
  bruteChecked, bruteFail, E: fmt(bestE), Z: fmt(bestZ), O: fmt(bestO),
  anomalies: anomalies.slice(0, 40), nAnom: anomalies.length,
}, null, 2));
