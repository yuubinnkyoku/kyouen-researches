#!/usr/bin/env node
// chunker.js — adaptive prefix-chunk driver for ksearchp.js (ksearch v3d) with a durable
// append-only record file (resume across processes/hosts) and a completeness audit mode.
//
// Method (declaration n9-ge19 lane, resume step 4): partition the search space by the
// m smallest chosen cells ("prefix" chunks), run ksearchp per chunk with an honest cap,
// and expand capped chunks into their children (a full, sound, disjoint partition of the
// parent's space — see ksearchp.js header). Chunks are never counted unless uncapped.
//
// Usage:
//   node chunker.js --mode=run   --n=8 --target=16 --cap=120 --wall=265 --state=chunks/n8t16.jsonl
//   node chunker.js --mode=audit --n=8 --target=16 --state=chunks/n8t16.jsonl
// Audit: walks the chunk tree implied by the records; PASS requires every feasible leaf to
// have an uncapped record, no record sat=true, and consistent bookkeeping.
// Deterministic traversal (FIFO frontier ascending d). No randomness.
'use strict';
const fs = require('fs');
const { execFile } = require('child_process');

const OPT = {};
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (a.startsWith('--')) { const eq = a.indexOf('='); OPT[a.slice(2, eq)] = a.slice(eq + 1); }
}
const N = parseInt(OPT.n || '8', 10);
const TARGET = parseInt(OPT.target, 10);
const MODE = OPT.mode || 'run';
const CAP = OPT.cap ? parseFloat(OPT.cap) : 120;
const WALL = OPT.wall ? parseFloat(OPT.wall) : 265;
const STATE = OPT.state || `chunks/n${N}t${TARGET}.jsonl`;
const SCRIPT = OPT.script || 'scripts/ksearchp.js';
const NCELL = N * N;

const key = (P) => P.join(',');
// child upper bound: after fixing P+[d] (|P|=m), need TARGET-m-1 more cells above d
const childUB = (m) => NCELL + m - TARGET; // inclusive; children d in [pm+1, childUB(m)]
function children(P) {
  const m = P.length;
  const pm = P[m - 1];
  const out = [];
  if (m + 1 > TARGET) return out; // m==TARGET: P is a leaf chunk, no children
  const ub = childUB(m);
  for (let d = pm + 1; d <= ub; d++) out.push(P.concat([d]));
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
      map.set(key(r.prefix), r);
    } catch (e) { /* tolerate torn tail line from a killed process */ }
  }
  return map;
}
function appendRecord(fd, r) { fs.writeSync(fd, JSON.stringify(r) + '\n'); }

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

async function run() {
  const recs = loadRecords();
  const fd = fs.openSync(STATE, 'a');
  const deadline = Date.now() + WALL * 1000;
  let settledUnsat = 0, runs = 0, expanded = 0;
  for (const [, r] of recs) if (!r.capped && r.sat === false) settledUnsat++;
  const queue = [];
  // root is always expanded (never run whole); its children are the min(S) chunks
  for (let c = 0; c <= NCELL - TARGET; c++) queue.push([c]);
  let satHit = null, budgetStop = false;
  // skip enqueueing chunks already settled or already expanded (capped with children progressed)
  function statusOf(rec) { return !rec ? 'none' : (rec.capped ? 'capped' : (rec.sat ? 'SAT' : 'done')); }
  while (queue.length) {
    const P = queue.shift();
    const rec = recs.get(key(P));
    const st = statusOf(rec);
    if (st === 'done') continue;
    if (st === 'SAT') { satHit = rec; break; }
    if (st === 'capped') { for (const ch of children(P)) queue.push(ch); expanded++; continue; }
    // fresh chunk
    const remainMs = deadline - Date.now();
    if (remainMs < 20000) { budgetStop = true; queue.unshift(P); break; }
    const maxsec = Math.min(CAP, Math.max(15, remainMs / 1000 - 3));
    let r;
    try { r = await runChunk(P, maxsec); } catch (e) { fs.closeSync(fd); console.log(JSON.stringify({ mode: 'run', error: String(e.message || e), at: key(P) })); return; }
    runs++;
    r.cap = maxsec;
    if (r.sat === true && r.witness) r.witness_verified = false;
    appendRecord(fd, r);
    recs.set(key(P), r);
    settledUnsat += (!r.capped && r.sat === false) ? 1 : 0;
    if (r.sat === true) { satHit = r; break; }
    if (r.capped) { for (const ch of children(P)) queue.push(ch); expanded++; }
  }
  fs.closeSync(fd);
  const out = {
    mode: 'run', n: N, target: TARGET, state: STATE, wall: WALL, cap: CAP,
    runs_this_call: runs, expanded_this_call: expanded,
    settled_unsat_records: settledUnsat,
    sat: satHit ? satHit.witness : null,
    stopped: budgetStop ? 'budget' : (satHit ? 'sat' : 'exhausted'),
    ts: new Date().toISOString(),
  };
  console.log(JSON.stringify(out));
}

function audit() {
  const recs = loadRecords();
  let leaves = 0, nodes = 0, cappedInternal = 0, satRecords = [], openLeaves = [], bad = [];
  const visit = (P) => {
    const m = P.length;
    if (m > TARGET) return; // infeasible branch by counting bound (never enumerated, guard)
    const rec = recs.get(key(P));
    if (m === TARGET) {
      // leaf chunk: space = {P} exactly (chosen set == P); requires an uncapped record
      if (!rec) { openLeaves.push(key(P)); return; }
      if (rec.capped) { bad.push('capped m==t leaf ' + key(P)); return; }
      nodes += rec.nodes || 0; leaves++;
      if (rec.sat === true) satRecords.push(key(P));
      return;
    }
    if (!rec) { openLeaves.push(key(P)); return; }
    if (!rec.capped) {
      // settled internal chunk: complete search over its space, verdict authoritative
      nodes += rec.nodes || 0; leaves++;
      if (rec.sat === true) satRecords.push(key(P));
      return;
    }
    cappedInternal++;
    // capped internal: partition coverage comes from children over the FULL feasible range
    for (const ch of children(P)) visit(ch);
  };
  // root = whole space; expanded always into min(S) chunks c=0..NCELL-TARGET;
  // c beyond that bound is infeasible (fewer than TARGET cells remain by counting).
  const rootPassed = [];
  for (let c = 0; c <= NCELL - TARGET; c++) { rootPassed.push(1); visit([c]); }
  const complete = openLeaves.length === 0 && bad.length === 0;
  const out = {
    mode: 'audit', n: N, target: TARGET, state: STATE,
    complete, all_unsat: complete && satRecords.length === 0,
    settled_leaves: leaves, capped_internal_nodes: cappedInternal,
    open_leaves: openLeaves.length, open_examples: openLeaves.slice(0, 5),
    sat_records: satRecords, bad: bad,
    nodes_total: nodes,
    ts: new Date().toISOString(),
  };
  console.log(JSON.stringify(out));
}

if (MODE === 'audit') audit(); else run();
