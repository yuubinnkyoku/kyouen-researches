#!/usr/bin/env node
// Cross-version audit of the same cost81 81-root S6->S7 sweep.
// Run from the repository root:
//   node research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost81_v15_v17_crosscheck_20261118.mjs
// This script performs no game search and extracts no certificate.
// It compares the historical v15 aggregate with the fresh v17 raw batches,
// independently recomputes D4 root canons, and checks the K0865 prediction.

import fs from "node:fs";
import crypto from "node:crypto";
import path from "node:path";

const ROOT = process.cwd();
const EXP = "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113";
const CENSUS = "research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json";
const CHILD = "00000000020000003800000080008000";
const PARENT = "00000000020000003800000080000000";
const OUTPUT = path.join(EXP, "output/class2-lane-cost81-v15-v17-cross-version-audit-20261118.json");

const files = {
  old_sweep: path.join(EXP, "output/class4-lane-cost81-sweep-20261114.json"),
  claim_v2: path.join(EXP, "output/class2-lane-cost81-inflight-20261118.json"),
  v17_audit: path.join(EXP, "output/class2-lane-cost81-raw-batches-1-9-audit-20261118.json"),
  k0865_census: CENSUS,
  v15_crosscheck: path.join(EXP, "output/class2-lane-cost81-v15-crosscheck-a-20261118.jsonl"),
  det_batch1: path.join(EXP, "output/class2-lane-cost81-det-batch1-20261118.jsonl"),
  det_batch8: path.join(EXP, "output/class2-lane-cost81-det-batch8-20261118.jsonl"),
  v15_runner: path.join(EXP, "scripts/class4_child1_runner.ts"),
  v17_runner: path.join(EXP, "scripts/class4_child1_runner_v17.ts"),
};
for (let i = 1; i <= 9; i++) {
  const suffix = i === 9 ? "raw-batch9-confirmation" : `raw-batch${i}`;
  files[`raw_batch_${i}`] = path.join(EXP, `output/class2-lane-cost81-${suffix}-20261118.jsonl`);
}

const expectedBlobSha = {
  old_sweep: "96d3ba0554af684d8f03f8a5008db8a88f24c6b3",
  claim_v2: "5dc331070094343d803fe9d1e1b1222ea4e60b73",
  v17_audit: "f90bdccdc25e2f11cbb3af1b152318d994e5761a",
  k0865_census: "9c251da3138c5cb0516e097be5e5d0427dfaf5f0",
  v15_crosscheck: "f42e202a83c81e088ba5e503ab4c7747dc6fe508",
  det_batch1: "bb3f35d6220a69a4d3b3b30b6358c0123a1eb3d8",
  det_batch8: "18e71d316e9372c69b846126411a1280f63297e4",
  v15_runner: "8744fc65b6b7cac6bd561403ce4c749e01c51359",
  v17_runner: "c132cc6425eee3feaeef1d697dd74f968cfedb59",
  raw_batch_1: "de9b0820371c00340bd9f652168563acfd24ea3f",
  raw_batch_2: "f2650a2a767df12f5db2b69c03d93900f086abb8",
  raw_batch_3: "7cd92c1e5a38a9a6ea45f0dcfcff7c8e5a99467d",
  raw_batch_4: "8ef37f89a268c522c8f957098e9366b3a80a76f3",
  raw_batch_5: "6391794c1ab54794fb6b0de7cd70aa1f194d4938",
  raw_batch_6: "afbae8f0d1d46a9b4e0ea4355320c8cb58ac98a4",
  raw_batch_7: "4f2a413142ee11b54ad90d9f0fbc5784f672916c",
  raw_batch_8: "8e515436a3db86baa46f819eba78cde3aba20e8f",
  raw_batch_9: "a1700d71e02f66c2a61c07350fe1229ce9f2317a",
};

