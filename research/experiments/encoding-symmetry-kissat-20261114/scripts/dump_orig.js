const S = require('./sat.js');
const [w,m,q] = process.argv.slice(2,5).map(Number);
const capArg = process.argv[5];
const opts = capArg ? { maxStones: Number(capArg) } : {};
const t0=Date.now();
const { enc } = S.encode(w,m,q,opts);
require('fs').writeFileSync(process.argv[6], S.toDimacs(enc));
console.log(JSON.stringify({w,m,q,maxStones:capArg?Number(capArg):null,vars:enc.nv,clauses:enc.clauses.length,ms:Date.now()-t0}));
