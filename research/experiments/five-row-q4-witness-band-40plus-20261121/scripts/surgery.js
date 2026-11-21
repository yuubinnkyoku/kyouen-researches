#!/usr/bin/env node
// Bounded-edit surgery for (5,4) m=40 witness search — single-owner lane
// five-row-q4-witness-band-40plus-20261121.
//
// Independent integer implementation (no shared code with append_criterion.py
// lineage; all arithmetic in JS safe integers, no floating point).
//
// Curves through integer lattice points:
//   line  : canonical (A,B,C), A x + B y + C = 0, gcd-normalized, sign-fix.
//   circle: canonical 4-tuple (al,be,ga,de): al*x + be*y + ga + de*(x^2+y^2) = 0
//           derived from the 3x3 determinant form, scaled to integers, gcd+sign.
//           NOTE: membership test is A*x+B*y+C + D*(x^2+y^2) === 0 (the original
//           draft used ... === D*(x^2+y^2) and was wrong; caught against the
//           Python Fraction second implementation on cell (0,1) of the
//           published m=39 witness).
//
// Witness conditions on board w x m (columns 0..m-1), q:
//   safety      : no line/circle contains >= q stones.
//   maximality  : every EMPTY cell is blocked (some line/circle through it
//                 contains >= q-1 stones).
//   row deficiency: every row has <= q-1 stones, some row has <= q-2 stones.
//
// Surgery space (stone-count conservation argument):
//   w=5, q=4: row cap 3, 15 stones => all rows 3 => no deficient row, so a
//   width-40 witness has <= 14 stones, and pure-add from a 14-stone witness is
//   impossible (15 stones => no deficiency). Edits enumerated from published
//   14-stone witnesses: +1/-1 (single move), +1/-2 (13 stones), +2/-2.
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

const onLine = (key, p) => { const [A, B, C] = key.split(',').map(Number); return A * p[0] + B * p[1] + C === 0; };
const onCircle = (key, p) => { const [A, B, C, D] = key.split(',').map(Number); return A * p[0] + B * p[1] + C + D * (p[0] * p[0] + p[1] * p[1]) === 0; };

// pre-split cache: avoid .split(',').map() in hot loops
const curveCache = new Map();
const parseKey = (key) => {
  let v = curveCache.get(key);
  if (!v) { v = key.split(',').map(Number); curveCache.set(key, v); }
  return v;
};
const fastOnLine = (key, p) => { const v = parseKey(key); return v[0] * p[0] + v[1] * p[1] + v[2] === 0; };
const fastOnCircle = (key, p) => { const v = parseKey(key); return v[0] * p[0] + v[1] * p[1] + v[2] + v[3] * (p[0] * p[0] + p[1] * p[1]) === 0; };

// ------------ base geometry of a stone set S on board (w, m) ------------
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
    this.blocking = new Map();  // "x,y" -> array of maskSets of blocking curves
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

// candidate set C = S - {remIdxs} + {addCells}; verify witness on (w,m,q)
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
  // removals never add blocking, so an uncovered base-unblocked empty cell
  // fails the candidate immediately.
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
  // safety: only curves through added cells can be new (a forbidden curve
  // created by the edit must contain one of the added stones)
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
  const addedKeys = addCells.map(p => p.join(','));
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
      // new curves through added stones and this cell
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

