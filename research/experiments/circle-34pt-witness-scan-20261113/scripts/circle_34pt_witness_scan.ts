// circle_34pt_witness_scan.ts — 2026-11-13 高速レーン
//
// 目的: 34点以上の円 witness の検証と掃引（w=56..106帯）。
// 1. 円 (2x-105)^2+(2y-105)^2=11050（R'=5525=5^2·13·17 の奇奇実現）の全48点と
//    per-window 計数を厳密整数演算で検証（K0785 下界の独立確認）。
// 2. 3原始実現（奇奇 R=2R' / 整数中心 R=R' / 混合パリティ R=R'・A奇B偶）の全てで
//    1mod4-smooth R'<=1e7・r2>=36 の全円を掃引し、34点帯の最良 witness を特定。
// 3. R'>1e7 の高表現円（r2<=256）の的を絞った確認。
// 制御: R'=65（130円）・R'=1105（2210円）の既知 per-w 計数と完全一致を主張。
// 単独実行: sandbox の run_typescript で main() を直接呼ぶ構造（依存なし・決定的）。

function reprPrime(p: number): [number, number] {
  for (let a = Math.floor(Math.sqrt(p / 2)); a >= 1; a--) {
    const b2 = p - a * a, b = Math.round(Math.sqrt(b2));
    if (b * b === p - a * a) return [Math.max(a, b), Math.min(a, b)];
  }
  throw new Error('no rep ' + p);
}
// R'（奇・1mod4-smooth）の象限 rep (X,Y) X>=Y>=0 をガウス整数結合で全列挙
function repsOf(pf: [number, number][]): [number, number][] {
  const factors: { re: number, im: number }[][] = [];
  for (const [p, e] of pf) {
    const [a, b] = reprPrime(p); const opts: { re: number, im: number }[] = [];
    for (let j = 0; j <= e; j++) {
      let re = 1, im = 0;
      for (let t = 0; t < j; t++) { const nr = re * a - im * b, ni = re * b + im * a; re = nr; im = ni; }
      for (let t = 0; t < e - j; t++) { const nr = re * a + im * b, ni = -re * b + im * a; re = nr; im = ni; }
      opts.push({ re, im });
    }
    factors.push(opts);
  }
  const out = new Set<string>();
  (function rec(i: number, re: number, im: number) {
    if (i === factors.length) { const X = Math.abs(re), Y = Math.abs(im); out.add(Math.max(X, Y) + ',' + Math.min(X, Y)); return; }
    for (const f of factors[i]) rec(i + 1, re * f.re - im * f.im, re * f.im + im * f.re);
  })(0, 1, 0);
  return [...out].map(s => { const [a, b] = s.split(',').map(Number); return [a, b] as [number, number]; });
}
// 3実現の行多重集合（位置は2倍座標・両側込み）。行=窓方向の格子行、点数/行を保持。
function rowsFor(qr: [number, number][]) {
  const mk = () => new Map<number, number>(); const oo = mk(), it = mk(), mx = mk();
  const add = (m: Map<number, number>, k: number, v: number) => m.set(k, (m.get(k) || 0) + v);
  for (const [X, Y] of qr) {
    if (Y === 0) { add(oo, X, 2); add(oo, -X, 2); add(it, 0, 2); add(mx, 0, 2); continue; }
    const s = X + Y, d = X - Y;
    add(oo, s, 2); add(oo, -s, 2); add(oo, d, 2); add(oo, -d, 2);
    add(it, Y * 2, 2); add(it, -Y * 2, 2); add(it, X * 2, 2); add(it, -X * 2, 2);
    const ev = (X % 2 === 0) ? X : Y; add(mx, ev, 2); add(mx, -ev, 2);
  }
  return [oo, it, mx] as const;
}
// 幅wの窓（2倍座標で範囲 2(w-1)）の最大点数。窓左端は行位置に合わせて滑らせる（完全）
function winTable(m: Map<number, number>, ws: number[]) {
  const pos = [...m.keys()].sort((a, b) => a - b); const n = pos.length;
  const pref = new Array(n + 1); pref[0] = 0;
  for (let i = 0; i < n; i++) pref[i + 1] = pref[i] + (m.get(pos[i]) || 0);
  return ws.map(w => {
    const span = 2 * (w - 1); let best = 0, e = 0;
    for (let i = 0; i < n; i++) {
      if (e < i) e = i; const target = pos[i] + span;
      while (e < n && pos[e] <= target) e++;
      const c = pref[e] - pref[i]; if (c > best) best = c;
    }
    return best;
  });
}
function sieve1mod4(limit: number) {
  const ps: number[] = []; const isC = new Uint8Array(limit + 1);
  for (let n = 3; n <= limit; n += 2) if (!isC[n]) { for (let m = n * n; m <= limit; m += n) isC[m] = 1; if (n % 4 === 1) ps.push(n); }
  return ps;
}
function tab(R: number, pf: [number, number][], ws: number[]) {
  const qr = repsOf(pf); const forms = rowsFor(qr); const names = ['oo', 'it', 'mx'];
  const t: Record<string, number[]> = {};
  for (let f = 0; f < 3; f++) t[names[f]] = winTable(forms[f], ws);
  return { R, nQuad: qr.length, r2: qr.length * 8, ...t };
}
async function main() {
  const ws: number[] = []; for (let w = 6; w <= 110; w++) ws.push(w);
  const at = (arr: number[], w: number) => arr[ws.indexOf(w)];
  // --- 制御1: R'=65 → 円(2x-11)^2+(2y-11)^2=130（K0767/K0789 witness） ---
  const c65 = tab(65, [[5, 1], [13, 1]], ws);
  const ctl65 = [at(c65.oo, 11) === 14, at(c65.oo, 12) === 16, at(c65.oo, 17) === 16, at(c65.oo, 21) === 16];
  // --- 制御2: R'=1105 → 2210円（K0786/K0790 witness・per-w 26/28/28/30/30/32..） ---
  const c1105 = tab(1105, [[5, 1], [13, 1], [17, 1]], ws);
  const ctl1105 = [43, 44, 45, 46, 47, 48, 49, 55].map((w, i) =>
    at(c1105.oo, w) === [26, 28, 28, 30, 30, 32, 32, 32][i]);
  // --- 制御3: R'=5525 → 11050円奇奇実現（本マシンの検証対象・K0785下界） ---
  const c5525 = tab(5525, [[5, 2], [13, 1], [17, 1]], ws);
  const exp5525: Record<number, number> = { 49: 22, 50: 22, 51: 24, 55: 24, 56: 26, 63: 26, 64: 28, 75: 28, 76: 30, 77: 30, 78: 32, 82: 32, 83: 34, 86: 34, 87: 36, 93: 36, 94: 38, 95: 38, 96: 40, 99: 40, 100: 42, 101: 44, 104: 44, 105: 46, 106: 48 };
  const ctl5525 = Object.keys(exp5525).every(k => at(c5525.oo, +k) === exp5525[+k]);
  const allCtl = [...ctl65, ...ctl1105, ctl5525].every(Boolean);
  // --- 独立経路: 11050円の点を直接 u掃引で列挙（ガウス結合と独立） ---
  const pts: number[] = []; const rows5525 = new Map<number, number>();
  for (let u = 1; u * u <= 11050; u += 2) {
    const v2 = 11050 - u * u, v = Math.round(Math.sqrt(v2));
    if (v * v === v2) { pts.push(u * u + v2 === 11050 ? 4 : 0);
      for (const s of [v, -v]) rows5525.set(s, (rows5525.get(s) || 0) + 2); }
  }
  const direct48 = [...rows5525.values()].reduce((a, b) => a + b, 0) === 48 && rows5525.size === 24;
  // --- 掃引: 1mod4-smooth R'<=1e7, prod(e+1)>=9（r2>=36）, 3実現すべて ---
  const ps = sieve1mod4(320000);
  const band: number[] = []; for (let w = 56; w <= 106; w++) band.push(w);
  const bIdx = band.map(w => ws.indexOf(w));
  const bestPts = new Array(band.length).fill(0); const bestWit = new Array(band.length).fill('');
  const process = (R: number, pf: [number, number][]) => {
    const qr = repsOf(pf); const forms = rowsFor(qr); const names = ['oo', 'it', 'mx'];
    for (let f = 0; f < 3; f++) { const t = winTable(forms[f], band);
      for (let i = 0; i < band.length; i++) if (t[i] > bestPts[i]) { bestPts[i] = t[i]; bestWit[i] = R + '-' + names[f]; } }
  };
  let processed = 0;
  const B = 1e7;
  (function dfs(i: number, prod: number, pe: number, pf: [number, number][]) {
    if (pe >= 9) { process(prod, pf); processed++; }
    for (let j = i; j < ps.length; j++) { const p = ps[j]; if (prod * p > B) break;
      let q = prod * p; let e = 1; const npf = pf.slice();
      while (q <= B) { npf.push([p, e]); dfs(j + 1, q, pe * (e + 1), npf.slice()); q *= p; e++; }
    }
  })(0, 1, 1, []);
  // --- 的を絞った大円（R'>1e7, 高r2） ---
  const big: any[] = [];
  const cand: [number, [number, number][]][] = [
    [48612265, [[5, 1], [13, 1], [17, 1], [29, 1], [37, 1], [41, 1]]],
    [6569225, [[5, 2], [13, 1], [17, 1], [29, 1], [41, 1]]],
    [8381425, [[5, 2], [13, 1], [17, 1], [37, 1], [41, 1]]],
    [17079985, [[5, 1], [13, 2], [17, 1], [29, 1], [41, 1]]],
    [35409725, [[5, 2], [13, 2], [17, 2], [29, 1]]],
    [29641625, [[5, 3], [13, 2], [17, 1], [29, 1]]],
    [62840245, [[5, 1], [13, 1], [17, 1], [29, 1], [41, 1], [53, 1]]],
  ];
  for (const [R, pf] of cand) { const t = tab(R, pf, band);
    big.push({ R, r2: t.r2, maxBand: Math.max(...t.oo, ...t.it, ...t.mx) }); }
  const minWfor = (pts: number) => { for (let i = 0; i < band.length; i++) if (bestPts[i] >= pts) return band[i]; return -1; };
  return {
    controls: { allPass: allCtl && direct48, c65: [11, 12, 17, 21].map(w => at(c65.oo, w)), c1105_oo_43to49: [43, 44, 45, 46, 47, 48, 49].map(w => at(c1105.oo, w)), direct_11050: { rows: rows5525.size, pts: 48 } },
    witness_5525_oo: { w49_110: ws.slice(48, 110).map((w, i) => ({ w, pts: c5525.oo[i + 48] })), w49_110_it: ws.slice(48, 110).map((w, i) => ({ w, pts: c5525.it[i + 48] })) },
    scan1e7: { processed, minW34: minWfor(34), minW36: minWfor(36), minW38: minWfor(38), minW40: minWfor(40), best: band.map((w, i) => ({ w, pts: bestPts[i], wit: bestWit[i] })) },
    bigCircles: big,
  };
}
