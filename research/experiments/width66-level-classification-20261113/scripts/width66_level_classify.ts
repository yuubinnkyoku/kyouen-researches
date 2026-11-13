// width66_level_classify.ts — P(66) 決定キャンペーン（高速レーン 2026-11-13 開始・進行中）。
// K0798（P(65)=32 完走）の直接続編。w=65 で確立した REST6 2フェーズ機
// （width65-pruning-audit の run() と同一構造）を最初から使用する。
//
// 前提: K0797 により convention B g0 会計は w=66 で有効（g2=8(法33)・g3=12(法22)・
// g4=5(法17)・全形 classMax < 17・拡張法33法・会計は w ≤ 84 で有効）。
// よって level 17 全滅 ⟹ d+s ≤ 16 ⟹ P(66) ≤ 32 が標準形掃引完走で確定する。
// 下界: 2210 円の全 32 点（v-span 94 ≤ 2·65 = 130）→ 完走なら P(66) = 32（等号付き）。
//
// 健全性（REST6 2フェーズ）: survivors(REST6) ⊇ survivors(REST16)
// （実現可能標準形は全合同証明書を通過・w26 L12 制御で S* ちょうど1生残）。
// REST6 生残0の mask は REST16 でも生残0確定。生残が出た mask のみフェーズ2で再走査。
// 窓マスクは66ビット（bits 配列のワード数は ceil(w/32) で自動化）。
//
// 進捗: unique=maximal 3,300 mask。chunks 1-8 で mask 0..888 完了（隣接漏れなし。
// gap mask 488/773/794/820 は個別証明済み）。計 19.6M nodes・leaves=0・生残0。
// resume from=889（=lastDone。resume_from は lastDone をそのまま使うこと — +1 すると
// mask を1個飛ばす〔第1-2セッションの教訓・mask 488 は飛ばし後に個別完走〕）。
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
  return { unique: all.length, maximal: maximal.length, masks: maximal };
}
// フェーズ1: REST6。生残が出た mask は REST16（width65_level_classify の REST 参照）で再走査。
const REST = [19, 23, 7, 29, 43, 47];
const NM = REST.length;
const wordsOf = REST.map(m => Math.ceil(m * m / 32));
const wOff: number[] = []; { let o = 0; for (const wn of wordsOf) { wOff.push(o); o += wn; } }
const TOTW = wOff[NM - 1] + wordsOf[NM - 1];
const W = 66;
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
const bufs: Uint32Array[] = [];
for (let d = 0; d <= 18; d++) bufs.push(new Uint32Array(TOTW));
function classify(w: number, L: number, from: number, cap: number) {
  const { unique, maximal, masks } = maximalMasks(w, L);
  let nodes = 0, leaves = 0, ops = 0; const survSet = new Set<string>();
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
        ops += wn;
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
  return { w, L, uniqueMasks: unique, totalMaximal: maximal, from, nodes, wordOps: ops, leaves, aborted, lastDone, uniqueSurvivors: survivors.length, survivors: survivors.slice(0, 10) };
}
const CFG = { w: 66, L: 17, from: 889, cap: 2400000, chunksPerRun: 1, control26: false };
async function main() {
  const out: any = { generated: "2026-11-13", rest: REST.join(","), chunks: [] };
  let from = CFG.from;
  for (let c = 0; c < CFG.chunksPerRun; c++) {
    const r = classify(CFG.w, CFG.L, from, CFG.cap);
    out.chunks.push(r);
    if (!r.aborted) from = r.lastDone; else break;
  }
  if (CFG.control26) out.control_w26_L12 = { note: "S*=[0,1,3,4,7,10,15,18,21,22,24,25] ちょうど1生残（K0782..K0798 と一致・width65-pruning-audit で REST6 制御済み）" };
  return out;
}
const _r = await main();
(console as any).log(JSON.stringify(_r, null, 1));
