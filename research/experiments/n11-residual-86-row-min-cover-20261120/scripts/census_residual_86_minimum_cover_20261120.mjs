#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";

const ROOT = process.cwd();
const SOURCE_MAIN_HEAD = "d94936209510177c599cf1fb05be919e71434d61";
const FIRST_WIN7_ROOT = "00000000000000821082000010800000";
const SOLE_SCAN_PARENT = "00000000000000801222000000800000";
const SOLE_SCAN_ROOT = "00000000000000a09002200080000000";
const OUTPUT_PATH = "research/experiments/n11-residual-86-row-min-cover-20261120/output/residual-86-minimum-cover-20261120.json";

const PIN = {
  resolve4: ["research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/output/post-eighth-receipt-cover-resolve4-20261119.json", "4560b7cd9b3cae57d79005464ff2f2f239287b24"],
  scan: ["research/experiments/n11-class2-lane-sterile-unclosability-20261116/output/theorem-applicability-scan-20261116.json", "24f214e6a9dd721ef95ac97d6b84cf34af33b14b"],
  joint: ["research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-parent-cover-sharing-cost16-20261118.json", "40581746dc3304bdaff4b1934fd6f1d3d2981ea5"],
  audit: ["research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-cover-cost16-five-parent-independent-audit-20261118.json", "7cdc7c9ef341b5d9759923b3fc4986231c48895f"],
  head1476: ["research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/head1476-cost71e-full-universe-verdict-join-20261118.json", "65d0c7ce0200638a50db5451b11b8cb88ec64b5d"],
  cost78c: ["research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost78c-inflight-20261117.json", "626409d50d0a7bb1b925ebecbff7dbee9adfa398"],
  cost79c: ["research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost79c-inflight-20261118.json", "054923a47ea0387b25f734222c499e60c054109b"],
  cost73j: ["research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73j-inflight-20261117.json", "74fc3417391e30cf4cff9c2ffce059dce529ed86"],
  globalFold: ["research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-receipt-harvest-global-fold-20261118.json", "753a4bf4d0e11bea894111f9fa43bcff5e9ab7dc"],
  fold78: ["research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost78c-79c-receipts-recompute-20261118.json", "7e6144cc4bc92c34faa14bed3058cde64fb3880e"],
  fold456: ["research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/output/fourth-fifth-sixth-win7-receipt-fold-20261119.json", "f794c2bc5562a4a28e1f9054f95ffc447cdf8dfd"],
  fold7: ["research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/output/seventh-win7-receipt-fold-20261119.json", "64fcd27daced861dd036a20b6248ed5b0473e818"],
  fold8: ["research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/output/eighth-win7-receipt-fold-20261119.json", "905d8c1776aa7608e8a38bd110ae78e61a31e34b"],
  sweep48: ["research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/residual-48-root-depth10-sweep-20261119.json", "37aba599d0b69275225bf231d56cb18feed14090"],
  sweep35: ["research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/sweep35/eligible-29-candidate-root-depth10-sweep-20261119.json", "9c00d6cfc8faeb976043e297335b5615364967f5"],
  sweep28: ["research/experiments/n11-head1410-witness-28-root-full-depth10-sweep-20261119/output/witness-28-root-depth10-sweep-20261119.json", "a4e5d6f8ef180b0b7910ea90bf240c1a3a773134"],
  firstReceiptKnowledge: ["research/knowledge/items/K1029-n11-first-residual-root-win7-d10-certificate.md", "1c5ea31b4ee252049c1cfa382e5953c47eee8f47"],
  latestN11Knowledge: ["research/knowledge/items/K1046-n11-117pool-d10-completion-7th8th-win7-certificates.md", "3685a35749eefc8477885640ef75921b0c896028"],
  rules: ["research/knowledge/items/K0001-complete-call-rules.md", "ef7483e011d72e0048d667313b6c996d3472729f"],
  candidateConvention: ["research/knowledge/items/K0868-n11-s6-s7-sweep-candidate-convention.md", "b097210d0b49d7cf014cc6a554298b1e49e83384"],
  resolve4Script: ["research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/resolve4.py", "c55ed9fbec19ca6b7419918fa14e45d6c6f6e842"]
};

