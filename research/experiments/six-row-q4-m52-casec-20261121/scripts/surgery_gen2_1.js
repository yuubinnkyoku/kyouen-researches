#!/usr/bin/env node
// surgery_gen2.1.js — generalized bounded-edit surgery for (w,m,q) witnesses,
// COMPLETE add enumeration (case-c included) and COMPLETE remove budget classes
// 1R1A / 2R1A / 2R2A / 3R1A / 3R2A. (3R3A out of scope by declaration.)
//
// Lane: six-row (6,4) m=52 case-c-complete escalation; controls: five-row
// (5,4) K1209 m39->40 (64 hits) and six-row (6,4) K1211 47->48 (4 witnesses).
// Single-owner declaration: research/log/2026-11-21-five-row-q4-band-41plus-and-six-row-q4-m52-casec-single-owner-note.md (commit bab006adc).
//
// Curve engine (canonLine/circleIR/parseKey/fastOnLine/fastOnCircle/Board)
// reused VERBATIM from the published K1209 surgery.js
// (sha256 0410d787a53ffadda3bc44b9c31b423ce4a38ab4798b28e279230cfb73ab7e25).
//
// COMPLETENESS statement (vs the published engine, which enumerated blocking
// curves for uncovered cells only through (cell, added, kept) triples and thus
// missed witnesses whose covering curve holds one surviving seed stone plus
// BOTH added stones — K1211's case-c gap, 56/64 on its K1209 control):
//
//   Let S be the safe+maximal seed (witness on w x m', maxx+1 <= m <= m'),
//   R a set of <=3 removed seed stones, A the set of <=2 added cells,
//   S2 = (S \ R) + A on the board w x m. Then S2 covers cell u iff some curve
//   holds >= q-1 = 3 points of S2 through u.
//   (a) A curve with no added point is a base curve; base safety gives it
//       <= 3 seed stones and removals only shrink it, so such curves keep
//       exactly the coverage they had in S. For a cell that was ALREADY
//       covered by a base curve all of whose stones survive (mask & R = 0),
//       nothing changes. NEEDED(R) = cells with NO surviving base mask. Only
//       those cells require new coverage.
//   (b) A new covering curve for u in NEEDED(R) contains an added point.
//   REMARK (gen2.1 fix): a kA=2 covering curve can be determined by (u,a,b)
//   alone - e.g. the circumcircle of u,a,b holding exactly ONE surviving seed
//   stone and no removed stone. It is NOT a >=2-seed-stone base curve, so it
//   never enters the precomputed CUR(u); the kA=2 sweep catches it with an
//   on-the-fly curve(u,a,b) survivor test. This closed the 56/64 -> 64/64 gap
//   on the K1209 m39->40 control (missing orbits 1,15)
//       (else it is a base curve, case (a)). With |A| <= 2 the point count on
//       the curve from S2 is: 1 add + (#surviving seed stones on it) [+1 if
//       the second add lies on it]. So coverage of u by {a,b} (or single a)
//       reduces to: u occupied by an add, or a curve through u with >=2
//       surviving seeds containing an add ("strong"), or a curve through u
//       with exactly 1 surviving seed containing BOTH adds (case c).
//   This engine precomputes, per empty cell u, ALL curves through u holding
//   >= 2 seed stones (line if u collinear with the pair, else the circumcircle
//   of u and the pair), so the classification above is exhaustive. Final
//   certification of every prefilter passer is a complete on-board check
//   (rows, complete safety over S2, complete maximality) — the prefilter is
//   only a sound rejection stage.
//
// Determinism: fixed iteration order, pure integer arithmetic, no randomness.

'use strict';

// ======== verbatim curve engine from published K1209 surgery.js ========
const gcd2 = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; };

