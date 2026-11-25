'use strict';
// census2.js — GP-set census for the binary cube {0,1}^d.
// GP (general position) = every (d+1)-point subset affinely independent
//   (= every m-subset of homogeneous (1,x) rows independent, m = d+1).
// Vertex-0-anchored: x -> x XOR u is a vertex-transitive affine automorphism,
//   so counting/deciding sets containing 0 is complete. (0,v2) pairs partition the tree.
// EXACTNESS: every gate is a zero-test of a 7x7 {0,1}-rows determinant
//   (hadamard (sqrt 7)^7 = 907 < PA = prime < 2^26). Field residues satisfy:
//   true det == 0  <=>  det == 0 in F_p (since |det| < p). Fast frames use
//   E = unnormalized fraction-free two-sided GJ of [W|I] with E*W diagonal
//   (pivots nonzero); every functional used per gate is a per-row/per-column
//   rescaling of the true functional, so zero-tests are invariant.
//   PA and PB (dual prime) are both computed for doubles/triples as
//   belt-and-suspenders; either alone is already exact.
// Modes:
//   node census2.js battery                 — full validation battery
//   node census2.js census <d> [maxSize]    — full anchored census for dim d
//   node census2.js task6 <v2>              — single (0,v2) pair, d=6, prints one JSON line
//   node census2.js check6 <v2> [maxChecks] — task6 + brute re-verification of every gate
//   node census2.js brute <d> <maxSize>     — independent anchored brute enumeration
//   node census2.js walk <d> <v> ...        — brute GP check of one given set
//   node census2.js primes

// ---------- primes ----------
function isPrime(x) {
  if (x < 2) return false;
  if (x % 2 === 0) return x === 2;
  for (let d = 3; d * d <= x; d += 2) if (x % d === 0) return false;
  return true;
}
function topPrimesBelow(limit, k) {
  const out = [];
  let x = limit - 1;
  if (x % 2 === 0) x--;
  while (out.length < k) { if (isPrime(x)) out.push(x); x -= 2; }
  return out;
}
const [PA, PB] = topPrimesBelow(1 << 26, 2);
function modpow(b, e, p) {
  b = ((b % p) + p) % p;
  let r = 1;
  while (e > 0) {
    if (e & 1) r = (r * b) % p;
    b = (b * b) % p;
    e = Math.floor(e / 2);
  }
  return r % p;
}

// ---------- rng ----------
function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// ---------- context ----------
function makeCtx(d) {
  const n = 1 << d, m = d + 1;
  const verts = new Float64Array(n * m);
  for (let v = 0; v < n; v++) {
    const base = v * m;
    verts[base] = 1;
    for (let b = 0; b < d; b++) if ((v >> b) & 1) verts[base + 1 + b] = 1;
  }
  const ones = new Array(n);
  for (let v = 0; v < n; v++) {
    const l = [0];
    for (let b = 0; b < d; b++) if ((v >> b) & 1) l.push(1 + b);
    ones[v] = l;
  }
  const ctx = { d, n, m, verts, ones };
  if (d === 6) {
    ctx.pairs21 = [];
    for (let a = 0; a < 7; a++) for (let b = a + 1; b < 7; b++) ctx.pairs21.push(a * 8 + b); // packed
    ctx.triples35 = [];
    for (let a = 0; a < 7; a++) for (let b = a + 1; b < 7; b++) for (let c = b + 1; c < 7; c++) ctx.triples35.push([a, b, c]);
  }
  return ctx;
}

