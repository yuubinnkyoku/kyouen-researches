#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";

const ROOT = process.cwd();
const SCRIPT_FILE = fileURLToPath(import.meta.url);
const SCRIPT_PATH = path.relative(ROOT, SCRIPT_FILE).replaceAll("\\", "/");
const SCAN_PATH = "research/experiments/n11-class2-lane-sterile-unclosability-20261116/output/theorem-applicability-scan-20261116.json";
const RESIDUAL_PATH = "research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/five-parent-residual-49-cover-20261119.json";
const SCAN_SOURCE_PATH = "research/experiments/n11-class2-lane-sterile-unclosability-20261116/theorem_applicability_scan_20261116.py";
const CONVENTION_PATH = "research/knowledge/items/K0868-n11-s6-s7-sweep-candidate-convention.md";
const OUTPUT_PATH = "research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-cache-exclusion-mobility-20261119.json";

const PIN = {
  scan: "24f214e6a9dd721ef95ac97d6b84cf34af33b14b",
  residual: "a8eaf00bd6494eda50a68e7d06498bed833a7688",
  scanSource: "44f188fbff846754de0ea4fe4da1c5f771a6805d",
  convention: "b097210d0b49d7cf014cc6a554298b1e49e83384"
};
const SOURCE_MAIN_HEAD = "317f6af8c9810941bda38b5cf355a8f27ce3aa65";

function need(condition, message) {
  if (!condition) throw new Error(message);
}
function gitBlobSha1(text) {
  const bytes = Buffer.from(text, "utf8");
  const header = Buffer.from("blob " + bytes.length + "\0", "utf8");
  return createHash("sha1").update(Buffer.concat([header, bytes])).digest("hex");
}
function readPinned(relativePath, expectedSha) {
  const text = fs.readFileSync(path.join(ROOT, relativePath), "utf8");
  const actual = gitBlobSha1(text);
  need(actual === expectedSha, relativePath + " Git blob SHA mismatch: " + actual);
  return text;
}
function stones(mask) {
  const out = [];
  for (let i = 0; i < 121; i++) {
    if ((mask >> BigInt(i)) & 1n) out.push(i);
  }
  return out;
}
function hex(mask) {
  return mask.toString(16).padStart(32, "0");
}
function transform(mask, swap, flipX, flipY) {
  let out = 0n;
  for (const i of stones(mask)) {
    const x = i % 11;
    const y = Math.floor(i / 11);
    let a = swap ? y : x;
    let b = swap ? x : y;
    if (flipX) a = 10 - a;
    if (flipY) b = 10 - b;
    out |= 1n << BigInt(a + 11 * b);
  }
  return out;
}
function d4Canon(mask) {
  let best = null;
  for (let swap = 0; swap < 2; swap++) {
    for (let flipX = 0; flipX < 2; flipX++) {
      for (let flipY = 0; flipY < 2; flipY++) {
        const candidate = transform(mask, swap, flipX, flipY);
        if (best === null || candidate < best) best = candidate;
      }
    }
  }
  return hex(best);
}
function d4OrbitSize(mask) {
  const variants = new Set();
  for (let swap = 0; swap < 2; swap++) {
    for (let flipX = 0; flipX < 2; flipX++) {
      for (let flipY = 0; flipY < 2; flipY++) {
        variants.add(hex(transform(mask, swap, flipX, flipY)));
      }
    }
  }
  return variants.size;
}
function permutations(items) {
  const out = [];
  function visit(a, k) {
    if (k === a.length) {
      let inversions = 0;
      for (let i = 0; i < a.length; i++) {
        for (let j = i + 1; j < a.length; j++) {
          if (a[i] > a[j]) inversions++;
        }
      }
      out.push({ p: a.slice(), sign: inversions % 2 ? -1n : 1n });
      return;
    }
    for (let i = k; i < a.length; i++) {
      [a[k], a[i]] = [a[i], a[k]];
      visit(a, k + 1);
      [a[k], a[i]] = [a[i], a[k]];
    }
  }
  visit(items.slice(), 0);
  return out;
}
const PERMS4 = permutations([0, 1, 2, 3]);
function matrixRows(indices) {
  return indices.map(i => {
    const x = BigInt(i % 11);
    const y = BigInt(Math.floor(i / 11));
    return [x * x + y * y, x, y, 1n];
  });
}
function detBareiss(indices) {
  const a = matrixRows(indices).map(row => row.slice());
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
        a[i][j] = (a[i][j] * pivot - a[i][k] * a[k][j]) / previousPivot;
      }
    }
    for (let i = k + 1; i < 4; i++) a[i][k] = 0n;
    previousPivot = pivot;
  }
  return sign * a[3][3];
}
function detLeibniz(indices) {
  const a = matrixRows(indices);
  let sum = 0n;
  for (const item of PERMS4) {
    sum += item.sign *
      a[0][item.p[0]] * a[1][item.p[1]] *
      a[2][item.p[2]] * a[3][item.p[3]];
  }
  return sum;
}
function chooseTuples(values, size) {
  const out = [];
  function visit(start, chosen) {
    if (chosen.length === size) {
      out.push(chosen.slice());
      return;
    }
    for (let i = start; i <= values.length - (size - chosen.length); i++) {
      chosen.push(values[i]);
      visit(i + 1, chosen);
      chosen.pop();
    }
  }
  visit(0, []);
  return out;
}

