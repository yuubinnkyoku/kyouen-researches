#!/usr/bin/env node
// Cross-check probe (independent lane instance): run the PUBLISHED engine
// (research/experiments/four-row-q4-m35-neighborhood-hunt-20261121, commit
// cf88217d, sha-pinned) on single-base slices to cross-validate against the
// completed independent run in _q44m35-engine-kit.
//
//   node probe_base.js --board 35 --base 32 --budget 240 --ledger L.jsonl
//
// Per placement, records: witnesses found (verifyConfig-passed), and for the
// R=empty config the uncovered set U (free cells with n3==0) directly from
// the published SearchState invariants. Ledger-resumable by placement key.

'use strict';
const fs = require('fs');
const path = require('path');
const E = { bound: null };

function args() {
  const a = {};
  for (let i = 2; i < process.argv.length; i++) {
    const t = process.argv[i];
    if (t.startsWith('--')) { const k = t.slice(2); const n = process.argv[i + 1]; if (n && !n.startsWith('--')) { a[k] = n; i++; } else a[k] = true; }
  }
  return a;
}

const a = args();
const board = parseInt(a.board, 10);
const baseM = parseInt(a.base, 10);
const budget = parseFloat(a.budget || '240');
const ledger = a.ledger;
// engine root: the published engine dir (cf88217d). Default resolves to the
// sibling experiment directory when this probe is checked out inside
// research/experiments/; override with --engine-root <dir> otherwise.
const ROOT = a['engine-root'] ||
  path.join(__dirname, '..', '..', 'four-row-q4-m35-neighborhood-hunt-20261121');
const { buildCensus, verifyConfig, placementsOfBase, SearchState, explorePlacement } =
  require(path.join(ROOT, 'engine', 'hunt_44.js'));

const alive4 = {};
{
  const t4 = JSON.parse(fs.readFileSync(path.join(ROOT, 'output', 'captable_q4.json'), 'utf8'))['4'];
  for (const k of Object.keys(t4)) alive4[k] = t4[k][1];
}
const alive = { m: board, alive: alive4 };

const wjson = JSON.parse(fs.readFileSync(path.join(ROOT, 'input', 'witnesses_44_m4_34.json'), 'utf8'));
const bases = wjson.witnesses.filter(w => w.m === baseM);
if (bases.length !== 1) { console.error('expected exactly 1 record for m=' + baseM + ', got ' + bases.length); process.exit(1); }
const b = bases[0];
console.log('base m=' + b.m + ' n=' + b.nStones + ' rows=' + JSON.stringify(b.rows));

const tCens = Date.now();
const cens = buildCensus(4, board, 4);
const censusSec = +((Date.now() - tCens) / 1000).toFixed(1);
console.log('census(4,' + board + ',4): total=' + cens.nTotal + ' lines=' + cens.nLines + ' circles=' + cens.nCircles + ' in ' + censusSec + 's');

const pls = placementsOfBase(cens, b.stones);
console.log('placements: ' + pls.length);

const done = new Set();
if (ledger && fs.existsSync(ledger)) {
  for (const line of fs.readFileSync(ledger, 'utf8').split('\n')) {
    if (!line.trim()) continue;
    done.add(JSON.parse(line).key);
  }
}
console.log('resume: ' + done.size + ' done');

const t0 = Date.now();
let stopped = false, witAll = [];
for (const pl of pls) {
  const key = baseM + '#' + pl.key;
  if (done.has(key)) continue;
  if ((Date.now() - t0) / 1000 > budget) { stopped = true; break; }
  const t1 = Date.now();
  // R = empty uncovered set straight from SearchState invariants
  const st0 = new SearchState(cens);
  for (const p of pl.idxs) st0.addStone(p);
  const U0set = [];
  for (let i = 0; i < cens.N; i++) if (st0.freeMask[i] && st0.n3[i] === 0) U0set.push(i);
  const U0cells = U0set.map(idx => [idx % cens.m, (idx / cens.m) | 0]);
  // full bounded-neighborhood exploration
  const st = new SearchState(cens);
  for (const p of pl.idxs) st.addStone(p);
  const r = explorePlacement(cens, alive, st, { maxAdd: 2 });
  const rec = {
    key, base: baseM, g: pl.g, tx: pl.tx, ty: pl.ty,
    U0: U0set.length, U0cells,
    witnesses: r.witnesses.length,
    witStones: r.witnesses.map(x => x.stones),
    rConfigs: r.rConfigs, sumU: r.sumU, maxU: r.maxU,
    d1Dead: r.d1Dead, d2Dead: r.d2Dead,
    singles: r.singleCandidates, pairs: r.pairCandidates,
    sec: +((Date.now() - t1) / 1000).toFixed(3)
  };
  if (ledger) fs.appendFileSync(ledger, JSON.stringify(rec) + '\n');
  done.add(key);
  witAll = witAll.concat(r.witnesses.map(x => x.stones));
  console.log('base=' + baseM + ' g=' + pl.g + ' tx=' + pl.tx + ' ty=' + pl.ty +
    ' U0=' + U0set.length + ' cells=' + JSON.stringify(U0cells) +
    ' wit=' + r.witnesses.length + ' rCfg=' + r.rConfigs +
    ' sec=' + rec.sec + (r.witnesses.length ? ' STONES=' + JSON.stringify(rec.witStones) : ''));
}
console.log('PROBE SUMMARY board=' + board + ' base=' + baseM +
  ' placements=' + pls.length + ' done=' + done.size + ' witnesses=' + witAll.length +
  ' stoppedAtBudget=' + stopped + ' censusSec=' + censusSec +
  ' runSec=' + +((Date.now() - t0) / 1000).toFixed(1));
