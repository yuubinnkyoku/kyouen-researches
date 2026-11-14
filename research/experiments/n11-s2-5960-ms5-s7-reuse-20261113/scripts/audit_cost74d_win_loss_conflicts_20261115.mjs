#!/usr/bin/env node
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const EXP_DIR = resolve(SCRIPT_DIR, '..');
const OUT_DIR = resolve(EXP_DIR, 'output');
const EXPERIMENTS_DIR = resolve(EXP_DIR, '..');

const VERIFIED = [
  ['class2-batch1-certificates-verified.json', '24ddd94bf60b2f315801cbd48f08962de81485c6'],
  ['class2-batch1b-certificates-verified.json', 'b25598a3d11d031bd7a4df0d3d3d4e3d41cda741'],
  ['class2-batch2-certificates-verified.json', '82098bfb0160758127af5c0c0769d89d19582bdd'],
  ['class2-batch2b-certificates-verified.json', '5d5e339b5bc9dd4dbe294c878412eb0295de8468'],
  ['class2-batch3-certificates-verified.json', '1fab35b3d598d629406a09d8f431cb5df2eb045b'],
  ['class2-batch5-certificates-verified.json', '02bb76b2b0c135356271978cab0fbd03612a704e'],
  ['class2-certificates-verified.json', '9f58be71f986b55632e4be658c4343bba7bd4518'],
  ['class2-last-loss-verified.json', 'caf1d228954f9e11d5686bf3d056bfe31a0e0626'],
  ['class2-next-certificates-verified.json', '05952496cd040bb614d45ab146598016bc9bffc7'],
  ['class2-next-loss-verified.json', '1af90ca059352eec9db796daf7eb15c818a0546a'],
  ['class2-next2-certificates-verified.json', '62171158ea54b0acd9238f6864b2dc7f0a935edc'],
  ['class2-next3-certificates-verified.json', '6654bfeefe0314d5e6e94578aa36e09de849aaaa'],
  ['class2-next4-certificates-verified.json', 'f0570f152fe5886f0589e5b00de3038fbf783094'],
  ['class2-third-loss-verified.json', '30f4070f88926c6ee2fe1fa1e42e37bffbc4ed20'],
  ['class4-batch1-certificates-verified.json', '6ff00942c9fb20e429194dd6a4ed2e0a2dfd50da'],
  ['class4-batch2-certificates-verified.json', 'd96dc6dbadfdc1284c6cf3c66558afab6f0bf1be'],
  ['priority-certificates-verified.json', '30970ad6f0aef8ceccdc2199090b29930eaecb6f'],
];

const FIXED = {
  cost72b: ['class2-lane-cost72b-win7-certificates-20261115.json', '27ca07f9bb49e3638c901f62cab7f961844c5106'],
  cost74d: ['class2-lane-cost74d-win7-certificates-20261115.json', '0f6e7860796b999c6ab3b41d43931881085ad09f'],
  central: ['../n11-central-19-cover-20261031/terminal_loss7_parent_lift_274_manifest.json', '0eb1a47559626a08364c7d23787480f4086c63a4'],
  knownloss: ['ms5_s7_knownloss_candidates.csv', '678ab8c7ce67e81c0b6fe29abd306118fa754cb0'],
};

function gitBlobSha(raw) {
  return createHash('sha1')
    .update(Buffer.concat([Buffer.from('blob ' + raw.length + '\0'), raw]))
    .digest('hex');
}
async function readPinned(path, expectedSha) {
  const raw = await readFile(path);
  const actualSha = gitBlobSha(raw);
  assert.equal(actualSha, expectedSha, 'pinned Git blob SHA changed: ' + path);
  return raw.toString('utf8');
}
async function parsePinned(path, expectedSha) {
  return JSON.parse(await readPinned(path, expectedSha));
}
function images(mask) {
  const result = Array(8).fill(0n);
  for (let p = 0; p < 121; p++) {
    if (!((mask >> BigInt(p)) & 1n)) continue;
    const x = p % 11, y = Math.floor(p / 11);
    const coords = [
      [x,y], [y,10-x], [10-x,10-y], [10-y,x],
      [10-x,y], [x,10-y], [y,x], [10-y,10-x],
    ];
    coords.forEach(([a,b], i) => { result[i] |= 1n << BigInt(11*b+a); });
  }
  return result;
}
const canonical = hex => images(BigInt('0x' + hex))
  .map(x => x.toString(16).padStart(32, '0')).sort()[0];
