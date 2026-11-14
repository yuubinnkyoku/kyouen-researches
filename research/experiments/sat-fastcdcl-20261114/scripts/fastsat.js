// fastsat.js - CDCL SAT solver in Node.js. DIMACS in, JSON verdict out.
// Options: --drat=FILE --maxconflicts=N --maxseconds=S --model=FILE
// Two-watched literals + blocker, EVSIDS binary heap, 1UIP + recursive
// minimization, Luby restarts, phase saving, LBD-based reduction + compaction.
'use strict';
const fs = require('fs');
const OPT = {};
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (a.startsWith('--')) { const eq = a.indexOf('='); OPT[a.slice(2, eq)] = a.slice(eq + 1); }
  else OPT.cnf = a;
}
// ---------- parse ----------
const raw = fs.readFileSync(OPT.cnf, 'utf8');
let nv = 0;
const clauses = [];
{
  const lines = raw.split('\n');
  for (const line of lines) {
    const t = line.trim();
    if (t.length === 0) continue;
    const c0 = t.charCodeAt(0);
    if (c0 === 99 || c0 === 112) continue; // 'c' comment / 'p' header
    const parts = t.split(/\s+/);
    let cur = [];
    for (const s of parts) {
      if (s.length === 0) continue;
      const n = parseInt(s, 10);
      if (Number.isNaN(n)) continue;
      if (n === 0) { if (cur.length) { clauses.push(cur); cur = []; } }
      else cur.push(n);
    }
    if (cur.length) clauses.push(cur);
  }
}
for (const c of clauses) for (const l of c) { const v = l > 0 ? l : -l; if (v > nv) nv = v; }
for (let i = 0; i < clauses.length; i++) {
  const c = clauses[i];
  const s = new Set(c);
  let taut = false;
  for (const l of s) if (s.has(-l)) taut = true;
  clauses[i] = taut ? [] : Array.from(s);
}
// ---------- clause memory ----------
let memCap = 1 << 22;
let mem = new Int32Array(memCap);
let memTop = 0;
const coff = [], csize = [], clbd = [], cact = [], alive = [];
let nClauses = 0;
function ensureMem(need) {
  while (memTop + need > memCap) {
    memCap *= 2;
    const nm = new Int32Array(memCap);
    nm.set(mem.subarray(0, memTop));
    mem = nm;
  }
}
function addClauseMem(lits, lbd) {
  const sz = lits.length;
  ensureMem(sz + 2);
  const off = memTop;
  mem[off] = sz; mem[off + 1] = lbd;
  for (let i = 0; i < sz; i++) mem[off + 2 + i] = lits[i];
  memTop = off + sz + 2;
  const id = nClauses++;
  coff[id] = off; csize[id] = sz; clbd[id] = lbd; cact[id] = 0; alive[id] = 1;
  return id;
}
const litIdx = (l) => (l > 0 ? 2 * l : -2 * l + 1);
const val = new Int8Array(nv + 1);
const lev = new Int32Array(nv + 1);
const reason = new Int32Array(nv + 1);
const antra = new Int8Array(nv + 1);
const trail = new Int32Array(nv + 2); let trailTop = 0;
const lims = [];
let qhead = 0;
const wl = new Array(2 * nv + 2);
for (let i = 0; i < 2 * nv + 2; i++) wl[i] = [];
let nOrig = 0;
for (let ci = 0; ci < clauses.length; ci++) {
  const c = clauses[ci];
  if (c.length === 0) continue;
  const id = addClauseMem(c, 0);
  nOrig++;
  if (c.length === 1) { wl[litIdx(c[0])].push(id, c[0]); }
  else { wl[litIdx(c[0])].push(id, c[1]); wl[litIdx(c[1])].push(id, c[0]); }
}
clauses.length = 0;
// cell var prioritization (applied after parse, before heap build)
const NCELLS = OPT.ncells ? parseInt(OPT.ncells) : 0;

