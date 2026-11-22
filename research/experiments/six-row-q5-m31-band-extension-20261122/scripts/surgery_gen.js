#!/usr/bin/env node
// Generalized bounded-edit surgery for fixed-width witness band extension
// (six-row band lane: (6,5) m=32, (6,6) m=25, (6,7) m=22 and the placement
// census discovered (6,5) m=31; seeds listed per config).
//
// Adapted from research/experiments/five-row-q4-witness-band-40plus-20261121/
// scripts/surgery.js (published sha256
// 0410d787a53ffadda3bc44b9c31b423ce4a38ab4798b28e279230cfb73ab7e25, verified
// byte-exact at lane start): the curve engines (canonLine, circleIR, Board,
// verifyCandidate) are kept verbatim; only parameterization changed (w, q,
// target width, base list, per-base checkpoint output, row-reflect uses w-1).
// All arithmetic in JS safe integers, no floating point.
//
// Witness conditions on board w x m (columns 0..m-1), q:
//   safety      : no line/circle contains >= q stones.
//   maximality  : every EMPTY cell is blocked (some line/circle through it
//                 contains >= q-1 stones).
//   row deficiency: every row has <= q-1 stones, some row has <= q-2 stones.
//
// Stone-count conservation (all lane targets): a def-mode witness has
// <= w(q-1)-1 stones (w(q-1) stones with all rows <= q-1 saturate all rows
// and lose the deficiency), and every base seed has exactly w(q-1)-1
// stones, so pure-add surgery is impossible; edit budget: single-move,
// remove-2/add-1, remove-2/add-2 (matching the m=40 lane precedent).
//
// Base placements: the config file lists the seed configs with per-seed
// x-offsets; by the board-isometry covariance lemma ((H(T) at offset s) =
// board-H of (T at offset M-span-s), same for V/HV), enumerating ALL
// placements of a config up to translation is complete modulo the board
// isometry group for searches from any D4 image of the config.
//
// Usage: node surgery_gen.js <config.json> [startBase] [endBaseExclusive]
//   config.json: { "tag": ..., "w": w, "q": q, "m": targetM,
//                  "bases": [ { "label": ..., "stones": [[x,y],...] }, ... ] }
// Per-base checkpoint file output/<tag>/base-<i>.json (resume-safe: an
// existing file is not recomputed), plus per-base stderr progress.
// Verify mode: node surgery_gen.js --verify <w> <m> <q> <stones.json>
//   (system-1 witness verification: safety + full-board maximality + rows;
//    exit code 0 iff WITNESS_OK)
'use strict';

const gcd2 = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; };

function canonLine(p, r) {
  let A = r[1] - p[1], B = p[0] - r[0], C = r[0] * p[1] - r[1] * p[0];
  const g = gcd2(gcd2(A, B), C) || 1;
  A /= g; B /= g; C /= g;
  if (A < 0 || (A === 0 && (B < 0 || (B === 0 && C < 0)))) { A = -A; B = -B; C = -C; }
  return A + ',' + B + ',' + C;
}

// circle through 3 non-collinear points; canonical key (al,be,ga,de) with
// al*x + be*y + ga + de*(x^2+y^2) = 0, gcd-normalized, sign-fixed (de > 0).
function circleIR(p, r, s) {
  const x1 = p[0], y1 = p[1], x2 = r[0], y2 = r[1], x3 = s[0], y3 = s[1];
  const a11 = x2 - x1, a12 = y2 - y1, a21 = x3 - x1, a22 = y3 - y1;
  const det = a11 * a22 - a12 * a21;
  if (det === 0) return null;
  const f1 = x1 * x1 + y1 * y1, f2 = x2 * x2 + y2 * y2, f3 = x3 * x3 + y3 * y3;
  const b1 = -(f2 - f1), b2 = -(f3 - f1);
  const al = b1 * a22 - b2 * a12;
  const be = a11 * b2 - a21 * b1;
  const ga = -(al * x1 + be * y1) - f1 * det;
  const de = det;
  const g = gcd2(gcd2(gcd2(al, be), ga), de) || 1;
  let A2 = al / g, B2 = be / g, C2 = ga / g, D2 = de / g;
  if (D2 < 0 || (D2 === 0 && (A2 < 0 || (A2 === 0 && (B2 < 0 || (B2 === 0 && C2 < 0)))))) {
    A2 = -A2; B2 = -B2; C2 = -C2; D2 = -D2;
  }
  return A2 + ',' + B2 + ',' + C2 + ',' + D2;
}

