// circle_strip_scan.ts — 幅w固定・長さm可変盤の円点数P(w)の家族スキャン（高速レーン 2026-11-12）
// 依存なし。node（または任意のJS処理系）で実行可。決定的（乱数・日時不使用）。
// 出力: JSON（stdout）— per-w 最大・制御比較・witness検証
//
// 意味論（K0784 と同一の strip 窓意味論）:
//   盤は幅 w（拘束軸）× 長さ m（自由軸・全 m>=1）。円の格子点のうち拘束軸座標が
//   長さ 2(w-1)（半整数中心 F1/F3）または w-1（整数中心 F2）の区間に収まる点を数える。
//   自由軸は m を大きくすれば非拘束。窓位置は円の平行移動で自由（全位置の max を取る）。
// 家族:
//   F1: (2x-A)^2+(2y-B)^2=R, A,B 奇（半整数中心）→ 拘束座標は奇。窓長 2(w-1)。
//   F2: (x-A)^2+(y-B)^2=R（整数中心）→ 拘束座標は任意。窓長 w-1。
//   F3: R 奇・混合パリティ中心 → 拘束座標は偶/奇クラス（各 r2/2 点）。窓長 2(w-1)。
// スコープ: 円の格子点座標の絶対値 <= CMAX=256（R <= 65536）の有限観測。
//   witness 構成（下界）は全て厳密（整数検証）。上界は主張しない。
// 実装注意（2026-11-12 に修正した2バグ・再発防止）:
//   1) 多重集合の対角外ブランチは ±a各2回・±b各2回が正しい。引数の誤植で片側が
//      3回/1回になると strip が過大に出る（R=650 で 8→10 を確認済み）。
//   2) r2 篩: p≡1 mod 4 の素因数は指数 e に対して (e+1)（e+2 ではない）。
//      p≡3 mod 4 は奇指数で r2=0。2の冪は r2 を変えない。

const CMAX = 256;
const RMAX = CMAX * CMAX;
const WMIN = 6, WMAX = 48, NW = WMAX - WMIN + 1;
const spf = new Int32Array(RMAX + 1);
for (let i = 2; i <= RMAX; i++) if (!spf[i]) for (let j = i; j <= RMAX; j += i) if (!spf[j]) spf[j] = i;
const r2c = new Int32Array(RMAX + 1);
for (let n = 1; n <= RMAX; n++) {
  let m = n, prod = 1, ok = true;
  while (m > 1) { const p = spf[m]; let e = 0; while (m % p === 0) { m /= p; e++; }
    if (p % 4 === 3) { if (e % 2) { ok = false; break; } } else if (p % 4 === 1) prod *= e + 1; }
  r2c[n] = ok ? 4 * prod : 0;
}
const isSq = (x) => { const s = Math.round(Math.sqrt(x)); return s * s === x ? s : -1; };
function pairsOfR(R) { const out = []; for (let a = 0; 2 * a * a <= R; a++) { const b = isSq(R - a * a); if (b >= a) out.push([a, b]); } return out; }
function multF1(R) { const vs = []; for (const [a, b] of pairsOfR(R)) { if (a === b) vs.push(a, a, -a, -a); else vs.push(a, a, -a, -a, b, b, -b, -b); } return vs.sort((x, y) => x - y); }
function multF2(R) { const vs = []; for (const [a, b] of pairsOfR(R)) { if (a === 0) vs.push(0, 0, b, -b); else if (a === b) vs.push(a, a, -a, -a); else vs.push(a, a, -a, -a, b, b, -b, -b); } return vs.sort((x, y) => x - y); }
function multF3(R) { const ve = [], vo = []; for (const [a, b] of pairsOfR(R)) { const ev = a % 2 === 0 ? a : b, od = a % 2 === 0 ? b : a;
  if (a === 0) { ve.push(0, 0); vo.push(b, -b); } else { ve.push(ev, ev, -ev, -ev); vo.push(od, od, -od, -od); } } return [ve.sort((x, y) => x - y), vo.sort((x, y) => x - y)]; }
