// extend1.js — column-extension enumeration from a single base witness (K0815 extend.js logic, single-witness driver)
// usage: node extend1.js witness.json toM out.json
const S = require('/home/user/krwork/enc/sat.js');
const fs = require('fs');
function subsets(arr, cap) {
  const res = []; const n = arr.length;
  const rec = (i, cur, sz) => { if (i===n){res.push(cur.slice());return;} rec(i+1,cur,sz); if(sz<cap){cur.push(arr[i]);rec(i+1,cur,sz+1);cur.pop();} };
  rec(0,[],0); return res;
}
const wit = JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const toM = Number(process.argv[3]);
const st = wit.stones; const w = wit.w; const q = wit.q; const m = wit.m || (wit.verify ? Math.max(...st.map(s=>s[0]))+1 : undefined);
const M = toM; const dm = M - m;
const capDef = w*(q-1)-1; const spare = capDef - st.length;
console.error(JSON.stringify({w,q,m,M,dm,capDef,spare,baseSize:st.length}));
const found = [];
if (dm >= 1 && dm*2 <= 12) {
  for (let off = 0; off <= dm; off++) {
    const shifted = st.map(([x,y]) => [x+off, y]);
    const cells = [];
    for (let x = 0; x < M; x++) for (let y = 0; y < w; y++) if (!(x >= off && x < off + m)) cells.push([x,y]);
    const subs = subsets(cells, spare);
    console.error('off', off, 'cells', cells.length, 'spare', spare, 'subsets', subs.length);
    for (const sub of subs) {
      const cand = shifted.concat(sub);
      const v = S.verifyConfig(w, M, q, cand);
      if (v.ok) found.push({w,q,fromM:m,toM:M,off,size:cand.length,stones:cand,rows:v.rows});
    }
  }
}
fs.writeFileSync(process.argv[4], JSON.stringify({w,q,fromM:m,toM:M,base:{size:st.length,stones:st},extensions:found},null,1));
console.log('extensions found:', found.length);
for (const f of found) console.log('WITNESS', JSON.stringify({w:6,q,toM:M,off:f.off,size:f.size,rows:f.rows}));
