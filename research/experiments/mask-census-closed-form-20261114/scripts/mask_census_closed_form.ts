// mask_census_closed_form.ts — K0805: level 17 窓マスク掃引の (unique(w), maximal(w)) センサス関数の
// 全幅閉形式決定の検証器（高速レーン 2026-11-14）。
//
// 前提（K0803 と同一の harness 生成）: 窓条件 cond(i) = m9[x][i mod 9] ∧ m11[y][i mod 11]
// （m9/m11 は (a,u) 全列挙 81/121 個の mod 9/11 二次剰余窓マスク）・L=17。
//
// 構造（本itemの定理）:
//   (1) パターン P = {i<99: cond(i)} は 3,994 相違（|P| ∈ {0,3,5,6,18,21,30,35,36,42}）。
//   (2) w<99: mask T_P(w) = P∩[0,w)（prefix）。passing big 上で単射（w=17..98 全幅で衝突 0）。
//       w≥99: 第1周期が完全に入り T から P が復元できる（単射）。
//   (3) |T_P(w)| = k·|P| + |P∩[0,rem)|（k=⌊w/99⌋・rem=w−99k）。
//       → unique(w) = #{P≠∅: |T_P(w)|≥17} = 交叉統計（各パターンの最小通過幅 w*(P) の累積）。
//       big は w*(P) = s17(P)+1（17番目の点の位置 + 1）∈ [37,96]。
//   (4) maximal（w<99）: T_P(w) ⊆ T_P'(w) ⟺ min(P\P') ≥ w（P\P' = ∅ を含む）。
//       ゆえに P は ordered pair (P,P') ごとに区間 [max(37,s17(P')+1), min(98,min(P\P'))]
//       で支配される（区間支配判定）。w≥99 では包含 ⟺ P⊆P'（反鎖）。
//   (5) 結論: maximal(w)=3300 がちょうど全 w≥66（w=66..98 は本判定で全幅厳密計算・
//       w≥99 は反鎖 3300 + K0803 支配補題）。w=37..65 では maximal=unique・w≤36 は 0。
//       unique(w)=3630 への到達は w=96 が鋭い。マスク初出現は w=37。
//       w=73 以降の unique 増分は既存パターンの真部分集合（maximal 不変の構造的原因）。
//
// 制御: census（maximal-mask-saturation-20261113 の 18 点）・K0804 dual-run unique（14 点）・
// K0803 広幅プローブ（unique(296)=3663・unique(396)=3960）・maximal(99) 反鎖 = 3300。
// 実行: node mask_census_closed_form.ts（依存なし・単一ファイル）。

const qrC: Record<number, Uint8Array> = {};
const getQR = (m: number): Uint8Array => {
  if (!qrC[m]) { const s = new Uint8Array(m); for (let x = 0; x < m; x++) s[(x * x) % m] = 1; qrC[m] = s; }
  return qrC[m];
};
function buildMasks(m: number): Uint8Array[] {
  const qr = getQR(m); const out: Uint8Array[] = [];
  for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
    const mk = new Uint8Array(m);
    for (let i = 0; i < m; i++) { let t = (a - (4 * i * i) % m - u * i) % m; if (t < 0) t += m; mk[i] = qr[t]; }
    out.push(mk);
  }
  return out;
}
const m9 = buildMasks(9), m11 = buildMasks(11);

// --- 相違パターン ---
const patMap = new Map<string, number[]>();
for (let x = 0; x < 81; x++) for (let y = 0; y < 121; y++) {
  const pts: number[] = [];
  for (let i = 0; i < 99; i++) if (m9[x][i % 9] && m11[y][i % 11]) pts.push(i);
  const key = pts.join(",");
  if (!patMap.has(key)) patMap.set(key, pts);
}
const pats = [...patMap.values()];
const big = pats.filter(p => p.length >= 18);
const N = big.length;

// --- ビット表現（30ビット×4ワード・32ビットシフトオーバーフロー回避） ---
const W0 = new Int32Array(N), W1 = new Int32Array(N), W2 = new Int32Array(N), W3 = new Int32Array(N);
const s17 = new Int32Array(N);
big.forEach((p, i) => {
  for (const b of p) {
    if (b < 30) W0[i] |= 1 << b;
    else if (b < 60) W1[i] |= 1 << (b - 30);
    else if (b < 90) W2[i] |= 1 << (b - 60);
    else W3[i] |= 1 << (b - 90);
  }
  s17[i] = p[16];
});

// --- (3) 最小通過幅 w*(P)（交叉統計） ---
function minPass(p: number[]): number {
  for (let w = 17; w <= 800; w++) {
    const k = Math.floor(w / 99), rem = w - 99 * k;
    let c = 0; for (const i of p) if (i < rem) c++; else break;
    if (k * p.length + c >= 17) return w;
  }
  return -1;
}
const changePoints = new Map<number, number>();
for (const p of pats) { if (p.length === 0) continue; const w = minPass(p); if (w > 0) changePoints.set(w, (changePoints.get(w) ?? 0) + 1); }
const cpSorted = [...changePoints.entries()].sort((a, b) => a[0] - b[0]);
const uniqAt = (w: number) => { let n = 0; for (const [cw, c] of cpSorted) if (cw <= w) n += c; return n; };

