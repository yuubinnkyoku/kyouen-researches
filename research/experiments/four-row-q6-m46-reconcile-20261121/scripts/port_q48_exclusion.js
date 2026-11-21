#!/usr/bin/env node
// port_q48_exclusion.js — Node.js line-by-line port of research/experiments/fixed-width/scripts/q48_q6_exclusion.cpp
// (third-implementation replay for the K0302 finite-exclusion tier 16..35; byte-level reproduction of the
//  published per-case count fields is the acceptance gate). Mask = BigInt (board <= 4*68=272 bits).
//
// Usage: node port_q48_exclusion.js <lo> <hi> <cap> [--out=<jsonl>]
// Emits one JSON line per (m,target_row) to stdout (and --out file, appended) with the
// same fields the C++ main() prints. found_witness => exit code 3; any unknown => 4.
'use strict';
const fs = require('fs');

const MASK_WHOLE = 272;
// BigInt bit helpers
const bitOn = (p) => 1n << BigInt(p);

let m, target, cap, nodes, totalNodes, demandPrunes, aborted, found;
let circles, choices, failed, baseOptions, pairOptions, incident, circleCounts;
let rowCounts = new Array(4).fill(0), checked, stamp = 0;
let rowMasks = new Array(4);
let allSubsets, representatives, searched, unknown, anyFound;

function safe(s) {
  for (let y = 0; y < 4; y++) {
    let v = s & rowMasks[y];
    let c = 0; while (v) { c += Number(v & 1n); v >>= 1n; }
    if (c > 5) return false;
  }
  for (const cir of circles) {
    let v = s & cir.mask; let c = 0; while (v) { c += Number(v & 1n); v >>= 1n; }
    if (c > 5) return false;
  }
  return true;
}

function updateCounts(points, sign) {
  for (const p of points) {
    rowCounts[Math.floor(p / m)] += sign;
    for (const id of incident[p]) circleCounts[id] += sign;
  }
}

function extend(s, option, out) {
  out.mask = s | option.mask;
  out.added.length = 0;
  const delta = [0, 0, 0, 0];
  for (const p of option.points) if (((s >> BigInt(p)) & 1n) === 0n) { out.added.push(p); ++delta[Math.floor(p / m)]; }
  for (let y = 0; y < 4; y++) if (rowCounts[y] + delta[y] > 5) return false;
  ++stamp;
  for (const p of out.added) for (const id of incident[p]) if (checked[id] !== stamp) {
    checked[id] = stamp;
    let extra = 0;
    for (const v of out.added) if (((circles[id].mask >> BigInt(v)) & 1n) === 1n) ++extra;
    if (circleCounts[id] + extra > 5) return false;
  }
  return true;
}

function visit(s) {
  if (failed.has(s)) return false;
  if (++nodes > cap) { aborted = true; return false; }
  let best = null, pending = false;
  const demands = [[], [], [], []];
  for (const opts of choices) {
    let covered = false;
    for (const o of opts) if ((s & o.mask) === o.mask) { covered = true; break; }
    if (covered) continue;
    const next = [];
    const cand = { mask: 0n, added: [] };
    for (const o of opts) {
      if (extend(s, o, cand)) {
        let dup = false;
        for (const x of next) if (x.mask === cand.mask) { dup = true; break; }
        if (!dup) next.push({ mask: cand.mask, added: cand.added.slice() });
      }
    }
    if (next.length === 0) { failed.add(s); return false; }
    if (m >= 26) {
      const support = [0n, 0n, 0n, 0n];
      const minimum = [6, 6, 6, 6];
      for (const z of next) {
        const count = [0, 0, 0, 0];
        for (const p of z.added) { support[Math.floor(p / m)] |= bitOn(p); ++count[Math.floor(p / m)]; }
        for (let y = 0; y < 4; y++) minimum[y] = Math.min(minimum[y], count[y]);
      }
      for (let y = 0; y < 4; y++) if (minimum[y] > 0) demands[y].push([support[y], minimum[y]]);
    }
    if (!pending || next.length < best.length) { best = next; pending = true; }
    if (best.length === 1) break;
  }
  if (m >= 26) {
    for (let y = 0; y < 4; y++) for (let reverse = 0; reverse < 2; reverse++) {
      let used = 0n, required = 0;
      const ds = demands[y];
      const n = ds.length;
      for (let j = 0; j < n; j++) {
        const d = ds[reverse ? n - 1 - j : j];
        if ((used & d[0]) === 0n) { used |= d[0]; required += d[1]; }
      }
      if (required + rowCounts[y] > 5) { ++demandPrunes; failed.add(s); return false; }
    }
  }
  if (!pending) { found = s; return true; }
  for (const z of best) {
    updateCounts(z.added, 1);
    const win = visit(z.mask);
    updateCounts(z.added, -1);
    if (win) return true;
    if (aborted) return false;
  }
  failed.add(s);
  return false;
}