const scanText = readPinned(SCAN_PATH, PIN.scan);
const residualText = readPinned(RESIDUAL_PATH, PIN.residual);
readPinned(SCAN_SOURCE_PATH, PIN.scanSource);
readPinned(CONVENTION_PATH, PIN.convention);
const scan = JSON.parse(scanText);
const residual = JSON.parse(residualText);
const checks = [];
function check(name, pass, detail = null) {
  checks.push({ name, pass: !!pass, detail });
  need(!!pass, "check failed: " + name);
}

check("scan-schema", scan.schema === "n11-k0863-theorem-applicability-scan-20261116-v1");
check("scan-all-published-checks-pass", scan.checks.length === 8 && scan.checks.every(x => x.pass));
check("scan-engine-count", scan.engine_map.determined_bits === 8964);
check("scan-engine-conflict-free", scan.engine_map.source_conflicts.length === 0);
check("scan-verdict-breakdown",
  scan.engine_map["REFUTED-D10"] === 8305 &&
  scan.engine_map["WIN7-D10"] === 659 &&
  scan.engine_map["UNKNOWN-CAPPED"] === 0);
check("scan-transfer-breakdown",
  scan.transfers.total === 115 &&
  scan.transfers["REFUTED-D10"] === 115 &&
  scan.transfers["WIN7-D10"] === 0);
check("scan-raw-input-accounting",
  scan.inputs.raw_files === 1064 &&
  scan.inputs.raw_files_resolved === 1064 &&
  scan.inputs.raw_unresolved === 0);
check("scan-child-universe", Object.keys(scan.targets).length === 133);
check("residual-schema",
  residual.schema === "n11-five-parent-receipt-aware-residual-cover-20261119-v1");
check("residual-cover-size",
  residual.receipts.residual_rows === 97 &&
  residual.witness.length === 49 &&
  residual.matching.minimum_cover_lower_bound === 49);

const targetByCanonicalChild = new Map();
for (const [child, meta] of Object.entries(scan.targets)) {
  const childMask = BigInt("0x" + child);
  need(stones(childMask).length === 6, "scan target is not a six-stone child: " + child);
  const key = d4Canon(childMask);
  if (!targetByCanonicalChild.has(key)) targetByCanonicalChild.set(key, []);
  targetByCanonicalChild.get(key).push({ child, meta });
}

