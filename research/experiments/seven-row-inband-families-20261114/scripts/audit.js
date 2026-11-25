// audit.js — (A) finite verification of the 10-point-circle classification for w=7 (q=10 census)
//           (B) blocking-structure audit of a deficient-row witness.
'use strict';
const path = require('path');
const S = require(path.join(__dirname, 'sat.js'));

// --- (A) classification ---
// Conjecture (finitely verified): in a 7 x m board, every 10-point circle is a translate of
// one of exactly two families: A (doubled rows {0,2,3,5,6}, canonical offsets
// row0={1,6}, row2={0,7}, row3={0,7}, row5={1,6}, row6={3,4}) and B (doubled rows
// {0,1,3,4,6}, row0={3,4}, row1={1,6}, row3={0,7}, row4={0,7}, row6={1,6}; V-image of A),
// with an 8-column window [t, t+7]; count exactly 2(m-7).
function classify(mMax) {
  const A = '0,2,3,5,6', B = '0,1,3,4,6';
  const canonA = new Map(), canonB = new Map();
  let allOK = true;
  const rows = [];
  for (let m = 8; m <= mMax; m++) {
    let tens = null, nA = 0, nB = 0, bad = 0, ok = false;
    try {
      const { P, curves } = S.buildCensus(7, m, 10);
      tens = curves.filter(c => c.type === 'circle' && c.pts.length === 10);
      const tset = new Set();
      for (const c of tens) {
        const byRow = new Map();
        let minX = Infinity, maxX = -1;
        for (const i of c.pts) { const [x, y] = P[i]; if (!byRow.has(y)) byRow.set(y, []); byRow.get(y).push(x); if (x < minX) minX = x; if (x > maxX) maxX = x; }
        const doubled = [...byRow.keys()].filter(y => byRow.get(y).length === 2).sort().join(',');
        if (byRow.size !== 5 || [...byRow.values()].some(v => v.length !== 2) || (doubled !== A && doubled !== B) || maxX - minX !== 7) { bad++; continue; }
        const t = minX;
        tset.add(t);
        const rel = [];
        for (const y of [...byRow.keys()].sort((a, b) => a - b)) rel.push(byRow.get(y).map(x => x - t).sort((a, b) => a - b).join(';'));
        const relKey = JSON.stringify(rel);
        if (doubled === A) { nA++; canonA.set(relKey, (canonA.get(relKey) || 0) + 1); }
        else { nB++; canonB.set(relKey, (canonB.get(relKey) || 0) + 1); }
      }
      const expect = 2 * (m - 7);
      ok = tens.length === expect && nA === m - 7 && nB === m - 7 && bad === 0 && [...tset].length === m - 7;
    } catch (e) { ok = false; }
    rows.push({ m, tens: tens === null ? -1 : tens.length, nA, nB, bad, expect: 2 * (m - 7), ok });
    if (!ok) allOK = false;
    require('fs').writeFileSync(__dirname + '/../output/classification_q10.json', JSON.stringify({ allOK, mMax, rows, canonicalA: [...canonA.keys()], canonicalB: [...canonB.keys()] }) + '\n');
  }
  return { allOK, mMax, rows, canonicalA: [...canonA.keys()], canonicalB: [...canonB.keys()] };
}

// --- (B) witness blocking audit (w=7, q=10) ---
function audit(wit, w, q) {
  const { m, stones } = wit;
  const { P, curves } = S.buildCensus(w, m, q);
  const stoneSet = new Set(stones.map(([x, y]) => y * m + x));
  const rows = Array.from({ length: w }, (_, y) => stones.filter(s => s[1] === y).length);
  const L = rows.findIndex(c => c <= q - 2);
  if (L < 0 || rows.some((c, y) => y !== L && c !== q - 1)) return { error: 'unexpected row profile', rows };
  const perCell = [];
  let typeBad = 0;
  const partnerDist = new Map();
  for (let x = 0; x < m; x++) {
    const idx = L * m + x;
    if (stoneSet.has(idx)) continue;
    const blockers = [];
    for (const cu of curves) {
      if (cu.pts.length < q || !cu.pts.includes(idx)) continue;
      const stonesOn = cu.pts.filter(p => stoneSet.has(p));
      if (stonesOn.length < q - 1) continue;
      const lpts = cu.pts.filter(p => Math.floor(p / m) === L);
      const lstones = lpts.filter(p => stoneSet.has(p));
      const okType1 = cu.pts.length === 10 && lpts.length === 2 && lstones.length === 1 && stonesOn.length === 9 && lpts.includes(idx);
      if (!okType1) typeBad++;
      const partner = lpts.find(p => p !== idx);
      if (partner && stoneSet.has(partner)) {
        const d = Math.abs((partner % m) - x);
        partnerDist.set(d, (partnerDist.get(d) || 0) + 1);
      }
      blockers.push({ type: cu.type, pts: cu.pts.length, stonesOn: stonesOn.length, lpts: lpts.length, lstones: lstones.length, okType1, partnerOffset: partner != null ? (partner % m) - x : null });
    }
    perCell.push({ x, n: blockers.length, allType1: blockers.every(b => b.okType1) });
  }
  return { w, m, q, L, rows, deficientStones: rows[L], emptyCells: perCell.length,
    blockedOK: perCell.every(c => c.n > 0),
    allType1: typeBad === 0 && perCell.every(c => c.n > 0 && c.allType1),
    partnerDistances: Object.fromEntries(partnerDist),
    perCell };
}

if (require.main === module) {
  const mode = process.argv[2];
  if (mode === 'classify') {
    const r = classify(parseInt(process.argv[3]));
    console.log(JSON.stringify({ allOK: r.allOK, mMax: r.mMax, canonicalA: r.canonicalA, canonicalB: r.canonicalB }));
    process.exit(r.allOK ? 0 : 1);
  } else if (mode === 'witness') {
    const fs = require('fs');
    const wits = JSON.parse(fs.readFileSync(process.argv[3], 'utf8')).families;
    const out = {};
    for (const fam of Object.keys(wits)) {
      const mm = /^w(\d+)q(\d+)$/.exec(fam);
      if (!mm) continue;
      const w = Number(mm[1]), q = Number(mm[2]);
      for (const wit of wits[fam]) out[`${fam}_m${wit.m}`] = audit(wit, w, q);
    }
    fs.writeFileSync(__dirname + '/../output/witness_audit_q10.json', JSON.stringify(out, null, 1) + '\n');
    console.log(JSON.stringify(Object.fromEntries(Object.entries(out).map(([k, v]) => [k, { L: v.L, blockedOK: v.blockedOK, allType1: v.allType1, partnerDistances: v.partnerDistances }]))));
  } else { console.error('usage: audit.js classify <mMax> | witness <witnesses.json>'); process.exit(2); }
}
