// width60_63_level_classify.ts — P(60)=P(61)=P(62)=P(63)=32 の完全決定（高速レーン 2026-11-13）。
// K0790/K0792 streaming level 分類機の直接拡張。本版はノード上限チャンクを機械に組み込み、
// classify(w, L, from, cap) が nodes >= cap で冪等に打ち切り lastDone（次チャンクの先頭）を返す。
// （K0792 運用の「1.2M ノード上限 + lastDone 記録」を関数化したもの。実行は 2 チャンク/1実行。）
//
// 意味論（K0784/K0788/K0790/K0792 と同一）: level 17 全滅 ⟹ d+s ≤ 16 ⟹ P ≤ 32。
// g0 ≥ 2 形は convention B classMax（K0792 数表: w60 g2 8/g3 12/g4 15・w61..63 g2 8/g3 13/g4 16・全て < 17）。
// 下界: 2210 円の全 32 点（v-span 94 ≤ 2(w−1), w ≥ 49）→ P(60..63) = 32 全称・等号付き。
// 注意: g4 類サイズ引数は w ≤ 64 で有効。w=65 で ⌈65/4⌉ = 17 = L に飽和。
//
// 制御: w=26 L=12 は S* ちょうど 1 生残（K0782/K0784/K0788/K0790/K0792 と一致）。
const qrC: Record<number, Uint8Array> = {};
const getQR = (m: number): Uint8Array => {
  if (!qrC[m]) { const s = new Uint8Array(m); for (let x = 0; x < m; x++) s[(x * x) % m] = 1; qrC[m] = s; }
  return qrC[m];
};
const REST = [19, 23, 7, 5, 27, 43, 47, 13, 17, 8, 16, 25, 29, 31, 37, 41];
const NM = REST.length;
const wordsOf = REST.map(m => Math.ceil(m * m / 32));
const wOff: number[] = []; { let o = 0; for (const wn of wordsOf) { wOff.push(o); o += wn; } }
const TOTW = wOff[NM - 1] + wordsOf[NM - 1];
const rowMask: Uint32Array[] = [];
for (let i = 0; i < 64; i++) {
  const bs = new Uint32Array(TOTW);
  for (let mi = 0; mi < NM; mi++) {
    const m = REST[mi], qr = getQR(m), off = wOff[mi];
    const ii4 = (4 * i * i) % m;
    for (let a = 0; a < m; a++) { const am = a - ii4; for (let u = 0; u < m; u++) {
      let t = (am - u * i) % m; if (t < 0) t += m;
      if (qr[t]) { const bit = a * m + u; bs[off + (bit >> 5)] |= 1 << (bit & 31); }
    } }
  }
  rowMask.push(bs);
}
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
  const bits = all.map(T => { let lo = 0, hi = 0; for (const i of T) { if (i < 32) lo |= 1 << i; else hi |= 1 << (i - 32); } return [lo, hi]; });
  const maximal: number[][] = [];
  for (let i = 0; i < all.length; i++) {
    let isMax = true;
    for (let j = 0; j < all.length; j++) {
      if (i === j) continue;
      if ((bits[i][0] & bits[j][0]) === bits[i][0] && (bits[i][1] & bits[j][1]) === bits[i][1]) {
        if (bits[i][0] !== bits[j][0] || bits[i][1] !== bits[j][1]) { isMax = false; break; }
      }
    }
    if (isMax) maximal.push(all[i]);
  }
  return { unique: all.length, maximal: maximal.length, masks: maximal };
}
const bufs: Uint32Array[] = [];
for (let d = 0; d <= 21; d++) bufs.push(new Uint32Array(TOTW));
function classify(w: number, L: number, from: number, cap: number) {
  const { unique, maximal, masks } = maximalMasks(w, L);
  let nodes = 0, leaves = 0; const survSet = new Set<string>();
  let aborted = false; let lastDone = -1;
  const S: number[] = [];
  function dfs(start: number, T: number[], depth: number) {
    if (depth === L) { leaves++; survSet.add(S.join(",")); return; }
    const cur = bufs[depth], nxt = bufs[depth + 1];
    for (let pi = start; pi <= T.length - (L - depth); pi++) {
      if (nodes >= cap) { aborted = true; return; }
      const i = T[pi]; nodes++;
      const rm = rowMask[i];
      let alive = true;
      for (let mi = 0; mi < NM; mi++) {
        const off = wOff[mi], wn = wordsOf[mi];
        let any = false;
        for (let k = off; k < off + wn; k++) { const v = cur[k] & rm[k]; nxt[k] = v; if (v !== 0) any = true; }
        if (!any) { alive = false; break; }
      }
      if (alive) { S.push(i); dfs(pi + 1, T, depth + 1); S.pop(); if (aborted) return; }
    }
  }
  for (let mi = from; mi < masks.length; mi++) {
    bufs[0].fill(0xFFFFFFFF); dfs(0, masks[mi], 0);
    if (!aborted) lastDone = mi + 1;
    if (aborted || nodes >= cap) break;
  }
  const survivors = [...survSet].map(s => s.split(",").map(Number));
  return { w, L, uniqueMasks: unique, totalMaximal: maximal, from, nodes, leaves, aborted, lastDone, uniqueSurvivors: survivors.length, survivors: survivors.slice(0, 10) };
}
const CFG = { w: 60, L: 17, from: 0, cap: 1200000, control26: true };
async function main() {
  const out: any = { generated: "2026-11-13", chunk: classify(CFG.w, CFG.L, CFG.from, CFG.cap) };
  if (CFG.control26) out.control_w26_L12 = classify(26, 12, 0, 10000000);
  return out;
}
const _r = await main();
(console as any).log(JSON.stringify(_r, null, 1));