function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; }

function generateCircles(width) {
  const products = Array.from({ length: 2 * width - 1 }, () => []);
  for (let a = 0; a < width; a++) for (let b = a + 1; b < width; b++) products[a + b].push(a * b);
  const keys = new Set();
  const keyStr = (k) => k.join(',');
  for (let i = 0; i < 4; i++) for (let j = i + 1; j < 4; j++) {
    const h = j - i;
    for (let s = 0; s < 2 * width - 1; s++) for (const pa of products[s]) for (const pb of products[s]) {
      const c = pb - pa - h * (i + j);
      const d = h * pa - h * i * i - c * i;
      let key = [h, -s * h, c, d];
      let g = 0; for (const v of key) g = gcd(g, v);
      for (let idx = 0; idx < 4; idx++) key[idx] = Math.trunc(key[idx] / g);
      keys.add(keyStr(key));
    }
  }
  const sorted = [...keys].map(k => k.split(',').map(Number)).sort((A, B) => (A[0] - B[0]) || (A[1] - B[1]) || (A[2] - B[2]) || (A[3] - B[3]));
  const out = [];
  for (const key of sorted) {
    const [a, b, c, d] = key;
    let mask = 0n;
    const points = [];
    for (let y = 0; y < 4; y++) {
      const disc = b * b - 4 * a * (a * y * y + c * y + d);
      if (disc < 0) continue;
      let root = Math.floor(Math.sqrt(disc));
      while ((root + 1) * (root + 1) <= disc) ++root;
      while (root * root > disc) --root;
      if (root * root !== disc) continue;
      for (const sign of [-1, 1]) {
        const numerator = -b + sign * root;
        if (numerator % (2 * a) !== 0) continue;
        const x = numerator / (2 * a);
        if (x < 0 || x >= width) continue;
        const k = y * width + x;
        if (((mask >> BigInt(k)) & 1n) === 0n) { mask |= bitOn(k); points.push(k); }
      }
    }
    if (points.length >= 6) out.push({ mask, points });
  }
  return out;
}

function addSubsets(vs, need, out) {
  const n = vs.length;
  for (let bits = 0; bits < (1 << n); bits++) {
    let pc = 0, t = bits; while (t) { pc += t & 1; t >>= 1; }
    if (pc !== need) continue;
    const z = { mask: 0n, points: [] };
    for (let i = 0; i < n; i++) if ((bits >> i) & 1) { z.mask |= bitOn(vs[i]); z.points.push(vs[i]); }
    out.push(z);
  }
}

function prepareOptions() {
  baseOptions = Array.from({ length: m }, () => []);
  pairOptions = Array.from({ length: m }, () => Array.from({ length: m }, () => []));
  for (const c of circles) {
    const inPts = [], outPts = [];
    for (const k of c.points) (Math.floor(k / m) === target ? inPts : outPts).push(k);
    for (const k of inPts) {
      const x = k % m;
      let partner = -1;
      for (const other of inPts) if (other !== k) partner = other % m;
      const base = [];
      addSubsets(outPts, 5, base);
      // NOTE: C++ builds `base` then pushes each element of base into base_options[x] as {option, absent_partner}
      for (const option of base) baseOptions[x].push({ option, absent_partner: partner });
      if (partner >= 0) addSubsets(outPts, 4, pairOptions[x][partner]);
    }
  }
}

