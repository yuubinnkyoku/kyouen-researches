#!/usr/bin/env node
// dfsr.js — deepest-open-leaf-first closure driver over a chunker.js partition state.
//
// Same record schema, same sound prefix-partition semantics, and the same audit walk as
// the pinned chunker.js (blob addab28282fb…). Differences from chunker.js --mode=run:
//   * work order: instead of FIFO/BFS over the queue, each step re-walks the partition
//     tree (exactly the chunker --mode=audit walk), collects open prefixes (reachable,
//     no record yet), and picks the DEEPEST open prefix (tie-break: lexicographic) first.
//     Rationale: capped internal chunks are finished by closing their children; chasing
//     the deepest open prefix converts search work into settled (uncapped) leaf records
//     at the highest rate and never introduces a chunk order the audit depends on
//     (records are append-only and order-agnostic; completeness is chunker-audit-decided).
//   * --wall defaults to effectively unbounded (background marathon use); a fresh chunk
//     always gets --maxsec=CAP (recorded in r.cap, same as chunker.js).
// Chunks themselves are run by the pinned ksearchp.js (blob 66938de2b6…) unchanged;
// this file only schedules them. No verdict is ever taken from a capped record
// (identical honesty rule as chunker.js).
//
// Usage:
//   node dfsr.js --mode=run   --n=9 --target=19 --cap=200 --wall=100000 --state=records.jsonl
//   node dfsr.js --mode=audit --n=9 --target=19 --state=records.jsonl   (identical to chunker audit)
'use strict';
const fs = require('fs');
const { execFile } = require('child_process');

const OPT = {};
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (a.startsWith('--')) { const eq = a.indexOf('='); OPT[a.slice(2, eq)] = a.slice(eq + 1); }
}
const N = parseInt(OPT.n || '9', 10);
const TARGET = parseInt(OPT.target, 10);
const MODE = OPT.mode || 'run';
const CAP = OPT.cap ? parseFloat(OPT.cap) : 200;
const WALL = OPT.wall ? parseFloat(OPT.wall) : 100000;
const STATE = OPT.state || `chunks/n${N}t${TARGET}.jsonl`;
const SCRIPT = OPT.script || 'scripts/ksearchp.js';
const NCELL = N * N;

const key = (P) => P.join(',');
const childUB = (m) => NCELL + m - TARGET; // inclusive; children d in [pm+1, childUB(m)]
function children(P) {
  const m = P.length;
  const pm = P[m - 1];
  if (m + 1 > TARGET) return [];
  const out = [];
  for (let d = pm + 1; d <= childUB(m); d++) out.push(P.concat([d]));
  return out;
}
function loadRecords() {
  const map = new Map();
  if (!fs.existsSync(STATE)) return map;
  const txt = fs.readFileSync(STATE, 'utf8');
  for (const line of txt.split('\n')) {
    const t = line.trim();
    if (!t) continue;
    try {
      const r = JSON.parse(t);
      if (!Array.isArray(r.prefix)) continue;
      map.set(key(r.prefix), r); // last-wins, same as chunker.js
    } catch (e) { /* tolerate torn tail line from a killed process */ }
  }
  return map;
}

// audit walk (identical semantics to chunker.js --mode=audit)
function walk(recs) {
  let leaves = 0, nodes = 0, cappedInternal = 0, open = [], satRecords = [], bad = [];
  const visit = (P) => {
    const m = P.length;
    if (m > TARGET) return;
    const rec = recs.get(key(P));
    if (m === TARGET) {
      if (!rec) { open.push(P); return; }
      if (rec.capped) { bad.push('capped m==t leaf ' + key(P)); return; }
      nodes += rec.nodes || 0; leaves++;
      if (rec.sat === true) satRecords.push(key(P));
      return;
    }
    if (!rec) { open.push(P); return; }
    if (!rec.capped) {
      nodes += rec.nodes || 0; leaves++;
      if (rec.sat === true) satRecords.push(key(P));
      return;
    }
    cappedInternal++;
    for (const ch of children(P)) visit(ch);
  };
  for (let c = 0; c <= NCELL - TARGET; c++) visit([c]);
  return { leaves, nodes, cappedInternal, open, satRecords, bad };
}

