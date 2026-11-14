const fs = require('fs');
const { verifyIndependent } = require('/home/user/sa/sa_machine.js');
const lines = fs.readFileSync(process.argv[2], 'utf8').trim().split('\n');
for (const line of lines) {
  try {
    const r = JSON.parse(line);
    if (!r.witness) { console.log(JSON.stringify({ case: r.case, noWitness: true, min: r.min })); continue; }
    const v = verifyIndependent(r.w, r.m, r.q, r.witness);
    const ok = v.safe && v.maximal && v.n === r.witness.length;
    console.log(JSON.stringify({ case: r.case, seed: r.seed, n: v.n, safe: v.safe, maximal: v.maximal, worstLine: v.worstLine, worstCirc: v.worstCirc, pass: ok }));
  } catch (e) { console.log(JSON.stringify({ parseError: true, msg: String(e).slice(0,80) })); }
}
