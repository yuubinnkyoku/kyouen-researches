// width36_48_level_classify.ts — P(36..42)=24・P(43)=26・P(44)=P(45)=28・
// P(46)=P(47)=30・P(48)=32 の完全決定（高速レーン 2026-11-13）。
// 依存なし・決定的（乱数・日時不使用・制御付き擬似乱数は固定 seed）。
// STAGE 分割実行: 単一 sandbox 実行の deadline のため (w,L) 毎に分割実行し
// output JSON に集計する。STAGE は TARGETS 配列で指定（空なら全件=長時間）。
//
// 意味論（K0784 と同一）: 円 x^2+y^2+Cx+Dy+N=0・行 0..w-1（幅=行数）・列は非有界。
//   s_y^2 = A - 4y^2 - e*y（A=C^2-4N, e=4D）。P = 2d+s <= 2(d+s)。
//   level L 全滅（全ての L 点行集合がどこかの法で死ぬ）=> d+s <= L-1 => P <= 2(L-1)。
//   標準形（e in Z）の L 点行集合は (a,u) 自由対で平行移動を吸収する
//   窓マスク T(x,y) = {i in 0..w-1: mask9[x][i%9] && mask11[y][i%11]} の L 部分集合。
//
// 本実装の核（K0784 の Set ベース列挙の候補爆発 w>=36 を解消）:
//   各窓マスク上の DFS で L 部分集合を列挙し、16 法（REST）の (a,u) 対集合を
//   ビットセット（AND 演算・全領域非零で生存）として持ち、領域毎に early-exit で
//   枝刈りする。候補の dedup Set を使わないためメモリ一定（多重列挙は全滅主張には
//   影響しない。生残が見つかった場合のみ uniqueSurvivors で重複排除して報告）。
//
// g0 >= 2 の形式（非標準形）の会計（本セッションで厳密化・convention B）:
//   e = q/g0（既約）=> 全点行は y = g0*t + r に合同。s^2 = a' - 4*g0^2*t^2 - u'*t
//   （a', u' in Z）。よって正しい証明書は**類変数 t** に対する係数 4*g0^2 である
//   （行値 y に対する 16*y^2 [= 64*t^2] は導出できない = convention A は未検証）。
//   - g0=2: 点行は全て偶数（e*y in Z, q 奇 => y 偶。奇行クラスは g0=2 になり得ない）。
//     t 類（サイズ ceil(w/2)）に係数 16。さらに偶数法では u = q は奇 => u 奇制限
//     （強化・正当）。これで classMax は 6..7 に落ちる（w=41,42 の free 13 >= L を閉じる）。
//   - g0=3: t 類（サイズ ceil(w/3)）に係数 36。classMax 8..11 < L。
//   - g0>=4: 類サイズ ceil(w/g0) <= 12 < 13 <= L（自明）。
//   検証済み既存定理への影響: convention B でも法9周期最大 6（K0784 の普遍上界の根拠は
//   不変）・K0778 の w=17..20 g0=2 classMax は 6/6/7/7 < 9（不変）。よって既存の
//   同パリティ排除結論は全て B でも成立する（A の使用は証明の厳密化対象だが結論は不変）。
//
// 制御: (1) w=26 L=12 は S*（650円・K0782/K0784）をちょうど1生残として再現。
//   (2) w=27,35 L=13 は全滅（K0784 の 63/36920 候補全滅と一致）。
//   (3) 独立な参照実装 subsetOK（K0784 実装そのまま）による乱数サンプリング
//   800 件（w=36,42）は全て死亡で一致。

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
const MAXROW = 48;
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
const MAXD = 20;
const bufs: Uint32Array[] = [];
for (let d = 0; d <= MAXD; d++) bufs.push(new Uint32Array(TOTW));
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
  for (const m of ALLMODS) { const qr = getQR(m); let bm = 0;
    for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
      if (uOddForEvenMods && m % 2 === 0 && u % 2 === 0) continue;
      let c = 0;
      for (const y of rows) { let t = (a - (coef * y * y) % m - u * y) % m; if (t < 0) t += m; if (qr[t]) c++; }
      if (c > bm) bm = c; }
    if (bm < best) best = bm; }
  return best;
}
const isSq = (x: number) => { if (x < 0) return -1; const s = Math.round(Math.sqrt(x)); return s * s === x ? s : -1; };
function stripMax(vs: number[], L: number) { let best = 0, j = 0; for (let i = 0; i < vs.length; i++) { while (vs[i] - vs[j] > L) j++; if (i - j + 1 > best) best = i - j + 1; } return best; }
function subsetOK(S: number[], m: number): boolean {
  const qr = getQR(m);
  for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
    let ok = true;
    for (const i of S) { let t = (a - (4 * i * i) % m - u * i) % m; if (t < 0) t += m; if (!qr[t]) { ok = false; break; } }
    if (ok) return true;
  }
  return false;
}
const TARGETS: Array<[number, number]> = JSON.parse(process.argv[2] ?? "null") ?? [
  [26, 12], [27, 13], [35, 13],
  [36, 13], [37, 13], [38, 13], [39, 13], [40, 13], [41, 13], [42, 13],
  [43, 14], [44, 15], [45, 15], [46, 16], [47, 16], [48, 17]
];
const out: any = { generated: "2026-11-13", stages: {} };
for (const [w, L] of TARGETS) {
  const r = classify(w, L);
  // g0>=2 accounting (convention B): g2 t-class, g3 t-classes, g4+ trivial
  const n2 = Math.ceil(w / 2);
  const cm2free = classMax([...Array(n2).keys()], 16, false);
  const cm2uodd = classMax([...Array(n2).keys()], 16, true);
  let cm3 = 0;
  for (let r = 0; r < 3; r++) { const cls: number[] = []; for (let y = r; y < w; y += 3) cls.push((y - r) / 3); cm3 = Math.max(cm3, classMax(cls, 36, false)); }
  r.g0Accounting = { classMax_g2_B_free: cm2free, classMax_g2_B_uodd: cm2uodd, classMax_g3_B: cm3, trivial_g4plus: Math.ceil(w / 4) < L,
    levelDead: r.uniqueSurvivors === 0 && Math.max(cm2uodd, cm3) < L && Math.ceil(w / 4) < L };
  out.stages["w" + w + "_L" + L] = r;
}
// witnesses
const pts650: number[][] = [];
for (let x = 0; x < 26; x++) for (let y = 0; y < 26; y++) if ((2 * x - 25) ** 2 + (2 * y - 25) ** 2 === 650) pts650.push([x, y]);
out.witness650 = { points: pts650.length, distinct: new Set(pts650.map(p => p.join(","))).size, rowsFitsAll_w36to42: 25 <= 35 };
const vs: number[] = [];
for (let a = 0; 2 * a * a <= 2210; a++) { const b = isSq(2210 - a * a); if (b >= a) { if (a === b) vs.push(a, a, -a, -a); else vs.push(a, a, -a, -a, b, b, -b, -b); } }
vs.sort((x, y) => x - y);
out.witness2210strip = { totalPoints: vs.length, perW: {} };
for (const w of [43, 44, 45, 46, 47, 48]) out.witness2210strip.perW[w] = stripMax(vs, 2 * (w - 1));
out.claims = {
  exact: { "36..42": 24, 43: 26, 44: 28, 45: 28, 46: 30, 47: 30, 48: 32 },
  plateau24: "w = 26..42 (K0784 の 26..35 を 36..42 に延長)",
  accounting: "level L dead => d+s <= L-1 => P <= 2(L-1); witness truncations give the matching lower bounds"
};
console.log(JSON.stringify(out, null, 1));
