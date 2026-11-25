#!/usr/bin/env node
/**
 * Independent structural preread for rank-31 of the cost-16 parent.
 * Reads three pinned JSON files; does not call the Pm engine or infer game verdicts.
 * Run from repository root: node research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/cost16_survival_k31_preread_20261118.mjs
 */
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const EXP = "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118";
const INPUTS = {
  aggregate: { path: path.join(EXP, "output/cost16-b-phase-groups-20261118.json"), sha: "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87" },
  k29: { path: path.join(EXP, "output/cost16-survival-k29-20261118.json"), sha: "795665316c300a186979bafd2817b6961de2de60" },
  k30: { path: path.join(EXP, "output/cost16-survival-k30-20261118.json"), sha: "9c24e7a30ad213d3b7675e620ec606b00f73a330" }
};
const OUT = path.join(EXP, "output/cost16-survival-k31-preread-20261118.json");

function gitBlobSha1(bytes) {
  const header = Buffer.from("blob " + bytes.length + "\0");
  return crypto.createHash("sha1").update(Buffer.concat([header, bytes])).digest("hex");
}
function loadPinned(spec) {
  const bytes = fs.readFileSync(spec.path);
  const actual = gitBlobSha1(bytes);
  if (actual !== spec.sha) throw new Error(spec.path + ": blob SHA-1 " + actual + " != " + spec.sha);
  return JSON.parse(bytes.toString("utf8"));
}
function* combinations(n, k, start = 0, prefix = []) {
  if (k === 0) { yield prefix; return; }
  for (let i = start; i <= n - k; i++) yield* combinations(n, k - 1, i + 1, [...prefix, i]);
}
function classifyMap(rows, ids) {
  const counts = new Map();
  for (const i of ids) for (const r of rows[i]) counts.set(r, (counts.get(r) || 0) + 1);
  let max = 0, doubles = 0, doubleRow = null;
  for (const [r, n] of counts) {
    if (n > max) max = n;
    if (n === 2) { doubles++; doubleRow = r; }
  }
  if (max >= 3 || doubles >= 2) return { kind: "zero", doubleRow: null };
  if (doubles === 1) return { kind: "b_only", doubleRow };
  return { kind: "disjoint", doubleRow: null };
}
function makeRowMasks(rows, rowCount) {
  const masks = Array(rowCount).fill(0n);
  for (let i = 0; i < rows.length; i++) for (const r of rows[i]) masks[r] |= 1n << BigInt(i);
  return masks;
}
function popcount(x) {
  let n = 0;
  while (x) { x &= x - 1n; n++; }
  return n;
}
function classifyMask(rowMasks, ids) {
  let selected = 0n;
  for (const i of ids) selected |= 1n << BigInt(i);
  let max = 0, doubles = 0, doubleRow = null;
  for (let r = 0; r < rowMasks.length; r++) {
    const n = popcount(rowMasks[r] & selected);
    if (n > max) max = n;
    if (n === 2) { doubles++; doubleRow = r; }
  }
  if (max >= 3 || doubles >= 2) return { kind: "zero", doubleRow: null };
  if (doubles === 1) return { kind: "b_only", doubleRow };
  return { kind: "disjoint", doubleRow: null };
}
function binom(n, k) {
  let v = 1;
  for (let i = 1; i <= k; i++) v = v * (n - k + i) / i;
  return Math.round(v);
}
function classCounts(records) {
  const c = { b_only: 0, zero: 0, disjoint: 0 };
  for (const v of Object.values(records)) c[v.class]++;
  return c;
}
function newCensus(k, rows, rowMasks) {
  const idx = k - 1, result = {}, hist = {}, profiles = {}, disjointQuads = [];
  let compared = 0, mismatches = 0;
  for (const [size, name] of [[2, "pair"], [3, "triple"], [4, "quad"], [5, "quint"]]) {
    const counts = { b_only: 0, zero: 0, disjoint: 0 };
    for (const prior of combinations(idx, size - 1)) {
      const ids = [...prior, idx];
      const a = classifyMap(rows, ids), b = classifyMask(rowMasks, ids);
      compared++;
      if (a.kind !== b.kind || a.doubleRow !== b.doubleRow) mismatches++;
      counts[a.kind]++;
      if (name === "quint" && a.kind === "b_only") {
        const profile = { b_only: 0, zero: 0, disjoint: 0 };
        for (let drop = 0; drop < 5; drop++) profile[classifyMap(rows, ids.filter((_, j) => j !== drop)).kind]++;
        const key = profile.b_only + "/" + profile.disjoint + "/" + profile.zero;
        profiles[key] = (profiles[key] || 0) + 1;
        hist[String(a.doubleRow)] = (hist[String(a.doubleRow)] || 0) + 1;
      }
      if (name === "quad" && a.kind === "disjoint") {
        const union = [...new Set(ids.flatMap(i => rows[i]))].sort((x, y) => x - y);
        disjointQuads.push({ indices: ids, rows_union: union });
      }
    }
    counts.total = counts.b_only + counts.zero + counts.disjoint;
    counts.expected_total = binom(idx, size - 1);
    result[name] = counts;
  }
  return { result, hist, profiles, disjointQuads, compared, mismatches };
}
function fullCensus(n, size, rows, rowMasks) {
  const counts = { b_only: 0, zero: 0, disjoint: 0 }, hist = {};
  let compared = 0, mismatches = 0;
  for (const ids of combinations(n, size)) {
    const a = classifyMap(rows, ids), b = classifyMask(rowMasks, ids);
    compared++;
    if (a.kind !== b.kind || a.doubleRow !== b.doubleRow) mismatches++;
    counts[a.kind]++;
    if (a.kind === "b_only") hist[String(a.doubleRow)] = (hist[String(a.doubleRow)] || 0) + 1;
  }
  return { counts, total: compared, hist, compared, mismatches };
}
function sortedObject(o) {
  return Object.fromEntries(Object.entries(o).sort((a, b) => a[0].localeCompare(b[0])));
}
function same(a, b) { return JSON.stringify(sortedObject(a)) === JSON.stringify(sortedObject(b)); }

