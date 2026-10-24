#!/usr/bin/env node
'use strict';
// Independent terminal recheck of the 52 selected leaves, followed by a
// provenance-limited S8 LOSS -> S7 LOSS -> S6 coverage union.
// Outcomes are fixed-original-first WIN/LOSS, not side-to-move P/N.
const fs = require('node:fs');
const path = require('node:path');
const g = require('../n11-gap6-terminal-20261019/verify_js.js');
const {ROOTS: BATCH8} = require('../n11-terminal-s7-batch8-union-20261024/audit.js');
const {ROOTS: LEGACY3} = require('../n11-terminal-s7-three-legacy-s9-union-20261024/audit.js');
const base = path.resolve(__dirname, '..');
const read = p => fs.readFileSync(path.join(base, p), 'utf8');
const keys = s => s.trim().split(/\s+/);
const need = (ok, msg) => { if (!ok) throw Error(msg); };
const groupPaths = [
  'n11-s9-win29-lift-20261023/s9-win29.keys',
  'n11-s9-win27-expansion-20261024/s9-win27.keys',
  'n11-s9-win2-followup-20261024/s9-win2.keys',
  'n11-s9-win10-20261024/s9-win10.keys',
  'n11-s9-win7-expansion-20261024/s9-win7.keys',
  'n11-s9-win20-neighbor-20261024/s9-win20.keys',
  'n11-s8-frontier-13way-20261024/s9-win7.keys'
];
const fourPath = 'n11-four-s8-joint-terminal52-20261023/';
function terminalBoundary(roots, selected, rows, terminal = true) {
  need(roots.length === 4 && new Set(roots).size === 4, 'four distinct S8 roots required');
  need(selected.length === 52 && new Set(selected).size === 52, '52 distinct S10 leaves required');
  const obligations = new Set();
  for (const h of roots) {
    for (const child of g.children(g.board(h, 8))) obligations.add(child);
  }
  need(obligations.size === 103, 'S9 obligations changed');
  const covered = new Set();
  let states = 0;
  for (const h of selected) {
    const b = g.board(h, 10);
    const row = rows.get(h);
    need(row && row.verdict === 'LOSS', 'selected leaf missing or not LOSS: ' + h);
    if (terminal) {
      const result = g.solve10(h);
      need(!result.win && result.states === row.states && result.legal === row.legal,
        'independent S10 result differs: ' + h);
      states += result.states;
    }
    for (const p of g.pts(b)) {
      const parent = g.key(g.canonical(b ^ (1n << BigInt(p))));
      if (obligations.has(parent)) covered.add(parent);
    }
  }
  need(covered.size === obligations.size, 'uncovered S9 obligation');
  if (terminal) need(states === 12280, 'terminal state count changed');
  return {obligations: obligations.size, selectedLeaves: selected.length,
    independentlyRecomputedLeaves: terminal ? selected.length : 0,
    states: terminal ? states : null};
}
function audit({terminal = true} = {}) {
  const roots = keys(read(fourPath + 'roots4.keys'));
  const selected = keys(read(fourPath + 'selected52.keys'));
  const rows = new Map(read(fourPath + 's10-all1017.tsv').trim().split(/\r?\n/).map(line => {
    const [h, verdict, states, legal] = line.trim().split(/\s+/);
    need(/^[0-9a-f]{32}$/.test(h) && /^(WIN|LOSS)$/.test(verdict) &&
      Number.isInteger(+states) && Number.isInteger(+legal), 'invalid S10 table row');
    return [h, {verdict, states: +states, legal: +legal}];
  }));
  need(rows.size === 1017, 'S10 table changed');
  const terminalResult = terminalBoundary(roots, selected, rows, terminal);
  const oldCert = JSON.parse(read('n11-s7-terminal-loss12-20261024/certificate.json'));
  const gap = JSON.parse(read('n11-gap6-terminal-20261019/gap6-terminal-cert.json'));
  const loss8 = new Set([
    ...keys(read('n11-s8-compact385-pruned1946-20261020/loss_roots35.txt')),
    ...oldCert.s8_loss, gap.s8_loss_root,
    '00000000000040001000044400830000'
  ]);
  need(loss8.size === 40 && roots.every(h => !loss8.has(h)), 'prior LOSS8 overlap');
  const s9 = new Set([
    ...groupPaths.flatMap(p => keys(read(p))),
    ...oldCert.new_s9_win, ...BATCH8, ...LEGACY3
  ]);
  need(s9.size === 131, 'certified S9 baseline changed');
  const win8 = g.reverse(s9);
  for (const p of [
    'n11-s7-38-terminal-20261019/s8_38_win_proof.tsv',
    'n11-s8-neighbor24-round8-20261020/proof24_optimized.tsv',
    'n11-s8-round9-global78-20261020/round9_proof_optimized.tsv'
  ]) for (const line of read(p).split(/\r?\n/)) {
    if (line.startsWith('ROOT\t')) {
      const row = line.split('\t');
      if (row[2] === 'WIN') win8.add(row[1]);
    }
  }
  const fourCert = JSON.parse(read('n11-s7-four-win-terminal-20261020/s7_win_four_min_certificate.json'));
  for (const h of Object.keys(fourCert.s8_witness)) win8.add(h);
  for (const line of read('n11-s7-fifth-terminal-20261015/fifth-s7-win-terminal.cert').split(/\r?\n/))
    if (line.startsWith('EDGE ')) win8.add(line.split(' ')[1]);
  for (const row of gap.s8_win_roots) win8.add(row.root);
  need(win8.size === 1326, 'certified WIN8 baseline changed');
  const frozenWin8 = new Set(keys(read('n11-targeted-terminal-lift-20261015/data/lifted_s8_win_51571.txt')));
  const frozenLoss8 = new Set(keys(read('n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt')));
  need(frozenWin8.size === 13501 && frozenLoss8.size === 294, 'frozen comparison changed');
  need(roots.every(h => !win8.has(h) && !frozenWin8.has(h)), 'WIN/LOSS conflict at S8');
  need(roots.filter(h => frozenLoss8.has(h)).length === 1, 'frozen LOSS8 overlap changed');
  const old7 = g.reverse(loss8), new7 = g.reverse(roots);
  const all7 = g.reverse([...loss8, ...roots]);
  const fresh7 = new Set([...new7].filter(h => !old7.has(h)));
  const frozenWin7 = new Set(keys(read('n11-targeted-terminal-lift-20261015/data/all_s7_win_17.txt')));
  const frozenLoss7 = new Set(keys(read('n11-targeted-terminal-lift-20261015/data/all_s7_loss_2232.txt')));
  need(frozenWin7.size === 17 && frozenLoss7.size === 2232, 'frozen S7 comparison changed');
  need([...new7].every(h => !frozenWin7.has(h)), 'WIN/LOSS conflict at S7');
  const old6 = g.reverse(old7), new6 = g.reverse(new7), all6 = g.reverse(all7);
  const addedPairs = new Set();
  for (const h of fresh7) {
    const b = g.board(h, 7);
    for (const p of g.pts(b)) {
      const parent = g.key(g.canonical(b ^ (1n << BigInt(p))));
      addedPairs.add(parent + ':' + h);
    }
  }
  const frozenLossOverlap = [...fresh7].filter(h => frozenLoss7.has(h)).length;
  need(old7.size === 282 && new7.size === 30 && fresh7.size === 29 &&
    all7.size === 311 && old6.size === 854 && new6.size === 97 &&
    all6.size === 944 && addedPairs.size === 203 && frozenLossOverlap === 12,
    'reverse coverage baseline changed');
  return {terminal: terminalResult, priorS8Loss: 40, addedS8Loss: 4, allS8Loss: 44,
    priorS7Loss: old7.size, newS7FromFour: new7.size,
    addedS7Loss: fresh7.size, allS7Loss: all7.size,
    addedS7AlreadyFrozenLoss: frozenLossOverlap,
    addedS7AbsentFromFrozenLoss: fresh7.size - frozenLossOverlap,
    priorS6Parents: old6.size, newS6ParentsFromFour: new6.size,
    addedS6Parents: all6.size - old6.size, allS6Parents: all6.size,
    addedS6S7ClassEdges: addedPairs.size, certifiedS8Win: win8.size,
    certifiedS9Win: s9.size, polarityConflicts: 0,
    newS6Closure: 0, newTwoStoneClosure: 0, emptyBoard: 'UNKNOWN'};
}
if (require.main === module) {
  console.log(JSON.stringify(audit(), null, 2));
  if (process.argv.includes('--negative')) {
    const roots = keys(read(fourPath + 'roots4.keys'));
    const selected = keys(read(fourPath + 'selected52.keys'));
    const rows = new Map(read(fourPath + 's10-all1017.tsv').trim().split(/\r?\n/).map(line => {
      const [h, verdict, states, legal] = line.trim().split(/\s+/);
      return [h, {verdict, states: +states, legal: +legal}];
    }));
    const trials = [
      () => terminalBoundary(roots, selected.slice(1), rows, false),
      () => terminalBoundary(roots, [selected[0], ...selected.slice(0, 51)], rows, false),
      () => terminalBoundary([roots[0], roots[0], roots[2], roots[3]], selected, rows, false),
      () => {
        const bad = new Map(rows);
        bad.set(selected[0], {...rows.get(selected[0]), verdict: 'WIN'});
        terminalBoundary(roots, selected, bad, false);
      }
    ];
    for (const trial of trials) {
      let rejected = false;
      try { trial(); } catch (_) { rejected = true; }
      need(rejected, 'tampered certificate accepted');
    }
    console.error('PASS four malformed-certificate rejections');
  }
}
module.exports = {audit, terminalBoundary};