function canonLine(p, r) {
  let A = r[1] - p[1], B = p[0] - r[0], C = r[0] * p[1] - r[1] * p[0];
  const g = gcd2(gcd2(A, B), C) || 1;
  A /= g; B /= g; C /= g;
  if (A < 0 || (A === 0 && (B < 0 || (B === 0 && C < 0)))) { A = -A; B = -B; C = -C; }
  return A + ',' + B + ',' + C;
}

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
    this.blockingMask = new Map();
    this.unblocked = [];
    for (let x = 0; x < m; x++) for (let y = 0; y < w; y++) {
      const c = x + ',' + y;
      if (this.sset.has(c)) continue;
      const masks = [];
      for (const [key, st] of lineMap) if (fastOnLine(key, [x, y]) && st.size >= q - 1) masks.push(st);
      for (const [key, st] of circMap) if (fastOnCircle(key, [x, y]) && st.size >= q - 1) masks.push(st);
      if (masks.length === 0) this.unblocked.push([x, y]);
      this.blocking.set(c, masks);
      const mInts = [];
      for (const st of masks) { let mi = 0; for (const i of st) mi |= (1 << i); mInts.push(mi); }
      this.blockingMask.set(c, mInts);
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
// ======== end verbatim curve engine (Board extended with integer masks) ========

const POP = new Uint8Array(1 << 17);
for (let i = 1; i < POP.length; i++) POP[i] = POP[i >> 1] + (i & 1);

// complete safety of a stone list
function safetyOf(stones, q) {
  const n = stones.length;
  let ml = 0, mc = 0;
  const lineMap = new Map();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    const k = canonLine(stones[i], stones[j]); lineMap.set(k, (lineMap.get(k) || 0) + 1);
  }
  for (const k of lineMap.keys()) { let c = 0; for (const p of stones) if (fastOnLine(k, p)) c++; ml = Math.max(ml, c); }
  const keys = new Set();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) for (let k2 = j + 1; k2 < n; k2++) {
    const ck = circleIR(stones[i], stones[j], stones[k2]); if (ck) keys.add(ck);
  }
  for (const k of keys) { let c = 0; for (const p of stones) if (fastOnCircle(k, p)) c++; mc = Math.max(mc, c); }
  return ml < q && mc < q;
}