// ---------- fraction-free mod elimination helpers (allocation-free, no inverses) ----------
// scratch buffers reused across calls (single-threaded)
const SCR = new Float64Array(64 * 16); // up to 7x14
function ffRank(ctx, rowsList, prime) { // rank of rows (each vertex id)
  const m = ctx.m, r = rowsList.length, V = ctx.verts;
  const A = SCR;
  for (let i = 0; i < r; i++) for (let j = 0; j < m; j++) A[i * m + j] = V[rowsList[i] * m + j];
  let rank = 0;
  for (let c = 0; c < m && rank < r; c++) {
    let piv = -1;
    for (let i = rank; i < r; i++) { const v = A[i * m + c] % prime; if (v !== 0) { A[i * m + c] = v; piv = i; break; } }
    if (piv < 0) continue;
    if (piv !== rank) for (let j = c; j < m; j++) { const t = A[rank * m + j]; A[rank * m + j] = A[piv * m + j]; A[piv * m + j] = t; }
    const pv = A[rank * m + c];
    for (let i = rank + 1; i < r; i++) {
      const f = A[i * m + c];
      if (f === 0) continue;
      for (let j = c; j < m; j++) {
        let x = (A[i * m + j] * pv - f * A[rank * m + j]) % prime;
        if (x < 0) x += prime;
        A[i * m + j] = x;
      }
    }
    rank++;
  }
  return rank;
}
function ffDetNonzero(ctx, rowsList, prime) { // square (len == m) det != 0 test
  const m = ctx.m, r = rowsList.length, V = ctx.verts;
  if (r !== m) throw new Error('ffDetNonzero non-square');
  const A = SCR;
  for (let i = 0; i < r; i++) for (let j = 0; j < m; j++) A[i * m + j] = V[rowsList[i] * m + j];
  for (let k = 0; k < m; k++) {
    let piv = -1;
    for (let i = k; i < m; i++) { const v = A[i * m + k] % prime; if (v !== 0) { A[i * m + k] = v; piv = i; break; } }
    if (piv < 0) return false; // pivot column dependent => det == 0
    if (piv !== k) for (let j = k; j < m; j++) { const t = A[k * m + j]; A[k * m + j] = A[piv * m + j]; A[piv * m + j] = t; }
    const pv = A[k * m + k];
    for (let i = k + 1; i < m; i++) {
      const f = A[i * m + k];
      if (f === 0) continue;
      for (let j = k; j < m; j++) {
        let x = (A[i * m + j] * pv - f * A[k * m + j]) % prime;
        if (x < 0) x += prime;
        A[i * m + j] = x;
      }
    }
  }
  return true;
}

// ---------- normalized inverse mod p (two-sided GJ; exact inverse E = W^{-1} mod p) ----------
const GJBUF = new Float64Array(7 * 14);
function gjInv(ctx, rowsList, prime) {
  const m = 7, W2 = 14;
  const A = GJBUF, V = ctx.verts;
  for (let i = 0; i < 7; i++) {
    const rbase = rowsList[i] * m;
    for (let j = 0; j < 7; j++) A[i * W2 + j] = V[rbase + j];
    for (let j = 0; j < 7; j++) A[i * W2 + 7 + j] = (i === j) ? 1 : 0;
  }
  for (let k = 0; k < 7; k++) {
    let piv = -1;
    for (let i = k; i < 7; i++) { const v = A[i * W2 + k] % prime; if (v !== 0) { A[i * W2 + k] = v; piv = i; break; } }
    if (piv < 0) return null;
    if (piv !== k) for (let j = 0; j < W2; j++) { const t = A[k * W2 + j]; A[k * W2 + j] = A[piv * W2 + j]; A[piv * W2 + j] = t; }
    const pv = A[k * W2 + k];
    const inv = modpow(pv, prime - 2, prime);
    for (let j = k; j < W2; j++) A[k * W2 + j] = (A[k * W2 + j] * inv) % prime;
    for (let i = k + 1; i < 7; i++) {
      const f = A[i * W2 + k];
      if (f === 0) continue;
      for (let j = k; j < W2; j++) {
        let x = (A[i * W2 + j] - f * A[k * W2 + j]) % prime;
        if (x < 0) x += prime;
        A[i * W2 + j] = x;
      }
    }
  }
  for (let k = 6; k >= 1; k--) {
    for (let i = 0; i < k; i++) {
      const f = A[i * W2 + k];
      if (f === 0) continue;
      for (let j = k; j < W2; j++) {
        let x = (A[i * W2 + j] - f * A[k * W2 + j]) % prime;
        if (x < 0) x += prime;
        A[i * W2 + j] = x;
      }
    }
  }
  const E = new Float64Array(49);
  for (let i = 0; i < 7; i++) for (let j = 0; j < 7; j++) E[i * 7 + j] = A[i * W2 + 7 + j];
  return E;
}
// E = true inverse of W mod prime. All gate functionals are y(x) = (E^T x) = W^{-T} x:
//   det(W row i <- x) = det(W) * y(x)_i                     (zero-test exact)
//   det(W rows S <- p1,...) = det(W) * det [ y(p_t)_j ]_{t, j in S}   (verified numerically)

