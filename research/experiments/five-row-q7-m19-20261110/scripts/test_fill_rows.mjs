// Exercise the actual row-filling functions with each possible deficient row.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { runInNewContext } from 'node:vm';

const dir = dirname(fileURLToPath(import.meta.url));
const names = ['five_row_q7_blocker_dfs.ts', 'slice_runner_class0.ts', 'slice_runner_class1.ts'];

function functionsFrom(source) {
  const start = source.indexOf('  function fillRows(');
  const fillComb = source.indexOf('  function fillComb(', start);
  const end = source.indexOf('\n  function ', fillComb + 1);
  assert(start >= 0 && fillComb > start && end > fillComb);
  return stripTypeScriptTypes(source.slice(start, end));
}

function runFixture(functions, deficientRow, deficientCount, oneMissing) {
  const fixture = `
    const W=5, M=6, N=W*M, Y0=${deficientRow}, NODE_CAP=100;
    const ys=Array.from({length:N}, (_,p)=>Math.floor(p/M));
    const xs=Array.from({length:N}, (_,p)=>p%M);
    const forced=Array(N).fill(1), rowStone=Array(W).fill(6), rowPts=[];
    for (let y=0;y<W;y++) rowPts.push(Array.from({length:M},(_,x)=>y*M+x));
    rowStone[Y0]=${deficientCount};
    for (let x=${deficientCount};x<M;x++) forced[Y0*M+x]=2;
    const partial=(Y0+1)%W;
    if (${oneMissing}) { forced[partial*M+M-1]=0; rowStone[partial]--; }
    const trail=[]; let nodes=0, capped=false, witnesses=0; const witnessList=[];
    function forceStone(p) { if (forced[p]!==0) return false; trail.push(p); forced[p]=1; rowStone[ys[p]]++; return true; }
    function undoTo(mark) { while (trail.length>mark) { const p=trail.pop(); forced[p]=0; rowStone[ys[p]]--; } }
    ${functions}
    fillRows(0);
    ({witnesses, capped, witnessList});`;
  return runInNewContext(fixture);
}

for (const name of names) {
  const source = readFileSync(join(dir, name), 'utf8');
  assert.match(source, /leaves\+\+;\s*return fillRows\(0\)/);
  const functions = functionsFrom(source);
  for (let deficient = 0; deficient < 5; deficient++) {
    for (let count = 0; count <= 5; count++) {
      for (const oneMissing of [false, true]) {
        const result = runFixture(functions, deficient, count, oneMissing);
        assert.equal(result.witnesses, 1, `${name}: row ${deficient}, ${count} stones`);
        assert.equal(result.capped, false);
        assert.equal(result.witnessList[0][deficient].length, count);
        for (let row=0; row<5; row++) if (row !== deficient)
          assert.equal(result.witnessList[0][row].length, 6);
      }
    }
  }
  // The old code skipped row 0 only, then incorrectly required six stones in row 1.
  const oldFunctions = functions.replace(/if \(row === Y0\) return fillRows\(row \+ 1\);/, '');
  assert.equal(runFixture(oldFunctions, 1, 5, false).witnesses, 0);
}
console.log(`PASS: ${names.length * 5 * 6 * 2} row-filling cases; old class-1 behavior rejected`);
