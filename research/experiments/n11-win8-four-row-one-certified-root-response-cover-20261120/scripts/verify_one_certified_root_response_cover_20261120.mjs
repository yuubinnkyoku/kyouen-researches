#!/usr/bin/env node
// Independent geometric re-derivation of the four-row WIN8 response-cover plan.
// Uses 4x4 Bareiss determinants and all unordered two-stone extensions.
// It does not run DFPN and does not close S6 rows.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const EXP_DIR = path.resolve(SCRIPT_DIR, "..");
const REPO_ROOT = path.resolve(SCRIPT_DIR, "../../../..");
const OUT_PATH = path.join(EXP_DIR, "output", "one-certified-root-response-cover-second-verification-20261120.json");
const N = 11;
const K1096_ROOT = "00000000000000003800000008003180";
const K1095_ROOT = "0000000800000000380000000810000a";
const EXPECTED_REFUTED_HIT = "00000008000000003800000008100006";
const HEADER = "n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS";

const PINS = {
  k1085: {
    path: "research/experiments/n11-residual72-unsafe-classification-add2stones-20261120/output/residual72-unsafe-classification-add2stones-20261120.json",
    sha256: "5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e",
    blob: "cb66fe9dd6454783bece126a643bf247d84def20"
  },
  k1097: {
    path: "research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json",
    sha256: "2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40",
    blob: "4660c012333b04896c36a23a0837fbdbc2572ef9"
  },
  plan: {
    path: "research/experiments/n11-win8-four-row-two-ply-response-cover-20261120/output/selected-response-cover-plan.json",
    sha256: "633c11719d8eef91062b56dc5eab772807b98a8e586905eaeec153a673bee7c0",
    blob: "1c8f9cd34a19922ae8abe0f0840c0d60273b390d"
  },
  k1096Certificate: {
    path: "research/experiments/n11-residual72-win8-cert-extract-root8003180-20261120/certs/win8-root-00000000000000003800000008003180-20261120.n11",
    sha256: "1393128972a2ee2bd7586239c830caac967ee45166be8ed87107907c42f23e2c",
    blob: "afc0a1bc005215696e18e02baaaad3c3bf9ba599"
  },
  k1096Audit: {
    path: "research/experiments/n11-residual72-win8-cert-extract-root8003180-20261120/output/win8-cert-extract-verification-20261120.json",
    sha256: "ad0d9fb3a30edbd76fcb5562ab01f1e7e51781381377a04fa4a195378eb887da",
    blob: "fa70a6f12927ada9bed3da4c02c7dffef87631ad"
  },
  priorVerifier: {
    path: "research/experiments/n11-win8-four-row-two-ply-response-cover-20261120/scripts/verify_response_cover_plan.py",
    blob: "e87237026bdf207b8f3052dc6e4fc8e425d40f74"
  }
};

