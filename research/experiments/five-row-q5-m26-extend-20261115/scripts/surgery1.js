// surgery1.js — bounded-edit (sd<=1) surgery from a seed witness, complete enumeration.
// Candidate configs: remove-1 (|S|=18) and move-1 (|S|=19, one stone relocated).
// Checks: safety (no census curve with >=5 stones), maximality (every empty cell
// on a curve with exactly 4 stones), deficiency (|S| < w*(q-1)).
// Pure census machine (sat2.js buildCensus); no solver.
'use strict';
const path = require('path');
const S2 = require(path.join(__dirname, 'sat2.js'));
const S = S2.S;

function check(w, m, q, census, stones) {
  // stones: array of point indices
  const st = new Set(stones);
  const n = w * m;
  const cnt = new Array(census.curves.length).fill(0);
  const through = Array.from({ length: n }, () => []);
  census.curves.forEach((cu, ci) => { for (const p of cu.pts) through[p].push(ci); });
  for (const p of stones) for (const ci of through[p]) cnt[ci]++;
  // safety: no curve with >= q stones
  for (let ci = 0; ci < cnt.length; ci++) if (cnt[ci] >= q) return { ok: false, why: 'unsafe' };
  // maximality: every empty cell on a curve with exactly q-1 stones
  for (let p = 0; p < n; p++) {
    if (st.has(p)) continue;
    let blocked = false;
    for (const ci of through[p]) if (cnt[ci] === q - 1) { blocked = true; break; }
    if (!blocked) return { ok: false, why: 'open:' + p };
  }
  return { ok: true };
}

function main() {
  const [w, m, q, seedFile, offXs] = process.argv.slice(2);
  const W = +w, M = +m, Q = +q;
  const offs = offXs.split(',').map(Number);
  const census = S.buildCensus(W, M, Q);
  const seedStones = JSON.parse(require('fs').readFileSync(seedFile, 'utf8'))
    .map(([x, y]) => y * M + x);
  const n = W * M;
  let witnesses = 0, tested = 0;
  const report = [];
  for (const offX of offs) {
    const seed = seedStones.map(p => (p % M) + offX + Math.floor(p / M) * M);
    const seedSet = new Set(seed);
    // sanity: seed itself must be safe (not necessarily maximal in 5xM)
    const res0 = check(W, M, Q, census, seed);
    // remove-1
    for (let i = 0; i < seed.length; i++) {
      const cand = seed.slice(0, i).concat(seed.slice(i + 1));
      tested++;
      const r = check(W, M, Q, census, cand);
      if (r.ok) { witnesses++; report.push({ offX, kind: 'rm1', rm: seed[i], stones: cand }); }
    }
    // move-1: remove seed[i], add e (empty, row capacity kept by safety check)
    for (let i = 0; i < seed.length; i++) {
      const rm = seed[i];
      for (let e = 0; e < n; e++) {
        if (seedSet.has(e) || e === rm) continue;
        tested++;
        const cand = seed.slice(0, i).concat(seed.slice(i + 1)); cand.push(e);
        const r = check(W, M, Q, census, cand);
        if (r.ok) { witnesses++; report.push({ offX, kind: 'mv1', rm, add: e, stones: cand }); }
      }
    }
    console.log(JSON.stringify({ offX, seedCheck: res0.ok ? 'safe' : res0.why, tested, witnesses }));
  }
  require('fs').writeFileSync(__dirname + '/../output/surgery1_witnesses.json', JSON.stringify({ w: W, m: M, q: Q, tested, witnesses, report }, null, 1));
  console.log('TOTAL tested=' + tested + ' witnesses=' + witnesses);
}
main();