function stripMax(vs, L) { let best = 0, j = 0; for (let i = 0; i < vs.length; i++) { while (vs[i] - vs[j] > L) j++; if (i - j + 1 > best) best = i - j + 1; } return best; }
const mk = () => ({ b: new Int32Array(NW), R: new Int32Array(NW) });
const F1 = mk(), F2 = mk(), F3e = mk(), F3o = mk();
function upd(T, R, vs, Lmul) {
  for (let k = 0; k < NW; k++) { const w = WMIN + k, L = Lmul === 'half' ? 2 * (w - 1) : (w - 1);
    const c = stripMax(vs, L); if (c > T.b[k]) { T.b[k] = c; T.R[k] = R; } } }
for (let R = 2; R <= RMAX; R += 4) if (r2c[R] >= 8) upd(F1, R, multF1(R), 'half');
for (let R = 1; R <= RMAX; R++) if (r2c[R] >= 8) upd(F2, R, multF2(R), 'int');
for (let R = 1; R <= RMAX; R += 2) if (r2c[R] >= 16) { const [ve, vo] = multF3(R); upd(F3e, R, ve, 'half'); upd(F3o, R, vo, 'half'); }
const known = { 6: 8, 7: 10, 8: 12, 9: 12, 10: 12, 11: 14, 12: 16, 13: 16, 14: 16, 15: 16, 16: 16, 17: 16, 18: 16,
  22: 18, 23: 20, 24: 20, 25: 22, 26: 24, 27: 24, 28: 24, 29: 24, 30: 24, 31: 24, 32: 24, 33: 24, 34: 24, 35: 24 };
const perW = [];
for (let k = 0; k < NW; k++) {
  const w = WMIN + k;
  const fams = [['F1', F1.b[k], F1.R[k]], ['F2', F2.b[k], F2.R[k]], ['F3e', F3e.b[k], F3e.R[k]], ['F3o', F3o.b[k], F3o.R[k]]];
  let bm = fams[0]; for (const f of fams) if (f[1] > bm[1]) bm = f;
  perW.push({ w, max: bm[1], fam: bm[0], R: bm[2], F1: F1.b[k], F2: F2.b[k], F3e: F3e.b[k], F3o: F3o.b[k],
    known: known[w] ?? null, agree: known[w] === undefined ? null : bm[1] === known[w] });
}
function verify2210(w) {
  const R = 2210;
  const sols = [];
  for (let u = -Math.floor(Math.sqrt(R)); u <= Math.floor(Math.sqrt(R)); u++) { const v = isSq(R - u * u); if (v >= 0) { sols.push([u, v]); if (v > 0) sols.push([u, -v]); } }
  let best = { c: 0, A: 0, pts: [] };
  for (let A = 1; A <= 200; A += 2) { const lo = -A, hi = -A + 2 * (w - 1);
    const pts = sols.filter(([u]) => u >= lo && u <= hi); if (pts.length > best.c) best = { c: pts.length, A, pts }; }
  const minv = Math.min(...best.pts.map(p => p[1])), B = -minv;
  const bpts = best.pts.map(([u, v]) => [(u + best.A) / 2, (v + B) / 2]);
  const m = Math.max(...bpts.map(p => p[1])) + 1;
  const onCircle = bpts.every(([x, y]) => (2 * x - best.A) ** 2 + (2 * y - B) ** 2 === R);
  const inBoard = bpts.every(([x, y]) => x >= 0 && x < w && y >= 0 && y < m);
  const distinct = new Set(bpts.map(p => p.join(','))).size === bpts.length;
  return { w, count: best.c, A: best.A, B, board: [w, m], onCircle, inBoard, distinct, ok: onCircle && inBoard && distinct };
}
const witnesses = [];
for (const w of [43, 44, 45, 46, 47, 48]) witnesses.push(verify2210(w));
console.log(JSON.stringify({ semantics: 'strip-window on constrained axis; free axis unbounded (m variable)', CMAX, WMIN, WMAX, perW, witnesses }, null, 1));
