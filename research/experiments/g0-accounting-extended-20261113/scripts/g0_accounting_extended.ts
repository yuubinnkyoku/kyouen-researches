// g0_accounting_extended.ts — convention B g0会計の有効範囲を拡張法で決定（高速レーン 2026-11-13）。
// K0794 レジューム(1)「w >= 65 用 g4 形 classMax 精密化」への回答。
//
// 意味論（K0788 convention B と同一）: e = q/g0（既約）の非標準形では全点行が
//   y = g0*t + r に合同し、s^2 = a' - 4*g0^2*t^2 - u'*t（a', u' in Z）。
//   g0 偶 => q 奇 => 偶数法では u' 奇制限が正当。
//   classMax(類, 4g0^2, uOdd) := min over m of max over (a,u) of
//     #{t in class: a - 4g0^2 t^2 - u t が QR(m)（0込み・x^2 mod m 全列挙で厳密）}。
//   classMax < 17 ⟹ level 17 の17点行集合（全点行が同一 g0 形）はどの (a,u) でも
//   どこかの法で死ぬ ⟹ 非標準形候補は全滅。
//
// 本実行の確定事項:
//   1. g4 形は壁ではない（classMax 5..9・u奇制限と係数64で自明に切れる）。
//   2. 拡張法（49, 121, 343, 53..83, 32, 64, 81, 125, 169 等）で
//      会計は w = 65..84 で有効。基底18法のみなら w <= 78。
//   3. 真の壁は g3 形: 類サイズ 29（w = 85..87）で全法（343 含む）とも
//      classMax = 17。witness (a,u) = (0,1) mod 31 が17点を生存させる。
//   4. g2 形は m = 32/64（u奇制限付き）で大幅強化され size 43 まで 10。
//
// 制御: (a) K0788/K0792/K0794 の base18 値（w36: 6/8・w42: 7/10・w48: 7/11・
//   w64: 8/13）を直接法で再現、(b) 増分sweepと直接法の一致（2点）、
//   (c) g3 size29 失敗 witness の明示。
// 依存なし・決定的（乱数・日時不使用）。単一 sandbox 実行で完走。
const qrC: Record<number, Uint8Array> = {};
const getQR = (m: number): Uint8Array => {
  if (!qrC[m]) { const s = new Uint8Array(m); for (let x = 0; x < m; x++) s[(x * x) % m] = 1; qrC[m] = s; }
  return qrC[m];
};
const BASE18 = [9, 11, 19, 23, 7, 5, 13, 17, 8, 16, 25, 27, 29, 31, 37, 41, 43, 47];
const EXTRA = [49, 121, 53, 59, 61, 67, 71, 73, 32, 64, 81, 125, 169, 79, 83];
const BIG = [343, 89, 97, 101, 103, 107, 109, 113, 127, 128, 243, 289, 131, 137, 139];
const COMBINED = [...BASE18, ...EXTRA, ...BIG];
function sweepBests(m: number, coef: number, uOdd: boolean, sMax: number) {
  const qr = getQR(m);
  const cnt = new Int16Array(m * m);
  const best = new Int16Array(sMax + 1);
  for (let s = 1; s <= sMax; s++) {
    const t = s - 1, tt = (coef * t * t) % m;
    for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
      if (uOdd && m % 2 === 0 && u % 2 === 0) continue;
      let v = (a - tt - (u * t) % m) % m; if (v < 0) v += m;
      if (qr[v]) cnt[a * m + u]++;
    }
    let b = 0; for (let k = 0; k < cnt.length; k++) if (cnt[k] > b) b = cnt[k];
    best[s] = b;
  }
  return best;
}
function classMaxDirect(size: number, coef: number, uOdd: boolean, mods: number[]) {
  let best = Infinity, bestM = -1, wA = -1, wU = -1;
  for (const m of mods) {
    const qr = getQR(m); let bm = 0, wa = -1, wu = -1;
    for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
      if (uOdd && m % 2 === 0 && u % 2 === 0) continue;
      let c = 0;
      for (let t = 0; t < size; t++) { let v = (a - (coef * t * t) % m - (u * t) % m) % m; if (v < 0) v += m; if (qr[v]) c++; }
      if (c > bm) { bm = c; wa = a; wu = u; }
    }
    if (bm < best) { best = bm; bestM = m; wA = wa; wU = wu; }
  }
  return { cm: best, bestM, witnessAU: [wA, wU] };
}
const L = 17, WMAX = 90;
const coefOf: Record<number, { coef: number; uOdd: boolean; sMax: number }> = {};
for (let g0 = 2; g0 <= 6; g0++) {
  if (Math.ceil(WMAX / g0) < L) break;
  coefOf[g0] = { coef: 4 * g0 * g0, uOdd: g0 % 2 === 0, sMax: Math.ceil(WMAX / g0) };
}
const swTab: Record<string, Int16Array> = {};
for (const g0 of Object.keys(coefOf).map(Number)) {
  const { coef, uOdd, sMax } = coefOf[g0];
  for (const m of COMBINED) swTab[g0 + ':' + m] = sweepBests(m, coef, uOdd, sMax);
}
function classMaxCombined(g0: number, size: number) {
  let best = Infinity, bestM = -1;
  for (const m of COMBINED) { const b = swTab[g0 + ':' + m][size]; if (b < best) { best = b; bestM = m; } }
  return { cm: best, bestM };
}
const accounting: any = {};
let frontier = 64;
for (let w = 65; w <= WMAX; w++) {
  const forms: any = {}; let valid = true;
  for (const g0 of Object.keys(coefOf).map(Number)) {
    const size = Math.ceil(w / g0);
    if (size < L) { forms['g' + g0] = { size, trivial: true }; continue; }
    const r = classMaxCombined(g0, size);
    forms['g' + g0] = { size, cm: r.cm, bestM: r.bestM };
    if (r.cm >= L) valid = false;
  }
  accounting['w' + w] = { valid, forms };
  if (valid) frontier = w; else if (frontier === w - 1) break;
}
let frontierB18 = 64;
for (let w = 65; w <= WMAX; w++) {
  let valid = true;
  for (const g0 of Object.keys(coefOf).map(Number)) {
    const size = Math.ceil(w / g0);
    if (size < L) continue;
    let best = Infinity;
    for (const m of BASE18) { const b = swTab[g0 + ':' + m][size]; if (b < best) best = b; }
    if (best >= L) { valid = false; break; }
  }
  if (valid) frontierB18 = w; else break;
}
const controls: any = {};
controls.k0788_k0792_k0794_base18 = {
  w36: { g2: classMaxDirect(18, 16, true, BASE18).cm, g3: classMaxDirect(12, 36, false, BASE18).cm },
  w42: { g2: classMaxDirect(21, 16, true, BASE18).cm, g3: classMaxDirect(14, 36, false, BASE18).cm },
  w48: { g2: classMaxDirect(24, 16, true, BASE18).cm, g3: classMaxDirect(16, 36, false, BASE18).cm },
  w64: { g2: classMaxDirect(32, 16, true, BASE18).cm, g3: classMaxDirect(22, 36, false, BASE18).cm },
  expect: { w36: [6, 8], w42: [7, 10], w48: [7, 11], w64: [8, 13] },
};
controls.sweep_vs_direct = {
  g2_m16_s32: [swTab['2:16'][32], classMaxDirect(32, 16, true, [16]).cm],
  g3_m49_s28: [swTab['3:49'][28], classMaxDirect(28, 36, false, [49]).cm],
};
{ const r = classMaxDirect(29, 36, false, COMBINED); controls.g3_size29_failure = { cm: r.cm, bestM: r.bestM, witness_au: r.witnessAU }; }
const out = {
  generated: '2026-11-13',
  claim: {
    accounting_valid_w_le: frontier,
    base18_only_frontier: frontierB18,
    wall: 'g3 form: class size 29 (w=85..87) has classMax=17 under every modulus tried (incl. 343); g4 form is NOT a wall (classMax 5..9 via uOdd + coef 64)',
  },
  controls, accounting,
  modulusLists: { BASE18, EXTRA, BIG },
};
(console as any).log(JSON.stringify(out, null, 1));
