// Self-test of the 1-for-0 (19-stone direct maximality) checker used in sweep69.js.
// Positive control: the published width-68 witness (20 stones, one deficient row) is maximal on 7x68.
// Negative control: same witness with one stone removed is NOT maximal on 7x68.
// Both use the same blocked-cell union logic (C(n,3) triple curves) as maxCheckOneForZero.
'use strict';
const fs = require('fs');
const { Board } = require('./enum_two.js');

function maximalCheck(board, stones, W) {
  const rows = new Array(7).fill(0);
  for (const [x, y] of stones) rows[y]++;
  const occ = new Set(stones.map(([x, y]) => x + ':' + y));
  const blocked = new Set();
  const n = stones.length;
  for (let a = 0; a < n; a++) for (let b = a + 1; b < n; b++) for (let c = b + 1; c < n; c++) {
    const pts = board.key3(stones[a][0], stones[a][1], stones[b][0], stones[b][1], stones[c][0], stones[c][1]);
    for (const u of pts) blocked.add((u % W) + ':' + ((u / W) | 0));
  }
  if (blocked.size === 0) return { maximal: false, firstUnblocked: null };
  for (let y = 0; y < 7; y++) {
    if (rows[y] === 3) continue;
    for (let x = 0; x < W; x++) {
      if (occ.has(x + ':' + y)) continue;
      if (!blocked.has(x + ':' + y)) return { maximal: false, firstUnblocked: [x, y] };
    }
  }
  return { maximal: true, firstUnblocked: null };
}

const w68 = JSON.parse(fs.readFileSync('../output/w68/witnesses_68.json', 'utf8'))[0].stones;
const pos = maximalCheck(new Board(68), w68, 68);
const pert = w68.slice(); pert.splice(0, 1);
const neg = maximalCheck(new Board(68), pert, 68);
const ok = pos.maximal === true && neg.maximal === false && neg.firstUnblocked !== null;
fs.writeFileSync('output/w69/selftest_1f0.json', JSON.stringify({
  positive_control_maximal: pos.maximal,
  negative_control_maximal: neg.maximal,
  negative_control_first_unblocked: neg.firstUnblocked,
  pass: ok
}, null, 2) + '\n');
console.log(JSON.stringify({ pass: ok, pos, neg }));
process.exit(ok ? 0 : 1);
