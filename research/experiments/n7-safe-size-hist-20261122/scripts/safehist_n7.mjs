// safehist_n7.mjs — complete safe-subset size histogram Z_n(λ) for the n x n
// standard kyouen board (q = 4), by exhaustive DFS over the safe-prefix tree.
//
// Semantics (re-derived independently here, matching dfs_py.py --safehist of the
// published n3-n6-safe-histograms-sat-crosscheck-20261122 machinery):
//   A subset S of cells is SAFE iff no forbidden quartet Q satisfies Q ⊆ S.
//   The DFS places stones at strictly increasing cell index. All prefixes of a
//   safe set are safe; every safe set is reachable, because a cell c is
//   placeable on prefix P exactly when adding c keeps P ∪ {c} quartet-free,
//   which is tracked incrementally by cov[]:
//     stInF[q]  = # stones of the current prefix inside quartet q
//     cov[c]    = # quartets q ∋ c with stInF[q] == 3 (adding c would complete q)
//   A cell c is placeable iff cov[c] == 0.
//   Every node of the DFS tree (each safe prefix, including the empty set) is
//   histogrammed at hist[|S|].
//
// Geometry source: canonical quartets text (forbidgen.py det-brute-force
// catalog; sha256 cross-checked byte-identical against census.mjs machinery
// for n=3..7 by crosscheck_catalog_n7.mjs).
//
// Determinism: no randomness, no timing in the output file; two runs produce
// byte-identical files. Timing metadata is printed to stdout only.
//
// Usage: node safehist_n7.mjs <n> <quartets.txt> <out.jsonl> [rangeLo:rangeHi]
// Optional shard spec restricts the FIRST stone of each set to cells
// [rangeLo, rangeHi); shards partition all safe sets exactly once because each
// set has a unique smallest cell index. Root (empty set) is attributed to the
// shard with rangeLo == 0 only, so shard sums add up with no double counting.

import * as fs from 'node:fs';
import { createHash } from 'node:crypto';

const n = parseInt(process.argv[2], 10);
const quartetsPath = process.argv[3];
const outPath = process.argv[4];
const rangeArg = process.argv[5] ?? null;
let rangeLo = 0, rangeHi = n * n;
if (rangeArg !== null) {
  const m = rangeArg.match(/^(\d+):(\d+)$/);
  if (!m) throw new Error('bad range spec');
  rangeLo = parseInt(m[1], 10);
  rangeHi = parseInt(m[2], 10);
}
if (!(n >= 3 && n <= 9) || !quartetsPath || !outPath) {
  throw new Error('usage: node safehist_n7.mjs <n> <quartets.txt> <out.jsonl> [lo:hi]');
}

const N = n * n;
const qt = fs.readFileSync(quartetsPath, 'utf8').split('\n').filter(t => t && !t.startsWith('n='));
const F = qt.length;
const qTextSha = createHash('sha256').update(fs.readFileSync(quartetsPath)).digest('hex');

// quartet cells ascending
const q4 = new Uint8Array(4 * F);
{
  for (let q = 0; q < F; q++) {
    const a = qt[q].split(' ').map(Number);
    if (a.length !== 4 || a.some(x => !Number.isInteger(x) || x < 0 || x >= N) ||
        !(a[0] < a[1] && a[1] < a[2] && a[2] < a[3])) {
      throw new Error('bad quartet row: ' + qt[q]);
    }
    q4.set(a, 4 * q);
  }
}

// per-cell quartet membership (CSR)
const deg = new Int32Array(N);
for (let q = 0; q < F; q++) for (let s = 0; s < 4; s++) deg[q4[4 * q + s]]++;
const cellQOff = new Int32Array(N + 1);
for (let c = 0; c < N; c++) cellQOff[c + 1] = cellQOff[c] + deg[c];
const cellQ = new Int32Array(cellQOff[N]);
{
  const fill = new Int32Array(N);
  for (let q = 0; q < F; q++) for (let s = 0; s < 4; s++) {
    const c = q4[4 * q + s];
    cellQ[cellQOff[c] + fill[c]++] = q;
  }
}

const stInF = new Int32Array(F);    // stones per quartet
const cov = new Int32Array(N);      // covered (unplaceable) cell count
const stoneFlag = new Uint8Array(N);
const MAXDEPTH = N;
const hist = new Float64Array(MAXDEPTH + 1); // counts < 2^53 stay exact

// delta log for cov undo
let deltaD = new Int32Array(1 << 16);
let deltaTop = 0;

function place(c) {
  stoneFlag[c] = 1;
  const off = cellQOff[c], end = cellQOff[c + 1];
  for (let i = off; i < end; i++) stInF[cellQ[i]]++;
  for (let i = off; i < end; i++) {
    const q = cellQ[i];
    if (stInF[q] === 3) {
      let d = -1;
      for (let t = 0; t < 4; t++) {
        const cc = q4[4 * q + t];
        if (cc !== c && !stoneFlag[cc]) { d = cc; break; }
      }
      if (d < 0) throw new Error('inconsistent quartet state');
      if (deltaTop >= deltaD.length) {
        const nd = new Int32Array(deltaD.length * 2);
        nd.set(deltaD); deltaD = nd;
      }
      deltaD[deltaTop++] = d;
      cov[d]++;
    } else if (stInF[q] > 3) {
      throw new Error('quartet overfull — safety filter broken');
    }
  }
}

function unplace(c) {
  // cov deltas are undone by the caller via undoDeltas() BEFORE this call.
  const off = cellQOff[c], end = cellQOff[c + 1];
  for (let i = off; i < end; i++) stInF[cellQ[i]]--;
  stoneFlag[c] = 0;
}

function undoDeltas(mark) {
  while (deltaTop > mark) {
    deltaTop--;
    cov[deltaD[deltaTop]]--;
  }
}

function dfs(start, depth) {
  hist[depth]++;
  for (let c = start; c < N; c++) {
    if (cov[c] > 0) continue;
    const mark = deltaTop;
    place(c);
    dfs(c + 1, depth + 1);
    undoDeltas(mark);
    unplace(c);
  }
}

const t0 = Date.now();

if (rangeLo === 0) hist[0]++;
for (let c = rangeLo; c < rangeHi; c++) {
  if (cov[c] > 0) continue;
  const mark = deltaTop;
  place(c);
  dfs(c + 1, 1);
  undoDeltas(mark);
  unplace(c);
}

let dens = '';
{
  let sum = 0, mx = -1;
  const obj = {};
  for (let s = 0; s <= MAXDEPTH; s++) {
    const v = hist[s];
    if (v > 0) { obj[s] = v; sum += v; mx = s; }
  }
  dens = JSON.stringify(obj);
  const fd = fs.openSync(outPath, 'w');
  fs.writeSync(fd, JSON.stringify({ type: 'header', impl: 'cov', n, N, F, quartets_sha256: qTextSha, first_stone_range: [rangeLo, rangeHi] }) + '\n');
  fs.writeSync(fd, JSON.stringify({ type: 'safehist', impl: 'cov', histogram: dens, total_safe_subsets: sum, max_safe_size: mx }) + '\n');
  fs.closeSync(fd);
  console.log(JSON.stringify({ n, impl: 'cov', rangeLo, rangeHi, total: sum, maxSafe: mx, elapsedMs: Date.now() - t0 }));
}