// ---------- sparse functionals ----------
function sparseT(E, ctx, x, out, prime) { // out[a] = (E^T x)_a mod prime = sum_{j in ones(x)} E[j*7+a]
  const ones = ctx.ones[x];
  for (let a = 0; a < 7; a++) {
    let s = 0;
    for (let t = 0; t < ones.length; t++) s += E[ones[t] * 7 + a];
    let r = s % prime;
    if (r < 0) r += prime;
    out[a] = r;
  }
}
function det3mod(u0, u1, u2, z0, z1, z2, x0, x1, x2, prime) {
  // 3x3 det with rows = points (u,z,x), cols = components (a,b,c):
  // [[yu_a, yu_b, yu_c], [yz_a, yz_b, yz_c], [yx_a, yx_b, yx_c]]
  const t1 = u0 * ((z1 * x2 - z2 * x1) % prime);
  const t2 = u1 * ((z0 * x2 - z2 * x0) % prime);
  const t3 = u2 * ((z0 * x1 - z1 * x0) % prime);
  let x = ((t1 - t2 + t3) % prime + 2 * prime) % prime;
  return x;
}

// ---------- brute GP check (independent reference) ----------
function bruteIsGP(ctx, vs) {
  const s = vs.length, m = ctx.m;
  if (s <= m) return ffRank(ctx, vs, PA) === s;
  const cur = [];
  let ok = true;
  (function rec(start, need) {
    if (!ok) return;
    if (need === 0) {
      const rows = cur.slice().map(i => vs[i]);
      if (!ffDetNonzero(ctx, rows, PA)) ok = false;
      return;
    }
    for (let i = start; i <= s - need; i++) { cur.push(i); rec(i + 1, need - 1); cur.pop(); if (!ok) return; }
  })(0, m, 0);
  return ok;
}

// ---------- census ----------
function makeFastScratch() {
  return {
    EA: new Float64Array(49), EB: new Float64Array(49), EBready: false,
    xi8A: new Float64Array(7), xi9A: new Float64Array(7),
    xi8B: new Float64Array(7), xi9B: new Float64Array(7),
    yA: new Float64Array(7), xiA: new Float64Array(7), xiB: new Float64Array(7),
  };
}