const cacheRecords = [];
for (const witness of residual.witness) {
  const rootMask = BigInt("0x" + witness.root);
  const rootCanonical = d4Canon(rootMask);
  need(rootCanonical === witness.root, "witness root is not D4-canonical: " + witness.root);
  const rootStones = stones(rootMask);
  need(rootStones.length === 7, "witness root is not seven stones: " + witness.root);
  const matches = [];
  for (const removedBit of rootStones) {
    const childMask = rootMask ^ (1n << BigInt(removedBit));
    const childCanonical = d4Canon(childMask);
    for (const hit of (targetByCanonicalChild.get(childCanonical) || [])) {
      const targetMask = BigInt("0x" + hit.child);
      const addBits = [];
      for (let bit = 0; bit < 121; bit++) {
        if (d4Canon(targetMask | (1n << BigInt(bit))) === rootCanonical) {
          addBits.push(bit);
        }
      }
      if (addBits.length) {
        const engineCount = Object.values(hit.meta.engine).reduce((a, b) => a + b, 0);
        const refutedTransfers = hit.meta.transferred["REFUTED-D10"];
        const winTransfers = hit.meta.transferred["WIN7-D10"];
        const transferCount = refutedTransfers.length + winTransfers.length;
        const accountingMatches =
          hit.meta.legal_count === hit.meta.open + engineCount + transferCount;
        const candidateBits = addBits.map(bit => {
          const transfer = refutedTransfers.find(x => x.bit === bit) ||
                           winTransfers.find(x => x.bit === bit) || null;
          let status = "not-resolved-by-this-summary";
          if (engineCount === 0 && transfer === null && accountingMatches) {
            status = "open";
          } else if (transfer !== null) {
            status = refutedTransfers.some(x => x.bit === bit) ? "REFUTED-D10" : "WIN7-D10";
          } else if (engineCount > 0) {
            status = "engine-bucket-nonempty-needs-bit-level-lookup";
          }
          return { bit, status };
        });
        matches.push({
          child: hit.child,
          removed_bit_from_canonical_root: removedBit,
          add_bits_in_target_orientation: addBits,
          engine_counts: hit.meta.engine,
          transferred_refuted_bits: refutedTransfers.map(x => x.bit).sort((a, b) => a - b),
          transferred_win_bits: winTransfers.map(x => x.bit).sort((a, b) => a - b),
          legal_count: hit.meta.legal_count,
          open_count: hit.meta.open,
          accounting_matches: accountingMatches,
          candidate_bits: candidateBits
        });
      }
    }
  }
  const uniqueMatches = [];
  const seen = new Set();
  for (const m of matches) {
    const key = m.child + ":" + m.add_bits_in_target_orientation.join(",");
    if (!seen.has(key)) {
      seen.add(key);
      uniqueMatches.push(m);
    }
  }
  let status;
  if (uniqueMatches.length === 0) {
    status = "no-child-orbit-in-published-index";
  } else if (uniqueMatches.every(m =>
    m.engine_counts["REFUTED-D10"] + m.engine_counts["WIN7-D10"] +
      m.engine_counts["UNKNOWN-CAPPED"] === 0 &&
    m.candidate_bits.every(x => x.status === "open"))) {
    status = "candidate-bit-open-in-published-index";
  } else {
    status = "requires-further-bit-level-classification";
  }
  cacheRecords.push({
    root: witness.root,
    covered_rows: witness.rows.length,
    status,
    matches: uniqueMatches
  });
}

const noChild = cacheRecords.filter(x => x.status === "no-child-orbit-in-published-index").length;
const openMatch = cacheRecords.filter(x => x.status === "candidate-bit-open-in-published-index").length;
const unknownCount = noChild + openMatch;
check("all-49-cache-nonmembership",
  cacheRecords.length === 49 && noChild === 48 && openMatch === 1 && unknownCount === 49);
const soleMatch = cacheRecords.find(x => x.matches.length > 0);
check("sole-parent-match-is-open-bit74",
  soleMatch.root === "00000000000000909002200080000000" &&
  soleMatch.matches.length === 1 &&
  soleMatch.matches[0].child === "00000000000000801222000000800000" &&
  soleMatch.matches[0].add_bits_in_target_orientation.length === 1 &&
  soleMatch.matches[0].add_bits_in_target_orientation[0] === 74 &&
  soleMatch.matches[0].engine_counts["REFUTED-D10"] === 0 &&
  soleMatch.matches[0].engine_counts["WIN7-D10"] === 0 &&
  soleMatch.matches[0].engine_counts["UNKNOWN-CAPPED"] === 0 &&
  soleMatch.matches[0].transferred_refuted_bits.join(",") === "55,65,109" &&
  soleMatch.matches[0].transferred_win_bits.length === 0 &&
  soleMatch.matches[0].candidate_bits[0].status === "open" &&
  soleMatch.matches[0].open_count === 66 &&
  soleMatch.matches[0].legal_count === 69);

