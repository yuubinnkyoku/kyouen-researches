const S = require('./sat.js');
const fs = require('fs');
const [w,m,q] = process.argv.slice(2,5).map(Number);
const capArg = process.argv[5];
const opts = capArg ? { maxStones: Number(capArg) } : {};
const { enc, cell, P } = S.encode(w,m,q,opts);
const out = fs.readFileSync(process.argv[6],'utf8');
const lits = [];
for (const line of out.split('\n')) if (line.startsWith('v ')) for (const t of line.slice(2).trim().split(/\s+/)) lits.push(Number(t));
const val = {}; for (const l of lits) { if (l===0) continue; val[Math.abs(l)] = l>0; }
const stones = [];
for (let i=0;i<P.length;i++) if (val[cell[i]]) stones.push(P[i]);
const verify = S.verifyConfig(w,m,q,stones);
console.log(JSON.stringify({w,m,q,maxStones:capArg?Number(capArg):null,stones,verify}));
