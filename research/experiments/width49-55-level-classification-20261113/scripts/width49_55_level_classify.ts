// width49_55_level_classify.ts — P(49) = ... = P(55) = 32 の完全決定（高速レーン 2026-11-13）。
// K0788 の streaming level 分類機の直接拡張（MAXROW 60・TARGETS を w=49..55 L=17 に）。
// 依存なし・決定的。STAGE 分割実行: TARGETS で (w,L) を 1..2 件ずつ指定して
// output JSON に集計する（単一 sandbox の deadline 対策・K0788 と同一運用）。
//
// 意味論・証明構造（K0784/K0788 と同一）:
//   level 17 全滅（全ての 17 点行集合がどこかの法で死ぬ）⟹ d+s ≤ 16 ⟹ P ≤ 32。
//   g0 ≥ 2 形は convention B classMax（g2 uodd 7..8・g3 11・g4+ 類サイズ ≤ 14 < 17）。
//   下界: 2210 円 (2x−A)²+(2y−B)²=2210 の全 32 点（v-span 94 ≤ 2(w−1), w ≥ 49）
//   → P(w) = 32 が w=49..55 で等号付き全称決定。
//   32 プラトーは w=43(K0788 の 26 から漸増し w=48 で 32)を経て w=55 まで継続。
//
// 制御: w=26 L=12 は S* ちょうど 1 生残（K0782/K0784/K0788 と一致）。
//   2210 witness の per-w 点数は K0786 の記録（26/28/28/30/30/32）に一致。

const qrC: Record<number, Uint8Array> = {};
const getQR = (m: number): Uint8Array => {
  if (!qrC[m]) { const s = new Uint8Array(m); for (let x = 0; x < m; x++) s[(x * x) % m] = 1; qrC[m] = s; }
  return qrC[m];
};
const REST = [19, 23, 7, 5, 27, 43, 47, 13, 17, 8, 16, 25, 29, 31, 37, 41];
const ALLMODS = [9, 11, 19, 23, 7, 5, 13, 17, 8, 16, 25, 27, 29, 31, 37, 41, 43, 47];
const NM = REST.length;
const wordsOf = REST.map(m => Math.ceil(m * m / 32));
const wOff: number[] = []; { let o = 0; for (const wn of wordsOf) { wOff.push(o); o += wn; } }
const TOTW = wOff[NM - 1] + wordsOf[NM - 1];
const MAXROW = 60;
const rowMask: Uint32Array[] = [];
for (let i = 0; i < MAXROW; i++) {
  const bs = new Uint32Array(TOTW);
  for (let mi = 0; mi < NM; mi++) {
    const m = REST[mi], qr = getQR(m), off = wOff[mi];
    const ii4 = (4 * i * i) % m;
    for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
      let t = (a - ii4 - u * i) % m; if (t < 0) t += m;
      if (qr[t]) { const bit = a * m + u; bs[off + (bit >> 5)] |= 1 << (bit & 31); }
    }
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
for (let d = 0; d <= 20; d++) bufs.push(new Uint32Array(TOTW));
function classify(w: number, L: number) {
  const { unique, maximal, masks } = maximalMasks(w, L);
  let nodes = 0, leaves = 0; const survSet = new Set<string>();
  const S: number[] = [];
  function dfs(start: number, T: number[], depth: number) {
    if (depth === L) { leaves++; survSet.add(S.join(",")); return; }
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
  for (const T of masks) { bufs[0].fill(0xFFFFFFFF); dfs(0, T, 0); }
  const survivors = [...survSet].map(s => s.split(",").map(Number));
  return { w, L, uniqueMasks: unique, maximalMasks: maximal, nodes, leaves, uniqueSurvivors: survivors.length, survivors: survivors.slice(0, 10) };
}
function classMax(rows: number[], coef: number, uOddForEvenMods: boolean): number {
  let best = Infinity;
  for (const m of ALLMODS) {
    const qr = getQR(m); let bm = 0;
    for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
      if (uOddForEvenMods && m % 2 === 0 && u % 2 === 0) continue;
      let c = 0;
      for (const y of rows) { let t = (a - (coef * y * y) % m - u * y) % m; if (t < 0) t += m; if (qr[t]) c++; }
      if (c > bm) bm = c;
    }
    if (bm < best) best = bm;
  }
  return best;
}
const isSq = (x: number) => { if (x < 0) return -1; const s = Math.round(Math.sqrt(x)); return s * s === x ? s : -1; };

async function main() {
  const TARGETS: Array<[number, number]> = JSON.parse((globalThis as any).process?.argv?.[2] ?? "null") ?? [
    [49, 17], [50, 17], [51, 17], [52, 17], [53, 17], [54, 17], [55, 17],
  ];
  const out: any = { generated: "2026-11-13", stages: {} };
  for (const [w, L] of TARGETS) {
    const r = classify(w, L);
    const n2e = Math.ceil(w / 2), n2o = Math.floor(w / 2);
    const cm2e = classMax([...Array(n2e).keys()], 16, true);
    const cm2o = classMax([...Array(n2o).keys()], 16, true);
    let cm3 = 0;
    for (let rr = 0; rr < 3; rr++) { const cls: number[] = []; for (let y = rr; y < w; y += 3) cls.push((y - rr) / 3); cm3 = Math.max(cm3, classMax(cls, 36, false)); }
    r.g0Accounting = { classMax_g2_B_uodd: { evens: cm2e, odds: cm2o }, classMax_g3_B: cm3, g4_classSize: Math.ceil(w / 4),
      levelDead: r.uniqueSurvivors === 0 && Math.max(cm2e, cm2o, cm3) < L && Math.ceil(w / 4) < L };
    out.stages["w" + w + "_L" + L] = r;
  }
  // witness 2210: per-w strip counts (control vs K0786: 26/28/28/30/30/32 at w=43..48)
  const vs: number[] = [];
  for (let a = 0; 2 * a * a <= 2210; a++) { const b = isSq(2210 - a * a); if (b >= a) { if (a === b) vs.push(a, a, -a, -a); else if (a === 0) vs.push(0, 0, b, b, -b, -b); else vs.push(a, a, -a, -a, b, b, -b, -b); } }
  vs.sort((x, y) => x - y);
  const perW: Record<number, number> = {};
  for (const w of [43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55]) {
    let best = 0, j = 0;
    for (let i = 0; i < vs.length; i++) { while (vs[i] - vs[j] > 2 * (w - 1)) j++; if (i - j + 1 > best) best = i - j + 1; }
    perW[w] = best;
  }
  out.witness2210 = { totalPoints: vs.length, vSpan: vs[vs.length - 1] - vs[0], perW };
  out.claims = {
    exact: { "49..55": 32 },
    plateau32: "w = 49..55 (K0788 の w=43..48 の帯 26..32 に続き、32 が平らに継続)",
    accounting: "level 17 dead => d+s <= 16 => P <= 32; 2210 witness (32 pts, span 94 <= 2(w-1)) => P >= 32",
    next: "level 17 revival point lies in (55, 83] (K0785: P(83) >= 34 => alive at 83). Binary search needs heavy runs (~1e8+ nodes); prime-power extended mods (K0789) may prune.",
  };
  return out;
}
const _r = await main();
(console as any).log(JSON.stringify(_r, null, 1));
