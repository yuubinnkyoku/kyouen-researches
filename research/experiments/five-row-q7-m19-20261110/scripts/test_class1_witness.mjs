// Reach an actual class-1 search leaf on a 5x8 board and check its witness.
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = dirname(fileURLToPath(import.meta.url));
const source = readFileSync(join(dir, 'slice_runner_class1.ts'), 'utf8');
assert.match(source, /const W = 5, M = 19;/);
assert.match(source, /const START = 79;/);
assert.match(source, /const NODE_CAP = 600_000;/);
const runnable = source.replace('const W = 5, M = 19;', 'const W = 5, M = 8;')
  .replace('const START = 79;', 'const START = 0;')
  .replace('const NODE_CAP = 600_000;', 'const NODE_CAP = 50_000;');
const tmp = mkdtempSync(join(tmpdir(), 'five-row-class1-'));
try {
  const file = join(tmp, 'search.ts');
  writeFileSync(file, runnable + '\nmain().then(result => console.log(JSON.stringify(result)));\n');
  const output = execFileSync(process.execPath, ['--disable-warning=ExperimentalWarning', file],
                              {encoding:'utf8', timeout:60000});
  const result = JSON.parse(output);
  assert(result.leaves > 0 && result.witnesses > 0);
  const candidate = {columns:8, deficient_row:1, rows:result.witnessList[0]};
  const checked = JSON.parse(execFileSync('python3', [join(dir, 'verify_five_row_witness.py')],
    {input:JSON.stringify(candidate), encoding:'utf8', timeout:60000}));
  assert.equal(checked.stones, 29);
  assert.equal(checked.blocked_empty_points, 11);
  const previous = runnable.replace('if (row === Y0) return fillRows(row + 1);', '');
  assert.notEqual(previous, runnable);
  writeFileSync(file, previous + '\nmain().then(result => console.log(JSON.stringify(result)));\n');
  const previousResult = JSON.parse(execFileSync(process.execPath,
    ['--disable-warning=ExperimentalWarning', file], {encoding:'utf8', timeout:60000}));
  assert(previousResult.leaves > 0);
  assert.equal(previousResult.witnesses, 0);
  console.log('PASS: real 5x8 class-1 search produces an independently verified witness');
} finally {
  rmSync(tmp, {recursive:true, force:true});
}