const vact = new Float64Array(nv + 1);
const heap = new Int32Array(4 * nv + 8); const hpos = new Int32Array(nv + 1);
let heapN = 0;
function heapSwap(i, j) { const t = heap[i]; heap[i] = heap[j]; heap[j] = t; hpos[heap[i]] = i; hpos[heap[j]] = j; }
function heapUp(i) { while (i > 1) { const p = i >> 1; if (vact[heap[i]] > vact[heap[p]]) { heapSwap(i, p); i = p; } else break; } }
function heapDown(i) { for (;;) { const l = 2 * i, r = l + 1; let m = i;
  if (l <= heapN && vact[heap[l]] > vact[heap[m]]) m = l;
  if (r <= heapN && vact[heap[r]] > vact[heap[m]]) m = r;
  if (m === i) break; heapSwap(i, m); i = m; } }
for (let v = 1; v <= nv; v++) { heapN++; heap[heapN] = v; hpos[v] = heapN; }
if (NCELLS > 0 && OPT.cellboost) { const cb = parseFloat(OPT.cellboost); for (let v = 1; v <= NCELLS && v <= nv; v++) vact[v] = cb; for (let v = 1; v <= nv; v++) if (v > NCELLS) vact[v] = 1; for (let v = 1; v <= nv; v++) heapUp(v); }
function bump(v, inc) { vact[v] += inc; if (vact[v] > 1e100) { for (let i = 1; i <= nv; i++) vact[i] *= 1e-100; } if (hpos[v] > 0) heapUp(hpos[v]); }
function heapRemoveTop() { const v = heap[1]; heapSwap(1, heapN); heapN--; hpos[v] = -1; if (heapN > 0) heapDown(1); return v; }
function heapReinsert(v) { heapN++; heap[heapN] = v; hpos[v] = heapN; heapUp(heapN); }
function popVar() { while (heapN > 0) { const v = heapRemoveTop(); if (val[v] === 0) return v; } return 0; }
const phase = new Int8Array(nv + 1).fill(1);
if (OPT.cellphase === '0') { for (let v = 1; v <= NCELLS && v <= nv; v++) phase[v] = -1; }
let varInc = 1;
const VAR_DECAY = OPT.vdecay ? parseFloat(OPT.vdecay) : 0.95;
let propCount = 0;
function litVal(l) { const v = l > 0 ? l : -l; const a = val[v]; return l > 0 ? a : -a; }
function enqueue(l, r) {
  const v = l > 0 ? l : -l;
  val[v] = l > 0 ? 1 : -1; lev[v] = lims.length; reason[v] = r;
  trail[trailTop++] = l;
  if (hpos[v] > 0) { const i = hpos[v]; heapSwap(i, heapN); heapN--; hpos[v] = -1; if (i <= heapN) { heapDown(i); heapUp(i); } }
  phase[v] = l > 0 ? 1 : -1;
}
function backtrack(lv) {
  while (lims.length > lv) lims.pop();
  while (trailTop > 0) {
    const l = trail[trailTop - 1]; const v = l > 0 ? l : -l;
    if (lev[v] <= lv) break;
    trailTop--; val[v] = 0; reason[v] = 0;
    heapReinsert(v);
  }
  qhead = trailTop;
}
// ---------- propagate ----------
function propagate() {
  while (qhead < trailTop) {
    propCount++;
    const p = trail[qhead++]; const pl = -p;
    const list = wl[litIdx(pl)];
    let k = 0, sz = list.length;
    while (k < sz) {
      const id = list[k]; const blocker = list[k + 1];
      if (blocker !== 0 && litVal(blocker) === 1) { k += 2; continue; }
      const off = coff[id];
      const csizeL = csize[id];
      if (csizeL === 1) { qhead = trailTop; return id; }
      let w1 = mem[off + 2], w2 = mem[off + 3];
      if (w1 !== pl && w2 !== pl) { k += 2; continue; } // stale
      if (w1 !== pl) { mem[off + 2] = w2; mem[off + 3] = w1; const t = w1; w1 = w2; w2 = t; }
      if (litVal(w2) === 1) { list[k + 1] = w2; k += 2; continue; }
      let f = 0;
      for (let t = 2; t < csizeL; t++) {
        const l = mem[off + 2 + t];
        if (litVal(l) !== -1) {
          mem[off + 2] = l; mem[off + 2 + t] = pl;
          wl[litIdx(l)].push(id, w2);
          list[k] = list[sz - 2]; list[k + 1] = list[sz - 1]; sz -= 2; list.length = sz;
          f = 1; break;
        }
      }
      if (f) continue;
      list[k + 1] = w2;
      if (litVal(w2) === -1) { qhead = trailTop; return id; }
      enqueue(w2, id + 1);
      k += 2;
    }
  }
  return -1;
}
// ---------- minimization ----------
const seenList = [];
function litRedundant(l, budget) {
  const v = l > 0 ? l : -l;
  const r = reason[v];
  if (r === 0) return false;
  const stack = [];
  const added = [];
  let ok = true;
  let ops = 0;
  {
    const roff = coff[r - 1]; const rsize = csize[r - 1];
    for (let t = 0; t < rsize; t++) {
      const s = mem[roff + 2 + t]; if (s === -l) continue;
      const sv = s > 0 ? s : -s;
      if (antra[sv]) continue;
      if (lev[sv] === 0) continue;
      stack.push(sv);
    }
  }
  while (stack.length) {
    if (ops++ > budget) { ok = false; break; }
    const qv = stack.pop();
    if (antra[qv]) continue;
    const rr = reason[qv];
    if (rr === 0) { ok = false; break; }
    antra[qv] = 1; added.push(qv);
    const roff = coff[rr - 1]; const rsize = csize[rr - 1];
    for (let t = 0; t < rsize; t++) {
      const s = mem[roff + 2 + t];
      const sv = s > 0 ? s : -s;
      if (sv === qv) continue;
      if (antra[sv]) continue;
      if (lev[sv] === 0) continue;
      stack.push(sv);
    }
  }
  if (!ok) { for (const v2 of added) antra[v2] = 0; }
  else { for (const v2 of added) seenList.push(v2); }
  return ok;
}
// ---------- analyze ----------
function mark(v) { if (!antra[v]) { antra[v] = 1; seenList.push(v); } }
function analyze(cid, curLev) {
  seenList.length = 0;
  const off = coff[cid]; const size = csize[cid];
  let pathC = 0;
  const out = [];
  for (let t = 0; t < size; t++) {
    const l = mem[off + 2 + t]; const v = l > 0 ? l : -l;
    if (lev[v] === 0) continue;
    mark(v); bump(v, varInc);
    if (lev[v] >= curLev) pathC++;
    else out.push(l);
  }
  let idx = trailTop - 1;
  let p = 0;
  while (pathC > 0) {
    if (idx < 0) throw new Error('analyze underflow');
    while (idx >= 0 && !antra[trail[idx] > 0 ? trail[idx] : -trail[idx]]) idx--;
    if (idx < 0) {
      const offD = coff[cid]; const sizeD = csize[cid];
      let cldbg = '';
      for (let t = 0; t < sizeD; t++) { const l = mem[offD + 2 + t]; const v = l > 0 ? l : -l; cldbg += l + '(v' + val[v] + ',L' + lev[v] + ') '; }
      // trail membership check for var 3522-ish: find first marked var
      const mv = seenList[0];
      let onTrail = -1;
      for (let i = 0; i < trailTop; i++) { const v2 = trail[i] > 0 ? trail[i] : -trail[i]; if (v2 === mv) { onTrail = i; break; } }
      throw new Error('analyze underflow2 pathC=' + pathC + ' curLev=' + curLev + ' trailTop=' + trailTop + ' marked=' + mv + ' onTrailIdx=' + onTrail + ' val=' + val[mv] + ' clause=[' + cldbg + ']');
    }
    p = trail[idx]; idx--;
    const v = p > 0 ? p : -p;
    if (lev[v] < curLev) continue;
    pathC--;
    if (pathC === 0) break;
    const r = reason[v];
    if (r !== 0) {
      const roff = coff[r - 1]; const rsize = csize[r - 1];
      for (let t = 0; t < rsize; t++) {
        const q = mem[roff + 2 + t]; if (q === p) continue;
        const qv = q > 0 ? q : -q;
        if (lev[qv] === 0) continue;
        if (!antra[qv]) { mark(qv); bump(qv, varInc); if (lev[qv] >= curLev) pathC++; else out.push(q); }
      }
    }
  }
  if (p === 0) throw new Error('no UIP');
  out.unshift(-p);
  const kept = [out[0]];
  if (OPT.mini) for (let t = 1; t < out.length; t++) {
    const l = out[t];
    if (litRedundant(l, 50)) continue;
    kept.push(l);
  }
  else for (let t = 1; t < out.length; t++) kept.push(out[t]);
  for (const v of seenList) antra[v] = 0;
  seenList.length = 0;
  let blevel = 0, bIdx = 1;
  for (let t = 1; t < kept.length; t++) { const v = kept[t] > 0 ? kept[t] : -kept[t]; if (lev[v] > blevel) { blevel = lev[v]; bIdx = t; } }
  if (kept.length > 1) { const t0 = kept[1]; kept[1] = kept[bIdx]; kept[bIdx] = t0; }
  return { lits: kept, blevel };
}
function computeLBD(lits) {
  const s = new Set();
  for (const l of lits) { const v = l > 0 ? l : -l; s.add(lev[v]); }
  return s.size;
}
// ---------- reduction + compaction ----------
let nLearnt = 0, claInc = 1;
const CLA_DECAY = 0.999;
function reduceDB() {
  const locked = new Set();
  for (let v = 1; v <= nv; v++) if (reason[v] !== 0) locked.add(reason[v] - 1);
  const cand = [];
  for (let id = nOrig; id < nClauses; id++) {
    if (!alive[id]) continue;
    if (locked.has(id)) continue;
    if (clbd[id] <= 3) continue;
    if (csize[id] <= 2) continue;
    cand.push(id);
  }
  if (cand.length < 2000) return 0;
  cand.sort((a, b) => cact[a] - cact[b]);
  const half = cand.length >> 1;
  for (let i = 0; i < half; i++) alive[cand[i]] = 0;
  const newMem = new Int32Array(memCap);
  let nTop = 0;
  const newOff = new Int32Array(nClauses);
  for (let id = 0; id < nClauses; id++) {
    if (!alive[id]) continue;
    const off = coff[id]; const sz = csize[id];
    for (let t = 0; t < sz + 2; t++) newMem[nTop + t] = mem[off + t];
    newOff[id] = nTop; nTop += sz + 2;
  }
  mem = newMem; memTop = nTop;
  for (let id = 0; id < nClauses; id++) coff[id] = newOff[id];
  for (let i = 0; i < wl.length; i++) wl[i].length = 0;
  for (let id = 0; id < nClauses; id++) {
    if (!alive[id]) continue;
    const off = coff[id];
    if (csize[id] === 1) { wl[litIdx(mem[off + 2])].push(id, mem[off + 2]); continue; }
    wl[litIdx(mem[off + 2])].push(id, mem[off + 3]);
    wl[litIdx(mem[off + 3])].push(id, mem[off + 2]);
  }
  return half;
}
// ---------- DRAT ----------
let dratFd = null;
if (OPT.drat) dratFd = fs.openSync(OPT.drat, 'w');
let dratChunks = [];
function dratEmit(lits) {
  if (!dratFd) return;
  let s = '';
  for (let i = 0; i < lits.length; i++) s += lits[i] + ' ';
  dratChunks.push(s + '0\n');
  if (dratChunks.length > 10000) { fs.writeSync(dratFd, dratChunks.join('')); dratChunks.length = 0; }
}
// ---------- luby ----------
let lubyI = 0;
const LUBY = [1,1,2,1,1,2,4,1,1,2,1,1,2,4,8,1,1,2,1,1,2,4,1,1,2,1,1,2,4,8,16,
 1,1,2,1,1,2,4,1,1,2,1,1,2,4,8,1,1,2,1,1,2,4,1,1,2,1,1,2,4,8,16,32,
 1,1,2,1,1,2,4,1,1,2,1,1,2,4,8,1,1,2,1,1,2,4,1,1,2,1,1,2,4,8,16,1,1,2,1,1,2,4,
 1,1,2,1,1,2,4,8,1,1,2,1,1,2,4,1,1,2,1,1,2,4,8,16,32,64];