// complete witness certification of S2 = kept + adds
function verifyComplete(board, remIdxs, addCells) {
  const { w, m, q } = board;
  const rem = new Set(remIdxs);
  const kept = board.S.filter((_, i) => !rem.has(i));
  const S2 = kept.concat(addCells.map(a => a.slice()));
  const n2 = S2.length;
  if (n2 !== new Set(S2.map(p => p.join(','))).size) return null;
  const rows = new Array(w).fill(0);
  for (const [, y] of S2) rows[y]++;
  for (const c of rows) if (c > q - 1) return null;
  if (!rows.some(c => c <= q - 2)) return null;
  if (!safetyOf(S2, q)) return null;
  const sset = new Set(S2.map(p => p.join(',')));
  for (let x = 0; x < m; x++) for (let y = 0; y < w; y++) {
    const ck2 = x + ',' + y;
    if (sset.has(ck2)) continue;
    let blockedFlag = false;
    const masks = board.blocking.get(ck2);
    if (masks) {
      for (const mask of masks) {
        let ok = true;
        for (const i of rem) if (mask.has(i)) { ok = false; break; }
        if (ok) { blockedFlag = true; break; }
      }
    }
    if (!blockedFlag) {
      // new curves through an added stone: line(u,t) and circles(u,t,s), s in S2
      for (const t of addCells) {
        const lk = canonLine([x, y], t);
        let c = 0; for (const p of S2) if (fastOnLine(lk, p)) c++;
        if (c >= q - 1) { blockedFlag = true; break; }
        for (const s of S2) {
          if (s === t || (s[0] === x && s[1] === y)) continue;
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

// -------- per-seed precompute --------
function precompute(board) {
  const { m, w } = board;
  const empties = [];
  for (let x = 0; x < m; x++) for (let y = 0; y < w; y++) if (!board.sset.has(x + ',' + y)) empties.push([x, y]);
  const E = empties.length;
  const WORDS = (E + 31) >> 5;
  const ordOf = new Map(empties.map((p, i) => [p[0] + ',' + p[1], i]));
  const cellOrd = (p) => ordOf.get(p[0] + ',' + p[1]);

  // CUR[c]: curves through empty cell c with >= 2 seed stones.
  // per cell: recMask[] (int), recWords[] (WORDS each, bits over empty ordinals on the curve)
  const cur = new Array(E);
  const n = board.n;
  for (let ci = 0; ci < E; ci++) {
    const c = empties[ci];
    const seen = new Map(); // key -> recIdx
    const recMask = [];
    const recWords = []; // flat, WORDS per rec
    const addRec = (key) => {
      if (seen.has(key)) return; // dedupe (first computation wins)
      const isCircle = key.indexOf(',', key.indexOf(',', key.indexOf(',') + 1) + 1) >= 0; // 4th component
      // count seed stones on key
      let mask = 0;
      for (let i = 0; i < n; i++) {
        const p = board.S[i];
        const on = isCircle ? fastOnCircle(key, p) : fastOnLine(key, p);
        if (on) mask |= (1 << i);
      }
      if (POP[mask] < 2) return; // only curves with >=2 seed stones matter
      let words = new Uint32Array(WORDS);
      for (let ei = 0; ei < E; ei++) {
        const e = empties[ei];
        const on = isCircle ? fastOnCircle(key, e) : fastOnLine(key, e);
        if (on) words[ei >> 5] |= (1 << (ei & 31));
      }
      seen.set(key, recMask.length);
      recMask.push(mask);
      recWords.push(words);
    };
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
      const lk = canonLine(board.S[i], board.S[j]);
      if (fastOnLine(lk, c)) { addRec(lk); continue; }
      const ck = circleIR(c, board.S[i], board.S[j]);
      if (ck === null) continue;
      addRec(ck);
    }
    cur[ci] = { recMask: Int32Array.from(recMask), recWords, count: recMask.length };
  }
  return { empties, E, WORDS, ordOf, cellOrd, cur };
}

// -------- class sweep --------
function classSweep(board, pc, kR, kA, label) {
  const { empties, E, WORDS, ordOf, cur } = pc;
  const { w, q } = board;
  const n = board.n;
  const NEED = q - 1;
  const remLists = [];
  const stack = [];
  const genRem = (start) => {
    if (stack.length === kR) { remLists.push(stack.slice()); return; }
    for (let i = start; i < n; i++) { stack.push(i); genRem(i + 1); stack.pop(); }
  };
  genRem(0);

  const results = [];
  let tried = 0, passFrontier = 0, passVerify = 0;
  const cellKeys = [];
  for (let x = 0; x < board.m; x++) for (let y = 0; y < w; y++) if (!board.sset.has(x + ',' + y)) cellKeys.push(x + ',' + y);

  // alloc reusable per-rem structures
  let strongW = []; const k1List = [];
  let neededIdx = new Int32Array(E);

  for (const rem of remLists) {
    let remBits = 0; for (const i of rem) remBits |= (1 << i);
    const keptMask = ~remBits & ((1 << n) - 1);
    const keptList = [];
    for (let i = 0; i < n; i++) if ((remBits & (1 << i)) === 0) keptList.push(i);
    // NEEDED cells: no surviving base mask
    let nNeeded = 0;
    for (let ci = 0; ci < E; ci++) {
      const masks = board.blockingMask.get(cellKeys[ci]);
      let alive = false;
      if (masks) for (const mi of masks) { if ((mi & remBits) === 0) { alive = true; break; } }
      if (!alive) neededIdx[nNeeded++] = ci;
    }
    // (nNeeded === 0 is handled uniformly: the coverage loop below trivially
    // passes; the cheap row check and verifyComplete do the real filtering.)
    // classify per needed cell
    strongW = [];
    k1List.length = 0;
    for (let t = 0; t < nNeeded; t++) {
      const ci = neededIdx[t];
      const { recMask, recWords, count } = cur[ci];
      const sw = new Uint32Array(WORDS);
      const k1 = [];
      for (let r = 0; r < count; r++) {
        const k = POP[recMask[r] & keptMask];
        if (k >= 2) {
          const src = recWords[r];
          for (let wi = 0; wi < WORDS; wi++) sw[wi] |= src[wi];
        } else if (k === 1 && kA === 2) {
          k1.push(r);
        }
      }
      strongW.push(sw); k1List.push(k1);
    }
    // cheap row-capacity/deficiency check for a candidate (adds vs rem)
    const rowsOK = (a, b) => {
      const rowsN = board.rows.slice();
      for (const i of rem) rowsN[board.S[i][1]]--;
      const ry = empties[a][1]; rowsN[ry]++;
      if (rowsN[ry] > q - 1) return false;
      if (b >= 0) { const ry2 = empties[b][1]; rowsN[ry2]++; if (rowsN[ry2] > q - 1) return false; }
      if (!rowsN.some(c => c <= q - 2)) return false;
      return true;
    };
    if (kA === 1) {
      for (let a = 0; a < E; a++) {
        tried++;
        let ok = true;
        for (let t = 0; t < nNeeded; t++) {
          if (a === neededIdx[t]) continue;
          const sw = strongW[t];
          if (((sw[a >> 5] >> (a & 31)) & 1) === 0) { ok = false; break; }
        }
        if (!ok) continue;
        passFrontier++;
        if (!rowsOK(a, -1)) continue;
        const r = verifyComplete(board, rem, [empties[a]]);
        if (r) { passVerify++; results.push({ kind: `${kR}R${kA}A`, rem: rem.slice(), add: [empties[a].slice()], stones: r.stones, rows: r.rows }); }
      }
    } else {
      for (let a = 0; a < E; a++) {
        const swA = null; // placeholder to keep symmetric structure readable
        for (let b = a + 1; b < E; b++) {
          tried++;
          let ok = true;
          for (let t = 0; t < nNeeded; t++) {
            if (a === neededIdx[t] || b === neededIdx[t]) continue;
            const sw = strongW[t];
            if (((sw[a >> 5] >> (a & 31)) & 1) !== 0) continue;
            if (((sw[b >> 5] >> (b & 31)) & 1) !== 0) continue;
            let cov = false;
            const k1 = k1List[t];
            for (let ki = 0; ki < k1.length; ki++) {
              const rw = cur[neededIdx[t]].recWords[k1[ki]];
              if (((rw[a >> 5] >> (a & 31)) & 1) && ((rw[b >> 5] >> (b & 31)) & 1)) { cov = true; break; }
            }
            if (!cov) {
              // FINAL case-c (gen2.1): the covering curve is determined by the
              // needed cell and BOTH adds alone and holds exactly ONE surviving
              // seed stone and no removed stone => it is not a >=2-seed-stone
              // base curve and hence absent from the precomputed CUR(t).
              // Coverage: stones = a + b + kept >= q-1 = 3 iff >=1 surviving
              // seed lies on curve(t,a,b). On-the-fly, fixed order, complete:
              // the kA=2 classification is then exactly
              //   occupy / strong / k1(>=2 base seeds) / curve(t,a,b) survivor.
              const c2 = empties[neededIdx[t]];
              const pa = empties[a], pb = empties[b];
              const cross = (pa[0] - c2[0]) * (pb[1] - c2[1]) - (pa[1] - c2[1]) * (pb[0] - c2[0]);
              if (cross === 0) {
                const lkk = canonLine(c2, pa);
                for (let ki2 = 0; ki2 < keptList.length; ki2++) {
                  if (fastOnLine(lkk, board.S[keptList[ki2]])) { cov = true; break; }
                }
              } else {
                const ckk = circleIR(c2, pa, pb);
                if (ckk !== null) {
                  for (let ki2 = 0; ki2 < keptList.length; ki2++) {
                    if (fastOnCircle(ckk, board.S[keptList[ki2]])) { cov = true; break; }
                  }
                }
              }
            }
            if (!cov) { ok = false; break; }
          }
          if (!ok) continue;
          passFrontier++;
          if (!rowsOK(a, b)) continue;
          const r = verifyComplete(board, rem, [empties[a].slice(), empties[b].slice()]);
          if (r) { passVerify++; results.push({ kind: `${kR}R${kA}A`, rem: rem.slice(), add: [empties[a].slice(), empties[b].slice()], stones: r.stones, rows: r.rows }); }
        }
      }
    }
  }
  console.error(`[${label}] ${kR}R${kA}A: tried=${tried} passFrontier=${passFrontier} witnesses=${results.length}`);
  return { tried, passFrontier, witnesses: results };
}

// -------- main --------
const fs = require('fs');
const cfgPath = process.argv[2];
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
const { w, m, q, seed, classes, label } = cfg;
const board = new Board(w, m, q, seed);
const saf = board.safety();
console.error(`[seed ${label}] n=${board.n} rows=${JSON.stringify(board.rows)} safe=${saf.safe} (ml=${saf.ml} mc=${saf.mc}) unblocked=${board.unblocked.length}`);
if (!saf.safe) { console.error('seed not safe, abort'); process.exit(1); }
const t0 = Date.now();
const pc = precompute(board);
console.error(`[seed ${label}] precompute done in ${Date.now() - t0}ms (E=${pc.E})`);
const out = { label, w, m, q, seed, seedSafe: saf, seedUnblocked: board.unblocked, counts: {}, witnesses: [] };
for (const cls of classes) {
  const mm = cls.match(/^(\d)R(\d)A$/);
  if (!mm) continue;
  const kR = parseInt(mm[1], 10), kA = parseInt(mm[2], 10);
  const tc = Date.now();
  const r = classSweep(board, pc, kR, kA, label);
  console.error(`[${label}] ${cls} done in ${Date.now() - tc}ms`);
  out.counts[cls] = { tried: r.tried, passFrontier: r.passFrontier, witnesses: r.witnesses.length };
  for (const wit of r.witnesses) out.witnesses.push(wit);
}
const outPath = process.argv[3] || cfg.out || (cfgPath.replace(/\.json$/, '') + '-result.json');
fs.writeFileSync(outPath, JSON.stringify(out, null, 1));
console.log(`written ${outPath}: witnesses=${out.witnesses.length}`);
