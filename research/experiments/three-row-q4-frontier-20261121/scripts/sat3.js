// sat3.js — three-row q4 lane: deficient-row stone-count exact split (extension of sat2.js).
// Reuses sat2.js exports (encodeCore, totalizerAtMost, lexLeader, toDimacs2, S) verbatim.
// Modes: --rowY=Y (row Y deficient: <= q-2 stones, same as sat2 rowfixed) plus
//         --kex=K (exactly K stones in row Y; K in 0..q-2)   [complete case split]
//         --lex=H,V / HV as in sat2.
// Soundness: the piece condition "row Y has exactly K stones" is invariant under
// H (column reflection) and, for Y in the middle row, V (row reflection); pieces
// K = 0..q-2 union to the full deficient-row space.
// Usage: node sat3.js w m q --rowY=Y --kex=K [--lex=H,V] out.cnf
'use strict';
const S2 = require('./sat2.js');
const { encodeCore, totalizerAtMost, lexLeader, toDimacs2, S } = S2;

const SIG = {
  H: (x, y, m, w) => [m - 1 - x, y],
  V: (x, y, m, w) => [x, w - 1 - y],
  HV: (x, y, m, w) => [m - 1 - x, w - 1 - y],
};

function dump3(w, m, q, opts) {
  const { enc, cell, P, n, curves, rowGe } = encodeCore(w, m, q);
  if (opts.rowY == null) throw new Error('--rowY required');
  const rv = rowGe[opts.rowY];
  if (!rv) throw new Error('row not found ' + opts.rowY);
  enc.add([[-rv]]);                        // row rowY deficient (<= q-2 stones)
  const rowCells = [];
  for (let x = 0; x < m; x++) rowCells.push(cell[opts.rowY * m + x]);
  if (opts.kex != null) {
    const k = opts.kex;
    if (k === 0) {
      for (const c of rowCells) enc.add([[-c]]);
    } else {
      const root = totalizerAtMost(enc, rowCells, k);   // forbids >= k+1
      // top node covers all m leaves; root[k] = ">= k" auxiliary output
      if (!root[k]) throw new Error('kex root var missing k=' + k);
      enc.add([[root[k]]]);                             // and require >= k
    }
  }
  for (const nm of (opts.lex || []))
    lexLeader(enc, cell, m, w, (x, y) => SIG[nm](x, y, m, w));
  return {
    meta: { w, m, q, curves: curves.length, mode: 'rowfixed-kex', rowY: opts.rowY,
            kex: opts.kex, lex: opts.lex || [], vars: enc.nv, clauses: enc.clauses.length },
    dimacs: toDimacs2(enc)
  };
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const [w, m, q] = [Number(args[0]), Number(args[1]), Number(args[2])];
  let i = 3, lex = [], rowY = null, kex = null, out = null;
  for (; i < args.length; i++) {
    const a = args[i];
    if (a.startsWith('--lex=')) lex = a.slice(6).split(',').filter(s => SIG[s]);
    else if (a.startsWith('--rowY=')) rowY = Number(a.slice(7));
    else if (a.startsWith('--kex=')) kex = Number(a.slice(6));
    else if (!out) out = a;
  }
  if (w === 3 && kex !== null && (kex < 0 || kex > q - 2)) throw new Error('kex range');
  if (w === 3 && rowY !== null && rowY !== (w - 1 - rowY) && (lex.includes('V') || lex.includes('HV')))
    throw new Error('unsound: V/HV lex with non-middle fixed row');
  const { meta, dimacs } = dump3(w, m, q, { rowY, kex, lex });
  require('fs').writeFileSync(out, dimacs);
  meta.file = out;
  console.log(JSON.stringify(meta));
}
