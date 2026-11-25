import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { extractBatch } from './class4_child1_cert_extractor_exact_v16.ts';

// Golden replay of the already independently verified bit-7 WIN7 certificate.
// The root includes cell 31, so M0 has its signed Int32 high bit set.
const KILL_BIT7 = {0:114,8:21,10:81,15:40,18:40,21:40,28:80,32:81,33:18,34:83,38:70,40:18,44:81,45:28,50:18,54:8,66:18,67:80,70:38,72:88,75:50,76:40,78:70,80:28,81:32,82:50,83:8,84:40,86:72,87:70,88:72,90:8,91:8,92:50,93:8,94:28,102:90,104:40,105:18,106:81,108:18,109:70,110:8,112:82,113:81,114:38,116:8,117:8,118:18,120:28};
const moves = Object.keys(KILL_BIT7).map(Number);
assert.equal(moves.length, 50, 'all legal opponent replies must be represented');
assert.deepEqual(moves, moves.slice().sort((a, b) => a - b));

const result = extractBatch(
  '00000000020000003800000080080000',
  7,
  KILL_BIT7,
  moves
);
assert.equal(result.fatal, undefined);
assert.equal(result.fbt_drops, 0);
assert.equal(result.nRows, 30947);
assert.equal(result.rows.length, 30947);
assert.equal(Object.keys(result.perMove).length, 50);
assert.ok(Object.values(result.perMove).every(x => x.ok && !x.capped));

const terminals = Object.values(result.perMove).flatMap(x => x.terminalRange);
assert.deepEqual([Math.min(...terminals), Math.max(...terminals)], [13, 17]);

const certificate = [
  'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS',
  'root 00000000020000003800000080080080',
  ...result.rows.slice().sort()
].join(String.fromCharCode(10)) + String.fromCharCode(10);
const md5 = createHash('md5').update(certificate).digest('hex');
assert.equal(md5, '0f1fedfe06c658acdd02577f9d7da9d2');

process.stdout.write(JSON.stringify({
  status: 'PASS',
  root: '00000000020000003800000080080080',
  subRoots: moves.length,
  rows: result.nRows,
  fbtDrops: result.fbt_drops,
  terminalStoneRange: [13, 17],
  md5
}) + String.fromCharCode(10));
