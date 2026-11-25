// Resumable WIN7-D10 strategy-certificate extraction driver for the witness WIN roots
// (2026-11-19, recovery epoch after environment loss; logic identical to the epoch-1 driver:
//  ascending legal first-mover moves, one blind extractBatch call per move, killTable empty).
// Usage: node --experimental-strip-types extract_root_rec_20261119.mjs <rootHex> <outDir>
import { extractBatch } from './scripts/class4_child1_cert_extractor_exact_v16.ts';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const BASE = path.dirname(fileURLToPath(import.meta.url));
const SOURCE_MAIN = 'cc8be6d6dc1df9ef87dd10aae4b9103035e82754';
const rootHex = process.argv[2];
const outDir = process.argv[3];
if (!rootHex || !outDir) throw new Error('usage: extract_root_rec_20261119.mjs <rootHex> <outDir>');
fs.mkdirSync(outDir, { recursive: true });
const legalMap = JSON.parse(fs.readFileSync(path.join(BASE, 'win_legal_gen.json'), 'utf8'));
const legal = legalMap[rootHex]?.legal;
if (!legal || legal.length !== legalMap[rootHex].expected_count) throw new Error('no legal list for ' + rootHex);
const X = i => i % 11, Y = i => (i / 11) | 0;
function rootCells(h) { const v = BigInt('0x' + h); const out = []; for (let i = 0; i < 121; i++) if ((v >> BigInt(i)) & 1n) out.push(i); return out; }
// survival legality recheck inside the driver (independent of the generator)
{
  const cells = rootCells(rootHex);
  const css = new Set(cells), blocked = new Set(cells);
  for (let i = 0; i < cells.length; i++) for (let j = i + 1; j < cells.length; j++) for (let k = j + 1; k < cells.length; k++) {
    const a = cells[i], b = cells[j], c = cells[k];
    const qa = X(a)*X(a)+Y(a)*Y(a), qb2 = X(b)*X(b)+Y(b)*Y(b)-qa, qbx = X(b)-X(a), qby = Y(b)-Y(a);
    const qc2 = X(c)*X(c)+Y(c)*Y(c)-qa, qcx = X(c)-X(a), qcy = Y(c)-Y(a);
    for (let d = 0; d < 121; d++) {
      if (d === a || d === b || d === c) continue;
      const qd2 = X(d)*X(d)+Y(d)*Y(d)-qa, qdx = X(d)-X(a), qdy = Y(d)-Y(a);
      const det = qb2*(qcx*qdy-qcy*qdx) - qbx*(qc2*qdy-qcy*qd2) + qby*(qc2*qdx-qcx*qd2);
      if (det === 0) blocked.add(d);
    }
  }
  const lm = [];
  for (let d = 0; d < 121; d++) if (!blocked.has(d)) lm.push(d);
  if (JSON.stringify(lm) !== JSON.stringify(legal)) throw new Error('legal list disagreement: ' + lm.length + ' vs ' + legal.length);
}
const cells = rootCells(rootHex);
const bit = Math.max(...cells);
const mask = BigInt('0x' + rootHex);
if (((mask >> BigInt(bit)) & 1n) !== 1n) throw new Error('bit not set');
const child = (mask ^ (1n << BigInt(bit))).toString(16).padStart(32, '0');
const moves = legal;
const rowsPath = path.join(outDir, `rows-${rootHex}.txt`);
const progressPath = path.join(outDir, `win7-root-${rootHex}-extraction-progress-20261119.jsonl`);
const certPath = path.join(outDir, `win7-root-${rootHex}-20261119.n11`);
const summaryPath = path.join(outDir, `win7-root-${rootHex}-extraction-summary-20261119.json`);
const seen = new Set();
if (fs.existsSync(rowsPath)) for (const l of fs.readFileSync(rowsPath, 'utf8').split(/\r?\n/)) if (l.trim()) seen.add(l.trim());
const doneMoves = new Set();
if (fs.existsSync(progressPath)) for (const l of fs.readFileSync(progressPath, 'utf8').split(/\r?\n/)) {
  if (!l.trim()) continue;
  try { const p = JSON.parse(l); if (p.status === 'OK') doneMoves.add(p.move); } catch {}
}
let total = 0, minTerm = 121, maxTerm = 0, failure = null;
const completed = [];
try {
  for (const move of moves) {
    if (doneMoves.has(move)) { completed.push(move); continue; }
    const t0 = Date.now();
    const r = extractBatch(child, bit, {}, [move]);
    const p = r.perMove?.[String(move)];
    if (r.fatal || !r.rows || !p || !p.ok || p.capped || (r.fbt_drops ?? 0) !== 0) {
      failure = { move, fatal: r.fatal ?? null, perMove: p ?? null, fbt_drops: r.fbt_drops ?? null };
      fs.appendFileSync(progressPath, JSON.stringify({ move, status: 'FAIL', ...failure }) + '\n');
      break;
    }
    const fresh = [];
    for (const line of r.rows) if (!seen.has(line)) { seen.add(line); fresh.push(line); }
    if (fresh.length) fs.appendFileSync(rowsPath, fresh.join('\n') + '\n');
    total += p.nodes;
    if (p.terminalRange) { minTerm = Math.min(minTerm, p.terminalRange[0]); maxTerm = Math.max(maxTerm, p.terminalRange[1]); }
    completed.push(move);
    fs.appendFileSync(progressPath, JSON.stringify({ move, status: 'OK', nodes: p.nodes, new_rows: fresh.length, total_rows: seen.size, ms: Date.now() - t0, terminal_range: p.terminalRange, fbt_drops: r.fbt_drops }) + '\n');
  }
  let status = 'INCOMPLETE', certificateSha256 = null;
  if (!failure && [...new Set(completed)].length === moves.length) {
    const sorted = [...seen].sort((a, b) => a < b ? -1 : a > b ? 1 : 0);
    const cert = ['n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS', 'root ' + rootHex, ...sorted].join('\n') + '\n';
    fs.writeFileSync(certPath, cert);
    certificateSha256 = createHash('sha256').update(cert).digest('hex');
    status = 'EXTRACTED_UNVERIFIED';
  }
  const summary = { schema: 'n11-win7-d10-certificate-extraction-v1', source_main: SOURCE_MAIN, root: rootHex, child, added_bit: bit, legal_next_moves: moves.length, completed_moves: [...new Set(completed)].length, completed_move_list: [...new Set(completed)].sort((a,b)=>a-b), total_nodes_this_process: total, unique_strategy_rows: seen.size, terminal_stone_range: completed.length ? [minTerm, maxTerm] : null, fbt_drops: failure?.fbt_drops ?? 0, failure, status, certificate_sha256: certificateSha256 };
  fs.writeFileSync(summaryPath, JSON.stringify(summary, null, 2) + '\n');
  console.log(JSON.stringify(summary));
  if (status !== 'EXTRACTED_UNVERIFIED') process.exitCode = 1;
} catch (e) {
  console.error('EXTRACT_ERROR', e.message);
  process.exitCode = 2;
}
