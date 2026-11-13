
// K0801（P(67)=32 完走）の直接続編。w=65..67 で確立した REST6 2フェーズ機
// （width67_level_classify.ts の verbatim 移植・W=68・窓マスク 68 ビット・ワード数 ceil(w/32) 自動）。
//
// 前提: K0797 により convention B g0 会計は w ≤ 84 で有効（拡張法33法・全 g0 形 classMax < 17）。
// よって level 17 全滅 ⟹ d+s ≤ 16 ⟹ P(68) ≤ 32 が標準形掃引完走で確定する。
// 下界: 2210 円の全 32 点（v-span 94 ≤ 2·67 = 134）→ 完走なら P(68) = 32（等号付き）。
//
// 健全性（REST6 2フェーズ）: survivors(REST6) ⊇ survivors(REST16)
// （実現可能標準形は全合同証明書を通過・w26 L12 制御で S* ちょうど1生残・width65-pruning-audit）。
// REST6 生残0の mask は REST16 でも生残0確定。生残が出た mask のみフェーズ2で再走査。
//
// 【完走済み・K0802（P(68)=32）として昇格】
// 全 3,300 maximal mask を完走（sandbox chunks 1-24 + ネイティブ Node chunks 25-40・
// 総 92,219,331 + gap 587,531 nodes・leaves=0・生残0・phase2 必要 mask 0件）。
// 加えてネイティブ Node による独立全幅再実行（from=0・42チャンク・96,626,896 nodes・
// 28.6秒・leaves=0・生残0・gap なし単一連続）で二重確認済み
// （output/width68_native_completion.json。chunks 1-6 の境界と wordOps は sandbox 記録と
// 完全一致・mask 788/807 の classifyOne node 数も完全一致）。
// heavy band 構造: 第一帯 ~770..984（~46..480k/mask・最重要部 chunk12-13 の ~480k）→
// ~1000 沈み込み（~17k）→ 第二帯 ~1190..1308（~31..240k/mask・終点は w=67 の 1320 を
// 下回り右肩上がり則の反例）→ 以降 ~9..18k/mask の軽い帯。
// CFG.from=3300（完走状態・これ以上の再開不要）。
// CFG.from は resume_from=lastDone 規約（+1 すると mask を飛ばす・progress JSON が正本）。
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
const W = 68;
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
// 完走実行のドライバ: resume ループは r.lastDone > from の間継続
// （aborted チャンクも lastDone までの mask は完了済みなので from=lastDone で冪等再開）。
const CFG = { w: 68, L: 17, from: 3300, cap: 2400000, chunksPerRun: 200, note: "完走済み（K0802）。再実行時は from=0 から" };
async function main() {
  const out: any = { generated: "2026-11-14", rest: REST.join(","), chunks: [] };
  let from = CFG.from;
  for (let c = 0; c < CFG.chunksPerRun; c++) {
    const r = classify(CFG.w, CFG.L, from, CFG.cap);
    out.chunks.push(r);
    if (r.lastDone > from) from = r.lastDone; else break;
  }
  return out;
}
const _r = await main();
(console as any).log(JSON.stringify(_r, null, 1));
