// block_lift.mjs — append "known-leader blocking clauses" to a base at-most-k CNF
// produced by the pinned enc_sat2.mjs v2.1, producing a lifted CNF whose models
// all have stone count == k PROVIDED the leader list enumerates ALL maximal-safe
// models with < k stones under the lex-leader constraints.
//
// Blocking clause for a known model with stone set S (0-based cell indices):
//   OR_{c in S} -x_c      (forbids the exact assignment "all of S are stones")
//
// This removes ONLY assignments in which every cell of S is a stone. It is sound
// for row-k emptiness because (given the completeness of the leader list) the
// only < k-stone models of the at-most-k encoding are the listed leaders' exact
// assignments; no other assignment is removed (an assignment with all of S set
// and |S|<k stones is exactly the leader's model).
//
// --shuffle=SEED mirrors enc_sat2.mjs's variable permutation EXACTLY (same rng,
// same Fisher-Yates pass) so that cell literal c maps to the permuted id; use
// --nvars=NVARS to match the shuffled encoding's total variable count.
//
// Usage: node block_lift.mjs <base.cnf> <out.cnf> <leadersJSON> [--meta=meta.json]
//        [--shuffle=SEED] [--nvars=NVARS]
//   leadersJSON: JSON array of stone arrays, e.g. "[[10,...],[18,...]]"
import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

function rng(seed) {
  let a = seed >>> 0;
  return () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0); };
}

const args = process.argv.slice(2);
const [basePath, outPath, leadersRaw] = [args[0], args[1], args[2]];
const leaders = JSON.parse(leadersRaw);
const metaOpt = args.find(a => a.startsWith('--meta='));
const sha256 = (p) => createHash('sha256').update(readFileSync(p)).digest('hex');

const base = readFileSync(basePath, 'utf8');
const lines = base.split('\n');
const hdr = lines[0];
const m = hdr.match(/^p cnf (\d+) (\d+)$/);
if (!m) throw new Error('bad header: ' + hdr);
const [nVars, nCls] = [parseInt(m[1], 10), parseInt(m[2], 10)];
const body = lines.slice(1).filter(l => l.length > 0);
if (body.length !== nCls) throw new Error(`clause count mismatch: header ${nCls} body ${body.length}`);

const shOpt = args.find(a => /^--shuffle=/.test(a));
const nvOpt = args.find(a => /^--nvars=/.test(a));
let lit = (c) => -(c + 1);
let shuffleMeta = null;
if (shOpt) {
  const seed = parseInt(shOpt.split('=')[1], 10) >>> 0;
  const nVarsTotal = nvOpt ? parseInt(nvOpt.split('=')[1], 10) : nVars;
  const r = rng(seed);
  const ids = new Int32Array(nVarsTotal);
  for (let i = 0; i < nVarsTotal; i++) ids[i] = i + 1;
  for (let i = nVarsTotal - 1; i > 0; i--) { const j = (r() % (i + 1)); const t = ids[i]; ids[i] = ids[j]; ids[j] = t; }
  lit = (c) => -ids[c];   // cell c (0-based) -> permuted positive id, negated
  shuffleMeta = { seed, nVarsTotal };
}

const blockClauses = leaders.map(stones => stones.map(c => lit(c)).join(' ') + ' 0');
const out = `p cnf ${nVars} ${nCls + blockClauses.length}\n` + body.join('\n') + '\n' + blockClauses.join('\n') + '\n';
writeFileSync(outPath, out);
const meta = {
  basePath, baseSha256: sha256(basePath), outPath, outSha256: sha256(outPath),
  nVars, nClausesBase: nCls, nBlockClauses: blockClauses.length, nClausesOut: nCls + blockClauses.length,
  shuffle: shuffleMeta,
  leaders, blockClauses,
};
if (metaOpt) writeFileSync(metaOpt.split('=')[1], JSON.stringify(meta, null, 1) + '\n');
console.log(JSON.stringify({ outPath, outSha256: meta.outSha256, nClausesOut: meta.nClausesOut, shuffle: shuffleMeta }));
