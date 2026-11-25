// wsearch34.js — structural (3,a,3)-family witness search for w=3, q=4 boards of width m.
//
// Family: one deficient row Y with a ∈ {0,1,2} stones (≤ q−2 = 2), the two other
// rows full (exactly 3 stones each). Exact search WITHIN that family:
// it finds a witness iff the family has one at (m, Y) with deficient row Y.
// No claim about other row-count profiles (multi-deficient-row witnesses would
// need a wider search).
//
// Reduction (lane note): full rows (3 stones) are automatically maximal (row lines,
// m ≥ 4) and safe (3 < q). Non-horizontal lines have ≤ 3 lattice points on a
// 3-row board, so only circles matter cross-row. Row-Y blocking needs a circle
// with ≥ 3 stones through each empty cell:
//   U0 = row-Y lattice cells on the 18 three-base-stone circles,
//   W(s) = second row-Y crossings of circles (row-Y stone s + base pair).
// Stones must sit off U0 (else 4 co-circular with a base triple).
// Safety (all 4-subsets): 2+2 across rows (P22/P11 per-b fourth-point tables),
// 2 base + s (ON tables), 1+1+s+t / 2+s+t (CX tables, t ∈ W(s)).
//
// Usage: node wsearch34.js <m> <Y> [--examples=N] [--quiet]
'use strict';
const S = require('./sat.js');

const argv = process.argv.slice(2);
const args = argv.filter(a => !a.startsWith('--'));
const m = Number(args[0]);
const Y = Number(args[1]);
const [o1, o2] = [0, 1, 2].filter(r => r !== Y);
const quiet = argv.includes('--quiet');
const maxEx = (() => { const f = argv.find(a => a.startsWith('--examples=')); return f ? Number(f.slice(11)) : 3; })();
if (!(4 <= m && m <= 31)) throw new Error('require 4 <= m <= 31');
const FULL = (1 << m) - 1;
const bit = x => 1 << x;
function pop(x) { x >>>= 0; x -= (x >> 1) & 0x55555555; x = (x & 0x33333333) + ((x >> 2) & 0x33333333); x = (x + (x >> 4)) & 0x0f0f0f0f; return (x * 0x01010101) >>> 24; }

function quadRoots(a, b, c) {
  if (a === 0) {
    if (b === 0) return [];
    const r = -c / b;
    return Number.isInteger(r) && r >= 0 && r < m ? [r] : [];
  }
  const disc = b * b - 4 * a * c;
  if (disc < 0) return [];
  const s = Math.sqrt(disc);
  if (s * s !== disc) return [];
  const out = [];
  for (const sg of [s, -s]) {
    const num = -b + sg, den = 2 * a;
    if (num % den === 0) { const r = num / den; if (r >= 0 && r < m) out.push(r); }
  }
  return out;
}
function rowCells(co, y) {
  const [a, b, c, d] = co;
  return quadRoots(a, b, a * y * y + c * y + d);
}

// --- tables ------------------------------------------------------------
const M_AB = new Int32Array(m * m * m); // [(a1,a2),b] -> row-Y mask of circle((a1,o1),(a2,o1),(b,o2))
const M_BA = new Int32Array(m * m * m); // [(b1,b2),a] -> row-Y mask of circle((b1,o2),(b2,o2),(a,o1))
const P22 = new Int32Array(m * m * m); // [(a1,a2),b] -> bit of OTHER o2 crossing (2+2 co-circularity)
const P11 = new Int32Array(m * m * m); // [(b1,b2),a] -> bit of OTHER o1 crossing
for (let a1 = 0; a1 < m; a1++) for (let a2 = a1 + 1; a2 < m; a2++) {
  for (let b = 0; b < m; b++) {
    const co = S.circleABC([a1, o1], [a2, o1], [b, o2]);
    if (!co) continue;
    for (const x of rowCells(co, Y)) M_AB[(a1 * m + a2) * m + b] |= bit(x);
    for (const x of rowCells(co, o2)) if (x !== b) P22[(a1 * m + a2) * m + b] |= bit(x);
  }
}
for (let b1 = 0; b1 < m; b1++) for (let b2 = b1 + 1; b2 < m; b2++) {
  for (let a = 0; a < m; a++) {
    const co = S.circleABC([b1, o2], [b2, o2], [a, o1]);
    if (!co) continue;
    for (const x of rowCells(co, Y)) M_BA[(b1 * m + b2) * m + a] |= bit(x);
    for (const x of rowCells(co, o1)) if (x !== a) P11[(b1 * m + b2) * m + a] |= bit(x);
  }
}

