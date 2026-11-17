#!/usr/bin/env node
// K0908 sweep engine: compact-memo JavaScript mask twin of the Python
// mask_game / mask_verdict spec of record (the K0893 verifier). The
// game logic, recursion order, budget semantics and record format are
// verbatim identical to the committed K0893 engine
// (mask_engine_fast_r9.js); the ONLY change is the memo representation:
// the K0893 engine keyed a JS Map with a 65-char string built per
// visited state (two allocations per state, ~170MB of string garbage
// per heavy profile, which dominated the run time through major GCs),
// while this engine stores the same keys in a preallocated byte arena
// addressed by an open-addressing uint32 table (FNV-1a hash, linear
// probing, exact 8-byte-block key comparison via Float64Array views,
// zero garbage per state).
//
// The memo is a pure cache: the returned (sv, fl, states) of a record
// do not depend on the memo representation, and `states` remains the
// number of distinct visited states (== K0893 memo.size). Records are
// pure functions of (profile, r), so sweep segments produced with
// different start indices are byte-identical when concatenated.
//
// Validated against the committed K0893/K0876 records byte-identically
// (r=8 cap<=12 column and r=9 cap<=10 column samples, see report.md).
//
// CLI: node mask_engine_fast2.js profs.json R out.jsonl [start]
//
// Record format (one JSON object per line, index i = position in the
// canonical enumeration of the given profs file):
//   {"i":..,"atoms":[..7 ints..],"determined":bool,
//    "survivors":[..],"first_losers":[..],"states":int}
// states == distinct visited state count, matching the Python twins.
// Budget is effectively unbounded (200M nodes).

'use strict';
const fs = require('fs');

const STAR = [0, 0x55, 0x66, 0x78];            // star[i], k=3, 7 atoms
const INV_STAR = [0, ~0x55 & 0x7f, ~0x66 & 0x7f, ~0x78 & 0x7f];

function nextActive(p, r, active) {
  for (let d = 1; d <= r; d++) {
    const q = (p + d) % r;
    if ((active >> q) & 1) return q;
  }
  throw new Error('no active player after ' + p);
}

// ---------------------------------------------------------------------------
// Compact open-addressing memo. Key layout (KW = 7r+3 bytes, zero-padded
// to an 8-byte multiple STR): [mover, active_lo, active_hi,
// counts[0..7r-1]] -- the same 7r+2-tuple of small non-negative ints
// the K0893 engine serialized as (x+1) chars. Exactness: a hit is only
// reported after a full STR-byte comparison of the arena entry against
// the live key (Float64 block compares), so no hash collision can
// produce a false hit; a miss is always a true miss (probe stops at the
// first empty slot, and the slot is claimed by store() before any other
// state can claim it).
// ---------------------------------------------------------------------------
function CompactMemo(r) {
  const KW = 7 * r + 3;
  const STR = Math.ceil(KW / 8) * 8;
  this.KW = KW;
  this.STR = STR;
  this.STRD = STR / 8;
  this.cap = 1 << 16;
  this.mask = this.cap - 1;
  this.limit = (this.cap * 0.6) | 0;
  this.table = new Uint32Array(this.cap);   // slot -> id+1 (0 = empty)
  this.arena = new Uint8Array(this.STR * this.cap);
  this.arenaF = new Float64Array(this.arena.buffer);
  this.vals = new Uint32Array(this.cap);
  this.n = 0;
}

CompactMemo.prototype.hash = function (b) {
  let h = 0x811c9dc5;
  for (let i = 0; i < this.KW; i++) {
    h ^= b[i];
    h = Math.imul(h, 0x01000193);
  }
  h ^= h >>> 15;
  h = Math.imul(h, 0x2545f491);
  h ^= h >>> 13;
  return h >>> 0;
};

// Read-only lookup for the key in scratch buffer b (Uint8Array(STR)) /
// bF (its Float64 view). Returns the stored value (>= 0) on hit, or -1
// on miss. Never inserts, never grows.
CompactMemo.prototype.lookup = function (b, bF) {
  let h = this.hash(b) & this.mask;
  const table = this.table;
  const aF = this.arenaF;
  const STRD = this.STRD;
  for (;;) {
    const e = table[h];
    if (e === 0) return -1;
    const id = e - 1;
    const off = id * STRD;
    let eq = true;
    for (let d = 0; d < STRD; d++) {
      if (aF[off + d] !== bF[d]) { eq = false; break; }
    }
    if (eq) return this.vals[id];
    h = (h + 1) & this.mask;
  }
};

