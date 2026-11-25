#!/usr/bin/env node
// port_q48_exclusion_fast.js — fast second Node port of q48_q6_exclusion.cpp (third-implementation replay).
// Same algorithm and exact same search order as the literal BigInt port (port_q48_exclusion.js) and the C++:
// masks are 9-word uint32 arrays (272 bits <= 288), the failure memo is an epoch-based open-addressing table.
// The literal BigInt port is the reference; this port reproduces the same per-case count fields.
//
// Usage: node port_q48_exclusion_fast.js <lo> <hi> <cap> [--out=<jsonl>]
'use strict';
const fs = require('fs');

const WORDS = 9;          // 9*32 = 288 >= 4*68 bits
const WSHIFT = 5, WMASK = 31;

function hasBit(mask, p) { return (mask[p >>> WSHIFT] >>> (p & WMASK)) & 1; }

let m, target, cap, nodes, totalNodes, demandPrunes, aborted, found;
let circles, choices, failedInit, baseOptions, pairOptions, incident, circleCounts;
let rowCounts = [0, 0, 0, 0];
let checked, stamp = 0;
let rowMasks;
let allSubsets, representatives, searched, unknown, anyFound;

// ---------- failure memo: epoch open-addressing table ----------
const TB = 1 << 22;                 // 4M cells
const TKEY = new Int32Array(TB * WORDS);
const TEPO = new Int32Array(TB);
let epoch = 0;
function hash9(w) {
  let h = (w[0] | 0) * 0x9e3779b1 ^ (w[1] | 0) * 0x85ebca6b ^ (w[2] | 0) * 0xc2b2ae35 ^ (w[3] | 0) * 0x27d4eb2f ^ (w[4] | 0) * 0x9e3779b1 ^ (w[5] | 0) * 0x85ebca6b ^ (w[6] | 0) * 0xc2b2ae35 ^ (w[7] | 0) * 0x27d4eb2f ^ (w[8] | 0) * 0x9e3779b1;
  return (h ^ (h >>> 16)) & (TB - 1);
}
function failedHas(s) {
  let i = hash9(s);
  for (;;) {
    if (TEPO[i] !== epoch) return false;
    const base = i * WORDS;
    let eq = true;
    for (let t = 0; t < WORDS; t++) if (TKEY[base + t] !== (s[t] | 0)) { eq = false; break; }
    if (eq) return true;
    i = (i + 1) & (TB - 1);
  }
}
function failedAdd(s) {
  let i = hash9(s);
  for (;;) {
    if (TEPO[i] !== epoch) {
      const base = i * WORDS;
      for (let t = 0; t < WORDS; t++) TKEY[base + t] = s[t] | 0;
      TEPO[i] = epoch;
      return;
    }
    const base = i * WORDS;
    let eq = true;
    for (let t = 0; t < WORDS; t++) if (TKEY[base + t] !== (s[t] | 0)) { eq = false; break; }
    if (eq) return;
    i = (i + 1) & (TB - 1);
  }
}

function popcountRow(s, rowMask) {
  let c = 0;
  for (let t = 0; t < WORDS; t++) { let v = s[t] & rowMask[t]; while (v) { c += v & 1; v >>>= 1; } }
  return c;
}

function safe(s) {
  for (let y = 0; y < 4; y++) if (popcountRow(s, rowMasks[y]) > 5) return false;
  for (const cir of circles) if (popcountRow(s, cir.mask) > 5) return false;
  return true;
}

function updateCounts(points, sign) {
  for (const p of points) {
    rowCounts[(p / m) | 0] += sign;
    const inc = incident[p];
    for (let i = 0; i < inc.length; i++) circleCounts[inc[i]] += sign;
  }
}

function extend(s, option, outMask, outAdded) {
  // outMask = s | option.mask ; outAdded cleared and refilled
  for (let t = 0; t < WORDS; t++) outMask[t] = s[t] | option.mask[t];
  outAdded.length = 0;
  const delta = [0, 0, 0, 0];
  const pts = option.points;
  for (let i = 0; i < pts.length; i++) {
    const p = pts[i];
    if (!hasBit(s, p)) { outAdded.push(p); delta[(p / m) | 0]++; }
  }
  for (let y = 0; y < 4; y++) if (rowCounts[y] + delta[y] > 5) return false;
  ++stamp;
  for (let i = 0; i < outAdded.length; i++) {
    const p = outAdded[i];
    const inc = incident[p];
    for (let a = 0; a < inc.length; a++) {
      const id = inc[a];
      if (checked[id] !== stamp) {
        checked[id] = stamp;
        let extra = 0;
        const cm = circles[id].mask;
        for (let j = 0; j < outAdded.length; j++) if (hasBit(cm, outAdded[j])) ++extra;
        if (circleCounts[id] + extra > 5) return false;
      }
    }
  }
  return true;
}