const curveCache = new Map();
const parseKey = (key) => {
  let v = curveCache.get(key);
  if (!v) { v = key.split(',').map(Number); curveCache.set(key, v); }
  return v;
};
const fastOnLine = (key, p) => { const v = parseKey(key); return v[0] * p[0] + v[1] * p[1] + v[2] === 0; };
const fastOnCircle = (key, p) => { const v = parseKey(key); return v[0] * p[0] + v[1] * p[1] + v[2] + v[3] * (p[0] * p[0] + p[1] * p[1]) === 0; };

class Board {
  constructor(w, m, q, stones) {
    this.w = w; this.m = m; this.q = q;
    this.S = stones.map(s => s.slice());
    this.sset = new Set(this.S.map(p => p[0] + ',' + p[1]));
    this.n = this.S.length;
    this.rows = new Array(w).fill(0);
    for (const [x, y] of this.S) this.rows[y]++;
    const lineMap = new Map();
    for (let i = 0; i < this.n; i++) for (let j = i + 1; j < this.n; j++) {
      const key = canonLine(this.S[i], this.S[j]);
      let st = lineMap.get(key); if (!st) { st = new Set(); lineMap.set(key, st); }
      st.add(i); st.add(j);
    }
    const circMap = new Map();
    for (let i = 0; i < this.n; i++) for (let j = i + 1; j < this.n; j++) for (let k = j + 1; k < this.n; k++) {
      const key = circleIR(this.S[i], this.S[j], this.S[k]);
      if (key === null) continue;
      let st = circMap.get(key); if (!st) { st = new Set(); circMap.set(key, st); }
      st.add(i); st.add(j); st.add(k);
    }
    this.blocking = new Map();
    this.unblocked = [];
    for (let x = 0; x < m; x++) for (let y = 0; y < w; y++) {
      const c = x + ',' + y;
      if (this.sset.has(c)) continue;
      const masks = [];
      for (const [key, st] of lineMap) if (fastOnLine(key, [x, y]) && st.size >= q - 1) masks.push(st);
      for (const [key, st] of circMap) if (fastOnCircle(key, [x, y]) && st.size >= q - 1) masks.push(st);
      if (masks.length === 0) this.unblocked.push([x, y]);
      this.blocking.set(c, masks);
    }
  }
  safety() {
    let ml = 0, mc = 0;
    const lineMap = new Map();
    for (let i = 0; i < this.n; i++) for (let j = i + 1; j < this.n; j++) {
      const k = canonLine(this.S[i], this.S[j]); lineMap.set(k, (lineMap.get(k) || 0) + 1);
    }
    for (const k of lineMap.keys()) { let c = 0; for (const p of this.S) if (fastOnLine(k, p)) c++; ml = Math.max(ml, c); }
    const keys = new Set();
    for (let i = 0; i < this.n; i++) for (let j = i + 1; j < this.n; j++) for (let k2 = j + 1; k2 < this.n; k2++) {
      const ck = circleIR(this.S[i], this.S[j], this.S[k2]); if (ck) keys.add(ck);
    }
    for (const k of keys) { let c = 0; for (const p of this.S) if (fastOnCircle(k, p)) c++; mc = Math.max(mc, c); }
    return { ml, mc, safe: ml < this.q && mc < this.q };
  }
}

