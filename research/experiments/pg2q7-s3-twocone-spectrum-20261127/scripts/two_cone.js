// PG(2,q) s-parameter Kyouen game — complete Grundy spectrum via TWO-CONE double counting.
// Fresh implementation. Masks: two 32-bit words (lo: pts 0..31, hi: pts 32..63).
// s=3 two-cone identity: N_m(g)*C(m,3) = N3nc*D_m(g) + N3c*D'_m(g)   (proof in kit README)
'use strict';
const [,, qqArg, sArg, modeArg, fsetArg] = process.argv;
const q = parseInt(qqArg), s = parseInt(sArg);
const mode = modeArg || 'count';
const fset = parseInt(fsetArg || '0') % 3;

// ---- build PG(2,q) ----
const pts = [];
for (let y = 0; y < q; y++) for (let x = 0; x < q; x++) pts.push([x, y, 1]);
for (let m = 0; m < q; m++) pts.push([1, m, 0]);
pts.push([0, 1, 0]);
const n = pts.length;
const lines = [];
const lineKeys = new Set();
for (let a = 0; a < q; a++) for (let b = 0; b < q; b++) for (let c = 0; c < q; c++) {
  if (!a && !b && !c) continue;
  const fn = a ? 0 : (b ? 1 : 2);
  const lead = fn === 0 ? a : (fn === 1 ? b : c);
  let inv = -1;
  for (let t = 0; t < q; t++) if ((lead * t) % q === 1) { inv = t; break; }
  const na = (a * inv) % q, nb = (b * inv) % q, nc = (c * inv) % q;
  const key = na + ',' + nb + ',' + nc;
  if (lineKeys.has(key)) continue;
  lineKeys.add(key);
  let lo = 0, hi = 0;
  for (let i = 0; i < n; i++) {
    const d = (na * pts[i][0] + nb * pts[i][1] + nc * pts[i][2]) % q;
    if (d === 0) { if (i < 32) lo |= 1 << i; else hi |= 1 << (i - 32); }
  }
  lines.push({ lo, hi });
}
const nlines = lines.length;
const linesOfPt = Array.from({ length: n }, () => []);
lines.forEach((L, li) => {
  for (let i = 0; i < n; i++) {
    const bit = i < 32 ? (L.lo >>> i) & 1 : (L.hi >>> (i - 32)) & 1;
    if (bit) linesOfPt[i].push(li);
  }
});
for (const L of lines) { let c = 0; for (let i = 0; i < n; i++) c += (i < 32 ? (L.lo >>> i) & 1 : (L.hi >>> (i - 32)) & 1); if (c !== q + 1) throw new Error('line size'); }
for (let i = 0; i < n; i++) if (linesOfPt[i].length !== q + 1) throw new Error('lines per point');
for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
  let c = 0;
  for (const L of lines) {
    const bi = i < 32 ? (L.lo >>> i) & 1 : (L.hi >>> (i - 32)) & 1;
    const bj = j < 32 ? (L.lo >>> j) & 1 : (L.hi >>> (j - 32)) & 1;
    if (bi && bj) c++;
  }
  if (c !== 1) throw new Error('pair lines ' + c);
}

const pc16 = new Uint8Array(65536);
for (let i = 1; i < 65536; i++) pc16[i] = pc16[i >> 1] + (i & 1);
const pop = (x) => pc16[x & 65535] + pc16[(x >>> 16) & 65535];

function legalAdd(Slo, Shi, p) {
  const ls = linesOfPt[p];
  for (let k = 0; k < ls.length; k++) {
    const L = lines[ls[k]];
    if (pop(Slo & L.lo) + pop(Shi & L.hi) >= s) return false;
  }
  return true;
}

function mkMask(idxs) { let lo = 0, hi = 0; for (const i of idxs) { if (i < 32) lo |= 1 << i; else hi |= 1 << (i - 32); } return [lo, hi]; }

