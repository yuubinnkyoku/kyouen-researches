// z9_identity.mjs — identity gate for the safe-subset histogram coefficient λ=9:
//   Z_n(9) = C(N,9) - covered9
// where covered9 = number of 9-cell subsets containing at least one forbidden quartet.
// Same DIRECT bitset method as z678_identity.mjs (colex-rank bitset, no DFS machinery),
// sharded by QUARTET INDEX RANGE with the bitset persisted to a file between runs
// (a covered 9-set containing several quartets is generated once per containing quartet,
// so the bitset must be shared across shards; sharding by quartet ranges keeps the
// dedup global while bounding each run's work).
// Self-tests at startup: rank bijection (exhaustive, small N) as in z678_identity.mjs.
//
// Usage: node z9_identity.mjs <quartets_dir> <n> <bits_file> <lo> <hi>
//   processes quartets [lo,hi) of quartets_n<n>.txt; loads <bits_file> if present,
//   ORs in this shard's marks, and rewrites <bits_file>. Prints a JSON line with the
//   running popcount; when hi == F it also prints the final match line against the
//   published Z_n(9) (K1228 n=3..6, K1230 n=7).
// Determinism: no randomness, no timing in the output.

import * as fs from 'node:fs';

const qdir = process.argv[2];
const n = parseInt(process.argv[3], 10);
const bitsFile = process.argv[4];
const lo = parseInt(process.argv[5], 10);
const hi = process.argv[6] === 'POP' ? 'POP' : parseInt(process.argv[6], 10);
const popOnly = hi === 'POP';
if (!qdir || !(n > 0) || !bitsFile || !popOnly && (!(lo >= 0) || !(hi > lo))) {
  console.error('usage: node z9_identity.mjs <quartets_dir> <n> <bits_file> <lo> <hi>');
  process.exit(1);
}
const K = 9;

// --- combinatorials ---
const C = Array.from({ length: 61 }, () => new Float64Array(10));
for (let m = 0; m <= 60; m++) { C[m][0] = 1; for (let r = 1; r <= 9; r++) C[m][r] = r > m ? 0 : C[m - 1][r - 1] + C[m - 1][r]; }
const cnk = (m, r) => C[m][r];

// --- rank bijection self-test ---
{
  const testN = 10, testK = 8;
  const seen = new Uint8Array(cnk(testN, testK));
  let cnt = 0;
  const enumerate = (start, chosen) => {
    if (chosen.length === testK) {
      let rk = 0;
      for (let i = 0; i < testK; i++) rk += cnk(chosen[i], i + 1);
      if (rk < 0 || rk >= seen.length || seen[rk]) throw new Error('rank bijection FAIL');
      seen[rk] = 1; cnt++;
      return;
    }
    for (let c = start; c < testN; c++) { chosen.push(c); enumerate(c + 1, chosen); chosen.pop(); }
  };
  enumerate(0, []);
  if (cnt !== cnk(testN, testK)) throw new Error('rank count FAIL');
}

const N = n * n;
const qt = fs.readFileSync(`${qdir}/quartets_n${n}.txt`, 'utf8').split('\n').filter(t => t && !t.startsWith('n='));
const quads = qt.map(r => r.split(' ').map(Number));
const F = quads.length;
const hiC = popOnly ? F : Math.min(hi, F);
const total = cnk(N, K);
const bits = new Uint8Array((total >> 3) + 1);
if (fs.existsSync(bitsFile)) {
  const prev = fs.readFileSync(bitsFile);
  if (prev.length !== bits.length) { console.error(`bits file size ${prev.length} != expected ${bits.length}`); process.exit(1); }
  bits.set(prev);
}

const cells = new Int32Array(K);
const K4 = K - 4;
for (let qi = popOnly ? F : lo; qi < hiC; qi++) {
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
      for (let i = 0; i < K; i++) rk += cnk(cells[i], i + 1);
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

// persist only when this run added marks
if (!popOnly) {
  const tmp = bitsFile + '.tmp';
  fs.writeFileSync(tmp, bits);
  fs.renameSync(tmp, bitsFile);
}

// popcount per byte (correct for any length incl. odd; see z678 tail-byte bug note)
let pop = 0;
const POP8 = new Uint8Array(256);
for (let i = 1; i < 256; i++) POP8[i] = POP8[i >> 1] + (i & 1);
for (let i = 0; i < bits.length; i++) pop += POP8[bits[i]];

const done = hiC === F;
const out = { lambda: 9, n, N, F, range: popOnly ? 'popcount-only audit of persisted bitset' : [lo, hiC], covered_running: pop };
if (done) {
  const PUBLISHED = { 3: 0, 4: 0, 5: 100, 6: 438952, 7: 55173324 };
  const z9 = total - pop;
  out.C9 = total;
  out.covered9 = pop;
  out.z9_identity = z9;
  out.z9_published = PUBLISHED[n] ?? null;
  out.z9_match = (PUBLISHED[n] ?? null) === null ? null : PUBLISHED[n] === z9;
}
console.log(JSON.stringify(out));
