// Dual-independent verification driver for the witness WIN7-D10 certificates (2026-11-19 recovery).
// BigInt exact-determinant verifier (no engine cache) + Bareiss 4x4 integer determinant verifier
// (no engine import), then union audit: consumed winner states over all sub-roots must equal the
// certificate row set exactly, and aggregate statistics must agree between the two verifiers.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const BASE = path.dirname(fileURLToPath(import.meta.url));
const ROOTS = [
  { name: 'fifth', root: '00000000000000805202080001000000', moves: 54, rows: 55857, dir: 'out-D' },
  { name: 'sixth', root: '00000000040000801202000080100000', moves: 55, rows: 30984, dir: 'out-E' },
];
const BIGINT = path.join(BASE, 'scripts', 'verify_win7_certificate_bigint_independent.mjs');
const BAREISS = path.join(BASE, 'scripts', 'verify_bit7_win7_cert.ts');
for (const R of ROOTS) {
  const dir = path.join(BASE, R.dir);
  const certPath = path.join(dir, `win7-root-${R.root}-20261119.n11`);
  const summaryPath = path.join(dir, `win7-root-${R.root}-extraction-summary-20261119.json`);
  const verificationPath = path.join(dir, `win7-root-${R.root}-independent-verification-20261119.json`);
  const bareissPath = path.join(dir, `win7-root-${R.root}-bareiss-subroots-20261119.jsonl`);
  const unionPath = path.join(dir, `win7-root-${R.root}-bareiss-union-audit-20261119.json`);
  const summary = JSON.parse(fs.readFileSync(summaryPath, 'utf8'));
  if (summary.root !== R.root || summary.completed_moves !== R.moves) throw new Error('summary gate ' + R.name);
  const cert = fs.readFileSync(certPath);
  const certSha = crypto.createHash('sha256').update(cert).digest('hex');
  if (certSha !== summary.certificate_sha256) throw new Error('cert sha gate ' + R.name);
  const moves = summary.completed_move_list.join(',');
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'n11-verify2-'));
  const consumedPath = path.join(tempDir, 'consumed.txt');
  try {
    const big = spawnSync(process.execPath, [BIGINT, certPath, String(R.moves)], { encoding: 'utf8', maxBuffer: 16 * 1024 * 1024 });
    if (big.status !== 0) throw new Error('BigInt verifier failed ' + R.name + ': ' + big.stderr);
    const verification = JSON.parse(big.stdout.trim());
    if (verification.verdict !== 'WIN7 certificate independently verified' || verification.root_hex !== R.root
        || verification.subroots_passed !== R.moves || verification.union_missing !== 0 || verification.union_extra !== 0
        || verification.strategy_rows !== R.rows || verification.root_safe !== true || verification.root_mobility !== R.moves
        || verification.terminal_range[0] !== 13 || verification.terminal_range[1] !== 17) throw new Error('BigInt gates ' + R.name);
    const bareiss = spawnSync(process.execPath, ['--experimental-strip-types', BAREISS, '--cert', certPath, '--root', R.root, '--root-check', '--subroots', moves, '--consumed-out', consumedPath], { encoding: 'utf8', maxBuffer: 32 * 1024 * 1024 });
    if (bareiss.status !== 0) throw new Error('Bareiss verifier failed ' + R.name + ': ' + bareiss.stderr);
    const bl = bareiss.stdout.trim().split(/\r?\n/);
    if (bl.length !== 2) throw new Error('bareiss line count ' + R.name);
    const rootCheck = JSON.parse(bl[0]), stats = JSON.parse(bl[1]);
    const st = Object.values(stats.stats);
    if (rootCheck.stones !== 7 || rootCheck.loserMobility !== R.moves || stats.rows !== R.rows || st.length !== R.moves) throw new Error('Bareiss gates ' + R.name);
    const totals = { seen: st.reduce((s, x) => s + x.seen, 0), terminals: st.reduce((s, x) => s + x.terminals, 0), opponent_edges: st.reduce((s, x) => s + x.opponentEdges, 0), terminal_min: Math.min(...st.map(x => x.range[0])), terminal_max: Math.max(...st.map(x => x.range[1])) };
    if (totals.seen !== verification.visited_states_across_subroots || totals.terminals !== verification.terminal_count
        || totals.opponent_edges !== verification.loser_reply_edges
        || totals.terminal_min !== verification.terminal_range[0] || totals.terminal_max !== verification.terminal_range[1]) throw new Error('cross-verifier aggregate disagreement ' + R.name);
    const certRows = new Set(cert.toString('utf8').trimEnd().split(/\r?\n/).slice(2).map(l => l.split(' ')[0]));
    const consumed = fs.readFileSync(consumedPath, 'utf8').trim().split(/\r?\n/).filter(Boolean);
    const consumedUnique = new Set(consumed);
    const missing = [...certRows].filter(x => !consumedUnique.has(x)).length;
    const extra = [...consumedUnique].filter(x => !certRows.has(x)).length;
    if (certRows.size !== R.rows || missing !== 0 || extra !== 0 || consumedUnique.size !== R.rows) throw new Error('union audit ' + R.name);
    const unionAudit = { certificate_rows: certRows.size, consumed_records: consumed.length, consumed_unique: consumedUnique.size, missing, extra, exact_union: true };
    fs.writeFileSync(verificationPath, JSON.stringify(verification, null, 2) + '\n');
    fs.writeFileSync(bareissPath, bl.join('\n') + '\n');
    fs.writeFileSync(unionPath, JSON.stringify(unionAudit, null, 2) + '\n');
    console.log(JSON.stringify({ root: R.root, name: R.name, status: 'dual-independent-verification-pass', certificate_sha256: certSha, bigint: { subroots: verification.subroots_passed, union_missing: verification.union_missing, union_extra: verification.union_extra, terminals: verification.terminal_count, visited: verification.visited_states_across_subroots, loser_reply_edges: verification.loser_reply_edges }, bareiss: { subroots: st.length, ...totals }, unionAudit }));
  } finally {
    fs.rmSync(tempDir, { recursive: true, force: true });
  }
}