const rootOf = row => (row.root || row.root_hex).toLowerCase();
const d4Set = roots => new Set(roots.map(canonical));
const intersection = (a,b) => [...a].filter(x => b.has(x)).sort();
const popcount = hex => {
  let n = BigInt('0x' + hex), count = 0;
  while (n) { n &= n - 1n; count++; }
  return count;
};

const verified = [];
for (const [name, sha] of VERIFIED) {
  const path = resolve(OUT_DIR, name);
  const doc = await parsePinned(path, sha);
  const records = (doc.certificates || []).map(row => ({
    root: rootOf(row),
    verdict: row.verdict,
  }));
  assert(records.every(row => /^[0-9a-f]{32}$/.test(row.root)));
  verified.push({ name, sha, records });
}
const priorRecords = verified.flatMap(item => item.records);
const priorWins = priorRecords.filter(row => row.verdict === 'WIN7').map(row => row.root);
const priorLosses = priorRecords.filter(row => row.verdict === 'LOSS7').map(row => row.root);

const cost72bPath = resolve(OUT_DIR, FIXED.cost72b[0]);
const cost74dPath = resolve(OUT_DIR, FIXED.cost74d[0]);
const cost72b = await parsePinned(cost72bPath, FIXED.cost72b[1]);
const cost74d = await parsePinned(cost74dPath, FIXED.cost74d[1]);
const centralPath = resolve(EXPERIMENTS_DIR, FIXED.central[0]);
const central = await parsePinned(centralPath, FIXED.central[1]);
const knownlossPath = resolve(OUT_DIR, FIXED.knownloss[0]);
const knownlossText = await readPinned(knownlossPath, FIXED.knownloss[1]);

const targetRecords = cost74d.certificates;
assert.equal(targetRecords.length, 15);
assert(targetRecords.every(row => row.verdict === 'WIN7'));
assert(targetRecords.every(row => row.root_check?.match === true && row.root_check?.stones === 7));
assert(targetRecords.every(row => row.sub_roots_pass === row.sub_roots_total));
assert(targetRecords.every(row => row.union_missing === 0 && row.union_extra === 0));
assert(targetRecords.every(row => row.terminal_range?.[0] === 13 && row.terminal_range?.[1] === 17));
assert(targetRecords.every(row => popcount(row.root_hex) === 7));
assert(targetRecords.every(row => canonical(row.root_hex) === row.d4_canonical_hex));

const targetD4 = d4Set(targetRecords.map(row => row.root_hex));
const priorWinD4 = d4Set(priorWins);
const priorLossD4 = d4Set(priorLosses);
const centralRoots = central.combined_terminal_loss7_keys.map(x => x.toLowerCase());
const centralD4 = d4Set(centralRoots);

const knownLines = knownlossText.trimEnd().split(/\r?\n/);
const header = knownLines.shift().split(',');
assert.equal(header[0], 's7_hex');
assert.equal(header[3], 'cat');
const knownRows = knownLines.map(line => line.split(','));
assert(knownRows.every(row => row.length >= 4 && row[3] === '1'));
const knownRoots = knownRows.map(row => row[0].toLowerCase());
const knownD4 = d4Set(knownRoots);

const cost72bRoots = cost72b.certificates.map(rootOf);
const cost72bD4 = d4Set(cost72bRoots);
const overlaps = {
  cost74d_vs_prior_win7: intersection(targetD4, priorWinD4),
  cost74d_vs_prior_loss7: intersection(targetD4, priorLossD4),
  cost74d_vs_central_loss7_parent_lift: intersection(targetD4, centralD4),
  cost74d_vs_knownloss_category1: intersection(targetD4, knownD4),
  cost74d_vs_cost72b_win7: intersection(targetD4, cost72bD4),
};
const sourceOverlaps = {
  prior_win7_vs_prior_loss7: intersection(priorWinD4, priorLossD4),
  prior_loss7_vs_central_parent_lift: intersection(priorLossD4, centralD4),
  prior_loss7_vs_knownloss_category1: intersection(priorLossD4, knownD4),
  central_parent_lift_vs_knownloss_category1: intersection(centralD4, knownD4),
};

assert.equal(verified.length, 17);
assert.equal(priorRecords.length, 277);
assert.equal(priorWins.length, 77);
assert.equal(priorLosses.length, 200);
assert.equal(priorWinD4.size, 77);
assert.equal(priorLossD4.size, 200);
assert.equal(centralRoots.length, 274);
assert.equal(centralD4.size, 274);
assert.equal(knownRoots.length, 396);
assert.equal(knownD4.size, 396);
assert.equal(targetD4.size, 15);
assert(Object.values(sourceOverlaps).every(rows => rows.length === 0));
for (const key of Object.keys(overlaps).filter(key => key !== 'cost74d_vs_cost72b_win7')) {
  assert.equal(overlaps[key].length, 0, key);
}
assert.equal(overlaps.cost74d_vs_cost72b_win7.length, 1);