function need(ok, message) {
  if (!ok) throw new Error(message);
}
function sha256(bytes) {
  return crypto.createHash("sha256").update(bytes).digest("hex");
}
function gitBlobSha(bytes) {
  const header = Buffer.from("blob " + bytes.length + "\0", "utf8");
  return crypto.createHash("sha1").update(Buffer.concat([header, bytes])).digest("hex");
}
function readPinned(name) {
  const pin = PINS[name];
  const bytes = fs.readFileSync(path.join(REPO_ROOT, pin.path));
  if (pin.sha256) need(sha256(bytes) === pin.sha256, name + " SHA-256 mismatch");
  need(gitBlobSha(bytes) === pin.blob, name + " Git blob SHA-1 mismatch");
  return bytes;
}
function readJson(name) {
  return JSON.parse(readPinned(name).toString("utf8"));
}
function bit(p) {
  return 1n << BigInt(p);
}
function pointsOf(mask) {
  const out = [];
  for (let p = 0; p < 121; p++) if ((mask & bit(p)) !== 0n) out.push(p);
  return out;
}
function popcount(mask) {
  let n = 0;
  while (mask !== 0n) {
    mask &= mask - 1n;
    n++;
  }
  return n;
}
function hex(mask) {
  return mask.toString(16).padStart(32, "0");
}
function lifted(p) {
  const x = p % N;
  const y = Math.floor(p / N);
  return [BigInt(x * x + y * y), BigInt(x), BigInt(y), 1n];
}
// Bareiss fraction-free elimination; no floating point and no division except exact pivots.
function det4Bareiss(ps) {
  let a = ps.map(lifted);
  let sign = 1n;
  let previousPivot = 1n;
  for (let col = 0; col < 3; col++) {
    let pivotRow = col;
    while (pivotRow < 4 && a[pivotRow][col] === 0n) pivotRow++;
    if (pivotRow === 4) return 0n;
    if (pivotRow !== col) {
      const tmp = a[pivotRow];
      a[pivotRow] = a[col];
      a[col] = tmp;
      sign = -sign;
    }
    const pivot = a[col][col];
    for (let row = col + 1; row < 4; row++) {
      for (let j = col + 1; j < 4; j++) {
        const numerator = a[row][j] * pivot - a[row][col] * a[col][j];
        need(numerator % previousPivot === 0n, "Bareiss non-exact division");
        a[row][j] = numerator / previousPivot;
      }
      a[row][col] = 0n;
    }
    previousPivot = pivot;
  }
  return sign * a[3][3];
}
function safeMask(mask) {
  const ps = pointsOf(mask);
  for (let i = 0; i < ps.length; i++) {
    for (let j = i + 1; j < ps.length; j++) {
      for (let k = j + 1; k < ps.length; k++) {
        for (let l = k + 1; l < ps.length; l++) {
          if (det4Bareiss([ps[i], ps[j], ps[k], ps[l]]) === 0n) return false;
        }
      }
    }
  }
  return true;
}
function transformPoint(p, t) {
  const x = p % N;
  const y = Math.floor(p / N);
  const table = [
    [x, y],
    [10 - y, x],
    [10 - x, 10 - y],
    [y, 10 - x],
    [10 - x, y],
    [x, 10 - y],
    [y, x],
    [10 - y, 10 - x]
  ];
  const xy = table[t];
  return N * xy[1] + xy[0];
}
function transform(mask, t) {
  let out = 0n;
  for (const p of pointsOf(mask)) out |= bit(transformPoint(p, t));
  return out;
}
function canonical(mask) {
  let best = null;
  for (let t = 0; t < 8; t++) {
    const image = transform(mask, t);
    if (best === null || image < best) best = image;
  }
  return best;
}
function obligationKey(rowIndex, move) {
  return rowIndex + ":" + move;
}
function coverageRecords(coverage, rows) {
  const result = [];
  for (let ri = 0; ri < rows.length; ri++) {
    const moves = [];
    for (let p = 0; p < 121; p++) if (coverage.has(obligationKey(ri, p))) moves.push(p);
    if (moves.length) result.push({ row_hex: hex(rows[ri]), first_moves: moves });
  }
  return result;
}
function intersectsCount(a, b) {
  let n = 0;
  for (const x of a) if (b.has(x)) n++;
  return n;
}
function intersection(a, b) {
  const out = new Set();
  for (const x of a) if (b.has(x)) out.add(x);
  return out;
}

const k1085Bytes = readPinned("k1085");
const k1097Bytes = readPinned("k1097");
const planBytes = readPinned("plan");
const certBytes = readPinned("k1096Certificate");
const auditBytes = readPinned("k1096Audit");
const priorVerifierBytes = fs.readFileSync(path.join(REPO_ROOT, PINS.priorVerifier.path));
need(gitBlobSha(priorVerifierBytes) === PINS.priorVerifier.blob, "prior verifier blob mismatch");

const k1085 = JSON.parse(k1085Bytes.toString("utf8"));
const k1097 = JSON.parse(k1097Bytes.toString("utf8"));
const plan = JSON.parse(planBytes.toString("utf8"));
const k1096Audit = JSON.parse(auditBytes.toString("utf8"));

