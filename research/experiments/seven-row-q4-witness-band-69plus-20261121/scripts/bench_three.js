// One-base benchmark for the production configuration (W=69, xMin=52, fresh 3-for-3).
'use strict';
const fs = require('fs');
const path = require('path');
const { Board, runThree, bruteVerify } = require('./enum_three.js');
const bases = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'input', 'bases.json'), 'utf8'));
const tag = process.argv[2] || 'w65';
const idx = parseInt(process.argv[3] || '0', 10);
const matches = bases.map((b, i) => ({ ...b, i })).filter(b => b.tag === tag);
const base = matches[idx % matches.length];
const board = new Board(69);
const t0 = Date.now();
const res = runThree(board, base.stones, { holes: false, xMin: 52, maxWitnesses: 512, budgetMs: 200000 });
const total = Date.now() - t0;
const out = {
  tag: base.tag, base_index_in_tag_list: idx % matches.length, base_array_index: base.i,
  maxX: Math.max(...base.stones.map(p => p[0])),
  timed_out: !!res.timed_out, ms_engine: res.ms, ms_total: total,
  triples: res.triples_examined, safe: res.safe_triples, shape: res.shape_fails,
  maximal: res.safe_maximal_row_deficient, n_witnesses: res.witnesses.length,
  witness_maxX: res.witnesses.length ? Math.max(...res.witnesses.flat().map(p => p[0])) : null
};
console.log(JSON.stringify(out));
if (res.witnesses.length) {
  let bad = 0;
  for (const w of res.witnesses) { const v = bruteVerify(board, w); if (!(v.safe && v.shape_ok && v.maximal)) bad++; }
  out.brute_bad = bad;
  console.log(JSON.stringify({ brute_bad: bad }));
}