function verifyCandidate(bd, remIdxs, addCells) {
  const { w, m, q } = bd;
  const rem = new Set(remIdxs);
  const kept = bd.S.filter((_, i) => !rem.has(i));
  const S2 = kept.concat(addCells);
  if (S2.length !== new Set(S2.map(p => p.join(','))).size) return null;
  const rows = new Array(w).fill(0);
  for (const [, y] of S2) rows[y]++;
  for (const c of rows) if (c > q - 1) return null;           // row cap violated (also unsafe)
  if (!rows.some(c => c <= q - 2)) return null;              // no deficient row
  const sset = new Set(S2.map(p => p.join(',')));
  // ---- fast frontier check: base-unblocked cells must be newly blocked or occupied.
  for (const [ux, uy] of bd.unblocked) {
    if (sset.has(ux + ',' + uy)) continue;
    let covered = false;
    for (const t of addCells) {
      const lk = canonLine([ux, uy], t);
      let c = 0; for (const p of S2) if (fastOnLine(lk, p)) c++;
      if (c >= q - 1) { covered = true; break; }
      for (const s of kept) {
        if (fastOnLine(lk, s)) continue;
        const ck = circleIR([ux, uy], t, s);
        if (ck === null) continue;
        let cc = 0; for (const p of S2) if (fastOnCircle(ck, p)) cc++;
        if (cc >= q - 1) { covered = true; break; }
      }
      if (covered) break;
    }
    if (!covered) return null;
  }
  // safety: only curves through added cells can be new
  for (const t of addCells) {
    for (const s of kept) {
      const lk = canonLine(t, s);
      let c = 0; for (const p of S2) if (fastOnLine(lk, p)) c++;
      if (c >= q) return null;
    }
    for (let i = 0; i < kept.length; i++) for (let j = i + 1; j < kept.length; j++) {
      const ck = circleIR(t, kept[i], kept[j]);
      if (ck === null) continue;
      let c = 0; for (const p of S2) if (fastOnCircle(ck, p)) c++;
      if (c >= q) return null;
    }
  }
  // maximality: every empty cell blocked
  for (let x = 0; x < m; x++) for (let y = 0; y < w; y++) {
    const ck2 = x + ',' + y;
    if (sset.has(ck2)) continue;
    let blockedFlag = false;
    const masks = bd.blocking.get(ck2);
    if (masks) {
      for (const mask of masks) {
        let ok = true;
        for (const i of rem) if (mask.has(i)) { ok = false; break; }
        if (ok) { blockedFlag = true; break; }
      }
    }
    if (!blockedFlag) {
      for (const t of addCells) {
        const lk = canonLine([x, y], t);
        let c = 0; for (const p of S2) if (fastOnLine(lk, p)) c++;
        if (c >= q - 1) { blockedFlag = true; break; }
        for (const s of kept) {
          if (fastOnLine(lk, s)) continue;
          const ck = circleIR([x, y], t, s);
          if (ck === null) continue;
          let cc = 0; for (const p of S2) if (fastOnCircle(ck, p)) cc++;
          if (cc >= q - 1) { blockedFlag = true; break; }
        }
        if (blockedFlag) break;
      }
    }
    if (!blockedFlag) return null;
  }
  return { stones: S2, rows };
}

function surgery(base, w, m, q, label) {
  const bd = new Board(w, m, q, base);
  const saf = bd.safety();
  const results = [];
  const stats = { label, baseN: bd.n, baseRows: bd.rows, baseSafe: saf.safe, baseMl: saf.ml, baseMc: saf.mc, unblockedCells: bd.unblocked.length };
  console.error(`[base ${label}] n=${bd.n} rows=${JSON.stringify(bd.rows)} safe=${saf.safe} (ml=${saf.ml} mc=${saf.mc}) unblockedCells=${bd.unblocked.length} -> ${JSON.stringify(bd.unblocked)}`);
  if (!saf.safe) { stats.skipped = 'base not safe'; return { results, stats }; }
  const emptyCells = [];
  for (let x = 0; x < m; x++) for (let y = 0; y < w; y++) if (!bd.sset.has(x + ',' + y)) emptyCells.push([x, y]);
  let tried = 0;
  for (let i = 0; i < bd.n; i++) {
    for (const t of emptyCells) {
      tried++;
      if (bd.S[i][0] === t[0] && bd.S[i][1] === t[1]) continue;
      const r = verifyCandidate(bd, [i], [t.slice()]);
      if (r) results.push({ kind: 'move1rem1add', rem: [i], add: [t.slice()], stones: r.stones, rows: r.rows });
    }
  }
  stats.move1Candidates = tried;
  stats.move1Witnesses = results.length;
  console.error(`[base ${label}] single-move candidates=${tried} witnesses=${results.length}`);
  let t21 = 0;
  for (let i = 0; i < bd.n; i++) for (let j = i + 1; j < bd.n; j++) {
    for (const t of emptyCells) {
      t21++;
      const r = verifyCandidate(bd, [i, j], [t.slice()]);
      if (r) results.push({ kind: 'rem2add1', rem: [i, j], add: [t.slice()], stones: r.stones, rows: r.rows });
    }
  }
  stats.rem2add1Candidates = t21;
  stats.afterRem2add1 = results.length;
  console.error(`[base ${label}] after rem2add1 total=${results.length}`);
  let tried22 = 0;
  for (let i = 0; i < bd.n; i++) for (let j = i + 1; j < bd.n; j++) {
    for (let a = 0; a < emptyCells.length; a++) for (let b = a + 1; b < emptyCells.length; b++) {
      tried22++;
      const r = verifyCandidate(bd, [i, j], [emptyCells[a].slice(), emptyCells[b].slice()]);
      if (r) results.push({ kind: 'rem2add2', rem: [i, j], add: [emptyCells[a].slice(), emptyCells[b].slice()], stones: r.stones, rows: r.rows });
    }
  }
  stats.rem2add2Candidates = tried22;
  stats.totalWitnesses = results.length;
  console.error(`[base ${label}] rem2add2 candidates=${tried22} total=${results.length}`);
  return { results, stats };
}