need(k1085.schema === "n11-residual72-unsafe-classification-add2stones-20261120-v1", "K1085 schema");
need(k1085.base_state.residual_row_hex.length === 72, "K1085 residual72 count");
need(k1085.add_two_stones_census.safe8 === 120474, "K1085 safe8 count");
need(k1097.schema === "n11-residual72-safe8-refuted50-refsolve-20261120-v1", "K1097 schema");
need(k1097.exclusion.refuted_d10_roots_excluded.length === 50, "K1097 REFUTED-D10 count");
need(k1097.exclusion.win8_d10_candidates.length === 16, "K1097 WIN8 candidate count");
need(plan.schema === "n11-win8-four-row-two-ply-response-cover-plan-20261120-v2", "response-cover plan schema");
need(plan.parent_rows.length === 4, "four parent rows");
need(plan.fixed_roots.length === 2 && plan.additional_roots.length === 147, "published plan root counts");
need(plan.source_pins.k1096_certificate_sha256 === PINS.k1096Certificate.sha256, "plan K1096 certificate SHA pin");
need(plan.source_pins.k1096_certificate_git_blob_sha1 === PINS.k1096Certificate.blob, "plan K1096 certificate blob pin");
need(plan.source_pins.k1096_audit_sha256 === PINS.k1096Audit.sha256, "plan K1096 audit SHA pin");
need(plan.source_pins.k1097_refsolve_git_blob_sha1 === PINS.k1097.blob, "plan K1097 blob pin");
need(plan.source_pins.k1095_sweep_sha256 === k1097.inputs.k1095_sweep_sha256, "K1095 sweep pin crosscheck");
need(plan.source_pins.k1086_sweep_sha256 === k1097.inputs.k1086_sweep_sha256, "K1086 sweep pin crosscheck");

const certText = certBytes.toString("utf8");
const certLines = certText.replace(/\r/g, "").trimEnd().split("\n");
need(certLines[0] === HEADER, "K1096 certificate header");
need(certLines.includes(K1096_ROOT), "K1096 certificate root row absent");
need(certLines.length === 34531, "K1096 certificate line count");
need(k1096Audit.all_gates_pass === true && k1096Audit.gate_count === 18, "K1096 audit aggregate");
need(k1096Audit.gates.length === 18 && k1096Audit.gates.every(g => g.passed === true), "K1096 audit gates");
need(k1096Audit.root === K1096_ROOT && k1096Audit.verdict.includes("triple-verified"), "K1096 audit root/verdict");

const residual72 = new Set(k1085.base_state.residual_row_hex);
const rowsHex = plan.parent_rows;
need(rowsHex.every(h => residual72.has(h)), "four parent rows are not all in K1085 residual72");
const rows = rowsHex.map(h => BigInt("0x" + h));
need(rows.every(m => popcount(m) === 6 && safeMask(m)), "parent row safety/stone count");

const legalMoves = rows.map(row => {
  const moves = [];
  for (let p = 0; p < 121; p++) {
    if ((row & bit(p)) === 0n && safeMask(row | bit(p))) moves.push(p);
  }
  return moves;
});
const obligations = new Set();
for (let ri = 0; ri < rows.length; ri++) {
  for (const p of legalMoves[ri]) obligations.add(obligationKey(ri, p));
}
need(legalMoves.map(x => x.length).join(",") === "79,82,69,74", "legal first-move counts");
need(obligations.size === 304, "obligation count");

const allRootsSet = new Set();
let generatedPairs = 0;
let safePairs = 0;
for (const row of rows) {
  const occupied = new Set(pointsOf(row));
  const availablePoints = [];
  for (let p = 0; p < 121; p++) if (!occupied.has(p)) availablePoints.push(p);
  need(availablePoints.length === 115, "two-stone extension point count");
  for (let i = 0; i < availablePoints.length; i++) {
    for (let j = i + 1; j < availablePoints.length; j++) {
      generatedPairs++;
      const root = row | bit(availablePoints[i]) | bit(availablePoints[j]);
      if (!safeMask(root)) continue;
      safePairs++;
      allRootsSet.add(hex(canonical(root)));
    }
  }
}
const allRoots = [...allRootsSet].sort();
need(generatedPairs === 26220, "raw two-stone pair count");
need(safePairs === 9744, "safe raw two-stone pair count");
need(allRoots.length === 9490, "safe8 D4 orbit count");
for (const h of allRoots) {
  const m = BigInt("0x" + h);
  need(popcount(m) === 8 && safeMask(m) && canonical(m) === m, "candidate root shape/safety/canonicality " + h);
}

