// crosscheck_catalog_n7.mjs — census.mjs (line/circle machinery) quartet catalog vs
// forbidgen.py det/brute-force text, n=3..7. Canonical numeric-order comparison of
// the forbidgen-formatted text (n=<n> header + sorted "a b c d" rows), matching the
// published quartets_nN.txt format exactly.
import { census, quartetList } from './census.mjs';
import * as fs from 'node:fs';
import { createHash } from 'node:crypto';
let allOk = true;
for (const n of [3,4,5,6,7]) {
  const cen = census(n);
  const flat = quartetList(cen);
  const F = flat.length / 4;
  const rows = [];
  for (let q = 0; q < F; q++) {
    const a = [flat[4*q], flat[4*q+1], flat[4*q+2], flat[4*q+3]].sort((x,y)=>x-y);
    rows.push(a.join(' '));
  }
  if (cen.F !== undefined && cen.F !== F) { console.error(`cen.F=${cen.F} != flat/4=${F}`); allOk = false; }
  rows.sort((u,v)=>{const A=u.split(' ').map(Number),B=v.split(' ').map(Number);for(let i=0;i<4;i++){if(A[i]!==B[i])return A[i]-B[i];}return 0;});
  const text = `n=${n}\n` + rows.join('\n') + '\n';
  const py = fs.readFileSync(`/home/user/knowledge/kyouen-research/_n7-hist-kit/outputs/quartets_n${n}.txt`, 'utf8');
  const shaPy = createHash('sha256').update(py).digest('hex');
  const identical = py === text;
  console.log(JSON.stringify({ n, F, D: cen.D, C: cen.C, shaForbidgenText: shaPy, identical: identical && cen.F === F }));
  if (!identical || cen.F !== F) allOk = false;
}
console.log(JSON.stringify({ allOk }));
