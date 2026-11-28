// pin.js — append row exact-count (krow) + minpos pins to a sat3s rowfixed CNF.
// Usage: M=<m> node pin.js base.cnf out.cnf --row=Y --k=K [--minpos=P]
// Cell var of point (x,y) = y*m + x + 1 (sat.js pts is row-major, cells are vars 1..n).
// Counter = sat3s.js counter() verbatim (zero encoding drift).
'use strict';
const fs = require('fs');
const path = require('path');
const { counter } = require(path.join(__dirname, 'sat3s.js'));

function main() {
  const args = process.argv.slice(2);
  const [base, out] = [args[0], args[1]];
  let row = null, k = null, minpos = null;
  for (const a of args.slice(2)) {
    if (a.startsWith('--row=')) row = Number(a.slice(6));
    else if (a.startsWith('--k=')) k = Number(a.slice(4));
    else if (a.startsWith('--minpos=')) minpos = Number(a.slice(9));
  }
  const m = Number(process.env.M);
  if (!m) throw new Error('M env required');
  const raw = fs.readFileSync(base, 'utf8');
  const nl = raw.indexOf('\n');
  const hm = raw.slice(0, nl).match(/^p cnf (\d+) (\d+)$/);
  if (!hm) throw new Error('bad header');
  const nv0 = Number(hm[1]), nc = Number(hm[2]);
  const body = raw.slice(nl + 1);
  const extra = [];
  const enc = {
    nv: nv0,
    v() { return ++this.nv; },
    add(cls) { for (const c0 of cls) { const c = c0.filter(l => l !== 0); if (c.length) extra.push(c.join(' ') + ' 0'); } },
  };
  const rowCells = [];
  for (let x = 0; x < m; x++) rowCells.push(row * m + x + 1);
  if (k != null) {
    if (k === 0) { for (const v of rowCells) enc.add([[-v]]); }
    else {
      const s = counter(enc, rowCells, k + 1); // chain '>= j' up to j = k+1
      enc.add([[-s[rowCells.length - 1][k + 1]]]); // forbid >= k+1  (at most k)
      enc.add([[s[rowCells.length - 1][k]]]);     // require >= k     (at least k)
    }
  }
  if (minpos != null) {
    for (let x = 0; x < minpos; x++) enc.add([[-rowCells[x]]]);
    enc.add([[rowCells[minpos]]]);
  }
  const outStr = 'p cnf ' + enc.nv + ' ' + (nc + extra.length) + '\n' + body + (body.endsWith('\n') ? '' : '\n') + (extra.length ? extra.join('\n') + '\n' : '');
  fs.writeFileSync(out, outStr);
  console.log(JSON.stringify({ base, out, row, k, minpos, addedClauses: extra.length, nv: enc.nv, nc: nc + extra.length }));
}
main();
