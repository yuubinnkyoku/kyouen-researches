#!/usr/bin/env node
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";

const ROOT = process.cwd();
const BASE_MAIN_HEAD = "105657faacc05350d16ba0abf6fe79d445e6868b";
const EXP = "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113";
const claimPath = EXP + "/output/class2-lane-cost74h-inflight-20261115.json";
const mergedPath = EXP + "/output/class-frontier-merged-cost65l-74g-recompute-20261115.json";
const rankingPath = EXP + "/output/class-frontier-s5-ranking-after-merged-cost65l-74g-20261115.csv";
const manifestPaths = [1, 2, 3, 4, 5, 6].map(n =>
  "research/experiments/n11-s2-5960-milestone5-20261112/output/ms5_s6_manifest_part" + n + ".csv"
);
const scriptPath = EXP + "/scripts/audit_cost74h_claim_independent_20261115.mjs";
const outputPath = EXP + "/output/cost74h-claim-independent-audit-20261115.json";

function read(rel) {
  return fs.readFileSync(path.join(ROOT, rel), "utf8").replace(/^\uFEFF/, "");
}
function git(args) {
  return execFileSync("git", args, { cwd: ROOT, encoding: "utf8" }).trim();
}
function csvRows(rel) {
  const lines = read(rel).trim().split(/\r?\n/);
  const header = lines.shift().split(",");
  return lines.filter(Boolean).map(line => {
    const cells = line.split(",");
    assert.equal(cells.length, header.length, "unexpected simple-CSV column count in " + rel);
    return Object.fromEntries(header.map((key, i) => [key, cells[i]]));
  });
}
function detBareiss4(matrix) {
  const a = matrix.map(row => row.map(BigInt));
  let sign = 1n;
  let previousPivot = 1n;
  for (let k = 0; k < 3; k++) {
    let pivotRow = k;
    while (pivotRow < 4 && a[pivotRow][k] === 0n) pivotRow++;
    if (pivotRow === 4) return 0n;
    if (pivotRow !== k) {
      [a[pivotRow], a[k]] = [a[k], a[pivotRow]];
      sign = -sign;
    }
    const pivot = a[k][k];
    for (let i = k + 1; i < 4; i++) {
      for (let j = k + 1; j < 4; j++) {
        const numerator = a[i][j] * pivot - a[i][k] * a[k][j];
        assert.equal(numerator % previousPivot, 0n, "Bareiss division must be exact");
        a[i][j] = numerator / previousPivot;
      }
    }
    for (let i = k + 1; i < 4; i++) a[i][k] = 0n;
    previousPivot = pivot;
  }
  return sign * a[3][3];
}
function bitIndices(mask) {
  const out = [];
  for (let i = 0; i < 121; i++) if ((mask >> BigInt(i)) & 1n) out.push(i);
  return out;
}
function safe(mask) {
  const stones = bitIndices(mask).map(i => [i % 11, Math.floor(i / 11)]);
  for (let a = 0; a < stones.length; a++)
    for (let b = a + 1; b < stones.length; b++)
      for (let c = b + 1; c < stones.length; c++)
        for (let d = c + 1; d < stones.length; d++) {
          const four = [stones[a], stones[b], stones[c], stones[d]];
          if (detBareiss4(four.map(([x, y]) => [x * x + y * y, x, y, 1])) === 0n) return false;
        }
  return true;
}
function d4Canonical(mask) {
  const transforms = [
    (x, y) => [x, y], (x, y) => [y, 10 - x],
    (x, y) => [10 - x, 10 - y], (x, y) => [10 - y, x],
    (x, y) => [10 - x, y], (x, y) => [x, 10 - y],
    (x, y) => [y, x], (x, y) => [10 - y, 10 - x]
  ];
  let best = null;
  for (const transform of transforms) {
    let image = 0n;
    for (const i of bitIndices(mask)) {
      const [x, y] = transform(i % 11, Math.floor(i / 11));
      image |= 1n << BigInt(11 * y + x);
    }
    if (best === null || image < best) best = image;
  }
  return best.toString(16).padStart(32, "0");
}

const claim = JSON.parse(read(claimPath));
const merged = JSON.parse(read(mergedPath));
const child = BigInt("0x" + claim.s6_child);
const stones = bitIndices(child);
assert.equal(stones.length, 6);
assert.deepEqual(stones, claim.child_stones_bit_indices);
assert.equal(safe(child), true);

const legalCandidates = [];
for (let i = 0; i < 121; i++) {
  if ((child >> BigInt(i)) & 1n) continue;
  if (safe(child | (1n << BigInt(i)))) legalCandidates.push(i);
}
assert.deepEqual(legalCandidates, claim.legal_candidates);
assert.equal(legalCandidates.length, 74);
assert.equal(claim.candidate_count, 74);
assert.equal(claim.s6_s7_edge_cost, 74);