const aggregate = loadPinned(INPUTS.aggregate);
const k29 = loadPinned(INPUTS.k29);
const k30 = loadPinned(INPUTS.k30);
const top50 = aggregate.derived.top50_by_membership;
const top = top50.slice(0, 31);
const rows = top.map(x => x.rows_covered);
const rowMasks = makeRowMasks(rows, aggregate.derived.rows);
const memA = aggregate.derived.membership_A_part_pair_roots;
const memB = aggregate.derived.membership_B_part_pair_roots;
const c29 = newCensus(29, rows, rowMasks), f29t = fullCensus(29, 3, rows, rowMasks), f29q = fullCensus(29, 5, rows, rowMasks);
const c30 = newCensus(30, rows, rowMasks), f30t = fullCensus(30, 3, rows, rowMasks), f30q = fullCensus(30, 5, rows, rowMasks);
const c31 = newCensus(31, rows, rowMasks), f31t = fullCensus(31, 3, rows, rowMasks), f31q = fullCensus(31, 5, rows, rowMasks);
const priorHits31 = {};
for (const r of rows[30]) priorHits31[String(r)] = rows.slice(0, 30).filter(rs => rs.includes(r)).length;
const priorHitIndices31 = {};
for (const r of rows[30]) priorHitIndices31[String(r)] = rows.slice(0, 30).map((rs, i) => rs.includes(r) ? i : -1).filter(i => i >= 0);
const hist31Diff = {};
for (const [r, v] of Object.entries(f31q.hist)) {
  const d = v - (f30q.hist[r] || 0);
  if (d) hist31Diff[r] = d;
}
const k29PairCensus = k29.checks.filter(x => x.name === "pairs.new_census")[0].detail;
const k30PairCensus = k30.checks.filter(x => x.name === "pairs.new_census")[0].detail;
const k29TripleNew = classCounts(k29.values.new_triples);
const k30TripleNew = classCounts(k30.values.new_triples);
let sextet = { b_only: 0, zero: 0, disjoint: 0 }, sextetTotal = 0, sextetMismatch = 0;
for (const ids of combinations(31, 6)) {
  const a = classifyMap(rows, ids), b = classifyMask(rowMasks, ids);
  if (a.kind !== b.kind || a.doubleRow !== b.doubleRow) sextetMismatch++;
  sextet[a.kind]++;
  sextetTotal++;
}
const checks = [];
const add = (name, pass, detail = {}) => checks.push({ name, pass, detail });
add("top50_has_50_unique_pair_roots", top50.length === 50 && new Set(top50.map(x => x.root)).size === 50 && top50.every(x => x.rows_covered.length === 2));
add("k30_declares_pinned_k29_input", k30.inputs.survival_k29_json.git_blob_sha1 === INPUTS.k29.sha);
add("rank29_root_matches_published", top[28].root === k29.structure.rank29_root.root && same({ rows: rows[28] }, { rows: k29.structure.rank29_root.rows }) && rows[28].join(",") === "0,16");
add("rank29_new_census_matches_published", c29.result.pair.b_only === k29PairCensus.shared && c29.result.pair.disjoint === k29PairCensus.disjoint && c29.result.triple.b_only === k29TripleNew.b_only && c29.result.triple.zero === k29TripleNew.zero && c29.result.triple.disjoint === k29TripleNew.disjoint && c29.result.quad.b_only === k29.structure.new_quad_census.b_only && c29.result.quad.zero === k29.structure.new_quad_census.zero && c29.result.quad.disjoint === k29.structure.new_quad_census.disjoint && c29.result.quint.b_only === k29.structure.new_quint_census.b_only && c29.result.quint.zero === k29.structure.new_quint_census.zero && same(c29.hist, { "15": 283, "16": 172, "18": 1297, "19": 376 }), { pair: k29PairCensus, triple: k29TripleNew });
add("rank29_full_census_matches_published", f29t.counts.b_only === k29.structure.triple_census_k29.b_only && f29t.counts.zero === k29.structure.triple_census_k29.zero && f29t.counts.disjoint === k29.structure.triple_census_k29.disjoint && f29q.counts.b_only === k29.structure.quint_census_k29.b_only && f29q.counts.zero === k29.structure.quint_census_k29.zero && f29q.counts.disjoint === k29.structure.quint_census_k29.disjoint && same(f29q.hist, k29.structure.quint_b_only_double_rows));
add("rank29_two_classifiers_agree", c29.mismatches === 0 && f29t.mismatches === 0 && f29q.mismatches === 0);
add("rank30_root_matches_published", top[29].root === k30.structure.rank30_root.root && same({ rows: rows[29] }, { rows: k30.structure.rank30_root.rows }) && rows[29].join(",") === "14,19");
add("rank30_new_census_matches_published", c30.result.pair.b_only === k30PairCensus.shared && c30.result.pair.disjoint === k30PairCensus.disjoint && c30.result.triple.b_only === k30TripleNew.b_only && c30.result.triple.zero === k30TripleNew.zero && c30.result.triple.disjoint === k30TripleNew.disjoint && c30.result.quad.b_only === k30.structure.new_quad_census.b_only && c30.result.quad.zero === k30.structure.new_quad_census.zero && c30.result.quad.disjoint === k30.structure.new_quad_census.disjoint && c30.result.quint.b_only === k30.structure.new_quint_census.b_only && c30.result.quint.zero === k30.structure.new_quint_census.zero, { pair: k30PairCensus, triple: k30TripleNew });
add("rank30_full_census_matches_published", f30t.counts.b_only === k30.structure.triple_census_k30.b_only && f30t.counts.zero === k30.structure.triple_census_k30.zero && f30t.counts.disjoint === k30.structure.triple_census_k30.disjoint && f30q.counts.b_only === k30.structure.quint_census_k30.b_only && f30q.counts.zero === k30.structure.quint_census_k30.zero && f30q.counts.disjoint === k30.structure.quint_census_k30.disjoint && same(f30q.hist, k30.structure.quint_b_only_double_rows));
add("rank30_two_classifiers_agree", c30.mismatches === 0 && f30t.mismatches === 0 && f30q.mismatches === 0);
add("rank31_root_matches_top50", top[30].root === "00000000000040809002001000100000" && same({ rows: rows[30] }, { rows: [18, 26] }));
add("rank31_prior_hits_match", same(priorHits31, { "18": 15, "26": 0 }) && priorHitIndices31["18"].length === 15 && priorHitIndices31["26"].length === 0, { prior_hits: priorHits31, prior_hit_indices: { "18": priorHitIndices31["18"] } });
add("rank31_membership_split_identity", memA[top[30].root] + memB[top[30].root] === top[30].membership && top[30].membership === 120181378067473630, { membership: top[30].membership, a_part: memA[top[30].root], b_part: memB[top[30].root] });
add("rank31_new_pair_census", c31.result.pair.b_only === 15 && c31.result.pair.zero === 0 && c31.result.pair.disjoint === 15 && c31.result.pair.total === 30);
add("rank31_new_triple_census", c31.result.triple.b_only === 265 && c31.result.triple.zero === 115 && c31.result.triple.disjoint === 55 && c31.result.triple.total === 435);
add("rank31_new_quad_census", c31.result.quad.b_only === 986 && c31.result.quad.zero === 3025 && c31.result.quad.disjoint === 49 && c31.result.quad.total === 4060);
add("rank31_new_quint_census", c31.result.quint.b_only === 819 && c31.result.quint.zero === 26586 && c31.result.quint.disjoint === 0 && c31.result.quint.total === 27405);
add("rank31_two_classifiers_agree", c31.mismatches === 0 && f31t.mismatches === 0 && f31q.mismatches === 0);
add("rank31_full_census_totals", f31t.total === 4495 && f31q.total === 169911 && f31t.counts.b_only === 2717 && f31t.counts.zero === 930 && f31t.counts.disjoint === 848 && f31q.counts.b_only === 6787 && f31q.counts.zero === 163124 && f31q.counts.disjoint === 0);
add("rank31_full_minus_new_equals_rank30", f31t.counts.b_only - c31.result.triple.b_only === k30.structure.triple_census_k30.b_only && f31t.counts.zero - c31.result.triple.zero === k30.structure.triple_census_k30.zero && f31t.counts.disjoint - c31.result.triple.disjoint === k30.structure.triple_census_k30.disjoint && f31q.counts.b_only - c31.result.quint.b_only === k30.structure.quint_census_k30.b_only && f31q.counts.zero - c31.result.quint.zero === k30.structure.quint_census_k30.zero && f31q.counts.disjoint - c31.result.quint.disjoint === k30.structure.quint_census_k30.disjoint);
add("rank31_quint_histogram_increment_matches", same(hist31Diff, c31.hist) && same(c31.hist, { "15": 78, "16": 18, "18": 613, "19": 110 }));
add("rank31_disjoint_quad_unions_all_size8", c31.disjointQuads.length === 49 && c31.disjointQuads.every(q => q.rows_union.length === 8));
add("rank31_b_only_quint_profiles_partition", same(c31.profiles, { "3/2/0": 819 }));
add("rank31_sextet_census_all_zero", sextetTotal === 736281 && sextet.b_only === 0 && sextet.zero === 736281 && sextet.disjoint === 0 && sextetMismatch === 0);