const NP = 2 * m; // base pids: 0..m-1 row o1 cells, m..2m-1 row o2 cells
const FX = new Int32Array(m * NP * NP);  // [s,(p,q)] other row-Y crossing of circle((s,Y),p,q) or -1
const ON1 = new Int32Array(m * NP * NP); // [s,(p,q)] o1 cells on that circle, excl p/q own cells
const ON2 = new Int32Array(m * NP * NP);
const CX1 = new Int32Array(m * m * NP);  // [s,t,p] o1 cells on circle((s,Y),(t,Y),p), excl p cell
const CX2 = new Int32Array(m * m * NP);
for (let s = 0; s < m; s++) {
  for (let p = 0; p < NP; p++) for (let q2 = p + 1; q2 < NP; q2++) {
    const P1 = p < m ? [p, o1] : [p - m, o2];
    const Q1 = q2 < m ? [q2, o1] : [q2 - m, o2];
    const co = S.circleABC([s, Y], P1, Q1);
    const idx = (s * NP + p) * NP + q2;
    FX[idx] = -1;
    if (!co) continue;
    for (const x of rowCells(co, Y)) if (x !== s) FX[idx] = x;
    let m1 = 0, m2 = 0;
    for (const x of rowCells(co, o1)) m1 |= bit(x);
    for (const x of rowCells(co, o2)) m2 |= bit(x);
    if (p < m) m1 &= ~bit(p); else m2 &= ~bit(p - m);
    if (q2 < m) m1 &= ~bit(q2); else m2 &= ~bit(q2 - m);
    ON1[idx] = m1; ON2[idx] = m2;
  }
}
for (let s = 0; s < m; s++) for (let t = 0; t < m; t++) {
  if (s === t) continue;
  for (let p = 0; p < NP; p++) {
    const P1 = p < m ? [p, o1] : [p - m, o2];
    const co = S.circleABC([s, Y], [t, Y], P1);
    const idx = (s * m + t) * NP + p;
    CX1[idx] = 0; CX2[idx] = 0;
    if (!co) continue;
    let m1 = 0, m2 = 0;
    for (const x of rowCells(co, o1)) m1 |= bit(x);
    for (const x of rowCells(co, o2)) m2 |= bit(x);
    if (p < m) m1 &= ~bit(p); else m2 &= ~bit(p - m);
    CX1[idx] = m1; CX2[idx] = m2;
  }
}

// --- subsets -----------------------------------------------------------
const subs3 = [];
for (let i = 0; i < m; i++) for (let j = i + 1; j < m; j++) for (let k = j + 1; k < m; k++) subs3.push([i, j, k]);
const nSub = subs3.length;
const subMask = new Int32Array(nSub), subPairKey = [];
for (let i = 0; i < nSub; i++) {
  const s = subs3[i];
  subMask[i] = bit(s[0]) | bit(s[1]) | bit(s[2]);
  const pk = [];
  for (let u = 0; u < 3; u++) for (let v = u + 1; v < 3; v++) {
    pk.push(s[u] < s[v] ? s[u] * m + s[v] : s[v] * m + s[u]);
  }
  subPairKey[i] = pk;
}

// --- search ------------------------------------------------------------
const t0 = Date.now();
const witnesses = [];
let cntA0 = 0, cntA1 = 0, cntA2 = 0, configCount = 0, safeCount = 0, deepCount = 0;
const exCount = {};
function report(a, stones) {
  if (a === 0) cntA0++; else if (a === 1) cntA1++; else cntA2++;
  exCount[a] = (exCount[a] || 0) + 1;
  if (exCount[a] <= maxEx) witnesses.push({ a, stones });
}

