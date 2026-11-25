// permute.js in.cnf out.cnf map.json seed
const fs = require('fs');
const [inp, outp, mapp, seedArg] = process.argv.slice(2);
const seed = Number(seedArg);
let s = seed >>> 0 || 1;
function rnd() { s ^= s << 13; s >>>= 0; s ^= s >> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; }
const lines = fs.readFileSync(inp, 'utf8').split('\n').filter(l => l.length);
const header = lines[0].split(' ');
const nv = Number(header[2]);
const perm = new Array(nv + 1);
for (let i = 1; i <= nv; i++) perm[i] = i;
for (let i = nv; i >= 2; i--) { const j = 1 + Math.floor(rnd() * i); const t = perm[i]; perm[i] = perm[j]; perm[j] = t; }
const clauses = lines.slice(1);
for (let i = clauses.length - 1; i >= 1; i--) { const j = Math.floor(rnd() * (i + 1)); const t = clauses[i]; clauses[i] = clauses[j]; clauses[j] = t; }
const out = ['p cnf ' + nv + ' ' + clauses.length];
for (const c of clauses) {
  const lits = c.trim().split(/\s+/).map(Number).filter(x => x !== 0);
  for (let i = lits.length - 1; i >= 1; i--) { const j = Math.floor(rnd() * (i + 1)); const t = lits[i]; lits[i] = lits[j]; lits[j] = t; }
  out.push(lits.map(l => (l > 0 ? perm[l] : -perm[-l])).join(' ') + ' 0');
}
fs.writeFileSync(outp, out.join('\n') + '\n');
fs.writeFileSync(mapp, JSON.stringify({ nv, seed, perm }));
console.log(JSON.stringify({ nv, clauses: clauses.length, seed }));
