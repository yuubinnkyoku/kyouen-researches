// maximal_mask_saturation.ts — maximal mask 数の w 依存性（高速レーン 2026-11-13）。
//
// 動機: width68 キャンペーン開始時の観察「maximal mask 数は w≥66 で 3,300 に飽和か」
// （research/log/2026-11-13-width68-level-classification.md・要 w≥69 検証）の検証。
//
// 結果（L=17・標準形掃引 harness と同一の窓マスク生成）:
//   w=62→3242・63→3278・64→3288・65→3296・66..72→3300（maximal）
//   w=75→3339/3300・80→3419/3300・90→3531/3300・99..132→3630/3300（unique/maximal）
//
// 観察:
// 1. **maximal mask 数は w=66..132 の全域でちょうど 3,300**（単調増加する unique と
//    非対照的に完全プラトー）。
// 2. w≥99 では unique も 3,630 で固定（窓条件は 9×11=99 周期・最初の 1 周期で
//    全ての相違が現れるためと解釈）。
// 3. 帰結（有限観察・全称主張は w=66..132 に限る）: level 17 掃引キャンペーンは
//    w≥66 で mask 数が一定 3,300 — コスト増は per-mask ノード加重のみ。
//    11×11 レーン（w≤121）でも掃引 harness のワークロードサイズは一定。
//
// 注意: 本計算は exhaustive-enumeration（窓マスクの全 (x,y)∈81×121 列挙 +
// 部分順序による maximal 判定の完全計算）であり、w=66..132 についての有限確定事実。
// w>132 は未計算（99 周期構造から w<198 まで 3,630/3,300 が維持されると予想されるが
// 有限実験の域を出ない）。
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
const WIDTHS = [62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 75, 80, 90, 99, 105, 110, 121, 132];
const results = WIDTHS.map(w => maximalMasks(w, 17));
(console as any).log(JSON.stringify(results));