const allRootSet = new Set(allRoots);
const knownWins = new Set(k1097.exclusion.win8_d10_candidates.map(h => hex(canonical(BigInt("0x" + h)))));
const knownRefuted = new Set(k1097.exclusion.refuted_d10_roots_excluded.map(h => hex(canonical(BigInt("0x" + h)))));
const winHits = [...allRootSet].filter(h => knownWins.has(h)).sort();
const refutedHits = [...allRootSet].filter(h => knownRefuted.has(h)).sort();
need(winHits.join(",") === [K1095_ROOT, K1096_ROOT].sort().join(","), "known WIN8 candidate intersection");
need(refutedHits.join(",") === EXPECTED_REFUTED_HIT, "known REFUTED-D10 intersection");
const availableRoots = allRoots.filter(h => !knownRefuted.has(h));
need(availableRoots.length === 9489, "available safe8 orbit count");

function rootCoverage(rootHex) {
  const root = BigInt("0x" + rootHex);
  const images = new Set();
  for (let t = 0; t < 8; t++) images.add(hex(transform(root, t)));
  const covered = new Set();
  for (const imageHex of images) {
    const image = BigInt("0x" + imageHex);
    for (let ri = 0; ri < rows.length; ri++) {
      if ((image & rows[ri]) !== rows[ri]) continue;
      const difference = image ^ rows[ri];
      if (popcount(difference) !== 2) continue;
      for (const p of pointsOf(difference)) covered.add(obligationKey(ri, p));
    }
  }
  return covered;
}

const allCoverageHistogram = {};
const coverageByRoot = new Map();
for (const rootHex of availableRoots) {
  const covered = rootCoverage(rootHex);
  coverageByRoot.set(rootHex, covered);
  const n = covered.size;
  allCoverageHistogram[n] = (allCoverageHistogram[n] || 0) + 1;
}
need(JSON.stringify(allCoverageHistogram) === JSON.stringify({ "2": 9237, "4": 251, "8": 1 }), "all-root obligation coverage histogram");

const k1096Root = hex(canonical(BigInt("0x" + K1096_ROOT)));
const k1095Root = hex(canonical(BigInt("0x" + K1095_ROOT)));
need(k1096Root === K1096_ROOT && k1095Root === K1095_ROOT, "fixed root canonicality");
need(availableRoots.includes(k1096Root) && availableRoots.includes(k1095Root), "fixed roots in available candidate universe");
const k1096Coverage = coverageByRoot.get(k1096Root);
const k1095Coverage = coverageByRoot.get(k1095Root);
need(k1096Coverage.size === 8, "K1096 proof-root obligation coverage");
need(k1095Coverage.size === 2, "K1095 candidate obligation coverage");
const k1096Records = coverageRecords(k1096Coverage, rows);
const k1095Records = coverageRecords(k1095Coverage, rows);
need(JSON.stringify(k1096Records) === JSON.stringify(plan.fixed_roots[0].coverage), "K1096 coverage differs from published plan");
need(JSON.stringify(k1095Records) === JSON.stringify(plan.fixed_roots[1].coverage), "K1095 coverage differs from published plan");
need(plan.fixed_roots[0].status === "certificate-verified", "K1096 fixed-root status");
need(plan.fixed_roots[1].status === "WIN8-D10-candidate-certificate-not-yet-extracted", "K1095 is not a certificate");