function censusRun(ctx, opts) {
  const n = ctx.n, m = ctx.m;
  const maxS = opts.maxSize || (ctx.d === 6 ? 10 : 8);
  const counts = new Array(maxS + 1).fill(0);
  const nodes = new Array(maxS + 1).fill(0);
  const witnesses = [];
  const cs = new Int32Array(maxS + 1);
  const fr = [];
  for (let s = 0; s <= maxS; s++) fr.push(makeFastScratch());
  let selfChecks = 0, selfCheckFails = 0;
  const maxSelfChecks = opts.maxSelfChecks || 0;
  const rowsBuf = [];

  function gateSelfCheck(s, v, fastAns) {
    if (!maxSelfChecks || selfChecks >= maxSelfChecks) return fastAns;
    const sl = rowsBuf.slice(0, s);
    for (let i = 0; i < s; i++) sl[i] = cs[i];
    sl.push(v);
    const truth = bruteIsGP(ctx, sl);
    selfChecks++;
    if (truth !== fastAns) {
      selfCheckFails++;
      throw new Error('GATE DISAGREEMENT s=' + s + ' set=' + sl.join(',') + ' fast=' + fastAns + ' brute=' + truth);
    }
    return fastAns;
  }

  function gateGeneric(s, v) {
    const k1 = s + 1;
    const sl = [];
    for (let i = 0; i < s; i++) sl.push(cs[i]);
    sl.push(v);
    if (k1 <= m) return ffRank(ctx, sl, PA) === k1;
    const cur = [];
    let ok = true;
    (function rec2(start, need) {
      if (!ok) return;
      if (need === 0) {
        const rows = cur.slice().map(i => cs[i]);
        rows.push(v);
        if (!ffDetNonzero(ctx, rows, PA)) ok = false;
        return;
      }
      for (let i = start; i <= s - need; i++) { cur.push(i); rec2(i + 1, need - 1); cur.pop(); if (!ok) return; }
    })(0, m - 1);
    return ok;
  }

  function gate6(v) {
    for (let i = 0; i < 6; i++) rowsBuf[i] = cs[i];
    rowsBuf[6] = v;
    return ffDetNonzero(ctx, rowsBuf, PA);
  }
  function gate7(v) {
    const F = fr[7];
    sparseT(F.EA, ctx, v, F.yA, PA);
    const y = F.yA;
    for (let a = 0; a < 7; a++) if (y[a] === 0) return false;
    return true;
  }
  function gate8(v) {
    const F = fr[8];
    sparseT(F.EA, ctx, v, F.yA, PA);   // candidate y(x) mod PA
    const y = F.yA;
    for (let a = 0; a < 7; a++) if (y[a] === 0) return false;
    const xA = y, xB = F.xiB;           // xB: y(x) mod PB
    sparseT(F.EB, ctx, v, xB, PB);
    const uA = F.xi8A, uB = F.xi8B;     // y(u8) both primes (per node)
    const P = ctx.pairs21;
    for (let p = 0; p < 21; p++) {
      const pk = P[p], a = pk >> 3, b = pk & 7;
      const A2 = (uA[a] * xA[b] - uA[b] * xA[a]) % PA;
      if (A2 === 0) {
        const B2 = (uB[a] * xB[b] - uB[b] * xB[a]) % PB;
        if (B2 === 0) return false;
      }
    }
    return true;
  }
  function gate9(v) {
    const F = fr[9];
    sparseT(F.EA, ctx, v, F.yA, PA);
    const y = F.yA;
    for (let a = 0; a < 7; a++) if (y[a] === 0) return false;
    const xA = y, xB = F.xiB;
    sparseT(F.EB, ctx, v, xB, PB);
    const P = ctx.pairs21;
    for (let j = 0; j < 2; j++) {
      const uA = j === 0 ? F.xi8A : F.xi9A, uB = j === 0 ? F.xi8B : F.xi9B;
      for (let p = 0; p < 21; p++) {
        const pk = P[p], a = pk >> 3, b = pk & 7;
        const A2 = (uA[a] * xA[b] - uA[b] * xA[a]) % PA;
        if (A2 === 0) {
          const B2 = (uB[a] * xB[b] - uB[b] * xB[a]) % PB;
          if (B2 === 0) return false;
        }
      }
    }
    for (let t = 0; t < 35; t++) {
      const tr = ctx.triples35[t];
      const a = tr[0], b = tr[1], c = tr[2];
      const u8A = F.xi8A, u9A = F.xi9A, u8B = F.xi8B, u9B = F.xi9B;
      const dBfirst = det3mod(u8B[a], u8B[b], u8B[c], u9B[a], u9B[b], u9B[c], xB[a], xB[b], xB[c], PB);
      if (dBfirst === 0) {
        const dA = det3mod(u8A[a], u8A[b], u8A[c], u9A[a], u9A[b], u9A[c], xA[a], xA[b], xA[c], PA);
        if (dA === 0) return false;
      }
    }
    return true;
  }

  function gate(s, v) {
    let ans;
    if (s + 1 <= m) {
      const sl = rowsBuf.slice(0, s);
      for (let i = 0; i < s; i++) sl[i] = cs[i];
      sl.push(v);
      ans = ffRank(ctx, sl, PA) === s + 1;
    } else if (ctx.d === 6) {
      if (s === 6) ans = gate6(v);
      else if (s === 7) ans = gate7(v);
      else if (s === 8) ans = gate8(v);
      else if (s === 9) ans = gate9(v);
      else ans = gateGeneric(s, v);
    } else {
      ans = gateGeneric(s, v);
    }
    if (maxSelfChecks && selfChecks < maxSelfChecks) ans = gateSelfCheck(s, v, ans);
    return ans;
  }

  function initFrame(s) {
    nodes[s]++;
    if (s !== 7 && s !== 8 && s !== 9) return;
    const F = fr[s];
    if (s === 7) {
      for (let i = 0; i < 7; i++) rowsBuf[i] = cs[i];
      const EA = gjInv(ctx, rowsBuf, PA);
      if (!EA) throw new Error('EA singular at s=7 (impossible)');
      F.EA.set(EA);
      fr[7].EBready = false;
    } else if (s === 8) {
      if (!fr[7].EBready) {
        for (let i = 0; i < 7; i++) rowsBuf[i] = cs[i];
        const EB = gjInv(ctx, rowsBuf, PB);
        if (!EB) throw new Error('EB singular at s=8 (impossible)');
        fr[7].EB.set(EB);
        fr[7].EBready = true;
      }
      F.EA.set(fr[7].EA); F.EB.set(fr[7].EB);
      const u = cs[7];
      sparseT(F.EA, ctx, u, F.xi8A, PA);   // y(u8) mod PA
      sparseT(F.EB, ctx, u, F.xi8B, PB);   // y(u8) mod PB
    } else { // s === 9
      F.EA.set(fr[7].EA); F.EB.set(fr[7].EB);
      sparseT(F.EA, ctx, cs[7], F.xi8A, PA);
      sparseT(F.EB, ctx, cs[7], F.xi8B, PB);
      sparseT(F.EA, ctx, cs[8], F.xi9A, PA);
      sparseT(F.EB, ctx, cs[8], F.xi9B, PB);
    }
  }

  function rec(s) {
    if (s >= maxS) return;
    let start = cs[s - 1] + 1;
    let end = n;
    if (s === 2 && (opts.v3lo !== undefined || opts.v3hi !== undefined)) {
      if (opts.v3lo !== undefined && start < opts.v3lo) start = opts.v3lo;
      if (opts.v3hi !== undefined) end = Math.min(n, opts.v3hi + 1);
    }
    for (let v = start; v < end; v++) {
      if (gate(s, v)) {
        cs[s] = v;
        counts[s + 1]++;
        if (s + 1 === 10) {
          witnesses.push(Array.from(cs.slice(0, 10)).join(','));
          cs[s] = 0;
          continue;
        }
        if (s + 1 === maxS) { cs[s] = 0; continue; }
        if (ctx.d === 6 && s + 1 >= 7) initFrame(s + 1);
        else nodes[s + 1]++;
        rec(s + 1);
        cs[s] = 0;
      }
    }
  }

  if (opts.v2 !== null && opts.v2 !== undefined) {
    cs[0] = 0; cs[1] = opts.v2;
    counts[1] = 1;
    counts[2] = 1;
    nodes[2]++;
    rec(2);
  } else {
    for (let v2 = 1; v2 < n; v2++) {
      cs[0] = 0; cs[1] = v2;
      nodes[2]++;
      rec(2);
    }
    counts[1] = 1;
    counts[2] = n - 1;
  }
  return { counts, nodes, witnesses, selfChecks, selfCheckFails };
}

