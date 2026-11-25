// sat4.js — three-row q4 lane: full row-sum partition encoding (extension of sat3.js).
// Usage: node sat4.js 3 m q --rspec="Y:K,..." [--lex=H,V] out.cnf
//   --rspec lists rows with an EXACT stone count constraint (complete partition piece).
//   A deficient row is expressed as listing its exhaustive k-pieces externally,
//   or here: --rspec with exact counts for any subset of rows; other rows free.
// Soundness note: each piece condition "row y has exactly K stones for all listed rows"
// is invariant under H; it is V-compatible iff the multiset of row constraints is
// V-symmetric (row y <-> row w-1-y constraints equal or absent symmetric) — the
// caller is responsible for using V/HV lex only on V-compatible pieces
// (enforced below for w=3).
'use strict';
const { encodeCore, totalizerAtMost, lexLeader, toDimacs2 } = require('./sat2.js');

const SIG = {
  H: (x, y, m, w) => [m - 1 - x, y],
  V: (x, y, m, w) => [x, w - 1 - y],
  HV: (x, y, m, w) => [m - 1 - x, w - 1 - y],
};

function dump4(w, m, q, rspec, lex) {
  const { enc, cell, P, curves } = encodeCore(w, m, q);
  for (const [y, k] of Object.entries(rspec).map(a => [Number(a[0]), Number(a[1])])) {
    const rowCells = [];
    for (let x = 0; x < m; x++) rowCells.push(cell[y * m + x]);
    if (k === 0) {
      for (const c of rowCells) enc.add([[-c]]);
    } else {
      const root = totalizerAtMost(enc, rowCells, k);  // forbids >= k+1
      if (!root[k]) throw new Error('rspec root var missing k=' + k);
      enc.add([[root[k]]]);                            // require >= k
    }
  }
  for (const nm of lex || []) lexLeader(enc, cell, m, w, (x, y) => SIG[nm](x, y, m, w));
  return {
    meta: { w, m, q, curves: curves.length, mode: 'rspec',
            rspec: Object.fromEntries(Object.entries(rspec).map(([y, k]) => [y, Number(k)])),
            lex: lex || [], vars: enc.nv, clauses: enc.clauses.length },
    dimacs: toDimacs2(enc)
  };
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const [w, m, q] = [Number(args[0]), Number(args[1]), Number(args[2])];
  let lex = [], rspec = {}, out = null;
  for (const a of args.slice(3)) {
    if (a.startsWith('--lex=')) lex = a.slice(6).split(',').filter(s => SIG[s]);
    else if (a.startsWith('--rspec=')) {
      for (const part of a.slice(8).split(',')) {
        if (!part) continue;
        const [y, k] = part.split(':').map(Number);
        rspec[y] = k;
      }
    } else if (!out) out = a;
  }
  // V-compatibility guard for w=3: rows 0 and 2 constraint pattern must be symmetric
  if (w === 3 && (lex.includes('V') || lex.includes('HV'))) {
    const ok = (rspec[0] === undefined) === (rspec[2] === undefined) &&
               (rspec[0] === undefined || rspec[0] === rspec[2]);
    if (!ok) throw new Error('unsound: V/HV lex with asymmetric row constraints');
  }
  const { meta, dimacs } = dump4(w, m, q, rspec, lex);
  require('fs').writeFileSync(out, dimacs);
  meta.file = out;
  console.log(JSON.stringify(meta));
}