const output = {
  schema: "n11-cost16-k31-preread-20261118-v1",
  date: "2026-11-18",
  lane: "n11 long lane (verification side)",
  title: "31-row cost-16 parent: rank-31 structural preread",
  inputs: {
    aggregate: { path: INPUTS.aggregate.path, git_blob_sha1: INPUTS.aggregate.sha },
    k29_result: { path: INPUTS.k29.path, git_blob_sha1: INPUTS.k29.sha },
    k30_result: { path: INPUTS.k30.path, git_blob_sha1: INPUTS.k30.sha },
    k30_publication: "result JSON commit f6a08dc5, record JSONL commit b3b5ee32"
  },
  scope: { parent: "00000000000000003800000008001000", rows: 31, minimum_cover_size: 16, top50_rank: 31, rank_convention: "top50_by_membership; 1-based rank 31" },
  rank30_regression: {
    new_census: c30.result,
    full_triples: f30t.counts,
    full_quints: f30q.counts,
    full_quint_double_row_histogram: f30q.hist,
    classifier_comparisons: c30.compared + f30t.compared + f30q.compared,
    mismatches: c30.mismatches + f30t.mismatches + f30q.mismatches
  },
  rank31: {
    root: top[30].root,
    rows: rows[30],
    membership: top[30].membership,
    a_part: memA[top[30].root],
    b_part: memB[top[30].root],
    prior_hits: priorHits31,
    prior_hit_indices: priorHitIndices31,
    note: "rank-31 (18,26) is a hub-band root: row 18 is covered by 15 prior top roots (indices 1,4,5,6,7,11,12,18,19,20,21,23,24,26,27), while row 26 receives its first-ever cover (no prior top-30 root contains it), so no new b_only/zero row-26 double-row family can appear before rank-32 adds another row-26 sharer",
    new_census: c31.result,
    new_quint_double_row_histogram: c31.hist,
    b_only_quint_four_subset_profiles: c31.profiles,
    disjoint_quad_count: c31.disjointQuads.length,
    disjoint_quad_union_sizes: [...new Set(c31.disjointQuads.map(q => q.rows_union.length))].sort((a, b) => a - b),
    full_triples: { counts: f31t.counts, total: f31t.total, double_row_histogram: f31t.hist, compared: f31t.compared, mismatches: f31t.mismatches },
    full_quints: { counts: f31q.counts, total: f31q.total, double_row_histogram: f31q.hist, compared: f31q.compared, mismatches: f31q.mismatches },
    sextet_census: { total: sextetTotal, counts: sextet, mismatches: sextetMismatch }
  },
  checks,
  check_count: checks.length,
  all_pass: checks.every(x => x.pass),
  interpretation_guard: "Structural overlap census only. It is not a Pm survival value, game verdict, certificate, or closure claim. Standard 11x11 empty board, two-stone roots, S2, and classes 1/2/4 remain UNKNOWN."
};
if (!output.all_pass) throw new Error("one or more checks failed");
fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify(output, null, 2) + "\n");
process.stdout.write(JSON.stringify({ all_pass: output.all_pass, check_count: output.check_count, output: OUT }) + "\n");
