#!/usr/bin/env node
// K0876 sweep engine: JavaScript mask twin of the Python mask_game /
// mask_verdict in verify_remo_k_branch_cap12_r456_boundary.py (that
// Python twin is the spec of record; this engine is a faithful port
// tuned for speed). Each record is a pure function of (profile, r), so
// sweep segments produced with different start indices are
// byte-identical when concatenated.
//
// CLI: node mask_engine_fast.js profs.json R out.jsonl [start]
//
// Record format (one JSON object per line, index i = position in the
// canonical cap<=12 enumeration):
//   {"i":..,"atoms":[..7 ints..],"determined":bool,
//    "survivors":[..],"first_losers":[..],"states":int}
// states == memo size (reachable state count), matching the Python
// twins. Budget is effectively unbounded (200M nodes).

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

function maskRun(atoms, r, budget) {
  const sizes = [0, 0, 0];
  for (let i = 1; i <= 3; i++) {
    let t = 0;
    for (let m = 1; m <= 7; m++) if ((m >> (i - 1)) & 1) t += atoms[m - 1];
    sizes[i - 1] = t;
  }
  const counts = new Int32Array(7 * r);          // counts[atom*r + player]
  const memo = new Map();
  const kp = new Array(7 * r + 2);
  let nodes = budget;
  const fullActive = (1 << r) - 1;

  function rec(mover, active) {
    kp[0] = mover + 1;
    kp[1] = active + 1;
    for (let i = 0; i < 7 * r; i++) kp[i + 2] = counts[i] + 1;
    const key = String.fromCharCode.apply(String, kp);
    const got = memo.get(key);
    if (got !== undefined) return got;
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
        let last = newActive, b = 0;
        while (((last >> b) & 1) === 0) b++;
        sv = 1 << b;
      } else {
        // per-call save buffer: eliminations NEST for r >= 4 (4->3->2),
        // so the outer restore must not see an inner elimination's
        // saved values (a shared buffer clobbers the outer restore).
        const saved = new Int32Array(7);
        for (let m = 0; m < 7; m++) {
          const b = m * r;
          saved[m] = counts[b + loser];
          counts[b + loser] = 0;
        }
        const res = rec(nextActive(loser, r, newActive), newActive);
        for (let m = 0; m < 7; m++) counts[m * r + loser] = saved[m];
        sv = res >> 8;
      }
      out = (sv << 8) | (1 << loser);
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
        svm |= res >> 8;
        flm |= res & 0xff;
      }
      out = (svm << 8) | flm;
    }
    memo.set(key, out);
    return out;
  }

  const packed = rec(0, fullActive);
  return {
    sv: packed >> 8,
    fl: packed & 0xff,
    states: memo.size,
  };
}

function main() {
  const [profPath, rArg, outPath, startArg] = process.argv.slice(2);
  if (!profPath || !rArg || !outPath) {
    process.stderr.write(
      'usage: node mask_engine_fast.js profs.json R out.jsonl [start]\n');
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
