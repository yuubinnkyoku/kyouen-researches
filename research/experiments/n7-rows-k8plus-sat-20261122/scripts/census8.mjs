// census8.mjs — enumerate ALL D4-lex-leader models of the n7 at-most-8 encoding
// minus the two known 7-stone leaders (O1, O2), i.e. the complete lex-leader
// census of the 8-stone maximal-safe row, by iterative model blocking.
//
// The set of models is complete for the 8-stone row iff this loop terminates
// with UNSAT (every 8-stone orbit's lex-minimal member is enumerated exactly
// once, because the lex-leader gates of enc_sat2 admit exactly the orbit
// lex-minima [P1..P5 machine-verified, K1221]).
//
// Resume-safe: appends each found leader to <state.json> incrementally.
// Budget: --maxsec (wall clock) and --maxmodels; on INDET/timeout records it.
//
// Usage: node census8.mjs <workdir> <stateFile> [--maxsec=S] [--maxmodels=M]
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const args = process.argv.slice(2);
const [basePath, statePath] = [args[0], args[1]];
const opt = {};
for (const a of args.slice(2)) { const m = a.match(/^--([a-z]+)=(.*)$/); if (m) opt[m[1]] = m[2]; }
const maxsec = parseFloat(opt.maxsec ?? '200');
const maxmodels = parseInt(opt.maxmodels ?? '100000', 10);

const O1 = [10, 13, 14, 17, 19, 21, 45];
const O2 = [18, 21, 22, 26, 31, 32, 38];

const base = readFileSync(basePath, 'utf8');
const lines = base.split('\n');
const hdr = lines[0];
const m0 = hdr.match(/^p cnf (\d+) (\d+)$/);
const nVars = parseInt(m0[1], 10), nCls = parseInt(m0[2], 10);
const body = lines.slice(1).filter(l => l.length > 0);
if (body.length !== nCls) throw new Error('clause mismatch');

let state;
if (existsSync(statePath)) {
  state = JSON.parse(readFileSync(statePath, 'utf8'));
} else {
  state = { basePath, baseSha256: createHash('sha256').update(base).digest('hex'), nVars, nClausesBase: nCls, leaders: [], iter: 0, complete: false, indet: false, iterMs: [], history: [] };
}

const t0 = Date.now();
let indet = false;
while (!state.complete && state.leaders.length < maxmodels) {
  const el = Date.now() - t0;
  if (el > maxsec * 1000) { state.note = 'wall-clock budget reached'; break; }
  state.iter++;
  const blocks = [O1, O2, ...state.leaders]
    .map(S => S.map(c => -(c + 1)).join(' ') + ' 0\n').join('');
  const cur = `p cnf ${nVars} ${nCls + 2 + state.leaders.length}\n` + body.join('\n') + '\n' + blocks;
  const cnfPath = statePath + '.cur.cnf';
  writeFileSync(cnfPath, cur);
  const t1 = Date.now();
  const r = spawnSync('/tmp/kissat-4.0.4-linux-amd64', ['--time=' + Math.max(10, Math.ceil(maxsec - el / 1000)), cnfPath], { encoding: 'utf8' });
  const ms = Date.now() - t1;
  const out = r.stdout ?? '';
  if (!out.includes('s SATISFIABLE') && !out.includes('s UNSATISFIABLE')) {
    state.indet = true; state.indetIter = state.iter; state.note = 'kissat INDET/timeout at iter ' + state.iter;
    indet = true; break;
  }
  if (out.includes('s UNSATISFIABLE')) { state.complete = true; state.unsatIterMs = ms; break; }
  // decode stones: positives among cell vars 1..49 in v lines
  const lits = [];
  for (const l of out.split('\n')) if (l.startsWith('v ')) for (const t of l.slice(2).trim().split(/\s+/)) if (t) lits.push(parseInt(t, 10));
  const stones = lits.filter(v => v > 0 && v <= 49).map(v => v - 1).sort((a, b) => a - b);
  if (stones.length !== 8) { throw new Error('model with ' + stones.length + ' stones at iter ' + state.iter); }
  state.leaders.push(stones);
  state.iterMs.push(ms);
  state.history.push({ iter: state.iter, ms, stones });
  writeFileSync(statePath, JSON.stringify(state));
}
writeFileSync(statePath, JSON.stringify(state));
console.log(JSON.stringify({ complete: state.complete, indet: state.indet, nLeaders: state.leaders.length, iter: state.iter, wallMs: Date.now() - t0, note: state.note ?? null }));
