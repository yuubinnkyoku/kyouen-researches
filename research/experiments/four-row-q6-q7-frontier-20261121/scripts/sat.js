// deficient-maximal SAT machinery for w x m q-point circle/line boards (fixed-width kyouen).
// Exact integer arithmetic in doubles (all values < 2^53 for board sizes used here;
// for very large boards switch to BigInt variants).
// Census: lines via pairs, circles via triples; canonical integer (A,B,C,D)/(a,b,c).
// Usage: node sat_kyouen.js census w m q | brute w m q | sat w m q [--cap=K] [--dpll]
'use strict';

function pts(w, m) { const P = []; for (let y = 0; y < w; y++) for (let x = 0; x < m; x++) P.push([x, y]); return P; }
function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a; }

// circle through p1,p2,p3 (non-collinear): A(x^2+y^2)+Bx+Cy+D=0, canonical integer form.
function circleABC(p1, p2, p3) {
  const [x1, y1] = p1, [x2, y2] = p2, [x3, y3] = p3;
  const s1 = x1 * x1 + y1 * y1, s2 = x2 * x2 + y2 * y2, s3 = x3 * x3 + y3 * y3;
  // solve [[x1,y1,1],[x2,y2,1],[x3,y3,1]] [b,c,d]^T = [-s1,-s2,-s3]; multiply by det.
  const det = x1 * (y2 - y3) - y1 * (x2 - x3) + (x2 * y3 - x3 * y2);
  if (det === 0) return null; // collinear (line covers it)
  const B = s1 * (y2 - y3) - y1 * (s2 - s3) + (s2 * y3 - s3 * y2);
  const C = x1 * (s2 - s3) - s1 * (x2 - x3) + (x2 * s3 - x3 * s2);
  const D = x1 * (y2 * s3 - y3 * s2) - y1 * (x2 * s3 - x3 * s2) + s1 * (x2 * y3 - x3 * y2);
  let a = det, b = -B, c = -C, d = -D;
  const g = gcd(gcd(gcd(a, b), c), d);
  if (g > 1) { a /= g; b /= g; c /= g; d /= g; }
  if (a < 0 || (a === 0 && (b < 0 || (b === 0 && (c < 0 || (c === 0 && d < 0)))))) { a = -a; b = -b; c = -c; d = -d; }
  return [a, b, c, d];
}
const onCircle = (co, x, y) => co[0] * (x * x + y * y) + co[1] * x + co[2] * y + co[3] === 0;

function lineABC(p1, p2) {
  const [x1, y1] = p1, [x2, y2] = p2;
  let a = y2 - y1, b = x1 - x2, c = x2 * y1 - x1 * y2;
  const g = gcd(gcd(a, b), c);
  if (g > 1) { a /= g; b /= g; c /= g; }
  if (a < 0 || (a === 0 && b < 0)) { a = -a; b = -b; c = -c; }
  return [a, b, c];
}
const onLine = (lo, x, y) => lo[0] * x + lo[1] * y + lo[2] === 0;

function buildCensus(w, m, q) {
  const P = pts(w, m), n = P.length;
  const lineMap = new Map();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    const lo = lineABC(P[i], P[j]);
    const key = lo[0] + ',' + lo[1] + ',' + lo[2];
    if (!lineMap.has(key)) lineMap.set(key, lo);
  }
  const circMap = new Map();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    const pi = P[i], pj = P[j];
    for (let k = j + 1; k < n; k++) {
      const co = circleABC(pi, pj, P[k]);
      if (co === null) continue;
      const key = co.join(',');
      if (!circMap.has(key)) circMap.set(key, co);
    }
  }
  const curves = [];
  for (const lo of lineMap.values()) {
    const set = [];
    for (let idx = 0; idx < n; idx++) if (onLine(lo, P[idx][0], P[idx][1])) set.push(idx);
    if (set.length >= q) curves.push({ type: 'line', co: lo, pts: set });
  }
  for (const co of circMap.values()) {
    const set = [];
    for (let idx = 0; idx < n; idx++) if (onCircle(co, P[idx][0], P[idx][1])) set.push(idx);
    if (set.length >= q) curves.push({ type: 'circle', co: co, pts: set });
  }
  return { P, n, curves };
}