function need(ok, message) {
  if (!ok) throw new Error(message);
}
function readPinned(name) {
  const [relative, expected] = PIN[name];
  const text = fs.readFileSync(path.join(ROOT, relative), "utf8");
  const bytes = Buffer.from(text, "utf8");
  const actual = createHash("sha1")
    .update(Buffer.concat([Buffer.from("blob " + bytes.length + "\0"), bytes]))
    .digest("hex");
  need(actual === expected, name + " Git blob mismatch: " + actual);
  return text;
}
function load(name) {
  return JSON.parse(readPinned(name));
}
const raw = {};
for (const name of Object.keys(PIN)) raw[name] = readPinned(name);
const data = {};
for (const name of Object.keys(PIN)) {
  if (!["firstReceiptKnowledge", "latestN11Knowledge", "rules", "candidateConvention", "resolve4Script"].includes(name)) {
    data[name] = JSON.parse(raw[name]);
  }
}
need(raw.firstReceiptKnowledge.includes(FIRST_WIN7_ROOT), "K1029 first WIN7 root anchor");
need(raw.candidateConvention.includes("det4"), "K0868 determinant convention anchor");

function stones(mask) {
  const out = [];
  for (let p = 0; p < 121; p++) if ((mask >> BigInt(p)) & 1n) out.push(p);
  return out;
}
function hex(mask) {
  return mask.toString(16).padStart(32, "0");
}
function d4Canon(mask) {
  let best = null;
  for (let t = 0; t < 8; t++) {
    let z = 0n;
    for (let p = 0; p < 121; p++) {
      if (!((mask >> BigInt(p)) & 1n)) continue;
      const x = p % 11, y = Math.floor(p / 11);
      let X, Y;
      if (t === 0) { X = x; Y = y; }
      else if (t === 1) { X = 10 - y; Y = x; }
      else if (t === 2) { X = 10 - x; Y = 10 - y; }
      else if (t === 3) { X = y; Y = 10 - x; }
      else if (t === 4) { X = 10 - x; Y = y; }
      else if (t === 5) { X = x; Y = 10 - y; }
      else if (t === 6) { X = y; Y = x; }
      else { X = 10 - y; Y = 10 - x; }
      z |= 1n << BigInt(11 * Y + X);
    }
    if (best === null || z < best) best = z;
  }
  return hex(best);
}
function det3(a, b, c) {
  const [x1, y1] = a, [x2, y2] = b, [x3, y3] = c;
  const q1 = BigInt(x1 * x1 + y1 * y1);
  const q2 = BigInt(x2 * x2 + y2 * y2);
  const q3 = BigInt(x3 * x3 + y3 * y3);
  return q1 * BigInt(x2 * y3 - x3 * y2)
       - q2 * BigInt(x1 * y3 - x3 * y1)
       + q3 * BigInt(x1 * y2 - x2 * y1);
}
function det4Expansion(points) {
  const [a, b, c, d] = points;
  return det3(a, b, c) - det3(a, b, d) + det3(a, c, d) - det3(b, c, d);
}
function det4Bareiss(points) {
  const a = points.map(([x, y]) => {
    const X = BigInt(x), Y = BigInt(y);
    return [X * X + Y * Y, X, Y, 1n];
  });
  let sign = 1n, previous = 1n;
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
        need(numerator % previous === 0n, "Bareiss division is not exact");
        a[i][j] = numerator / previous;
      }
    }
    for (let i = k + 1; i < 4; i++) a[i][k] = 0n;
    previous = pivot;
  }
  return sign * a[3][3];
}
let determinantCalls = 0;
function det4(points) {
  determinantCalls++;
  const a = det4Expansion(points);
  const b = det4Bareiss(points);
  need(a === b, "determinant methods disagree");
  return a;
}
const point = p => [p % 11, Math.floor(p / 11)];
function safe(stoneBits) {
  for (let a = 0; a < stoneBits.length; a++)
    for (let b = a + 1; b < stoneBits.length; b++)
      for (let c = b + 1; c < stoneBits.length; c++)
        for (let d = c + 1; d < stoneBits.length; d++)
          if (det4([point(stoneBits[a]), point(stoneBits[b]), point(stoneBits[c]), point(stoneBits[d])]) === 0n) return false;
  return true;
}
function legalAdds(stoneBits) {
  const occupied = new Set(stoneBits);
  const out = [];
  for (let q = 0; q < 121; q++) {
    if (occupied.has(q)) continue;
    let legal = true;
    for (let a = 0; a < stoneBits.length && legal; a++)
      for (let b = a + 1; b < stoneBits.length && legal; b++)
        for (let c = b + 1; c < stoneBits.length; c++) {
          if (det4([point(stoneBits[a]), point(stoneBits[b]), point(stoneBits[c]), point(q)]) === 0n) {
            legal = false;
            break;
          }
        }
    if (legal) out.push(q);
  }
  return out;
}
function addCanonical(set, rootHex) {
  set.add(d4Canon(BigInt("0x" + rootHex)));
}
const knownRefuted = new Set(), knownWin = new Set();
function addTransferMap(source) {
  for (const x of Object.values(source.transfers || {})) {
    if (x.verdict === "REFUTED-D10") addCanonical(knownRefuted, x.root_canon);
    else if (x.verdict === "WIN7-D10") addCanonical(knownWin, x.root_canon);
  }
}
for (const x of data.head1476.candidate_root_universe.matched_roots) {
  if (x.verdict === "REFUTED-D10") addCanonical(knownRefuted, x.d4_canon_root);
  else if (x.verdict === "WIN7-D10") addCanonical(knownWin, x.d4_canon_root);
}
for (const name of ["cost78c", "cost79c"]) {
  const c = data[name];
  addTransferMap(c);
  for (const bit of c.actual_execution.refuted_d10_bits)
    addCanonical(knownRefuted, (BigInt("0x" + c.s6_child) | (1n << BigInt(bit))).toString(16));
  for (const bit of c.actual_execution.win7_d10_bits)
    addCanonical(knownWin, (BigInt("0x" + c.s6_child) | (1n << BigInt(bit))).toString(16));
}
{
  const c = data.cost73j;
  addTransferMap(c);
  const wins = new Set(c.actual_execution.results.win7_d10_bits);
  for (const bit of c.engine_candidate_bits.open_bits) {
    const root = (BigInt("0x" + c.s6_child) | (1n << BigInt(bit))).toString(16);
    addCanonical(wins.has(bit) ? knownWin : knownRefuted, root);
  }
}
function addReceiptRows(container) {
  for (const row of container?.receipts_by_row || [])
    for (const x of row.receipts || []) addCanonical(knownWin, x.root);
  for (const x of container?.marginal_by_root || []) addCanonical(knownWin, x.root);
}
addReceiptRows(data.globalFold);
addReceiptRows(data.fold78.new_receipt_coverage);
for (const source of [data.fold456, data.fold7, data.fold8])
  for (const x of source.receipts) addCanonical(knownWin, x.root);