const aLo = (() => { const f = argv.find(a => a.startsWith('--ia=')); return f ? Number(f.slice(5)) : 0; })();
const aHi = (() => { const f = argv.find(a => a.startsWith('--ib=')); return f ? Number(f.slice(5)) : nSub; })();
for (let ia = aLo; ia < Math.min(aHi, nSub); ia++) {
  const Amask = subMask[ia];
  const A = subs3[ia], Apk = subPairKey[ia];
  for (let ib = 0; ib < nSub; ib++) {
    const B = subs3[ib], Bmask = subMask[ib], Bpk = subPairKey[ib];
    configCount++;
    let unsafe = false;
    for (let u = 0; u < 3; u++) {
      const base = Apk[u] * m;
      for (let bi = 0; bi < 3; bi++) if (P22[base + B[bi]] & Bmask) { unsafe = true; break; }
      if (unsafe) break;
    }
    if (!unsafe) for (let u = 0; u < 3; u++) {
      const base = Bpk[u] * m;
      for (let ai = 0; ai < 3; ai++) if (P11[base + A[ai]] & Amask) { unsafe = true; break; }
      if (unsafe) break;
    }
    if (unsafe) continue;
    safeCount++;
    let U0 = 0;
    for (let u = 0; u < 3; u++) { const base = Apk[u] * m; U0 |= M_AB[base + B[0]] | M_AB[base + B[1]] | M_AB[base + B[2]]; }
    for (let u = 0; u < 3; u++) { const base = Bpk[u] * m; U0 |= M_BA[base + A[0]] | M_BA[base + A[1]] | M_BA[base + A[2]]; }
    const defn = (FULL & ~U0) >>> 0;
    const d = pop(defn);
    if (d === 0) {
      report(0, [].concat(A.map(x => [x, o1]), B.map(x => [x, o2])));
      continue;
    }
    if (d > 32) continue;
    deepCount++;
    const cand = [];
    for (let x = 0; x < m; x++) if (defn & bit(x)) cand.push(x);
    const cells = A.map(x => x).concat(B.map(x => x + m)); // 6 base pids: row o1, row o2
    const W = new Map();
    for (const s of cand) {
      let w = 0, ok = true;
      for (let u = 0; u < 6 && ok; u++) for (let v = u + 1; v < 6 && ok; v++) {
        const p = cells[u] < cells[v] ? cells[u] : cells[v];
        const r = cells[u] < cells[v] ? cells[v] : cells[u];
        const idx = (s * NP + p) * NP + r;
        if ((ON1[idx] & Amask) || (ON2[idx] & Bmask)) ok = false;
        else { const f = FX[idx]; if (f >= 0) w |= bit(f); }
      }
      if (ok) W.set(s, w);
    }
    for (const s of cand) {
      const w = W.get(s);
      if (w !== undefined && ((w | bit(s)) & defn) === defn) report(1, [].concat(A.map(x => [x, o1]), B.map(x => [x, o2]), [[s, Y]]));
    }
    for (let i = 0; i < cand.length; i++) {
      const s = cand[i], ws = W.get(s);
      if (ws === undefined) continue;
      for (let j = i + 1; j < cand.length; j++) {
        const t = cand[j], wt = W.get(t);
        if (wt === undefined) continue;
        if ((ws >>> t) & 1) continue;
        if ((wt >>> s) & 1) continue;
        let bad = false;
        for (const pid of cells) {
          const idx = (s * m + t) * NP + pid;
          if ((CX1[idx] & Amask) || (CX2[idx] & Bmask)) { bad = true; break; }
        }
        if (bad) continue;
        if (((ws | wt | bit(s) | bit(t)) & defn) === defn) {
          report(2, [].concat(A.map(x => [x, o1]), B.map(x => [x, o2]), [[s, Y], [t, Y]]));
        }
      }
    }
  }
}

console.log(JSON.stringify({ m, Y, ia: [aLo, Math.min(aHi, nSub)], o1, o2, configs: configCount, safe: safeCount, deep: deepCount, a0: cntA0, a1: cntA1, a2: cntA2, ms: Date.now() - t0 }));
if (!quiet) for (const w of witnesses) console.log(JSON.stringify(w));
