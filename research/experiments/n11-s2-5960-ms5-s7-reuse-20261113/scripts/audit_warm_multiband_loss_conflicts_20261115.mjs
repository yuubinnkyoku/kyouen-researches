#!/usr/bin/env node
import assert from 'node:assert/strict';
import { readFile, readdir, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const EXP_DIR = resolve(SCRIPT_DIR, '..');
const OUT_DIR = resolve(EXP_DIR, 'output');
const EXPERIMENTS_DIR = resolve(EXP_DIR, '..');
const CENTRAL_PATH = resolve(EXPERIMENTS_DIR, 'n11-central-19-cover-20261031', 'terminal_loss7_parent_lift_274_manifest.json');

const readText = p => readFile(p, 'utf8');
const parseJSON = async p => JSON.parse(await readText(p));

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
const canonical = mask => images(mask).map(x => x.toString(16).padStart(32,'0')).sort()[0];
const d4Set = roots => new Set(roots.map(x => canonical(BigInt('0x'+x))));
const intersection = (a,b) => [...a].filter(x => b.has(x));
const uniqueCount = xs => new Set(xs).size;
const popcount = hex => {
  let n = BigInt('0x'+hex), c = 0;
  while (n) { n &= n-1n; c++; }
  return c;
};

const warmDoc = await parseJSON(resolve(OUT_DIR, 'class2-lane-warm-multiband-certificates-20261115.json'));
const warmRoots = warmDoc.records.map(r => r.root_hex.toLowerCase());
const manifestNames = (await readdir(OUT_DIR)).filter(n => n.endsWith('-verified.json')).sort();
assert.equal(manifestNames.length, 17, 'verified-manifest snapshot changed; review before updating this audit');
const manifests = [];
for (const name of manifestNames) {
  const doc = await parseJSON(resolve(OUT_DIR, name));
  const records = (doc.certificates || []).map(r => ({root:(r.root || r.root_hex).toLowerCase(), verdict:r.verdict}));
  assert(records.every(r => /^[0-9a-f]{32}$/.test(r.root)));
  manifests.push({name, records});
}
const priorWins = manifests.flatMap(m => m.records.filter(r => r.verdict === 'WIN7').map(r => r.root));
const priorLosses = manifests.flatMap(m => m.records.filter(r => r.verdict === 'LOSS7').map(r => r.root));

const centralDoc = await parseJSON(CENTRAL_PATH);
const centralRoots = centralDoc.combined_terminal_loss7_keys.map(x => x.toLowerCase());
const knownText = await readText(resolve(OUT_DIR, 'ms5_s7_knownloss_candidates.csv'));
const knownLines = knownText.trimEnd().split(/\\r?\\n/);
const header = knownLines.shift().split(',');
assert.equal(header[0], 's7_hex');
assert.equal(header[3], 'cat');
const knownRows = knownLines.map(line => line.split(','));
assert(knownRows.every(r => r.length >= 4 && r[3] === '1'));
const knownRoots = knownRows.map(r => r[0].toLowerCase());

assert.equal(warmRoots.length, 35);
assert.equal(uniqueCount(warmRoots), 35);
assert.equal(new Set(warmRoots.map(popcount)).size, 1);
assert.equal(popcount(warmRoots[0]), 7);
assert.equal(manifests.length, 17);
assert.equal(manifests.reduce((n,m)=>n+m.records.length,0), 277);
assert.equal(priorWins.length, 77);
assert.equal(priorLosses.length, 200);
assert.equal(uniqueCount(priorWins), 77);
assert.equal(uniqueCount(priorLosses), 200);
assert.equal(centralRoots.length, 274);
assert.equal(uniqueCount(centralRoots), 274);
assert.equal(knownRoots.length, 396);
assert.equal(uniqueCount(knownRoots), 396);

const warmD4 = d4Set(warmRoots);
const winD4 = d4Set(priorWins);
const lossD4 = d4Set(priorLosses);
const centralD4 = d4Set(centralRoots);
const knownD4 = d4Set(knownRoots);
const sourceOverlaps = {
  prior_win7_vs_prior_loss7: intersection(winD4,lossD4).length,
  prior_loss7_vs_central_parent_lift: intersection(lossD4,centralD4).length,
  prior_loss7_vs_knownloss_candidates: intersection(lossD4,knownD4).length,
  central_parent_lift_vs_knownloss_candidates: intersection(centralD4,knownD4).length,
};
const conflicts = {
  warm_vs_prior_win7_d4: intersection(warmD4,winD4),
  warm_vs_prior_loss7_d4: intersection(warmD4,lossD4),
  warm_vs_central_parent_lift_d4: intersection(warmD4,centralD4),
  warm_vs_knownloss_category1_d4: intersection(warmD4,knownD4),
};
assert(Object.values(sourceOverlaps).every(x=>x===0));
assert(Object.values(conflicts).every(x=>x.length===0));

const result = {
  schema:'n11-warm-multiband-win-loss-conflict-audit-20261115-v1',
  method:'D4 canonicalization using the same eight coordinate images as audit_published_candidates.py; exact integer bitmasks, no floating point',
  warm_multiband:{records:warmRoots.length,unique_roots:uniqueCount(warmRoots),unique_d4_orbits:warmD4.size,stone_counts:[7]},
  prior_verified_manifests:{
    manifest_count:manifests.length,record_count:manifests.reduce((n,m)=>n+m.records.length,0),
    win7_records:priorWins.length,loss7_records:priorLosses.length,
    unique_win7_d4_orbits:winD4.size,unique_loss7_d4_orbits:lossD4.size,
    manifest_names:manifestNames,
  },
  additional_loss_sources:{
    central49_parent_lift:{entries:centralRoots.length,unique_d4_orbits:centralD4.size},
    knownloss_category1_candidate_pool:{rows:knownRoots.length,unique_d4_orbits:knownD4.size,interpretation:'candidate rows, not independent LOSS7 certificates'},
    combined_unique_d4_orbits:new Set([...lossD4,...centralD4,...knownD4]).size,
    cross_source_d4_overlaps:sourceOverlaps,
  },
  conflicts:{...Object.fromEntries(Object.entries(conflicts).map(([k,v])=>[k,v.length])),total:0},
  interpretation_guard:'Bounded audit of published manifests and the category-1 candidate index only; not every raw cache or private worker cache. No frontier count or game outcome is changed.',
};
await writeFile(resolve(OUT_DIR, 'warm-multiband-loss-conflict-audit-20261115.json'), JSON.stringify(result,null,2)+'\\n');
console.log(JSON.stringify({warm:35,priorWin7:77,priorLoss7:200,centralParentLift:274,knownlossCategory1:396,conflicts:0},null,2));
