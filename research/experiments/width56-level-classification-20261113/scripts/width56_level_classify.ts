// width56_level_classify.ts — P(56) = 32 の完全決定 + w=57 分割実行（高速レーン 2026-11-13）。
// K0790 の streaming level 分類機の直接拡張。CFG で (w, L, from, to) を指定して
// maximal mask 列を分割実行する（sandbox deadline 対策・K0788/K0790 と同一運用）。
// K0789 の素数冪法 49/121/343 をリーフ証明書として追加（生残 17-集合に適用。
// 本実行では全 chunks で leaves=0 のため不発 — 元 16 法だけで w=56 は全滅）。
//
// 意味論（K0784/K0788/K0790 と同一）: level 17 全滅 ⟹ d+s ≤ 16 ⟹ P ≤ 32。
// g0 ≥ 2 形は convention B classMax（g2 uodd 8・g3 11・g4+ 類サイズ 14・全て < 17）。
// 下界: 2210 円の全 32 点（v-span 94 ≤ 2(w−1), w ≥ 49）→ P(56) = 32 全称・等号付き。
// 注意: この会計は w ≤ 64 で有効。w=65 で g4 類サイズ ⌈65/4⌉ = 17 = L に飽和し
// w ≥ 65 には g4 の精密化が必要（レポート参照）。
//
// 制御: w=26 L=12 は S* ちょうど 1 生残（K0782/K0784/K0788/K0790 と一致）。
const qrC: Record<number, Uint8Array> = {};
const getQR = (m: number): Uint8Array => {
  if (!qrC[m]) { const s = new Uint8Array(m); for (let x = 0; x < m; x++) s[(x * x) % m] = 1; qrC[m] = s; }
  return qrC[m];
};
const REST = [19, 23, 7, 5, 27, 43, 47, 13, 17, 8, 16, 25, 29, 31, 37, 41];
const PP = [49, 121, 343]; // K0789 素数冪リーフ証明書
const NM = REST.length;
const wordsOf = REST.map(m => Math.ceil(m * m / 32));
const wOff: number[] = []; { let o = 0; for (const wn of wordsOf) { wOff.push(o); o += wn; } }
const TOTW = wOff[NM - 1] + wordsOf[NM - 1];
const ppWords = PP.map(m => Math.ceil(m * m / 32));
const ppOff: number[] = []; { let o = 0; for (const wn of ppWords) { ppOff.push(o); o += wn; } }
const PPW = ppOff[PP.length - 1] + ppWords[PP.length - 1];
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
let rowPP: Uint32Array[] | null = null;
function buildPP() {
  rowPP = [];
  for (let i = 0; i < 64; i++) {
    const bp = new Uint32Array(PPW);
    for (let mi = 0; mi < PP.length; mi++) {
      const m = PP[mi], qr = getQR(m), off = ppOff[mi];
      const ii4 = (4 * i * i) % m;
      for (let a = 0; a < m; a++) { const am = a - ii4; for (let u = 0; u < m; u++) {
        let t = (am - u * i) % m; if (t < 0) t += m;
        if (qr[t]) { const bit = a * m + u; bp[off + (bit >> 5)] |= 1 << (bit & 31); }
      } }
    }
    rowPP.push(bp);
  }
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
for (let d = 0; d <= 20; d++) bufs.push(new Uint32Array(TOTW));
function ppKilled(S: number[]): boolean {
  if (!rowPP) buildPP();
  for (let mi = 0; mi < PP.length; mi++) {
    const off = ppOff[mi], wn = ppWords[mi];
    const acc = new Uint32Array(wn); acc.fill(0xFFFFFFFF);
    let anyAtEnd = false;
    for (const i of S) { const bp = rowPP![i]; let a2 = false;
      for (let k = 0; k < wn; k++) { acc[k] &= bp[off + k]; if (acc[k] !== 0) a2 = true; }
      if (!a2) return true;
    }
    for (let k = 0; k < wn; k++) if (acc[k] !== 0) { anyAtEnd = true; break; }
    if (!anyAtEnd) return true;
  }
  return false;
}
function classify(w: number, L: number, from: number, to: number) {
  const { unique, maximal, masks } = maximalMasks(w, L);
  let nodes = 0, leaves = 0, ppKills = 0; const survSet = new Set<string>();
  const S: number[] = [];
  function dfs(start: number, T: number[], depth: number) {
    if (depth === L) { leaves++;
      if (ppKilled(S)) { ppKills++; return; }
      survSet.add(S.join(",")); return; }
    const cur = bufs[depth], nxt = bufs[depth + 1];
    for (let pi = start; pi <= T.length - (L - depth); pi++) {
      const i = T[pi]; nodes++;
      const rm = rowMask[i];
      let alive = true;
      for (let mi = 0; mi < NM; mi++) {
        const off = wOff[mi], wn = wordsOf[mi];
        let any = false;
        for (let k = off; k < off + wn; k++) { const v = cur[k] & rm[k]; nxt[k] = v; if (v !== 0) any = true; }
        if (!any) { alive = false; break; }
      }
      if (alive) { S.push(i); dfs(pi + 1, T, depth + 1); S.pop(); }
    }
  }
  for (let mi = from; mi < Math.min(to, masks.length); mi++) { bufs[0].fill(0xFFFFFFFF); dfs(0, masks[mi], 0); }
  const survivors = [...survSet].map(s => s.split(",").map(Number));
  return { w, L, uniqueMasks: unique, totalMaximal: masks.length, maskRange: [from, Math.min(to, masks.length)], nodes, leaves, ppKills, uniqueSurvivors: survivors.length, survivors: survivors.slice(0, 10) };
}
const CFG = { w: 56, L: 17, from: 0, to: 2752, control26: true }; // chunk 実行時は from/to を書き換える
async function main() {
  const out: any = { generated: "2026-11-13", chunk: classify(CFG.w, CFG.L, CFG.from, CFG.to) };
  if (CFG.control26) out.control_w26_L12 = classify(26, 12, 0, 999);
  return out;
}
const _r = await main();
(console as any).log(JSON.stringify(_r, null, 1));