for (const x of data.sweep48.classification.refuted_d10.roots) addCanonical(knownRefuted, x);
for (const x of data.sweep48.classification.win7_d10.roots) addCanonical(knownWin, x);
for (const x of data.sweep35.classification.refuted_d10.roots) addCanonical(knownRefuted, x);
for (const x of data.sweep35.classification.win7_d10.roots) addCanonical(knownWin, x);
for (const x of data.resolve4.verdict_pool.sweep6_ingest.refuted) addCanonical(knownRefuted, x);
for (const x of data.resolve4.verdict_pool.sweep6_ingest.win) addCanonical(knownWin, x);
for (const x of data.sweep28.classification.refuted_d10.roots) addCanonical(knownRefuted, x);
for (const x of data.sweep28.classification.win7_d10.roots) addCanonical(knownWin, x);
addCanonical(knownWin, FIRST_WIN7_ROOT);
const baseJoin = {
  refuted: knownRefuted.size,
  win: knownWin.size,
  conflicts: [...knownRefuted].filter(x => knownWin.has(x)).length
};
need(baseJoin.refuted === 340 && baseJoin.win === 164 && baseJoin.conflicts === 0, "K1046 explicit known-verdict join mismatch");

const scanTransfers = new Set();
const scanWinTransfers = new Set();
for (const [child, target] of Object.entries(data.scan.targets)) {
  for (const v of target.transferred?.["REFUTED-D10"] || []) {
    const root = d4Canon(BigInt("0x" + child) | (1n << BigInt(v.bit)));
    scanTransfers.add(root);
    knownRefuted.add(root);
  }
  for (const v of target.transferred?.["WIN7-D10"] || []) {
    const root = d4Canon(BigInt("0x" + child) | (1n << BigInt(v.bit)));
    scanTransfers.add(root);
    scanWinTransfers.add(root);
    knownWin.add(root);
  }
}
need(scanWinTransfers.size === 0, "unexpected K0863 WIN7-D10 transfers");
need(data.scan.engine_map.source_conflicts.length === 0, "K0863 source conflict");