const RBASE = OPT.base ? parseInt(OPT.base) : 512;
function nextRestartLen() { const v = LUBY[lubyI % LUBY.length] * RBASE; lubyI++; return v; }
// ---------- main ----------
let conflicts = 0, decisions = 0;
const maxConf = OPT.maxconflicts ? parseInt(OPT.maxconflicts) : Infinity;
const maxSec = OPT.maxseconds ? parseFloat(OPT.maxseconds) : Infinity;
let nextRestart = nextRestartLen();
let nextReduce = 4000;
let status = 'UNKNOWN';
const t0 = Date.now();
let lastReport = 0;
try {
  {
    const cid = propagate();
    if (cid >= 0) status = 'UNSAT';
  }
  while (status === 'UNKNOWN') {
    const cid = propagate();
    if (cid >= 0) {
      // tripwire: conflict clause must be fully false
      {
        const offT = coff[cid]; const sizeT = csize[cid];
        for (let t = 0; t < sizeT; t++) {
          const l = mem[offT + 2 + t];
          if (litVal(l) !== -1) {
            let cldbg = '';
            for (let t2 = 0; t2 < sizeT; t2++) { const l2 = mem[offT + 2 + t2]; const v2 = l2 > 0 ? l2 : -l2; cldbg += l2 + '(v' + val[v2] + ',L' + lev[v2] + ') '; }
            let tr = '';
            for (let i = Math.max(0, qhead - 5); i < trailTop && tr.length < 400; i++) tr += trail[i] + ' ';
            throw new Error('SPURIOUS CONFLICT cid=' + cid + ' clause=[' + cldbg + '] qhead=' + qhead + ' trailTop=' + trailTop + ' recent=[' + tr + ']');
          }
        }
      }
      conflicts++;
      if (lims.length === 0) { status = 'UNSAT'; break; }
      if (conflicts > maxConf || (Date.now() - t0) / 1000 > maxSec) { status = 'TIMEOUT'; break; }
      const { lits, blevel } = analyze(cid, lims.length);
      dratEmit(lits);
      const lbd = computeLBD(lits);
      claInc /= CLA_DECAY;
      if (claInc > 1e20) { for (let id = nOrig; id < nClauses; id++) cact[id] *= 1e-20; claInc = 1; }
      if (lits.length === 1) {
        backtrack(0);
        const l = lits[0]; const v = l > 0 ? l : -l;
        if (val[v] !== 0) throw new Error('unit at level0 conflict');
        val[v] = l > 0 ? 1 : -1; lev[v] = 0; reason[v] = 0;
        trail[trailTop++] = l; qhead = trailTop - 1;
        const id = addClauseMem(lits, lbd);
        cact[id] = claInc;
        wl[litIdx(lits[0])].push(id, lits[0]);
      } else {
        const id = addClauseMem(lits, lbd);
        nLearnt++;
        cact[id] = claInc;
        backtrack(blevel);
        enqueue(lits[0], id + 1);
        wl[litIdx(lits[0])].push(id, lits[1]);
        wl[litIdx(lits[1])].push(id, lits[0]);
      }
      varInc /= VAR_DECAY;
      if (conflicts >= nextRestart) { nextRestart = conflicts + nextRestartLen(); backtrack(0); }
      if (conflicts >= nextReduce) { const oldInt = nextReduce - conflicts; nextReduce = conflicts + Math.max(4000, oldInt + Math.floor(oldInt * 0.5)); reduceDB(); }
      if (conflicts - lastReport >= 100000) { lastReport = conflicts; if (OPT.progress) console.error('c conflicts=' + conflicts + ' sec=' + ((Date.now() - t0) / 1000).toFixed(1) + ' learnt=' + nLearnt + ' memMB=' + (memTop * 4 / 1048576).toFixed(0)); }
    } else {
      if (conflicts >= nextRestart) { nextRestart = conflicts + nextRestartLen(); backtrack(0); continue; }
      const v = popVar();
      if (v === 0) { status = 'SAT'; break; }
      decisions++;
      lims.push(trailTop);
      enqueue(phase[v] === 1 ? v : -v, 0);
    }
  }
} catch (e) { status = 'ERROR'; globalThis.errMsg = e.stack; }
if (dratFd) {
  if (status === 'UNSAT') { if (dratChunks.length) { fs.writeSync(dratFd, dratChunks.join('')); dratChunks.length = 0; } fs.writeSync(dratFd, '0\n'); }
  fs.closeSync(dratFd);
}
if (status === 'SAT' && OPT.model) {
  const m = [];
  for (let v = 1; v <= nv; v++) m.push(val[v] === 0 ? (phase[v] === 1 ? v : -v) : (val[v] === 1 ? v : -v));
  fs.writeFileSync(OPT.model, m.join(' '));
}
const out = { status, nv, nOrig, conflicts, decisions, props: propCount, learnt: nLearnt, sec: +((Date.now() - t0) / 1000).toFixed(1), memMB: +(memTop * 4 / 1048576).toFixed(1), err: globalThis.errMsg || null };
console.log(JSON.stringify(out));
