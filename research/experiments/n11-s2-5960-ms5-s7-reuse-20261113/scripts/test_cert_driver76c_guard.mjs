import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const driverSource = fs.readFileSync(path.join(here, 'cert_driver76c.ts'), 'utf8');
const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'n11-cost76c-driver-guard-'));
const driverPath = path.join(temp, 'cert_driver76c.ts');
const mockPath = path.join(temp, 'class4_child1_cert_extractor_exact_v16.ts');
const child = '00000000010000809002000001000000';
const valid61 = [0,1,2,4,6,7,9,10,14,15,18,21,26,28,29,30,32,34,36,41,43,45,46,48,54,66,67,69,70,76,77,78,81,85,86,87,89,91,94,95,98,99,103,106,108,109,110,111,113,114,116,117,118,119,120];
const valid99 = [2,4,6,7,9,10,14,15,17,18,19,20,21,26,28,29,30,32,34,36,41,43,45,46,47,53,54,56,59,61,62,64,65,66,68,69,70,76,77,78,81,85,86,87,89,91,94,95,96,98,102,103,105,106,107,110,111,112,113,114,116,117,118,119,120];

const mock = [
  "import fs from 'node:fs';",
  "export function extractBatch(child, bit, killTable, moves) {",
  "  if (process.env.CALLED_MARKER) fs.writeFileSync(process.env.CALLED_MARKER, moves.join(','));",
  "  const mode = process.env.MOCK_MODE;",
  "  const perMove = Object.fromEntries(moves.map(m => [m, {",
  "    ok: true, capped: false, nodes: 1, terminalRange: [13, 17]",
  "  }]));",
  "  const base = {",
  "    perMove, sum: moves.length, nRows: 1,",
  "    rows: ['00000000000000000000000000000000 1'],",
  "    fbt_drops: 0, fatal: undefined",
  "  };",
  "  if (mode === 'fatal') return { ...base, fatal: 'fbt_saturation', fbt_drops: 1 };",
  "  if (mode === 'drops') return { ...base, fbt_drops: 1 };",
  "  if (mode === 'missing') return { ...base, rows: undefined };",
  "  if (mode === 'bad-per-move') return { ...base, perMove: { ...perMove, 1: { ok: false, capped: false } } };",
  "  if (mode === 'bad-row') return { ...base, rows: ['not-a-certificate-row'] };",
  "  if (mode === 'duplicate-board') return { ...base, nRows: 2, rows: [",
  "    '00000000000000000000000000000000 1',",
  "    '00000000000000000000000000000000 2'",
  "  ] };",
  "  return base;",
  "}",
].join('\n') + '\n';

function runCase(c) {
  const outPath = path.join(temp, c.mode + '.cert');
  const marker = path.join(temp, c.mode + '.called');
  const run = spawnSync(process.execPath, [
    '--experimental-strip-types', driverPath, child, String(c.bit ?? 61), outPath
  ], {
    input: 'ignored header\n' + c.moves.join(',') + '\n',
    encoding: 'utf8',
    env: { ...process.env, MOCK_MODE: c.mode, CALLED_MARKER: marker }
  });
  if (run.error) throw run.error;
  const exists = fs.existsSync(outPath);
  const called = fs.existsSync(marker);
  if (run.status !== c.expectedStatus || exists !== c.expectedFile || called !== c.expectedCalled) {
    throw new Error(c.mode + ': status=' + run.status + ', file=' + exists +
      ', called=' + called + ', stderr=' + run.stderr);
  }
  if (exists) {
    const root = (BigInt('0x' + child) | (1n << BigInt(c.bit ?? 61))).toString(16).padStart(32, '0');
    const lines = fs.readFileSync(outPath, 'utf8').trimEnd().split('\n');
    if (!lines[0].startsWith('n11-terminal-strategy-v1 ') ||
        lines[1] !== 'root ' + root ||
        lines[2] !== '00000000000000000000000000000000 1') {
      throw new Error('success output has an invalid certificate header, root, or row');
    }
  }
  return {
    mode: c.mode, bit: c.bit ?? 61, status: run.status,
    output_created: exists, extractor_called: called, pass: true
  };
}

try {
  fs.writeFileSync(driverPath, driverSource);
  fs.writeFileSync(mockPath, mock);
  const cases = [
    { mode: 'ok-bit61', bit: 61, moves: valid61, expectedStatus: 0, expectedFile: true, expectedCalled: true },
    { mode: 'ok-bit99', bit: 99, moves: valid99, expectedStatus: 0, expectedFile: true, expectedCalled: true },
    { mode: 'missing-defense', bit: 61, moves: valid61.slice(0, -1), expectedStatus: 1, expectedFile: false, expectedCalled: false },
    { mode: 'illegal-defense', bit: 61, moves: [3, ...valid61.slice(1)], expectedStatus: 1, expectedFile: false, expectedCalled: false },
    { mode: 'duplicate-defense', bit: 61, moves: [...valid61.slice(0, -1), 0], expectedStatus: 1, expectedFile: false, expectedCalled: false },
    { mode: 'unsorted-defense', bit: 61, moves: [valid61[1], valid61[0], ...valid61.slice(2)], expectedStatus: 1, expectedFile: false, expectedCalled: false },
    { mode: 'missing-bit99', bit: 99, moves: valid99.slice(0, -1), expectedStatus: 1, expectedFile: false, expectedCalled: false },
    { mode: 'fatal', bit: 61, moves: valid61, expectedStatus: 1, expectedFile: false, expectedCalled: true },
    { mode: 'drops', bit: 61, moves: valid61, expectedStatus: 1, expectedFile: false, expectedCalled: true },
    { mode: 'missing', bit: 61, moves: valid61, expectedStatus: 1, expectedFile: false, expectedCalled: true },
    { mode: 'bad-per-move', bit: 61, moves: valid61, expectedStatus: 1, expectedFile: false, expectedCalled: true },
    { mode: 'bad-row', bit: 61, moves: valid61, expectedStatus: 1, expectedFile: false, expectedCalled: true },
    { mode: 'duplicate-board', bit: 61, moves: valid61, expectedStatus: 1, expectedFile: false, expectedCalled: true },
    { mode: 'occupied-bit', bit: 60, moves: valid61, expectedStatus: 2, expectedFile: false, expectedCalled: false }
  ];
  const results = cases.map(runCase);
  process.stdout.write(JSON.stringify({
    schema: 'n11-cost76c-driver-guard-mock-test-v2',
    cases: results,
    all_pass: true,
    actual_extractor_invoked: false
  }, null, 2) + '\n');
} finally {
  fs.rmSync(temp, { recursive: true, force: true });
}
