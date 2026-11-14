// width85_realizability_scan.mjs — 2026-11-14 高速レーン（w=84 正制御・実在性スキャン）
// width83_realizability_scan.ts（K0807・repo掲載）の w=84 版。
// 1. 4生残17行パターンのREST16再検査（16法の各法で共通証明書が空でないこと）。
// 2. 11050円の4窓（x∈[-1,82],[0,83],[22,105],[23,106]）が各パターンを実現することの直接検証。
// 3. 有限実在スキャン: R'<=1e6・1mod4-smooth・prod(e+1)>=9 の全円・3実現形・84幅窓全位置で
//    17行以上の窓を行集合が4生残パターンのいずれかと一致するか（孤立性）。
const W = 85, ROWMAX = W - 1;
const PATS = {
  p456:  [0,5,7,19,27,32,40,52,54,59,63,70,73,76,77,81,82],
  p2696: [2,3,7,8,11,14,21,25,30,32,44,52,57,65,77,79,84],
  p3052: [2,7,9,21,29,34,42,54,56,61,65,72,75,78,79,83,84],
  p1909: [1,6,8,20,28,33,41,53,55,60,64,71,74,77,78,82,83],
  p2612: [1,2,6,7,10,13,20,24,29,31,43,51,56,64,76,78,83],
  p3119: [0,1,5,6,9,12,19,23,28,30,42,50,55,63,75,77,82],
};
const patKeys = Object.keys(PATS);
const REST16 = [19, 23, 7, 5, 27, 43, 47, 13, 17, 8, 16, 25, 29, 31, 37, 41];
const qrC = {};
const getQR = (m) => { if (!qrC[m]) { const s = new Uint8Array(m); for (let x = 0; x < m; x++) s[(x * x) % m] = 1; qrC[m] = s; } return qrC[m]; };
function rowMaskFor(m, i) {
  const qr = getQR(m); const s = new Set();
  const ii4 = (4 * i * i) % m;
  for (let a = 0; a < m; a++) { const am = a - ii4; for (let u = 0; u < m; u++) { let t = (am - u * i) % m; if (t < 0) t += m; if (qr[t]) s.add(a * m + u); } }
  return s;
}
function rest16Check(pat) {
  const per = {}; let allPass = true;
  for (const m of REST16) {
    const masks = pat.map(i => rowMaskFor(m, i));
    let cnt = 0;
    for (const b of masks[0]) { let ok = true; for (let k = 1; k < masks.length; k++) if (!masks[k].has(b)) { ok = false; break; } if (ok) cnt++; }
    per[m] = cnt; if (cnt === 0) allPass = false;
  }
  return { allPass, perModulus: per };
}
function witnessCheck(windowX, pat) {
  const pts = [];
  for (let x = -15; x <= 120; x++) for (let y = -15; y <= 120; y++)
    if ((2 * x - 105) ** 2 + (2 * y - 105) ** 2 === 11050) pts.push([x, y]);
  const inW = pts.filter(p => p[0] >= windowX[0] && p[0] <= windowX[1]);
  const rows = [...new Set(inW.map(p => p[0] - windowX[0]))].sort((a, b) => a - b);
  return { points: inW.length, nRows: rows.length, equalsPattern: JSON.stringify(rows) === JSON.stringify(pat) };
}
function reprPrime(p) {
  for (let a = Math.floor(Math.sqrt(p / 2)); a >= 1; a--) { const b2 = p - a * a, b = Math.round(Math.sqrt(b2)); if (b * b === p - a * a) return [Math.max(a, b), Math.min(a, b)]; }
  throw new Error('no rep');
}
function repsOf(pf) {
  const factors = [];
  for (const [p, e] of pf) {
    const [a, b] = reprPrime(p); const opts = [];
    for (let j = 0; j <= e; j++) { let re = 1, im = 0; for (let t = 0; t < j; t++) { const nr = re * a - im * b, ni = re * b + im * a; re = nr; im = ni; } for (let t = 0; t < e - j; t++) { const nr = re * a + im * b, ni = -re * b + im * a; re = nr; im = ni; } opts.push({ re, im }); }
    factors.push(opts);
  }
  const out = new Set();
  (function rec(i, re, im) {
    if (i === factors.length) { const X = Math.abs(re), Y = Math.abs(im); out.add(Math.max(X, Y) + ',' + Math.min(X, Y)); return; }
    for (const f of factors[i]) rec(i + 1, re * f.re - im * f.im, re * f.im + im * f.re);
  })(0, 1, 0);
  return [...out].map(s => { const [a, b] = s.split(',').map(Number); return [a, b]; });
}
function rowsFor(qr) {
  const mk = () => new Map(); const oo = mk(), it = mk(), mx = mk();
  const add = (m, k, v) => m.set(k, (m.get(k) || 0) + v);
  for (const [X, Y] of qr) {
    if (Y === 0) { add(oo, X, 2); add(oo, -X, 2); add(it, 0, 2); add(mx, 0, 2); continue; }
    add(oo, X + Y, 2); add(oo, -(X + Y), 2); add(oo, X - Y, 2); add(oo, -(X - Y), 2);
    add(it, Y * 2, 2); add(it, -Y * 2, 2); add(it, X * 2, 2); add(it, -X * 2, 2);
    const ev = (X % 2 === 0) ? X : Y; add(mx, ev, 2); add(mx, -ev, 2);
  }
  return [oo, it, mx];
}
const patSets = {}; for (const k of patKeys) patSets[k] = new Set(PATS[k]);
function check(m) {
  const keys = [...m.keys()].sort((a, b) => a - b);
  const hits = [];
  for (let i = 0; i < keys.length; i++) {
    const L = keys[i];
    const rel = keys.map(k => (k - L) / 2).filter(r => r >= 0 && r <= ROWMAX);
    if (rel.length < 17) continue;
    const rs = new Set(rel);
    for (const k of patKeys) {
      const ps = patSets[k];
      if (rs.size !== ps.size) continue;
      let eq = true; for (const r of rs) if (!ps.has(r)) { eq = false; break; }
      if (eq) { const pts = rel.reduce((s, r) => s + (m.get(L + 2 * r) || 0), 0); hits.push({ L, pat: k, rows: rel.length, pts }); }
    }
  }
  return hits;
}
function test(R, pf, tag, results) {
  const qr = repsOf(pf); const forms = rowsFor(qr); const names = ['oo', 'it', 'mx'];
  for (let f = 0; f < 3; f++) {
    const h = check(forms[f]);
    for (const x of h) results.push({ R, tag, form: names[f], hit: x });
  }
}
const results = [];
test(5525, [[5, 2], [13, 1], [17, 1]], 'control-11050', results);
const ps = []; const LIMIT = 1000; const isC = new Uint8Array(LIMIT + 1);
for (let n = 3; n <= LIMIT; n += 2) if (!isC[n]) { for (let m2 = n * n; m2 <= LIMIT; m2 += n) isC[m2] = 1; if (n % 4 === 1) ps.push(n); }
let cnt = 0;
(function dfs(i, prod, pe, pf) {
  if (pe >= 9) { test(prod, pf, 'scan', results); cnt++; }
  for (let j = i; j < ps.length; j++) { const p = ps[j]; if (prod * p > 1e6) break;
    let q = prod * p; let e = 1; const npf = pf.slice();
    while (q <= 1e6) { npf.push([p, e]); dfs(j + 1, q, pe * (e + 1), npf.slice()); q *= p; e++; }
  }
})(0, 1, 1, []);
const rest16 = {}; for (const k of patKeys) rest16[k] = rest16Check(PATS[k]);
const witness = {
  p456:  witnessCheck([23, 106], PATS.p456),
  p1909: witnessCheck([22, 105], PATS.p1909),
  p2696: witnessCheck([-2, 82], PATS.p2696),
  p3052: witnessCheck([21, 105], PATS.p3052),
  p2612: witnessCheck([-1, 82], PATS.p2612),
  p3119: witnessCheck([0, 83], PATS.p3119),
};
console.log(JSON.stringify({ w: W, rest16, witness, scan1e6: { processed: cnt, results } }, null, 1));
