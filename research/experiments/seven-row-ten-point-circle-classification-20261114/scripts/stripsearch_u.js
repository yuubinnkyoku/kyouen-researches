// stripsearch_u.js — chord-bounded exhaustive search for circle configurations
// with >=10 lattice points inside 7 consecutive integer rows. Companion to
// stripsearch.js (which bounds R); here the bound is the maximum chord length
// UMAX = max double-row chord (u), which is exactly the constraint for a circle
// to fit in a 7 x m grid with m = UMAX+1 (all 10 points must have distinct
// x-coords within [0, m-1] per row pair). The search is exhaustive over ALL R:
// the adjacent-double-pair relation (u-u')(u+u') = 4|Z+1| bounds |Z| <= UMAX^2/4
// once both chords are <= UMAX, so the enumeration is finite and complete.
// Case analysis (q-denominator lemmas) identical to stripsearch.js: q=1 only.
'use strict';
const UMAX = Number(process.argv[2] || 1078);
const ZMAX = Math.floor(UMAX * UMAX / 4) + 2; // |Z+1| <= (u u')(pair)/4 <= UMAX^2/4
const t0 = Date.now();

const SPFN = ZMAX + 3;
const spf = new Int32Array(SPFN);
for (let i = 2; i < SPFN; i++) if (spf[i] === 0) for (let j = i; j < SPFN; j += i) if (spf[j] === 0) spf[j] = i;
function isqrt(v) { if (v < 0) return -1; let x = Math.floor(Math.sqrt(v)); while (x * x > v) x--; while ((x + 1) * (x + 1) <= v) x++; return x; }

const qual = new Map();
let nearMiss4 = 0, pairs = 0, survived = 0;
function record(R, wStart, dbl, tng, allEven, points, maxu) {
  const key = R + '|' + wStart;
  if (!qual.has(key)) qual.set(key, { R, wStart, dbl, tng, allEven, points, maxu });
}
function scanWindows(R, Z, uRef) {
  for (let y = 0; y <= 5; y++) {
    let dbl = 0, tng = 0, ok = true, maxu = 0;
    for (let i = 0; i < 7; i++) {
      const z = Z + 2 * (i - y);
      const V = R - z * z; if (V < 0) continue;
      const X = isqrt(V); if (X * X !== V) continue;
      if (X === 0) { tng++; continue; }
      if ((X & 1) !== (uRef & 1)) { ok = false; break; }
      if (X > UMAX) { ok = false; break; }
      dbl++; if (X > maxu) maxu = X;
    }
    if (!ok) continue;
    const allEven = uRef % 2 === 0;
    const points = 2 * dbl + (allEven ? tng : 0);
    if (points >= 10) record(R, Z - 2 * y, dbl, tng, allEven, points, maxu);
    else if (points === 8 && dbl === 4 && tng === 0) nearMiss4++;
  }
}

// Case A: adjacent double pair (Z, Z+2), Z != -1
for (let Z = -ZMAX - 2; Z <= ZMAX; Z++) {
  if (Z === -1) continue;
  const H = Math.abs(4 * (Z + 1));
  let n = Z + 1; if (n < 0) n = -n;
  const primes = [], exps = [];
  let m = n;
  while (m > 1) { const f = spf[m]; let e = 0; while (m % f === 0) { m /= f; e++; } primes.push(f); exps.push(e); }
  { const pi = primes.indexOf(2); if (pi >= 0) exps[pi] += 2; else { primes.push(2); exps.push(2); } }
  const nd = primes.length; const divs = [];
  (function rec(idx, d) { if (idx === nd) { divs.push(d); return; } let p = 1; for (let e = 0; e <= exps[idx]; e++) { rec(idx + 1, d * p); p *= primes[idx]; } })(0, 1);
  const zc = Math.abs(Z) < Math.abs(Z + 2) ? Z : Z + 2;
  for (const a of divs) {
    const b = H / a; if (a > b) continue;
    if (((a ^ b) & 1)) continue;
    const uBig = (a + b) / 2, uSm = (b - a) / 2;
    if (uSm === 0) continue;
    if (uBig > UMAX) continue;
    const R = uBig * uBig + zc * zc;
    pairs++;
    let good = 0; const cand = [];
    for (let k = 1; k <= 6; k++) cand.push(Z - 2 * k);
    for (let k = 1; k <= 5; k++) cand.push(Z + 2 + 2 * k);
    for (const z of cand) {
      const V = R - z * z; if (V < 0) continue;
      const X = isqrt(V); if (X * X !== V || X === 0 || X > UMAX) continue;
      if ((X & 1) !== (uBig & 1)) continue;
      good++;
    }
    if (good < 3) continue;
    survived++;
    scanWindows(R, Z, uBig);
  }
}

// Case A': symmetric pair (-1,1), u = u' <= UMAX
for (let u = 1; u <= UMAX; u += 2) { // parity: window doubles share u parity; u and its mirror...
  const R = u * u + 1;
  let good = 2; const cand = [];
  for (let k = 1; k <= 6; k++) cand.push(-1 - 2 * k);
  for (let k = 1; k <= 5; k++) cand.push(1 + 2 * k);
  for (const z of cand) {
    const V = R - z * z; if (V < 0) continue;
    const X = isqrt(V); if (X * X !== V || X === 0 || X > UMAX) continue;
    if ((X & 1) !== (u & 1)) continue;
    good++;
  }
  if (good >= 5) scanWindows(R, -1, u);
}
// even u too (all-even parity classes allowed; tangents may mix)
for (let u = 2; u <= UMAX; u += 2) {
  const R = u * u + 1;
  let good = 2; const cand = [];
  for (let k = 1; k <= 6; k++) cand.push(-1 - 2 * k);
  for (let k = 1; k <= 5; k++) cand.push(1 + 2 * k);
  for (const z of cand) {
    const V = R - z * z; if (V < 0) continue;
    const X = isqrt(V); if (X * X !== V || X === 0 || X > UMAX) continue;
    if ((X & 1) !== (u & 1)) continue;
    good++;
  }
  if (good >= 5) scanWindows(R, -1, u);
}

// Case B: 4 doubles + 2 tangents, R = Zt^2 <= 36
for (let Zt = 1; Zt <= 6; Zt++) {
  const R = Zt * Zt;
  for (let s = -Zt - 12; s <= -Zt + 12; s++) {
    if (Math.abs(s - Zt) % 2 !== 0) continue;
    const slots = []; for (let i = 0; i < 7; i++) slots.push(s + 2 * i);
    if (!slots.includes(-Zt) || !slots.includes(Zt)) continue;
    let dbl = 0, tng = 0, ok = true, maxu = 0;
    for (const z of slots) {
      if (z === Zt || z === -Zt) { tng++; continue; }
      const V = R - z * z; if (V < 0) continue;
      const X = isqrt(V); if (X * X !== V) continue;
      if (X === 0) { tng++; continue; }
      if (X % 2 !== 0 || X > UMAX) { ok = false; break; }
      dbl++; if (X > maxu) maxu = X;
    }
    if (ok && 2 * dbl + tng >= 10) record(R, s, dbl, tng, true, 2 * dbl + tng, maxu);
  }
}

const out = {
  schema: 1, tool: 'stripsearch_u.js', UMAX, zmax: ZMAX,
  elapsedSec: Number(((Date.now() - t0) / 1000).toFixed(1)),
  pairsTested: pairs, pairsSurvivedFilter: survived, nearMiss4Windows: nearMiss4,
  qualifying: [...qual.values()].sort((x, y) => x.R - y.R || x.wStart - y.wStart)
};
console.log(JSON.stringify(out));
