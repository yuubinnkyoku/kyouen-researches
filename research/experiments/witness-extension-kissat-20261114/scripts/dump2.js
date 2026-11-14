const S = require('./sat.js');
const [w,m,q,cap] = process.argv.slice(2,6).map(Number);
const { enc, cell, curves, counters, P } = S.encode(w,m,q,{ maxStones: cap });
const rowNegGe = [];
for (const c of counters) {
  if (c.tag && c.tag.startsWith('line:0,1,')) {
    const y = -Number(c.tag.split(',')[2]);
    if (y < Math.ceil(w/2)) rowNegGe.push(-c.s[c.xs.length-1][q-1]);
  }
}
if (rowNegGe.length !== Math.ceil(w/2)) throw new Error('rows '+rowNegGe.length);
enc.add([rowNegGe]);
require('fs').writeFileSync(process.argv[6], S.toDimacs(enc));
console.log(JSON.stringify({w,m,q,cap,vars:enc.nv,clauses:enc.clauses.length}));
