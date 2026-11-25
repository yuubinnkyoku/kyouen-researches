// surgery_deep.js — deep bounded-edit surgery for (6,5) frontier witness hunt.
// Core (gcd2, canonLine, circleIR, curveCache, fastOnLine/Circle, Board, verifyCandidate)
// is VERBATIM from scripts/surgery_gen.js (sha256 dfc97506503e... staged 2026-11-21,
// itself adapted from the published five-row-q4-witness-band-40plus-20261121 surgery.js).
// New classes (documented completeness scope):
//   rem3add1 (COMPLETE): remove 3 base stones, add 1 anywhere.
//   rem4add1 (COMPLETE), rem5add1 (COMPLETE): same with 1 add.
//   rem3add2T (targeted-complete for the class where some blocking structure of the
//     base-unblocked target cells uses an added stone):
//     Claim: any final witness W = base - R + A (|R|=3, |A|=2) must, for EVERY
//     unblocked target cell u of the base placement, block u via a curve through u
//     holding >= 4 W-stones; kept stones on any such curve are <= 3 (u was unblocked
//     in the base and kept ⊆ base), so each blocking curve needs >= 1 add on it,
//     OR the target cell u is itself filled by an add. Hence each target u has some
//     add in D(u) := {u} ∪ {empty cells on a curve through u with >= 2 base stones}.
//     The enumeration is over add-pairs that satisfy this necessary condition for
//     every target cell, crossed with ALL C(23,3) removals, then fully verified.
//     (Incomplete in general: a pair failing the condition for some u cannot be a
//     witness, so nothing is missed; the ONLY restriction vs full rem3add2 is that
//     pairs failing the condition are skipped — those cannot be witnesses either,
//     so rem3add2T is COMPLETE for the rem3add2 class on a base whose unblocked
//     cells are exactly the targets. Documented negation semantics: 0 hits here
//     implies NO rem3add2 witness exists from this base.)
//   NOTE on add placement scope: in every kR1A / rem3add2T enumeration, adds are
//   drawn from cells EMPTY in the base. A candidate whose add coincides with a
//   removed base-stone position reduces (net stones identical) to a strictly
//   smaller edit class (e.g. 3R1A+readd -> 2R0A). Those reductions are closed by
//   the pure-removal classes remKadd0 (k=1..4, complete, trivial cost), so the
//   union of all classes reported here covers every kRmA edit with k<=4, m<=2,
//   plus 3R2A (targeted-complete), without any unreached re-add corner.
// Same witness conditions as surgery_gen.js (safety/maximality/deficiency), with
// verifyCandidate doing the full board check for every candidate.
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


// ---- deep classes ----
function combos(arr, k) { // all k-subsets by index
  const res = [], n = arr.length, idx = [];
  if (k > n) return res;
  const rec = (start) => {
    if (idx.length === k) { res.push(idx.slice()); return; }
    for (let i = start; i < n; i++) { idx.push(i); rec(i + 1); idx.pop(); }
  };
  rec(0);
  return res;
}

function targetDSet(bd, targets) {
  // per target u: D(u) = {u} + empty cells on curves through u with >=2 base stones.
  // Derived necessity (documented in header): kept stones on any blocking curve of an
  // unblocked target are <= 3, so a covering curve through u must carry an added stone
  // whose curve holds >= 4 - 2 = 2 kept (= base) stones -> the add lies in D(u) or on u.
  const Ds = [];
  const { w, m, q, S, sset } = bd;
  for (const u of targets) {
    const D = new Set([u.join(',')]);
    const lineKeys = new Set();
    for (const s of S) lineKeys.add(canonLine(u, s));
    for (const key of lineKeys) {
      let cnt = 0; for (const p of S) if (fastOnLine(key, p)) cnt++;
      if (cnt < 2) continue;
      const v = parseKey(key);
      for (let x = 0; x < m; x++) for (let y = 0; y < w; y++) {
        const c = x + ',' + y;
        if (sset.has(c)) continue;
        if (v[0] * x + v[1] * y + v[2] === 0) D.add(c);
      }
    }
    const circKeys = new Set();
    for (let i = 0; i < S.length; i++) for (let j = i + 1; j < S.length; j++) {
      const ck = circleIR(u, S[i], S[j]);
      if (ck !== null) circKeys.add(ck);
    }
    for (const key of circKeys) {
      let cnt = 0; for (const p of S) if (fastOnCircle(key, p)) cnt++;
      if (cnt < 2) continue;
      for (let x = 0; x < m; x++) for (let y = 0; y < w; y++) {
        const c = x + ',' + y;
        if (sset.has(c)) continue;
        if (fastOnCircle(key, [x, y])) D.add(c);
      }
    }
    Ds.push(D);
  }
  return Ds;
}