// ---------- DIMACS encoding ----------
class Enc {
  constructor() { this.nv = 0; this.clauses = []; }
  v() { return ++this.nv; }
  add(cls) { for (let c of cls) { c = c.filter(l => l !== 0); if (c.length) this.clauses.push(c); } }
}
// sequential >=-counter over xs up to level K; s[i][j] === ">=j among xs[0..i]".
function counter(enc, xs, K) {
  const nE = xs.length;
  const s = Array.from({ length: nE }, () => new Array(K + 1).fill(0));
  for (let i = 0; i < nE; i++) for (let j = 1; j <= Math.min(K, i + 1); j++) s[i][j] = enc.v();
  for (let i = 0; i < nE; i++) for (let j = 1; j <= Math.min(K, i + 1); j++) {
    const S = s[i][j];
    if (i === 0) {
      enc.add([[xs[0], -S]]);   // x0 -> s[0][1]
      enc.add([[-xs[0], S]]);   // s[0][1] -> x0
    } else {
      const Sp = (j <= i) ? s[i - 1][j] : 0;
      const Spp = (j >= 2 && j - 1 <= i) ? s[i - 1][j - 1] : 0;
      if (j <= i) {
        enc.add([[-S, Sp, xs[i]]]);            // S -> Sp or xi
        if (Spp) enc.add([[-S, Sp, Spp]]);     // S -> Sp or Spp
        enc.add([[-Sp, S]]);                   // Sp -> S
        if (Spp) enc.add([[-xs[i], -Spp, S]]); // xi & Spp -> S
        else enc.add([[-xs[i], S]]);           // j==1: xi -> S
      } else {
        // j == i+1: S <-> xi & Spp
        enc.add([[-S, xs[i]]]);
        enc.add([[-S, Spp]]);
        enc.add([[-xs[i], -Spp, S]]);
      }
    }
  }
  return s;
}

function encode(w, m, q, opts = {}) {
  const { P, n, curves } = buildCensus(w, m, q);
  const enc = new Enc();
  const counters = [];
  const cell = new Array(n).fill(0).map(() => enc.v());
  const geVars = [];
  for (const cu of curves) {
    const K = q;
    const xs = cu.pts.map(p => cell[p]);
    const s = counter(enc, xs, K);
    counters.push({ xs, s, tag: cu.type + ':' + cu.co.join(',') });
    const last = s[cu.pts.length - 1];
    enc.add([[-last[q]]]);        // safety: <= q-1 stones per curve
    geVars.push(last[q - 1]);    // blocking signal: >= q-1 stones on curve
  }
  const through = Array.from({ length: n }, () => []);
  curves.forEach((cu, ci) => { for (const p of cu.pts) through[p].push(geVars[ci]); });
  for (let i = 0; i < n; i++) enc.add([[cell[i], ...through[i]]]); // maximality
  let mode = 'total';
  if (opts.maxStones != null) {
    mode = 'total';
    const K = opts.maxStones + 1;
    const xs = cell.slice();
    const s = counter(enc, xs, K);
    counters.push({ xs, s, tag: 'TOTAL' });
    enc.add([[-s[n - 1][K]]]); // total <= maxStones
  } else if (opts.deficientRow !== false) {
    // deficient (default): some row has <= q-2 stones. Since safety caps every row
    // at <= q-1, this is equivalent to total <= w(q-1)-1. Single clause: not all
    // rows have >= q-1 stones. Rows are lines with co = (0,1,-y).
    mode = 'row-deficient';
    const rowGe = [];
    curves.forEach((cu, ci) => { if (cu.type === 'line' && cu.co[0] === 0 && cu.co[1] === 1) rowGe.push(-geVars[ci]); });
    if (rowGe.length !== w) throw new Error('row curves miscount ' + rowGe.length);
    enc.add([rowGe]);
  }
  return { enc, cell, curves, P, through, counters, mode };
}

function toDimacs(enc) {
  const out = ['p cnf ' + enc.nv + ' ' + enc.clauses.length];
  for (const c of enc.clauses) out.push(c.join(' ') + ' 0');
  return out.join('\n');
}

