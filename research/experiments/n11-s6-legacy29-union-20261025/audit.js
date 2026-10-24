#!/usr/bin/env node
'use strict';
// Provenance-limited integration of the 2026-10-15 terminal-proved 29 S8 LOSS roots.
// WIN/LOSS is fixed-original-first polarity. This is a structural audit:
// the 483 S10 LOSS leaf verdicts are independently established by K0426's
// C++ and Python terminal verifiers, not recomputed by this script.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const g = require('../n11-gap6-terminal-20261019/verify_js.js');
const {ROOTS: BATCH8} = require('../n11-terminal-s7-batch8-union-20261024/audit.js');
const {ROOTS: LEGACY3} = require('../n11-terminal-s7-three-legacy-s9-union-20261024/audit.js');
const EXP = path.resolve(__dirname, '..');
const read = p => fs.readFileSync(path.join(EXP, p), 'utf8');
const need = (ok, why) => { if (!ok) throw Error(why); };
const keys = p => read(p).trim().split(/\s+/);
const unique = a => new Set(a);
const oldCertPath = 'n11-s7-terminal-loss12-20261024/certificate.json';
const gapPath = 'n11-gap6-terminal-20261019/gap6-terminal-cert.json';
const oldCert = () => JSON.parse(read(oldCertPath));
const gapCert = () => JSON.parse(read(gapPath));
function extractCertificate() {
  const raw = read('n11-s6-terminal-loss-20261015/s6-loss-optimized.cert');
  need(crypto.createHash('sha256').update(raw).digest('hex') ===
    'cb2e73c277c6fd526689db64b1d8c07ebd1ca1bd8c2a966e0757d22c4471ebf6',
    'terminal certificate differs from the independently verified K0426 SHA-256');
  const lines = raw.split(/\r?\n/);
  need(lines.filter(x => x === 'END').length === 1 && lines.filter(Boolean).at(-1) === 'END',
    'certificate END marker missing or duplicated');
  need(lines[0] === '# n11-S8-LOSS-global-terminal-v1' && lines[1] === 'BOARD 11',
    'unexpected source certificate format');
  const roots = [], leaves = [];
  for (const line of lines.slice(2)) {
    if (!line || line === 'END') continue;
    const m = /^(ROOT|LEAF) ([0-9a-f]{32})$/.exec(line);
    need(!!m, 'unexpected certificate line: ' + line);
    (m[1] === 'ROOT' ? roots : leaves).push(m[2]);
  }
  return {roots, leaves};
}
function boundary(roots, leaves) {
  need(roots.length === 29 && unique(roots).size === 29, '29 distinct S8 roots required');
  need(leaves.length === 483 && unique(leaves).size === 483, '483 distinct S10 leaves required');
  const obligations = new Set();
  let edges = 0;
  for (const h of roots) {
    const children = g.children(g.board(h, 8));
    edges += children.size;
    for (const c of children) obligations.add(c);
  }
  need(edges === 1046 && obligations.size === 1035, 'S8 to S9 boundary changed');
  const covered = new Set();
  for (const h of leaves) {
    const b = g.board(h, 10);
    for (const p of g.pts(b)) {
      const parent = g.key(g.canonical(b ^ (1n << BigInt(p))));
      if (obligations.has(parent)) covered.add(parent);
    }
  }
  need(covered.size === obligations.size, 'S9 obligation uncovered by certified S10 leaves');
  return {s8Roots: roots.length, s9ClassEdges: edges,
    s9DistinctObligations: obligations.size, s10CertifiedLeaves: leaves.length,
    coveredObligations: covered.size};
}
function certifiedWin8() {
  const old = oldCert(), gap = gapCert();
  const paths = [
    'n11-s9-win29-lift-20261023/s9-win29.keys',
    'n11-s9-win27-expansion-20261024/s9-win27.keys',
    'n11-s9-win2-followup-20261024/s9-win2.keys',
    'n11-s9-win10-20261024/s9-win10.keys',
    'n11-s9-win7-expansion-20261024/s9-win7.keys',
    'n11-s9-win20-neighbor-20261024/s9-win20.keys',
    'n11-s8-frontier-13way-20261024/s9-win7.keys'
  ];
  const s9 = unique([...paths.flatMap(keys), ...old.new_s9_win, ...BATCH8, ...LEGACY3]);
  need(s9.size === 131, 'certified S9 WIN sources changed');
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
  const four = JSON.parse(read('n11-s7-four-win-terminal-20261020/s7_win_four_min_certificate.json'));
  for (const h of Object.keys(four.s8_witness)) win8.add(h);
  for (const line of read('n11-s7-fifth-terminal-20261015/fifth-s7-win-terminal.cert').split(/\r?\n/))
    if (line.startsWith('EDGE ')) win8.add(line.split(' ')[1]);
  for (const row of gap.s8_win_roots) win8.add(row.root);
  need(win8.size === 1326, 'certified S8 WIN union changed');
  return win8;
}
function audit() {
  const {roots, leaves} = extractCertificate();
  const source = boundary(roots, leaves);
  const old = oldCert(), gap = gapCert();
  const old8 = unique([
    ...keys('n11-s8-compact385-pruned1946-20261020/loss_roots35.txt'),
    ...old.s8_loss, gap.s8_loss_root,
    '00000000000040001000044400830000',
    ...keys('n11-four-s8-joint-terminal52-20261023/roots4.keys')
  ]);
  need(old8.size === 44 && roots.every(h => !old8.has(h)), 'old S8 LOSS roots overlap');
  const win8 = certifiedWin8();
  const frozenWin8 = unique(keys('n11-targeted-terminal-lift-20261015/data/lifted_s8_win_51571.txt'));
  const frozenLoss8 = unique(keys('n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'));
  need(frozenWin8.size === 13501 && frozenLoss8.size === 294, 'frozen S8 comparison changed');
  need(roots.every(h => !win8.has(h) && !frozenWin8.has(h) && frozenLoss8.has(h)),
    'S8 WIN/LOSS conflict or frozen provenance mismatch');
  const old7 = g.reverse(old8), new7 = g.reverse(roots);
  const all7 = unique([...old7, ...new7]);
  const added7 = [...new7].filter(h => !old7.has(h)).sort();
  need(old7.size === 311 && new7.size === 223 && added7.length === 223 &&
    all7.size === 534, 'S7 reverse closure changed');
  const frozenWin7 = unique(keys('n11-targeted-terminal-lift-20261015/data/all_s7_win_17.txt'));
  const frozenLoss7 = unique(keys('n11-targeted-terminal-lift-20261015/data/all_s7_loss_2232.txt'));
  need(frozenWin7.size === 17 && frozenLoss7.size === 2232 &&
    added7.every(h => !frozenWin7.has(h) && frozenLoss7.has(h)),
    'S7 WIN/LOSS conflict or frozen provenance mismatch');
  const old6 = g.reverse(old7), new6 = g.reverse(new7), all6 = g.reverse(all7);
  const added6 = [...all6].filter(h => !old6.has(h)).sort();
  need(old6.size === 944 && new6.size === 709 && added6.length === 709 &&
    all6.size === 1653, 'S6 reverse closure changed');
  need(added7.join('\n') + '\n' ===
    read('n11-s6-legacy29-union-20261025/s7-loss223.keys'),
    'S7 manifest mismatch');
  need(added6.join('\n') + '\n' ===
    read('n11-s6-legacy29-union-20261025/s6-parents709.keys'),
    'S6 manifest mismatch');
  let totalEdges = 0, securedEdges = 0, minGap = Infinity;
  const closed = [];
  for (const h of all6) {
    const children = g.children(g.board(h, 6));
    const secured = [...children].filter(c => all7.has(c)).length;
    totalEdges += children.size;
    securedEdges += secured;
    const missing = children.size - secured;
    minGap = Math.min(minGap, missing);
    if (missing === 0) closed.push(h);
  }
  need(totalEdges === 128009 && securedEdges === 3738 && minGap === 0 &&
    closed.length === 1 && closed[0] === '00000000040004001004000004010000',
    'S6 complete-child coverage changed');
  const s5Parents = g.reverse(closed);
  need(s5Parents.size === 6, 'six certified S5 LOSS parents changed');
  return {...source, previousS8Loss: old8.size, totalS8Loss: old8.size + roots.length,
    previousS7Loss: old7.size, addedS7Loss: added7.length, totalS7Loss: all7.size,
    previousS6Parents: old6.size, addedS6Parents: added6.length, totalS6Parents: all6.size,
    previousSecuredS6Edges: 2177, securedS6Edges: securedEdges,
    addedSecuredS6Edges: securedEdges - 2177, allS6LegalEdges: totalEdges,
    closedS6: closed, knownS5LossParents: s5Parents.size,
    newlyDiscoveredS6Verdicts: 0, newTwoStoneClosures: 0, emptyBoard: 'UNKNOWN'};
}
if (require.main === module) {
  console.log(JSON.stringify(audit(), null, 2));
  if (process.argv.includes('--negative')) {
    const {roots, leaves} = extractCertificate();
    const tests = [
      () => boundary(roots.slice(1), leaves),
      () => boundary([roots[0], ...roots.slice(0, 28)], leaves),
      () => boundary(roots, leaves.slice(1)),
      () => boundary(roots, [roots[0], ...leaves.slice(1)])
    ];
    for (const test of tests) {
      let rejected = false;
      try { test(); } catch (_) { rejected = true; }
      need(rejected, 'tampered source certificate accepted');
    }
    console.error('PASS four malformed-certificate rejections');
  }
}
module.exports = {audit, boundary, extractCertificate, certifiedWin8};
