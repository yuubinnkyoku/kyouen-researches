// surgery2.js — bounded-edit surgery add<=2 remove<=2 from a seed, complete enumeration.
// Families with deficiency (total < w*(q-1)): rm2 (17), rm2+add1 (18), rm2+add2 (19),
// rm1 (18, done in surgery1), mv1=rm1+add1 (19, done in surgery1).
// rm1+add2 / add-only reach total >= 20 (full) or violate row capacity => excluded.
'use strict';
const path = require('path');
const fs = require('fs');
const S2 = require(path.join(__dirname, 'sat2.js'));
const S = S2.S;

function buildOnce(w, m, q) {
  const census = S.buildCensus(w, m, q);
  const n = w * m;
  const through = Array.from({ length: n }, () => []);
  census.curves.forEach((cu, ci) => { for (const p of cu.pts) through[p].push(ci); });
  return { census, through, n, nCurves: census.curves.length };
}

function checkFast(M, stones, through, nCurves, q, n) {
  const st = new Set(stones);
  const cnt = new Int32Array(nCurves);
  for (const p of stones) { const th = through[p]; for (let k = 0; k < th.length; k++) cnt[th[k]]++; }
  for (let ci = 0; ci < nCurves; ci++) if (cnt[ci] >= q) return false;
  for (let p = 0; p < n; p++) {
    if (st.has(p)) continue;
    let blocked = false;
    const th = through[p];
    for (let k = 0; k < th.length; k++) if (cnt[th[k]] === q - 1) { blocked = true; break; }
    if (!blocked) return false;
  }
  return true;
}

function main() {
  const [w, m, q, seedFile, offXs] = process.argv.slice(2);
  const W = +w, M = +m, Q = +q;
  const offs = offXs.split(',').map(Number);
  const { through, n, nCurves } = buildOnce(W, M, Q);
  const seedStones = JSON.parse(fs.readFileSync(seedFile, 'utf8')).map(([x, y]) => y * M + x);
  let tested = 0, witnesses = 0;
  const report = [];
  const t0 = Date.now();
  for (const offX of offs) {
    const seed = seedStones.map(p => (p % M) + offX + Math.floor(p / M) * M);
    const seedSet = new Set(seed);
    const empty = [];
    for (let e = 0; e < n; e++) if (!seedSet.has(e)) empty.push(e);
    // rm2
    for (let i = 0; i < seed.length; i++) for (let j = i + 1; j < seed.length; j++) {
      const cand = seed.filter((_, k) => k !== i && k !== j);
      tested++;
      if (checkFast(M, cand, through, nCurves, Q, n)) { witnesses++; report.push({ offX, kind: 'rm2', rm: [seed[i], seed[j]], stones: cand }); }
    }
    // rm2 + add1
    for (let i = 0; i < seed.length; i++) for (let j = i + 1; j < seed.length; j++) {
      const base = seed.filter((_, k) => k !== i && k !== j);
      for (const e of empty) {
        if (e === seed[i] || e === seed[j]) continue;
        tested++;
        const cand = base.concat([e]);
        if (checkFast(M, cand, through, nCurves, Q, n)) { witnesses++; report.push({ offX, kind: 'rm2add1', rm: [seed[i], seed[j]], add: e, stones: cand }); }
      }
    }
    // rm2 + add2
    for (let i = 0; i < seed.length; i++) for (let j = i + 1; j < seed.length; j++) {
      const base = seed.filter((_, k) => k !== i && k !== j);
      for (let a = 0; a < empty.length; a++) {
        if (empty[a] === seed[i] || empty[a] === seed[j]) continue;
        for (let b = a + 1; b < empty.length; b++) {
          if (empty[b] === seed[i] || empty[b] === seed[j]) continue;
          tested++;
          const cand = base.concat([empty[a], empty[b]]);
          if (checkFast(M, cand, through, nCurves, Q, n)) { witnesses++; report.push({ offX, kind: 'rm2add2', rm: [seed[i], seed[j]], add: [empty[a], empty[b]], stones: cand }); }
        }
      }
      if (Date.now() - t0 > 1000 * 60 * 25) { console.error('time-guard hit at pair ' + i + ',' + j); process.exit(9); }
    }
    console.log(JSON.stringify({ offX, cumulativeTested: tested, witnesses }));
  }
  fs.writeFileSync(__dirname + '/../output/surgery2_witnesses.json', JSON.stringify({ w: W, m: M, q: Q, tested, witnesses, report }, null, 1));
  console.log('TOTAL tested=' + tested + ' witnesses=' + witnesses + ' ms=' + (Date.now() - t0));
}
main();