// ---------- independent census-free verifier ----------
function verifyConfig(w, m, q, stones) {
  const S = new Set(stones.map(p => p[0] + ',' + p[1]));
  const st = stones.map(p => [p[0], p[1]]);
  const N = st.length;
  const cntOn = (co, type) => {
    let cnt = 0;
    for (const [x, y] of st) if (type === 'line' ? onLine(co, x, y) : onCircle(co, x, y)) cnt++;
    return cnt;
  };
  const seenLine = new Set(), seenCirc = new Set();
  for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) {
    const lo = lineABC(st[i], st[j]); const key = lo.join(',');
    if (!seenLine.has(key)) { seenLine.add(key); if (cntOn(lo, 'line') >= q) return { ok: false, why: 'unsafe-line', co: key }; }
    for (let k = j + 1; k < N; k++) {
      const co = circleABC(st[i], st[j], st[k]);
      if (!co) continue;
      const ckey = co.join(',');
      if (!seenCirc.has(ckey)) { seenCirc.add(ckey); if (cntOn(co, 'circle') >= q) return { ok: false, why: 'unsafe-circle', co: ckey }; }
    }
  }
  for (let y = 0; y < w; y++) for (let x = 0; x < m; x++) {
    if (S.has(x + ',' + y)) continue;
    let blocked = false;
    const seen = new Set();
    outer:
    for (let i = 0; i < N; i++) {
      const lo = lineABC([x, y], st[i]); const key = lo.join(',');
      if (!seen.has(key)) { seen.add(key); if (cntOn(lo, 'line') >= q - 1) { blocked = true; break outer; } }
      for (let j = i + 1; j < N; j++) {
        const co = circleABC([x, y], st[i], st[j]);
        if (!co) continue;
        const ckey = co.join(',');
        if (!seen.has(ckey)) { seen.add(ckey); if (cntOn(co, 'circle') >= q - 1) { blocked = true; break outer; } }
      }
    }
    if (!blocked) return { ok: false, why: 'not-maximal', cell: x + ',' + y };
  }
  const rows = Array(w).fill(0);
  for (const [x, y] of st) rows[y]++;
  return { ok: true, size: N, rows, minRow: Math.min(...rows) };
}

