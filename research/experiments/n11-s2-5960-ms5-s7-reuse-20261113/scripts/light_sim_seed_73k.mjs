#!/usr/bin/env node
// Light seeding simulator for the cost-73k merged worker-memo seed
// (K0909 follow-up: N-way merge seed capacity design, 2026-11-17).
//
// Replicates the repo-verbatim extractor's memoEntry() insertion semantics
// EXACTLY for the seed phase:
//   - mHash(): h = ((imul(M0,73856093)^imul(M1,19349663)^
//                  imul(M2,83492791)^imul(M3,39916801))>>>0)&MM
//     (line verbatim from class4_child1_cert_extractor_exact.ts blob 52bcaf50)
//   - probe: 64-slot linear probing from h, insert at first empty slot,
//     wrap at MM; failure when all 64 slots are occupied.
// The merged seed table contains DISTINCT keys only (merge_pass_nway
// writes each key union element exactly once), so during the seed phase
// memoEntry's key-match branch can never fire for two different records
// and an occupancy-only table (1 byte/slot, no key arrays) reproduces
// the engine's own seedMemo() {seeded, inserted, failed} counts exactly.
// (Caveat, kept deliberate: a seed file with duplicate records would be
// over-inserted by this simulator; merged seeds are distinct by
// construction, see merge_pass_nway.)
// Validation gate: at MS=1<<24 the failed count must equal the published
// 4-way seedrun seed failure count (16137, worker-split4-memo-merge-73k
// measurement JSON) and the 2-way count (1448) respectively.
//
// Additionally records the base-index cluster statistics needed for the
// seed capacity design rule:
//   - count-of-counts histogram of keys per base index h
//   - for each failed record, the cluster size c_h of its own base
//     (attribution: own-cluster saturation when c_h >= 64 vs window
//     spill-over from neighbouring clusters when c_h < 64)
//
// Usage: node light_sim_seed_73k.mjs <seed.kyoenwm2> <msShift> [prefixLimit] [outJson]
import fs from 'fs';

const seedPath = process.argv[2];
const msShift = parseInt(process.argv[3], 10);
const prefixLimit = process.argv[4] ? parseInt(process.argv[4], 10) : Infinity;
const outJson = process.argv[5] || null;

const MS = 1 << msShift, MM = MS - 1;
const occ = new Uint8Array(MS);
const counts = new Uint32Array(MS);

let seeded = 0, inserted = 0, failed = 0;
let ownClusterFails = 0;    // failed records whose own base has >=64 keys
let spillFails = 0;         // failed records whose own base has <64 keys
let maxCluster = 0;
const failOwnC = [];        // c_h values of a sample of failures (c_h >= 64)
const failSpillC = [];      // c_h values of a sample of failures (c_h < 64)

// stream the seed file
const fd = fs.openSync(seedPath, 'r');
const chunk = Buffer.alloc(1 << 22);
let rem = '', first = true;
outer:
for (;;) {
  const n = fs.readSync(fd, chunk, 0, chunk.length, null);
  if (n <= 0) break;
  const data = rem + chunk.toString('latin1', 0, n);
  const lines = data.split('\n');
  rem = lines.pop();
  for (const l of lines) {
    if (first) { first = false; continue; }
    if (!l) continue;
    if (seeded >= prefixLimit) break outer;
    const sp = l.indexOf(' ');
    const sp2 = l.indexOf(' ', sp + 1);
    const sp3 = l.indexOf(' ', sp2 + 1);
    const sp4 = l.indexOf(' ', sp3 + 1);
    const M0 = parseInt(l.slice(0, sp), 16) | 0;
    const M1 = parseInt(l.slice(sp + 1, sp2), 16) | 0;
    const M2 = parseInt(l.slice(sp2 + 1, sp3), 16) | 0;
    const M3 = parseInt(l.slice(sp3 + 1, sp4), 16) | 0;
    const h0 = ((Math.imul(M0, 73856093) ^ Math.imul(M1, 19349663) ^
                 Math.imul(M2, 83492791) ^ Math.imul(M3, 39916801)) >>> 0) & MM;
    counts[h0]++;
    seeded++;
    let h = h0;
    let ok = false;
    for (let n2 = 0; n2 < 64; n2++) {
      if (occ[h] === 0) { occ[h] = 1; ok = true; break; }
      h = (h + 1) & MM;
    }
    if (ok) inserted++;
    else {
      failed++;
      const ch = counts[h0];
      if (ch >= 64) { ownClusterFails++; if (failOwnC.length < 64) failOwnC.push(ch); }
      else { spillFails++; if (failSpillC.length < 64) failSpillC.push(ch); }
    }
  }
}
fs.closeSync(fd);

// cluster statistics: count-of-counts over non-empty bases
const cc = new Map();
let nonEmptyBases = 0;
for (let i = 0; i < MS; i++) {
  const c = counts[i];
  if (c === 0) continue;
  nonEmptyBases++;
  if (c > maxCluster) maxCluster = c;
  cc.set(c, (cc.get(c) || 0) + 1);
}
const topClusters = [...cc.entries()].sort((a, b) => b[0] - a[0]).slice(0, 16)
  .map(([c, m]) => ({ keys_per_base: c, bases: m }));
let basesGE64 = 0, basesGE32 = 0, basesGE16 = 0, basesGE8 = 0;
for (const [c, m] of cc) {
  if (c >= 64) basesGE64 += m;
  if (c >= 32) basesGE32 += m;
  if (c >= 16) basesGE16 += m;
  if (c >= 8) basesGE8 += m;
}
let occupied = 0;
for (let i = 0; i < MS; i++) if (occ[i]) occupied++;

const doc = {
  schema: 'n11-class2-lane-light-seed-sim-73k-20261117-v1',
  seed_path: seedPath,
  ms_shift: msShift,
  ms: MS,
  prefix_limit: prefixLimit === Infinity ? null : prefixLimit,
  seeded, inserted, failed,
  failure_rate: failed / Math.max(1, seeded),
  occupied_after: occupied,
  load_factor: occupied / MS,
  base_clusters: {
    non_empty_bases: nonEmptyBases,
    max_cluster: maxCluster,
    bases_ge_64: basesGE64,
    bases_ge_32: basesGE32,
    bases_ge_16: basesGE16,
    bases_ge_8: basesGE8,
    top_clusters: topClusters,
  },
  failure_attribution: {
    own_cluster_ge64: ownClusterFails,
    spill_over_lt64: spillFails,
    own_cluster_c_sample: failOwnC,
    spill_over_c_sample: failSpillC,
  },
};
const line = JSON.stringify(doc);
if (outJson) fs.writeFileSync(outJson, line + '\n');
console.log(line);