// --- (2) prefix 単射の全幅確認（衝突 0） ---
let collisionsOK = true;
for (let w = 17; w <= 98; w++) {
  const seen = new Set<string>();
  let npass = 0, ncls = 0;
  for (const p of big) {
    if (p[16] >= w) continue;
    npass++;
    const pre: number[] = []; for (const i of p) { if (i < w) pre.push(i); else break; }
    const k = pre.join(",");
    if (seen.has(k)) ncls++; else seen.add(k);
  }
  if (ncls !== 0) collisionsOK = false;
}

// --- (4) 区間支配判定で maximal(w), w=37..98 を一括厳密計算 ---
const BASE = 37, NW = 62;
const dominated = new Uint8Array(N * NW);
const dom99 = new Uint8Array(N);
let orderedPairs = 0;
for (let i = 0; i < N; i++) {
  for (let j = 0; j < N; j++) {
    if (i === j) continue;
    orderedPairs++;
    let x = W0[i] & ~W0[j]; let d = -1;
    if (x !== 0) d = 31 - Math.clz32(x & -x);
    else {
      x = W1[i] & ~W1[j];
      if (x !== 0) d = 30 + (31 - Math.clz32(x & -x));
      else {
        x = W2[i] & ~W2[j];
        if (x !== 0) d = 60 + (31 - Math.clz32(x & -x));
        else {
          x = W3[i] & ~W3[j];
          if (x !== 0) d = 90 + (31 - Math.clz32(x & -x));
          else d = 99; // P_i ⊂ P_j（真部分集合）: P_j が通過する全 w で支配
        }
      }
    }
    if (d === 99) {
      dom99[i] = 1;
      const lo = Math.max(BASE, s17[j] + 1);
      for (let w = lo; w <= 98; w++) dominated[i * NW + (w - BASE)] = 1;
    } else if (d >= BASE) {
      const lo = Math.max(BASE, s17[j] + 1), hi = Math.min(98, d);
      for (let w = lo; w <= hi; w++) dominated[i * NW + (w - BASE)] = 1;
    }
  }
}
const table: { w: number; unique: number; maximal: number }[] = [];
for (let w = 17; w <= 98; w++) {
  if (w < BASE) { table.push({ w, unique: 0, maximal: 0 }); continue; }
  let uniq = 0, mx = 0;
  for (let i = 0; i < N; i++) {
    if (s17[i] >= w) continue;
    uniq++;
    if (!dominated[i * NW + (w - BASE)]) mx++;
  }
  // 交叉統計との一致（prefix 単射）
  if (uniq !== uniqAt(w)) throw new Error("unique mismatch at w=" + w);
  table.push({ w, unique: uniq, maximal: mx });
}
let max99 = 0; for (let i = 0; i < N; i++) if (!dom99[i]) max99++;

// --- 制御照合 ---
const census: Record<number, [number, number]> = {
  62: [3242, 3242], 63: [3278, 3278], 64: [3288, 3288], 65: [3296, 3296], 66: [3300, 3300],
  67: [3300, 3300], 68: [3300, 3300], 69: [3300, 3300], 70: [3300, 3300], 71: [3300, 3300],
  72: [3300, 3300], 75: [3339, 3300], 80: [3419, 3300], 90: [3531, 3300]
};
const dual: Record<number, number> = {
  69: 3300, 70: 3300, 71: 3300, 72: 3300, 73: 3313, 74: 3326, 75: 3339, 76: 3353,
  77: 3367, 78: 3381, 79: 3400, 80: 3419, 81: 3438, 82: 3447
};
const failures: string[] = [];
for (const [ws, [u, mx]] of Object.entries(census)) {
  const r = table.find(t => t.w === +ws)!;
  if (r.unique !== u || r.maximal !== mx) failures.push("census w=" + ws);
}
for (const [ws, u] of Object.entries(dual)) {
  const r = table.find(t => t.w === +ws)!;
  if (r.unique !== u) failures.push("dual w=" + ws);
}
if (uniqAt(296) !== 3663) failures.push("wide296");
if (uniqAt(396) !== 3960) failures.push("wide396");
if (max99 !== 3300) failures.push("antichain99");
if (!collisionsOK) failures.push("prefixInjectivity");
const maximalPlateauAll = table.filter(t => t.w >= 66).every(t => t.maximal === 3300);
const maximalEqUniqueBelow = table.filter(t => t.w >= 37 && t.w <= 65).every(t => t.maximal === t.unique);

const out = {
  distinctPatterns: pats.length, bigPatterns: N, orderedPairsChecked: orderedPairs,
  prefixInjectivity_w17_98: collisionsOK,
  maximalPlateau3300_all_w66_98: maximalPlateauAll,
  maximalEqualsUnique_w37_65: maximalEqUniqueBelow,
  uniqueReaches3630_at: table.find(t => t.unique === 3630)!.w,
  firstMasksAt: table.find(t => t.unique > 0)!.w,
  maximalAt99_antichain: max99,
  wideUnique: { w296: uniqAt(296), w396: uniqAt(396) },
  controlFailures: failures,
  allControlsPass: failures.length === 0 && maximalPlateauAll && maximalEqUniqueBelow,
  table
};
console.log(JSON.stringify(out, null, 1));