const positive = new Set([...obligations].filter(x => !k1096Coverage.has(x)));
need(positive.size === 296, "positive obligations after fixing K1096 only");
const afterK1096Histogram = {};
let maxAdditionalCoverage = 0;
for (const rootHex of availableRoots) {
  if (rootHex === k1096Root) continue;
  const n = intersectsCount(coverageByRoot.get(rootHex), positive);
  afterK1096Histogram[n] = (afterK1096Histogram[n] || 0) + 1;
  if (n > maxAdditionalCoverage) maxAdditionalCoverage = n;
}
need(JSON.stringify(afterK1096Histogram) === JSON.stringify({ "2": 9488 }), "every nonfixed candidate must cover exactly two positive obligations");
need(maxAdditionalCoverage === 2, "maximum additional-root coverage");

const selectedRoots = [k1095Root, ...plan.additional_roots.map(h => hex(canonical(BigInt("0x" + h))))];
need(selectedRoots.length === 148 && new Set(selectedRoots).size === 148, "148 distinct additional roots");
const selectedUnion = new Set();
const selectedRecords = [];
for (let i = 0; i < selectedRoots.length; i++) {
  const rootHex = selectedRoots[i];
  need(availableRoots.includes(rootHex) && rootHex !== k1096Root, "selected root unavailable or duplicates K1096: " + rootHex);
  const covered = intersection(coverageByRoot.get(rootHex), positive);
  need(covered.size === 2, "selected root does not cover exactly two positive obligations: " + rootHex);
  const overlap = intersectsCount(selectedUnion, covered);
  need(overlap === 0, "selected roots overlap on an obligation: " + rootHex);
  for (const obligation of covered) selectedUnion.add(obligation);
  selectedRecords.push({
    root_hex: rootHex,
    source: rootHex === k1095Root ? "K1095_WIN8_D10_candidate_no_certificate" : "published_147_root_geometric_plan_no_verdict",
    obligations: [...covered].sort()
  });
}
need(selectedUnion.size === 296, "selected 148 roots do not cover all positive obligations");
need([...positive].every(x => selectedUnion.has(x)), "positive obligation left uncovered");

const lowerBound = Math.ceil(positive.size / maxAdditionalCoverage);
need(lowerBound === 148, "dual/counting lower bound");
need(selectedRecords.length === lowerBound, "matching upper bound does not attain lower bound");

const checks = [
  { gate: "all_input_sha256_and_git_blob_pins", passed: true },
  { gate: "prior_verifier_blob_pin", passed: true },
  { gate: "k1085_residual72_and_four_parent_membership", passed: true },
  { gate: "four_parent_rows_are_safe_six_stone_positions", passed: true },
  { gate: "legal_first_moves_rederived_79_82_69_74", passed: true },
  { gate: "304_first_move_obligations_rederived", passed: true },
  { gate: "all_safe8_extensions_rebuilt_by_bareiss_and_d4", passed: true },
  { gate: "9490_candidate_orbits_and_9744_safe_raw_pairs", passed: true },
  { gate: "known_win8_intersection_is_exactly_k1096_and_k1095", passed: true },
  { gate: "known_refuted_intersection_is_exactly_one_root", passed: true },
  { gate: "k1096_certificate_bytes_and_existing_18_gate_audit_pinned", passed: true },
  { gate: "k1096_certificate_is_the_only_fixed_proof_root", passed: true },
  { gate: "k1096_covers_exactly_eight_obligations", passed: true },
  { gate: "k1095_reclassified_as_unproved_candidate_covering_two", passed: true },
  { gate: "296_positive_obligations_after_k1096", passed: true },
  { gate: "all_9488_nonfixed_candidates_cover_exactly_two_positive_obligations", passed: true },
  { gate: "148_additional_roots_are_safe_unique_and_available", passed: true },
  { gate: "148_roots_cover_296_obligations_exactly_once", passed: true },
  { gate: "lower_bound_148_equals_constructed_cover_148", passed: true }
];

