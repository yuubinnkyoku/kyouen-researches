#!/usr/bin/env node
/**
 * Independent structural preread for rank-30 of the cost-16 parent.
 * Reads three pinned JSON files; does not call the Pm engine or infer game verdicts.
 * Run from repository root: node research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/cost16_survival_k30_preread_20261118.mjs
 */
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const EXP = "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118";
const INPUTS = {
  aggregate: { path: path.join(EXP, "output/cost16-b-phase-groups-20261118.json"), sha: "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87" },
  k27: { path: path.join(EXP, "output/cost16-survival-k27-20261118.json"), sha: "3dc30ad6c51cc2d7678cc8777e4af2376267ddb8" },
  k28: { path: path.join(EXP, "output/cost16-survival-k28-20261118.json"), sha: "99db3a9a48d044727b3a4d83fb7fc97daa7513d2" }
};
const OUT = path.join(EXP, "output/cost16-survival-k30-preread-20261118.json");

function gitBlobSha1(bytes) {
  const header = Buffer.from("blob " + bytes.length + "\\0");
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
const k27 = loadPinned(INPUTS.k27);
const k28 = loadPinned(INPUTS.k28);
const top50 = aggregate.derived.top50_by_membership;
const top = top50.slice(0, 30);
const rows = top.map(x => x.rows_covered);
const rowMasks = makeRowMasks(rows, aggregate.derived.rows);
const c28 = newCensus(28, rows, rowMasks), f28t = fullCensus(28, 3, rows, rowMasks), f28q = fullCensus(28, 5, rows, rowMasks);
const c29 = newCensus(29, rows, rowMasks), f29t = fullCensus(29, 3, rows, rowMasks), f29q = fullCensus(29, 5, rows, rowMasks);
const c30 = newCensus(30, rows, rowMasks), f30t = fullCensus(30, 3, rows, rowMasks), f30q = fullCensus(30, 5, rows, rowMasks);
const priorHits = {};
for (const r of rows[29]) priorHits[String(r)] = rows.slice(0, 29).filter(rs => rs.includes(r)).length;
const expected29FullHist = {};
for (const r of new Set([...Object.keys(k28.structure.quint_b_only_double_rows), ...Object.keys(c29.hist)])) {
  expected29FullHist[r] = Number(k28.structure.quint_b_only_double_rows[r] || 0) + Number(c29.hist[r] || 0);
}
const hist30Diff = {};
for (const [r, v] of Object.entries(f30q.hist)) {
  const d = v - (f29q.hist[r] || 0);
  if (d) hist30Diff[r] = d;
}
const checks = [];
const add = (name, pass, detail = {}) => checks.push({ name, pass, detail });
add("top50_has_50_unique_pair_roots", top50.length === 50 && new Set(top50.map(x => x.root)).size === 50 && top50.every(x => x.rows_covered.length === 2));
add("rank28_root_matches_published", top[27].root === k28.structure.rank28_root.root && same({ rows: rows[27] }, { rows: k28.structure.rank28_root.rows }));
add("rank28_new_census_matches_published", c28.result.pair.b_only === 14 && c28.result.pair.zero === 0 && c28.result.pair.disjoint === 13 && c28.result.triple.b_only === 214 && c28.result.triple.zero === 99 && c28.result.triple.disjoint === 38 && c28.result.quad.b_only === 626 && c28.result.quad.zero === 2277 && c28.result.quad.disjoint === 22 && c28.result.quint.b_only === 331 && c28.result.quint.zero === 17219 && c28.result.quint.disjoint === 0);
add("rank28_full_census_matches_published", f28t.counts.b_only === k28.structure.triple_census_k28.b_only && f28t.counts.zero === k28.structure.triple_census_k28.zero && f28t.counts.disjoint === k28.structure.triple_census_k28.disjoint && f28q.counts.b_only === k28.structure.quint_census_k28.b_only && f28q.counts.zero === k28.structure.quint_census_k28.zero && f28q.counts.disjoint === k28.structure.quint_census_k28.disjoint && same(f28q.hist, k28.structure.quint_b_only_double_rows));
add("rank28_two_classifiers_agree", c28.mismatches === 0 && f28t.mismatches === 0 && f28q.mismatches === 0);
add("rank29_root_matches_log_anchor", top[28].root === "00000000000000801202000000101001" && same({ rows: rows[28] }, { rows: [0, 16] }));
add("rank29_new_census_matches_log_anchor", c29.result.pair.b_only === 4 && c29.result.pair.disjoint === 24 && c29.result.triple.b_only === 195 && c29.result.triple.zero === 32 && c29.result.triple.disjoint === 151 && c29.result.quad.b_only === 1516 && c29.result.quad.zero === 1535 && c29.result.quad.disjoint === 225 && c29.result.quint.b_only === 2128 && c29.result.quint.zero === 18347 && c29.result.quint.disjoint === 0 && same(c29.hist, { "15": 283, "16": 172, "18": 1297, "19": 376 }));
add("rank29_full_census_matches_log_anchor", f29t.counts.b_only === 2204 && f29t.counts.zero === 759 && f29t.counts.disjoint === 691 && f29q.counts.b_only === 4640 && f29q.counts.zero === 114115 && f29q.counts.disjoint === 0 && same(f29q.hist, expected29FullHist));
add("rank29_two_classifiers_agree", c29.mismatches === 0 && f29t.mismatches === 0 && f29q.mismatches === 0);
add("rank30_root_matches_top50", top[29].root === "00000000080008003800000008001000" && same({ rows: rows[29] }, { rows: [14, 19] }));
add("rank30_prior_hits_match", same(priorHits, { "14": 1, "19": 7 }));
add("rank30_new_pair_census", c30.result.pair.b_only === 8 && c30.result.pair.zero === 0 && c30.result.pair.disjoint === 21 && c30.result.pair.total === 29);
add("rank30_new_triple_census", c30.result.triple.b_only === 248 && c30.result.triple.zero === 56 && c30.result.triple.disjoint === 102 && c30.result.triple.total === 406);
add("rank30_new_quad_census", c30.result.quad.b_only === 1302 && c30.result.quad.zero === 2241 && c30.result.quad.disjoint === 111 && c30.result.quad.total === 3654);
add("rank30_new_quint_census", c30.result.quint.b_only === 1328 && c30.result.quint.zero === 22423 && c30.result.quint.disjoint === 0 && c30.result.quint.total === 23751);
add("rank30_two_classifiers_agree", c30.mismatches === 0);
add("rank30_full_census_totals", f30t.total === 4060 && f30q.total === 142506 && f30t.counts.b_only === 2452 && f30t.counts.zero === 815 && f30t.counts.disjoint === 793 && f30q.counts.b_only === 5968 && f30q.counts.zero === 136538 && f30q.counts.disjoint === 0);
add("rank30_full_minus_new_equals_rank29", f30t.counts.b_only - c30.result.triple.b_only === f29t.counts.b_only && f30t.counts.zero - c30.result.triple.zero === f29t.counts.zero && f30t.counts.disjoint - c30.result.triple.disjoint === f29t.counts.disjoint && f30q.counts.b_only - c30.result.quint.b_only === f29q.counts.b_only && f30q.counts.zero - c30.result.quint.zero === f29q.counts.zero && f30q.counts.disjoint - c30.result.quint.disjoint === f29q.counts.disjoint);
add("rank30_quint_histogram_increment_matches", same(hist30Diff, c30.hist));
add("rank30_disjoint_quad_unions_all_size8", c30.disjointQuads.length === 111 && c30.disjointQuads.every(q => q.rows_union.length === 8));
add("rank30_b_only_quint_profiles_partition", same(c30.profiles, { "3/2/0": 1328 }));

const output = {
  schema: "n11-cost16-k30-preread-20261118-v1",
  date: "2026-11-18",
  lane: "n11 long lane (verification side)",
  title: "31-row cost-16 parent: rank-30 structural preread",
  inputs: {
    aggregate: { path: INPUTS.aggregate.path, git_blob_sha1: INPUTS.aggregate.sha },
    k27_result: { path: INPUTS.k27.path, git_blob_sha1: INPUTS.k27.sha },
    k28_result: { path: INPUTS.k28.path, git_blob_sha1: INPUTS.k28.sha },
    rank29_anchor: "research/log/2026-11-18-n11-cost16-survival-k29-preread.md"
  },
  scope: { parent: "00000000000000003800000008001000", rows: 31, minimum_cover_size: 16, top50_rank: 30, rank_convention: "top50_by_membership; 1-based rank 30" },
  rank29_regression: {
    new_census: c29.result,
    new_quint_double_row_histogram: c29.hist,
    full_triples: f29t.counts,
    full_quints: f29q.counts,
    full_quint_double_row_histogram: f29q.hist,
    classifier_comparisons: c29.compared + f29t.compared + f29q.compared,
    mismatches: c29.mismatches + f29t.mismatches + f29q.mismatches
  },
  rank30: {
    root: top[29].root,
    rows: rows[29],
    prior_hits: priorHits,
    new_census: c30.result,
    new_quint_double_row_histogram: c30.hist,
    b_only_quint_four_subset_profiles: c30.profiles,
    disjoint_quad_count: c30.disjointQuads.length,
    disjoint_quad_union_sizes: [...new Set(c30.disjointQuads.map(q => q.rows_union.length))].sort((a, b) => a - b),
    full_triples: { counts: f30t.counts, total: f30t.total, double_row_histogram: f30t.hist, compared: f30t.compared, mismatches: f30t.mismatches },
    full_quints: { counts: f30q.counts, total: f30q.total, double_row_histogram: f30q.hist, compared: f30q.compared, mismatches: f30q.mismatches }
  },
  checks,
  check_count: checks.length,
  all_pass: checks.every(x => x.pass),
  interpretation_guard: "Structural overlap census only. It is not a Pm survival value, game verdict, certificate, or closure claim. Standard 11x11 empty board, two-stone roots, S2, and classes 1/2/4 remain UNKNOWN."
};
if (!output.all_pass) throw new Error("one or more checks failed");
fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify(output, null, 2) + "\\n");
process.stdout.write(JSON.stringify({ all_pass: output.all_pass, check_count: output.check_count, output: OUT }) + "\\n");