// ---------- brute enumeration (independent reference) ----------
function bruteCensus(ctx, maxS) {
  const n = ctx.n;
  const counts = new Array(maxS + 1).fill(0);
  const cs = new Int32Array(maxS + 1);
  function rec(s) {
    if (s >= maxS) return;
    for (let v = cs[s - 1] + 1; v < n; v++) {
      const sl = [];
      for (let i = 0; i < s; i++) sl.push(cs[i]);
      sl.push(v);
      if (bruteIsGP(ctx, sl)) {
        cs[s] = v; counts[s + 1]++;
        rec(s + 1); cs[s] = 0;
      }
    }
  }
  cs[0] = 0; counts[1] = 1;
  rec(1);
  counts[2] = n - 1;
  return counts;
}

// ---------- Laplace BigInt reference det ----------
function laplaceDet(ctx, rowsList) {
  const m = ctx.m, V = ctx.verts;
  const M = [];
  for (const r of rowsList) {
    const row = [];
    for (let j = 0; j < m; j++) row.push(BigInt(V[r * m + j]));
    M.push(row);
  }
  function det(Mx) {
    const n = Mx.length;
    if (n === 1) return Mx[0][0];
    if (n === 2) return Mx[0][0] * Mx[1][1] - Mx[0][1] * Mx[1][0];
    let sum = 0n, sgn = 1n;
    for (let j = 0; j < n; j++) {
      if (Mx[0][j] !== 0n) {
        const sub = [];
        for (let i = 1; i < n; i++) { const r = Mx[i].slice(); r.splice(j, 1); sub.push(r); }
        sum += sgn * Mx[0][j] * det(sub);
      }
      sgn = -sgn;
    }
    return sum;
  }
  return det(M);
}

