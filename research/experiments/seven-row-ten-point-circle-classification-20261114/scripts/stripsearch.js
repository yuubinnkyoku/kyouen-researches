// stripsearch.js — exhaustive search for circle configurations with >=10 lattice
// points inside 7 consecutive integer rows (a "7-row strip"), without any width
// bound on x. Configurations are classified by (q, R) where
//   2*beta = p/q in lowest terms (q = denominator of the center-y*2),
//   doubles at rows y have integer half-chords u_y>0 with
//     (q*u_y)^2 + Z_y^2 = R,  Z_y = 2q*y - p  (Z's form a 7-term AP, step 2q),
//   tangents have u_y = 0 (single point, valid only if the common center-x
//   alpha is integral, i.e. all double u's are even).
//
// Structural lemmas used to make the search finite (see report for proofs):
//  L1: >=10 points in <=7 rows requires >=5 double rows, or 4 doubles + 2 tangent
//      rows (each row has <=2 points; singles with t!=0 are impossible once a
//      double exists, since alpha in (1/2)Z then forces t in (1/2)Z).
//  L2: with >=5 doubles in rows 0..6, some two double rows are adjacent
//      (5 rows in 7 slots), giving q | 4; with 4 doubles + 2 tangents the six
//      rows force q | 8, and both tangents in the 7-window force Z_t = +-sqrt(R)
//      with 2*Z_t <= 12q -> also q | Z_t, but gcd(Z_t,q)=1 -> q=1, R<=36.
//  L3: for q in {2,4} the adjacent-double relation q(u^2-u'^2) = 4(Z+q) is
//      unsolvable / parity-inconsistent (Z odd), so 5-double configs have q=1.
// Hence the exhaustive search reduces to:
//  (A)  q=1, adjacent (delta=1) double pairs (Z, Z+2), all R <= B;
//  (A') q=1, the symmetric pair (Z,Z+2)=(-1,1) (u=u'), R = u^2+1 <= B;
//  (B)  q=1, 4 doubles + 2 tangents, R = Zt^2 <= 36.
// Any configuration with R <= B is found; qualifying ones (>=10 points) reported.
'use strict';
const B = Number(process.argv[2] || 1e12);
const ZMAX = Math.floor(Math.sqrt(B)) + 2;
const t0 = Date.now();

// SPF sieve up to ZMAX+2 for factoring |Z+1|.
const SPFN = ZMAX + 3;
const spf = new Int32Array(SPFN);
for (let i = 2; i < SPFN; i++) {
  if (spf[i] === 0) {
    for (let j = i; j < SPFN; j += i) if (spf[j] === 0) spf[j] = i;
  }
}
function isqrt(v) {
  if (v < 0) return -1;
  let x = Math.floor(Math.sqrt(v));
  while (x * x > v) x--;
  while ((x + 1) * (x + 1) <= v) x++;
  return x;
}

const qual = new Map();   // R -> Set of window-start (canonicalized by reflection to min)
let nearMiss4 = 0;        // windows with exactly 4 doubles, R <= B (informational)
let pairs = 0, survived = 0;

function record(R, wStart, dbl, tng, uParOk, points) {
  const key = R + '|' + wStart;
  if (!qual.has(key)) qual.set(key, { R, wStart, dbl, tng, uParOk, points });
}

// full window scan for a candidate (R, pair Z at row y). Window slots:
// W_i = Z + 2*(i - y), i=0..6. Count doubles/tangents with parity consistency.
function scanWindows(R, Z, uRef) {
  for (let y = 0; y <= 5; y++) {
    let dbl = 0, tng = 0, ok = true;
    for (let i = 0; i < 7; i++) {
      const z = Z + 2 * (i - y);
      const V = R - z * z;
      if (V < 0) continue;
      const X = isqrt(V);
      if (X * X !== V) continue;
      if (X === 0) { tng++; continue; }
      if ((X & 1) !== (uRef & 1)) { ok = false; break; } // center-x parity conflict
      dbl++;
    }
    if (!ok) continue;
    const allEven = uRef % 2 === 0;
    const points = 2 * dbl + (allEven ? tng : 0);
    if (points >= 10) record(R, Z - 2 * y, dbl, tng, allEven, points);
    else if (points === 8 && dbl === 4 && tng === 0) nearMiss4++;
  }
}