const FncCands = [mkMask([0, 1, q]), mkMask([0, 2, q + 1]), mkMask([1, 3, q + 2])];
const FcCands = [];
for (const L of lines) {
  const on = [];
  for (let i = 0; i < n && on.length < 3; i++) { const b = i < 32 ? (L.lo >>> i) & 1 : (L.hi >>> (i - 32)) & 1; if (b) on.push(i); }
  FcCands.push(mkMask(on));
  if (FcCands.length >= 3) break;
}
const contains = (L, idxs) => { for (const i of idxs) { const b = i < 32 ? (L.lo >>> i) & 1 : (L.hi >>> (i - 32)) & 1; if (!b) return false; } return true; };
function maskIdx(F) { const r = []; for (let i = 0; i < n; i++) { const b = i < 32 ? (F[0] >>> i) & 1 : (F[1] >>> (i - 32)) & 1; if (b) r.push(i); } return r; }
for (const F of FncCands) { const fi = maskIdx(F); let c = 0; for (const L of lines) if (contains(L, fi)) c++; if (c !== 0) throw new Error('Fnc collinear'); }
for (const F of FcCands) { const fi = maskIdx(F); let c = 0; for (const L of lines) if (contains(L, fi)) c++; if (c !== 1) throw new Error('Fc not collinear'); }

function runCone(F, full) {
  const [Flo, Fhi] = F;
  const layers = [];
  const sizesOnly = [];
  let nodes = 0;
  function ensure(d) { while (layers.length < d) { layers.push([]); sizesOnly.push(0); } }
  function rec(Slo, Shi, last, depth) {
    nodes++;
    ensure(depth);
    if (full) layers[depth - 1].push([Slo, Shi]); else sizesOnly[depth - 1]++;
    for (let p = last + 1; p < n; p++) {
      const inS = p < 32 ? (Slo >>> p) & 1 : (Shi >>> (p - 32)) & 1;
      if (inS) continue;
      if (!legalAdd(Slo, Shi, p)) continue;
      rec(p < 32 ? Slo | (1 << p) : Slo, p < 32 ? Shi : Shi | (1 << (p - 32)), p, depth + 1);
    }
  }
  rec(Flo, Fhi, -1, 3);
  if (full) return { layers, nodes };
  return { layers: sizesOnly.map(c => new Array(c).fill(0)), nodes, sizesOnly };
}

const Fnc = FncCands[fset], Fc = FcCands[fset];
const A = runCone(Fnc, mode === "full");
const B = runCone(Fc, mode === "full");

const coneSizes = (C) => (C.sizesOnly || C.layers.map(L => L.length)).join(',');
console.error(`board PG(2,${q}) points=${n} lines=${nlines} s=${s} fset=${fset}`);
console.error(`cone_noncoll nodes=${A.nodes} layers=[${coneSizes(A)}]`);
console.error(`cone_coll    nodes=${B.nodes} layers=[${coneSizes(B)}]`);

if (mode === 'count') { console.log(JSON.stringify({ board: `PG(2,${q})`, s, fset, nodes_noncoll: A.nodes, layers_noncoll: A.sizesOnly, nodes_coll: B.nodes, layers_coll: B.sizesOnly })); process.exit(0); }

// ---- grundy DP per cone ----
function grundyCone(C) {
  const layers = C.layers;
  const maxm = layers.length;
  const G = [], cnt = [], maximal = [];
  for (let m = maxm; m >= 3; m--) {
    const Lv = layers[m - 1];
    Lv.sort((a, b) => (a[0] - b[0]) || (a[1] - b[1]));
    const Gm = new Uint8Array(Lv.length);
    const cm = new Array(64).fill(0);
    let maxcnt = 0;
    const Lp = m < maxm ? layers[m] : null;
    const Gp = m < maxm ? G[m+1] : null;
    for (let i = 0; i < Lv.length; i++) {
      const Slo = Lv[i][0], Shi = Lv[i][1];
      const childv = new Uint8Array(64);
      let any = false;
      if (Lp) {
        for (let p = 0; p < n; p++) {
          const inS = p < 32 ? (Slo >>> p) & 1 : (Shi >>> (p - 32)) & 1;
          if (inS) continue;
          if (!legalAdd(Slo, Shi, p)) continue;
          const nlo = p < 32 ? Slo | (1 << p) : Slo;
          const nhi = p < 32 ? Shi : Shi | (1 << (p - 32));
          let lo2 = 0, hi2 = Lp.length - 1, found = -1;
          while (lo2 <= hi2) {
            const mid = (lo2 + hi2) >> 1;
            const e = Lp[mid];
            const cmp = (e[0] - nlo) || (e[1] - nhi);
            if (cmp === 0) { found = mid; break; }
            else if (cmp < 0) lo2 = mid + 1; else hi2 = mid - 1;
          }
          if (found < 0) { console.error('FATAL missing child'); process.exit(3); }
          childv[Gp[found]] = 1; any = true;
        }
      }
      let g = 0; while (childv[g]) g++;
      Gm[i] = g; cm[g]++;
      if (!any) maxcnt++;
    }
    G[m] = Gm; cnt[m] = cm; maximal[m] = maxcnt;
  }
  return { G, cnt, maximal, maxm };
}