const joined = {
  refuted: knownRefuted.size,
  win: knownWin.size,
  conflicts: [...knownRefuted].filter(x => knownWin.has(x)).length,
  scan_transfers: scanTransfers.size
};
need(joined.refuted === 455 && joined.win === 164 && joined.conflicts === 0 && scanTransfers.size === 115,
     "K0863 transfer union mismatch");

const residualRows = data.resolve4.receipts.residual_row_hex.slice().sort();
need(residualRows.length === 86, "residual row count must be 86");
const residualSet = new Set(residualRows);
const candidates = new Map();
const perRow = [];
for (const rowHex of residualRows) {
  const mask = BigInt("0x" + rowHex);
  const bits = stones(mask);
  need(bits.length === 6 && safe(bits), "unsafe or non-six-stone residual row " + rowHex);
  const additions = legalAdds(bits);
  perRow.push({ row: rowHex, legal_extensions: additions.length });
  for (const q of additions) {
    const root = d4Canon(mask | (1n << BigInt(q)));
    if (!candidates.has(root)) candidates.set(root, { mask: BigInt("0x" + root), covered: new Set(), sources: new Set() });
    candidates.get(root).sources.add(rowHex);
  }
}
for (const [root, item] of candidates) {
  const bits = stones(item.mask);
  need(bits.length === 7 && safe(bits), "unsafe seven-stone candidate " + root);
  for (const p of bits) {
    const parent = d4Canon(item.mask ^ (1n << BigInt(p)));
    if (residualSet.has(parent)) item.covered.add(parent);
  }
  need(item.covered.size >= 1 && item.covered.size <= 2, "candidate span outside 1..2: " + root);
}
const coverage = { one_row: 0, two_rows: 0 };
const candidateStatus = { refuted_d10: 0, win7_d10: 0, not_in_pinned_join: 0 };
for (const [root, item] of candidates) {
  if (item.covered.size === 1) coverage.one_row++;
  else coverage.two_rows++;
  if (knownWin.has(root)) candidateStatus.win7_d10++;
  else if (knownRefuted.has(root)) candidateStatus.refuted_d10++;
  else candidateStatus.not_in_pinned_join++;
}
need(candidates.size === 5247 && coverage.one_row === 4153 && coverage.two_rows === 1094,
     "candidate census mismatch");
need(candidateStatus.refuted_d10 === 110 && candidateStatus.win7_d10 === 0 && candidateStatus.not_in_pinned_join === 5137,
     "candidate known-verdict classification mismatch");

