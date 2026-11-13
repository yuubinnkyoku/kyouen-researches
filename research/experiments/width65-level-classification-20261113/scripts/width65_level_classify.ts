// width65_level_classify.ts — P(65) 決定キャンペーン（高速レーン 2026-11-13 開始・進行中）。
// K0793/K0794 機（16法 REST bit-set DFS + classify 内蔵ノード上限チャンク 1.2M・
// lastDone 返却・冪等再開）の w=65 実行版。**w=65 は窓マスクが65ビットになるため
// bits を3ワード化**（K0794 の2ワード版からの唯一の構造変更）。
//
// 前提: K0797 により convention B g0 会計は w=65 で有効
// （g2=8(33)・g3=12(22)・g4=5(17)・全形 classMax < 17・拡張法33法）。
// よって level 17 全滅 ⟹ d+s ≤ 16 ⟹ P(65) ≤ 32 が標準形掃引完走で確定する。
// 下界: 2210 円の全 32 点（v-span 94 ≤ 2·64）→ 完走なら P(65) = 32（等号付き）。
//
// 進捗（2026-11-13 第3セッション末）: mask 0..974 完了（lastDone=975）・
// ノード計 21.6M（18チャンク×1.2M・w26制御別）・leaves=0・生残0。重い帯は mask ~772 以降
// 沈まず 71k..100k nodes/mask でほぼ平坦（総ノード推定 ~200..250M に上方修正）。
// 制御: w=26 L=12 は S* ちょうど1生残（K0782..K0794 と一致・初回実行で確認済み）。
//
// レジューム: CFG.from を直前の lastDone に更新して再実行（チャンク境界は
// マスク単位で冪等）。uniqueMasks 3,296・totalMaximal 3,296。
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
const W = 65;
const rowMask: Uint32Array[] = [];
for (let i = 0; i < W; i++) {
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
  const bits = all.map(T => { const b = [0, 0, 0]; for (const i of T) b[i >> 5] |= 1 << (i & 31); return b; });
  const maximal: number[][] = [];
  for (let i = 0; i < all.length; i++) {
    let isMax = true;
    for (let j = 0; j < all.length; j++) {
      if (i === j) continue;
      let sub = true, eq = true;
      for (let k = 0; k < 3; k++) {
        if ((bits[i][k] & bits[j][k]) !== bits[i][k]) { sub = false; break; }
        if (bits[i][k] !== bits[j][k]) eq = false;
      }
      if (sub && !eq) { isMax = false; break; }
    }
    if (isMax) maximal.push(all[i]);
  }
  return { unique: all.length, maximal: maximal.length, masks: maximal };
}
const MAXD = 18;
const bufs: Uint32Array[] = [];
for (let d = 0; d <= MAXD; d++) bufs.push(new Uint32Array(TOTW));
function classify(w: number, L: number, from: number, cap: number) {
  const { unique, maximal, masks } = maximalMasks(w, L);
  let nodes = 0, leaves = 0; const survSet = new Set<string>();
  let aborted = false, lastDone = -1;
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
const CFG = { w: 65, L: 17, from: 3296, cap: 1200000, chunksPerRun: 2, control26: false };
// 完走（2026-11-13）: 全 3,296 maximal mask・leaves=0・生残0（chunks 1-18 本機 REST16・
// chunks 19-27 は width65-pruning-audit の REST6 2フェーズ機 cap 2.4M）。P(65)=32 → K0798。
async function main() {
  const out: any = { generated: "2026-11-13", chunks: [] };
  let from = CFG.from;
  for (let c = 0; c < CFG.chunksPerRun; c++) {
    const r = classify(CFG.w, CFG.L, from, CFG.cap);
    out.chunks.push(r);
    if (!r.aborted) from = r.lastDone; else break;
  }
  if (CFG.control26) out.control_w26_L12 = classify(26, 12, 0, 10000000);
  return out;
}
const _r = await main();
(console as any).log(JSON.stringify(_r, null, 1));