// ---- main ----
const fs = require('fs');
const path = require('path');
if (process.argv[2] === '--verify') {
  // Independent witness verification with the same engine (system 1):
  // safety() + full-board maximality + row deficiency on w x m.
  const [w, m, q, stonesPath] = [parseInt(process.argv[3], 10), parseInt(process.argv[4], 10),
                                 parseInt(process.argv[5], 10), process.argv[6]];
  const stones = JSON.parse(fs.readFileSync(stonesPath, 'utf8'));
  const bd = new Board(w, m, q, stones);
  const saf = bd.safety();
  const res = verifyCandidate(bd, [], []);
  const rows = new Array(w).fill(0);
  for (const [, y] of stones) rows[y]++;
  const rowOk = rows.every(r => r <= q - 1) && rows.some(r => r <= q - 2);
  console.log(JSON.stringify({ w, m, q, n: stones.length, rows, safe: saf.safe, maxline: saf.ml, maxcirc: saf.mc,
                               maximal: res !== null, deficient: rowOk,
                               verdict: (saf.safe && res !== null && rowOk) ? 'WITNESS_OK' : 'FAIL',
                               unblockedEmpty: bd.unblocked.length }));
  process.exit(saf.safe && res !== null && rowOk ? 0 : 1);
}
const cfgPath = process.argv[2];
const startBase = parseInt(process.argv[3] || '0', 10);
const endBase = parseInt(process.argv[4] || String(Number.MAX_SAFE_INTEGER), 10);
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
const { tag, w, q, m: targetM } = cfg;
const outDir = path.join(path.dirname(cfgPath), '..', 'output', tag);
fs.mkdirSync(outDir, { recursive: true });
for (let i = startBase; i < Math.min(endBase, cfg.bases.length); i++) {
  const base = cfg.bases[i];
  const outFile = path.join(outDir, `base-${String(i).padStart(3, '0')}.json`);
  if (fs.existsSync(outFile)) { console.log(`skip base ${i} (${base.label}) already done`); continue; }
  const t0 = Date.now();
  const { results, stats } = surgery(base.stones, w, targetM, q, base.label);
  stats.elapsedMs = Date.now() - t0;
  const out = { baseIndex: i, label: base.label, ...stats,
    witnesses: results.map(r => ({ kind: r.kind, rem: r.rem, add: r.add, stones: r.stones, rows: r.rows })) };
  fs.writeFileSync(outFile, JSON.stringify(out, null, 1));
  console.log(`base ${i} (${base.label}): total=${stats.totalWitnesses ?? 0} witnesses, ${(stats.elapsedMs/1000).toFixed(1)}s -> ${outFile}`);
}
console.log('done range', startBase, endBase, 'of', cfg.bases.length, 'bases');