const parentLifts = stones.map(bit => ({
  lift_stone: bit,
  s5_hex: d4Canonical(child & ~(1n << BigInt(bit)))
}));
assert.equal(new Set(parentLifts.map(x => x.s5_hex)).size, 6);

const rankingRows = csvRows(rankingPath).map(row => ({
  s5_hex: row.s5_hex,
  classes: Number(row.classes),
  remaining_s6_orbits: Number(row.remaining_s6_orbits),
  remaining_s7_edge_cost: Number(row.remaining_s7_edge_cost)
}));
const ranking = new Map(rankingRows.map(row => [row.s5_hex, row]));
const openParentLifts = parentLifts.filter(parent => ranking.has(parent.s5_hex));
assert.equal(openParentLifts.length, 2);
assert.deepEqual(
  openParentLifts.map(x => x.s5_hex).sort(),
  claim.open_parents_at_head_1270.map(x => x.s5_hex).sort()
);
const openParents = openParentLifts.map(parent => {
  const row = ranking.get(parent.s5_hex);
  const claimed = claim.open_parents_at_head_1270.find(x => x.s5_hex === parent.s5_hex);
  assert.equal(row.classes, claimed.classes_bitmask);
  assert.equal(row.remaining_s6_orbits, claimed.remaining_s6_orbits);
  assert.equal(row.remaining_s7_edge_cost, claimed.remaining_s7_edge_cost);
  assert.equal(claimed.lift_stone, parent.lift_stone);
  return {
    lift_stone: parent.lift_stone,
    s5_hex: parent.s5_hex,
    classes_bitmask: row.classes,
    remaining_s6_orbits: row.remaining_s6_orbits,
    remaining_s7_edge_cost: row.remaining_s7_edge_cost
  };
});
assert.deepEqual(openParents.map(x => x.classes_bitmask), [2, 2]);
assert.deepEqual(claim.demand, { c1: 0, c2: 2, c4: 0 });

const manifestRows = manifestPaths.flatMap(rel => csvRows(rel).map(row => ({
  hex: row.hex, cost: Number(row.cost), classes: Number(row.classes)
})));
assert.equal(manifestRows.length, 7867);
const manifestHits = manifestRows.filter(row => row.hex === claim.s6_child);
assert.equal(manifestHits.length, 1);
assert.deepEqual(manifestHits[0], { hex: claim.s6_child, cost: 74, classes: 2 });

const frontier = merged.frontier_after_merged;
const chainHead = [
  frontier.solved_s6_in_manifest, frontier.unique_remaining_s6,
  frontier.sum_remaining_cost, frontier.s6_needed_by_open_classes,
  frontier.cost_needed_by_open_classes
].join("/");
assert.ok(claim.chain_head_at_claim.startsWith(chainHead));

const inputPaths = [claimPath, mergedPath, rankingPath, ...manifestPaths];
const inputBlobShas = Object.fromEntries(inputPaths.map(rel => [rel, git(["rev-parse", "HEAD:" + rel])]));
const output = {
  schema: "n11-class2-cost74h-claim-independent-audit-20261115-v1",
  date: "2026-11-15",
  status: "verified structural preconditions; no sweep result",
  execution: "The initial result was generated by the equivalent V8 execution in this run; this saved Node.js script was not run in a repository checkout during this run.",
  audit_base_main_head: BASE_MAIN_HEAD,
  audit_script_blob_sha: git(["rev-parse", "HEAD:" + scriptPath]),
  input_blob_shas: inputBlobShas,
  target: {
    s6_child: claim.s6_child,
    child_stones_bit_indices: stones,
    s6_safe: true,
    safe_four_subsets_checked: 15,
    s6_s7_edge_cost: 74,
    legal_candidate_count: legalCandidates.length,
    legal_candidates_exact_match_claim: true,
    legal_candidates: legalCandidates,
    s6_manifest_row: manifestHits[0]
  },
  parent_lifts: parentLifts,
  open_parents: openParents,
  closed_parent_lifts: parentLifts.filter(parent => !ranking.has(parent.s5_hex)),
  demand: { c1: 0, c2: 2, c4: 0 },
  canonical_head: chainHead,
  ranking_rows: rankingRows.length,
  manifest_rows: manifestRows.length,
  controls: {
    safe_s6: true,
    legal_candidate_list_exact: true,
    six_parent_orbits_distinct: true,
    exactly_two_open_parents: true,
    open_parent_rows_match_claim: true,
    manifest_membership_cost_and_class_match: true,
    claim_head_matches_merged_frontier: true
  },
  limitations: [
    "This audit does not run the v16 depth-10 sweep.",
    "It does not independently reconstruct the full 17-row remaining set or prove that cost 74 is the cheapest unswept child among every prior claim.",
    "It creates no WIN/LOSS verdict, certificate, or receipt fold."
  ],
  game_value: "UNKNOWN"
};
fs.writeFileSync(path.join(ROOT, outputPath), JSON.stringify(output, null, 2) + "\n", "utf8");
process.stdout.write(JSON.stringify(output, null, 2) + "\n");