// ---------- battery ----------
function battery() {
  const t0 = Date.now();
  const ctx6 = makeCtx(6);
  const rnd = mulberry32(20261121);
  function rvert() { return Math.floor(rnd() * 64); }
  function rset(k) { const s = new Set(); while (s.size < k) s.add(rvert()); return Array.from(s); }
  let pass = 0, fail = 0;
  function check(name, cond, extra) {
    if (cond) { pass++; } else { fail++; console.log('FAIL ' + name + (extra ? ' :: ' + extra : '')); }
  }
  check('prime PA', isPrime(PA), String(PA));
  check('prime PB', isPrime(PB), String(PB));
  console.log('primes PA=' + PA + ' PB=' + PB);

  // B1: gjInv gives true inverse (E*W == I)
  {
    let trials = 0, bad = 0;
    for (let iter = 0; iter < 400 && trials < 150; iter++) {
      const rows = rset(7);
      if (laplaceDet(ctx6, rows) === 0n) continue;
      trials++;
      for (const prime of [PA, PB]) {
        const E = gjInv(ctx6, rows, prime);
        if (!E) { bad++; continue; }
        const V = ctx6.verts;
        let okFull = true;
        for (let i = 0; i < 7; i++) {
          for (let j = 0; j < 7; j++) {
            let s = 0;
            for (let k = 0; k < 7; k++) s += E[i * 7 + k] * V[rows[k] * 7 + j];
            const sv = s % prime;
            const want = (i === j) ? (sv === 1) : (sv === 0);
            if (!want) okFull = false;
          }
        }
        if (!okFull) bad++;
      }
    }
    check('B1 gjInv identity', bad === 0 && trials >= 50, 'trials=' + trials + ' bad=' + bad);
  }

  // B1.5: ffDetNonzero pinned to Laplace ground truth (mixed singular/independent)
  {
    let trials = 0, bad = 0;
    for (let iter = 0; iter < 250; iter++) {
      const rows = rset(7);
      const lap = laplaceDet(ctx6, rows);
      const ff = ffDetNonzero(ctx6, rows, PA);
      if ((lap === 0n) !== (!ff)) { bad++; console.log('B1.5 mismatch rows=' + rows); }
      trials++;
    }
    check('B1.5 ffDetNonzero vs Laplace', bad === 0 && trials >= 200, 'trials=' + trials + ' bad=' + bad);
  }

  // B2: singles: (E^T x)_a == 0 (mod PA) <=> det(W row a <- x) == 0 (ref: ffDetNonzero)
  {
    let trials = 0, bad = 0;
    for (let iter = 0; iter < 30000 && trials < 7200; iter++) {
      const rows = rset(7);
      if (laplaceDet(ctx6, rows) === 0n) continue;
      const E = gjInv(ctx6, rows, PA);
      if (!E) { bad++; continue; }
      const y = new Float64Array(7);
      for (let x = 0; x < 64; x++) {
        sparseT(E, ctx6, x, y, PA);
        for (let a = 0; a < 7; a++) {
          const Wr = rows.slice(); Wr[a] = x;
          const d = ffDetNonzero(ctx6, Wr, PA);
          if (d !== (y[a] !== 0)) { bad++; console.log('B2 mismatch W=' + rows + ' x=' + x + ' a=' + a); }
          trials++;
        }
      }
    }
    check('B2 singles functional', bad === 0 && trials >= 7000, 'trials=' + trials + ' bad=' + bad);
  }

  // B3: doubles both-prime zero <=> det of row-pair replacement (ref: ffDetNonzero)
  {
    let trials = 0, bad = 0;
    for (let iter = 0; iter < 4000 && trials < 2000; iter++) {
      const rows = rset(7);
      if (!ffDetNonzero(ctx6, rows, PA)) continue;
      const EA = gjInv(ctx6, rows, PA), EB = gjInv(ctx6, rows, PB);
      if (!EA || !EB) { bad++; continue; }
      const u = rvert(), x = rvert();
      const uA = new Float64Array(7), uB = new Float64Array(7), xA = new Float64Array(7), xB = new Float64Array(7);
      sparseT(EA, ctx6, u, uA, PA); sparseT(EB, ctx6, u, uB, PB);
      sparseT(EA, ctx6, x, xA, PA); sparseT(EB, ctx6, x, xB, PB);
      for (let ti = 0; ti < 3; ti++) {
        const a = Math.floor(rnd() * 7) | 0, b = Math.floor(rnd() * 7) | 0;
        if (a === b) continue;
        const A2 = (((uA[a] * xA[b] - uA[b] * xA[a]) % PA) + PA) % PA;
        const B2 = (((uB[a] * xB[b] - uB[b] * xB[a]) % PB) + PB) % PB;
        const fastZero = (A2 === 0) && (B2 === 0);
        const perm = {}; perm[a] = u; perm[b] = x;
        const W2rows = [];
        for (let i = 0; i < 7; i++) W2rows.push(perm[i] !== undefined ? perm[i] : rows[i]);
        const d = ffDetNonzero(ctx6, W2rows, PA);
        if (d !== (!fastZero)) { bad++; console.log('B3 mismatch rows=' + rows + ' u=' + u + ' x=' + x + ' a=' + a + ' b=' + b); }
        trials++;
      }
    }
    check('B3 doubles functional', bad === 0 && trials >= 800, 'trials=' + trials + ' bad=' + bad);
  }

  // B4: triples both-prime zero <=> det of row-triple replacement (ref: ffDetNonzero)
  {
    let trials = 0, bad = 0;
    for (let iter = 0; iter < 4000 && trials < 1000; iter++) {
      const rows = rset(7);
      if (!ffDetNonzero(ctx6, rows, PA)) continue;
      const EA = gjInv(ctx6, rows, PA), EB = gjInv(ctx6, rows, PB);
      if (!EA || !EB) { bad++; continue; }
      const u = rvert(), z = rvert(), x = rvert();
      const uA = new Float64Array(7), uB = new Float64Array(7), zA = new Float64Array(7), zB = new Float64Array(7), xA = new Float64Array(7), xB = new Float64Array(7);
      sparseT(EA, ctx6, u, uA, PA); sparseT(EB, ctx6, u, uB, PB);
      sparseT(EA, ctx6, z, zA, PA); sparseT(EB, ctx6, z, zB, PB);
      sparseT(EA, ctx6, x, xA, PA); sparseT(EB, ctx6, x, xB, PB);
      const a = Math.floor(rnd() * 7) | 0;
      let b = Math.floor(rnd() * 7) | 0;
      let c = Math.floor(rnd() * 7) | 0;
      if (a === b || b === c || a === c) continue;
      const dA = det3mod(uA[a], uA[b], uA[c], zA[a], zA[b], zA[c], xA[a], xA[b], xA[c], PA);
      const dB = det3mod(uB[a], uB[b], uB[c], zB[a], zB[b], zB[c], xB[a], xB[b], xB[c], PB);
      const fastZero = (dA === 0) && (dB === 0);
      const perm = {}; perm[a] = u; perm[b] = z; perm[c] = x;
      const W3rows = [];
      for (let i = 0; i < 7; i++) W3rows.push(perm[i] !== undefined ? perm[i] : rows[i]);
      const d = ffDetNonzero(ctx6, W3rows, PA);
      if (d !== (!fastZero)) { bad++; console.log('B4 mismatch rows=' + rows + ' abc=' + a + b + c); }
      trials++;
    }
    check('B4 triples functional', bad === 0 && trials >= 300, 'trials=' + trials + ' bad=' + bad);
  }

  // B6: census vs brute for d=3,4 all sizes; d=5 sizes<=6
  {
    for (const d of [3, 4]) {
      const ctx = makeCtx(d);
      const ms = d === 3 ? 6 : 7;
      const c = censusRun(ctx, { maxSize: ms });
      const b = bruteCensus(ctx, ms);
      let ok = true;
      for (let s = 1; s <= ms; s++) if (c.counts[s] !== b[s]) { ok = false; console.log('B6 d=' + d + ' size=' + s + ' census=' + c.counts[s] + ' brute=' + b[s]); }
      check('B6 census-vs-brute d=' + d, ok);
    }
    {
      const ctx = makeCtx(5);
      const c = censusRun(ctx, { maxSize: 6 });
      const b = bruteCensus(ctx, 6);
      let ok = true;
      for (let s = 1; s <= 6; s++) if (c.counts[s] !== b[s]) { ok = false; console.log('B6 d=5 size=' + s + ' census=' + c.counts[s] + ' brute=' + b[s]); }
      check('B6 census-vs-brute d=5 (<=6)', ok);
    }
  }

  // B7: witness anchors
  {
    const w1 = [11, 22, 28, 37, 42, 49, 57, 58, 63];
    check('B7 published 9-witness GP', bruteIsGP(ctx6, w1) === true);
    const w2 = [0, 5, 6, 14, 21, 26, 35, 41, 52];
    check('B7 second 9-set GP', bruteIsGP(ctx6, w2) === true);
    const w1n = w1.map(v => v ^ 11).sort((a, b) => a - b);
    check('B7 normalized 9-witness GP 0-anchored', bruteIsGP(ctx6, w1n) === true && w1n[0] === 0);
    console.log('normalized witness = ' + w1n.join(','));
  }

  // B8: d=6 pairs with FULL gate brute re-verification
  {
    for (const [v2, mc] of [[62, 1e9], [61, 1e9], [58, 1e9], [45, 5e6], [40, 5e6], [35, 3e6]]) {
      const t1 = Date.now();
      const r = censusRun(ctx6, { v2, maxSize: 10, maxSelfChecks: mc });
      check('B8 selfcheck pair(0,' + v2 + ')', r.selfCheckFails === 0 && r.selfChecks > 0,
        'checks=' + r.selfChecks + ' ms=' + (Date.now() - t1) + ' counts=' + JSON.stringify(r.counts));
    }
  }

  // B9: v3-slicing consistency: sliced pair sums == whole pair (counts[2] aside, counted once per slice)
  {
    const whole = censusRun(ctx6, { v2: 45, maxSize: 10 });
    const s1 = censusRun(ctx6, { v2: 45, maxSize: 10, v3lo: 46, v3hi: 54 });
    const s2 = censusRun(ctx6, { v2: 45, maxSize: 10, v3lo: 55, v3hi: 63 });
    let ok = true;
    for (let sz = 3; sz <= 10; sz++) {
      if (whole.counts[sz] !== s1.counts[sz] + s2.counts[sz]) { ok = false; console.log('B9 size=' + sz + ' whole=' + whole.counts[sz] + ' sum=' + (s1.counts[sz] + s2.counts[sz])); }
    }
    check('B9 v3-slicing consistency', ok);
  }

  console.log('BATTERY ' + (fail === 0 ? 'PASS' : 'FAIL') + ' pass=' + pass + ' fail=' + fail + ' ms=' + (Date.now() - t0));
  process.exit(fail === 0 ? 0 : 1);
}