const scanTargetSet = new Set(Object.keys(data.scan.targets).map(h => d4Canon(BigInt("0x" + h))));
const scanParentHits = new Map();
const scanParentForms = new Set();
for (const [root, item] of candidates) {
  for (const p of stones(item.mask)) {
    const parent = d4Canon(item.mask ^ (1n << BigInt(p)));
    if (scanTargetSet.has(parent)) {
      scanParentHits.set(root, (scanParentHits.get(root) || 0) + 1);
      scanParentForms.add(parent);
    }
  }
}
need(scanParentHits.size === 363 && scanParentForms.size === 92, "K0863 cache-parent intersection mismatch");

const pool = new Set();
for (const x of data.audit.derived.witness_pairs) pool.add(d4Canon(BigInt("0x" + x.root)));
for (const item of data.joint.derived.joint_results)
  for (const root of item.witness_roots) pool.add(d4Canon(BigInt("0x" + root)));
need(pool.size === 117, "117-root pool reconstruction mismatch");
const poolOverlap = [...candidates.keys()].filter(root => pool.has(root));
need(poolOverlap.length === 98, "old 117-root pool overlap mismatch");
const poolStatus = { refuted_d10: 0, win7_d10: 0, not_in_pinned_join: 0 };
for (const root of pool) {
  if (knownWin.has(root)) poolStatus.win7_d10++;
  else if (knownRefuted.has(root)) poolStatus.refuted_d10++;
  else poolStatus.not_in_pinned_join++;
}
need(poolStatus.refuted_d10 === 109 && poolStatus.win7_d10 === 8 && poolStatus.not_in_pinned_join === 0,
     "117-root pool verdict join mismatch");

const selectedRoots = [
"00000000000000003800000008001081",
"00000000000000003800000008001120",
"00000000000000003800000008011200",
"00000000000000003800000008005800",
"00000000010000809042000080000000",
"00000000000000003800000008002140",
"0000000000000000380000000a080008",
"00000000000000003800000908001000",
"00000000000000003800200088001000",
"00000000000080003800000048000100",
"00000000000000003800000209040000",
"00000000010000809002000040080000",
"00000000020080801202000000100000",
"00000000000000043800080009000000",
"00000000000000083800040048000000",
"00000000000000043840000008080000",
"00000000000000083800200008100000",
"00000000000000801202000001008100",
"00000000020010003800000008001000",
"00000000000000103800000009080000",
"00000000000000801202010000101000",
"00000000000000801202000000800500",
"00000000000000801202000000880200",
"00000000000000801202000000940000",
"00000000000000801202000001040200",
"00000000000000801202000001080400",
"00000000000000801202020020001000",
"00000000001020003800000048000000",
"00000000000000801202040000801000",
"00000000000000801222080000001000",
"00000000000000889002400000100000",
"00000000020000801212000001000000",
"00000000000000a09002200080000000",
"00000000000000821082000000000101",
"00000000000000821082000000000048",
"00000008000000821082000000100000",
"00000000000000821082040200000000",
"00000000000000821092200000000000",
"00000000000000a21086000000000000",
"00000000000020889002000080000000",
"00000000000040909002000000100000",
"00000008010000003800000008100000",
"00000010000000801202000100000400"
];
need(selectedRoots.length === 43, "selected root count");
const coveredBy = new Map();
const selected = [];
for (const root of selectedRoots) {
  const item = candidates.get(root);
  need(item, "selected root absent from exhaustive candidate universe: " + root);
  need(item.covered.size === 2, "selected root must cover exactly two residual rows: " + root);
  need(!knownRefuted.has(root) && !knownWin.has(root), "selected root already has a joined verdict: " + root);
  need(!scanTransfers.has(root), "selected root overlaps K0863 transfer cache: " + root);
  need(!pool.has(root), "selected root overlaps the old 117-root pool: " + root);
  for (const row of item.covered) {
    need(!coveredBy.has(row), "duplicate residual row coverage: " + row);
    coveredBy.set(row, root);
  }
  const bits = stones(item.mask);
  const parentHits = [];
  for (const p of bits) {
    const parent = d4Canon(item.mask ^ (1n << BigInt(p)));
    if (scanTargetSet.has(parent)) parentHits.push(parent);
  }
  selected.push({
    root,
    covered_rows: [...item.covered].sort(),
    legal_next_moves: legalAdds(bits).length,
    scan_parent_hits: parentHits
  });
}
need(coveredBy.size === 86, "selected 43 roots do not cover all 86 rows");
const selectedMobility = selected.map(x => x.legal_next_moves).sort((a, b) => a - b);
const selectedScanHits = selected.filter(x => x.scan_parent_hits.length > 0);
need(selectedScanHits.length === 1, "selected root cache-parent hit count");
need(selectedScanHits[0].root === SOLE_SCAN_ROOT &&
     selectedScanHits[0].scan_parent_hits.length === 1 &&
     selectedScanHits[0].scan_parent_hits[0] === SOLE_SCAN_PARENT,
     "sole selected cache-parent hit mismatch");
