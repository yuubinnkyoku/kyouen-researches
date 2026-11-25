// width83_survivor_probe.mjs — 2026-11-14 高速レーン（w=83 正制御・付録プローブ）
//
// 目的: width_sweep.mjs（K0804機・repo掲載）の w=83 完走結果（leaves=2・生残2）の
//   生存マスク特定と、生残17行集合の完全抽出。width_sweep.mjs と同一アルゴリズム
//   （REST6=[19,23,7,29,43,47]・maximalMasks mod 9×11・bit-set DFS level 17）に
//   「どの mask が生残を出したか（survivorMasks）」と「生残17行集合そのもの
//   （survivorSets）」の記録を加えたもの。決定的・依存なし。
//
// 用法: node width83_survivor_probe.mjs <W> <FROM> <TO> <CAP>
//   mask FROM..TO−1 を cap CAP で分類し、生残 mask と生残集合を stdout に出力。
//   実行例（K0807 の実行値・Node.js v22 ネイティブ実行）:
//     node width83_survivor_probe.mjs 83 454 467 60000000
//       -> mask 456: {0,5,7,19,27,32,40,52,54,59,63,70,73,76,77,81,82} (1 leaf)
//     node width83_survivor_probe.mjs 83 3114 3120 60000000
//       -> mask 3119: {0,1,5,6,9,12,19,23,28,30,42,50,55,63,75,77,82} (1 leaf)
//   この2件が state_w83.json の leaves=2 の全容（完走走査・K0804 と同じ前提）。
const W = parseInt(process.argv[2], 10);
const FROM = parseInt(process.argv[3], 10);
const TO = parseInt(process.argv[4], 10);
const CAP = parseInt(process.argv[5], 10);
const L = 17;
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
function maximalMasks(w, Lv) {
  const seen = new Map();
  for (let x = 0; x < 81; x++) for (let y = 0; y < 121; y++) {
    const T = [];
    for (let i = 0; i < w; i++) if (m9[x][i % 9] && m11[y][i % 11]) T.push(i);
    if (T.length >= Lv) { const k = T.join(","); if (!seen.has(k)) seen.set(k, T); }
  }
  const all = [...seen.values()];
  const nword = Math.ceil(w / 32);
  const bits = all.map(T => { const b = new Array(nword).fill(0); for (const i of T) b[i >> 5] |= 1 << (i & 31); return b; });
  const maximalIdx = [];
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
    if (isMax) maximalIdx.push(i);
  }
  return { unique: all.length, masks: maximalIdx.map(i => all[i]) };
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
const bufs = []; for (let d = 0; d <= 18; d++) bufs.push(new Uint32Array(TOTW));
const { unique, masks } = maximalMasks(W, L);
const S = []; let nodes = 0; const survMaskIdx = new Set(); const survivorSets = new Set(); let curMi = -1;
function dfs(start, T, depth) {
  if (depth === L) { survMaskIdx.add(curMi); survivorSets.add(S.join(",")); return; }
  const cur = bufs[depth], nxt = bufs[depth + 1];
  for (let pi = start; pi <= T.length - (L - depth); pi++) {
    if (nodes >= CAP) return;
    const i = T[pi]; nodes++;
    const rm = rowMask[i]; let alive = true;
    for (let mi = 0; mi < NM; mi++) {
      const off = wOff[mi], wn = wordsOf[mi]; let any = false;
      for (let k = off; k < off + wn; k++) { const v = cur[k] & rm[k]; nxt[k] = v; if (v !== 0) any = true; }
      if (!any) { alive = false; break; }
    }
    if (alive) { S.push(i); dfs(pi + 1, T, depth + 1); S.pop(); }
  }
}
const out = { w: W, uniqueMasks: unique, probed: [], totalNodes: 0, survivorSets: [], survivorMasks: [] };
for (let mi = FROM; mi < Math.min(TO, masks.length); mi++) {
  curMi = mi; const before = survivorSets.size;
  bufs[0].fill(0xFFFFFFFF); dfs(0, masks[mi], 0);
  out.probed.push({ mi, rows: masks[mi].length, newSurvivors: survivorSets.size - before });
}
out.totalNodes = nodes; out.survivorSets = [...survivorSets]; out.survivorMasks = [...survMaskIdx];
console.log(JSON.stringify(out));