function assert(condition, message) {
  if (!condition) throw new Error(message);
}
function read(name) {
  const p = path.join(ROOT, files[name]);
  const bytes = fs.readFileSync(p);
  const gitBlobSha = crypto.createHash("sha1")
    .update(Buffer.concat([Buffer.from(`blob ${bytes.length}\0`), bytes]))
    .digest("hex");
  assert(gitBlobSha === expectedBlobSha[name], `${name}: Git blob SHA mismatch ${gitBlobSha}`);
  return { bytes, text: bytes.toString("utf8"), gitBlobSha, byteLength: bytes.length };
}
function parseJsonl(text, label) {
  const lines = text.trim().split(/\r?\n/);
  return lines.map((line, i) => {
    try { return JSON.parse(line); }
    catch (error) { throw new Error(`${label} line ${i + 1}: ${error.message}`); }
  });
}
function sortedObjectWithoutMs(row) {
  return Object.fromEntries(Object.entries(row).filter(([key]) => key !== "ms").sort(([a], [b]) => a.localeCompare(b)));
}
function sameWithoutMs(a, b) {
  const aa = parseJsonl(a, "left").map(sortedObjectWithoutMs);
  const bb = parseJsonl(b, "right").map(sortedObjectWithoutMs);
  return JSON.stringify(aa) === JSON.stringify(bb);
}
function d4Canon(hex) {
  const board = BigInt("0x" + hex);
  const forms = [];
  for (let symmetry = 0; symmetry < 8; symmetry++) {
    let transformed = 0n;
    for (let bit = 0; bit < 121; bit++) {
      if (((board >> BigInt(bit)) & 1n) === 0n) continue;
      const x = bit % 11, y = Math.floor(bit / 11);
      let X, Y;
      switch (symmetry) {
        case 0: [X, Y] = [x, y]; break;
        case 1: [X, Y] = [10 - y, x]; break;
        case 2: [X, Y] = [10 - x, 10 - y]; break;
        case 3: [X, Y] = [y, 10 - x]; break;
        case 4: [X, Y] = [10 - x, y]; break;
        case 5: [X, Y] = [10 - y, 10 - x]; break;
        case 6: [X, Y] = [x, 10 - y]; break;
        case 7: [X, Y] = [y, x]; break;
      }
      transformed |= 1n << BigInt(Y * 11 + X);
    }
    forms.push(transformed.toString(16).padStart(32, "0"));
  }
  return forms.sort()[0];
}

const loaded = Object.fromEntries(Object.keys(files).map(name => [name, read(name)]));
const old = JSON.parse(loaded.old_sweep.text);
const claim = JSON.parse(loaded.claim_v2.text);
const audit = JSON.parse(loaded.v17_audit.text);
const census = JSON.parse(loaded.k0865_census.text);
const oldCandidates = old.candidates;
const oldByBit = new Map(oldCandidates.map(row => [row.bit, row]));
const newBatches = [];
const batchSizes = [];
const pilotNodes = [];
for (let i = 1; i <= 9; i++) {
  const rows = parseJsonl(loaded[`raw_batch_${i}`].text, `raw batch ${i}`);
  newBatches.push(rows);
  const pilots = rows.filter(row => row.control === "pilot_d6");
  const candidates = rows.filter(row => Object.hasOwn(row, "bit"));
  assert(pilots.length === 1 && pilots[0].loss === false && pilots[0].nodes === 3402 && pilots[0].capped === false,
    `raw batch ${i}: pilot_d6 control mismatch`);
  assert(candidates.length === (i <= 7 ? 9 : i === 8 ? 3 : 15), `raw batch ${i}: candidate count mismatch`);
  batchSizes.push(candidates.length);
  pilotNodes.push(pilots[0].nodes);
}
const newCandidates = newBatches.flat().filter(row => Object.hasOwn(row, "bit"));
const newByBit = new Map(newCandidates.map(row => [row.bit, row]));
const v15Rows = parseJsonl(loaded.v15_crosscheck.text, "v15 crosscheck");
const v15Pilot = v15Rows.find(row => row.control === "pilot_d6");
const v15Candidates = v15Rows.filter(row => Object.hasOwn(row, "bit"));
const det1Matches = sameWithoutMs(loaded.det_batch1.text, loaded.raw_batch_1.text);
const det8Matches = sameWithoutMs(loaded.det_batch8.text, loaded.raw_batch_8.text);

assert(old.candidate_count === 81 && oldCandidates.length === 81, "old v15 sweep candidate count mismatch");
assert(old.summary.win7_d10.length === 0 && old.summary.refuted_d10.length === 81 && old.summary.capped.length === 0,
  "old v15 sweep is not 81/81 REFUTED-D10");
assert(claim.candidate_count === 81 && claim.batches_run === 9 && claim.open_bits_completed === 66 && claim.open_bits_remaining === 0,
  "v17 claim completion counts mismatch");
assert(audit.counts.win7_d10 === 0 && audit.counts.refuted_d10 === 81 && audit.counts.capped === 0,
  "v17 audit verdict counts mismatch");
assert(newCandidates.length === 81 && newByBit.size === 81, "v17 raw rows are missing or duplicated");
assert(claim.legal_candidates.length === 81 && newCandidates.every(row => claim.legal_candidates.includes(row.bit)),
  "v17 raw bits do not match claim legal candidates");
assert(claim.legal_candidates.every(bit => newByBit.has(bit)) && oldByBit.size === 81 &&
  claim.legal_candidates.every(bit => oldByBit.has(bit)), "old/new bit sets differ");