// Insert the key b / bF with value out. Probes the CURRENT table
// (never trusts a slot derived before the possibly growing recursive
// computation): if the key is already present (a transposition stored
// it in the meantime) the value is overwritten and n is NOT
// incremented -- exactly the JS Map semantics of the K0893 engine's
// memo.set. Growth (when it happens) re-probes from scratch.
CompactMemo.prototype.insert = function (b, bF, out) {
  if (this.n + 1 > this.limit) {
    this.grow();
  }
  let h = this.hash(b) & this.mask;
  const table = this.table;
  const STRD = this.STRD;
  for (;;) {
    const e = table[h];
    if (e === 0) {
      const id = this.n;
      this.arenaF.set(bF, id * STRD);
      this.vals[id] = out;
      table[h] = id + 1;
      this.n++;
      return;
    }
    const id = e - 1;
    const off = id * STRD;
    const aF = this.arenaF;
    let eq = true;
    for (let d = 0; d < STRD; d++) {
      if (aF[off + d] !== bF[d]) { eq = false; break; }
    }
    if (eq) { this.vals[id] = out; return; }   // transposition: overwrite
    h = (h + 1) & this.mask;
  }
};

CompactMemo.prototype.grow = function () {
  const oldCap = this.cap;
  const oldN = this.n;
  const oldVals = this.vals;
  this.cap = oldCap * 2;
  this.mask = this.cap - 1;
  this.limit = (this.cap * 0.6) | 0;
  this.table = new Uint32Array(this.cap);
  const newArena = new Uint8Array(this.STR * this.cap);
  newArena.set(this.arena.subarray(0, oldN * this.STR), 0);
  this.arena = newArena;
  this.arenaF = new Float64Array(newArena.buffer);
  const newVals = new Uint32Array(this.cap);
  newVals.set(oldVals.subarray(0, oldN), 0);
  this.vals = newVals;
  // rehash: recompute the hash of every stored arena entry
  const KW = this.KW;
  const STR = this.STR;
  const table = this.table;
  const arena = this.arena;
  for (let id = 0; id < oldN; id++) {
    let h = 0x811c9dc5;
    const base = id * STR;
    for (let i = 0; i < KW; i++) {
      h ^= arena[base + i];
      h = Math.imul(h, 0x01000193);
    }
    h ^= h >>> 15;
    h = Math.imul(h, 0x2545f491);
    h ^= h >>> 13;
    let idx = h & this.mask;
    while (table[idx] !== 0) idx = (idx + 1) & this.mask;
    table[idx] = id + 1;
  }
};