function visit(s) {
  if (failedHas(s)) return false;
  if (++nodes > cap) { aborted = true; return false; }
  let best = null, pending = false;
  const demands = [null, null, null, null];
  const groups = choices;
  for (let gi = 0; gi < groups.length; gi++) {
    const opts = groups[gi];
    let covered = false;
    for (let oi = 0; oi < opts.length; oi++) {
      const om = opts[oi].mask;
      let eq = true;
      for (let t = 0; t < WORDS; t++) if ((s[t] & om[t]) !== om[t]) { eq = false; break; }
      if (eq) { covered = true; break; }
    }
    if (covered) continue;
    const next = [];
    const candMask = new Array(WORDS).fill(0);
    const candAdded = [];
    for (let oi = 0; oi < opts.length; oi++) {
      if (extend(s, opts[oi], candMask, candAdded)) {
        let dup = false;
        for (let ni = 0; ni < next.length; ni++) {
          const nm = next[ni].mask;
          let eq = true;
          for (let t = 0; t < WORDS; t++) if (nm[t] !== candMask[t]) { eq = false; break; }
          if (eq) { dup = true; break; }
        }
        if (!dup) next.push({ mask: candMask.slice(), added: candAdded.slice() });
      }
    }
    if (next.length === 0) { failedAdd(s); return false; }
    if (m >= 26) {
      if (!demands[0]) { demands[0] = []; demands[1] = []; demands[2] = []; demands[3] = []; }
      const support = [new Array(WORDS).fill(0), new Array(WORDS).fill(0), new Array(WORDS).fill(0), new Array(WORDS).fill(0)];
      const minimum = [6, 6, 6, 6];
      for (const z of next) {
        const count = [0, 0, 0, 0];
        for (const p of z.added) {
          const y = (p / m) | 0;
          support[y][p >>> WSHIFT] |= 1 << (p & WMASK);
          ++count[y];
        }
        for (let y = 0; y < 4; y++) minimum[y] = Math.min(minimum[y], count[y]);
      }
      for (let y = 0; y < 4; y++) if (minimum[y] !== 0) demands[y].push([support[y], minimum[y]]);
    }
    if (!pending || next.length < best.length) { best = next; pending = true; }
    if (best.length === 1) break;
  }
  if (m >= 26 && demands[0]) {
    for (let y = 0; y < 4; y++) for (let reverse = 0; reverse < 2; reverse++) {
      const used = new Array(WORDS).fill(0);
      let required = 0;
      const ds = demands[y];
      const n = ds.length;
      for (let j = 0; j < n; j++) {
        const d = ds[reverse ? n - 1 - j : j];
        let inter = false;
        for (let t = 0; t < WORDS; t++) if ((used[t] & d[0][t]) !== 0) { inter = true; break; }
        if (!inter) {
          for (let t = 0; t < WORDS; t++) used[t] |= d[0][t];
          required += d[1];
        }
      }
      if (required + rowCounts[y] > 5) { ++demandPrunes; failedAdd(s); return false; }
    }
  }
  if (!pending) { found = s.slice(); return true; }
  for (const z of best) {
    updateCounts(z.added, 1);
    const win = visit(z.mask);
    updateCounts(z.added, -1);
    if (win) return true;
    if (aborted) return false;
  }
  failedAdd(s);
  return false;
}

function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; }