let rootSafetyCases = 0;
let candidateDeterminantCases = 0;
const mobility = [];
for (const witness of residual.witness) {
  const mask = BigInt("0x" + witness.root);
  const occupied = stones(mask);
  const triples = chooseTuples(occupied, 3);
  const quadruples = chooseTuples(occupied, 4);
  for (const quad of quadruples) {
    const a = detBareiss(quad);
    const b = detLeibniz(quad);
    rootSafetyCases++;
    need(a === b && a !== 0n, "root safety determinant failure: " + witness.root);
  }
  const legalBits = [];
  for (let point = 0; point < 121; point++) {
    if ((mask >> BigInt(point)) & 1n) continue;
    let legal = true;
    for (const triple of triples) {
      const four = [...triple, point];
      const a = detBareiss(four);
      const b = detLeibniz(four);
      candidateDeterminantCases++;
      need(a === b, "Bareiss/Leibniz disagreement at " + witness.root + " + " + point);
      if (a === 0n) {
        legal = false;
        break;
      }
    }
    if (legal) legalBits.push(point);
  }
  const rootOrbitSize = d4OrbitSize(mask);
  const successorClasses = new Set(
    legalBits.map(bit => d4Canon(mask | (1n << BigInt(bit))))
  );
  mobility.push({
    root: witness.root,
    covered_rows: witness.rows.length,
    legal_next_moves: legalBits.length,
    legal_bits: legalBits,
    root_d4_orbit_size: rootOrbitSize,
    distinct_d4_successor_classes: successorClasses.size
  });
}
mobility.sort((a, b) =>
  a.legal_next_moves - b.legal_next_moves ||
  b.covered_rows - a.covered_rows ||
  a.root.localeCompare(b.root)
);
const values = mobility.map(x => x.legal_next_moves).sort((a, b) => a - b);
const histogram = {};
for (const value of values) histogram[String(value)] = (histogram[String(value)] || 0) + 1;
const mean = values.reduce((a, b) => a + b, 0) / values.length;
const median = values[Math.floor(values.length / 2)];
const orbitSizes = [...new Set(mobility.map(x => x.root_d4_orbit_size))].sort();
check("all-49-roots-independently-safe",
  mobility.length === 49 && rootSafetyCases === 49 * 35);
check("exact-mobility-determinant-crosscheck",
  candidateDeterminantCases > 0 &&
  mobility.every(x => x.distinct_d4_successor_classes === x.legal_next_moves));
check("no-root-stabilizer",
  orbitSizes.length === 1 && orbitSizes[0] === 8);
check("mobility-range-and-summary",
  values[0] === 47 && values[values.length - 1] === 77 &&
  median === 62 && Math.abs(mean - 60.91836734693877) < 1e-12);

