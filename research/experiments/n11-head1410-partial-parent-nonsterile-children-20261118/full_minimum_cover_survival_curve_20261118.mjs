#!/usr/bin/env node
import { readFile, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, "../../..");
const BASE = "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118";
const INPUTS = {
  membership: {
    path: BASE + "/output/minimum-cover-root-membership-20261118.json",
    sha1: "ab1e655f4a89a677e57515cdbacfe56894323013"
  },
  prior: {
    path: BASE + "/output/minimum-cover-elimination-structure-20261118.json",
    sha1: "5f6185483f7a6458535b8e38a73483a23db2ef29"
  }
};
const OUT = BASE + "/output/full-minimum-cover-survival-prefix-20261118.json";

function gitBlobSha1(bytes) {
  return createHash("sha1")
    .update(Buffer.from("blob " + bytes.length + "\0"))
    .update(bytes)
    .digest("hex");
}
async function readPinned(key) {
  const pin = INPUTS[key];
  const bytes = await readFile(resolve(ROOT, pin.path));
  const sha1 = gitBlobSha1(bytes);
  if (sha1 !== pin.sha1) throw new Error(key + " blob SHA mismatch: " + sha1);
  return JSON.parse(bytes.toString("utf8"));
}
function compareHex(a, b) {
  return a < b ? -1 : a > b ? 1 : 0;
}
function countSuffix(roots, masks, full, start, forcedIndices = []) {
  const forced = new Set(forcedIndices);
  let initMask = 0;
  for (const i of forcedIndices) initMask |= masks[i];
  const initK = forcedIndices.length;
  const dp = Array.from({ length: full + 1 }, () => Array(7).fill(0));
  dp[initMask][initK] = 1;
  for (let i = start; i < roots.length; i++) {
    if (forced.has(i)) continue;
    const x = masks[i];
    for (let q = 6; q >= initK + 1; q--) {
      for (let mask = 0; mask <= full; mask++) {
        const w = dp[mask][q - 1];
        if (!w) continue;
        const next = mask | x;
        if (next !== mask) dp[next][q] += w;
      }
    }
  }
  return dp[full][6];
}
async function main() {
  const [membership, prior] = await Promise.all([
    readPinned("membership"),
    readPinned("prior")
  ]);
  const rowHexes = membership.derived.per_row.map(x => x.row);
  const N = rowHexes.length;
  if (N !== 11) throw new Error("expected 11 target rows");
  const rowIndex = new Map(rowHexes.map((h, i) => [h, i]));
  const full = (1 << N) - 1;
  const roots = membership.derived.all_root_memberships.slice().sort((a, b) =>
    b.membership - a.membership || compareHex(a.root, b.root)
  );
  const total = membership.derived.cover_space.total_minimum_covers;
  if (roots.length !== 757 || total !== 359610 ||
      membership.derived.cover_space.minimum_root_count !== 6) {
    throw new Error("unexpected cover universe");
  }
  const masks = roots.map(e => {
    let mask = 0;
    for (const h of e.cover_rows) {
      if (!rowIndex.has(h)) throw new Error("unknown target row " + h);
      mask |= 1 << rowIndex.get(h);
    }
    if (e.cover_rows.length < 1 || e.cover_rows.length > 2) {
      throw new Error("root span outside 1..2");
    }
    return mask;
  });

  // Reverse suffix DP: after adding roots i..end, dp[full][6] counts
  // minimum covers avoiding the first i membership-ranked roots.
  const dp = Array.from({ length: 1 << N }, () => Array(7).fill(0));
  dp[0][0] = 1;
  const curve = new Array(roots.length + 1);
  curve[roots.length] = 0;
  for (let i = roots.length - 1; i >= 0; i--) {
    const x = masks[i];
    for (let q = 6; q >= 1; q--) {
      for (let mask = 0; mask <= full; mask++) {
        const w = dp[mask][q - 1];
        if (!w) continue;
        const next = mask | x;
        if (next !== mask) dp[next][q] += w;
      }
    }
    curve[i] = dp[full][6];
  }

  const priorCurve = prior.derived.survival_curve_excluding_topk_membership_roots;
  const priorMatch = priorCurve.every(p => curve[p.k] === p.surviving_covers);
  const membershipSum = roots.reduce((s, e) => s + e.membership, 0);
  const firstZeroPrefix = curve.findIndex(x => x === 0);
  const prefix = curve.slice(0, 16).map((remaining, k) => ({
    k,
    surviving_covers: remaining,
    killed_covers: total - remaining,
    marginal_kill: k === 0 ? 0 : curve[k - 1] - remaining,
    killed_share: Number(((total - remaining) / total).toFixed(8))
  }));
  const top15 = roots.slice(0, 15).map((e, i) => ({
    rank: i + 1,
    root: e.root,
    membership: e.membership,
    cover_rows: e.cover_rows
  }));
  const residualSingles = [12, 13, 14].map(i => ({
    rank: i + 1,
    root: roots[i].root,
    membership: roots[i].membership,
    cover_rows: roots[i].cover_rows,
    residual_forced_covers: countSuffix(roots, masks, full, 12, [i])
  }));
  const residualPairs = [[12, 13], [12, 14], [13, 14]].map(([a, b]) => ({
    ranks: [a + 1, b + 1],
    roots: [roots[a].root, roots[b].root],
    joint_residual_covers: countSuffix(roots, masks, full, 12, [a, b])
  }));
  const residualTriple = countSuffix(roots, masks, full, 12, [12, 13, 14]);

  const checks = [
    { name: "pin.membership", pass: true, detail: INPUTS.membership.sha1 },
    { name: "pin.prior_elimination", pass: true, detail: INPUTS.prior.sha1 },
    { name: "target.rows", pass: N === 11, detail: String(N) },
    { name: "roots.unique", pass: new Set(roots.map(e => e.root)).size === 757, detail: String(roots.length) },
    { name: "roots.all_cover_1_or_2_rows", pass: masks.every((m, i) => roots[i].cover_rows.length === 1 || roots[i].cover_rows.length === 2), detail: "757" },
    { name: "cover.total", pass: total === 359610 && curve[0] === total, detail: String(curve[0]) },
    { name: "cover.minimum_size", pass: membership.derived.cover_space.minimum_root_count === 6, detail: "6" },
    { name: "membership.sum_identity", pass: membershipSum === 6 * total, detail: String(membershipSum) },
    { name: "prior.k0_to_k12_reproduced", pass: priorMatch, detail: priorCurve.length + " points" },
    { name: "curve.monotone", pass: curve.every((v, i) => i === 0 || v <= curve[i - 1]), detail: "758 suffix counts" },
    { name: "top15.are_pair_roots", pass: top15.every(e => e.cover_rows.length === 2), detail: "15" },
    { name: "prefix.k14_nonzero", pass: curve[14] === 4875, detail: String(curve[14]) },
    { name: "prefix.k15_zero", pass: curve[15] === 0, detail: String(curve[15]) },
    { name: "prefix.first_zero_is_15", pass: firstZeroPrefix === 15, detail: String(firstZeroPrefix) },
    { name: "residual.after_top12", pass: curve[12] === 14625, detail: String(curve[12]) },
    { name: "residual.final_three_each_4875", pass: residualSingles.every(x => x.residual_forced_covers === 4875), detail: JSON.stringify(residualSingles.map(x => x.residual_forced_covers)) },
    { name: "residual.final_three_pairwise_disjoint", pass: residualPairs.every(x => x.joint_residual_covers === 0), detail: JSON.stringify(residualPairs.map(x => x.joint_residual_covers)) },
    { name: "residual.final_three_cover_all", pass: residualSingles.reduce((s, x) => s + x.residual_forced_covers, 0) === curve[12], detail: String(residualSingles.reduce((s, x) => s + x.residual_forced_covers, 0)) },
    { name: "residual.triple_joint_zero", pass: residualTriple === 0, detail: String(residualTriple) }
  ];
  const result = {
    schema: "n11-head1476-class2-full-minimum-cover-survival-prefix-20261118-v1",
    date: "2026-11-18",
    lane: "standard 11x11 weak-resolution, verification side",
    title: "Exact full membership-ranked prefix survival curve for the 359,610 minimum 6-root covers",
    inputs: {
      membership: { path: INPUTS.membership.path, git_blob_sha1: INPUTS.membership.sha1 },
      prior_elimination: { path: INPUTS.prior.path, git_blob_sha1: INPUTS.prior.sha1 }
    },
    method: "One reverse suffix 0/1 DP over 11-row masks and exact root count 0..6. Roots are processed from lowest to highest membership rank; after adding rank i, dp[full][6] counts 6-root covers using only ranks i..757. The no-new-row transition is skipped because every 6-root cover is minimum and hence every selected root is essential. Forced-inclusion DP partitions the k=12 residual by ranks 13..15.",
    derived: {
      target_parent: "00000000000000403800000008000000",
      target_rows: rowHexes,
      candidate_roots: roots.length,
      minimum_root_count: 6,
      total_minimum_covers: total,
      membership_sum: membershipSum,
      full_prefix_survival_k0_to_k15: prefix,
      first_zero_membership_prefix_length: firstZeroPrefix,
      zero_survival_for_all_larger_prefixes: true,
      top15_membership_roots: top15,
      residual_after_top12: {
        surviving_minimum_covers: curve[12],
        partition_roots: residualSingles,
        pairwise_joint_counts: residualPairs,
        triple_joint_count: residualTriple,
        exact_partition: true
      }
    },
    checks,
    check_count: checks.length,
    all_pass: checks.every(c => c.pass),
    interpretation_guard: "Exact combinatorial bookkeeping for minimum 6-root candidate covers only. The top-15 prefix is a hitting set for all minimum covers in the published membership ranking, but this does not prove it is a globally minimum hitting set. If all 15 roots were unavailable to depth-10 receipts, no 6-root receipt plan would remain; larger covers may still exist. No root verdict, WIN7-D10 receipt, S6 fold, S5 closure, or game-theoretic outcome is created. REFUTED-D10 and STERILE are not LOSS proofs.",
    unknown_status: {
      standard_11x11_empty_board: "UNKNOWN",
      two_stone_roots: "UNKNOWN",
      S2_59_60: "UNKNOWN",
      classes_1_2_4: "UNKNOWN"
    }
  };
  if (!result.all_pass) throw new Error("verification checks failed");
  await writeFile(resolve(ROOT, OUT), JSON.stringify(result, null, 2) + "\n");
  console.log(JSON.stringify({
    checks: checks.length,
    all_pass: result.all_pass,
    firstZeroPrefix,
    curve: prefix,
    residualAfterTop12: curve[12]
  }));
}
main().catch(err => {
  console.error(err);
  process.exitCode = 1;
});
