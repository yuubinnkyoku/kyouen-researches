#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const SOURCE_MAIN_HEAD = "0c9881826a2e25bf665a19804ba5655f14aa932e";
const EXP = "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118";
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../..");
const OUT = path.join(ROOT, EXP, "output", "rank1-parent-head1476-reconciliation-20261118.json");
const LANE = "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/";
const PARENT = "00000000000000801202000040000000";
const ROW_76C = "00000000010000809002000001000000";
const ROW_76D = "00000000040000003800080008000000";
const ROW_77E = "00000000040000809002000000004000";

const PINS = {
  k0863: ["research/knowledge/items/K0863-sterile-row-depth10-unclosability.md", "c2ae353cab4a7dbcd28ec53b0f57d35ab4f26a5d"],
  k0865: ["research/knowledge/items/K0865-head1410-sterile-coverage-census.md", "6b79dbcb2db0b8c34c108c1c227be139a3f1493b"],
  k0868: ["research/knowledge/items/K0868-n11-s6-s7-sweep-candidate-convention.md", "b097210d0b49d7cf014cc6a554298b1e49e83384"],
  k0865_census: ["research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json", "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"],
  rank1_script: [EXP + "/audit_rank1_parent_receipt_channel_20261118.py", "606de306c9d08bac3cc0e119a486dc59cb04de6e"],
  rank1_output: [EXP + "/output/rank1-parent-receipt-channel-20261118.json", "881b7c7777b313bd88ae1840e32f06f397a31e7c"],
  worklist1410: ["research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv", "2fee1d0718547a62e346d35f5858d7913e37c097"],
  s5_closability1410: ["research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-s5-closability-after-cost60c-20261116.csv", "65215b6582de6efedfed8d77d91630edd883a2cb"],
  claim76c: [LANE + "class2-lane-cost76c-inflight-20261116.json", "678211c5a35c25cf41b4a56473942860903647f6"],
  fold76c: [LANE + "class-frontier-cost76c-receipts-recompute-20261117.json", "953beaea054989e8b1de33f48b1f2ebc13ae7e11"],
  audit76c: [LANE + "class2-lane-cost76c-fold-audit-20261117.json", "de79a3a7bfc6c5b8fb77db885354f01b82e023f7"],
  manifest76c: [LANE + "class2-lane-cost76c-certificates/class2-lane-cost76c-win7-certificates-20261117.json", "00cf337f9365b10ac1db090b9f9cf9a464b83347"],
  claim76d: [LANE + "class2-lane-cost76d-inflight-20261116.json", "ec598676317b748eb34c7d2bf4044992343c518e"],
  claim77e: [LANE + "class2-lane-cost77e-inflight-20261116.json", "36515c516c7270e1869a52d0a76285200b1e33e8"],
  fold76d77e: [LANE + "class-frontier-cost76d77e-receipts-recompute-20261116.json", "8d4bc622f9da22b8754f2e398e5481359656d956"],
  verify76d77e: [LANE + "class2-lane-cost76d-77e-second-independent-verification-20261116.json", "d267fa8d93017110ff74df4520b3a8e8a47bee5b"],
  claim66i: [LANE + "class2-lane-cost66i-inflight-20261116.json", "f8556f6c054d821e845b7ebe5035b8c280d2e97b"],
  audit66i: [LANE + "class2-lane-cost66i-bit19-receipt-fold-audit-20261118.json", "e1fbf301bb6795432dbb015289b4a68c63095ef0"],
  fold66i: [LANE + "class-frontier-cost66i-bit19-receipts-recompute-20261118.json", "a555ee3a575df04ecddf98ce890bd8eec53dd415"]
};

