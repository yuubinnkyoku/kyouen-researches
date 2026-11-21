#!/usr/bin/env node
// Driver for the (4,4) m=35/36 bounded-neighborhood witness hunt (part 2 of
// the four-row q4 m35 witness-hunt-counting lane). Modes:
//
//   node engine/hunt_driver.js --census-anchors
//       rebuild the 8 pinned curve censuses from first principles and compare
//       them to input/pin_census4_check_output.txt (fail-closed: any mismatch
//       exits 1).
//
//   node engine/hunt_driver.js --verify-published
//       re-verify every published (4,4) def-mode witness m=4..34 (schema
//       safety, maximality, deficiency, rows, capped class alive, m <= B).
//
//   node engine/hunt_driver.js --battery --board 10 --bases 9,8 --placements 8
//       layered-vs-brute: for each chosen witness-base placement, enumerate
//       the bounded neighborhood twice -- once with the layered engine
//       (helper pools, votes, gates), once with a plain brute-force over all
//       removal subsets |R|<=2 x all addition subsets |A|<=2 -- and require
//       the witness SETS to be identical. Exit 1 on any DIFF.
//
//   node engine/hunt_driver.js --board 35 --base-min 4 \
//        --budget-seconds 240 --ledger output/hunt_m35.jsonl
//       the hunt itself: placements of all published witness bases into the
//       4 x board board, ledger-resumable, stopping cleanly at the budget.
//
// Nothing in this driver claims witness absence at any m: a completed
// negative run is a record of which finite bounded neighborhoods yielded no
// witness, and every witness candidate that appears is verified by
// verifyConfig (independent exact integer geometry) before being reported.

'use strict';
const fs = require('fs');
const path = require('path');
const E = require(path.join(__dirname, 'hunt_44.js'));
const { buildCensus, verifyConfig, placementsOfBase, SearchState, explorePlacement } = E;

function args() {
  const a = { _: [] };
  for (let i = 2; i < process.argv.length; i++) {
    const t = process.argv[i];
    if (t.startsWith('--')) {
      const key = t.slice(2);
      const next = process.argv[i + 1];
      if (next !== undefined && !next.startsWith('--')) { a[key] = next; i++; }
      else a[key] = true;
    } else a._.push(t);
  }
  return a;
}

function loadCaptable(p) {
  const t4 = JSON.parse(fs.readFileSync(p, 'utf8'))['4'];
  const alive = {};
  for (const k of Object.keys(t4)) alive[k] = t4[k][1]; // [caps, B] -> B
  return alive;
}

function cappedKeyOf(rows) {
  return '(' + rows.map(r => Math.min(3, r)).sort((x, y) => x - y).join(', ') + ')';
}

// ---------- mode: census anchors ------------------------------------------
function modeCensusAnchors(alive4) {
  const pin = fs.readFileSync(path.join(__dirname, '..', 'input', 'pin_census4_check_output.txt'), 'utf8')
    .split('\n').filter(x => x.trim()).map(x => JSON.parse(x));
  let pass = 0, fail = 0;
  for (const c of pin) {
    if (c.event === 'summary') {
      const ok = (pass === c.nCases) && fail === 0;
      console.log(`SUMMARY ${pass}/${c.nCases} PASS, allPass=${ok}`);
      process.exit(ok ? 0 : 1);
    }
    const t0 = Date.now();
    const cens = buildCensus(c.w, c.m, c.q);
    const total = cens.nTotal, lines = cens.nLines, circles = cens.nCircles;
    const expLines = c.satCurves - c.c4Circles;
    const ok = total === c.satCurves && circles === c.c4Circles &&
      lines === expLines && c.satCurves === c.c4Curves;
    if (ok) pass++; else fail++;
    console.log(`(${c.w},${c.m},${c.q}) total=${total} lines=${lines} circles=${circles}` +
      ` | pin sat=${c.satCurves} circles=${c.c4Circles} | ${ok ? 'PASS' : 'FAIL'} (${((Date.now() - t0) / 1000).toFixed(1)}s)`);
  }
}