function runChunk(P, maxsec) {
  return new Promise((resolve, reject) => {
    execFile('node', [SCRIPT, `--n=${N}`, `--target=${TARGET}`, `--prefix=${key(P)}`, `--maxsec=${maxsec}`],
      { maxBuffer: 1 << 24 }, (err, stdout, stderr) => {
      if (err && !stdout) { reject(new Error('ksearchp failed: ' + stderr)); return; }
      try {
        const r = JSON.parse(stdout.trim().split('\n').pop());
        if (r.n !== N || r.target !== TARGET || key(r.prefix) !== key(P)) {
          reject(new Error('chunk identity mismatch: ' + JSON.stringify(r).slice(0, 300)));
          return;
        }
        resolve(r);
      } catch (e) { reject(e); }
    });
  });
}

const lexLess = (a, b) => {
  for (let i = 0; i < Math.min(a.length, b.length); i++) if (a[i] !== b[i]) return a[i] < b[i];
  return a.length < b.length;
};

async function run() {
  const fd = fs.openSync(STATE, 'a');
  const deadline = Date.now() + WALL * 1000;
  let runs = 0, stats = walk(loadRecords());
  fs.writeSync(fd, ''); // append-mode noop, open handle
  while (true) {
    const recs = loadRecords();
    stats = walk(recs);
    if (stats.bad.length > 0) {
      console.log(JSON.stringify({ mode: 'dfs-run', fatal: 'bad-records', bad: stats.bad }));
      break;
    }
    if (stats.satRecords.length > 0) {
      const satKey = stats.satRecords[0];
      console.log(JSON.stringify({ mode: 'dfs-run', sat: satKey, note: 'STOP — independent verification required before any claim' }));
      break;
    }
    if (stats.open.length === 0) {
      console.log(JSON.stringify({ mode: 'dfs-run', complete: true, all_unsat: true,
        settled_leaves: stats.leaves, nodes_total: stats.nodes }));
      break;
    }
    if (Date.now() > deadline) {
      console.log(JSON.stringify({ mode: 'dfs-run', stopped: 'wall', runs_this_process: runs,
        settled_leaves: stats.leaves, nodes_total: stats.nodes, open_leaves: stats.open.length }));
      break;
    }
    // deepest open prefix, tie-break lexicographic (deterministic)
    let best = null;
    for (const P of stats.open) {
      if (!best) best = P;
      else if (P.length > best.length) best = P;
      else if (P.length === best.length && lexLess(P, best)) best = P;
    }
    const remainMs = deadline - Date.now();
    const maxsec = Math.min(CAP, Math.max(15, remainMs / 1000 - 3));
    let r;
    try { r = await runChunk(best, maxsec); } catch (e) {
      console.log(JSON.stringify({ mode: 'dfs-run', error: String(e.message || e), at: key(best) }));
      break;
    }
    runs++;
    r.cap = maxsec;
    fs.writeSync(fd, JSON.stringify(r) + '\n');
    console.log(JSON.stringify({ mode: 'dfs-step', ran: key(r.prefix), m: r.prefix.length,
      capped: !!r.capped, sat: r.sat === undefined ? null : r.sat, nodes: r.nodes, ms: r.ms,
      settled_leaves: stats.leaves }));
  }
  fs.closeSync(fd);
}

if (MODE === 'audit') { const s = walk(loadRecords()); console.log(JSON.stringify({ mode: 'audit', n: N, target: TARGET, state: STATE, complete: s.open.length === 0 && s.bad.length === 0, all_unsat: s.open.length === 0 && s.bad.length === 0 && s.satRecords.length === 0, settled_leaves: s.leaves, capped_internal_nodes: s.cappedInternal, open_leaves: s.open.length, open_examples: s.open.slice(0, 5), sat_records: s.satRecords, bad: s.bad, nodes_total: s.nodes })); }
else run();
