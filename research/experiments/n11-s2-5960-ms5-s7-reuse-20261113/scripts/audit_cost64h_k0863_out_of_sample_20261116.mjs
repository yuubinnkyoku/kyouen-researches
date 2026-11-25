#!/usr/bin/env node
// Independent out-of-sample audit for cost-64h WIN7-D10 roots against K0863 STERILE rows.
// Run from repository root:
//   node research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost64h_k0863_out_of_sample_20261116.mjs
// Uses only Node.js built-ins. It does not run a game search or extract certificates.

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import assert from "node:assert/strict";

const ROOT = process.cwd();
const EXP = "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113";
const OUT = EXP + "/output";
const SCAN = "research/experiments/n11-class2-lane-sterile-unclosability-20261116/output/theorem-applicability-scan-20261116.json";
const PINS = {
  [OUT + "/class2-lane-cost64h-inflight-20261116.json"]: "68e4878094b78eaf0a465033d0289a6db5d94861",
  [OUT + "/class2-lane-cost64h-raw-batch1-20261116.jsonl"]: "47da4e04357b7012c55903aea22160f3ca0767c9",
  [OUT + "/class2-lane-cost64h-raw-batch2-20261116.jsonl"]: "04e59e2ed62ba2306c80743e9c0517a6d89e70a2",
  [OUT + "/class2-lane-cost64h-raw-batch3-20261116.jsonl"]: "78bb44093ef56191110119009ce788d0cd4f383f",
  [OUT + "/class2-lane-cost64h-raw-batch4-20261116.jsonl"]: "7d196917961356c69cfa608930c3a1b7716aaf59",
  [OUT + "/class2-lane-cost64h-raw-batch5-20261116.jsonl"]: "ba6a36d4cb93111461aeec86b55e2909cbc0a489",
  [OUT + "/class2-lane-cost64h-raw-batch6-20261116.jsonl"]: "a49e2b9cd7d239fd95681afa83793deb075b4ccf",
  [OUT + "/class2-lane-cost64h-raw-batch7-20261116.jsonl"]: "6771b7a900191fce3d11feccf3da0e2e05f001e9",
  [OUT + "/class2-lane-cost64h-raw-batch8-20261116.jsonl"]: "5e778cae345d2a1d0d50455a3633ea673b6c08be",
  [OUT + "/class2-lane-cost64h-v15-crosscheck-20261116.jsonl"]: "0d32c2a0f5411d455f5b1503bc37c95c58f0b155",
  [SCAN]: "24f214e6a9dd721ef95ac97d6b84cf34af33b14b"
};

function gitBlobSha(bytes) {
  const header = Buffer.from("blob " + bytes.length + "\0", "utf8");
  return crypto.createHash("sha1").update(header).update(bytes).digest("hex");
}
function readPinned(relativePath, expectedSha) {
  const bytes = fs.readFileSync(path.join(ROOT, relativePath));
  assert.equal(gitBlobSha(bytes), expectedSha, "Git blob pin mismatch: " + relativePath);
  return bytes.toString("utf8");
}
function parseJsonl(text) {
  return text.trim().split(/\r?\n/).filter(Boolean).map(line => JSON.parse(line));
}
function points(mask) {
  const result = [];
  for (let i = 0; i < 121; i++) if ((mask >> BigInt(i)) & 1n) result.push(i);
  return result;
}
function determinant4(rows) {
  const a = rows.map(row => row.map(BigInt));
  let sign = 1n;
  let previous = 1n;
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
        a[i][j] = (a[i][j] * pivot - a[i][k] * a[k][j]) / previous;
      }
    }
    for (let i = k + 1; i < 4; i++) a[i][k] = 0n;
    previous = pivot;
  }
  return sign * a[3][3];
}
const safeCache = new Map();
function isSafe(mask) {
  const key = mask.toString(16);
  if (safeCache.has(key)) return safeCache.get(key);
  const p = points(mask);
  let result = true;
  for (let a = 0; a < p.length && result; a++) {
    for (let b = a + 1; b < p.length && result; b++) {
      for (let c = b + 1; c < p.length && result; c++) {
        for (let d = c + 1; d < p.length; d++) {
          const rows = [p[a], p[b], p[c], p[d]].map(i => {
            const x = i % 11;
            const y = Math.floor(i / 11);
            return [x * x + y * y, x, y, 1];
          });
          if (determinant4(rows) === 0n) {
            result = false;
            break;
          }
        }
      }
    }
  }
  safeCache.set(key, result);
  return result;
}
function legalCandidates(mask) {
  const result = [];
  for (let bit = 0; bit < 121; bit++) {
    const stone = 1n << BigInt(bit);
    if (!(mask & stone) && isSafe(mask | stone)) result.push(bit);
  }
  return result;
}
const canonCache = new Map();
function d4Canonical(mask) {
  const key = mask.toString(16);
  if (canonCache.has(key)) return canonCache.get(key);
  let best = null;
  for (let swap = 0; swap < 2; swap++) {
    for (let flipX = 0; flipX < 2; flipX++) {
      for (let flipY = 0; flipY < 2; flipY++) {
        let transformed = 0n;
        for (const i of points(mask)) {
          let x = i % 11;
          let y = Math.floor(i / 11);
          if (swap) [x, y] = [y, x];
          if (flipX) x = 10 - x;
          if (flipY) y = 10 - y;
          transformed |= 1n << BigInt(x + 11 * y);
        }
        const hex = transformed.toString(16).padStart(32, "0");
        if (best === null || hex < best) best = hex;
      }
    }
  }
  canonCache.set(key, best);
  return best;
}

