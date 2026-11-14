import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const runnerPath = fileURLToPath(new URL('./class4_child1_runner_v16.ts', import.meta.url));
const childHex = '00000000020000003800000280000000';
const run = spawnSync(process.execPath, [
  '--experimental-strip-types',
  runnerPath,
  '--bits', '15',
  '--depth', '8',
  '--cap', '200000',
  '--andclose', '1',
  '--child', childHex
], { encoding: 'utf8', maxBuffer: 1024 * 1024 });

assert.equal(run.status, 0, run.stderr || 'runner exited unsuccessfully');
const rows = run.stdout.trim().split(/\r?\n/).map(line => JSON.parse(line));
assert.equal(rows.length, 2);
assert.deepEqual(rows[0], { control: 'pilot_d6', loss: false, nodes: 3402, capped: false });
assert.equal(rows[1].bit, 15);
assert.equal(rows[1].loss, false);
assert.equal(rows[1].nodes, 56791);
assert.equal(rows[1].capped, false);
assert.deepEqual(rows[1].terminalStoneRange, [13, 15]);
assert.equal(rows[1].andclose, true);

process.stdout.write(JSON.stringify({
  status: 'PASS',
  pilot_nodes: rows[0].nodes,
  regression: { bit: rows[1].bit, nodes: rows[1].nodes, terminalStoneRange: rows[1].terminalStoneRange }
}) + '\n');