// ---------- mode: verify published witnesses -------------------------------
function modeVerifyPublished(alive4) {
  const wj = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'input', 'witnesses_44_m4_34.json'), 'utf8'));
  const ws = wj.witnesses;
  let pass = 0, fail = 0;
  const censusCache = new Map();
  const censOf = (m) => {
    if (!censusCache.has(m)) censusCache.set(m, buildCensus(4, m, 4));
    return censusCache.get(m);
  };
  for (const wst of ws) {
    const m = wst.m;
    const cens = censOf(m);
    const idxs = wst.stones.map(([x, y]) => y * m + x);
    const v = verifyConfig(cens, idxs);
    const rowsOK = JSON.stringify(v.rows.slice().sort((a, b) => a - b)) === JSON.stringify(wst.rows.slice().sort((a, b) => a - b));
    const nOK = v.n === wst.nStones;
    const ck = cappedKeyOf(v.rows);
    const B = alive4[ck];
    const classOK = B !== undefined && B >= m;
    const ok = v.ok && v.safe && v.maximal && v.deficient && rowsOK && nOK && classOK;
    if (ok) pass++; else fail++;
    if (!ok || process.env.VERBOSE) {
      console.log(`m=${m} safe=${v.safe} max=${v.maximal} def=${v.deficient} rowsOK=${rowsOK} nOK=${nOK} class=${ck} B=${B} classOK=${classOK} -> ${ok ? 'PASS' : 'FAIL'}`);
    }
  }
  console.log(`verify-published: ${pass}/${ws.length} PASS, ${fail} FAIL`);
  process.exit(fail === 0 ? 0 : 1);
}

// ---------- brute force (battery ground truth) ------------------------------
function bruteNeighborhood(census, alive, baseIdxs) {
  const { q } = census;
  const boardM = census.m;
  const classAliveRows = (rowsNow) => {
    const B = alive[cappedKeyOf(rowsNow)];
    return B !== undefined && B >= boardM && rowsNow.some(r => r <= 2);
  };
  const N = census.N;
  const res = { configs: 0, witnessKeys: new Set() };
  const base = baseIdxs.slice().sort((a, b) => a - b);
  const removalSets = [[]];
  for (let i = 0; i < base.length; i++) {
    removalSets.push([base[i]]);
    for (let j = i + 1; j < base.length; j++) removalSets.push([base[i], base[j]]);
  }
  for (const R of removalSets) {
    const stones = base.filter(p => !R.includes(p));
    const stoneSet = new Set(stones);
    const free = [];
    for (let p = 0; p < N; p++) if (!stoneSet.has(p)) free.push(p);
    // |A| = 0
    res.configs++;
    {
      const v = verifyConfig(census, stones);
      if (v.any && classAliveRows(v.rows)) res.witnessKeys.add(stones.join(','));
    }
    for (const a of free) {
      res.configs++;
      const st = stones.concat([a]).sort((x, y) => x - y);
      const v = verifyConfig(census, st);
      if (v.any && classAliveRows(v.rows)) res.witnessKeys.add(st.join(','));
    }
    for (let i = 0; i < free.length; i++) {
      for (let j = i + 1; j < free.length; j++) {
        res.configs++;
        const st = stones.concat([free[i], free[j]]).sort((x, y) => x - y);
        const v = verifyConfig(census, st);
        if (v.any && classAliveRows(v.rows)) res.witnessKeys.add(st.join(','));
      }
    }
  }
  return res;
}

