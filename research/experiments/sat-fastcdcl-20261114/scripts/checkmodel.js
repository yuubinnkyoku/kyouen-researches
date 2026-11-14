const fs = require('fs');
const cnf = fs.readFileSync(process.argv[2], 'utf8').split('\n');
const model = fs.readFileSync(process.argv[3], 'utf8').trim().split(/\s+/).map(Number);
const val = {}; for (const l of model) val[l > 0 ? l : -l] = l > 0 ? 1 : -1;
let bad = 0, ncl = 0;
for (const line of cnf) {
  const t = line.trim();
  if (!t || t[0] === 'p' || t[0] === 'c') continue;
  ncl++;
  let sat = false;
  for (const s of t.split(/\s+/)) { const x = parseInt(s, 10); if (isNaN(x) || x === 0) continue; if ((val[x > 0 ? x : -x] || 0) === (x > 0 ? 1 : -1)) { sat = true; break; } }
  if (!sat) { bad++; if (bad <= 3) console.log('UNSAT clause:', t); }
}
console.log(JSON.stringify({ clauses: ncl, unsatisfied: bad }));
