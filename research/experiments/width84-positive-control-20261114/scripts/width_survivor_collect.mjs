// w=69..84 level 17 全滅掃引機（K0802 完走機のパラメータ化版）。
// 用法: node width_sweep.mjs <W> <nodeBudgetPerRun> [deadlineSeconds=240]
// 進行状況は /home/user/sweep/state_w<W>.json に永続化し、冪等再開できる。
// 前提: K0797 会計は w ≤ 84 で有効。2210 円下界（32点）は w ≥ 49 で有効。
// したがって各幅で leaves=0・生残0 なら P(w) = 32（等号付き・全称）。
// w=83/84 は 34 点 witness（K0785/K0791・11050 円）が既知 → 生残が出るはず（正制御）。
// 単一maskがcapを超える停滞時は dynCap を8倍に拡張して進行保証（w=73 mask 927 は
// 2,504,084 nodes で cap 2.4M を超える初例・停滞検出は必須）。
import fs from 'fs';
const W = parseInt(process.argv[2], 10);
const BUDGET = parseInt(process.argv[3], 10) || 20000000;
const STATE = `/home/user/sweep/probe_w${W}.json`;
const CAP = 2400000;
const qrC = {};
const getQR = (m) => {
  if (!qrC[m]) { const s = new Uint8Array(m); for (let x = 0; x < m; x++) s[(x * x) % m] = 1; qrC[m] = s; }
  return qrC[m];
};
function buildMasks(m) {
  const qr = getQR(m); const masks = [];
  for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
    const mk = new Uint8Array(m);
    for (let i = 0; i < m; i++) { let t = (a - (4 * i * i) % m - u * i) % m; if (t < 0) t += m; mk[i] = qr[t]; }
    masks.push(mk);
  }
  return masks;
}
const m9 = buildMasks(9), m11 = buildMasks(11);
function maximalMasks(w, L) {
  const seen = new Map();
  for (let x = 0; x < 81; x++) for (let y = 0; y < 121; y++) {
    const T = [];
    for (let i = 0; i < w; i++) if (m9[x][i % 9] && m11[y][i % 11]) T.push(i);
    if (T.length >= L) { const k = T.join(","); if (!seen.has(k)) seen.set(k, T); }
  }
  const all = [...seen.values()];
  const nword = Math.ceil(w / 32);
  const bits = all.map(T => { const b = new Array(nword).fill(0); for (const i of T) b[i >> 5] |= 1 << (i & 31); return b; });
  const maximal = [];
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
const REST = [19, 23, 7, 29, 43, 47];
const NM = REST.length;
const wordsOf = REST.map(m => Math.ceil(m * m / 32));
const wOff = []; { let o = 0; for (const wn of wordsOf) { wOff.push(o); o += wn; } }
const TOTW = wOff[NM - 1] + wordsOf[NM - 1];
const rowMask = [];
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
const bufs = [];
for (let d = 0; d <= 18; d++) bufs.push(new Uint32Array(TOTW));
function classify(w, L, from, cap) {
  const { unique, maximal, masks } = maximalMasks(w, L);
  let nodes = 0, leaves = 0, ops = 0; const survSet = new Set();
  let aborted = false, lastDone = -1;
  const S = [];
  function dfs(start, T, depth) {
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
  return { uniqueMasks: unique, totalMaximal: maximal, from, nodes, wordOps: ops, leaves, aborted, lastDone, uniqueSurvivors: survivors.length, survivors: survivors.slice(0, 10) };
}
const L = 17;
let st = { from: 0, totalNodes: 0, chunks: [], done: false, survivors: 0, leaves: 0 };
if (fs.existsSync(STATE)) st = JSON.parse(fs.readFileSync(STATE, 'utf8'));
const t0 = Date.now();
let budget = BUDGET;
const DEADLINE = parseInt(process.argv[4] || '240', 10) * 1000;
fs.writeFileSync(STATE, JSON.stringify(st, null, 1));
let dynCap = CAP;
while (budget > 0 && !st.done) {
  if (Date.now() - t0 > DEADLINE) break;
  const cap = Math.min(dynCap, budget);
  const r = classify(W, L, st.from, cap);
  if (r.lastDone <= r.from && r.nodes > 0) { dynCap = dynCap * 8; st.capEscalations = (st.capEscalations || 0) + 1; }
  else dynCap = CAP;
  st.totalNodes += r.nodes;
  st.leaves += r.leaves;
  st.survivors += r.uniqueSurvivors;
  st.chunks.push({ from: r.from, lastDone: r.lastDone, nodes: r.nodes, wordOps: r.wordOps, leaves: r.leaves, aborted: r.aborted, survivors: r.uniqueSurvivors, survPats: r.survivors, uniqueMasks: r.uniqueMasks, totalMaximal: r.totalMaximal });
  budget -= r.nodes;
  if (r.lastDone > st.from) st.from = r.lastDone;
  if (!r.aborted && r.lastDone >= r.totalMaximal) st.done = true;
  if (r.lastDone <= st.from && r.nodes === 0) break;
  fs.writeFileSync(STATE, JSON.stringify(st, null, 1));
}
st.elapsedMs = Date.now() - t0;
st.w = W; st.L = L;
fs.writeFileSync(STATE, JSON.stringify(st, null, 1));
const last = st.chunks[st.chunks.length - 1];
console.log(JSON.stringify({ w: W, done: st.done, from: st.from, totalMasks: last ? last.totalMaximal : null, unique: last ? last.uniqueMasks : null, chunks: st.chunks.length, totalNodes: st.totalNodes, leaves: st.leaves, survivors: st.survivors, elapsedMs: st.elapsedMs, capEscalations: st.capEscalations || 0 }));