const inputs = {};
for (const [relativePath, expectedSha] of Object.entries(PINS)) {
  inputs[relativePath] = readPinned(relativePath, expectedSha);
}
const claim = JSON.parse(inputs[OUT + "/class2-lane-cost64h-inflight-20261116.json"]);
const child = BigInt("0x" + claim.s6_child);
const expectedBits = [...claim.legal_candidates].sort((a, b) => a - b);
const actualBits = legalCandidates(child);
assert.equal(isSafe(child), true);
assert.deepEqual(actualBits, expectedBits, "independent legal-candidate set differs from claim");

const allRecords = [];
const batchSummaries = [];
for (let batch = 1; batch <= 8; batch++) {
  const relativePath = OUT + "/class2-lane-cost64h-raw-batch" + batch + "-20261116.jsonl";
  const rows = parseJsonl(inputs[relativePath]);
  const pilot = rows[0];
  assert.equal(rows.length, 9);
  assert.equal(pilot.control, "pilot_d6");
  assert.equal(pilot.loss, false);
  assert.equal(pilot.nodes, 3402);
  assert.equal(pilot.capped, false);
  const records = rows.slice(1);
  const bits = records.map(row => row.bit).sort((a, b) => a - b);
  const claimedBatch = claim.engine.batch_bits["batch" + batch].slice().sort((a, b) => a - b);
  assert.deepEqual(bits, claimedBatch, "batch bit partition mismatch");
  for (const row of records) {
    assert.equal(row.capped, false);
    assert.equal(row.andclose, true);
    assert.deepEqual(row.terminalStoneRange, [13, 17]);
    assert.ok(Number.isSafeInteger(row.nodes) && row.nodes > 0);
  }
  allRecords.push(...records);
  batchSummaries.push({
    batch,
    bits,
    nodes: records.reduce((sum, row) => sum + row.nodes, 0),
    win7_d10: records.filter(row => row.loss === true).length,
    refuted_d10: records.filter(row => row.loss === false).length
  });
}
const uniqueBits = [...new Set(allRecords.map(row => row.bit))].sort((a, b) => a - b);
assert.equal(allRecords.length, 64);
assert.equal(uniqueBits.length, 64);
assert.deepEqual(uniqueBits, expectedBits);

const winBits = allRecords.filter(row => row.loss === true).map(row => row.bit).sort((a, b) => a - b);
const refutedCount = allRecords.filter(row => row.loss === false).length;
const nodeSum = allRecords.reduce((sum, row) => sum + row.nodes, 0);
assert.deepEqual(winBits, claim.sweep_results.win7_d10_bits.slice().sort((a, b) => a - b));
assert.equal(winBits.length, 23);
assert.equal(refutedCount, 41);
assert.equal(nodeSum, 47017565);

const v15Rows = parseJsonl(inputs[OUT + "/class2-lane-cost64h-v15-crosscheck-20261116.jsonl"]);
const v15Data = v15Rows.filter(row => Number.isInteger(row.bit));
const v15WinBits = v15Data.filter(row => row.loss === true && row.capped === false)
  .map(row => row.bit).sort((a, b) => a - b);
const v15NodeSum = v15Data.reduce((sum, row) => sum + row.nodes, 0);
assert.equal(v15Rows.length, 24);
assert.equal(v15Rows[0].control, "pilot_d6");
assert.equal(v15Rows[0].nodes, 5949);
assert.equal(v15Rows[0].loss, false);
assert.deepEqual(v15WinBits, winBits);
assert.equal(v15NodeSum, 55171821);
for (const row of v15Data) {
  assert.equal(row.capped, false);
  assert.equal(row.andclose, true);
  assert.deepEqual(row.terminalStoneRange, [13, 17]);
}

const d4Groups = new Map();
for (const row of allRecords) {
  const root = child | (1n << BigInt(row.bit));
  const canonical = d4Canonical(root);
  if (!d4Groups.has(canonical)) d4Groups.set(canonical, []);
  d4Groups.get(canonical).push(row);
}
const d4Conflicts = [...d4Groups.entries()].filter(([, rows]) =>
  new Set(rows.map(row => row.loss ? "WIN7-D10" : "REFUTED-D10")).size > 1);
assert.equal(d4Conflicts.length, 0);
assert.equal(d4Groups.size, 64);

