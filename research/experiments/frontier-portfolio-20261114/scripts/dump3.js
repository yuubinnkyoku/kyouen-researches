// dump3.js w m q cap rowY out.cnf -- deficient row FIXED to rowY (unit: row rowY has <= q-2 stones)
const S = require('./sat.js');
const [w, m, q, cap, rowY] = process.argv.slice(2, 7).map(Number);
const { enc, cell, curves, counters, P } = S.encode(w, m, q, { maxStones: cap });
let unit = null;
for (const c of counters) {
  if (c.tag && c.tag.startsWith('line:0,1,') && -Number(c.tag.split(',')[2]) === rowY) unit = -c.s[c.xs.length - 1][q - 1];
}
if (!unit) throw new Error('row not found ' + rowY);
enc.add([[unit]]);
require('fs').writeFileSync(process.argv[7], S.toDimacs(enc));
console.log(JSON.stringify({ w, m, q, cap, rowY, vars: enc.nv, clauses: enc.clauses.length }));