const selectedBySource = {
  k1095_candidate_without_certificate: 1,
  safe8_candidates_without_verdict_or_certificate: 147
};
const audit = {
  schema: "n11-win8-four-row-one-certified-root-response-cover-second-verification-v1",
  date: "2026-11-20",
  status: "verified-geometric-response-cover-not-game-solved",
  all_gates_pass: checks.every(x => x.passed),
  gate_count: checks.length,
  inputs: Object.fromEntries(Object.entries(PINS).map(([name, pin]) => [name, {
    path: pin.path,
    sha256: pin.sha256 || null,
    git_blob_sha1: pin.blob
  }])),
  prior_verifier: {
    path: PINS.priorVerifier.path,
    git_blob_sha1: PINS.priorVerifier.blob,
    method_difference: "This verifier enumerates all unordered two-stone extensions and uses 4x4 Bareiss elimination; the prior verifier uses sequential legal additions and a 24-term 4x4 determinant."
  },
  parents: {
    rows: rowsHex,
    legal_first_moves: legalMoves.map((moves, i) => ({ row_hex: rowsHex[i], count: moves.length, moves })),
    obligations_total: obligations.size
  },
  candidate_universe: {
    raw_two_stone_pairs: generatedPairs,
    safe_raw_extensions: safePairs,
    safe8_d4_orbits_before_refuted_exclusion: allRoots.length,
    known_win8_candidate_hits: winHits,
    known_refuted_d10_hits: refutedHits,
    available_safe8_d4_orbits_after_refuted_exclusion: availableRoots.length,
    all_root_obligation_coverage_histogram: allCoverageHistogram
  },
  proof_backed_fixed_root: {
    root_hex: k1096Root,
    certificate_sha256: PINS.k1096Certificate.sha256,
    certificate_git_blob_sha1: PINS.k1096Certificate.blob,
    certificate_bytes: certBytes.length,
    certificate_lines: certLines.length,
    existing_audit_sha256: PINS.k1096Audit.sha256,
    existing_audit_gate_count: k1096Audit.gate_count,
    existing_audit_all_gates_pass: k1096Audit.all_gates_pass,
    reverified_in_this_run: false,
    obligations_covered: k1096Records
  },
  additional_obligations: {
    total: positive.size,
    coverage_histogram_over_all_nonfixed_candidates: afterK1096Histogram,
    maximum_coverage_per_nonfixed_candidate: maxAdditionalCoverage
  },
  optimal_response_cover: {
    lower_bound_additional_roots: lowerBound,
    constructed_additional_roots: selectedRecords.length,
    total_roots_including_k1096: selectedRecords.length + 1,
    exact_once_coverage: true,
    k1095_reclassified_as_additional_candidate: true,
    selected_root_status_counts: selectedBySource,
    selected_roots: selectedRecords
  },
  checks,
  interpretation_guard: [
    "K1096 is the only proof-backed root fixed in this plan; its existing triple-verification audit and certificate bytes are hash-pinned but its proof is not re-run here.",
    "K1095 is only a WIN8-D10 candidate and is counted among the 148 additional roots, not as an already-proved root.",
    "The other 147 selected roots are safe 8-stone candidates only; this audit assigns them no WIN/LOSS verdict.",
    "The 149-root minimum is for this four-parent, two-ply response-cover construction after excluding the known REFUTED-D10 orbit, conditional on proving all 148 additional roots.",
    "This is a geometric response-cover result only: no S6 row is closed, no receipt is folded, and no game value is inferred.",
    "REFUTED-D10 is not a LOSS proof; node counts and solved counts are not game outcomes.",
    "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
  ]
};

need(audit.all_gates_pass, "audit gates did not all pass");
const output = JSON.stringify(audit, null, 2) + "\n";
fs.mkdirSync(path.dirname(OUT_PATH), { recursive: true });
fs.writeFileSync(OUT_PATH, output, "utf8");
process.stdout.write(JSON.stringify({
  all_gates_pass: audit.all_gates_pass,
  gate_count: audit.gate_count,
  candidate_orbits: allRoots.length,
  available_orbits: availableRoots.length,
  obligations: obligations.size,
  fixed_k1096_obligations: k1096Coverage.size,
  positive_obligations: positive.size,
  nonfixed_coverage_histogram: afterK1096Histogram,
  additional_roots: selectedRecords.length,
  lower_bound: lowerBound,
  total_roots: selectedRecords.length + 1,
  output_sha256: sha256(Buffer.from(output, "utf8"))
}) + "\n");