assert(newCandidates.every(row => row.loss === false && row.capped === false && row.andclose === true &&
  row.terminalStoneRange?.[0] === 13 && row.terminalStoneRange?.[1] === 17), "v17 raw candidate verdict/terminal mismatch");
assert(newCandidates.every(row => oldByBit.get(row.bit).verdict === "REFUTED-D10" &&
  oldByBit.get(row.bit).capped === false &&
  oldByBit.get(row.bit).terminal_range?.[0] === 13 && oldByBit.get(row.bit).terminal_range?.[1] === 17),
  "old v15 per-bit result is not REFUTED-D10/[13,17]");
assert([...oldByBit.keys()].every(bit => newByBit.has(bit)), "v15/v17 per-bit comparison is incomplete");
assert(pilotNodes.length === 9 && pilotNodes.every(n => n === 3402), "v17 pilot controls are not 9/9");
assert(det1Matches && det8Matches, "determinism rerun differs beyond ms");
assert(v15Pilot?.nodes === 5949 && v15Pilot.loss === false && v15Pilot.capped === false, "v15 pilot_d6 mismatch");
assert(v15Candidates.length === 15, "v15 crosscheck candidate count mismatch");
const confirmationBits = claim.engine_candidate_bits.confirmation_bits;
assert(v15Candidates.length === confirmationBits.length, "v15 confirmation bit count mismatch");
assert(v15Candidates.every(row => confirmationBits.includes(row.bit) && row.loss === false && row.capped === false &&
  row.terminalStoneRange?.[0] === 13 && row.terminalStoneRange?.[1] === 17 &&
  oldByBit.get(row.bit)?.nodes === row.nodes), "v15 confirmation does not reproduce historical v15 nodes/verdicts");

const auditPerBit = Array.isArray(audit.per_bit)
  ? new Map(audit.per_bit.map(row => [row.bit, row]))
  : new Map(Object.entries(audit.per_bit).map(([bit, row]) => [Number(bit), row]));
const child = BigInt("0x" + claim.s6_child);
const canonicalByBit = [];
for (const bit of claim.legal_candidates) {
  const rootHex = (child | (1n << BigInt(bit))).toString(16).padStart(32, "0");
  const canon = d4Canon(rootHex);
  assert(auditPerBit.get(bit)?.root_canon === canon, `bit ${bit}: independent D4 canon mismatch`);
  canonicalByBit.push({ bit, root_hex: rootHex, root_canon: canon });
}
assert(new Set(canonicalByBit.map(row => row.root_canon)).size === 81, "D4 root canons are not all distinct");

const parent = census.open_s5_census.find(row => row.hex === PARENT);
assert(parent?.classification === "all_remaining_sterile" && parent.sterile_refs.length === 18,
  "K0865 class-4 parent census prediction mismatch");
const sterileRef = parent.sterile_refs.find(row => row.hex === CHILD && row.cost === 81);
assert(!!sterileRef, "cost81 child is not one of K0865's 18 sterile refs");

const perBit = claim.legal_candidates.map(bit => {
  const before = oldByBit.get(bit), after = newByBit.get(bit);
  return {
    bit,
    old_v15_nodes: before.nodes,
    fresh_v17_nodes: after.nodes,
    node_ratio_v15_over_v17: Number((before.nodes / after.nodes).toFixed(8)),
    old_v15_verdict: before.verdict,
    fresh_v17_verdict: after.loss ? "WIN7-D10" : "REFUTED-D10",
  };
});
const ratios = perBit.map(row => row.node_ratio_v15_over_v17).sort((a, b) => a - b);
const oldTotal = old.summary.total_nodes;
const newTotal = newCandidates.reduce((sum, row) => sum + row.nodes, 0);
assert(newTotal === claim.actual_execution.total_candidate_nodes && newTotal === audit.total_candidate_nodes,
  "v17 candidate node total mismatch");
assert(oldTotal === 325836995 && newTotal === 86480711, "unexpected published node totals");
const percentReduction = (oldTotal - newTotal) / oldTotal * 100;
const checks = {
  pinned_inputs_match_git_blobs: true,
  old_v15_81_candidates_refuted_uncapped: true,
  v17_81_raw_candidates_complete_unique: true,
  old_v15_and_new_v17_bit_sets_match_81_of_81: true,
  old_v15_and_new_v17_verdicts_match_81_of_81: true,
  all_v17_terminal_ranges_are_13_to_17: true,
  all_v17_candidates_are_andclose_and_uncapped: true,
  v17_pilot_controls_9_of_9_at_3402: true,
  v17_node_sum_matches_claim_and_audit: true,
  det_batch1_and_batch8_match_except_elapsed_ms: true,
  v15_confirmation_15_of_15_matches_historical_v15_nodes: true,
  independent_bigint_d4_canons_match_audit_81_of_81: true,
  all_81_root_d4_canons_are_distinct: true,
  k0865_parent_predicts_all_18_rows_sterile_and_includes_cost81: true,
};
assert(Object.values(checks).every(Boolean), "one or more cross-version checks failed");

