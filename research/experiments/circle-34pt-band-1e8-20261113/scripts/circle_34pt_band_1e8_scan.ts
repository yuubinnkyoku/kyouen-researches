// circle_34pt_band_1e8_scan.ts — 2026-11-13 高速レーン
//
// 目的: (10^7,10^8] 34点帯掃引（K0791 レジューム項目1）と旧掃引の再検証。
// 1. 制御: R'=65 / 1105 / 5525 の既知窓計数（K0767/K0786/K0789/K0790/K0791 と完全一致を主張）。
// 2. 完全列挙: 1mod4-smooth R'<=1e8・prod(e_i+1)>=9 の全円を指数列（composition）ベースで
//    列挙する。旧 circle_34pt_witness_scan.ts の dfs は npf.push 蓄積で指数 e を
//    e(e+1)/2 に腐敗させるバグを持ち、prod と幾何が一致しない（実証: prod=5525 は
//    pf=[5^1,5^2,13^1,17^1]、すなわち 5^3*13*17=27625 の rep を受け取る）。
//    修正列挙は 11,711 タスク（(指数列,p1,p2)）・359,096 円（<=1e7 は 29,832 = 旧計数と一致）。
// 3. 幾何: 旧スキャン verbatim の repsOf/rowsFor/winTable（3原始実現 oo/it/mx）。
//    rowsForB(bug=true) は本実験セッションで一度混入した -d 多重度4バグを再現し、
//    「膨張表 >= 正表」の保守的上界として事前フィルタに使う。
// 4. 事前フィルタ: maxSpan(form, w=106) >= 26（膨張表）。窓計数は幅単調なので
//    34点達成円（w∈[49,106]）は必ず通る。通過円のみ正表を計算する。
// 5. 出力: 通過円の正表・34点達成円・minW34。
//
// 実行: main() 単独（制御+列挙計数）。sweep(START,END) でバッチ掃引（冪等・決定的）。
// LEAF_BUDGET は1呼び出しの処理円数上限（sandbox 時間予算に合わせ 33,000 前後）。