function surgery(base, w, m, q, label, doDouble) {
  const bd = new Board(w, m, q, base);
  const saf = bd.safety();
  const results = [];
  console.error(`[base ${label}] n=${bd.n} rows=${JSON.stringify(bd.rows)} safe=${saf.safe} (ml=${saf.ml} mc=${saf.mc}) unblockedCells=${bd.unblocked.length} -> ${JSON.stringify(bd.unblocked)}`);
  if (!saf.safe) { console.error('  base not safe, skip'); return results; }
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
  console.error(`[base ${label}] single-move candidates=${tried} witnesses=${results.length}`);
  for (let i = 0; i < bd.n; i++) for (let j = i + 1; j < bd.n; j++) {
    for (const t of emptyCells) {
      const r = verifyCandidate(bd, [i, j], [t.slice()]);
      if (r) results.push({ kind: 'rem2add1', rem: [i, j], add: [t.slice()], stones: r.stones, rows: r.rows });
    }
  }
  console.error(`[base ${label}] after rem2add1 total=${results.length}`);
  if (doDouble) {
    let tried22 = 0;
    for (let i = 0; i < bd.n; i++) for (let j = i + 1; j < bd.n; j++) {
      for (let a = 0; a < emptyCells.length; a++) for (let b = a + 1; b < emptyCells.length; b++) {
        tried22++;
        const r = verifyCandidate(bd, [i, j], [emptyCells[a].slice(), emptyCells[b].slice()]);
        if (r) results.push({ kind: 'rem2add2', rem: [i, j], add: [emptyCells[a].slice(), emptyCells[b].slice()], stones: r.stones, rows: r.rows });
      }
    }
    console.error(`[base ${label}] rem2add2 candidates=${tried22} total=${results.length}`);
  }
  return results;
}

// ---- main ----
const fs = require('fs');
const mode = process.argv[2] || 'main';
const targetM = parseInt(process.argv[3] || '40', 10);
const stopAfter = process.argv[4] || 'none';  // quit after this many witnesses (safety)
const B = {
  m37: JSON.parse(fs.readFileSync(__dirname + '/../witnesses/s5x37q4.json', 'utf8')),
  m38: JSON.parse(fs.readFileSync(__dirname + '/../witnesses/s5x38q4.json', 'utf8')),
  m39: JSON.parse(fs.readFileSync(__dirname + '/../witnesses/s5x39q4.json', 'utf8')),
};
const W = 5, Q = 4;
const images = (S, m) => ({
  id: S.map(p => p.slice()),
  H: S.map(([x, y]) => [m - 1 - x, y]),
  V: S.map(([x, y]) => [x, 4 - y]),
  HV: S.map(([x, y]) => [m - 1 - x, 4 - y]),
});

let all = [];
const bases = [['m37', B.m37], ['m38', B.m38], ['m39', B.m39]];
if (mode === 'control') {
  for (const [lbl, S] of bases) {
    for (const [img, T] of Object.entries(images(S, targetM))) {
      const rs = surgery(T, W, targetM, Q, `${lbl}/${img}`, false);
      all.push({ base: `${lbl}/${img}`, found: rs.length, sample: rs.slice(0, 3).map(r => ({ kind: r.kind, stones: r.stones, rows: r.rows })) });
    }
  }
} else {
  outer:
  for (const [lbl, S] of bases) {
    for (const [img, T] of Object.entries(images(S, targetM))) {
      const rs = surgery(T, W, targetM, Q, `${lbl}/${img}`, true);
      for (const r of rs) all.push({ base: `${lbl}/${img}`, ...r });
      if (stopAfter !== 'none' && all.length >= parseInt(stopAfter, 10)) {
        console.error(`early stop after ${all.length} witnesses`);
        break outer;
      }
    }
  }
}
const out = { mode, w: W, m: targetM, q: Q, totalWitnesses: all.reduce((a, r) => a + (r.kind ? 1 : 0), 0),
  results: all.map(r => r.kind ? ({ base: r.base, kind: r.kind, rem: r.rem, add: r.add, stones: r.stones, rows: r.rows })
                                 : ({ base: r.base, found: r.found, sample: r.sample })) };
fs.writeFileSync(__dirname + `/../output/surgery-${mode}-m${targetM}.json`, JSON.stringify(out, null, 1));
console.log(`totalWitnesses=${out.totalWitnesses} written surgery-${mode}-m${targetM}.json`);
for (const r of all.slice(0, 10)) if (r.kind) console.log(JSON.stringify({ base: r.base, kind: r.kind, stones: r.stones, rows: r.rows }));
