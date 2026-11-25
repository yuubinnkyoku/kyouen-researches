#!/usr/bin/env node
// n11 residual72 36-root exact class-membership regeneration (2026-11-21)
// Single-owner lane: research/experiments/n11-residual72-36root-exact-class-membership-20261121/
// Method pin (verbatim reproduction target):
//   research/experiments/n11-residual72-36root-three-ply-frontier-20261120/audit_36_root_three_ply_frontier_20261120.mjs
//   SHA-256 7177a25a799510d0fa65424fddaaeeefa9148fb0c389ffdcb2384676fdd5d57a
// Input pin (K1075 witness_full, verified):
//   research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json
//   SHA-256 49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa
//   git blob SHA-1 45744d8255f454eae3e0d59b0e2246df80e98667
// Usage:
//   regen:    node exact_membership_regen_20261121.mjs regen <input.json> <chunkdir>
//   assemble: node exact_membership_regen_20261121.mjs assemble <input.json> <chunkdir> \
//               <published-census.json> <candidate-partition.json> <outdir>
// Interpretation: geometric class bookkeeping only. No probes, no verdicts, no game value.
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
const mode = process.argv[2];
const K1075_PATH = process.argv[3];
const CHUNK_DIR = process.argv[4];
const PIN = { blob_sha1: "45744d8255f454eae3e0d59b0e2246df80e98667", sha256: "49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa" };
const need = (ok, msg) => { if (!ok) throw new Error(msg); };
const bytes = fs.readFileSync(K1075_PATH);
need(createHash("sha256").update(bytes).digest("hex") === PIN.sha256, "input SHA-256 mismatch");
need(createHash("sha1").update(Buffer.concat([Buffer.from("blob " + bytes.length + "\0"), bytes])).digest("hex") === PIN.blob_sha1, "input blob SHA-1 mismatch");
const roots = JSON.parse(bytes.toString("utf8")).witness_full;
// ---- verbatim method core (from published audit_36_root_three_ply_frontier_20261120.mjs) ----
const N = 121, ALL = (1n << 121n) - 1n, BIT = Array.from({ length: N }, (_, i) => 1n << BigInt(i));
const ROW = Array.from({ length: N }, (_, i) => { const x = BigInt(i % 11), y = BigInt(Math.floor(i / 11)); return [x * x + y * y, x, y]; });
function detC(a, b, c, q) { const A = ROW[a], B = ROW[b], C = ROW[c], Q = ROW[q], u0 = B[0] - A[0], u1 = B[1] - A[1], u2 = B[2] - A[2], v0 = C[0] - A[0], v1 = C[1] - A[1], v2 = C[2] - A[2], w0 = Q[0] - A[0], w1 = Q[1] - A[1], w2 = Q[2] - A[2]; return u0 * (v1 * w2 - v2 * w1) - u1 * (v0 * w2 - v2 * w0) + u2 * (v0 * w1 - v1 * w0); }
function detL(a, b, c, q) { const A = ROW[a], B = ROW[b], C = ROW[c], Q = ROW[q], u0 = B[0] - A[0], u1 = B[1] - A[1], u2 = B[2] - A[2], v0 = C[0] - A[0], v1 = C[1] - A[1], v2 = C[2] - A[2], w0 = Q[0] - A[0], w1 = Q[1] - A[1], w2 = Q[2] - A[2]; return u0 * v1 * w2 + u1 * v2 * w0 + u2 * v0 * w1 - u2 * v1 * w0 - u1 * v0 * w2 - u0 * v2 * w1; }
const memo = new Map(); let pointChecks = 0;
function triple(a, b, c) { const s = [a, b, c].sort((x, y) => x - y), k = (s[0] * N + s[1]) * N + s[2]; if (memo.has(k)) return memo.get(k); let m = 0n; for (let q = 0; q < N; q++) { const x = detC(s[0], s[1], s[2], q), y = detL(s[0], s[1], s[2], q); pointChecks++; need(x === y, "determinant mismatch"); if (x === 0n) m |= BIT[q]; } memo.set(k, m); return m; }
const T = []; for (let s = 0; s < 2; s++) for (let fx = 0; fx < 2; fx++) for (let fy = 0; fy < 2; fy++) { const a = []; for (let i = 0; i < N; i++) { const x = i % 11, y = Math.floor(i / 11); let u = s ? y : x, v = s ? x : y; if (fx) u = 10 - u; if (fy) v = 10 - v; a[i] = u + 11 * v; } T.push(a); }
function bits(m) { const a = []; for (let i = 0; i < N; i++) if (m & BIT[i]) a.push(i); return a; }
function canon(st) { let best = null; for (const t of T) { let m = 0n; for (const p of st) m |= BIT[t[p]]; if (best === null || m < best) best = m; } return best.toString(16).padStart(32, "0"); }
function pairMask(st, p) { let m = 0n; for (let a = 0; a < st.length; a++) for (let b = a + 1; b < st.length; b++) m |= triple(st[a], st[b], p); return m; }
function pop(m) { let n = 0; while (m) { m &= m - 1n; n++; } return n; }
let rootQuads = 0;
function enumerateRoot(i) {
  const item = roots[i], root = BigInt("0x" + item.root), st = bits(root);
  need(item.safe === true && st.length === 7 && canon(st) === item.root, "root identity/safety failure");
  for (let a = 0; a < 7; a++) for (let b = a + 1; b < 7; b++) for (let c = b + 1; c < 7; c++) for (let d = c + 1; d < 7; d++) { const x = detC(st[a], st[b], st[c], st[d]), y = detL(st[a], st[b], st[c], st[d]); rootQuads++; need(x === y && x !== 0n, "unsafe root quadruple"); }
  let base = 0n; for (let a = 0; a < 7; a++) for (let b = a + 1; b < 7; b++) for (let c = b + 1; c < 7; c++) base |= triple(st[a], st[b], st[c]);
  const first = bits(ALL & ~(base | root));
  const c8 = new Set(), c9 = new Set(), c10 = new Set();
  for (const p of first) { c8.add(canon(st.concat(p))); }
  let n9 = 0, raw = 0, within = 0, third = 0, terms = 0, min3 = 999, max3 = -1;
  for (const p of first) {
    const ep = pairMask(st, p), occ8 = root | BIT[p], st8 = st.concat(p), legal8 = ALL & ~(base | ep | occ8);
    for (const q of first) {
      if (q <= p || !(legal8 & BIT[q])) continue;
      n9++; c9.add(canon(st8.concat(q)));
      const eq = pairMask(st8, q), occ9 = occ8 | BIT[q], replies = ALL & ~(base | ep | eq | occ9), n = pop(replies);
      third += n; if (n === 0) terms++; min3 = Math.min(min3, n); max3 = Math.max(max3, n);
      for (let r = q + 1; r < N; r++) if (replies & BIT[r]) { raw++; c10.add(canon(st8.concat(q, r))); }
    }
  }
  const d4 = c10.size; within = raw - d4;
  need(third === 3 * raw && raw - d4 === within, "frontier accounting failure");
  return { rank: i + 1, root: item.root, rows: item.rows, worker: i % 4, first: first.length, n9, third, raw10: raw, d4, within, terminal9: terms, min3, max3, c8: [...c8], c9: [...c9], c10: [...c10] };
}
if (mode === "regen") {
  fs.mkdirSync(CHUNK_DIR, { recursive: true });
  const t0 = Date.now();
  const per = [];
  for (let i = 0; i < roots.length; i++) {
    const chunkPath = path.join(CHUNK_DIR, "root-" + String(i).padStart(2, "0") + ".json");
    const rec = enumerateRoot(i);
    fs.writeFileSync(chunkPath, JSON.stringify(rec));
    per.push({ rank: rec.rank, root: rec.root, worker: rec.worker, first: rec.first, n9: rec.n9, third: rec.third, raw10: rec.raw10, d4: rec.d4, within: rec.within, terminal9: rec.terminal9, min3: rec.min3, max3: rec.max3 });
    process.stdout.write("root " + rec.rank + "/36 done " + (Date.now() - t0) + "ms memo=" + memo.size + "\n");
  }
  need(pointChecks === memo.size * N, "point check identity failed");
  fs.writeFileSync(path.join(CHUNK_DIR, "regen-summary.json"), JSON.stringify({ point_checks: pointChecks, unique_triples: memo.size, root_quads: rootQuads, wall_ms: Date.now() - t0, per_root: per }, null, 1));
  process.stdout.write("REGEN COMPLETE pointChecks=" + pointChecks + " uniqueTriples=" + memo.size + " rootQuads=" + rootQuads + "\n");
} else if (mode === "assemble") {
  const CENSUS_PATH = process.argv[5], CANDIDATE_PATH = process.argv[6], OUT_DIR = process.argv[7];
  const census = JSON.parse(fs.readFileSync(CENSUS_PATH, "utf8"));
  const cand = JSON.parse(fs.readFileSync(CANDIDATE_PATH, "utf8"));
  const regen = JSON.parse(fs.readFileSync(path.join(CHUNK_DIR, "regen-summary.json"), "utf8"));
  // --- gate 1: regeneration invariants (published 12-gate equivalents) ---
  const per = regen.per_root;
  const checks = [];
  checks.push(["36 roots", per.length === 36 && regen.root_quads === 1260]);
  checks.push(["determinant expansions", regen.point_checks === regen.unique_triples * 121]);
  const total9 = per.reduce((s, x) => s + x.n9, 0);
  const totalRaw10 = per.reduce((s, x) => s + x.raw10, 0);
  const totalD4 = per.reduce((s, x) => s + x.d4, 0);
  const withinAll = per.reduce((s, x) => s + x.within, 0);
  const terminal9 = per.reduce((s, x) => s + x.terminal9, 0);
  checks.push(["9-stone total", total9 === 56597]);
  checks.push(["raw 10-stone total", totalRaw10 === 733855]);
  checks.push(["D4 membership total", totalD4 === 733800]);
  checks.push(["within-root merges", withinAll === 55]);
  checks.push(["terminal count", terminal9 === 0]);
  checks.push(["third move identity", per.every(x => x.third === 3 * x.raw10)]);
  // --- build exact class->root membership maps from chunks ---
  const owners = [new Map(), new Map(), new Map()]; // [8-stone, 9-stone, 10-stone]
  for (let i = 0; i < roots.length; i++) {
    const rec = JSON.parse(fs.readFileSync(path.join(CHUNK_DIR, "root-" + String(i).padStart(2, "0") + ".json"), "utf8"));
    for (const k of rec.c8) { const m = owners[0]; m.set(k, (m.get(k) || 0n) | (1n << BigInt(i))); }
    for (const k of rec.c9) { const m = owners[1]; m.set(k, (m.get(k) || 0n) | (1n << BigInt(i))); }
    for (const k of rec.c10) { const m = owners[2]; m.set(k, (m.get(k) || 0n) | (1n << BigInt(i))); }
    // per-root published cross-check
    const pub = census.per_root.find(x => x.rank === rec.rank);
    need(pub, "published per_root missing rank " + rec.rank);
    for (const f of ["root", "worker", "first", "n9", "third", "raw10", "d4", "within", "terminal9", "min3", "max3"]) need(pub[f] === rec[f], "per_root field mismatch " + f + " rank " + rec.rank + " got " + rec[f] + " pub " + pub[f]);
  }
  checks.push(["global D4 classes", owners[2].size === 728370]);
  // --- gate 2: exact class-level validation against published census (10-stone) ---
  const multiplicity = {}; let dupMem = 0, maxM = 0;
  const multi10 = [];
  for (const [k, m] of owners[2]) { const n = popN(m); multiplicity[n] = (multiplicity[n] || 0) + 1; if (n > 1) { dupMem += n - 1; if (n > maxM) maxM = n; multi10.push({ c: k, roots: memberIds(m, roots) }); } }
  checks.push(["cross-root duplicates", dupMem === 5430]);
  checks.push(["multiplicity", maxM === 3]);
  need(multiplicity[2] === 5420 && multiplicity[3] === 5, "multiplicity histogram mismatch " + JSON.stringify(multiplicity));
  const pairCounts = Array.from({ length: roots.length }, () => new Uint32Array(roots.length));
  for (const m of owners[2].values()) { const mem = memberIds(m, roots); for (let a = 0; a < mem.length; a++) for (let b = a + 1; b < mem.length; b++) pairCounts[mem[a]][mem[b]]++; }
  const overlaps = [];
  for (let i2 = 0; i2 < roots.length; i2++) for (let j = i2 + 1; j < roots.length; j++) { const n2 = pairCounts[i2][j]; if (n2) overlaps.push({ a: roots[i2].root, b: roots[j].root, shared: n2, workerA: i2 % 4, workerB: j % 4 }); }
  overlaps.sort((x, y) => y.shared - x.shared || x.a.localeCompare(y.a) || x.b.localeCompare(y.b));
  const pubOv = census.pairwise_overlap;
  checks.push(["pairwise overlap count", overlaps.length === pubOv.length && pubOv.length === 221]);
  const pairwiseExact = overlaps.length === pubOv.length && overlaps.every((o, idx) => o.a === pubOv[idx].a && o.b === pubOv[idx].b && o.shared === pubOv[idx].shared && o.workerA === pubOv[idx].workerA && o.workerB === pubOv[idx].workerB);
  checks.push(["pairwise overlap exact match", pairwiseExact]);
  let sameW = 0, crossW = 0;
  for (const o of overlaps) { if (o.workerA === o.workerB) sameW += o.shared; else crossW += o.shared; }
  checks.push(["worker split overlap", sameW === 1242 && crossW === 4193]);
  // published summary equality
  const pubS = census.summary;
  checks.push(["published summary match",
    pubS.unique_9stone_positions === total9 && pubS.raw_10stone_positions === totalRaw10 && pubS.per_root_d4_memberships === totalD4 &&
    pubS.within_root_d4_merges === withinAll && pubS.global_unique_d4_classes === owners[2].size &&
    pubS.cross_root_duplicate_memberships === dupMem && pubS.pairwise_overlap_total === overlaps.reduce((s, o) => s + o.shared, 0) &&
    pubS.multiplicity_histogram["2"] === 5420 && pubS.multiplicity_histogram["3"] === 5 && pubS.overlapping_root_pairs === 221]);
  // worker stats check for baseline
  const wstats = Array.from({ length: 4 }, (_, w) => { const a = per.filter(x => x.worker === w); return { worker: w, roots: a.length, n9: a.reduce((s, x) => s + x.n9, 0), raw10: a.reduce((s, x) => s + x.raw10, 0), d4: a.reduce((s, x) => s + x.d4, 0), within: a.reduce((s, x) => s + x.within, 0) }; });
  checks.push(["worker stats match census", JSON.stringify(wstats) === JSON.stringify(census.worker_stats)]);
  // --- candidate assignment validation ---
  const rootIdx = new Map(roots.map((r, i) => [r.root, i]));
  const groups = cand.candidate.root_groups;
  const candWorkerOf = new Array(roots.length).fill(-1);
  const seen = new Set();
  groups.forEach((g, w) => { need(g.length === 9, "candidate group " + w + " not 9"); for (const rh of g) { need(rootIdx.has(rh), "candidate root unknown: " + rh); const idx = rootIdx.get(rh); need(!seen.has(idx), "candidate root duplicated: " + rh); seen.add(idx); candWorkerOf[idx] = w; } });
  checks.push(["candidate assignment exactly-once", seen.size === 36 && candWorkerOf.indexOf(-1) === -1]);
  // candidate pairwise cross/within from exact memberships
  function pairOverlapFor(workerOf) { let within = 0, cross = 0; for (const m of owners[2].values()) { const mem = memberIds(m, roots); for (let a = 0; a < mem.length; a++) for (let b = a + 1; b < mem.length; b++) { if (workerOf[mem[a]] === workerOf[mem[b]]) within++; else cross++; } } return { within, cross }; }
  const baseWorkerOf = roots.map((r, idx) => idx % 4);
  const baseOv = pairOverlapFor(baseWorkerOf);
  checks.push(["baseline cross/within matches candidate JSON", baseOv.cross === cand.baseline.cross_worker_pairwise_overlap && baseOv.within === cand.baseline.within_worker_pairwise_overlap]);
  const candOv = pairOverlapFor(candWorkerOf);
  checks.push(["candidate cross/within matches candidate JSON", candOv.cross === cand.candidate.cross_worker_pairwise_overlap && candOv.within === cand.candidate.within_worker_pairwise_overlap]);
  // --- NEW: exact class-level worker statistics (per assignment, per layer) ---
  function classStats(workerOf, ownersMap) {
    const perWorkerVisits = new Array(4).fill(0), perWorkerUnique = new Array(4).fill(0);
    let withinCopies = 0, crossClasses = 0, crossCopies = 0, spanHist = {};
    for (const m of ownersMap.values()) {
      const mem = memberIds(m, roots);
      for (const rid of mem) perWorkerVisits[workerOf[rid]]++;
      const wset = new Map();
      for (const rid of mem) { const w = workerOf[rid]; wset.set(w, (wset.get(w) || 0) + 1); }
      for (const w of wset.keys()) perWorkerUnique[w]++;
      for (const n of wset.values()) withinCopies += n - 1;
      const span = wset.size; spanHist[span] = (spanHist[span] || 0) + 1;
      if (span > 1) { crossClasses++; crossCopies += span - 1; }
    }
    return { per_worker_visits: perWorkerVisits, per_worker_unique_classes: perWorkerUnique, within_worker_redundant_copies: withinCopies, classes_spanning_multiple_workers: crossClasses, cross_worker_redundant_copies: crossCopies, worker_span_histogram: spanHist };
  }
  const stats = {
    baseline: { assignment: "roots[W::4]", stone10: classStats(baseWorkerOf, owners[2]), stone09: classStats(baseWorkerOf, owners[1]), stone08: classStats(baseWorkerOf, owners[0]) },
    candidate: { assignment: "worker-partition-candidate-20261121 root_groups", stone10: classStats(candWorkerOf, owners[2]), stone09: classStats(candWorkerOf, owners[1]), stone08: classStats(candWorkerOf, owners[0]) }
  };
  // candidate d4 per-worker loads cross-check against candidate JSON
  for (let w = 0; w < 4; w++) { need(stats.baseline.stone10.per_worker_visits[w] === cand.baseline.loads.d4[w], "baseline d4 load mismatch worker " + w); need(stats.candidate.stone10.per_worker_visits[w] === cand.candidate.loads.d4[w], "candidate d4 load mismatch worker " + w); }
  checks.push(["d4 per-worker loads match candidate JSON", true]);
  // 9-stone / 8-stone exact membership tables (multi-root classes)
  function multiTable(ownersMap) { const tbl = []; let dupmem = 0, maxmulti = 0, hist = {}; for (const [k, m] of ownersMap) { const n = popN(m); hist[n] = (hist[n] || 0) + 1; if (n > 1) { dupmem += n - 1; if (n > maxmulti) maxmulti = n; tbl.push({ c: k, roots: memberIds(m, roots) }); } } tbl.sort((x, y) => y.roots.length - x.roots.length || x.c.localeCompare(y.c)); return { multi_classes: tbl, duplicate_memberships: dupmem, max_multiplicity: maxmulti, multiplicity_histogram: hist, unique_classes: ownersMap.size }; }
  const t9 = multiTable(owners[1]);
  const t8 = multiTable(owners[0]);
  need(checks.every(([nm, pass]) => pass), "GATE FAILED: " + checks.filter(([nm, pass]) => !pass).map(([nm]) => nm).join(", "));
  const result = {
    schema: "n11-residual72-36root-exact-class-membership-20261121-v1",
    date: "2026-11-21",
    status: "exact-class-membership-regeneration-cross-checked",
    source: {
      k1075_sha256: PIN.sha256, k1075_git_blob_sha1: PIN.blob_sha1,
      census_sha256: "94fdb0c6e3503f1e9d19aaaf345f4478157c5a44374f10642c52325f346c2023",
      method_pin: "audit_36_root_three_ply_frontier_20261120.mjs 7177a25a799510d0fa65424fddaaeeefa9148fb0c389ffdcb2384676fdd5d57a",
      candidate_sha256: "09b394b88cfb0246c278b335b82cfc5f8763f551c0f42c89403977b5e273918b"
    },
    regen: { point_checks: regen.point_checks, unique_triples: regen.unique_triples, root_quads: regen.root_quads },
    stone10: {
      unique_d4_classes: owners[2].size,
      per_root_d4_memberships: totalD4,
      duplicate_memberships: dupMem,
      multiplicity_histogram: multiplicity,
      multi_root_classes_ref: "output/multi-root-classes-10stone-20261121.json",
      triple_root_classes: multi10.filter(x => x.roots.length === 3)
    },
    stone09: { unique_d4_classes: t9.unique_classes, duplicate_memberships: t9.duplicate_memberships, max_multiplicity: t9.max_multiplicity, multiplicity_histogram: t9.multiplicity_histogram },
    stone08: { unique_d4_classes: t8.unique_classes, duplicate_memberships: t8.duplicate_memberships, max_multiplicity: t8.max_multiplicity, multiplicity_histogram: t8.multiplicity_histogram },
    partition_stats: stats,
    pairwise_regeneration_exact_match: pairwiseExact,
    checks: checks.map(([nm, pass]) => ({ name: nm, pass })),
    check_count: checks.length, all_pass: true,
    interpretation_guard: [
      "Geometric class bookkeeping only; not DFPN cost, TT hit rate, or proof reuse.",
      "A shared D4 class does not imply identical search depth, proof boundary, or an actual TT hit.",
      "No change to the active 36-root depth-10 sweep or its assignment is made or proposed.",
      "REFUTED-D10 is not a LOSS proof. The 36 roots are candidates, not WIN certificates.",
      "Standard 11x11 empty board, two-stone roots, S2, class 1/2/4 verdicts remain UNKNOWN."
    ]
  };
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.writeFileSync(path.join(OUT_DIR, "exact-class-membership-20261121.json"), JSON.stringify(result, null, 2) + "\n");
  const sortedMulti10 = multi10.slice().sort((x, y) => y.roots.length - x.roots.length || x.c.localeCompare(y.c));
  fs.writeFileSync(path.join(OUT_DIR, "multi-root-classes-10stone-20261121.json"), JSON.stringify(sortedMulti10, null, 1) + "\n");
  const t9p = t9.multi_classes, t8p = t8.multi_classes;
  fs.writeFileSync(path.join(OUT_DIR, "multi-root-classes-09stone-20261121.json"), JSON.stringify({ classes: t9p, count: t9p.length, duplicate_memberships: t9.duplicate_memberships, max_multiplicity: t9.max_multiplicity }, null, 1) + "\n");
  fs.writeFileSync(path.join(OUT_DIR, "multi-root-classes-08stone-20261121.json"), JSON.stringify({ classes: t8p, count: t8p.length, duplicate_memberships: t8.duplicate_memberships, max_multiplicity: t8.max_multiplicity }, null, 1) + "\n");
  process.stdout.write("ASSEMBLE OK all " + checks.length + " gates pass\n");
} else { throw new Error("unknown mode"); }
function popN(m) { let n = 0n; while (m) { m &= m - 1n; n++; } return Number(n); }
function memberIds(m, rs) { const out = []; for (let i = 0; i < rs.length; i++) if ((m >> BigInt(i)) & 1n) out.push(i); return out; }
