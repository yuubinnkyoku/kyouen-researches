// crosscheck.js — independent brute-force cross-check of stripsearch.js for
// small R. Enumerates ALL representation pairs (X=q*u, Z) with X^2+Z^2 = R <= C,
// X === 0 mod q, gcd(Z,q)=1 (q in {1,2,4,8}), buckets them by R, and directly
// tests every 7-slot window (step 2q) for >=10-point configurations with the
// full semantic (doubles u>0 with consistent parity; tangents u=0 counted only
// when all double u's are even). No divisor-pair reasoning is used.
'use strict';
const C = Number(process.argv[2] || 1e7);
const t0 = Date.now();
const QS = [1, 2, 4, 8];

const res = [];
for (const q of QS) {
  // collect (R -> [{u, Z}]) for q^2 u^2 + Z^2 <= C, gcd(Z,q)=1
  const UMAX = Math.floor(Math.sqrt(C)) / q | 0;
  const ZMAX = Math.floor(Math.sqrt(C));
  const map = new Map();
  for (let Z = -ZMAX; Z <= ZMAX; Z++) {
    // q in {2,4,8}: window members must satisfy gcd(Z,q)=1 -> Z odd; Z=0 excluded
    if (q > 1 && (Z === 0 || (Z & 1) === 0)) continue;
    const Zr2 = Z * Z;
    for (let u = 0; u <= UMAX; u++) {
      const R = q * q * u * u + Zr2;
      if (R > C) break;
      if (R === 0) continue;
      let l = map.get(R); if (!l) { l = []; map.set(R, l); }
      l.push({ u, Z });
    }
  }
  // test windows per R
  const qual = [];
  for (const [R, reps] of map) {
    if (reps.length < 5) continue;
    const byZ = new Map();
    for (const r of reps) { if (!byZ.has(r.Z)) byZ.set(r.Z, r.u); }
    const zs = [...byZ.keys()].sort((a, b) => a - b);
    if (zs.length < 5) continue;
    // windows: 7-term AP step 2q. Try all starts among zs[i]-2q*6..zs[i]
    const starts = new Set();
    for (const z of zs) for (let k = 0; k <= 6; k++) starts.add(z - 2 * q * k);
    for (const s of starts) {
      let dbl = 0, tng = 0, ok = true, par = null;
      for (let i = 0; i < 7; i++) {
        const z = s + 2 * q * i;
        if (!byZ.has(z)) continue;
        const u = byZ.get(z);
        if (u === 0) { tng++; continue; }
        if (par === null) par = u & 1;
        else if ((u & 1) !== par) { ok = false; break; }
        dbl++;
      }
      if (!ok) continue;
      const allEven = par === 0;
      const points = 2 * dbl + (allEven ? tng : 0);
      if (points >= 10) qual.push({ q, R, s, dbl, tng, allEven, points });
    }
  }
  res.push({ q, repsTotal: map.size, qual });
}
console.log(JSON.stringify({ schema: 1, tool: 'crosscheck.js', C, elapsedSec: Number(((Date.now() - t0) / 1000).toFixed(1)), results: res }, null, 1));