// ---------- CDCL (watched literals, VSIDS, 1UIP, restarts) ----------
function cdcl(nv, clauses, maxConflicts = 2e7) {
  const nCl0 = clauses.length;
  const cl = clauses.map(c => c.slice());
  const lit2i = (l) => (l > 0 ? 2 * l : -2 * l + 1);
  const assigns = new Int8Array(nv + 1);
  const level = new Int32Array(nv + 1).fill(-1);
  const reason = new Array(nv + 1).fill(null);
  const trail = [], lim = [];
  const act = new Float64Array(nv + 1);
  const phase = new Int8Array(nv + 1).fill(1);
  let varInc = 1;
  const watches = new Array(2 * nCl0).fill(0);
  const wl = Array.from({ length: 2 * nv + 2 }, () => []);
  cl.forEach((c, ci) => {
    watches[2 * ci] = c[0]; watches[2 * ci + 1] = c.length > 1 ? c[1] : c[0];
    wl[lit2i(c[0])].push(ci);
    wl[lit2i(c.length > 1 ? c[1] : c[0])].push(ci);
  });
  const value = (l) => { const a = assigns[l > 0 ? l : -l]; return l > 0 ? a : -a; };
  const qhead = { i: 0 };
  function enqueue(l, r) {
    const v = Math.abs(l); assigns[v] = l > 0 ? 1 : -1; level[v] = lim.length; reason[v] = r;
    trail.push(l); phase[v] = l > 0 ? 1 : -1;
  }
  function propagate() {
    while (qhead.i < trail.length) {
      const p = trail[qhead.i++]; const pl = -p;
      const list = wl[lit2i(pl)];
      let k = 0, sz = list.length;
      while (k < sz) {
        const ci = list[k];
        let w1 = watches[2 * ci], w2 = watches[2 * ci + 1];
        if (w2 === pl) { const t = w1; w1 = w2; w2 = t; } // w1 === pl now
        if (value(w2) === 1) { k++; continue; }
        const c = cl[ci];
        let found = false;
        for (let t = 2; t < c.length; t++) {
          const l = c[t];
          if (value(l) !== -1) {
            const idx0 = (c[0] === pl) ? 0 : 1;
            c[idx0] = l; c[t] = pl;
            watches[2 * ci + idx0] = l;
            wl[lit2i(l)].push(ci);
            list[k] = list[sz - 1]; sz--; list.pop();
            found = true; break;
          }
        }
        if (found) continue;
        k++;
        if (value(w2) === -1) return ci;
        enqueue(w2, ci);
      }
    }
    return -1;
  }
  function backtrack(lv) {
    while (lim.length > lv) lim.pop();
    while (trail.length > 0 && level[Math.abs(trail[trail.length - 1])] > lv) {
      const l = trail.pop(); assigns[Math.abs(l)] = 0; reason[Math.abs(l)] = null; level[Math.abs(l)] = -1;
    }
    qhead.i = trail.length;
  }
  function analyze(ci) {
    const seen = new Set(); let cnt = 0; const queue = [];
    const touch = (v) => { if (!seen.has(v)) { seen.add(v); act[v] += varInc; if (level[v] === lim.length) cnt++; else queue.push(v); } };
    for (const l of cl[ci]) touch(Math.abs(l));
    let idx = trail.length - 1;
    while (cnt > 1) {
      while (!seen.has(Math.abs(trail[idx]))) idx--;
      const p = trail[idx]; idx--;
      const pv = Math.abs(p);
      seen.delete(pv);
      cnt--;
      const r = reason[pv];
      if (r === null) { queue.push(pv); continue; }
      for (const l of cl[r]) if (Math.abs(l) !== pv) touch(Math.abs(l));
    }
    let asserting = -1;
    for (const v of seen) if (level[v] === lim.length) { if (asserting !== -1) throw new Error('multi-assert'); asserting = v; }
    if (asserting === -1) throw new Error('no-assert');
    const aLit = assigns[asserting] === 1 ? -asserting : asserting;
    const clause = [aLit];
    let lv = 0;
    for (const v of seen) if (v !== asserting) { clause.push(assigns[v] === 1 ? -v : v); lv = Math.max(lv, level[v]); }
    for (const v of queue) { clause.push(assigns[v] === 1 ? -v : v); lv = Math.max(lv, level[v]); }
    return { clause, blevel: lv };
  }
  let conflicts = 0;
  let nextRestart = 200, restartInterval = 200;
  function reduceDB() {
    // delete non-locked learnt clauses longer than 3; keep originals
    const locked = new Set();
    for (let v = 1; v <= nv; v++) if (reason[v] !== null && reason[v] >= nCl0) locked.add(reason[v]);
    const keep = new Map(); // old index -> new index
    for (let ci = 0; ci < nCl0; ci++) keep.set(ci, ci);
    let next = nCl0;
    for (let ci = nCl0; ci < cl.length; ci++) {
      if (locked.has(ci) || cl[ci].length <= 3) keep.set(ci, next++);
    }
    const newCl = [];
    const newWatches = [];
    for (const [oldCi, newCi] of keep) { newCl[newCi] = cl[oldCi]; newWatches[2 * newCi] = watches[2 * oldCi]; newWatches[2 * newCi + 1] = watches[2 * oldCi + 1]; }
    cl.length = 0; for (let i = 0; i < newCl.length; i++) cl[i] = newCl[i];
    watches.length = 0; for (let i = 0; i < newWatches.length; i++) watches[i] = newWatches[i];
    // rebuild watch lists
    for (let i = 0; i < wl.length; i++) wl[i].length = 0;
    for (let ci = 0; ci < cl.length; ci++) {
      const c = cl[ci];
      wl[lit2i(watches[2 * ci])].push(ci);
      wl[lit2i(watches[2 * ci + 1])].push(ci);
    }
    // fix reason indices
    for (let v = 1; v <= nv; v++) if (reason[v] !== null) { if (keep.has(reason[v])) reason[v] = keep.get(reason[v]); else reason[v] = null; }
    return next;
  }
  let nextReduce = 5000;
  while (true) {
    const ci = propagate();
    if (ci >= 0) {
      conflicts++;
      if (lim.length === 0) return { sat: false, conflicts };
      if (conflicts > maxConflicts) return { timeout: true, conflicts };
      const { clause, blevel } = analyze(ci);
      cl.push(clause); const nci = cl.length - 1;
      watches.push(clause[0]); watches.push(clause.length > 1 ? clause[1] : clause[0]);
      wl[lit2i(clause[0])].push(nci);
      wl[lit2i(clause.length > 1 ? clause[1] : clause[0])].push(nci);
      varInc /= 1.0001;
      if (varInc < 1e-6) { for (let i = 1; i <= nv; i++) act[i] *= 1e-6; varInc = 1; }
      backtrack(blevel);
      if (clause.length === 1) {
        const v = Math.abs(clause[0]); assigns[v] = clause[0] > 0 ? 1 : -1; level[v] = 0; reason[v] = null;
        trail.push(clause[0]);
      } else enqueue(clause[0], nci);
      if (conflicts >= nextReduce) { nextReduce = conflicts + 5000; reduceDB(); }
    } else {
      if (conflicts >= nextRestart) { nextRestart = conflicts + restartInterval; restartInterval = Math.floor(restartInterval * 1.5); backtrack(0); continue; }
      let best = 0, ba = -1;
      for (let v = 1; v <= nv; v++) if (assigns[v] === 0 && act[v] > ba) { ba = act[v]; best = v; }
      if (best === 0) {
        const model = new Array(nv + 1);
        for (let v = 1; v <= nv; v++) model[v] = assigns[v] === 0 ? (phase[v] === 1) : (assigns[v] === 1);
        return { sat: true, model, conflicts };
      }
      lim.push(trail.length);
      enqueue(phase[best] === 1 ? best : -best, null);
    }
  }
}

