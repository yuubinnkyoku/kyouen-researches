import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const runnerPath = fileURLToPath(new URL('./class4_child1_runner_v16.ts', import.meta.url));
function run(args) {
  const result = spawnSync(process.execPath, [
    '--experimental-strip-types',
    runnerPath,
    ...args
  ], { encoding: 'utf8', maxBuffer: 1024 * 1024 });
  assert.equal(result.status, 0, result.stderr || 'runner exited unsuccessfully');
  return result.stdout.trim().split(/\r?\n/).map(line => JSON.parse(line));
}

// M0 sign-bit case: v15 had no memo hits for this root.
const class4 = run([
  '--bits', '15',
  '--depth', '8',
  '--cap', '200000',
  '--andclose', '1',
  '--child', '00000000020000003800000280000000'
]);
assert.equal(class4.length, 2);
assert.deepEqual(class4[0], { control: 'pilot_d6', loss: false, nodes: 3402, capped: false });
assert.equal(class4[1].bit, 15);
assert.equal(class4[1].loss, false);
assert.equal(class4[1].nodes, 56791);
assert.equal(class4[1].capped, false);
assert.deepEqual(class4[1].terminalStoneRange, [13, 15]);
assert.equal(class4[1].andclose, true);

// M1 sign-bit case: v15 hits the 200,000-node cap; v16 closes this depth-8 run.
const class2 = run([
  '--bits', '0',
  '--depth', '8',
  '--cap', '200000',
  '--andclose', '1',
  '--child', '00000000000000809102000001000000',
  '--nocontrol'
]);
assert.equal(class2.length, 1);
assert.equal(class2[0].bit, 0);
assert.equal(class2[0].loss, false);
assert.equal(class2[0].nodes, 121837);
assert.equal(class2[0].capped, false);
assert.deepEqual(class2[0].terminalStoneRange, [13, 15]);
assert.equal(class2[0].andclose, true);

process.stdout.write(JSON.stringify({
  status: 'PASS',
  class4_m0: { pilot_nodes: class4[0].nodes, nodes: class4[1].nodes, terminalStoneRange: class4[1].terminalStoneRange },
  class2_m1: { nodes: class2[0].nodes, terminalStoneRange: class2[0].terminalStoneRange }
}) + '\n');
