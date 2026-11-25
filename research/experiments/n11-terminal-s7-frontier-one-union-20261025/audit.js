#!/usr/bin/env node
'use strict';
// Reuse one overlooked 2026-10-17 S9 terminal certificate in the S7 proof-only union.
// All WIN/LOSS labels are from the fixed original-first viewpoint.
const fs = require('node:fs');
const path = require('node:path');
const g = require('../n11-gap6-terminal-20261019/verify_js.js');
const legacy = require('../n11-s6-legacy29-union-20261025/audit.js');
const previous = require('../n11-terminal-s7-s8-legacy187-union-20261025/audit.js');
const latestLoss = require('../n11-s6-legacy3-loss-union-20261025/audit.js');
const EXP = path.resolve(__dirname, '..');
const ROOT = '00000100110002001042100000000010';
const SOURCE = 'n11-frontier-5proofs-20261017/input/s9-win-' + ROOT + '.cert';
const read = p => fs.readFileSync(path.join(EXP, p), 'utf8');
const need = (ok, msg) => { if (!ok) throw Error(msg); };
const ADDED = [
  '00000000000010841000800110010000',
  '00000000000200003140400000000044',
  '00000000110002001042100000000010',
  '00000100010002001042100000000010',
  '00000100110000001042100000000010',
  '00000100110002000042100000000010',
  '00000100110002001040100000000010',
  '00000100110002001042000000000010'
];
function checkCertificate(raw, {terminal = true} = {}) {
  const lines = raw.trimEnd().split(/\r?\n/);
  need(lines.length === 21 &&
    lines[0] === '# n11-S9-WIN-terminal-v1' &&
    lines[1] === 'BOARD 11' &&
    lines[2] === 'S9 ' + ROOT &&
    lines[3] === 'S10_WIN_LEAVES 16' &&
    lines.at(-1) === 'END', 'invalid certificate frame');
  const root = g.board(ROOT, 9);
  const actual = g.children(root);
  const leaves = lines.slice(4, -1).map(line => {
    need(/^LEAF [0-9a-f]{32}$/.test(line), 'malformed leaf');
    const h = line.slice(5);
    g.board(h, 10);
    return h;
  });
  need(actual.size === 16 && leaves.length === 16 &&
    new Set(leaves).size === 16 &&
    leaves.every(h => actual.has(h)), 'S9 AND boundary incomplete');
  let states = 0;
  if (terminal) {
    for (const h of leaves) {
      const result = g.solve10(h);
      need(result.win, 'false terminal S10 WIN: ' + h);
      states += result.states;
    }
    need(states === 185, 'S10 terminal-state count changed');
  }
  return {root: ROOT, leaves: leaves.length, terminalStates: terminal ? states : null};
}
function audit() {
  const source = checkCertificate(read(SOURCE));
  const baseline = previous.audit();
  need(baseline.totalS8Win === 1513 && baseline.totalS7Parents === 6199 &&
    baseline.securedS7Moves === 12106 && baseline.securedS7Classes === 12104 &&
    baseline.closedS7 === 6, 'previous proof-only baseline changed');
  const win8 = new Set([...legacy.certifiedWin8(), ...previous.sourceEdges().keys()]);
  need(win8.size === 1513, 'S8 WIN baseline changed');
  const derived8 = g.reverse([ROOT]);
  need(derived8.size === 9 && !win8.has(ROOT), 'S9/S8 source count changed');
  for (const h of derived8)
    need(g.children(g.board(h, 8)).has(ROOT), 'illegal S8 to S9 witness');
  const added8 = new Set([...derived8].filter(h => !win8.has(h)));
  need(added8.size === 8 &&
    [...added8].sort().join('\n') === ADDED.join('\n'), 'new S8 keys changed');
  const certifiedLoss8 = new Set([
    ...previous.certifiedLoss8(), ...latestLoss.source().cert.roots
  ]);
  const frozenLoss8 = new Set(read(
    'n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'
  ).trim().split(/\s+/));
  need(certifiedLoss8.size === 76 && frozenLoss8.size === 294 &&
    [...added8].every(h => !certifiedLoss8.has(h) && !frozenLoss8.has(h)),
    'S8 WIN/LOSS conflict');
  const old7 = g.reverse(win8), affected7 = g.reverse(added8);
  const all7 = new Set([...old7, ...affected7]);
  need(old7.size === 6199 && affected7.size === 36 &&
    all7.size === 6226, 'S7 parent union changed');
  const certifiedLoss7 = g.reverse(certifiedLoss8);
  need(certifiedLoss7.size === 554, 'S7 LOSS comparison changed');
  let moves = 0, classes = 0, minAffectedGap = Infinity;
  const closed = [];
  for (const h of affected7) {
    const b = g.board(h, 7), legalClasses = new Set(), newClasses = new Set();
    const oldClasses = new Set();
    for (const p of g.legal(b)) {
      const child = g.key(g.canonical(b | (1n << BigInt(p))));
      legalClasses.add(child);
      if (added8.has(child)) { moves++; newClasses.add(child); }
      if (win8.has(child)) oldClasses.add(child);
    }
    classes += newClasses.size;
    const gap = legalClasses.size -
      new Set([...newClasses, ...oldClasses]).size;
    minAffectedGap = Math.min(minAffectedGap, gap);
    if (!gap) closed.push(h);
  }
  need(moves === 64 && classes === 64 && minAffectedGap === 28 &&
    closed.length === 0, 'S7 secured coverage or closure changed');
  return {...source, previousS9Win: 131, addedS9Win: 1,
    totalS9Win: 132, previousS8Win: 1513, addedS8Win: 8,
    totalS8Win: 1521, previousS7Parents: 6199, addedS7Parents: 27,
    totalS7Parents: 6226, affectedS7Parents: affected7.size,
    addedSecuredS7Moves: moves, securedS7Moves: 12106 + moves,
    addedSecuredS7Classes: classes, securedS7Classes: 12104 + classes,
    minimumUncoveredAmongAffectedS7: minAffectedGap,
    totalClosedS7: 6, newlyClosedS7: 0,
    independentlyProvedS8Loss: certifiedLoss8.size,
    independentlyProvedS7Loss: certifiedLoss7.size,
    winLossConflicts: 0, newlyClosedTwoStoneRoots: 0, emptyBoard: 'UNKNOWN'};
}
module.exports = {audit, checkCertificate};
if (require.main === module) {
  console.log(JSON.stringify(audit(), null, 2));
  if (process.argv.includes('--negative')) {
    const raw = read(SOURCE), lines = raw.trimEnd().split(/\r?\n/);
    const bad = [
      raw.replace('BOARD 11', 'BOARD 10'),
      lines.filter((_, i) => i !== 4).join('\n') + '\n',
      lines.map((s, i) => i === 5 ? lines[4] : s).join('\n') + '\n',
      raw.replace('S9 ' + ROOT, 'S9 ' + '0'.repeat(32))
    ];
    for (const changed of bad) {
      let rejected = false;
      try { checkCertificate(changed, {terminal: false}); }
      catch (_) { rejected = true; }
      need(rejected, 'malformed S9 certificate accepted');
    }
    console.error('PASS four malformed-certificate rejections');
  }
}