// ---------- independent simple DPLL (chronological, count-based) ----------
function dpll(nv, clauses) {
  const clauses2 = clauses.map(c => c.slice());
  const assign = new Int8Array(nv + 1);
  const nSat = new Int32Array(clauses2.length);
  const nFalse = new Int32Array(clauses2.length);
  const len = clauses2.map(c => c.length);
  const occurs = Array.from({ length: nv + 1 }, () => []);
  clauses2.forEach((c, ci) => { for (const l of c) occurs[Math.abs(l)].push(ci); });
  const trail = [];
  function assignLit(l) {
    const v = Math.abs(l); assign[v] = l > 0 ? 1 : -1; trail.push(v);
    const val = l > 0 ? 1 : -1;
    let conflict = false;
    for (const ci of occurs[v]) {
      const c = clauses2[ci]; let lit = 0;
      for (const x of c) if (Math.abs(x) === v) { lit = x; break; }
      if ((lit > 0 ? 1 : -1) === val) nSat[ci]++;
      else { nFalse[ci]++; if (nSat[ci] === 0 && nFalse[ci] === len[ci]) conflict = true; }
    }
    return !conflict;
  }
  function undoTo(mark) {
    while (trail.length > mark) {
      const v = trail.pop(); const wasTrue = assign[v] === 1; assign[v] = 0;
      for (const ci of occurs[v]) {
        const c = clauses2[ci]; let lit = 0;
        for (const x of c) if (Math.abs(x) === v) { lit = x; break; }
        if ((lit > 0 ? 1 : -1) === (wasTrue ? 1 : -1)) nSat[ci]--; else nFalse[ci]--;
      }
    }
  }
  function unitProp() {
    let moved = true;
    while (moved) {
      moved = false;
      for (let ci = 0; ci < clauses2.length; ci++) {
        if (nSat[ci] > 0 || nFalse[ci] === len[ci]) continue;
        if (nFalse[ci] === len[ci] - 1) {
          const c = clauses2[ci]; let uLit = 0;
          for (const l of c) if (assign[Math.abs(l)] === 0) { uLit = l; break; }
          if (uLit === 0) continue;
          if (!assignLit(uLit)) return false;
          moved = true;
        }
      }
    }
    return true;
  }
  let steps = 0, LIMIT = 5e7;
  function solve() {
    steps++;
    if (steps > LIMIT) throw new Error('dpll-limit');
    const mark = trail.length;
    if (!unitProp()) { undoTo(mark); return false; }
    let v = 0;
    for (let i = 1; i <= nv; i++) if (assign[i] === 0) { v = i; break; }
    if (v === 0) return true;
    const mark2 = trail.length;
    if (assignLit(v) && solve()) return true;
    undoTo(mark2); undoTo(mark);
    if (!unitProp()) { undoTo(mark); return false; }
    const mark3 = trail.length;
    if (assignLit(-v) && solve()) return true;
    undoTo(mark3); undoTo(mark);
    return false;
  }
  try {
    if (!solve()) return { sat: false, steps };
  } catch (e) { return { timeout: true, steps }; }
  const model = new Array(nv + 1);
  for (let i = 1; i <= nv; i++) model[i] = assign[i] === 1 ? true : (assign[i] === -1 ? false : true);
  return { sat: true, model, steps };
}