// ---------- mode: battery (layered vs brute) -------------------------------
function modeBattery(a, alive4) {
  const board = parseInt(a.board || '10', 10);
  const basesReq = (a.bases || '9,8').split(',').map(x => parseInt(x, 10));
  const maxPlacements = parseInt(a.placements || '4', 10);
  const wj = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'input', 'witnesses_44_m4_34.json'), 'utf8'));
  console.log(`battery: board=4x${board} bases=[${basesReq}] placements<=${maxPlacements}`);
  const tC = Date.now();
  const cens = buildCensus(4, board, 4);
  console.log(`census (4,${board},4): ${cens.nTotal} curves = ${cens.nLines} lines + ${cens.nCircles} circles (${((Date.now() - tC) / 1000).toFixed(1)}s)`);
  const alive = { m: board, alive: alive4 };
  let done = 0, equiv = 0, diffs = 0;
  outer:
  for (const bm of basesReq) {
    const wst = wj.witnesses.find(w => w.m === bm);
    if (!wst) { console.log(`base m=${bm}: NOT FOUND`); process.exit(1); }
    const pls = placementsOfBase(cens, wst.stones);
    console.log(`base m=${bm} (${wst.nStones} stones): ${pls.length} placements in 4x${board}`);
    for (let pi = 0; pi < pls.length; pi++) {
      if (done >= maxPlacements) break outer;
      const pl = pls[pi];
      done++;
      const t1 = Date.now();
      const st = new SearchState(cens);
      for (const p of pl.idxs) st.addStone(p);
      const layer = explorePlacement(cens, alive, st, { maxAdd: 2 });
      const layerKeys = new Set(layer.witnesses.map(w => w.stones.join(',')));
      const brute = bruteNeighborhood(cens, alive4, pl.idxs);
      const same = layerKeys.size === brute.witnessKeys.size &&
        [...layerKeys].every(k => brute.witnessKeys.has(k));
      if (same) equiv++; else diffs++;
      console.log(`  pl#${pi} g=${pl.g} tx=${pl.tx} ty=${pl.ty}: layered ${layerKeys.size} / brute ${brute.witnessKeys.size} witnesses, brute ${brute.configs} configs, rCfg=${layer.rConfigs} -> ${same ? 'EQUIV' : 'DIFF !!!'} (${((Date.now() - t1) / 1000).toFixed(1)}s)`);
      if (!same) {
        for (const k of layerKeys) if (!brute.witnessKeys.has(k)) console.log(`    layered-only: ${k}`);
        for (const k of brute.witnessKeys) if (!layerKeys.has(k)) console.log(`    brute-only:   ${k}`);
      }
    }
  }
  console.log(`battery result: ${done} placements, EQUIV ${equiv}, DIFF ${diffs} -> ${diffs === 0 && done > 0 ? 'ALL EQUIV' : 'FAILURE'}`);
  process.exit(diffs === 0 && done > 0 ? 0 : 1);
}