function maskRun(atoms, r, budget) {
  const sizes = [0, 0, 0];
  for (let i = 1; i <= 3; i++) {
    let t = 0;
    for (let m = 1; m <= 7; m++) if ((m >> (i - 1)) & 1) t += atoms[m - 1];
    sizes[i - 1] = t;
  }
  const counts = new Int32Array(7 * r);          // counts[atom*r + player]
  const memo = new CompactMemo(r);
  // per-depth scratch key buffers (max recursion depth is bounded by
  // the total stone count plus elimination nesting; 96 is ample for
  // cap<=12, r<=16)
  const scratch = [];
  const scratchF = [];
  for (let d = 0; d < 96; d++) {
    const b = new Uint8Array(memo.STR);
    scratch.push(b);
    scratchF.push(new Float64Array(b.buffer));
  }
  let depth = 0;
  let nodes = budget;
  const fullActive = (1 << r) - 1;
  const flMask = (1 << r) - 1;

  function rec(mover, active) {
    const b = scratch[depth];
    b[0] = mover;
    b[1] = active & 0xff;
    b[2] = (active >> 8) & 0xff;
    for (let i = 0; i < 7 * r; i++) b[3 + i] = counts[i];
    depth++;
    const got = memo.lookup(b, scratchF[depth - 1]);
    if (got >= 0) { depth--; return got; }
    if (--nodes < 0) throw new Error('budget exhausted');

    let occ = 0;
    for (let m = 0; m < 7; m++) {
      const base = m * r;
      let s = 0;
      for (let p = 0; p < r; p++) s += counts[base + p];
      if (s !== 0) occ |= 1 << m;
    }
    let out;
    let maximal = false;
    for (let i = 1; i <= 3; i++) {
      if ((occ & INV_STAR[i]) !== 0) continue;
      let t = 0;
      const st = STAR[i];
      for (let m = 0; m < 7; m++) {
        if ((st >> m) & 1) {
          const base = m * r;
          for (let p = 0; p < r; p++) t += counts[base + p];
        }
      }
      if (t === sizes[i - 1]) { maximal = true; break; }
    }
    if (maximal) {
      const loser = mover;
      const newActive = active & ~(1 << loser);
      let na = newActive, cnt = 0;
      while (na) { cnt++; na &= na - 1; }
      let sv;
      if (cnt === 1) {
        let last = newActive, bidx = 0;
        while (((last >> bidx) & 1) === 0) bidx++;
        sv = 1 << bidx;
      } else {
        // per-call save buffer: eliminations NEST for r >= 4 (4->3->2),
        // so the outer restore must not see an inner elimination's
        // saved values (a shared buffer clobbers the outer restore).
        const saved = new Int32Array(7);
        for (let m = 0; m < 7; m++) {
          const bidx = m * r;
          saved[m] = counts[bidx + loser];
          counts[bidx + loser] = 0;
        }
        const res = rec(nextActive(loser, r, newActive), newActive);
        for (let m = 0; m < 7; m++) counts[m * r + loser] = saved[m];
        sv = res >> r;
      }
      out = (sv << r) | (1 << loser);
    } else {
      let svm = 0, flm = 0;
      const nm = nextActive(mover, r, active);
      for (let mi = 0; mi < 7; mi++) {
        const base = mi * r;
        let tot = 0;
        for (let p = 0; p < r; p++) tot += counts[base + p];
        if (atoms[mi] - tot <= 0) continue;
        let legal = false;
        for (let i = 1; i <= 3; i++) {
          if ((occ & INV_STAR[i]) === 0 && ((STAR[i] >> mi) & 1)) {
            legal = true;
            break;
          }
        }
        if (!legal) continue;
        counts[base + mover] += 1;
        const res = rec(nm, active);
        counts[base + mover] -= 1;
        svm |= res >> r;
        flm |= res & flMask;
      }
      out = (svm << r) | flm;
    }
    memo.insert(b, scratchF[depth - 1], out);
    depth--;
    return out;
  }

  const packed = rec(0, fullActive);
  return {
    sv: packed >> r,
    fl: packed & flMask,
    states: memo.n,
  };
}

function main() {
  const [profPath, rArg, outPath, startArg] = process.argv.slice(2);
  if (!profPath || !rArg || !outPath) {
    process.stderr.write(
      'usage: node mask_engine_fast2.js profs.json R out.jsonl [start]\n');
    process.exit(2);
  }
  const r = parseInt(rArg, 10);
  const start = startArg ? parseInt(startArg, 10) : 0;
  const profs = JSON.parse(fs.readFileSync(profPath, 'utf8'));
  if (start === 0) {
    fs.writeFileSync(outPath, '');
  }
  const fd = fs.openSync(outPath, 'a');
  let buf = [];
  const t0 = Date.now();
  for (let i = start; i < profs.length; i++) {
    const atoms = profs[i];
    const res = maskRun(atoms, r, 200_000_000);
    const survivors = [];
    for (let p = 0; p < r; p++) if ((res.sv >> p) & 1) survivors.push(p);
    const firstLosers = [];
    for (let p = 0; p < r; p++) if ((res.fl >> p) & 1) firstLosers.push(p);
    buf.push(JSON.stringify({
      i: i,
      atoms: atoms,
      determined: survivors.length === 1,
      survivors: survivors,
      first_losers: firstLosers,
      states: res.states,
    }));
    if (buf.length >= 128) {
      fs.writeSync(fd, buf.join('\n') + '\n');
      buf = [];
    }
    if ((i - start) % 2000 === 1999) {
      process.stderr.write(
        `r=${r} ${i + 1}/${profs.length} ` +
        `${Date.now() - t0} ms elapsed\n`);
    }
  }
  if (buf.length) fs.writeSync(fd, buf.join('\n') + '\n');
  fs.closeSync(fd);
  process.stderr.write(`r=${r} DONE ${profs.length - start} records ` +
    `in ${Date.now() - t0} ms\n`);
}

main();