const mode = process.argv[2];
if (mode === 'battery') {
  battery();
} else if (mode === 'primes') {
  console.log('PA=' + PA + ' PB=' + PB);
} else if (mode === 'census') {
  const d = parseInt(process.argv[3]);
  const ms = parseInt(process.argv[4]) || (d === 6 ? 10 : 8);
  const ctx = makeCtx(d);
  const t0 = Date.now();
  const r = censusRun(ctx, { maxSize: ms });
  console.log(JSON.stringify({ d, counts: r.counts, nodes: r.nodes, witnesses: r.witnesses.length, ms: Date.now() - t0 }));
} else if (mode === 'task63') { // pair (0,v2) with third element restricted to [lo,hi]
  const v2 = parseInt(process.argv[3]);
  const lo = parseInt(process.argv[4]);
  const hi = parseInt(process.argv[5]);
  const ctx = makeCtx(6);
  const t0 = Date.now();
  const r = censusRun(ctx, { v2, maxSize: 10, v3lo: lo, v3hi: hi });
  console.log(JSON.stringify({ v2, lo, hi, counts: r.counts, nodes: r.nodes, nwit: r.witnesses.length, wlist: r.witnesses.slice(0, 20), ms: Date.now() - t0 }));
} else if (mode === 'task6') {
  const v2 = parseInt(process.argv[3]);
  const ctx = makeCtx(6);
  const t0 = Date.now();
  const r = censusRun(ctx, { v2, maxSize: 10 });
  console.log(JSON.stringify({ v2, counts: r.counts, nodes: r.nodes, nwit: r.witnesses.length, wlist: r.witnesses.slice(0, 20), ms: Date.now() - t0 }));
} else if (mode === 'check6') {
  const v2 = parseInt(process.argv[3]);
  const maxChecks = parseInt(process.argv[4]) || 2e6;
  const ctx = makeCtx(6);
  const t0 = Date.now();
  const r = censusRun(ctx, { v2, maxSize: 10, maxSelfChecks: maxChecks });
  console.log(JSON.stringify({ v2, counts: r.counts, selfChecks: r.selfChecks, selfCheckFails: r.selfCheckFails, ms: Date.now() - t0 }));
} else if (mode === 'walk') {
  const d = parseInt(process.argv[3]);
  const vs = process.argv.slice(4).map(Number).sort((a, b) => a - b);
  const ctx = makeCtx(d);
  console.log('bruteIsGP=' + bruteIsGP(ctx, vs));
} else {
  console.log('unknown mode');
  process.exit(1);
}