const bit91 = targetRecords.find(row => row.bit === 91);
const bit85 = cost72b.certificates.find(row => row.bit === 85);
assert(bit91 && bit85);
const duplicateCanonical = canonical(bit91.root_hex);
assert.equal(duplicateCanonical, canonical(rootOf(bit85)));
assert.deepEqual(overlaps.cost74d_vs_cost72b_win7, [duplicateCanonical]);

const result = {
  schema: 'n11-cost74d-win-loss-d4-conflict-audit-20261115-v1',
  date: '2026-11-15',
  method: 'Exact 121-bit BigInt D4 canonicalization using the same eight coordinate maps as audit_published_candidates.py; no floating point.',
  inputs: {
    prior_verified_manifests: verified.map(item => ({
      path: 'research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/' + item.name,
      git_blob_sha: item.sha,
      records: item.records.length,
      win7: item.records.filter(row => row.verdict === 'WIN7').length,
      loss7: item.records.filter(row => row.verdict === 'LOSS7').length,
    })),
    cost72b_manifest_git_blob_sha: FIXED.cost72b[1],
    cost74d_manifest_git_blob_sha: FIXED.cost74d[1],
    central_parent_lift_git_blob_sha: FIXED.central[1],
    knownloss_category1_git_blob_sha: FIXED.knownloss[1],
  },
  sources: {
    prior_verified_manifests: {
      count: verified.length,
      records: priorRecords.length,
      win7: priorWins.length,
      loss7: priorLosses.length,
      unique_win7_d4: priorWinD4.size,
      unique_loss7_d4: priorLossD4.size,
    },
    central49_loss7_parent_lift: {
      entries: centralRoots.length,
      unique_d4: centralD4.size,
      interpretation: 'LOSS7-derived parent-lift keys; separate from the 200 direct LOSS7 certificate records.',
    },
    knownloss_category1: {
      rows: knownRoots.length,
      unique_d4: knownD4.size,
      interpretation: 'Candidate classification rows, not independent LOSS7 certificates.',
    },
    source_overlaps: Object.fromEntries(Object.entries(sourceOverlaps).map(([key, rows]) => [key, rows.length])),
  },
  target: {
    child_s6_hex: cost74d.sweep_source.s6_child_hex,
    win7_d10_candidates: targetRecords.length,
    unique_d4_orbits: targetD4.size,
    bits: targetRecords.map(row => row.bit),
    new_d4_orbits_after_cost72b_union: targetD4.size - overlaps.cost74d_vs_cost72b_win7.length,
  },
  overlaps: Object.fromEntries(Object.entries(overlaps).map(([key, rows]) => [key, rows.length])),
  d4_reuse: {
    cost74d_bit: 91,
    cost74d_root_hex: bit91.root_hex,
    cost72b_bit: 85,
    cost72b_root_hex: rootOf(bit85),
    canonical_hex: duplicateCanonical,
    transform: '(x,y)->(x,10-y)',
    action: 'Reuse the cost72b bit85 certificate; do not publish a duplicate bit91 body.',
  },
  interpretation_guard: 'No D4-equivalent conflict was found between the 15 cost74d WIN7 roots and the 200 LOSS7 certificate roots, 274 central49 LOSS7 parent-lift keys, or 396 category-1 candidate rows in these pinned published sources. The only positive overlap is the intended WIN7 reuse cost74d bit91 == cost72b bit85. This is not a scan of every raw cache, private worker cache, or every repository certificate; it does not change S6 frontier counts and does not decide the empty board.',
  unknown_status: {
    standard_11x11_empty_board: 'UNKNOWN',
    two_stone_roots_49_60_59_60: 'UNKNOWN',
    s2_59_60: 'UNKNOWN',
    class2: 'UNKNOWN',
    class4: 'UNKNOWN',
  },
};
await writeFile(resolve(OUT_DIR, 'cost74d-win-loss-conflict-audit-20261115.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify({
  cost74d_win7_roots: targetRecords.length,
  target_d4_orbits: targetD4.size,
  prior_win7: priorWins.length,
  prior_loss7: priorLosses.length,
  central_parent_lift: centralRoots.length,
  category1_candidates: knownRoots.length,
  conflicts: Object.values(overlaps).filter(rows => rows.length > 0).length - 1,
  intended_cost72b_reuse: overlaps.cost74d_vs_cost72b_win7.length,
}, null, 2));