// ---------- mode: hunt ------------------------------------------------------
function modeHunt(a, alive4) {
  const board = parseInt(a.board || '35', 10);
  const baseMin = parseInt(a['base-min'] || '4', 10);
  const budget = parseFloat(a['budget-seconds'] || '240');
  const ledger = a.ledger || a.file || path.join(__dirname, '..', 'output', `hunt_m${board}.jsonl`);
  const wj = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'input', 'witnesses_44_m4_34.json'), 'utf8'));
  // dedup bases by normalized stone set (m=29,31,33 duplicate 28,30,32)
  const seenBases = new Map();
  for (const w of wj.witnesses) {
    const key = w.stones.map(s => s.join(',')).sort().join(';');
    if (!seenBases.has(key)) seenBases.set(key, w);
    else if (w.m !== seenBases.get(key).m) {
      // same stones, smaller board is the canonical published witness
      if (w.m < seenBases.get(key).m) seenBases.set(key, w);
    }
  }
  const bases = [...seenBases.values()].filter(w => w.m >= baseMin).sort((x, y) => x.m - y.m);
  console.log(`hunt: board=4x${board} base-min=${baseMin} budget=${budget}s ledger=${ledger}`);
  console.log(`bases: ${bases.length} (of ${wj.witnesses.length} published, dedup by stone set), m=[${bases.map(b => b.m).join(',')}]`);
  const tC = Date.now();
  const cens = buildCensus(4, board, 4);
  const censusSec = (Date.now() - tC) / 1000;
  console.log(`census (4,${board},4): ${cens.nTotal} curves = ${cens.nLines} lines + ${cens.nCircles} circles (${censusSec.toFixed(1)}s)`);
  const alive = { m: board, alive: alive4 };
  // build task list
  const tasks = [];
  for (const b of bases) {
    const pls = placementsOfBase(cens, b.stones);
    for (let pi = 0; pi < pls.length; pi++) {
      tasks.push({ base: b.m, nStones: b.nStones, pi, pl: pls[pi], key: b.m + '#' + pls[pi].key });
    }
  }
  console.log(`placements planned: ${tasks.length}`);
  const done = new Set();
  if (fs.existsSync(ledger)) {
    for (const line of fs.readFileSync(ledger, 'utf8').split('\n')) {
      if (!line.trim()) continue;
      try { done.add(JSON.parse(line).key); } catch (e) { console.error('ledger parse error, abort to avoid gaps'); process.exit(1); }
    }
  }
  console.log(`ledger resume: ${done.size} already done`);
  const t0 = Date.now();
  let proc = 0, witTotal = 0, wit = [];
  let rCfg = 0, sumU = 0, maxU = 0, d1 = 0, d2 = 0, singles = 0, pairs = 0;
  let stopped = false;
  for (const t of tasks) {
    if (done.has(t.key)) continue;
    if ((Date.now() - t0) / 1000 > budget) { stopped = true; break; }
    const t1 = Date.now();
    const st = new SearchState(cens);
    for (const p of t.pl.idxs) st.addStone(p);
    const r = explorePlacement(cens, alive, st, { maxAdd: 2 });
    proc++; rCfg += r.rConfigs; sumU += r.sumU; if (r.maxU > maxU) maxU = r.maxU;
    d1 += r.d1Dead; d2 += r.d2Dead; singles += r.singleCandidates; pairs += r.pairCandidates;
    witTotal += r.witnesses.length;
    const rec = {
      key: t.key, base: t.base, g: t.pl.g, tx: t.pl.tx, ty: t.pl.ty,
      witnesses: r.witnesses.length,
      witStones: r.witnesses.map(x => x.stones),
      rConfigs: r.rConfigs, sumU: r.sumU, maxU: r.maxU,
      d1Dead: r.d1Dead, d2Dead: r.d2Dead, singles: r.singleCandidates, pairs: r.pairCandidates,
      sec: +((Date.now() - t1) / 1000).toFixed(3)
    };
    fs.appendFileSync(ledger, JSON.stringify(rec) + '\n');
    done.add(t.key);
    if (r.witnesses.length > 0) wit = wit.concat(r.witnesses.map(x => x.stones));
    if (proc % 50 === 0) {
      console.error(`  progress: processed ${proc} this run, ${done.size}/${tasks.length} total, witnesses ${witTotal}, elapsed ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
  }
  const summary = {
    board, baseMin, planned: tasks.length, doneTotal: done.size, processedThisRun: proc,
    witnesses: witTotal, rCfgTotal: rCfg, sumU, maxU, d1Dead: d1, d2Dead: d2,
    singleCandidates: singles, pairCandidates: pairs,
    censusSec: +censusSec.toFixed(1), runSec: +((Date.now() - t0) / 1000).toFixed(1),
    stoppedAtBudget: stopped, ledger
  };
  console.log('SUMMARY ' + JSON.stringify(summary));
  if (wit.length > 0) {
    console.log('WITNESSES FOUND (all verifyConfig-passed):');
    for (const stones of wit) console.log('  ' + JSON.stringify(stones));
  }
}

// ---------- dispatch ---------------------------------------------------------
(function main() {
  const a = args();
  const capPath = a.captable || path.join(__dirname, '..', 'output', 'captable_q4.json');
  const alive4 = loadCaptable(capPath);
  if (a['census-anchors']) { modeCensusAnchors(alive4); return; }
  if (a['verify-published']) { modeVerifyPublished(alive4); return; }
  if (a.battery) { modeBattery(a, alive4); return; }
  modeHunt(a, alive4);
})();
