// Generic WIN7-D10 certificate extraction driver for a residual 5-parent cover root.
// Usage: node extract_resid_win7_root_20261119.mjs <root_hex> [date=20261119]
// Mirrors scripts/extract_first_win7_root_20261119.mjs from
// experiments/n11-head1410-residual-cover-after-receipt-fold-20261119 (same gates,
// parameterized root and added bit). Added bit = highest set bit of the root; the
// engine verdict and extracted strategy are independent of that choice because the
// root position set is unchanged (verified on the published root: bits 23/49/65/71
// all reproduce loss=true, nodes=392235, terminal [13,17]).
import { extractBatch } from '../../n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_cert_extractor_exact_v16.ts';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(SCRIPT_DIR, '../../../..');
const OUT = path.resolve(SCRIPT_DIR, '../output');
const EXTRACTOR = path.resolve(SCRIPT_DIR, '../../n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_cert_extractor_exact_v16.ts');
const gitBlobSha = b => createHash('sha1').update(Buffer.concat([Buffer.from('blob ' + b.length), Buffer.from([0]), b])).digest('hex');
const DATE = process.argv[3] || '20261119';
const rootHex = (process.argv[2] || '').toLowerCase();
if (!/^[0-9a-f]{32}$/.test(rootHex)) throw new Error('usage: extract_resid_win7_root_20261119.mjs <root_hex> [date]');
const expected = {
  cover: 'a8eaf00bd6494eda50a68e7d06498bed833a7688',
  mobility: 'b35d54a0ced182153802247452a593096a0acf81',
  extractor: '5518d375fc6b4a7a14c22a1a65586f0c1c5731c0'
};
const coverBytes = fs.readFileSync(path.join(ROOT, 'research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/five-parent-residual-49-cover-20261119.json'));
const mobilityBytes = fs.readFileSync(path.join(ROOT, 'research/experiments/n11-class2-lane-closability-ranking-20261116/output/49-root-cache-exclusion-mobility-20261119.json').replace('/research/experiments/n11-class2-lane-closability-ranking-20261116/', '/research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/'));
const extractorBytes = fs.readFileSync(EXTRACTOR);
for (const [k, b] of Object.entries({cover: coverBytes, mobility: mobilityBytes, extractor: extractorBytes})) {
  if (gitBlobSha(b) !== expected[k]) throw new Error('pinned blob mismatch: ' + k);
}
const cover = JSON.parse(coverBytes.toString('utf8'));
const mobility = JSON.parse(mobilityBytes.toString('utf8'));
const item = mobility.mobility.priority_order.find(x => x.root === rootHex);
const witness = cover.witness.find(x => x.root === rootHex);
if (!item || !witness) throw new Error('pinned root missing from source data');
const mask = BigInt('0x' + rootHex);
let bit = -1;
for (let b = 120; b >= 0; b--) if ((mask >> BigInt(b)) & 1n) { bit = b; break; }
if (bit < 0) throw new Error('empty root');
const child = (mask ^ (1n << BigInt(bit))).toString(16).padStart(32, '0');
const moves = item.legal_bits;
if (moves.length !== item.legal_next_moves) throw new Error('legal-move count mismatch');
const coveredRows = witness.rows;

const progressPath = path.join(OUT, 'resid-win7-root-' + rootHex + '-extraction-progress-' + DATE + '.jsonl');
const certPath = path.join(OUT, 'win7-root-' + rootHex + '-' + DATE + '.n11');
const summaryPath = path.join(OUT, 'resid-win7-root-' + rootHex + '-extraction-summary-' + DATE + '.json');
fs.writeFileSync(progressPath, '');
const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'n11-resid-extract-'));
const rowsPath = path.join(tempDir, 'strategy.rows');
fs.writeFileSync(rowsPath, '');
const seen = new Set();
const completed = [];
let totalNodes = 0, minTerm = 121, maxTerm = 0, failure = null;
try {
  for (const move of moves) {
    const t0 = Date.now();
    const r = extractBatch(child, bit, {}, [move]);
    const p = r.perMove?.[String(move)];
    if (r.fatal || !r.rows || !p || !p.ok || p.capped || (r.fbt_drops ?? 0) !== 0) {
      failure = {move, fatal: r.fatal ?? null, perMove: p ?? null, fbt_drops: r.fbt_drops ?? null};
      fs.appendFileSync(progressPath, JSON.stringify({move, status: 'FAIL', ...failure}) + '\n');
      break;
    }
    const fresh = [];
    for (const line of r.rows) if (!seen.has(line)) { seen.add(line); fresh.push(line); }
    if (fresh.length) fs.appendFileSync(rowsPath, fresh.join('\n') + '\n');
    totalNodes += p.nodes;
    if (p.terminalRange) { minTerm = Math.min(minTerm, p.terminalRange[0]); maxTerm = Math.max(maxTerm, p.terminalRange[1]); }
    completed.push(move);
    fs.appendFileSync(progressPath, JSON.stringify({move, status: 'OK', nodes: p.nodes, new_rows: fresh.length, total_rows: seen.size, ms: Date.now() - t0, terminal_range: p.terminalRange, fbt_drops: r.fbt_drops}) + '\n');
  }
  let status = 'INCOMPLETE';
  let certificateSha256 = null;
  if (!failure && completed.length === moves.length) {
    const sorted = [...seen].sort((a, b) => a < b ? -1 : a > b ? 1 : 0);
    const cert = ['n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS', 'root ' + rootHex, ...sorted].join('\n') + '\n';
    fs.writeFileSync(certPath, cert);
    certificateSha256 = createHash('sha256').update(cert).digest('hex');
    status = 'EXTRACTED_UNVERIFIED';
  }
  const summary = {schema: 'n11-win7-d10-certificate-extraction-v1', source_main: 'c8e974a26629a8b91662f479e1d84e10cae6ddcd', root: rootHex, child, added_bit: bit, added_bit_rule: 'highest set bit; verdict and strategy independent of the choice (same 7-stone set)', covered_rows: coveredRows, legal_next_moves: moves.length, completed_moves: completed.length, completed_move_list: completed, total_nodes: totalNodes, unique_strategy_rows: seen.size, terminal_stone_range: completed.length ? [minTerm, maxTerm] : null, fbt_drops: failure?.fbt_drops ?? 0, failure, status, certificate_path: 'research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/win7-root-' + rootHex + '-' + DATE + '.n11', certificate_sha256: certificateSha256};
  fs.writeFileSync(summaryPath, JSON.stringify(summary, null, 2) + '\n');
  console.log(JSON.stringify({status, root: rootHex, added_bit: bit, child, rows: seen.size, total_nodes: totalNodes, certificate_sha256: certificateSha256}));
  if (status !== 'EXTRACTED_UNVERIFIED') process.exitCode = 1;
} finally {
  fs.rmSync(tempDir, {recursive: true, force: true});
}