const gA = grundyCone(A), gB = grundyCone(B);
const maxm = Math.max(gA.maxm, gB.maxm);

const binom = (nn, k) => { if (k < 0 || k > nn) return 0; let r = 1; for (let i = 1; i <= k; i++) { r = r * (nn - k + i) / i; } return Math.round(r); };
const N3c = nlines * binom(q + 1, 3);
const N3nc = binom(n, 3) - N3c;

const tables = {};
let total = 0, maxG = 0;
const maximalCounts = {};
for (let m = 3; m <= maxm; m++) {
  const div = binom(m, 3);
  const row = {};
  const ca = gA.cnt[m] || new Array(64).fill(0);
  const cb = gB.cnt[m] || new Array(64).fill(0);
  const ma = gA.maximal[m] || 0, mb = gB.maximal[m] || 0;
  for (let g = 0; g < 64; g++) {
    const num = N3nc * (ca[g] || 0) + N3c * (cb[g] || 0);
    if (num === 0) continue;
    if (num % div !== 0) { console.error(`FATAL divisibility m=${m} g=${g}`); process.exit(4); }
    row[g] = num / div;
    total += num / div;
    if (g > maxG) maxG = g;
  }
  tables[m] = row;
  const mm = N3nc * ma + N3c * mb;
  if (mm !== 0) {
    if (mm % div !== 0) { console.error(`FATAL maximal divisibility m=${m}`); process.exit(5); }
    maximalCounts[m] = mm / div;
  }
}

// root chain
const v3nc = gA.G[3][0], v3c = gB.G[3][0];
let line01 = null;
for (const L of lines) { const b0 = (L.lo >>> 0) & 1, b1 = (L.lo >>> 1) & 1; if (b0 && b1) { line01 = L; break; } }
const childv2 = new Uint8Array(64);
for (let x = 2; x < n; x++) {
  const online = x < 32 ? (line01.lo >>> x) & 1 : (line01.hi >>> (x - 32)) & 1;
  childv2[online ? v3c : v3nc] = 1;
}
let v2 = 0; while (childv2[v2]) v2++;
const v1 = v2 === 0 ? 1 : 0;
const v0 = v1 === 0 ? 1 : 0;

const a3 = binom(n, 3);
const a4 = binom(n, 4) - nlines * binom(q + 1, 4);
const a5 = binom(n, 5) - nlines * (binom(q + 1, 4) * (n - (q + 1)) + binom(q + 1, 5));

const out = {
  board: `PG(2,${q})`, points: n, lines: nlines, s, fset,
  nodes_cone_noncoll: A.nodes, nodes_cone_coll: B.nodes,
  layers_noncoll: A.layers.map(l => l.length), layers_coll: B.layers.map(l => l.length),
  max_size: maxm, grundy_tables: tables, maximal_counts: maximalCounts,
  g_empty: v0, g_single: v1, g_pair: v2, g_triple_noncoll: v3nc, g_triple_coll: v3c,
  N3nc, N3c, anchor_totals: { m3: a3, m4: a4, m5: a5 },
  total_positions: total + binom(n, 2) + n + 1,
  max_grundy: maxG,
};
console.log(JSON.stringify(out));
