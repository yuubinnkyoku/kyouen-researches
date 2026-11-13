// width65_pruning_audit.ts — w=65 キャンペーン機の枝刈り監査（高速レーン 2026-11-13）。
// 問い: (a) K0789 の素数冪（121=11²）を REST に足すと heavy band は速くなるか、
// (b) 法の検査順は費用最適か、(c) heavy band で一度も殺さない10法を外した
// REST6=[19,23,7,29,43,47] だけで十分か（2フェーズ方式の健全性と費用）。
//
// 測定（本セッション実測・詳細は output/width65_pruning_audit.json）:
//  - heavy band masks 962..974: REST16 1,166,798 nodes / 221.4M word-ops。
//    REST16+121（末尾）: 1,042,011 nodes / 435.5M ops（nodes -10.7% だが ops +96.8% → 損）。
//    並べ替え [7,19,23,29,...]: 215.6M ops（-2.6% only）。
//    REST6: 1,236,093 nodes / 120.9M ops（ops -45.4%）・leaves=0・生残0。
//  - light band masks 0..19: REST16 235,712 nodes / 49.4M ops。
//    REST6: 278,687 nodes / 29.6M ops（ops -40.1%）・leaves=0。
//  - kill attribution（heavy・REST16順）: 19:266,585 / 23:180,991 / 7:154,972 /
//    29:28,203 / 43:12,703 / 47:9,141 / 他10法（5,27,13,17,8,16,25,31,37,41）: 0。
//  - 制御: w=26 L=12 を REST6 で走らせると S*=[0,1,3,4,7,10,15,18,21,22,24,25] が
//    ちょうど1生残（実現可能集合は部分集合の法リストでも誤殺されない）。
//
// 2フェーズ方式の健全性: 実現可能な標準形の行集合は全ての合同証明書を通過する
// （整数 (a,u) が任意の法に落ちる）ため survivors(REST6) ⊇ survivors(REST16)。
// よって REST6 で生残0の mask は REST16 でも生残0が確定し、K0797 会計と合わせて
// P(65) ≤ 32 の主張にそのまま使える。REST6 で生残が出た mask だけ REST16 で再走査する。
// 結論: heavy band が沈まない w=65 では REST6 フェーズ1方式で総 ops を約半減できる
// （総ノード推定 ~200..250M・ops 観点で約2倍高速）。素数冪 121 の追加は本機では不採用。
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
function run(REST: number[], w: number, L: number, from: number, to: number, cap: number) {
  const NM = REST.length;
  const wordsOf = REST.map(m => Math.ceil(m * m / 32));
  const wOff: number[] = []; { let o = 0; for (const wn of wordsOf) { wOff.push(o); o += wn; } }
  const TOTW = wOff[NM - 1] + wordsOf[NM - 1];
  const rowMask: Uint32Array[] = [];
  for (let i = 0; i < w; i++) {
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
  for (let d = 0; d <= L + 1; d++) bufs.push(new Uint32Array(TOTW));
  let nodes = 0, leaves = 0, ops = 0; const survSet = new Set<string>();
  let aborted = false, lastDone = -1;
  const killCount = new Array(NM).fill(0);
  const S: number[] = [];
  const MM = maximalMasks(w, L);
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
        if (!any) { alive = false; killCount[mi]++; break; }
      }
      if (alive) { S.push(i); dfs(pi + 1, T, depth + 1); S.pop(); if (aborted) return; }
    }
  }
  for (let mi = from; mi < Math.min(MM.masks.length, to); mi++) {
    bufs[0].fill(0xFFFFFFFF); dfs(0, MM.masks[mi], 0);
    if (!aborted) lastDone = mi + 1;
    if (aborted || nodes >= cap) break;
  }
  return { rest: REST.join(","), w, L, masksFrom: from, masksTo: to, uniqueMasks: MM.unique, totalMaximal: MM.maximal, nodes, wordOps: ops, leaves, aborted, lastDone, survivors: survSet.size, survivorSample: [...survSet].slice(0, 3), killCount };
}
const BASE16 = [19, 23, 7, 5, 27, 43, 47, 13, 17, 8, 16, 25, 29, 31, 37, 41];
const REST6 = [19, 23, 7, 29, 43, 47];
const CFG = { w: 65, L: 17, heavyFrom: 962, heavyTo: 975, lightFrom: 0, lightTo: 20, cap: 20000000 };
async function main() {
  const out: any = { generated: "2026-11-13", configs: [] };
  out.configs.push(run(BASE16, CFG.w, CFG.L, CFG.heavyFrom, CFG.heavyTo, CFG.cap));       // baseline heavy
  out.configs.push(run([...BASE16, 121], CFG.w, CFG.L, CFG.heavyFrom, CFG.heavyTo, CFG.cap)); // +121 last
  out.configs.push(run([7, 19, 23, 29, 43, 47, 5, 13, 17, 8, 16, 25, 27, 31, 37, 41], CFG.w, CFG.L, CFG.heavyFrom, CFG.heavyTo, CFG.cap)); // reorder
  out.configs.push(run(REST6, CFG.w, CFG.L, CFG.heavyFrom, CFG.heavyTo, CFG.cap));       // REST6 heavy
  out.configs.push(run(BASE16, CFG.w, CFG.L, CFG.lightFrom, CFG.lightTo, CFG.cap));     // baseline light
  out.configs.push(run(REST6, CFG.w, CFG.L, CFG.lightFrom, CFG.lightTo, CFG.cap));       // REST6 light
  out.control_w26_L12_REST6 = run(REST6, 26, 12, 0, 10000, 10000000);
  return out;
}
const _r = await main();
(console as any).log(JSON.stringify(_r, null, 1));
