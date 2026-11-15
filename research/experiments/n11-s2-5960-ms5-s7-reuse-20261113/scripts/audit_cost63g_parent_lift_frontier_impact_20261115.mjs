#!/usr/bin/env node
// Independent structural audit of cost63g's 14 published WIN7 roots.
// This checks D4 parent lifts and the target-S5 frontier intersection only.
// It does NOT replay certificate trees or claim that the receipt fold is done.
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = resolve(HERE, '../output');
const INPUTS = {
  audit: 'class2-lane-cost63g-sweep-audit-20261115.json',
  claim: 'class2-lane-cost63g-inflight-20261115.json',
  ranking: 'class-frontier-s5-ranking-after-cost63f-receipts-20261115.csv',
  top: 'class-frontier-top-candidates-s6-after-cost63f-receipts-20261115.csv',
  head: 'class-frontier-cost63f-receipts-recompute-20261115.json',
};
const EXPECTED_BLOBS = {
  audit: '9603730b745413e5a99e10a2fecd48075f81ba2c',
  claim: '663a9ba8459caa2b332683baa05232aeba046d70',
  ranking: '8f1037faa322a245ed7e4dafe047e9ab38935cba',
  top: 'd640a8edd4a3d1f829f493e710f20ca8cec7c63d',
  head: 'e1e72b12ca39769f2c4a298d91833b612c97afeb',
};
function assert(ok, message) { if (!ok) throw new Error(message); }
function readPinned(key) {
  const path = resolve(OUT, INPUTS[key]);
  const bytes = readFileSync(path);
  const blob = createHash('sha1')
    .update(Buffer.concat([Buffer.from('blob ' + bytes.length + '\0'), bytes]))
    .digest('hex');
  assert(blob === EXPECTED_BLOBS[key], key + ' Git blob SHA mismatch: ' + blob);
  return bytes.toString('utf8');
}
const source = Object.fromEntries(Object.keys(INPUTS).map(k => [k, readPinned(k)]));
const audit = JSON.parse(source.audit);
const claim = JSON.parse(source.claim);
const head = JSON.parse(source.head);
const child = BigInt('0x' + audit.child);
const target = audit.s5_target;
const frontier = head.frontier_after_cost63f;
assert(frontier.solved_s6_in_manifest === 1199, 'head solved count mismatch');
assert(frontier.unique_remaining_s6 === 6648, 'head remaining count mismatch');
assert(frontier.sum_remaining_cost === 524616, 'head remaining cost mismatch');
assert(frontier.s6_needed_by_open_classes === 4918, 'head open S6 demand mismatch');
assert(frontier.cost_needed_by_open_classes === 388339, 'head open cost demand mismatch');
assert(claim.status === 'sweep_and_certificates_complete_fold_pending', 'cost63g is not fold-pending');
assert(claim.rebase_target.startsWith('1199/6648/524616/4918/388339'), 'wrong rebase head');
assert(audit.candidates === 63 && audit.win7_count === 14 &&
  audit.refuted_count === 49 && audit.capped_count === 0 &&
  audit.candidate_nodes_total === 75637935, 'cost63g sweep totals mismatch');
assert(claim.win7_certificates.published === 14 &&
  claim.win7_certificates.total_rows === 419398, 'certificate claim totals mismatch');

const hex = n => n.toString(16).padStart(32, '0');
function canon(mask) {
  let best = null;
  for (let t = 0; t < 8; t++) {
    let z = 0n;
    for (let i = 0; i < 121; i++) if ((mask >> BigInt(i)) & 1n) {
      let x = i % 11, y = Math.floor(i / 11);
      if (t >= 4) x = 10 - x;
      for (let r = 0; r < t % 4; r++) { const q = x; x = 10 - y; y = q; }
      z |= 1n << BigInt(11 * y + x);
    }
    if (best === null || z < best) best = z;
  }
  return best;
}
const roots = Object.entries(audit.root_orbit_check.orbit_map)
  .map(([root, bits]) => ({ root: BigInt('0x' + root), rootHex: root, moveBit: bits[0] }));
assert(roots.length === 14, 'expected 14 roots');
const parentOrigins = new Map();
for (const r of roots) {
  assert(canon(r.root) === r.root, 'root is not D4-canonical: ' + r.rootHex);
  assert(canon(child | (1n << BigInt(r.moveBit))) === r.root,
    'root/child move relation mismatch: ' + r.rootHex);
  let stones = 0;
  for (let b = 0; b < 121; b++) if ((r.root >> BigInt(b)) & 1n) {
    stones++;
    const parent = hex(canon(r.root & ~(1n << BigInt(b))));
    if (!parentOrigins.has(parent)) parentOrigins.set(parent, []);
    parentOrigins.get(parent).push({
      root: r.rootHex, move_bit: r.moveBit, removed_stone: b,
    });
  }
  assert(stones === 7, 'root is not seven stones: ' + r.rootHex);
}
assert(parentOrigins.size === 85, 'expected 85 unique S6 parent orbits');
const shared = [...parentOrigins.entries()].filter(([, origins]) => origins.length > 1);
assert(shared.length === 1 && shared[0][0] === hex(child) &&
  shared[0][1].length === 14, 'the common parent must be the target child, shared 14 ways');