function testSubset(subset) {
  ++allSubsets;
  const reflected = [];
  for (let i = subset.length - 1; i >= 0; i--) reflected.push(m - 1 - subset[i]);
  // C++: if (subset > reflected) return;  — lexicographic vector comparison, ascending subsets
  if (lexGreater(subset, reflected)) return;
  ++representatives;
  let occupied = 0n;
  const selected = new Array(m).fill(false);
  for (const x of subset) { occupied |= bitOn(target * m + x); selected[x] = true; }
  rowCounts.fill(0);
  circleCounts.fill(0);
  const occupiedPoints = subset.map(x => target * m + x);
  updateCounts(occupiedPoints, 1);
  choices = [];
  for (let x = 0; x < m; x++) if (!selected[x]) {
    const options = [];
    for (const o of baseOptions[x]) if (o.absent_partner < 0 || !selected[o.absent_partner]) options.push(o.option);
    for (const y of subset) for (const o of pairOptions[x][y]) options.push(o);
    if (options.length === 0) return;
    choices.push(options);
  }
  // stable sort by size (V8 Array.prototype.sort is stable)
  choices.sort((A, B) => A.length - B.length);
  ++searched;
  failed = new Set();
  nodes = 0; aborted = false;
  if (visit(occupied)) {
    anyFound = true;
    // Extend the forced witness to a maximal safe configuration.
    for (let k = 0; k < 4 * m; k++) if (((found >> BigInt(k)) & 1n) === 0n) { const z = found | bitOn(k); if (safe(z)) found = z; }
    process.stderr.write('WITNESS m=' + m + ' target=' + target + '\n');
    for (let y = 0; y < 4; y++) { let line = ''; for (let x = 0; x < m; x++) if (((found >> BigInt(y * m + x)) & 1n) === 1n) line += x + ','; process.stderr.write(line + '\n'); }
  }
  totalNodes += nodes;
  if (aborted) ++unknown;
}

function lexGreater(A, B) {
  const n = Math.min(A.length, B.length);
  for (let i = 0; i < n; i++) { if (A[i] !== B[i]) return A[i] > B[i]; }
  return A.length > B.length;
}

function subsets(next, remaining, subset) {
  if (anyFound) return;
  if (remaining === 0) { testSubset(subset); return; }
  for (let x = next; x <= m - remaining; x++) {
    subset.push(x);
    subsets(x + 1, remaining - 1, subset);
    subset.pop();
    if (anyFound) return;
  }
}

function main() {
  const argv = process.argv.slice(2);
  const lo = argv.length > 0 ? parseInt(argv[0], 10) : 16;
  const hi = argv.length > 1 ? parseInt(argv[1], 10) : lo;
  cap = argv.length > 2 ? parseInt(argv[2], 10) : 1000000;
  let outPath = null;
  for (const a of argv) if (a.startsWith('--out=')) outPath = a.slice(6);
  if (lo < 6 || hi > 68 || lo > hi || !cap) { process.exit(2); }
  let anyUnknown = false;
  for (let mm = lo; mm <= hi; mm++) {
    m = mm;
    circles = generateCircles(m);
    rowMasks = [];
    for (let y = 0; y < 4; y++) { let mk = 0n; for (let x = 0; x < m; x++) mk |= bitOn(y * m + x); rowMasks.push(mk); }
    incident = Array.from({ length: 4 * m }, () => []);
    circleCounts = new Array(circles.length).fill(0);
    checked = new Array(circles.length).fill(0);
    for (let id = 0; id < circles.length; id++) for (const p of circles[id].points) incident[p].push(id);
    for (target = 0; target < 2; target++) {
      const start = Date.now();
      prepareOptions();
      allSubsets = representatives = searched = unknown = totalNodes = demandPrunes = 0;
      anyFound = false;
      const subset = [];
      for (let size = 0; size <= 4 && !anyFound; size++) subsets(0, size, subset);
      const seconds = (Date.now() - start) / 1000;
      const line = { m, target_row: target, circles: circles.length, target_subsets: allSubsets, reflection_representatives: representatives, searched_subsets: searched, visited_states: totalNodes, disjoint_support_prunes: demandPrunes, unknown_subsets: unknown, found_witness: anyFound, seconds };
      const text = JSON.stringify(line);
      console.log(text);
      if (outPath) fs.appendFileSync(outPath, text + '\n');
      if (anyFound) process.exit(3);
      if (unknown) anyUnknown = true;
    }
  }
  process.exit(anyUnknown ? 4 : 0);
}
main();
