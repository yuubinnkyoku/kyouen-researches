#!/usr/bin/env node
// compare_port_vs_published.js — third-implementation replay comparison against the published
// q48_q6_finite_exclusions.json (verified interval 16..35, 40 cases).
// Compares the 7 published count fields per case: m, target_row, circles, target_subsets,
// reflection_representatives, searched_subsets, unknown_subsets, found_witness.
// Extra port fields (visited_states, disjoint_support_prunes, seconds) are intentionally ignored
// (the published note omits order-dependent state counts and timings).
// bigint file (port_bigint_16.txt) covers m=16,17; fast jsonl covers m=17..35; m=17 must agree in both.
// Fail-closed: any field mismatch, missing case, duplicate (m,target) beyond the known m=17 overlap,
// unknown>0, or found_witness=true => exit nonzero and print the first mismatches.
'use strict';
const fs = require('fs');
const path = require('path');
const OUT = path.join(__dirname, '..', 'output', 'q48replay');
const PUB = process.argv[2] || path.join(__dirname, '..', '..', '..', '..', 'fixed-width', 'output', 'q48_q6_finite_exclusions.json');
const pub = JSON.parse(fs.readFileSync(PUB, 'utf8'));
const pubKeys = ['m','target_row','circles','target_subsets','reflection_representatives','searched_subsets','unknown_subsets','found_witness'];
const pubMap = new Map();
for (const c of pub.cases) pubMap.set(c.m + ':' + c.target_row, c);
const seen = new Map();
let lines = [];
const fastPath = path.join(OUT, 'port_fast_17_35.jsonl');
for (const t of fs.readFileSync(fastPath, 'utf8').split('\n')) if (t.trim()) lines.push(['fast', JSON.parse(t)]);
const bigPath = path.join(OUT, 'port_bigint_16.txt');
if (fs.existsSync(bigPath)) for (const t of fs.readFileSync(bigPath, 'utf8').split('\n')) if (t.trim()) lines.push(['bigint', JSON.parse(t)]);
const cross = [];
for (const [src, c] of lines) {
  const k = c.m + ':' + c.target_row;
  if (!pubMap.has(k)) { console.log('FAIL port case not in published interval: ' + k + ' (' + src + ')'); process.exit(1); }
  const p = pubMap.get(k);
  for (const f of pubKeys) {
    if (p[f] !== c[f]) { console.log('FAIL ' + k + ' (' + src + ') field ' + f + ': port=' + c[f] + ' published=' + p[f]); process.exit(1); }
  }
  if (c.unknown_subsets !== 0) { console.log('FAIL ' + k + ' (' + src + ') unknown_subsets=' + c.unknown_subsets + ' (fail-closed)'); process.exit(1); }
  if (c.found_witness !== false) { console.log('FAIL ' + k + ' (' + src + ') found_witness=true (fail-closed)'); process.exit(1); }
  if (seen.has(k)) {
    if (k === '17:0' || k === '17:1') cross.push(k);
    else { console.log('FAIL duplicate case beyond the m=17 cross-port overlap: ' + k); process.exit(1); }
  }
  seen.set(k, src);
}
for (const k of pubMap.keys()) if (!seen.has(k)) { console.log('FAIL missing port case: ' + k); process.exit(1); }
console.log('ALL ' + pub.cases.length + ' published cases reproduced by the Node ports (bigint: m=16,17; fast: m=17..35; m=17 cross-port sources: ' + (cross.length ? 'both' : 'missing!') + '), 7/7 fields exact, unknown=0 everywhere, no witness.');
console.log('bigint lines: ' + lines.filter(l => l[0] === 'bigint').length + ', fast lines: ' + lines.filter(l => l[0] === 'fast').length);
process.exit(0);
