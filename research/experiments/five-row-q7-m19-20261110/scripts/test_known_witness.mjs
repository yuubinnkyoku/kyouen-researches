// Run the real class-0 search against the independently saved 5x18 witness.
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = dirname(fileURLToPath(import.meta.url));
const source = readFileSync(join(dir, 'five_row_q7_blocker_dfs.ts'), 'utf8');
assert.match(source, /const M = 19;/);
assert.match(source, /const MODE = 'campaign';/);
const runnable = source.replace('const M = 19;', 'const M = 18;')
  .replace("const MODE = 'campaign';", "const MODE = 'single';");
const witness = JSON.parse(readFileSync(resolve(dir,
  '../../fixed-width-frontier-20261005/output/q57_independent_witness.json'), 'utf8'))
  .lower_bound_witness.rows;
const tmp = mkdtempSync(join(tmpdir(), 'five-row-witness-'));
try {
  const file = join(tmp, 'search.ts');
  writeFileSync(file, runnable + '\nmain().then(result => console.log(JSON.stringify(result)));\n');
  const stdout = execFileSync(process.execPath, ['--disable-warning=ExperimentalWarning', file],
                              {encoding:'utf8', timeout:60000});
  const result = JSON.parse(stdout);
  assert.equal(result.nC, 84);
  assert(result.witnesses >= 1);
  assert(result.witnessList.some(rows => JSON.stringify(rows) === JSON.stringify(witness)));
  console.log('PASS: real 5x18 search reproduces the stored witness');
} finally {
  rmSync(tmp, {recursive:true, force:true});
}
