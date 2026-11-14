const S = require('./sat.js');
const fs = require('fs');
function subsets(arr, cap) {
  const res = []; const n = arr.length;
  const rec = (i, cur, sz) => { if (i===n){res.push(cur.slice());return;} rec(i+1,cur,sz); if(sz<cap){cur.push(arr[i]);rec(i+1,cur,sz+1);cur.pop();} };
  rec(0,[],0); return res;
}
let pool = [];
for (const f of ['sa-frontier3-20261114','sa-frontier-extension-20261114','sa-row-deficient-witnesses-20261114']) {
  for (const line of fs.readFileSync('wits/'+f+'.jsonl','utf8').split('\n')) {
    if (!line.trim()) continue;
    const d = JSON.parse(line);
    const st = d.stones || d.witness; if (!st) continue;
    pool.push({w:d.w,q:d.q,m:d.m,st});
  }
}
const found = [];
for (const p of pool) {
  const capDef = p.w*(p.q-1)-1; const spare = capDef - p.st.length;
  if (spare < 0) continue;
  for (let dm = 1; dm <= 4; dm++) {
    const M = p.m + dm, cellsN = dm * p.w;
    if (cellsN > 12 || Math.pow(2,cellsN) > 5000) continue;
    for (let off = 0; off <= dm; off++) {
      const shifted = p.st.map(([x,y]) => [x+off, y]);
      const cells = [];
      for (let x = 0; x < M; x++) for (let y = 0; y < p.w; y++) if (!(x >= off && x < off + p.m)) cells.push([x,y]);
      for (const sub of subsets(cells, spare)) {
        const cand = shifted.concat(sub);
        const v = S.verifyConfig(p.w, M, p.q, cand);
        if (v.ok) found.push({w:p.w,q:p.q,fromM:p.m,toM:M,off,size:cand.length,stones:cand,rows:v.rows});
      }
    }
  }
}
const seen = new Set();
const uniq = found.filter(f => { const k=f.w+','+f.q+','+f.toM; if (seen.has(k)) return false; seen.add(k); return true; });
for (const f of uniq) console.log('WITNESS', JSON.stringify({w:f.w,q:f.q,toM:f.toM,size:f.size,rows:f.rows,fromM:f.fromM}));
fs.writeFileSync('/home/user/krwork/extended.json', JSON.stringify(uniq,null,1));
console.log('unique:', uniq.length);