function generateCircles(width) {
  const products = Array.from({ length: 2 * width - 1 }, () => []);
  for (let a = 0; a < width; a++) for (let b = a + 1; b < width; b++) products[a + b].push(a * b);
  const keys = new Set();
  for (let i = 0; i < 4; i++) for (let j = i + 1; j < 4; j++) {
    const h = j - i;
    for (let s = 0; s < 2 * width - 1; s++) for (const pa of products[s]) for (const pb of products[s]) {
      const c = pb - pa - h * (i + j);
      const d = h * pa - h * i * i - c * i;
      const key = [Math.trunc(h / 1), 0, 0, 0];
      let raw = [h, -s * h, c, d];
      let g = 0; for (const v of raw) g = gcd(g, v);
      for (let idx = 0; idx < 4; idx++) key[idx] = Math.trunc(raw[idx] / g);
      keys.add(key.join(','));
    }
  }
  const sorted = [...keys].map(k => k.split(',').map(Number)).sort((A, B) => (A[0] - B[0]) || (A[1] - B[1]) || (A[2] - B[2]) || (A[3] - B[3]));
  const out = [];
  for (const key of sorted) {
    const [a, b, c, d] = key;
    const mask = new Array(WORDS).fill(0);
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
        if (!hasBit(mask, k)) {
          mask[k >>> WSHIFT] |= 1 << (k & WMASK);
          points.push(k);
        }
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
    const z = { mask: new Array(WORDS).fill(0), points: [] };
    for (let i = 0; i < n; i++) if ((bits >> i) & 1) {
      const v = vs[i];
      z.mask[v >>> WSHIFT] |= 1 << (v & WMASK);
      z.points.push(v);
    }
    out.push(z);
  }
}

function prepareOptions() {
  baseOptions = Array.from({ length: m }, () => []);
  pairOptions = Array.from({ length: m }, () => Array.from({ length: m }, () => []));
  for (const c of circles) {
    const inPts = [], outPts = [];
    for (const k of c.points) (((k / m) | 0) === target ? inPts : outPts).push(k);
    for (const k of inPts) {
      const x = k % m;
      let partner = -1;
      for (const other of inPts) if (other !== k) partner = other % m;
      const base = [];
      addSubsets(outPts, 5, base);
      for (const option of base) baseOptions[x].push({ option, absent_partner: partner });
      if (partner >= 0) addSubsets(outPts, 4, pairOptions[x][partner]);
    }
  }
}

function lexGreater(A, B) {
  const n = Math.min(A.length, B.length);
  for (let i = 0; i < n; i++) { if (A[i] !== B[i]) return A[i] > B[i]; }
  return A.length > B.length;
}

function testSubset(subset) {
  ++allSubsets;
  const reflected = [];
  for (let i = subset.length - 1; i >= 0; i--) reflected.push(m - 1 - subset[i]);
  if (lexGreater(subset, reflected)) return;
  ++representatives;
  const occupied = new Array(WORDS).fill(0);
  const selected = new Array(m).fill(false);
  for (const x of subset) {
    const k = target * m + x;
    occupied[k >>> WSHIFT] |= 1 << (k & WMASK);
    selected[x] = true;
  }
  rowCounts[0] = rowCounts[1] = rowCounts[2] = rowCounts[3] = 0;
  circleCounts.fill(0);
  const occupiedPoints = subset.map(x => target * m + x);
  updateCounts(occupiedPoints, 1);
  choices = [];
  for (let x = 0; x < m; x++) if (!selected[x]) {
    const options = [];
    for (const o of baseOptions[x]) if (o.absent_partner < 0 || !selected[o.absent_partner]) options.push(o.option);
    for (const y of subset) { const po = pairOptions[x][y]; for (const o of po) options.push(o); }
    if (options.length === 0) return;
    choices.push(options);
  }
  choices.sort((A, B) => A.length - B.length);
  ++searched;
  ++epoch;                 // clears the failure memo
  nodes = 0; aborted = false;
  if (visit(occupied)) {
    anyFound = true;
    for (let k = 0; k < 4 * m; k++) if (!hasBit(found, k)) {
      found[k >>> WSHIFT] |= 1 << (k & WMASK);
      if (!safe(found)) found[k >>> WSHIFT] ^= 1 << (k & WMASK);
    }
    process.stderr.write('WITNESS m=' + m + ' target=' + target + '\n');
    for (let y = 0; y < 4; y++) {
      let line = '';
      for (let x = 0; x < m; x++) if (hasBit(found, y * m + x)) line += x + ',';
      process.stderr.write(line + '\n');
    }
  }
  totalNodes += nodes;
  if (aborted) ++unknown;
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
    for (let y = 0; y < 4; y++) {
      const mk = new Array(WORDS).fill(0);
      for (let x = 0; x < m; x++) { const k = y * m + x; mk[k >>> WSHIFT] |= 1 << (k & WMASK); }
      rowMasks.push(mk);
    }
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