const checks = [];
const inputs = {};
const raw = {};
function gitBlobSha1(buf) {
  const head = Buffer.from("blob " + buf.length + "\0", "utf8");
  return crypto.createHash("sha1").update(Buffer.concat([head, buf])).digest("hex");
}
function check(name, ok, detail = "") {
  checks.push({ check: name, pass: !!ok, detail: typeof detail === "string" ? detail : JSON.stringify(detail) });
}
function loadPinned(key) {
  const [rel, expected] = PINS[key];
  const buf = fs.readFileSync(path.resolve(ROOT, rel));
  const actual = gitBlobSha1(buf);
  inputs[key] = { path: rel, git_blob_sha1: actual };
  raw[key] = buf.toString("utf8");
  check("pin." + key, actual === expected, actual);
  return raw[key];
}
function loadJSON(key) {
  return JSON.parse(loadPinned(key));
}
function parseCSV(src) {
  const rows = [];
  let row = [], field = "", quoted = false;
  for (let i = 0; i < src.length; i++) {
    const c = src[i];
    if (quoted) {
      if (c === '"' && src[i + 1] === '"') { field += '"'; i++; }
      else if (c === '"') quoted = false;
      else field += c;
    } else if (c === '"') quoted = true;
    else if (c === ",") { row.push(field); field = ""; }
    else if (c === "\n") {
      row.push(field.replace(/\r$/, ""));
      if (row.length) rows.push(row);
      row = []; field = "";
    } else field += c;
  }
  if (field.length || row.length) { row.push(field.replace(/\r$/, "")); rows.push(row); }
  const header = rows.shift();
  return rows.filter(r => r.length === header.length).map(r =>
    Object.fromEntries(header.map((h, i) => [h, r[i] ?? ""]))
  );
}
function popcount(n) {
  let count = 0;
  while (n) { n &= n - 1n; count++; }
  return count;
}
function transformMask(mask, reflected, rotations) {
  let out = 0n;
  for (let i = 0; i < 121; i++) {
    if (((mask >> BigInt(i)) & 1n) === 0n) continue;
    let r = Math.floor(i / 11), c = i % 11;
    if (reflected) c = 10 - c;
    for (let k = 0; k < rotations; k++) {
      const nr = c, nc = 10 - r;
      r = nr; c = nc;
    }
    out |= 1n << BigInt(r * 11 + c);
  }
  return out;
}
function sameSet(a, b) {
  const aa = [...a].sort(), bb = [...b].sort();
  return aa.length === bb.length && aa.every((x, i) => x === bb[i]);
}
function sum(xs) { return xs.reduce((a, b) => a + Number(b), 0); }

