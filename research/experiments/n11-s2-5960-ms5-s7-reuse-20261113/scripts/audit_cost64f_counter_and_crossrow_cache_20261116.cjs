#!/usr/bin/env node
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");

const HERE = __dirname;
const OUT = path.resolve(HERE, "..", "output");
const PRESWEEP_NAME = "class2-lane-next-target-presweep-1435-v2-20261116.json";
const CLAIM_NAME = "class2-lane-cost64f-inflight-20261116.json";
const MARGINAL_NAME = "class2-lane-cost64f-parent-and-marginal-audit-20261116.json";
const EXPECTED_PRESWEEP_BLOB = "59d42a6b1d8db4dbc498872576283e0130a0c390";
const EXPECTED_MARGINAL_BLOB = "d9f5f377b9503f034cb7e9220b0d84d716bde87d";

function assert(condition, message) {
  if (!condition) throw new Error(message);
}
function gitBlobSha(buffer) {
  return crypto.createHash("sha1")
    .update(Buffer.from("blob " + buffer.length + "\0", "utf8"))
    .update(buffer)
    .digest("hex");
}
function readPinnedJson(name, expectedSha) {
  const buffer = fs.readFileSync(path.join(OUT, name));
  const actualSha = gitBlobSha(buffer);
  assert(actualSha === expectedSha, name + " blob pin mismatch: " + actualSha);
  return {value: JSON.parse(buffer.toString("utf8")), sha: actualSha};
}
function sorted(values) {
  return [...values].sort((a, b) => a - b);
}
function same(a, b) {
  return JSON.stringify(a) === JSON.stringify(b);
}
function d4CanonHex(hex) {
  const value = BigInt("0x" + hex);
  const cells = [];
  for (let i = 0; i < 121; i++) {
    if (((value >> BigInt(i)) & 1n) !== 0n) cells.push(i);
  }
  let best = null;
  for (let swap = 0; swap < 2; swap++) {
    for (let flipX = 0; flipX < 2; flipX++) {
      for (let flipY = 0; flipY < 2; flipY++) {
        let transformed = 0n;
        for (const cell of cells) {
          const x = cell % 11;
          const y = Math.floor(cell / 11);
          let a = swap ? y : x;
          let b = swap ? x : y;
          if (flipX) a = 10 - a;
          if (flipY) b = 10 - b;
          transformed |= 1n << BigInt(a + 11 * b);
        }
        const candidate = transformed.toString(16).padStart(32, "0");
        if (best === null || candidate < best) best = candidate;
      }
    }
  }
  return best;
}

