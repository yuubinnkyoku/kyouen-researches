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

const mock = `export function extractBatch(child, bit, killTable, moves) {
  const mode = process.env.MOCK_MODE;
  const perMove = Object.fromEntries(moves.map(m => [m, {
    ok: true, capped: false, nodes: 1, terminalRange: [13, 17]
  }]));
  const base = {
    perMove, sum: moves.length, nRows: 1,
    rows: ['00000000000000000000000000000000 1'],
    fbt_drops: 0, fatal: undefined
  };
  if (mode === 'fatal') return { ...base, fatal: 'fbt_saturation', fbt_drops: 1 };
  if (mode === 'drops') return { ...base, fbt_drops: 1 };
  if (mode === 'missing') return { ...base, rows: undefined };
  if (mode === 'bad-per-move') return {
    ...base, perMove: { ...perMove, 1: { ok: false, capped: false } }
  };
  return base;
}
`;

try {
  fs.writeFileSync(driverPath, driverSource);
  fs.writeFileSync(mockPath, mock);
  const cases = [
    { mode: 'ok', bit: 61, expectedStatus: 0, expectedFile: true },
    { mode: 'fatal', bit: 61, expectedStatus: 1, expectedFile: false },
    { mode: 'drops', bit: 61, expectedStatus: 1, expectedFile: false },
    { mode: 'missing', bit: 61, expectedStatus: 1, expectedFile: false },
    { mode: 'bad-per-move', bit: 61, expectedStatus: 1, expectedFile: false },
    { mode: 'occupied-bit', bit: 60, expectedStatus: 2, expectedFile: false }
  ];
  const results = [];
  for (const c of cases) {
    const outPath = path.join(temp, c.mode + '.cert');
    const run = spawnSync(process.execPath, [
      '--experimental-strip-types', driverPath,
      '00000000010000809002000001000000', String(c.bit), outPath
    ], {
      input: 'ignored header\\n0,1,2\\n',
      encoding: 'utf8',
      env: { ...process.env, MOCK_MODE: c.mode }
    });
    const exists = fs.existsSync(outPath);
    if (run.error) throw run.error;
    if (run.status !== c.expectedStatus || exists !== c.expectedFile) {
      throw new Error(`${c.mode}: status=${run.status}, file=${exists}, stderr=${run.stderr}`);
    }
    if (exists) {
      const lines = fs.readFileSync(outPath, 'utf8').split('\\n');
      if (!lines[0].startsWith('n11-terminal-strategy-v1 ') ||
          !lines[1].startsWith('root ') || !lines[2].endsWith(' 1')) {
        throw new Error('success output has an invalid certificate header or row');
      }
    }
    results.push({ mode: c.mode, status: run.status, output_created: exists, pass: true });
  }
  process.stdout.write(JSON.stringify({
    schema: 'n11-cost76c-driver-guard-mock-test-v1',
    cases: results,
    all_pass: true,
    actual_extractor_invoked: false
  }, null, 2) + '\\n');
} finally {
  fs.rmSync(temp, { recursive: true, force: true });
}
