// width83_realizability_scan.ts — 2026-11-14 高速レーン（K0807・実在性スキャン）
//
// 目的: w=83 の REST6 生残17行パターン2件（mask 3119・456 の leaf）の実在性判定。
//   1. 両パターンの REST16 再検査（16法 [19,23,7,5,27,43,47,13,17,8,16,25,29,31,37,41]
//      の各法で17行の共通証明書が空でないこと・phase 2 相当）。
//   2. 11050 円（(2x-105)^2+(2y-105)^2=11050・48点・K0785 witness）が両パターンを
//      2つの83幅窓で実現することの直接検証（点数・行集合がパターンと完全一致）。
//   3. 有限実在スキャン: R' <= 1e6 の 1mod4-smooth・prod(e+1)>=9 の全円（1,964個）・
//      3実現形（奇奇/整数中心/混合パリティ）・83幅窓の全位置で、行support が
//      mask 456/3119 に収まるか（>=17行）。結果: この2 mask を実現するのは
//      R'=5525（11050円）のみ（制御込み）。
// 単独実行: sandbox run_typescript で main() を直接呼ぶ構造（決定的・依存なし）。

// mask 行集合（幅83・行0..82・K0804機の maximal mask 456/3119）
const M3119 = new Set([0,1,5,6,9,12,19,23,27,28,30,33,39,41,42,45,50,55,60,63,64,66,72,75,77,78,82]);
const M456 = new Set([0,4,5,7,10,16,18,19,22,27,32,37,40,41,43,49,52,54,55,59,63,70,73,76,77,81,82]);
const W = 83, SPAN = 2 * (W - 1);
// 生残17行パターン（state_w83.json の leaves=2 の中身・probe で抽出）
const PAT3119 = [0,1,5,6,9,12,19,23,28,30,42,50,55,63,75,77,82];
const PAT456 = [0,5,7,19,27,32,40,52,54,59,63,70,73,76,77,81,82];
const REST16 = [19, 23, 7, 5, 27, 43, 47, 13, 17, 8, 16, 25, 29, 31, 37, 41];
const qrC: Record<number, Uint8Array> = {};
const getQR = (m: number): Uint8Array => {
  if (!qrC[m]) { const s = new Uint8Array(m); for (let x = 0; x < m; x++) s[(x * x) % m] = 1; qrC[m] = s; }
  return qrC[m];
};
// --- 1. REST16 再検査 ---
function rowMaskFor(m: number, i: number) {
  const qr = getQR(m); const s = new Set<number>();
  const ii4 = (4 * i * i) % m;
  for (let a = 0; a < m; a++) { const am = a - ii4; for (let u = 0; u < m; u++) { let t = (am - u * i) % m; if (t < 0) t += m; if (qr[t]) s.add(a * m + u); } }
  return s;
}
function rest16Check(pat: number[]) {
  const per: Record<string, number> = {};
  let allPass = true;
  for (const m of REST16) {
    const masks = pat.map(i => rowMaskFor(m, i));
    let cnt = 0;
    for (const b of masks[0]) { let ok = true; for (let k = 1; k < masks.length; k++) if (!masks[k].has(b)) { ok = false; break; } if (ok) cnt++; }
    per[m] = cnt; if (cnt === 0) allPass = false;
  }
  return { allPass, perModulus: per };
}
// --- 2. 11050円の直接検証 ---
function witnessCheck(windowX: [number, number], pat: number[]) {
  const pts: [number, number][] = [];
  for (let x = -10; x <= 115; x++) for (let y = -10; y <= 115; y++) {
    if ((2 * x - 105) ** 2 + (2 * y - 105) ** 2 === 11050) pts.push([x, y]);
  }
  const inW = pts.filter(p => p[0] >= windowX[0] && p[0] <= windowX[1]);
  const rows = [...new Set(inW.map(p => p[0] - windowX[0]))].sort((a, b) => a - b);
  return { points: inW.length, nRows: rows.length, rows, equalsPattern: JSON.stringify(rows) === JSON.stringify(pat) };
}
// --- 3. 有限実在スキャン（R'<=1e6・prod(e+1)>=9・3実現形） ---
function reprPrime(p: number): [number, number] {
  for (let a = Math.floor(Math.sqrt(p / 2)); a >= 1; a--) { const b2 = p - a * a, b = Math.round(Math.sqrt(b2)); if (b * b === p - a * a) return [Math.max(a, b), Math.min(a, b)]; }
  throw new Error('no rep');
}
function repsOf(pf: [number, number][]): [number, number][] {
  const factors: { re: number, im: number }[][] = [];
  for (const [p, e] of pf) {
    const [a, b] = reprPrime(p); const opts: { re: number, im: number }[] = [];
    for (let j = 0; j <= e; j++) { let re = 1, im = 0; for (let t = 0; t < j; t++) { const nr = re * a - im * b, ni = re * b + im * a; re = nr; im = ni; } for (let t = 0; t < e - j; t++) { const nr = re * a + im * b, ni = -re * b + im * a; re = nr; im = ni; } opts.push({ re, im }); }
    factors.push(opts);
  }
  const out = new Set<string>();
  (function rec(i: number, re: number, im: number) {
    if (i === factors.length) { const X = Math.abs(re), Y = Math.abs(im); out.add(Math.max(X, Y) + ',' + Math.min(X, Y)); return; }
    for (const f of factors[i]) rec(i + 1, re * f.re - im * f.im, re * f.im + im * f.re);
  })(0, 1, 0);
  return [...out].map(s => { const [a, b] = s.split(',').map(Number); return [a, b] as [number, number]; });
}
function rowsFor(qr: [number, number][]): Map<number, number>[] {
  const mk = () => new Map<number, number>(); const oo = mk(), it = mk(), mx = mk();
  const add = (m: Map<number, number>, k: number, v: number) => m.set(k, (m.get(k) || 0) + v);
  for (const [X, Y] of qr) {
    if (Y === 0) { add(oo, X, 2); add(oo, -X, 2); add(it, 0, 2); add(mx, 0, 2); continue; }
    add(oo, X + Y, 2); add(oo, -(X + Y), 2); add(oo, X - Y, 2); add(oo, -(X - Y), 2);
    add(it, Y * 2, 2); add(it, -Y * 2, 2); add(it, X * 2, 2); add(it, -X * 2, 2);
    const ev = (X % 2 === 0) ? X : Y; add(mx, ev, 2); add(mx, -ev, 2);
  }
  return [oo, it, mx];
}
function check(m: Map<number, number>, mask: Set<number>) {
  const keys = [...m.keys()].sort((a, b) => a - b);
  const hits: { L: number, rows: number, pts: number }[] = [];
  for (let i = 0; i < keys.length; i++) {
    const L = keys[i];
    const rel = keys.map(k => (k - L) / 2).filter(r => r >= 0 && r <= 82);
    if (rel.length < 17) continue;
    let ok = true; for (const r of rel) if (!mask.has(r)) { ok = false; break; }
    if (ok) { const pts = rel.reduce((s, r) => s + (m.get(L + 2 * r) || 0), 0); hits.push({ L, rows: rel.length, pts }); }
  }
  return hits;
}
async function main() {
  const results: any[] = [];
  const test = (R: number, pf: [number, number][], tag: string) => {
    const qr = repsOf(pf); const forms = rowsFor(qr); const names = ['oo', 'it', 'mx'];
    for (let f = 0; f < 3; f++) {
      const h456 = check(forms[f], M456); const h3119 = check(forms[f], M3119);
      if (h456.length) results.push({ R, tag, form: names[f], mask: 456, hits: h456 });
      if (h3119.length) results.push({ R, tag, form: names[f], mask: 3119, hits: h3119 });
    }
  };
  test(5525, [[5, 2], [13, 1], [17, 1]], 'control-11050');
  const ps: number[] = []; const LIMIT = 1000; const isC = new Uint8Array(LIMIT + 1);
  for (let n = 3; n <= LIMIT; n += 2) if (!isC[n]) { for (let m2 = n * n; m2 <= LIMIT; m2 += n) isC[m2] = 1; if (n % 4 === 1) ps.push(n); }
  let cnt = 0;
  (function dfs(i: number, prod: number, pe: number, pf: [number, number][]) {
    if (pe >= 9) { test(prod, pf, 'scan'); cnt++; }
    for (let j = i; j < ps.length; j++) { const p = ps[j]; if (prod * p > 1e6) break;
      let q = prod * p; let e = 1; const npf = pf.slice();
      while (q <= 1e6) { npf.push([p, e]); dfs(j + 1, q, pe * (e + 1), npf.slice()); q *= p; e++; }
    }
  })(0, 1, 1, []);
  return {
    rest16: { pat3119: rest16Check(PAT3119), pat456: rest16Check(PAT456) },
    witness11050: { window_0_82: witnessCheck([0, 82], PAT3119), window_23_105: witnessCheck([23, 105], PAT456) },
    scan1e6: { processed: cnt, results },
  };
}
const _r = await main();
(console as any).log(JSON.stringify(_r, null, 1));
