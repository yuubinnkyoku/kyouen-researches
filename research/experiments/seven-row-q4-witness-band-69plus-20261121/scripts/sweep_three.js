// Production sweep: restricted fresh 3-for-3 at W=69, window xMin=52, over the 199 published
// bases plus the w68 witness seed. Priority order (declared 2026-11-21 batch-2 note):
// w65 bases, w66 bases, pool_* anchors, then remaining w61-w64 families, then w68witness.
// Crash-safe resume: state.json + results.jsonl appended per base; slow (budget-exceeded)
// bases are deferred to a final escalation pass.
'use strict';
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const OUT = path.join(ROOT, 'output', 'w69', 'three');
const WITDIR = path.join(OUT, 'witnesses');
fs.mkdirSync(WITDIR, { recursive: true });
const { Board, runThree, bruteVerify } = require('./enum_three.js');

const args = {};
for (let i = 2; i < process.argv.length; i += 2) args[process.argv[i].replace(/^-+/, '')] = process.argv[i + 1];
const BUDGET_MS = Math.max(20000, parseInt(args['budget-ms'] || '140000', 10));
const MAX_BASES = Math.max(1, parseInt(args['max-bases'] || '3', 10));
const SHARD = parseInt(args.shard || '0', 10);
const NSHARDS = Math.max(1, parseInt(args.nshards || '1', 10));
const SUFFIX = NSHARDS > 1 ? `_s${SHARD}` : '';
const XMIN = 52, WIDTH = 69;

const bases = JSON.parse(fs.readFileSync(path.join(ROOT, 'input', 'bases.json'), 'utf8'));
const w68seed = JSON.parse(fs.readFileSync(path.join(ROOT, 'pub', 'witnesses_68.json'), 'utf8'))[0].stones;
const SEED_IDX = bases.length; // 199
bases.push({ tag: 'w68witness', stones: w68seed });

// priority: w65, w66, pool_*, w61-w64 (in array order), w68witness last
const prio = (t) => t === 'w65' ? 0 : t === 'w66' ? 1 : t.startsWith('pool_') ? 2 : t === 'w68witness' ? 99 : 3;
const orderAll = bases.map((b, i) => i).sort((a, b) => prio(bases[a].tag) - prio(bases[b].tag) || a - b);
const order = NSHARDS > 1 ? orderAll.filter((i) => i % NSHARDS === SHARD) : orderAll;

const statePath = path.join(OUT, `state${SUFFIX}.json`);
const resultsPath = path.join(OUT, `results${SUFFIX}.jsonl`);
let state = { done: {}, slow: {}, complete: false };
if (fs.existsSync(statePath)) state = JSON.parse(fs.readFileSync(statePath, 'utf8'));