const result = {
  schema: "n11-class2-lane-cost81-v15-v17-cross-version-audit-20261118-v1",
  date: "2026-11-18",
  status: "PASS",
  source_main_head_before_audit: "b1ba66fdecc912e51de777fab02cbe2930bf1b44",
  target: { s6_child: CHILD, s5_parent: PARENT, legal_candidates: 81, depth: 10, cap_per_bit: 1000000000, andclose: true },
  input_git_blob_sha: Object.fromEntries(Object.entries(loaded).map(([name, value]) => [files[name], value.gitBlobSha])),
  old_v15: {
    source: "class4-lane-cost81-sweep-20261114.json",
    total_candidate_nodes: oldTotal,
    candidate_count: oldCandidates.length,
    verdicts: { win7_d10: old.summary.win7_d10.length, refuted_d10: old.summary.refuted_d10.length, capped: old.summary.capped.length },
    runner_blob_sha: loaded.v15_runner.gitBlobSha,
  },
  fresh_v17: {
    source: "class2-lane-cost81 raw batches 1-9",
    total_candidate_nodes: newTotal,
    candidate_count: newCandidates.length,
    verdicts: { win7_d10: 0, refuted_d10: 81, capped: 0 },
    pilot_controls: { count: pilotNodes.length, nodes_each: 3402 },
    runner_blob_sha: loaded.v17_runner.gitBlobSha,
  },
  cross_version: {
    bit_set_agreement: "81/81",
    verdict_agreement: "81/81",
    old_v15_nodes: oldTotal,
    fresh_v17_nodes: newTotal,
    node_reduction: oldTotal - newTotal,
    node_reduction_percent: Number(percentReduction.toFixed(8)),
    old_v15_over_v17_node_ratio: Number((oldTotal / newTotal).toFixed(8)),
    per_bit_ratio: {
      min: ratios[0],
      median: ratios[Math.floor(ratios.length / 2)],
      max: ratios[ratios.length - 1],
    },
    v15_confirmation: { count: v15Candidates.length, historical_node_exact_matches: 15 },
    determinism: { batch1_field_identical_except_ms: det1Matches, batch8_field_identical_except_ms: det8Matches },
    performance_caveat: "This is a node-count comparison across v15 and v17, not an apples-to-apples runtime benchmark. v17 repairs the known fbtOR probe-exhaustion drop; the historical v15 run is retained only as a consistency baseline and is not promoted to proof.",
  },
  k0865_prediction: {
    parent_class: parent.classes,
    parent_classification: parent.classification,
    remaining_s6_orbits_at_head1410: parent.remaining_s6_orbits,
    remaining_s7_edge_cost_at_head1410: parent.remaining_s7_edge_cost,
    sterile_refs: parent.sterile_refs.length,
    cost81_child_is_one_of_18: true,
    interpretation: "The fresh v17 sweep revalidates one historical K0865 STERILE prediction; it is not a newly discovered S6 row and does not change the head-1410 census.",
  },
  independent_d4: {
    method: "BigInt bitboard; eight explicit D4 coordinate transforms; canonical minimum 32-hex representation",
    root_canons_recomputed: canonicalByBit.length,
    unique_root_canons: new Set(canonicalByBit.map(row => row.root_canon)).size,
    matches_existing_v17_audit: "81/81",
    roots: canonicalByBit,
  },
  per_bit: perBit,
  checks,
  interpretation_guard: "REFUTED-D10 means no first-player win within depth 10 from each individual seven-stone root; it is not a LOSS proof. The cost81 row has no WIN7-D10 certificate, so no receipt fold or new manifest row closure occurs. The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
};

fs.writeFileSync(OUTPUT, JSON.stringify(result, null, 2) + "\n");
process.stdout.write(JSON.stringify({
  status: result.status,
  old_v15_nodes: oldTotal,
  fresh_v17_nodes: newTotal,
  node_reduction_percent: result.cross_version.node_reduction_percent,
  node_ratio: result.cross_version.old_v15_over_v17_node_ratio,
  verdict_agreement: result.cross_version.verdict_agreement,
  d4_canons: result.independent_d4.unique_root_canons,
  output: OUTPUT,
}, null, 2) + "\n");
