// sat4.js — second-stone position split (--x2) on top of sat3.js dumpClass.
// For a single-deficient-row instance with --krow=y:k (k>=2) and --minpos=p on
// row y, --x2=B pins the 2nd-leftmost stone of row y at column B:
//   cells (y, p+1 .. B-1) = false (units), cell (y, B) = true (unit).
// The complete case split over B in {p+1 .. m-2} is exhaustive and disjoint
// (plain case analysis on the stone column — no symmetry assumption needed),
// so all-UNSAT over B proves the (class, krow, minpos) bucket UNSAT.
// NOTE: --x2 with --lex is unsound together for the same reason as minpos+lex
// (lex leaders are not preserved by the extra pin); do not combine.
'use strict';
const fs = require('fs');
const path = require('path');
const S3 = require(path.join(__dirname, 'sat3.js'));
const S2 = require(path.join(__dirname, 'sat2.js'));

function dumpClassX2(w, m, q, D, opts) {
  if (opts.minpos == null || opts.x2 == null) throw new Error('--minpos and --x2 required together');
  if (opts.lex && opts.lex.length) throw new Error('--x2 with --lex is unsound');
  const { enc, cell } = S3.dumpClass(w, m, q, D, opts); // applies class/krow/minpos
  const y = D[0], p = opts.minpos, B = opts.x2;
  if (B <= p || B > m - 2) throw new Error('x2 out of range (' + (p + 1) + '..' + (m - 2) + ')');
  for (let x = p + 1; x < B; x++) enc.add([[-cell[y * m + x]]]);
  enc.add([[cell[y * m + B]]]);
  const meta = { w, m, q, class: D.slice().sort((a, b) => a - b), krow: opts.krow || [], minpos: p, x2: B, lex: [], vars: enc.nv, clauses: enc.clauses.length };
  return { enc, meta };
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'decode') {
    // identical to sat3.js decode
    const [w, m, q] = [Number(args[1]), Number(args[2]), Number(args[3])];
    const txt = fs.readFileSync(args[4], 'utf8');
    const out = S3.decode(w, m, q, txt);
    const jo = args.find(a => a.startsWith('--json='));
    if (jo) fs.writeFileSync(jo.slice(7), JSON.stringify(out, null, 1));
    console.log(JSON.stringify({ nStones: out.nStones, verify: out.verify, ok: out.verify.ok }));
  } else {
    const [w, m, q] = [Number(args[0]), Number(args[1]), Number(args[2])];
    let i = 3, cls = null, out = null, krow = [], minpos = null, x2 = null;
    for (; i < args.length; i++) {
      const a = args[i];
      if (a.startsWith('--class=')) cls = a.slice(8).split(',').map(Number);
      else if (a.startsWith('--krow=')) krow = a.slice(7).split(',');
      else if (a.startsWith('--minpos=')) minpos = Number(a.slice(9));
      else if (a.startsWith('--x2=')) x2 = Number(a.slice(5));
      else if (!out) out = a;
    }
    if (cls == null) throw new Error('--class= required');
    const { enc, meta } = dumpClassX2(w, m, q, cls, { krow, minpos, x2 });
    fs.writeFileSync(out, S2.toDimacs2(enc));
    meta.file = out;
    console.log(JSON.stringify(meta));
  }
}
module.exports = { dumpClassX2 };