const board = new Board(WIDTH);
const startTs = Date.now();
let processed = 0;
for (const baseIdx of order) {
  if (processed >= MAX_BASES) break;
  if (Date.now() - startTs > BUDGET_MS) break;
  if (state.done[baseIdx]) continue;
  const tries = (state.slow[baseIdx] && state.slow[baseIdx].tries) || 0;
  if (tries >= 2) continue; // defer hard bases to the escalation phase
  const b = bases[baseIdx];
  const tag = b.tag;
  const remainingBudget = BUDGET_MS - (Date.now() - startTs);
  if (remainingBudget < 5000) break;
  let res;
  try {
    res = runThree(board, b.stones, { holes: false, xMin: XMIN, maxWitnesses: 512, budgetMs: remainingBudget });
  } catch (e) {
    const rec = { base_id: baseIdx, tag, error: String(e.message), ts: new Date().toISOString() };
    fs.appendFileSync(resultsPath, JSON.stringify(rec) + '\n');
    state.done[baseIdx] = { error: rec.error }; processed++;
    continue;
  }
  if (res.timed_out) {
    const prev = state.slow[baseIdx] || { tries: 0 };
    state.slow[baseIdx] = { tries: prev.tries + 1, attempted_ms: Date.now() - startTs, removal_triples_processed: res.removal_triples_processed || 0 };
    fs.writeFileSync(statePath, JSON.stringify(state));
    continue; // move on to next base; hard bases retried in escalation
  }
  const ms = res.ms;
  let nWit = res.witnesses.length, bruteBad = 0;
  const maxes = res.witnesses.map(w => Math.max(...w.map(p => p[0])));
  if (nWit > 0) {
    const bset = new Set(b.stones.map(p => p[0] + ',' + p[1]));
    for (const w of res.witnesses) {
      if (w.filter(p => bset.has(p[0] + ',' + p[1])).length !== 17)
        fs.appendFileSync(path.join(OUT, 'BRUTE_BAD_ALERT.txt'), `base ${baseIdx} tag ${tag}: fresh diff!=3 invariant violated\n`);
    }
    for (const w of res.witnesses) { const v = bruteVerify(board, w); if (!(v.safe && v.shape_ok && v.maximal)) bruteBad++; }
    fs.writeFileSync(path.join(WITDIR, `base_${baseIdx}.json`), JSON.stringify({ tag, base_id: baseIdx, width: WIDTH, xMin: XMIN, safe_maximal_row_deficient: res.safe_maximal_row_deficient, discarded_over_cap: res.safe_maximal_row_deficient - nWit, witnesses: res.witnesses }, null, 1));
  }
  if (bruteBad > 0) fs.appendFileSync(path.join(OUT, 'BRUTE_BAD_ALERT.txt'), `base ${baseIdx} tag ${tag}: ${bruteBad} bad witnesses\n`);
  const rec = {
    base_id: baseIdx, tag, width: WIDTH, xMin: XMIN, mode: 'fresh3',
    removal_triples_processed: res.removal_triples_processed,
    triples: res.triples_examined, safe: res.safe_triples, shape_fails: res.shape_fails,
    safe_maximal_row_deficient: res.safe_maximal_row_deficient,
    n_witnesses: nWit, brute_bad: bruteBad,
    witness_maxX_table: nWit ? maxes : null,
    ms
  };
  fs.appendFileSync(resultsPath, JSON.stringify(rec) + '\n');
  state.done[baseIdx] = { m: res.safe_maximal_row_deficient, ms, t: res.triples_examined, s: res.safe_triples };
  delete state.slow[baseIdx];
  fs.writeFileSync(statePath, JSON.stringify(state));
  processed++;
}
// final escalation: if everything else is done, retry hard slow bases one per call with full budget
const hardSlow = (i) => { const s = state.slow[i]; return s && (s.tries || 0) >= 2 && !state.done[i]; };
const pending = order.filter(i => !state.done[i] && !hardSlow(i));
if (pending.length === 0) {
  const slowLeft = Object.keys(state.slow).map(Number).filter(i => !state.done[i]);
  if (slowLeft.length === 0) { state.complete = true; fs.writeFileSync(statePath, JSON.stringify(state)); }
  else {
    const idx = slowLeft[0];
    const b = bases[idx];
    const t0 = Date.now();
    const res = runThree(board, b.stones, { holes: false, xMin: XMIN, maxWitnesses: 512, budgetMs: 200000 });
    if (!res.timed_out) {
      let nWit = res.witnesses.length;
      if (nWit > 0) {
        let bruteBad = 0;
        for (const w of res.witnesses) { const v = bruteVerify(board, w); if (!(v.safe && v.shape_ok && v.maximal)) bruteBad++; }
        fs.writeFileSync(path.join(WITDIR, `base_${idx}.json`), JSON.stringify({ tag: b.tag, base_id: idx, width: WIDTH, xMin: XMIN, safe_maximal_row_deficient: res.safe_maximal_row_deficient, witnesses: res.witnesses }, null, 1));
        if (bruteBad > 0) fs.appendFileSync(path.join(OUT, 'BRUTE_BAD_ALERT.txt'), `base ${idx} tag ${b.tag}: ${bruteBad} bad witnesses (escalation)\n`);
      }
      fs.appendFileSync(resultsPath, JSON.stringify({ base_id: idx, tag: b.tag, width: WIDTH, xMin: XMIN, mode: 'fresh3-escalated', triples: res.triples_examined, safe: res.safe_triples, shape_fails: res.shape_fails, safe_maximal_row_deficient: res.safe_maximal_row_deficient, n_witnesses: nWit, ms: res.ms }) + '\n');
      state.done[idx] = { m: res.safe_maximal_row_deficient, ms: res.ms, escalated: true };
      delete state.slow[idx];
      const slowLeft2 = Object.keys(state.slow).length;
      if (slowLeft2 === 0) { state.complete = true; }
      fs.writeFileSync(statePath, JSON.stringify(state));
    } else {
      const prev = state.slow[idx] || { tries: 0 };
      prev.tries = (prev.tries || 0) + 1;
      if (prev.tries >= 3) { state.done[idx] = { error: 'budget_exhausted_after_3_escalations' }; delete state.slow[idx]; if (Object.keys(state.slow).length === 0) state.complete = true; }
      else state.slow[idx] = prev;
      fs.writeFileSync(statePath, JSON.stringify(state));
    }
  }
}
const ndone = Object.keys(state.done).length;
console.log(JSON.stringify({ processed_this_call: processed, bases_done: ndone, total: bases.length, slow: Object.keys(state.slow).length, complete: !!state.complete, wall_ms: Date.now() - startTs }));
