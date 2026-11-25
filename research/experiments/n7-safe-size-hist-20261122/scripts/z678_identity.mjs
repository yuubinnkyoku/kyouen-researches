// z678_identity.mjs — identity gates for the safe-subset histogram coefficients λ=6,7,8:
//   Z_n(λ) = C(N,λ) - covered_λ
// where covered_λ = number of λ-cell subsets containing at least one forbidden quartet.
// Computed by DIRECT enumeration (quartet + λ-4 extra cells), NO DFS histogram machinery:
//   every (quartet, extra-cells) pair marks the resulting λ-set in a bitset indexed by the
//   COMBINATORIAL NUMBER SYSTEM (colex) rank of the λ-set, a bijection onto [0, C(N,λ));
//   covered_λ = popcount(bitset).
// Correctness self-check: the rank function is validated as a bijection by exhaustive
// permutation tests at (N=8,λ=6) and (N=9,λ=7) (assert all ranks distinct) at startup.
//
// Usage: node z678_identity.mjs <quartets_dir> [n ...]
//   reads <quartets_dir>/quartets_n<N>.txt (forbidgen catalog, header "n=..." skipped).
//   Default n = 3..7. Output: one JSON line per n with match flags against the published
//   Z_n values (K1228 n=3..6 spectrum, K1230 n=7 histogram).
// Determinism: no randomness, no timing in the output.
//
// Memory: worst case n=7 λ=8 → C(49,8)/8 ≈ 56.4 MB bitset; n=7 λ=7 → 10.7 MB.

import * as fs from 'node:fs';

const qdir = process.argv[2];
const ns = process.argv.slice(3).map(Number);
if (!qdir || ns.some(x => !x)) { console.error('usage: node z678_identity.mjs <quartets_dir> [n ...]'); process.exit(1); }
if (ns.length === 0) ns.push(3, 4, 5, 6, 7);
const LAMBDAS = [6, 7, 8];

// --- combinatorials C(m,r) exact for m<=60, r<=8 ---
const C = Array.from({ length: 61 }, () => new Float64Array(9));
for (let m = 0; m <= 60; m++) { C[m][0] = 1; for (let r = 1; r <= 8; r++) C[m][r] = r > m ? 0 : C[m - 1][r - 1] + C[m - 1][r]; }
const cnk = (m, r) => C[m][r];

// --- popcount table (16-bit) ---
const POP16 = new Uint8Array(65536);
for (let i = 1; i < 65536; i++) POP16[i] = POP16[i >> 1] + (i & 1);

// --- rank bijection self-test (exhaustive permutation test at small N) ---
function rankBijectionTest(N, k) {
  const seen = new Uint8Array(nk(N, k));
  let cnt = 0;
  const enumerate = (start, chosen) => {
    if (chosen.length === k) {
      const s = [...chosen].sort((a, b) => a - b);
      let rk = 0;
      for (let i = 0; i < k; i++) rk += cnk(s[i], i + 1);
      if (rk < 0 || rk >= seen.length || seen[rk]) throw new Error(`rank bijection FAIL at N=${N} set=${s}`);
      seen[rk] = 1; cnt++;
      return;
    }
    for (let c = start; c < N; c++) { chosen.push(c); enumerate(c + 1, chosen); chosen.pop(); }
  };
  enumerate(0, []);
  if (cnt !== nk(N, k)) throw new Error(`count FAIL N=${N} k=${k}`);
  return true;
}
const nk = (N, k) => cnk(N, k);
for (const [N, k] of [[8, 6], [9, 7]]) rankBijectionTest(N, k);

// --- popcount self-test: POP16 table vs naive per-bit loop (incl. odd array lengths) ---
{
  const naive = (bits) => { let p = 0; for (const b of bits) { let x = b; while (x) { x &= x - 1; p++; } } return p; };
  for (const len of [1, 2, 3, 7, 11, 12, 13, 513, 2048]) {
    const bits = new Uint8Array(len);
    for (let i = 0; i < len; i++) bits[i] = (i * 131 + 17) & 255;
    let s = 0;
    for (let i = 0; i < len; i++) s += POP16[bits[i]];
    if (s !== naive(bits)) throw new Error(`popcount FAIL len=${len}`);
  }
}

// --- covered_λ via bitset of colex ranks ---
function coveredK(quads, N, k) {
  const total = nk(N, k);
  const bits = new Uint8Array((total >> 3) + 1);
  const cells = new Int32Array(k);
  const K4 = k - 4;
  for (let qi = 0; qi < quads.length; qi++) {
    const q = quads[qi];
    const inQ = new Set(q);
    const free = [];
    for (let c = 0; c < N; c++) if (!inQ.has(c)) free.push(c);
    const extras = new Int32Array(K4);
    const rec = (start, chosenLen) => {
      if (chosenLen === K4) {
        let i0 = 0, i1 = 0, m = 0;
        while (i0 < 4 && i1 < K4) cells[m++] = q[i0] < extras[i1] ? q[i0++] : extras[i1++];
        while (i0 < 4) cells[m++] = q[i0++];
        while (i1 < K4) cells[m++] = extras[i1++];
        let rk = 0;
        for (let i = 0; i < k; i++) rk += cnk(cells[i], i + 1);
        bits[rk >> 3] |= 1 << (rk & 7);
        return;
      }
      for (let idx = start; idx < free.length; idx++) {
        extras[chosenLen] = free[idx];
        rec(idx + 1, chosenLen + 1);
      }
    };
    rec(0, 0);
  }
  let pop = 0;
  for (let i = 0; i < bits.length; i++) pop += POP16[bits[i]];
  return pop;
}

// Published Z_n(λ) for λ=6,7,8: K1228 (n=3..6), K1230 (n=7). null = not published there.
const PUBLISHED = {
  3: [0, 0, 0],
  4: [1064, 64, 0],
  5: [59192, 35208, 5172],
  6: [997796, 1783296, 1459292],
  7: [8796600, 29688640, 56927728],
};

for (const n of ns) {
  const N = n * n;
  const qt = fs.readFileSync(`${qdir}/quartets_n${n}.txt`, 'utf8').split('\n').filter(t => t && !t.startsWith('n='));
  const quads = qt.map(r => r.split(' ').map(Number));
  const F = quads.length;
  const rec = { n, N, F };
  const pub = PUBLISHED[n] ?? [null, null, null];
  LAMBDAS.forEach((lam, j) => {
    const Cl = cnk(N, lam);
    const cov = coveredK(quads, N, lam);
    const z = Cl - cov;
    rec[`C${lam}`] = Cl;
    rec[`covered${lam}`] = cov;
    rec[`z${lam}_identity`] = z;
    rec[`z${lam}_published`] = pub[j];
    rec[`z${lam}_match`] = pub[j] === null ? null : pub[j] === z;
  });
  console.log(JSON.stringify(rec));
}
