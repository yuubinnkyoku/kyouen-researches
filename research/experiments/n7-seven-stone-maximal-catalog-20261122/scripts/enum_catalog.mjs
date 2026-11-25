// enum_catalog.mjs — complete enumeration of ALL safe maximal k-stone configurations
// on the n x n standard kyouen board (q = 4), by exhaustive DFS over cell subsets
// with incremental forbidden-quartet bookkeeping.
//
// Geometry source: pinned census.mjs (byte-identical to the published
// s12-s13-sat-stabilization-20261122 machinery, K0057-anchored) — cross-checked
// against the independent Python detector forbidgen.py (sha256-identical
// quartet catalog for n=5,6,7).
//
// Invariants (see README §method):
//  - A subset S is SAFE iff no forbidden quartet q has q ⊆ S.
//  - cov[c] := #{quartets q : c is the missing cell of q, |q ∩ S| = 3}.
//    Adding a stone at c is safe iff cov[c] == 0 (it would complete no quartet).
//  - A full k-subset S is MAXIMAL iff every empty cell has cov > 0
//    (every empty cell completes some quartet with 3 stones of S).
//  - DFS places stones at strictly increasing cell index; all prefixes of a
//    safe set are safe; all safe sets are reachable, because cov[c]==0
//    exactly marks cells whose addition keeps the prefix safe.
//
// Determinism: no randomness; two runs produce byte-identical output.
//
// Usage: node enum_catalog.mjs <n> <k> <out.jsonl>
// Output: JSONL — header, one {"type":"cfg","stones":[...]} per configuration,
// summary record with found/node counts and elapsed ms.

import { census, quartetList } from '../pinned/census.mjs';
import * as fs from 'node:fs';

const nArg = parseInt(process.argv[2], 10);
const kArg = parseInt(process.argv[3], 10);
const outPath = process.argv[4];
// optional shard spec: first stone's cell restricted to [rangeLo, rangeHi)
// (default 0..N). Every configuration has a unique smallest stone index, so
// the shards partition the search space; union of shard outputs = full run.
const rangeArg = process.argv[5];
let rangeLo = null, rangeHi = null;
if (rangeArg) {
  const m = rangeArg.match(/^(\d+):(\d+)$/);
  if (!m) throw new Error('bad range spec, expected lo:hi');
  rangeLo = parseInt(m[1], 10); rangeHi = parseInt(m[2], 10);
}
if (!(nArg >= 4 && nArg <= 9) || !(kArg >= 1) || !outPath) throw new Error('usage: node enum_catalog.mjs <n> <k> <out.jsonl>');

const cen = census(nArg);
const flat = quartetList(cen);
const F = flat.length / 4;
const N = nArg * nArg;
const k = kArg;
if (rangeLo === null) { rangeLo = 0; rangeHi = N; }

// quartet cells, ascending (cells < 81 for n<=9 → Uint8Array is safe)
const q4 = new Uint8Array(4 * F);
for (let q = 0; q < F; q++) {
  const a = [flat[4 * q], flat[4 * q + 1], flat[4 * q + 2], flat[4 * q + 3]].sort((x, y) => x - y);
  q4[4 * q] = a[0]; q4[4 * q + 1] = a[1]; q4[4 * q + 2] = a[2]; q4[4 * q + 3] = a[3];
}

// per-cell quartet membership (flat)
const deg = new Int32Array(N);
for (let q = 0; q < F; q++) for (let s = 0; s < 4; s++) deg[q4[4 * q + s]]++;
const cellQOff = new Int32Array(N + 1);
for (let c = 0; c < N; c++) cellQOff[c + 1] = cellQOff[c] + deg[c];
const cellQ = new Uint16Array(cellQOff[N]);
{
  const fill = new Int32Array(N);
  for (let q = 0; q < F; q++) for (let s = 0; s < 4; s++) {
    const c = q4[4 * q + s];
    cellQ[cellQOff[c] + fill[c]++] = q;
  }
}

const stInF = new Int32Array(F);
const cov = new Int32Array(N);
const stoneFlag = new Uint8Array(N);
const stones = new Int32Array(k);

// delta log: per recorded event, cell d and whether cov[d] was 0 before (u affected)
let deltaD = new Int32Array(16384);
let deltaZ = new Uint8Array(16384);
let deltaTop = 0;                          // next free slot
const deltaMark = new Int32Array(k);       // per-depth saved deltaTop before placement

let u = N;
let found = 0;
let nodes = 0;
const t0 = Date.now();

const fd = fs.openSync(outPath, 'w');
fs.writeSync(fd, JSON.stringify({ type: 'header', n: nArg, k, N, F: cen.F, D: cen.D, C: cen.C, rangeLo, rangeHi }) + '\n');

function place(c) {
  stoneFlag[c] = 1;
  u--;
  const off = cellQOff[c], end = cellQOff[c + 1];
  for (let i = off; i < end; i++) {
    const q = cellQ[i];
    stInF[q]++;
  }
  // second pass: quartets that hit 3 get their missing cell covered
  for (let i = off; i < end; i++) {
    const q = cellQ[i];
    if (stInF[q] === 3) {
      let d = -1;
      for (let t = 0; t < 4; t++) {
        const cc = q4[4 * q + t];
        if (cc !== c && !stoneFlag[cc]) { d = cc; break; }
      }
      if (d < 0) throw new Error('inconsistent quartet state (no missing cell)');
      if (deltaTop >= deltaD.length) {
        const nd = new Int32Array(deltaD.length * 2); nd.set(deltaD); deltaD = nd;
        const nz = new Uint8Array(deltaZ.length * 2); nz.set(deltaZ); deltaZ = nz;
      }
      const wasZero = cov[d] === 0;
      deltaD[deltaTop] = d; deltaZ[deltaTop] = wasZero ? 1 : 0; deltaTop++;
      cov[d]++;
      if (wasZero) u--;
    } else if (stInF[q] > 3) {
      throw new Error('quartet overfull — safety filter broken');
    }
  }
}

function unplace(c) {
  const off = cellQOff[c], end = cellQOff[c + 1];
  for (let i = off; i < end; i++) stInF[cellQ[i]]--;
  stoneFlag[c] = 0;
  u++;
}

function undoDeltas(mark) {
  while (deltaTop > mark) {
    deltaTop--;
    const d = deltaD[deltaTop];
    cov[d]--;
    if (deltaZ[deltaTop]) u++;
  }
}

function dfs(depth, start) {
  const limHi = depth === 0 ? rangeHi : N - (k - 1 - depth);
  for (let c = start; c < limHi; c++) {
    if (cov[c] > 0) continue;
    nodes++;
    deltaMark[depth] = deltaTop;
    const before = u;
    place(c);
    stones[depth] = c;
    if (depth === k - 1) {
      if (u === 0) {
        found++;
        const arr = new Array(k);
        for (let t = 0; t < k; t++) arr[t] = stones[t];
        fs.writeSync(fd, JSON.stringify({ type: 'cfg', stones: arr }) + '\n');
      }
    } else {
      dfs(depth + 1, c + 1);
    }
    undoDeltas(deltaMark[depth]);
    unplace(c);
    if (u !== before) throw new Error('u not restored');
  }
}

dfs(0, rangeLo);
fs.writeSync(fd, JSON.stringify({ type: 'summary', n: nArg, k, found, nodes, elapsedMs: Date.now() - t0, rangeLo, rangeHi }) + '\n');
fs.closeSync(fd);
console.log(JSON.stringify({ n: nArg, k, found, nodes, elapsedMs: Date.now() - t0, rangeLo, rangeHi }));