function main() {
  const k0863Text = loadPinned("k0863");
  const k0865Text = loadPinned("k0865");
  const k0868Text = loadPinned("k0868");
  const census = loadJSON("k0865_census");
  const oldScript = loadPinned("rank1_script");
  const rank1 = loadJSON("rank1_output");
  const work = parseCSV(loadPinned("worklist1410"));
  const s5 = parseCSV(loadPinned("s5_closability1410"));
  const c76 = loadJSON("claim76c");
  const f76 = loadJSON("fold76c");
  const a76 = loadJSON("audit76c");
  const m76 = loadJSON("manifest76c");
  const c76d = loadJSON("claim76d");
  const c77e = loadJSON("claim77e");
  const f76d77e = loadJSON("fold76d77e");
  const v76d77e = loadJSON("verify76d77e");
  const c66i = loadJSON("claim66i");
  const a66i = loadJSON("audit66i");
  const f66i = loadJSON("fold66i");

  const parentMask = BigInt("0x" + PARENT);
  const parentImages = [];
  for (let reflected = 0; reflected < 2; reflected++) {
    for (let rotations = 0; rotations < 4; rotations++) {
      parentImages.push(transformMask(parentMask, !!reflected, rotations));
    }
  }
  const related = work.filter(row => {
    const rm = BigInt("0x" + row.s6_canonical_hex);
    return parentImages.some(pm => (pm & rm) === pm);
  }).map(row => ({
    hex: row.s6_canonical_hex,
    category: row.category,
    cost: Number(row.own_candidates_s6_s7_edge_cost),
    open_after_transfers: Number(row.open_candidates_after_transfers),
    win: Number(row.engine_win7_d10),
    refuted: Number(row.engine_refuted_d10)
  })).sort((a, b) => a.hex.localeCompare(b.hex));

  const oldRows = [...rank1.rows].sort((a, b) => a.hex.localeCompare(b.hex));
  const censusParent = census.open_s5_census.find(x => x.hex === PARENT);
  const s5Parent = s5.find(x => x.s5_hex === PARENT);
  const sterileRefs = censusParent.sterile_refs.map(x => ({ hex: x.hex, cost: Number(x.cost) })).sort((a, b) => a.hex.localeCompare(b.hex));
  const historicalSterile = oldRows.filter(x => x.category === "sterile").map(x => ({ hex: x.hex, cost: Number(x.cost) })).sort((a, b) => a.hex.localeCompare(b.hex));
  const lostRows = f76.parents_after[PARENT].lost_rows_hexes;
  const currentRows = related.filter(x => !lostRows.includes(x.hex));
  const currentRowsCost = sum(currentRows.map(x => x.cost));
  const lostNonsterile = related.filter(x => lostRows.includes(x.hex));
  const currentParent66iAffected = Object.prototype.hasOwnProperty.call(f66i.parents_after, PARENT);

  check("basis.source_main_head", SOURCE_MAIN_HEAD.length === 40, SOURCE_MAIN_HEAD);
  check("basis.k0863_proved", k0863Text.includes("status: proved") && k0863Text.includes("どのWIN7-D10 receipt rootにもcoverされない"));
  check("basis.k0865_historical_head1410", k0865Text.includes("head-1410") && census.head_state?.solved_manifest_rows === 1410);
  check("basis.k0868_survival_convention", k0868Text.includes("own_candidates") && k0868Text.includes("edge cost"));
  check("historical.audit_29_checks", rank1.all_checks_pass === true && rank1.checks.length === 29, rank1.checks.length);
  check("historical.audit_rank1_parent", rank1.summary.parent === PARENT && rank1.summary.remaining_rows === 5);
  check("historical.audit_record_time_pending_field", sameSet(rank1.summary.fold_pending_bands, ["cost76c", "cost76d", "cost77e"]));
  check("historical.script_checks_record_time_not_current_claims",
    oldScript.includes('check("F.folds_pending"') &&
    !oldScript.includes("class2-lane-cost76c-inflight-20261116.json"));

  check("join.worklist_row_count", work.length === 6438, work.length);
  check("join.parent_popcount", popcount(parentMask) === 5, popcount(parentMask));
  check("join.d4_related_rows", related.length === 5 && sameSet(related.map(x => x.hex), oldRows.map(x => x.hex)), related.map(x => x.hex));
  check("join.s5_closability_parent", !!s5Parent && Number(s5Parent.classes) === 2 &&
    Number(s5Parent.remaining_s6_orbits) === 5 && Number(s5Parent.remaining_s7_edge_cost) === 364);
  check("join.k0865_partial_parent", censusParent.classification === "partial_sterile" &&
    censusParent.remaining_s6_orbits === 5 && censusParent.sterile_refs_count === 2 &&
    censusParent.effective_remaining === 3 && censusParent.effective_cost === 229 &&
    censusParent.remaining_s7_edge_cost === 364 && censusParent.sterile_cost === 135);
  check("join.historical_costs", sum(related.map(x => x.cost)) === 364 &&
    sum(related.filter(x => x.category === "sterile").map(x => x.cost)) === 135 &&
    sum(related.filter(x => x.category !== "sterile").map(x => x.cost)) === 229);

  check("fold.76d77e_claims_complete", c76d.fold?.head_after === "1452/174/6396/506144/4669/370058" &&
    c77e.fold?.head_after === "1452/174/6396/506144/4669/370058" &&
    c76d.fold?.receipts === 4 && c77e.fold?.receipts === 4);
  check("fold.76d77e_parent_after", f76d77e.parents_after[PARENT].rows === 3 &&
    f76d77e.parents_after[PARENT].edge_cost === 211 &&
    f76d77e.parents_after[PARENT].rows_before === 5 &&
    f76d77e.parents_after[PARENT].edge_cost_before === 364);
  check("fold.76d77e_closed_rows", sameSet(f76d77e.totals.rows_closed_hexes, [ROW_76D, ROW_77E]) &&
    f76d77e.totals.receipts === 4 && f76d77e.totals.conflict_census_overlaps === 0);
  check("fold.76d77e_second_verification", v76d77e.verdict === "VERIFICATION PASSED");
  check("fold.76c_claim_complete", c76.receipt_fold?.status === "fold-complete" &&
    c76.receipt_fold?.basis_head?.[0] === 1472 && c76.receipt_fold?.frontier_after?.[0] === 1473);
  check("fold.76c_bit61_only_receipt", f76.receipts.length === 1 &&
    f76.receipts[0].bit === 61 && f76.receipts[0].certificate.git_blob_sha === c76.certificate_extraction.actual_extraction.git_blob_sha);
  check("fold.76c_manifest_and_audit", m76.certificates.length === 1 &&
    m76.certificates[0].bit === 61 &&
    m76.certificates[0].sha256 === c76.certificate_extraction.actual_extraction.sha256 &&
    a76.all_checks_pass === true &&
    a76.certificate_manifest_blob_sha === c76.certificate_extraction.manifest_blob_sha);
  check("fold.76c_parent_after", f76.parents_after[PARENT].rows_after === 2 &&
    f76.parents_after[PARENT].edge_cost_after === 135 &&
    f76.parents_after[PARENT].rows_before === 5 &&
    f76.parents_after[PARENT].edge_cost_before === 364);
  check("fold.76c_lost_rows_are_all_nonsterile", sameSet(f76.parents_after[PARENT].lost_rows_hexes, [ROW_76C, ROW_76D, ROW_77E]) &&
    sameSet(lostNonsterile.map(x => x.hex), [ROW_76C, ROW_76D, ROW_77E]));
  check("fold.current_rows_equal_sterile_refs", currentRows.length === 2 &&
    sameSet(currentRows.map(x => x.hex), sterileRefs.map(x => x.hex)) &&
    sameSet(currentRows.map(x => x.hex), historicalSterile.map(x => x.hex)));
  check("fold.current_cost_135", currentRowsCost === 135 &&
    sameSet(currentRows.map(x => String(x.cost)), ["64", "71"]) &&
    currentRowsCost === sum(sterileRefs.map(x => x.cost)));
  check("fold.66i_head1476", f66i.frontier_after_cost66i_bit19.solved_s6_in_manifest === 1476 &&
    f66i.frontier_after_cost66i_bit19.remaining_s5_orbits === 174 &&
    a66i.fold.frontier_after[0] === 1476 &&
    a66i.all_checks_pass === true &&
    c66i.receipt_fold?.status?.startsWith("partial-fold-complete"));
  check("fold.66i_does_not_touch_parent", !currentParent66iAffected &&
    f66i.frontier_after_cost66i_bit19.unique_remaining_s6 === 6372 &&
    f66i.frontier_after_cost66i_bit19.sum_remaining_cost === 504389);
  check("fold.no_s5_parent_closed", f76.parent_count_fully_closed === 0 &&
    f66i.parent_count_fully_closed === 0);

  const current = {
    head: "1476/174/6372/504389/4645/368303",
    parent: PARENT,
    historical_head1410: {
      classification: "partial_sterile",
      remaining_rows: 5,
      sterile_rows: 2,
      nonsterile_rows: 3,
      total_edge_cost: 364,
      effective_edge_cost: 229
    },
    current_head1476: {
      classification: "all_remaining_sterile_for_D10_receipts",
      remaining_rows: currentRows.map(x => ({ hex: x.hex, cost: x.cost, category: x.category })),
      remaining_row_count: currentRows.length,
      remaining_edge_cost: currentRowsCost,
      d10_receipt_closable: false,
      s5_parent_closed: false
    },
    completed_folds: ["cost76d+cost77e (head1450->1452)", "cost76c bit61 (head1472->1473)"],
    current_pending_folds_on_this_parent: [],
    win7_d10_bits_available_in_historical_rows: [19, 37, 49, 61, 69, 99],
    verified_certificate_bits_used_in_folds: [19, 37, 49, 61, 69],
    fallback_unextracted_bits: [99],
    note: "bit99 remains a fallback root and is not counted as a folded receipt; the later cost66i bit19 fold does not affect this parent."
  };

  const output = {
    schema: "n11-rank1-parent-head1476-reconciliation-20261118-v1",
    date: "2026-11-18",
    source_main_head: SOURCE_MAIN_HEAD,
    role: "current-head reconciliation of a historical head-1410 partial-STERILE parent; no new game verdicts",
    inputs,
    historical_audit: {
      path: EXP + "/output/rank1-parent-receipt-channel-20261118.json",
      git_blob_sha1: inputs.rank1_output.git_blob_sha1,
      check_count: rank1.checks.length,
      all_checks_pass: rank1.all_checks_pass,
      record_time_fold_pending_bands: rank1.summary.fold_pending_bands,
      time_scope_note: "The prior F.folds_pending check reads pinned sweep-record fields, not the current v2/v8 claims. Those record-time fields remain historically true but are stale as a current-main status."
    },
    fold_reconciliation: {
      cost76d77e: {
        status: "fold-complete",
        head_before: c76d.fold.head_before,
        head_after: c76d.fold.head_after,
        receipts: f76d77e.totals.receipts,
        rows_closed: f76d77e.totals.rows_closed_hexes,
        parent_rows_after: f76d77e.parents_after[PARENT]
      },
      cost76c: {
        status: c76.receipt_fold.status,
        basis_head: c76.receipt_fold.basis_head,
        frontier_after: c76.receipt_fold.frontier_after,
        folded_bits: [61],
        fallback_unextracted_bits: [99],
        cumulative_parent_rows_after: f76.parents_after[PARENT],
        fold_audit_all_checks_pass: a76.all_checks_pass
      },
      cost66i_bit19: {
        status: c66i.receipt_fold.status,
        frontier_after: f66i.frontier_after_cost66i_bit19,
        target_parent_affected: currentParent66iAffected
      }
    },
    current_parent: current,
    checks,
    check_count: checks.length,
    all_pass: checks.every(x => x.pass),
    interpretation_guard: "The two remaining S6 rows are STERILE, so K0863 excludes every WIN7-D10 receipt root from covering them. This does not prove LOSS, does not close the S5 parent, and says nothing decisive about the standard 11x11 empty board.",
    unknown_status: "11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
  };

  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(output, null, 2) + "\n");
  const failed = checks.filter(x => !x.pass);
  const bytes = fs.readFileSync(OUT);
  console.log(JSON.stringify({
    output: path.relative(ROOT, OUT),
    check_count: checks.length,
    passed: checks.length - failed.length,
    failed: failed.length,
    all_pass: failed.length === 0,
    output_git_blob_sha1: gitBlobSha1(bytes),
    output_sha256: crypto.createHash("sha256").update(bytes).digest("hex"),
    failures: failed
  }, null, 2));
  if (failed.length) process.exitCode = 1;
}

main();
