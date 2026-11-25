// sat_enum.mjs — enumerate ALL D4-lex-minimal models of the pinned v2.1
// at-most-k maximal-safe encoding (enc_sat2.mjs, byte-identical to the
// published s12-s13 machine) for n=7, k=7, by iterative blocking of the
// stone-indicator assignment (¬x_c for the model's stones).
//
// Each model's stone set is a maximal-safe configuration with <= k stones
// that is the lex-leader (index-lexicographic minimum) of its D4 orbit.
// The published s_7 >= 7 exclusion implies every model has exactly 7 stones;
// this is RE-DERIVED here, not assumed (model stone counts are recorded).
//
// Usage: node sat_enum.mjs <n> <k> <workdir> <out.json>
import * as fs from 'node:fs';
import { execFileSync, spawnSync } from 'node:child_process';

const [nArg, kArg, workdir, outPath] = process.argv.slice(2);
const n = parseInt(nArg, 10), k = parseInt(kArg, 10);
const N = n * n;

fs.mkdirSync(workdir, { recursive: true });
const cnfPath = `${workdir}/n${n}k${k}.cnf`;
if (!fs.existsSync(cnfPath)) {
  execFileSync('node', ['pinned/enc_sat2.mjs', String(n), String(k), `--out=${cnfPath}`, `--meta=${workdir}/meta.json`], { stdio: 'inherit' });
}
const base = fs.readFileSync(cnfPath, 'utf8');
const header = base.slice(0, base.indexOf('\n') + 1);
const bodyLines = base.split('\n').slice(1).filter(l => l.length);
const headerM = header.match(/p cnf (\d+) (\d+)/);
const nVars = parseInt(headerM[1], 10);
const nBaseClauses = parseInt(headerM[2], 10);

const models = [];
let iter = 0;
const t0 = Date.now();
while (true) {
  iter++;
  const cur = `${workdir}/cur_${iter}.cnf`;
  const blocks = models.map(st => st.stones.map(c => -(c + 1)).join(' ') + ' 0\n').join('');
  const cl = nBaseClauses + models.length;
  fs.writeFileSync(cur, `p cnf ${nVars} ${cl}\n` + bodyLines.join('\n') + '\n' + blocks);
  const r = spawnSync('./pinned/kissat', [cur], { encoding: 'utf8' });
  const stdout = r.stdout;
  if (stdout.includes('UNSATISFIABLE')) break;
  if (!(stdout.includes('SATISFIABLE'))) { console.error('unexpected status', r.status, String(r.stdout).slice(0, 200)); process.exit(1); }
  // decode stones: positives among 1..N
  const lits = [];
  for (const l of stdout.split('\n')) if (l.startsWith('v ')) for (const t of l.slice(2).trim().split(/\s+/)) if (t) lits.push(parseInt(t, 10));
  const stones = lits.filter(x => x >= 1 && x <= N).map(x => x - 1).sort((a, b) => a - b);
  if (stones.length !== new Set(stones).size) { console.error('dup stone literal'); process.exit(1); }
  const totalPos = lits.filter(x => x > 0).length;
  models.push({ iter, stones, size: stones.length, outLits: lits.length, posLits: totalPos });
  if (Date.now() - t0 > 1000 * 60 * 20) { console.error('time budget'); process.exit(1); }
}
const out = {
  n, k, nVars, nBaseClauses, iterations: iter - 1,
  models: models.map(m => ({ stones: m.stones, size: m.size })),
  cnf_sha256: (await import('node:crypto')).createHash('sha256').update(base).digest('hex'),
  elapsedMs: Date.now() - t0,
};
fs.writeFileSync(outPath, JSON.stringify(out, null, 1));
console.log(JSON.stringify({ models: models.length, iterations: iter - 1, sizes: models.map(m => m.size), elapsedMs: out.elapsedMs }));