// ---------- brute force (tiny boards) ----------
function popcount(x) { let c = 0; while (x) { x &= x - 1; c++; } return c; }
function bruteForce(w, m, q) {
  const { P, n, curves } = buildCensus(w, m, q);
  const res = { maximal: 0, deficientMaximal: 0, minMaximal: Infinity, minDeficient: Infinity };
  const through = Array.from({ length: n }, () => []);
  curves.forEach((cu, ci) => { for (const p of cu.pts) through[p].push(ci); });
  for (let mask = 0; mask < (1 << n); mask++) {
    let ok = true;
    for (const cu of curves) {
      let cnt = 0; for (const p of cu.pts) if (mask >> p & 1) { cnt++; if (cnt >= q) { ok = false; break; } }
      if (!ok) break;
    }
    if (!ok) continue;
    let max = true;
    for (let p = 0; p < n; p++) {
      if (mask >> p & 1) continue;
      let blocked = false;
      for (const ci of through[p]) {
        const cu = curves[ci]; let cnt = 0;
        for (const x of cu.pts) if (mask >> x & 1) cnt++;
        if (cnt >= q - 1) { blocked = true; break; }
      }
      if (!blocked) { max = false; break; }
    }
    if (!max) continue;
    const size = popcount(mask);
    res.maximal++; res.minMaximal = Math.min(res.minMaximal, size);
    if (size < w * (q - 1)) { res.deficientMaximal++; res.minDeficient = Math.min(res.minDeficient, size); }
  }
  return res;
}

module.exports = { pts, buildCensus, encode, toDimacs, verifyConfig, cdcl, dpll, bruteForce, circleABC, onCircle, lineABC, onLine };

if (require.main === module) {
  const cmd = process.argv[2];
  if (cmd === 'census') {
    const [w, m, q] = process.argv.slice(3).map(Number);
    const t0 = Date.now();
    const { curves } = buildCensus(w, m, q);
    const lines = curves.filter(c => c.type === 'line'), circs = curves.filter(c => c.type === 'circle');
    const h = {}; for (const c of circs) h[c.pts.length] = (h[c.pts.length] || 0) + 1;
    console.log(JSON.stringify({ w, m, q, lines: lines.length, circles: circs.length, ms: Date.now() - t0, circleHist: h }));
  } else if (cmd === 'brute') {
    const [w, m, q] = process.argv.slice(3).map(Number);
    const r = bruteForce(w, m, q);
    console.log(JSON.stringify({ w, m, q, maximal: r.maximal, minMaximal: r.minMaximal, deficientMaximal: r.deficientMaximal, minDeficient: r.minDeficient }));
  } else if (cmd === 'sat') {
    const [w, m, q] = process.argv.slice(3, 6).map(Number);
    const args = process.argv.slice(6);
    const useDpll = args.includes('--dpll');
    const capArg = args.find(a => a.startsWith('--cap='));
    const maxStones = capArg ? Number(capArg.slice(6)) : null;
    const t0 = Date.now();
    const { enc, cell, curves, P, mode } = encode(w, m, q, maxStones != null ? { maxStones } : {});
    const t1 = Date.now();
    let res;
    if (useDpll) res = dpll(enc.nv, enc.clauses);
    else res = cdcl(enc.nv, enc.clauses);
    const out = {
      w, m, q, mode, maxStones, curves: curves.length,
      lines: curves.filter(c => c.type === 'line').length, circles: curves.filter(c => c.type === 'circle').length,
      vars: enc.nv, clauses: enc.clauses.length, encMs: t1 - t0, solveMs: Date.now() - t1,
      solver: useDpll ? 'dpll' : 'cdcl', conflicts: res.conflicts || null, steps: res.steps || null
    };
    if (res.timeout) { out.result = 'timeout'; console.log(JSON.stringify(out)); process.exit(2); }
    if (res.sat) {
      out.result = 'SAT';
      const stones = [];
      for (let i = 0; i < P.length; i++) if (res.model[cell[i]]) stones.push(P[i]);
      out.stones = stones;
      out.verify = verifyConfig(w, m, q, stones);
    } else out.result = 'UNSAT';
    console.log(JSON.stringify(out));
  } else {
    console.log('cmds: census|brute|sat');
  }
}