const winRoots = winBits.map(bit => {
  const root = child | (1n << BigInt(bit));
  return {
    bit,
    root_hex: root.toString(16).padStart(32, "0"),
    d4_canonical_hex: d4Canonical(root)
  };
});
const winCanons = new Set(winRoots.map(root => root.d4_canonical_hex));
assert.equal(winCanons.size, 23);

const scan = JSON.parse(inputs[SCAN]);
const sterileDetails = [];
for (const row of scan.sterile_rows_detected) {
  const mask = BigInt("0x" + row.child);
  assert.equal(isSafe(mask), true);
  const bits = legalCandidates(mask);
  assert.equal(bits.length, row.engine_refuted, "STERILE row legal-candidate count mismatch");
  assert.equal(row.transferred_refuted, 0);
  const candidateCanons = new Set(bits.map(bit =>
    d4Canonical(mask | (1n << BigInt(bit)))));
  const overlaps = winRoots.filter(root => candidateCanons.has(root.d4_canonical_hex))
    .map(root => root.bit);
  assert.deepEqual(overlaps, [], "cost64h WIN root overlaps a K0863 STERILE row");
  sterileDetails.push({
    child: row.child,
    legal_candidates: bits.length,
    candidate_d4_orbits: candidateCanons.size,
    win64h_overlap_bits: overlaps
  });
}
const sterileCandidateCount = sterileDetails.reduce((sum, row) => sum + row.legal_candidates, 0);
assert.equal(sterileDetails.length, 35);
assert.equal(sterileCandidateCount, 2628);

const audit = {
  schema: "n11-class2-lane-cost64h-k0863-out-of-sample-audit-20261116-v1",
  date: "2026-11-16",
  target: {
    s6_child_hex: claim.s6_child,
    stones: points(child),
    edge_cost: 64,
    legal_candidate_count: 64
  },
  source_blob_pins: PINS,
  method: "Independent JavaScript re-derivation: exact BigInt Bareiss 4x4 determinants for safety/legal moves; fresh D4 canonicalization; raw v16 batches rejoined against claim batch partitions; v15 cross-engine comparison; K0863 STERILE rows independently re-enumerated and checked against every cost64h WIN root.",
  checks: [
    { name: "child safety and exact legal candidate set", pass: true },
    { name: "8 v16 batches cover all 64 legal bits exactly once", pass: true },
    { name: "v16 verdict totals 23 WIN7-D10 / 41 REFUTED-D10 / 0 capped", pass: true },
    { name: "v16 node sum and terminal-range invariants", pass: true },
    { name: "8 pilot controls", pass: true },
    { name: "independent v15 confirms all 23 WIN bits", pass: true },
    { name: "64 distinct D4 candidate-root classes; no WIN/REFUTED collision", pass: true },
    { name: "23 WIN roots are pairwise D4-distinct", pass: true },
    { name: "35 K0863 STERILE rows re-derived with 2,628 legal candidates", pass: true },
    { name: "no cost64h WIN root covers any K0863 STERILE row", pass: true }
  ],
  v16: {
    candidate_count: allRecords.length,
    win7_d10_bits: winBits,
    refuted_d10_count: refutedCount,
    capped_count: 0,
    node_sum: nodeSum,
    terminal_stone_range: [13, 17],
    andclose_all: true,
    batches: batchSummaries,
    pilots: 8
  },
  v15: {
    crosschecked_win7_d10_bits: v15WinBits,
    candidate_count: v15Data.length,
    node_sum: v15NodeSum,
    terminal_stone_range: [13, 17],
    all_uncapped: true
  },
  d4: {
    candidate_root_classes: d4Groups.size,
    verdict_conflicts: d4Conflicts.length,
    win_root_classes: winCanons.size,
    win_root_duplicates: 0,
    win_roots: winRoots
  },
  k0863_out_of_sample: {
    sterile_rows: sterileDetails.length,
    legal_candidate_count_sum: sterileCandidateCount,
    count_mismatches: 0,
    win_root_overlap_rows: 0,
    rows: sterileDetails
  },
  interpretation_guard: "This is an independent finite consistency audit, not a new game-theoretic result. WIN7-D10 proves only a first-player win within depth 10 from an individual 7-stone root; REFUTED-D10 is not a LOSS proof. K0863 concerns receipt-cover impossibility for STERILE rows, not their game-theoretic value. The 64h certificates have not yet been extracted or folded. Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
};
const outputPath = OUT + "/class2-lane-cost64h-k0863-out-of-sample-audit-20261116.json";
fs.writeFileSync(path.join(ROOT, outputPath), JSON.stringify(audit, null, 2) + "\n");
process.stdout.write(JSON.stringify({
  output: outputPath,
  checks: audit.checks.length,
  v16_win: winBits.length,
  v16_refuted: refutedCount,
  d4_classes: d4Groups.size,
  sterile_rows: sterileDetails.length,
  sterile_candidates: sterileCandidateCount,
  sterile_overlaps: 0
}, null, 2) + "\n");