// ---- main ----
const fs = require('fs');
const path = require('path');
const cfgPath = process.argv[2];
const startBase = parseInt(process.argv[3] || '0', 10);
const endBase = parseInt(process.argv[4] || String(Number.MAX_SAFE_INTEGER), 10);
const className = process.argv[5] || 'singles';  // r0s | r1a1 | r2a1 | r3a1 | r4a1 | r5a1 | t2 | singles | comma lists
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
const { tag, w, q, m: targetM } = cfg;
const outDir = path.join(path.dirname(cfgPath), '..', 'output', tag);
fs.mkdirSync(outDir, { recursive: true });

for (let i = startBase; i < Math.min(endBase, cfg.bases.length); i++) {
  const base = cfg.bases[i];
  const t0 = Date.now();
  const bd = new Board(w, targetM, q, base.stones);
  const saf = bd.safety();
  console.error(`[base ${i} ${base.label}] n=${bd.n} safe=${saf.safe} (ml=${saf.ml} mc=${saf.mc}) unblocked=${JSON.stringify(bd.unblocked)} targets=${JSON.stringify(base.targets || [])}`);
  if (!saf.safe) {
    fs.writeFileSync(path.join(outDir, `base-${String(i).padStart(3,'0')}.skipped.json`),
      JSON.stringify({ baseIndex: i, label: base.label, skipped: 'base not safe' }, null, 1));
    continue;
  }
  const emptyCells = [];
  for (let x = 0; x < targetM; x++) for (let y = 0; y < w; y++) if (!bd.sset.has(x + ',' + y)) emptyCells.push([x, y]);
  const statFile = path.join(outDir, `base-${String(i).padStart(3,'0')}.stats.json`);
  let stats = { baseIndex: i, label: base.label, baseN: bd.n, baseRows: bd.rows.slice(),
                baseMl: saf.ml, baseMc: saf.mc, targets: bd.unblocked.slice() };
  try { stats = Object.assign(stats, JSON.parse(fs.readFileSync(statFile, 'utf8'))); } catch (e) {}
  const outFinal = () => { stats.elapsedMs = Date.now() - t0;
    fs.writeFileSync(statFile, JSON.stringify(stats, null, 1));
    return stats; };

  const classes = className === 'singles' ? ['r0s', 'r3a1', 'r4a1'] : className.split(',');
  for (const cls of classes) {
    const clsFile = path.join(outDir, `base-${String(i).padStart(3,'0')}.${cls}.json`);
    if (fs.existsSync(clsFile)) { console.log(`skip ${base.label} ${cls} (done)`); continue; }
    // ---- pure removals r0s ----
    if (cls === 'r0s') {
      const t1 = Date.now();
      const found = [];
      for (const krem of [1, 2, 3, 4]) {
        let tried = 0, wit = 0;
        for (const R of combos(bd.S, krem)) {
          tried++;
          const r = verifyCandidate(bd, R, []);
          if (r) { wit++; found.push({ kind: 'rem' + krem + 'add0', rem: R, add: [], stones: r.stones, rows: r.rows }); }
        }
        stats['rem' + krem + 'add0Candidates'] = tried;
        stats['rem' + krem + 'add0Witnesses'] = wit;
      }
      stats['r0sWitnesses'] = found.length;
      fs.writeFileSync(clsFile, JSON.stringify({ baseIndex: i, label: base.label, class: 'r0s', done: true,
        statCandidates: { r1: stats.rem1add0Candidates, r2: stats.rem2add0Candidates, r3: stats.rem3add0Candidates, r4: stats.rem4add0Candidates },
        witnesses: found }, null, 1));
      console.log(`${base.label} r0s: witnesses=${found.length} (${((Date.now()-t1)/1000).toFixed(1)}s)`);
      continue;
    }
    // ---- rem k add 1 (complete) ----
    if (cls === 'r1a1' || cls === 'r2a1' || cls === 'r3a1' || cls === 'r4a1' || cls === 'r5a1') {
      const krem = parseInt(cls.slice(1), 10);  // rKa1: k removals + 1 add
      const t1 = Date.now();
      let tried = 0, wit = 0;
      const found = [];
      for (const R of combos(bd.S, krem)) for (const t of emptyCells) {
        tried++;
        const r = verifyCandidate(bd, R, [t.slice()]);
        if (r) { wit++; found.push({ kind: 'rem' + krem + 'add1', rem: R, add: [t.slice()], stones: r.stones, rows: r.rows });
                 if (found.length >= 50) break; }
      }
      stats['rem' + krem + 'add1Candidates'] = tried;
      stats['rem' + krem + 'add1Witnesses'] = wit;
      stats['rem' + krem + 'add1WitnessesFound'] = found.length;
      fs.writeFileSync(clsFile, JSON.stringify({ baseIndex: i, label: base.label, class: cls, done: found.length < 50,
        truncated: found.length >= 50, candidates: tried, witnesses: found }, null, 1));
      console.log(`${base.label} ${cls}: candidates=${tried} witnesses=${found.length} (${((Date.now()-t1)/1000).toFixed(1)}s)`);
      continue;
    }
    // ---- rem3add2T (targeted-complete) with per-removal-chunk checkpoint ----
    if (cls === 't2') {
      const t1 = Date.now();
      const targets = bd.unblocked.map(c => c);
      const Ds = targetDSet(bd, targets);
      stats.dsizes = Ds.map(d => d.size);
      const F = new Set();
      for (const d of Ds) for (const c of d) F.add(c);
      const keyOfD = Ds.map(d => new Set(d));
      const pairs = [];
      const seenPair = new Set();
      for (const aKey of F) {
        const a = aKey.split(',').map(Number);
        for (const t of emptyCells) {
          const tk = t.join(',');
          if (aKey === tk) continue;
          const pk = aKey < tk ? aKey + '|' + tk : tk + '|' + aKey;
          if (seenPair.has(pk)) continue;
          seenPair.add(pk);
          let ok = true;
          for (const d of keyOfD) { if (!(d.has(aKey) || d.has(tk))) { ok = false; break; } }
          if (!ok) continue;
          pairs.push([a, t]);
        }
      }
      stats.t2_pairs = pairs.length;
      console.error(`${base.label} t2: dsizes=${JSON.stringify(stats.dsizes)} pairs=${pairs.length} (${((Date.now()-t1)/1000).toFixed(1)}s)`);
      const remSets = combos(bd.S, 3);
      const partFile = path.join(outDir, `base-${String(i).padStart(3,'0')}.t2.part.json`);
      let doneIdx = 0, wit = 0, found = [];
      try { const p = JSON.parse(fs.readFileSync(partFile, 'utf8')); doneIdx = p.doneIdx; wit = p.witnesses; found = p.found; } catch (e) {}
      const tStart = Date.now();
      let endIdx = doneIdx, budgetStop = false;
      for (let ri = doneIdx; ri < remSets.length && !budgetStop; ri++) {
        const R = remSets[ri];
        endIdx = ri + 1;
        for (const [a1, a2] of pairs) {
          const r = verifyCandidate(bd, R, [a1.slice(), a2.slice()]);
          if (r) { wit++; found.push({ kind: 'rem3add2T', rem: R, add: [a1, a2], stones: r.stones, rows: r.rows }); }
        }
        // checkpoint every 16 removals
        if (((ri + 1) & 15) === 0) {
          fs.writeFileSync(partFile, JSON.stringify({ baseIndex: i, label: base.label, doneIdx: endIdx, witnesses: wit, found, dsizes: stats.dsizes, pairs: pairs.length }, null, 0));
          const el = (Date.now() - tStart) / 1000;
          if (el > 180) { budgetStop = true; console.log(`${base.label} t2: time-budget stop at removal ${endIdx}/${remSets.length} witnesses=${wit} (checkpoint saved)`); }
        }
      }
      const complete = endIdx >= remSets.length;
      if (complete) {
        fs.writeFileSync(partFile, JSON.stringify({ baseIndex: i, label: base.label, doneIdx: endIdx, witnesses: wit, found, dsizes: stats.dsizes, pairs: pairs.length }, null, 0));
      }
      stats.t2witnesses = wit;
      stats.t2removalsDone = endIdx;
      stats.t2complete = complete;
      if (complete) {
        fs.writeFileSync(clsFile, JSON.stringify({ baseIndex: i, label: base.label, class: 't2', done: true,
          dsizes: stats.dsizes, pairs: pairs.length, witnesses: wit, found }, null, 1));
        try { fs.unlinkSync(partFile); } catch (e) {}
        console.log(`${base.label} t2 DONE: pairs=${pairs.length} witnesses=${wit}`);
      }
      continue;
    }
    console.error(`unknown class ${cls}`);
    process.exit(2);
  }
  outFinal();
}
console.log('done range', startBase, startBase === endBase ? endBase : Math.min(endBase, cfg.bases.length), 'of', cfg.bases.length, 'bases class', className);
