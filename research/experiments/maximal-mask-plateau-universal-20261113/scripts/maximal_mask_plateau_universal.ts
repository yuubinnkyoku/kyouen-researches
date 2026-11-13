// maximal_mask_plateau_universal.ts — maximal mask 3,300 プラトーの全称化（高速レーン 2026-11-13）。
//
// 動機: maximal-mask-saturation-20261113 で w=62..132 の有限確定事実
// （maximal は w=66..132 の全測定点でちょうど 3,300）を得たが、
// 「w>132 は未計算・99 周期構造から w<198 まで維持が予想されるが予想の域」
// だった。本scriptは予想を**全称定理（99 ≤ w < 198）**に昇格させる検証器。
//
// 定理（proved・全称・L=17・標準形掃引 harness と同一の窓マスク生成）:
//   任意の幅 w ∈ [99, 198) に対し、窓マスク掃引の unique = 3,630・
//   maximal = 3,300 がちょうど成り立つ。
//
// 証明の骨子（機械検証は本script・紙証明は report.md）:
//   (a) 窓条件 cond(i) = [m9[x][i mod 9] ∧ m11[y][i mod 11]] は i について 99 周期
//       （99 ≡ 0 mod 9・mod 11）。全 (x,y)・i<99 で機械確認。
//   (b) w ≥ 99 で T(w) ∩ [0,99) = P（パターン）→ パターン→T(w) は単射で
//       T1(w) ⊆ T2(w) ⟺ P1 ⊆ P2（点順序の順序同型）。
//   (c) CRT: |P| = c9·c11（[0,99) で各 (i mod 9, i mod 11) 対がちょうど1回）。
//       全 81×121 対で機械確認（不一致 0）。
//   (d) popcount 集合: c9 ∈ {0,3,5,6}・c11 ∈ {1,6,7}（各 81/121 マスクの完全列挙）→
//       |P| ∈ {0,3,5,6,18,21,30,35,36,42} で [7,17] に空き（ヒストグラム検証）。
//   (e) 99 ≤ w < 198: |T(w)| = |P| + |P∩[0,w−99)|。|P| ≥ 18 → 通過・
//       |P| ≤ 6 → |T| ≤ 12 < 17 で不通過 → フィルタは w=99 と完全同値。
//       ゆえに unique・maximal は w=99 の値（3,630/3,300）と一致する。
//   (f) 境界の限定: k ≥ 2 周期（w ≥ 198 かつ余り大きい）では |P|=6 の
//       パターンが |T| ≥ 17 に届き新規参入する（w=296 で機械確認済み）→
//       定理は w ∈ [99,198) に真に限定される（安易な全 w への拡大は誤り）。
const qrC: Record<number, Uint8Array> = {};
const getQR = (m: number): Uint8Array => {
  if (!qrC[m]) { const s = new Uint8Array(m); for (let x = 0; x < m; x++) s[(x * x) % m] = 1; qrC[m] = s; }
  return qrC[m];
};
function buildMasks(m: number): Uint8Array[] {
  const qr = getQR(m); const masks: Uint8Array[] = [];
  for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
    const mk = new Uint8Array(m);
    for (let i = 0; i < m; i++) { let t = (a - (4 * i * i) % m - u * i) % m; if (t < 0) t += m; mk[i] = qr[t]; }
    masks.push(mk);
  }
  return masks;
}
const m9 = buildMasks(9), m11 = buildMasks(11);
const pc = (arr: Uint8Array) => arr.reduce((s, v) => s + v, 0);
function maximalMasks(w: number, L: number) {
  const seen = new Map<string, number[]>();
  for (let x = 0; x < 81; x++) for (let y = 0; y < 121; y++) {
    const T: number[] = [];
    for (let i = 0; i < w; i++) if (m9[x][i % 9] && m11[y][i % 11]) T.push(i);
    if (T.length >= L) { const k = T.join(","); if (!seen.has(k)) seen.set(k, T); }
  }
  const all = [...seen.values()];
  const nword = Math.ceil(w / 32);
  const bits = all.map(T => { const b = new Array(nword).fill(0); for (const i of T) b[i >> 5] |= 1 << (i & 31); return b; });
  const maximal: number[][] = [];
  for (let i = 0; i < all.length; i++) {
    let isMax = true;
    for (let j = 0; j < all.length; j++) {
      if (i === j) continue;
      let sub = true, eq = true;
      for (let k = 0; k < nword; k++) {
        if ((bits[i][k] & bits[j][k]) !== bits[i][k]) { sub = false; break; }
        if (bits[i][k] !== bits[j][k]) eq = false;
      }
      if (sub && !eq) { isMax = false; break; }
    }
    if (isMax) maximal.push(all[i]);
  }
  return { w, unique: all.length, maximal: maximal.length };
}
// (a) 周期性
let perOK = true;
outer: for (let x = 0; x < 81; x++) for (let y = 0; y < 121; y++) for (let i = 0; i < 99; i++) {
  if (!!(m9[x][i % 9] && m11[y][i % 11]) !== !!(m9[x][(i + 99) % 9] && m11[y][(i + 99) % 11])) { perOK = false; break outer; }
}
// (c) CRT |P| = c9·c11
let crtOK = true, crtBad = 0;
for (let x = 0; x < 81; x++) for (let y = 0; y < 121; y++) {
  let n = 0;
  for (let i = 0; i < 99; i++) if (m9[x][i % 9] && m11[y][i % 11]) n++;
  if (n !== pc(m9[x]) * pc(m11[y])) { crtOK = false; crtBad++; }
}
// (d) popcount 集合と |P| ヒストグラム（相違パターン）
const c9set = new Map<number, number>(), c11set = new Map<number, number>();
for (const mk of m9) c9set.set(pc(mk), (c9set.get(pc(mk)) ?? 0) + 1);
for (const mk of m11) c11set.set(pc(mk), (c11set.get(pc(mk)) ?? 0) + 1);
const seenPat = new Map<string, number>();
for (let x = 0; x < 81; x++) for (let y = 0; y < 121; y++) {
  const P: number[] = [];
  for (let i = 0; i < 99; i++) if (m9[x][i % 9] && m11[y][i % 11]) P.push(i);
  const k = P.join(",");
  seenPat.set(k, (seenPat.get(k) ?? 0) + 1);
}
const hist = new Map<number, number>();
for (const k of seenPat.keys()) { const n = k === "" ? 0 : k.split(",").length; hist.set(n, (hist.get(n) ?? 0) + 1); }
const histSorted = [...hist.entries()].sort((a, b) => a[0] - b[0]);
const gapOK = [...hist.keys()].every(n => n <= 6 || n >= 18);
// (e) サンプル幅での全称主張の再現（制御 w=99 + w∈[133,198) の代表点）
const WIDTHS = [99, 133, 140, 150, 160, 170, 180, 190, 197];
const sampled = WIDTHS.map(w => maximalMasks(w, 17));
// (f) 境界プローブ: w=296 で |P|=6 パターンがフィルタに参入するか
let smallEnters296 = false;
for (let x = 0; x < 81; x++) for (let y = 0; y < 121; y++) {
  if (pc(m9[x]) * pc(m11[y]) === 6) {
    let n = 0;
    for (let i = 0; i < 296; i++) if (m9[x][i % 9] && m11[y][i % 11]) n++;
    if (n >= 17) smallEnters296 = true;
  }
}
const out = {
  generated: "2026-11-13",
  theoremScope: "99 <= w < 198",
  checks: {
    periodicity99: perOK,
    crtAbs: crtOK, crtMismatches: crtBad,
    c9Popcounts: [...c9set.entries()].sort((a, b) => a[0] - b[0]),
    c11Popcounts: [...c11set.entries()].sort((a, b) => a[0] - b[0]),
    distinctPatterns: seenPat.size,
    patternPopcountHistogram: histSorted,
    gap7to17Empty: gapOK
  },
  sampledWidths: sampled,
  boundaryProbe_w296_smallPatternEnters: smallEnters296
};
(console as any).log(JSON.stringify(out, null, 1));