assert([...parentOrigins.values()].filter(x => x.length === 1).length === 84,
  'the other 84 parent orbits must be unique');

const ranking = source.ranking.trim().split(/\r?\n/).slice(1).map(line => {
  const [s5, classes, remaining, cost] = line.split(',');
  return { s5, classes: Number(classes), remaining: Number(remaining), cost: Number(cost) };
});
const targetRank = ranking.find(row => row.s5 === target);
assert(targetRank && targetRank.classes === 2 &&
  targetRank.remaining === 38 && targetRank.cost === 2837,
  'target S5 rank must be 2 / 38 / 2837');
const targetRows = [];
for (const line of source.top.trim().split(/\r?\n/)) {
  if (!line || line.startsWith('#') || line.startsWith('s5_hex,')) continue;
  const [s5, s6, cost] = line.split(',');
  if (s5 === target) targetRows.push({ s6, cost: Number(cost) });
}
assert(targetRows.length === 38, 'target S5 must have 38 remaining S6 rows');
assert(new Set(targetRows.map(row => row.s6)).size === 38, 'duplicate target S6 row');
assert(targetRows.reduce((sum, row) => sum + row.cost, 0) === 2837,
  'target S5 row costs must sum to 2837');
const expected = new Map([
  ['00000000080000801202000000200000', 63],
  ['00000000000000801206000000200000', 73],
  ['00000000000000801242000000200000', 71],
  ['00000008000000801202000000200000', 77],
  ['00000000200020003800000000000200', 83],
]);
const hits = targetRows.filter(row => parentOrigins.has(row.s6))
  .sort((a, b) => a.s6.localeCompare(b.s6));
assert(hits.length === 5, 'expected exactly five target-row overlaps');
assert(hits.every(row => expected.get(row.s6) === row.cost),
  'target-row overlap keys or costs mismatch');

const result = {
  schema: 'n11-class2-cost63g-parent-lift-frontier-impact-20261115-v1',
  date: '2026-11-15',
  baseline: {
    chain_head: '1199/6648/524616/4918/388339',
    solved_s6_in_manifest: 1199, remaining_s5_orbits: 175,
    unique_remaining_s6: 6648, sum_remaining_cost: 524616,
    s6_needed_by_open_classes: 4918, cost_needed_by_open_classes: 388339,
    source: 'class-frontier-cost63f-receipts-recompute-20261115.json',
  },
  cost63g: {
    s5_target: target, s6_child: hex(child), edge_cost: 63,
    candidates: 63, win7_d10: 14, refuted_d10: 49, capped: 0,
    claimed_certificates_published: 14, claimed_certificate_rows: 419398,
    note: 'The upstream inflight claim states that all 14 certificates were independently double-verified; this audit does not replay their certificate trees or rehash their bytes.',
  },
  d4_parent_lift: {
    canonical_win7_roots: roots.length, distinct_root_orbits: new Set(roots.map(r => hex(canon(r.root)))).size,
    root_to_parent_incidences: 98, unique_s6_parent_orbits: parentOrigins.size,
    shared_s6_parent_orbits: 1, shared_parent: hex(child),
    shared_parent_multiplicity: 14, other_s6_parent_orbits: 84,
    all_other_parent_multiplicity_one: true,
  },
  target_s5_impact: {
    before: { remaining_s6_orbits: 38, remaining_s7_edge_cost: 2837 },
    overlaps: hits.map(row => ({
      s6_hex: row.s6, edge_cost: row.cost,
      certificate_parent_lifts: parentOrigins.get(row.s6),
    })),
    distinct_remaining_s6_orbits_covered: 5, remaining_edge_cost_covered: 367,
    predicted_after: { remaining_s6_orbits: 33, remaining_s7_edge_cost: 2470 },
    status: 'conditional_prediction_only; not a receipt fold or updated global frontier',
  },
  inputs: Object.fromEntries(Object.entries(INPUTS).map(([key, path]) => [key, {
    path: 'research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/' + path,
    git_blob_sha: EXPECTED_BLOBS[key],
  }])),
  scope: "Exact integer D4 canonicalization of the 14 roots from the published cost63g sweep audit, their 98 one-stone deletions, and intersection with the target S5's 38 remaining S6 rows at chain head 1199. No game-theoretic value is inferred.",
};
writeFileSync(resolve(OUT, 'cost63g-parent-lift-frontier-impact-20261115.json'),
  JSON.stringify(result, null, 2) + '\n');
console.log('COST63G_PARENT_LIFT_AUDIT_PASS: 14 roots, 85 S6 parent orbits, ' +
  '5 target rows / 367 cost; predicted target 33 / 2470 (fold still pending)');