// ---- Case A: q=1, adjacent double pair (Z, Z+2), Z != -1 ----
for (let Z = -ZMAX - 2; Z <= ZMAX; Z++) {
  if (Z === -1) continue;
  const H = Math.abs(4 * (Z + 1)); // (u_close-u_far)(u_close+u_far)
  // factor H: pull powers of 2 from |Z+1| via spf on odd part
  let n = Z + 1; if (n < 0) n = -n; // <= ZMAX+1
  // collect prime factorization of H from spf[n] (n>=1; n=0 impossible since Z!=-1)
  const primes = [], exps = [];
  let m = n;
  while (m > 1) { const f = spf[m]; let e = 0; while (m % f === 0) { m /= f; e++; } primes.push(f); exps.push(e); }
  // H = 4n: add 2^2
  {
    let pi = primes.indexOf(2);
    if (pi >= 0) exps[pi] += 2; else { primes.push(2); exps.push(2); }
  }
  // enumerate divisors a of H with a <= b=H/a, a===b (mod 2)
  const nd = primes.length;
  const divs = [];
  (function rec(idx, d) {
    if (idx === nd) { divs.push(d); return; }
    let p = 1;
    for (let e = 0; e <= exps[idx]; e++) { rec(idx + 1, d * p); p *= primes[idx]; }
  })(0, 1);
  const zc = Math.abs(Z) < Math.abs(Z + 2) ? Z : Z + 2; // closer-to-zero member
  for (const a of divs) {
    const b = H / a;
    if (a > b) continue;
    if (((a ^ b) & 1)) continue; // need same parity
    const uBig = (a + b) / 2, uSm = (b - a) / 2;
    if (uSm === 0) continue; // handled by case A'
    const R = uBig * uBig + zc * zc;
    if (R > B) continue;
    pairs++;
    // fast filter: >=3 more good candidates among the 11 non-pair slots
    let good = 0;
    const cand = [];
    for (let k = 1; k <= 6; k++) { cand.push(Z - 2 * k); }
    for (let k = 1; k <= 5; k++) { cand.push(Z + 2 + 2 * k); }
    for (const z of cand) {
      const V = R - z * z; if (V < 0) continue;
      const X = isqrt(V); if (X * X !== V || X === 0) continue;
      if ((X & 1) !== (uBig & 1)) continue;
      good++;
    }
    if (good < 3) continue;
    survived++;
    scanWindows(R, Z, uBig);
  }
}

// ---- Case A': q=1, symmetric pair (-1, 1), u = u' ----
for (let u = 1; u * u + 1 <= B; u++) {
  const R = u * u + 1;
  // pair (-1,1): fast filter on the 11 candidates around them
  let good = 2; const cand = [];
  for (let k = 2; k <= 7; k++) cand.push(-1 - 2 * k + 2); // -1-2(k-1)
  for (let k = 1; k <= 6; k++) cand.push(1 + 2 * k);
  let ok = true;
  for (const z of cand) {
    const V = R - z * z; if (V < 0) continue;
    const X = isqrt(V); if (X * X !== V || X === 0) continue;
    if ((X & 1) !== (u & 1)) continue;
    good++;
  }
  if (good < 5) continue;
  scanWindows(R, -1, u);
}

// ---- Case B: q=1, 4 doubles + 2 tangents; both tangents in window -> R = Zt^2 <= 36 ----
for (let Zt = 1; Zt <= 6; Zt++) {
  const R = Zt * Zt;
  // windows (odd parity if Zt odd, even if even) containing both -Zt and Zt
  for (let s = -Zt - 12; s <= -Zt + 12; s++) {
    if (Math.abs(s - Zt) % 2 !== 0) continue;
    const slots = []; for (let i = 0; i < 7; i++) slots.push(s + 2 * i);
    if (!slots.includes(-Zt) || !slots.includes(Zt)) continue;
    let dbl = 0, tng = 0, ok = true, upar = null;
    for (const z of slots) {
      if (z === Zt || z === -Zt) { tng++; continue; }
      const V = R - z * z; if (V < 0) continue;
      const X = isqrt(V); if (X * X !== V) continue;
      if (X === 0) { tng++; continue; }
      if (X % 2 !== 0) { ok = false; break; } // tangents need alpha integral -> all u even
      dbl++;
    }
    if (ok && 2 * dbl + tng >= 10) record(R, s, dbl, tng, true, 2 * dbl + tng);
  }
}

const out = {
  schema: 1, tool: 'stripsearch.js', B, zmax: ZMAX,
  elapsedSec: Number(((Date.now() - t0) / 1000).toFixed(1)),
  pairsTested: pairs, pairsSurvivedFilter: survived, nearMiss4Windows: nearMiss4,
  qualifying: [...qual.values()].sort((x, y) => x.R - y.R || x.wStart - y.wStart)
};
console.log(JSON.stringify(out));
