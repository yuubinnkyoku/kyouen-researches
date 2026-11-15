// sat3.js — class-split / exact-count / minpos extension on top of sat2.js (K0810 core).
// Modes:
//   --class=D       D = comma row indices (deficient rows: <= q-2 stones);
//                   rows outside D forced FULL (exactly q-1) via unit rowGe[y].
//   --krow=y:k      exact stone count k of deficient row y (unit pins on the row >=j chain).
//   --minpos=P      leftmost stone of first deficient row pinned at column P (sound H-split).
//   --lex=H,V,HV    lex-leader symmetry breaking (sound for H with class/krow/minpos since
//                   H preserves rows; V/HV do NOT preserve class — use only with H).
// Usage:
//   node sat3.js w m q --class=D [--krow=y:k ...] [--minpos=P] [--lex=H] out.cnf
//   node sat3.js decode w m q model.txt   # parse kissat v-lines -> stones -> verifyConfig
'use strict';
const fs = require('fs');
const path = require('path');
const S2 = require(path.join(__dirname, 'sat2.js'));
const S = S2.S;

function encodeCore2(w, m, q) {
  const { P, n, curves } = S.buildCensus(w, m, q);
  const enc = { nv: 0, clauses: [], v() { this.nv++; return this.nv; }, add(cls) { for (const c0 of cls) { const c = c0.filter(l => l !== 0); if (c.length) this.clauses.push(c); } } };
  const cell = new Array(n).fill(0).map(() => enc.v());
  const geVars = [];
  const rowGe = {}, rowChain = {};
  const counter = (xs, K) => {
    const nE = xs.length;
    const s = Array.from({ length: nE }, () => new Array(K + 1).fill(0));
    for (let i = 0; i < nE; i++) for (let j = 1; j <= Math.min(K, i + 1); j++) s[i][j] = enc.v();
    for (let i = 0; i < nE; i++) for (let j = 1; j <= Math.min(K, i + 1); j++) {
      const Sv = s[i][j];
      if (i === 0) { enc.add([[xs[0], -Sv]]); enc.add([[-xs[0], Sv]]); }
      else {
        const Sp = (j <= i) ? s[i - 1][j] : 0;
        const Spp = (j >= 2 && j - 1 <= i) ? s[i - 1][j - 1] : 0;
        if (j <= i) {
          enc.add([[-Sv, Sp, xs[i]]]);
          if (Spp) enc.add([[-Sv, Sp, Spp]]);
          enc.add([[-Sp, Sv]]);
          if (Spp) enc.add([[-xs[i], -Spp, Sv]]);
          else enc.add([[-xs[i], Sv]]);
        } else {
          enc.add([[-Sv, xs[i]]]);
          enc.add([[-Sv, Spp]]);
          enc.add([[-xs[i], -Spp, Sv]]);
        }
      }
    }
    return s;
  };
  for (const cu of curves) {
    const s = counter(cu.pts.map(p => cell[p]), q);
    const last = s[cu.pts.length - 1];
    enc.add([[-last[q]]]);
    geVars.push(last[q - 1]);
    if (cu.type === 'line' && cu.co[0] === 0 && cu.co[1] === 1) { rowGe[-cu.co[2]] = last[q - 1]; rowChain[-cu.co[2]] = last; }
  }
  const through = Array.from({ length: n }, () => []);
  curves.forEach((cu, ci) => { for (const p of cu.pts) through[p].push(geVars[ci]); });
  for (let i = 0; i < n; i++) enc.add([[cell[i], ...through[i]]]);
  return { enc, cell, P, n, curves, rowGe, rowChain };
}

function dumpClass(w, m, q, D, opts) {
  const { enc, cell, P, n, curves, rowGe, rowChain } = encodeCore2(w, m, q);
  for (let y = 0; y < w; y++) {
    if (D.includes(y)) enc.add([[-rowGe[y]]]);
    else enc.add([[rowGe[y]]]);
  }
  if (opts.krow) {
    for (const kv of opts.krow) {
      const [y, k] = kv.split(':').map(Number);
      const chain = rowChain[y];
      if (!chain) throw new Error('no row chain ' + y);
      if (k === 0) enc.add([[-chain[1]]]);
      else enc.add([[chain[k]]]);
      if (k + 1 > q) throw new Error('k too big');
      enc.add([[-chain[k + 1]]]);
    }
  }
  if (opts.minpos != null) {
    const y = D[0];
    for (let x = 0; x < opts.minpos; x++) enc.add([[-cell[y * m + x]]]);
    enc.add([[cell[y * m + opts.minpos]]]);
  }
  for (const nm of (opts.lex || [])) S2.lexLeader(enc, cell, m, w, (x, y) => ({ H: (x, y) => [m - 1 - x, y], V: (x, y) => [x, w - 1 - y], HV: (x, y) => [m - 1 - x, w - 1 - y] })[nm](x, y));
  return { enc, cell, P, n, meta: { w, m, q, class: D.slice().sort((a, b) => a - b), krow: opts.krow || [], minpos: opts.minpos, lex: opts.lex || [], vars: enc.nv, clauses: enc.clauses.length } };
}

function parseModel(txt) {
  const lits = [];
  for (const line of txt.split('\n')) {
    const t = line.trim();
    if (t.startsWith('v ')) { for (const tok of t.slice(2).trim().split(/\s+/)) { const v = Number(tok); if (Number.isFinite(v) && v !== 0) lits.push(v); } }
  }
  return lits;
}

function decode(w, m, q, modelTxt) {
  const lits = parseModel(modelTxt);
  const val = new Map();
  for (const l of lits) val.set(Math.abs(l), l > 0);
  const P = S.pts(w, m);
  const stones = [];
  for (let i = 0; i < P.length; i++) if (val.get(i + 1)) stones.push(P[i]);
  const verify = S.verifyConfig(w, m, q, stones);
  return { w, m, q, nStones: stones.length, stones, verify, modelVars: lits.length ? Math.max(...lits.map(Math.abs)) : 0 };
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'decode') {
    const [w, m, q] = [Number(args[1]), Number(args[2]), Number(args[3])];
    const txt = fs.readFileSync(args[4], 'utf8');
    const out = decode(w, m, q, txt);
    const jo = args.find(a => a.startsWith('--json='));
    if (jo) fs.writeFileSync(jo.slice(7), JSON.stringify(out, null, 1));
    console.log(JSON.stringify({ nStones: out.nStones, verify: out.verify, ok: out.verify.ok }));
  } else {
    const [w, m, q] = [Number(args[0]), Number(args[1]), Number(args[2])];
    let i = 3, cls = null, out = null, lex = [], krow = [], minpos = null;
    for (; i < args.length; i++) {
      const a = args[i];
      if (a.startsWith('--class=')) cls = a.slice(8).split(',').map(Number);
      else if (a.startsWith('--lex=')) lex = a.slice(6).split(',').filter(s => ['H', 'V', 'HV'].includes(s));
      else if (a.startsWith('--krow=')) krow = a.slice(7).split(',');
      else if (a.startsWith('--minpos=')) minpos = Number(a.slice(9));
      else if (!out) out = a;
    }
    if (cls == null) throw new Error('--class= required');
    const { enc, meta } = dumpClass(w, m, q, cls, { lex, krow, minpos });
    fs.writeFileSync(out, S2.toDimacs2(enc));
    meta.file = out;
    console.log(JSON.stringify(meta));
  }
}
module.exports = { dumpClass, decode, parseModel };