const finalRoots = mobility.map(m => {
  const cache = cacheRecords.find(x => x.root === m.root);
  return { ...m, cache_status: cache.status, cache_matches: cache.matches };
});
const result = {
  schema: "n11-five-parent-49-root-cache-exclusion-mobility-20261119-v1",
  date: "2026-11-19",
  status: "all-49-unresolved-in-published-verdict-index",
  source_main_head: SOURCE_MAIN_HEAD,
  prior_residual_audit_source_main_head: residual.source_main_head,
  input_pins: {
    scan: { path: SCAN_PATH, git_blob_sha1: PIN.scan },
    residual_cover: { path: RESIDUAL_PATH, git_blob_sha1: PIN.residual },
    scan_generator: { path: SCAN_SOURCE_PATH, git_blob_sha1: PIN.scanSource },
    sweep_candidate_convention: { path: CONVENTION_PATH, git_blob_sha1: PIN.convention }
  },
  reproduction_script: {
    path: SCRIPT_PATH,
    git_blob_sha1: gitBlobSha1(fs.readFileSync(SCRIPT_FILE, "utf8"))
  },
  output_path: OUTPUT_PATH,
  cache_exclusion: {
    method: "For any seven-stone root X, every six-stone parent capable of producing X is X with one of its seven stones removed. Compare all seven parent D4 orbits against the complete 133-child universe of the pinned K0863 scan; then inspect the exact candidate bit in the matched child summary.",
    scan_engine_verdicts: scan.engine_map.determined_bits,
    scan_engine_breakdown: {
      refuted_d10: scan.engine_map["REFUTED-D10"],
      win7_d10: scan.engine_map["WIN7-D10"],
      unknown_capped: scan.engine_map["UNKNOWN-CAPPED"]
    },
    scan_transfers: {
      total: scan.transfers.total,
      refuted_d10: scan.transfers["REFUTED-D10"],
      win7_d10: scan.transfers["WIN7-D10"]
    },
    scan_child_universe: Object.keys(scan.targets).length,
    scan_input_accounting: {
      claims: scan.inputs.claims,
      sweeps: scan.inputs.sweeps,
      audits: scan.inputs.audits,
      raw_files: scan.inputs.raw_files,
      raw_files_resolved: scan.inputs.raw_files_resolved,
      raw_unresolved: scan.inputs.raw_unresolved
    },
    candidate_roots: cacheRecords.length,
    roots_without_any_parent_orbit_in_scan: noChild,
    roots_with_parent_orbit_match: openMatch,
    roots_with_known_engine_or_transfer_verdict: 0,
    roots_still_unknown_in_published_index: unknownCount,
    sole_parent_match: soleMatch
  },
  mobility: {
    rule: "A next point is legal exactly when det4(a,b,c,p) != 0 for every triple of existing stones; det4 is the integer determinant of rows [x^2+y^2,x,y,1], including collinear degeneracies.",
    independent_methods: ["BigInt Bareiss elimination", "BigInt Leibniz expansion"],
    root_safety_quadruple_cases: rootSafetyCases,
    candidate_quadruple_cases: candidateDeterminantCases,
    determinant_method_evaluations: 2 * (rootSafetyCases + candidateDeterminantCases),
    all_determinants_agree: true,
    minimum_legal_next_moves: values[0],
    maximum_legal_next_moves: values[values.length - 1],
    mean_legal_next_moves: Number(mean.toFixed(6)),
    median_legal_next_moves: median,
    histogram,
    root_d4_orbit_sizes: orbitSizes,
    all_roots_have_trivial_d4_stabilizer: orbitSizes.length === 1 && orbitSizes[0] === 8,
    all_legal_successors_are_d4_distinct: mobility.every(x =>
      x.distinct_d4_successor_classes === x.legal_next_moves),
    priority_order: finalRoots
  },
  checks,
  check_count: checks.length,
  all_pass: checks.every(x => x.pass),
  interpretation_guard: [
    "The 49 roots are candidate seven-stone positions, not WIN7-D10 certificates.",
    "The cache exclusion is a complete parent-side nonmembership proof against the pinned 8,964-verdict/115-transfer scan universe; it does not reread all 1,064 raw files in this run.",
    "Legal-next-move count is a structural branching measure, not measured DFPN nodes, runtime, proof cost, or a game-theoretic verdict.",
    "No new WIN/LOSS verdict or receipt was created. REFUTED-D10 is not a LOSS proof.",
    "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
  ]
};

need(result.all_pass, "one or more checks failed");
fs.mkdirSync(path.dirname(path.join(ROOT, OUTPUT_PATH)), { recursive: true });
fs.writeFileSync(path.join(ROOT, OUTPUT_PATH), JSON.stringify(result, null, 2) + "\n", "utf8");
console.log(JSON.stringify({
  all_pass: result.all_pass,
  check_count: result.check_count,
  cache_exclusion: {
    roots: result.cache_exclusion.candidate_roots,
    no_parent_orbit: result.cache_exclusion.roots_without_any_parent_orbit_in_scan,
    one_open_parent_match: result.cache_exclusion.roots_with_parent_orbit_match,
    still_unknown: result.cache_exclusion.roots_still_unknown_in_published_index
  },
  mobility: {
    min: result.mobility.minimum_legal_next_moves,
    max: result.mobility.maximum_legal_next_moves,
    mean: result.mobility.mean_legal_next_moves,
    median: result.mobility.median_legal_next_moves,
    lowest_root: result.mobility.priority_order[0].root,
    lowest_root_moves: result.mobility.priority_order[0].legal_next_moves
  },
  output: OUTPUT_PATH
}, null, 2));
