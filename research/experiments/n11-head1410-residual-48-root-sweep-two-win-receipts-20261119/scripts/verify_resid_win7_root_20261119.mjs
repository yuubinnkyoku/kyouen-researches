// Generic dual-independent-verification driver (BigInt 3x3 cofactor exact-lift plus
// Bareiss 4x4 integer elimination) for a WIN7-D10 certificate extracted by
// extract_resid_win7_root_20261119.mjs. Gates are sized from the pinned extraction
// summary instead of being hardcoded, mirroring
// verify_first_win7_root_20261119.mjs.
// Usage: node verify_resid_win7_root_20261119.mjs <root_hex> [date=20261119]
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(SCRIPT_DIR, '../../../..');
const OUT = path.resolve(SCRIPT_DIR, '../output');
const VERIFY_DIR = path.resolve(SCRIPT_DIR, '../../n11-s2-5960-ms5-s7-reuse-20261113/scripts');
const BIGINT = path.join(VERIFY_DIR, 'verify_win7_certificate_bigint_independent.mjs');
const BAREISS = path.join(VERIFY_DIR, 'verify_bit7_win7_cert.ts');
const DATE = process.argv[3] || '20261119';
const root = (process.argv[2] || '').toLowerCase();
if (!/^[0-9a-f]{32}$/.test(root)) throw new Error('usage: verify_resid_win7_root_20261119.mjs <root_hex> [date]');
const certPath = path.join(OUT, 'win7-root-' + root + '-' + DATE + '.n11');
const summaryPath = path.join(OUT, 'resid-win7-root-' + root + '-extraction-summary-' + DATE + '.json');
const verificationPath = path.join(OUT, 'resid-win7-root-' + root + '-independent-verification-' + DATE + '.json');
const bareissPath = path.join(OUT, 'resid-win7-root-' + root + '-bareiss-subroots-' + DATE + '.jsonl');
const unionPath = path.join(OUT, 'resid-win7-root-' + root + '-bareiss-union-audit-' + DATE + '.json');
const summary = JSON.parse(fs.readFileSync(summaryPath, 'utf8'));
const cert = fs.readFileSync(certPath);
const certSha256 = createHash('sha256').update(cert).digest('hex');
if (summary.root !== root || summary.status !== 'EXTRACTED_UNVERIFIED' || summary.certificate_sha256 !== certSha256) throw new Error('extraction summary/certificate mismatch');
const nMoves = summary.legal_next_moves;
const moves = summary.completed_move_list;
if (moves.length !== nMoves) throw new Error('incomplete extraction');
const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'n11-resid-verify-'));
const consumedPath = path.join(tempDir, 'consumed.txt');
fs.writeFileSync(consumedPath, '');
try {
  const big = spawnSync(process.execPath, [BIGINT, certPath, String(nMoves)], {encoding: 'utf8', maxBuffer: 32 * 1024 * 1024});
  if (big.status !== 0) throw new Error('BigInt verifier failed: ' + big.stderr);
  const verification = JSON.parse(big.stdout.trim());
  if (verification.verdict !== 'WIN7 certificate independently verified' || verification.root_hex !== root ||
      verification.subroots_passed !== nMoves || verification.union_missing !== 0 || verification.union_extra !== 0 ||
      verification.root_safe !== true || verification.root_mobility !== nMoves ||
      verification.strategy_rows !== summary.unique_strategy_rows || verification.consumed_winner_rows !== summary.unique_strategy_rows)
    throw new Error('BigInt verifier result gate failed');
  if (verification.terminal_range[0] !== summary.terminal_stone_range[0] || verification.terminal_range[1] !== summary.terminal_stone_range[1])
    throw new Error('terminal range disagreement between extraction and BigInt verifier');
  const bareiss = spawnSync(process.execPath, ['--experimental-strip-types', BAREISS, '--cert', certPath, '--root', root, '--root-check', '--subroots', moves.join(','), '--consumed-out', consumedPath], {encoding: 'utf8', maxBuffer: 32 * 1024 * 1024});
  if (bareiss.status !== 0) throw new Error('Bareiss verifier failed: ' + bareiss.stderr);
  const bareissLines = bareiss.stdout.trim().split(/\r?\n/);
  if (bareissLines.length !== 2) throw new Error('unexpected Bareiss output line count');
  const rootCheck = JSON.parse(bareissLines[0]);
  const stats = JSON.parse(bareissLines[1]);
  if (rootCheck.stones !== 7 || rootCheck.loserMobility !== nMoves || stats.rows !== summary.unique_strategy_rows || Object.keys(stats.stats).length !== nMoves)
    throw new Error('Bareiss root/subroot gate failed');
  const certRows = new Set(cert.toString('utf8').trimEnd().split(/\r?\n/).slice(2).map(line => line.split(' ')[0]));
  if (certRows.size !== summary.unique_strategy_rows) throw new Error('certificate row count mismatch');
  const consumed = fs.readFileSync(consumedPath, 'utf8').trim().split(/\r?\n/).filter(Boolean);
  const consumedUnique = new Set(consumed);
  const missing = [...certRows].filter(x => !consumedUnique.has(x));
  const extra = [...consumedUnique].filter(x => !certRows.has(x));
  const unionAudit = {certificate_rows: certRows.size, certificate_unique: certRows.size, consumed_records: consumed.length, consumed_unique: consumedUnique.size, missing: missing.length, extra: extra.length, exact_union: missing.length === 0 && extra.length === 0};
  if (!unionAudit.exact_union || certRows.size !== summary.unique_strategy_rows || consumedUnique.size !== certRows.size)
    throw new Error('Bareiss consumed-union gate failed');
  const bareissStats = Object.values(stats.stats);
  const totals = {seen: bareissStats.reduce((s, x) => s + x.seen, 0), terminals: bareissStats.reduce((s, x) => s + x.terminals, 0), opponent_edges: bareissStats.reduce((s, x) => s + x.opponentEdges, 0), terminal_min: Math.min(...bareissStats.map(x => x.range[0])), terminal_max: Math.max(...bareissStats.map(x => x.range[1]))};
  if (totals.terminal_min !== summary.terminal_stone_range[0] || totals.terminal_max !== summary.terminal_stone_range[1])
    throw new Error('Bareiss terminal range disagreement');
  const visitedMatch = verification.visited_states_across_subroots === totals.seen && verification.terminal_count === totals.terminals && verification.loser_reply_edges === totals.opponent_edges;
  fs.writeFileSync(verificationPath, JSON.stringify(verification, null, 2) + '\n');
  fs.writeFileSync(bareissPath, bareissLines.join('\n') + '\n');
  fs.writeFileSync(unionPath, JSON.stringify(unionAudit, null, 2) + '\n');
  console.log(JSON.stringify({status: 'dual-independent-verification-pass', root, certificate_sha256: certSha256, bigint: {subroots: verification.subroots_passed, union_missing: verification.union_missing, union_extra: verification.union_extra}, bareiss: {subroots: Object.keys(stats.stats).length, ...totals}, cross_method_state_flow_agreement: visitedMatch, unionAudit}, null, 2));
} finally {
  fs.rmSync(tempDir, {recursive: true, force: true});
}