function main() {
  const presweepRead = readPinnedJson(PRESWEEP_NAME, EXPECTED_PRESWEEP_BLOB);
  const marginalRead = readPinnedJson(MARGINAL_NAME, EXPECTED_MARGINAL_BLOB);
  const presweep = presweepRead.value;
  const marginal = marginalRead.value;
  const claimBuffer = fs.readFileSync(path.join(OUT, CLAIM_NAME));
  const claimBlob = gitBlobSha(claimBuffer);
  const claim = JSON.parse(claimBuffer.toString("utf8"));

  assert(claim.schema === "n11-class2-lane-cost64f-completed-20261116-v4", "claim schema is not v4");
  assert(claim.results.refuted_d10_count === 61, "corrected REFUTED-D10 count mismatch");
  assert(claim.results.refuted_d10_count_swept_v16 === 56, "swept REFUTED-D10 count mismatch");
  assert(claim.results.refuted_d10_count_transferred === 5, "transferred REFUTED-D10 count mismatch");
  assert(claim.results.win7_d10_count === 3 && claim.results.capped_count === 0, "claim verdict totals mismatch");
  assert(claim.results.determined_d10_count === 64, "determined count mismatch");

  const rawRows = [];
  const rawBatchPins = {};
  const batchSummaries = [];
  for (let i = 1; i <= 8; i++) {
    const name = "class2-lane-cost64f-raw-batch" + i + "-20261116.jsonl";
    const buffer = fs.readFileSync(path.join(OUT, name));
    const sha = gitBlobSha(buffer);
    const match = claim.results.raw_batches["batch" + i].match(/git blob ([0-9a-f]{40})/);
    assert(match && match[1] === sha, name + " blob pin mismatch");
    rawBatchPins[name] = sha;
    const lines = buffer.toString("utf8").trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
    const pilots = lines.filter(row => row.control === "pilot_d6");
    const bits = lines.filter(row => Number.isInteger(row.bit));
    assert(pilots.length === 1 && pilots[0].nodes === 3402 &&
      pilots[0].loss === false && pilots[0].capped === false, name + " pilot mismatch");
    const expectedBits = sorted(claim.results.batch_bit_lists[String(i)]);
    assert(same(sorted(bits.map(row => row.bit)), expectedBits), name + " bit-list mismatch");
    for (const row of bits) {
      assert(row.capped === false && row.andclose === true &&
        same(row.terminalStoneRange, [13, 17]), name + " terminal/cap mismatch at bit " + row.bit);
      rawRows.push({batch: i, row});
    }
    batchSummaries.push({
      batch: i,
      pilot_nodes: pilots[0].nodes,
      candidate_bits: bits.length,
      win_bits: sorted(bits.filter(row => row.loss === true).map(row => row.bit)),
      refuted_bits: sorted(bits.filter(row => row.loss === false).map(row => row.bit)),
      capped_bits: bits.filter(row => row.capped === true).map(row => row.bit),
      candidate_nodes: bits.reduce((sum, row) => sum + row.nodes, 0)
    });
  }

  const sweptBits = sorted(rawRows.map(item => item.row.bit));
  const winBits = sorted(rawRows.filter(item => item.row.loss === true).map(item => item.row.bit));
  const sweptRefuted = sorted(rawRows.filter(item => item.row.loss === false).map(item => item.row.bit));
  const transferred = sorted(claim.results.refuted_d10_bits_transferred);
  const candidates = sorted(claim.results.candidates);
  assert(rawRows.length === 59 && same(sweptBits, sorted(claim.open_candidates_to_sweep)), "swept/open bit mismatch");
  assert(same(winBits, sorted(claim.results.win7_d10_bits)), "WIN bit mismatch");
  assert(same(sweptRefuted, sorted(claim.results.refuted_d10_bits_swept_v16)), "swept REFUTED bit mismatch");
  assert(same(candidates, sorted([...new Set([...sweptBits, ...transferred])])), "candidate partition mismatch");
  assert(winBits.length === 3 && sweptRefuted.length === 56 && transferred.length === 5 &&
    new Set([...sweptBits, ...transferred]).size === 64, "expected 3 WIN + 56 swept REFUTED + 5 transferred REFUTED");
  const nodes = rawRows.reduce((sum, item) => sum + item.row.nodes, 0);
  assert(nodes === 54905391 && nodes === claim.results.candidate_nodes_excluding_pilots, "raw node sum mismatch");

  const child = BigInt("0x" + claim.s6_child);
  const winSet = new Set(winBits);
  const verdictByCanon = new Map();
  for (const bit of candidates) {
    const root = (child | (1n << BigInt(bit))).toString(16).padStart(32, "0");
    const canon = d4CanonHex(root);
    const verdict = winSet.has(bit) ? "WIN7-D10" : "REFUTED-D10";
    assert(!verdictByCanon.has(canon), "duplicate D4 orbit inside cost64f at " + canon);
    verdictByCanon.set(canon, {bit, root_hex: root, verdict});
  }
  assert(verdictByCanon.size === 64, "cost64f D4 orbit count mismatch");

  const rowSummaries = [];
  for (const [rowHex, entries] of Object.entries(presweep.cheapest_row_bit_tables)) {
    const seen = new Set();
    const statusCounts = {};
    let priorOpen = 0, priorRefuted = 0, priorWin = 0;
    const newHits = [], conflicts = [];
    for (const entry of entries) {
      assert(d4CanonHex(entry.root_canon) === entry.root_canon, "noncanonical row root " + entry.root_canon);
      assert(!seen.has(entry.root_canon), "duplicate canonical candidate within row " + rowHex);
      seen.add(entry.root_canon);
      statusCounts[entry.status] = (statusCounts[entry.status] || 0) + 1;
      if (entry.status === "open") priorOpen++;
      else if (entry.status.toLowerCase().includes("refuted")) priorRefuted++;
      else if (entry.status.toLowerCase().includes("win")) priorWin++;
      const fresh = verdictByCanon.get(entry.root_canon);
      if (!fresh) continue;
      if (entry.status === "open") {
        newHits.push({bit: entry.bit, root_canon: entry.root_canon, source_bit: fresh.bit, verdict: fresh.verdict});
      } else {
        const oldVerdict = entry.status.toLowerCase().includes("refuted") ? "REFUTED-D10" :
          entry.status.toLowerCase().includes("win") ? "WIN7-D10" : null;
        if (oldVerdict !== fresh.verdict) {
          conflicts.push({bit: entry.bit, prior_status: entry.status, new_verdict: fresh.verdict, source_bit: fresh.bit});
        }
      }
    }
    rowSummaries.push({
      s6_hex: rowHex,
      candidate_slots: entries.length,
      prior_open: priorOpen,
      prior_refuted: priorRefuted,
      prior_win: priorWin,
      prior_status_counts: statusCounts,
      cost64f_new_hits: newHits.length,
      remaining_open: priorOpen - newHits.length,
      new_hits: newHits,
      conflicts
    });
  }

  const byRow = new Map(rowSummaries.map(row => [row.s6_hex, row]));
  const totalCandidates = rowSummaries.reduce((sum, row) => sum + row.candidate_slots, 0);
  const totalPriorOpen = rowSummaries.reduce((sum, row) => sum + row.prior_open, 0);
  const totalNewHits = rowSummaries.reduce((sum, row) => sum + row.cost64f_new_hits, 0);
  const totalRemainingOpen = rowSummaries.reduce((sum, row) => sum + row.remaining_open, 0);
  const totalConflicts = rowSummaries.reduce((sum, row) => sum + row.conflicts.length, 0);
  const childRow = byRow.get(claim.s6_child);
  const siblingHex = "00000000000100003800000008080000";
  const sibling = byRow.get(siblingHex);
  const aliasRow = byRow.get("00000000000000801202010000800000");
  const anchorRow = byRow.get("00000000000000403800000008100000");
  assert(childRow && childRow.candidate_slots === 64 && childRow.prior_open === 59 &&
    childRow.prior_refuted === 5 && childRow.cost64f_new_hits === 59 && childRow.remaining_open === 0,
    "cost64f child row did not become fully determined");
  assert(sibling && sibling.prior_open === 59 && sibling.cost64f_new_hits === 0 && sibling.remaining_open === 59,
    "runner-up row cache count mismatch");
  assert(aliasRow && aliasRow.prior_open === 60 && aliasRow.cost64f_new_hits === 1 &&
    aliasRow.remaining_open === 59 && aliasRow.new_hits[0].bit === 51 && aliasRow.new_hits[0].source_bit === 40,
    "cross-row D4 alias mismatch");
  assert(anchorRow && anchorRow.prior_open === 64 && anchorRow.cost64f_new_hits === 0,
    "class-2 parent anchor row mismatch");
  assert(totalCandidates === 515 && totalPriorOpen === 302 && totalNewHits === 60 &&
    totalRemainingOpen === 242 && totalConflicts === 0, "cross-row aggregate mismatch");

  assert(presweep.chain_head === "1435/174/6413/507337/4686/371251" &&
    marginal.canonical_head_before_fold === "1435/174/6413/507337/4686/371251" &&
    marginal.fold_applied === false && marginal.new_marginal_row_count === 3, "fold baseline mismatch");
  const receiptMarginals = marginal.receipt_marginals_in_order;
  assert(same(receiptMarginals.map(row => row.bit), [39, 72, 107]) &&
    same(receiptMarginals.map(row => row.marginal_count), [1, 0, 2]) &&
    marginal.new_marginal_rows.some(row => row.s6_hex === claim.s6_child), "receipt marginal mismatch");

  const ranking = presweep.cheapest_open_rows_ranking;
  const nextRanked = ranking.map((row, index) => ({row, index, summary: byRow.get(row.s6_hex)}))
    .filter(item => item.summary && item.summary.remaining_open > 0 && item.row.s6_hex !== claim.s6_child)
    .sort((a, b) => a.row.cost - b.row.cost ||
      a.summary.remaining_open - b.summary.remaining_open || a.index - b.index);
  const next = nextRanked[0];
  assert(next && next.row.s6_hex === siblingHex && next.summary.remaining_open === 59,
    "next target after pending fold is not expected sibling");
  const directParents = Object.entries(presweep.family_census)
    .filter(([parent, doc]) => doc.rows.some(row => row.s6_hex === siblingHex))
    .map(([parent]) => parent);
  assert(directParents.includes(next.row.s5_hex), "next target parent ownership mismatch");

  const result = {
    schema: "n11-class2-lane-cost64f-counter-and-crossrow-cache-audit-20261116-v1",
    date: "2026-11-16",
    source_main_head_before_claim_correction: claim.counter_correction.source_main_head_before_correction,
    source_claim_blob_sha_after_correction: claimBlob,
    source_claim_blob_sha_before_correction: claim.counter_correction.previous_claim_blob_sha,
    source_presweep_blob_sha: presweepRead.sha,
    source_marginal_audit_blob_sha: marginalRead.sha,
    source_raw_batch_blob_shas: rawBatchPins,
    raw_sweep_recount: {
      candidate_bits_swept: rawRows.length,
      win7_d10_bits: winBits,
      win7_d10_count: winBits.length,
      refuted_d10_bits_swept_v16: sweptRefuted,
      refuted_d10_count_swept_v16: sweptRefuted.length,
      transferred_refuted_d10_bits: transferred,
      refuted_d10_count_transferred: transferred.length,
      refuted_d10_count_total: sweptRefuted.length + transferred.length,
      capped_count: 0,
      determined_d10_count: candidates.length,
      candidate_nodes_excluding_pilots: nodes,
      batch_summaries: batchSummaries
    },
    claim_counter_correction: {
      old_refuted_d10_count: claim.counter_correction.previous_value,
      corrected_refuted_d10_count: claim.counter_correction.corrected_value,
      identity: "64 candidates = 3 WIN7-D10 + 61 REFUTED-D10 + 0 capped",
      old_value_was_candidate_count: true
    },
    d4_cache: {
      cost64f_candidate_roots: 64,
      distinct_d4_orbits: verdictByCanon.size,
      duplicate_d4_orbits: 0,
      selected_presweep_rows: rowSummaries.length,
      candidate_slots_across_rows: totalCandidates,
      prior_open_slots: totalPriorOpen,
      newly_determined_open_slots: totalNewHits,
      remaining_open_slots: totalRemainingOpen,
      conflicts: totalConflicts,
      rows: rowSummaries
    },
    receipt_fold_projection: {
      fold_applied: false,
      canonical_head_before_fold: marginal.canonical_head_before_fold,
      projected_head_after_cost64f_fold: marginal.projected_head_after_cost64f_fold,
      new_manifest_rows: marginal.new_marginal_rows.map(row => row.s6_hex),
      new_manifest_row_count: marginal.new_marginal_row_count,
      per_receipt_marginals: receiptMarginals.map(row => ({
        bit: row.bit, marginal_count: row.marginal_count, marginal_rows: row.marginal_rows_in_receipt_order
      }))
    },
    next_target_after_pending_fold: {
      s5_parent: next.row.s5_hex,
      s6_child: next.row.s6_hex,
      cost: next.row.cost,
      demand: next.row.demand,
      prior_open_after_presweep: next.summary.prior_open,
      cost64f_new_hits: next.summary.cost64f_new_hits,
      remaining_open: next.summary.remaining_open,
      direct_parents_in_two_parent_census: directParents,
      reason: "cheapest remaining open row in the published head-1435 v2 ranking after excluding the cost64f receipt-ready child; projected only until the full fold is reproduced"
    },
    checks: {
      all_8_raw_batch_blob_pins_match: true,
      all_8_pilots_pass: true,
      raw_bits_equal_claim_open_sweep_bits: true,
      raw_verdict_bits_equal_claim: true,
      candidate_partition_64_exact: true,
      counter_identity_exact: true,
      all_64_cost64f_roots_have_distinct_d4_canons: true,
      crossrow_conflicts_zero: true,
      cost64f_child_row_all_64_candidates_determined: true,
      one_additional_d4_alias_hit_in_cost65_row: true,
      next_target_parent_mapping_correct: true,
      fold_not_applied: true
    },
    interpretation_guard: "This audit only reconciles depth-10 root verdict counts and D4 cache reuse across eight selected presweep rows. WIN7-D10 proves a first-player win from an individual seven-stone root only. REFUTED-D10 is not a LOSS proof. The cost64f fold is not applied; the projected head is manifest bookkeeping only. Standard 11x11, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
    unknown_status: "11x11 empty board, two-stone roots {49,60} and {59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN"
  };
  const outputPath = path.join(OUT, "class2-lane-cost64f-counter-and-crossrow-cache-audit-20261116.json");
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 1) + "\n");
  process.stdout.write(JSON.stringify({
    output: outputPath, swept: rawRows.length, win: winBits.length,
    refuted: sweptRefuted.length + transferred.length, d4_hits: totalNewHits,
    conflicts: totalConflicts, next_target: next.row.s6_hex, remaining_open: next.summary.remaining_open
  }, null, 2) + "\n");
}
main();