const soleTarget = data.scan.targets[SOLE_SCAN_PARENT];
const transferredBits = (soleTarget.transferred?.["REFUTED-D10"] || []).map(x => x.bit).sort((a, b) => a - b);
need(soleTarget.engine["REFUTED-D10"] === 0 &&
     soleTarget.engine["WIN7-D10"] === 0 &&
     soleTarget.engine["UNKNOWN-CAPPED"] === 0 &&
     soleTarget.legal_count === 69 &&
     soleTarget.open === 66 &&
     JSON.stringify(transferredBits) === JSON.stringify([55, 65, 109]),
     "sole target parent cache accounting mismatch");
need(!scanTransfers.has(SOLE_SCAN_ROOT), "sole selected root is in transfer cache");
const soleTargetBits = [];
for (let q = 0; q < 121; q++) {
  const parentMask = BigInt("0x" + SOLE_SCAN_PARENT);
  if ((parentMask >> BigInt(q)) & 1n) continue;
  if (d4Canon(parentMask | (1n << BigInt(q))) === SOLE_SCAN_ROOT) soleTargetBits.push(q);
}
need(JSON.stringify(soleTargetBits) === JSON.stringify([73]), "sole target orientation bit mismatch");

const selectedRows = [...coveredBy.keys()].sort();
const lowerBound = Math.ceil(residualRows.length / 2);
need(lowerBound === 43, "minimum-cover lower bound mismatch");
need(selectedRoots.length === lowerBound, "selected cover does not attain lower bound");
const record = {
  schema: "n11-residual-86-minimum-candidate-cover-20261120-v1",
  date: "2026-11-20",
  status: "minimum candidate cover; no root verdict or receipt fold",
  source_main_head: SOURCE_MAIN_HEAD,
  input_pins: Object.fromEntries(Object.entries(PIN).map(([name, [relative, sha]]) => [name, { path: relative, git_blob_sha1: sha }])),
  residual: {
    rows: residualRows.length,
    legal_extensions: perRow.reduce((s, x) => s + x.legal_extensions, 0),
    min_legal_extensions_per_row: Math.min(...perRow.map(x => x.legal_extensions)),
    max_legal_extensions_per_row: Math.max(...perRow.map(x => x.legal_extensions)),
  },
  candidate_universe: {
    d4_canonical_roots: candidates.size,
    coverage_span_distribution: coverage,
    maximum_residual_rows_covered_by_one_root: 2,
    candidate_verdict_join: candidateStatus,
    candidate_verdict_join_note: "not_in_pinned_join is not a game-theoretic UNKNOWN; selected roots are separately excluded from the full K0863 cache parent universe and its transfers"
  },
  known_verdict_join: {
    explicit_sources_before_k0863_transfers: baseJoin,
    after_all_k0863_transfers: joined,
    conflicts: 0,
    note: "REFUTED-D10 and WIN7-D10 are individual seven-stone-root depth-10 verdicts, not S6/S5 or empty-board verdicts."
  },
  old_117_root_pool: {
    roots: pool.size,
    overlap_with_new_candidate_universe: poolOverlap.length,
    verdicts: poolStatus
  },
  k0863_cache_exclusion: {
    engine_verdicts: data.scan.engine_map.determined_bits,
    engine_refuted_d10: data.scan.engine_map["REFUTED-D10"],
    engine_win7_d10: data.scan.engine_map["WIN7-D10"],
    engine_unknown_capped: data.scan.engine_map["UNKNOWN-CAPPED"],
    child_universe: Object.keys(data.scan.targets).length,
    transfer_roots: scanTransfers.size,
    candidate_roots_with_any_parent_in_child_universe: scanParentHits.size,
    distinct_parent_orbits_hit: scanParentForms.size,
    selected_roots_with_any_parent_in_child_universe: selectedScanHits.length,
    selected_roots_overlapping_transfer_cache: 0,
    sole_parent_hit: {
      selected_root: SOLE_SCAN_ROOT,
      child: SOLE_SCAN_PARENT,
      target_orientation_add_bit: 73,
      engine_counts: soleTarget.engine,
      transferred_refuted_bits: transferredBits,
      open_count: soleTarget.open,
      explanation: "The sole matched parent has zero engine verdicts; bit 73 is open and is not one of the three transferred REFUTED-D10 bits."
    }
  },
  minimum_cover: {
    rows: 86,
    maximum_span: 2,
    lower_bound: lowerBound,
    selected_roots: selected.length,
    covered_rows: selectedRows.length,
    exact_cover: true,
    selected_roots: selected
  },
  selected_root_mobility: {
    min: selectedMobility[0],
    median: selectedMobility[Math.floor(selectedMobility.length / 2)],
    max: selectedMobility[selectedMobility.length - 1],
    sum: selectedMobility.reduce((a, b) => a + b, 0),
    interpretation: "legal next-move count only; not a DFPN node/time estimate"
  },
  independent_verification: {
    determinant_methods: ["BigInt 3x3 cofactor expansion", "BigInt 4x4 Bareiss elimination"],
    every determinant call compared across both methods: true,
    all_residual_rows_safe: true,
    all_candidate_roots_safe: true,
    all_selected_roots_rederived: true,
    selected_cover_rechecked: true
  },
  checks: [
    "all source Git blob SHA-1 pins match",
    "base known-verdict join is 340 REFUTED-D10 / 164 WIN7-D10 / zero conflicts",
    "all 115 K0863 REFUTED-D10 transfers are merged without WIN/LOSS conflict",
    "86 residual rows have 6 stones and are safe",
    "6,341 legal one-stone extensions produce 5,247 D4 roots",
    "every candidate root covers exactly one or two residual rows",
    "43 selected roots cover all 86 residual rows exactly once",
    "43 attains the lower bound ceil(86/2)",
    "selected roots are absent from all joined verdict sources and all 115 transfers",
    "selected roots are excluded from the 8,964-engine-verdict K0863 cache by complete parent-orbit membership"
  ],
  interpretation_guard: {
    "not_a_win_certificate": true,
    "not_a_loss_certificate": true,
    "not_a_receipt_fold": true,
    "standard_11x11_empty_board": "UNKNOWN",
    "two_stone_roots_49_60_and_59_60": "UNKNOWN",
    "s2_59_60": "UNKNOWN",
    "class_1_2_4": "UNKNOWN"
  },
  next_step: "Probe the 43 selected seven-stone roots with the existing bounded DFPN runner, reusing shared cache and both AND orders. On REFUTED-D10, substitute another candidate root covering the same pair; on WIN7-D10, extract and independently verify a certificate before folding any S6 receipt."
};
process.stdout.write(JSON.stringify(record, null, 2) + "\n");