function reprPrime(p: number): [number, number] {
  for (let a = Math.floor(Math.sqrt(p / 2)); a >= 1; a--) {
    const b2 = p - a * a, b = Math.round(Math.sqrt(b2));
    if (b * b === p - a * a) return [Math.max(a, b), Math.min(a, b)];
  }
  throw new Error('no rep ' + p);
}
function repsOf(pf: [number, number][]): [number, number][] {
  const fs: { re: number, im: number }[][] = [];
  for (const [p, e] of pf) {
    const [a, b] = reprPrime(p); const o: { re: number, im: number }[] = [];
    for (let j = 0; j <= e; j++) {
      let re = 1, im = 0;
      for (let t = 0; t < j; t++) { const nr = re * a - im * b, ni = re * b + im * a; re = nr; im = ni; }
      for (let t = 0; t < e - j; t++) { const nr = re * a + im * b, ni = -re * b + im * a; re = nr; im = ni; }
      o.push({ re, im });
    }
    fs.push(o);
  }
  const out = new Set<string>();
  (function rec(i: number, re: number, im: number) {
    if (i === fs.length) { const X = Math.abs(re), Y = Math.abs(im); out.add(Math.max(X, Y) + ',' + Math.min(X, Y)); return; }
    for (const f of fs[i]) rec(i + 1, re * f.re - im * f.im, re * f.im + im * f.re);
  })(0, 1, 0);
  return [...out].map(s => { const [a, b] = s.split(',').map(Number); return [a, b] as [number, number]; });
}
// 3原始実現の行多重集合（bug=false が正。bug=true は -d 多重度4の監査用膨張版）
function rowsForB(qr: [number, number][], bug: boolean) {
  const mk = () => new Map<number, number>(); const oo = mk(), it = mk(), mx = mk();
  const add = (m: Map<number, number>, k: number, v: number) => m.set(k, (m.get(k) || 0) + v);
  for (const [X, Y] of qr) {
    if (Y === 0) { add(oo, X, 2); add(oo, -X, 2); add(it, 0, 2); add(mx, 0, 2); continue; }
    const s = X + Y, d = X - Y;
    add(oo, s, 2); add(oo, -s, 2); add(oo, d, 2); add(oo, -d, bug ? 4 : 2);
    add(it, Y * 2, 2); add(it, -Y * 2, 2); add(it, X * 2, 2); add(it, -X * 2, 2);
    const ev = (X % 2 === 0) ? X : Y; add(mx, ev, 2); add(mx, -ev, 2);
  }
  return [oo, it, mx] as const;
}
function wSpan(m: Map<number, number>, w: number) {
  const pos = [...m.keys()].sort((a, b) => a - b); const n = pos.length;
  const pref = new Array(n + 1); pref[0] = 0;
  for (let i = 0; i < n; i++) pref[i + 1] = pref[i] + (m.get(pos[i]) || 0);
  const span = 2 * (w - 1); let best = 0, e = 0;
  for (let i = 0; i < n; i++) {
    if (e < i) e = i; const target = pos[i] + span;
    while (e < n && pos[e] <= target) e++;
    const c = pref[e] - pref[i]; if (c > best) best = c;
  }
  return best;
}
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
// === 制御（旧スキャン exp 値・全て PASS を主張）===
function controls() {
  const wsC: number[] = []; for (let w = 6; w <= 110; w++) wsC.push(w);
  const at = (a: number[], w: number) => a[wsC.indexOf(w)];
  const c65 = winTable(rowsForB(repsOf([[5, 1], [13, 1]]), false)[0], wsC);
  const c1105 = winTable(rowsForB(repsOf([[5, 1], [13, 1], [17, 1]]), false)[0], wsC);
  const c5525 = winTable(rowsForB(repsOf([[5, 2], [13, 1], [17, 1]]), false)[0], wsC);
  return {
    c65: [at(c65, 11) === 14, at(c65, 12) === 16, at(c65, 17) === 16, at(c65, 21) === 16].every(Boolean),
    c1105: [43, 44, 45, 46, 47, 48, 49].map((w, i) => at(c1105, w) === [26, 28, 28, 30, 30, 32, 32][i]).every(Boolean),
    c5525: [49, 50, 51, 55, 56, 63, 64, 75, 76, 77, 78, 82, 83, 86, 87, 93, 94, 95, 96, 99, 100, 101, 104, 105, 106].every(
      (w, i) => at(c5525, w) === [22, 22, 24, 24, 26, 26, 28, 28, 30, 30, 32, 32, 34, 34, 36, 36, 38, 38, 40, 40, 42, 44, 44, 46, 48][i]),
  };
}
// === タスク列構築（決定的順序）===
function buildTasks(B: number) {
  const ps = sieve1mod4(320000);
  function mv(s: number[]) {
    const sd = s.slice().sort((a, b) => b - a); let v = 1;
    for (let i = 0; i < sd.length; i++) for (let t = 0; t < sd[i]; t++) { v *= ps[i]; if (v > B) return v; }
    return v;
  }
  const as: number[][] = [], s0: number[] = [];
  (function g(k: number, r: number) {
    if (k > 0) { const pr = s0.slice(0, k).reduce((a, e) => a * (e + 1), 1); if (pr >= 9 && mv(s0.slice(0, k)) <= B) as.push(s0.slice(0, k)); }
    if (k >= 6) return;
    for (let e = 1; e <= r; e++) { s0[k] = e; g(k + 1, r - e); }
  })(0, 11);
  type T = { s: number[], j: number, j2: number }; const tk: T[] = [];
  for (const s of as) {
    const L = s.length, e0 = s[0];
    for (let j = 0; j < ps.length; j++) {
      const p1 = ps[j]; let v = 1, ok = 1;
      for (let t = 0; t < e0; t++) { v *= p1; if (v > B) { ok = 0; break; } }
      if (!ok) break;
      if (L === 1) { tk.push({ s, j, j2: -1 }); continue; }
      if (j + 1 < ps.length && v * ps[j + 1] > B) break;
      const e1 = s[1];
      for (let j2 = j + 1; j2 < ps.length; j2++) {
        const p2 = ps[j2]; let v2 = v, ok2 = 1;
        for (let t = 0; t < e1; t++) { v2 *= p2; if (v2 > B) { ok2 = 0; break; } }
        if (!ok2) break;
        if (L === 2) { tk.push({ s, j, j2 }); continue; }
        let m2 = v2, ok3 = 1;
        for (let lv = 2; lv < L; lv++) {
          const pj = ps[Math.min(j2 + 1 + (lv - 2), ps.length - 1)];
          for (let t = 0; t < s[lv]; t++) { m2 *= pj; if (m2 > B) { ok3 = 0; break; } }
          if (!ok3) break;
        }
        if (ok3) tk.push({ s, j, j2 });
      }
    }
  }
  return { ps, tk };
}
// === 掃引バッチ（START..END・冪等）===
function sweep(START: number, END: number) {
  const B = 1e8, OLD = 1e7, LEAF_BUDGET = 33000;
  const { ps, tk } = buildTasks(B);
  const band: number[] = []; for (let w = 49; w <= 106; w++) band.push(w);
  let po = 0, pn = 0, ld = 0, nB26 = 0;
  const pas: any[] = []; const pf: [number, number][] = [];
  function process(R: number) {
    if (R <= OLD) po++; else pn++;
    const qr = repsOf(pf); const fb = rowsForB(qr, true);
    let mcB = 0; for (let f = 0; f < 3; f++) { const c = wSpan(fb[f], 106); if (c > mcB) mcB = c; }
    if (mcB < 26) return; nB26++;
    const fc = rowsForB(qr, false); const nm = ['oo', 'it', 'mx'];
    for (let f = 0; f < 3; f++) {
      const t = winTable(fc[f], band);
      pas.push({ R, form: nm[f], pf: pf.map(x => x.join('^')).join('*'), mx: Math.max(...t), t });
    }
  }
  function rt(t: { s: number[], j: number, j2: number }): number {
    const s = t.s, L = s.length; let lv2 = 0; pf.length = L;
    const e0 = s[0], p1 = ps[t.j]; let v0 = 1; for (let q = 0; q < e0; q++) v0 *= p1; pf[0] = [p1, e0];
    if (L === 1) { process(v0); return 1; }
    const e1 = s[1], p2 = ps[t.j2]; let v1 = v0; for (let q = 0; q < e1; q++) v1 *= p2; pf[1] = [p2, e1];
    (function asg(l: number, ix: number, v: number) {
      if (l === L) { lv2++; process(v); return; }
      const e = s[l];
      for (let j = ix; j < ps.length; j++) {
        const p = ps[j]; let q = v, ok = 1;
        for (let t2 = 0; t2 < e; t2++) { q *= p; if (q > B) { ok = 0; break; } }
        if (!ok) break; pf[l] = [p, e]; asg(l + 1, j + 1, q);
      }
    })(2, t.j2 + 1, v1);
    return lv2;
  }
  let ti = START;
  for (; ti < Math.min(END, tk.length); ti++) { if (ld >= LEAF_BUDGET) break; ld += rt(tk[ti]); }
  return { start: START, next: ti, ld, po, pn, nB26, pas };
}
function main() {
  const ctl = controls();
  const { tk } = buildTasks(1e8);
  return { controls: ctl, tasks: tk.length, note: 'sweep(START,END) でバッチ掃引。LEAF_BUDGET=33000 で全 359,096 円を約11バッチ' };
}
