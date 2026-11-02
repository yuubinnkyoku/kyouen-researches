#!/usr/bin/env node
'use strict';
// Independent 3x3 integer-geometry cross-inventory audit of the repaired
// central49 46-S6 / 1980-S7 conditional cover. This is NOT a verdict proof.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../../..');
const here = 'research/experiments/n11-central-19-cover-20261031/';
const files = {
  source: [here + 'conditional_s6_cover_46_exclude_certified_win6.json', '4b195bf055b1ef1f557e1c5f4d40556111f8a39c'],
  swaps: [here + 'conditional_s6_cover_46_repaired_1980_swaps.txt', '67cb49278ff068e163d793baaf6bacf78ab90e5d'],
  loss7: ['research/experiments/n11-targeted-terminal-lift-20261015/data/all_s7_loss_2232.txt', 'e2b8fc243422751ce048302a3ed65df1ef7e5211'],
  win7: ['research/experiments/n11-targeted-terminal-lift-20261015/data/all_s7_win_17.txt', '677e962f3f70be73abcd77037df8822880927b22'],
  lift: ['research/experiments/n11-s8-fixed37-terminal-closure-20261030/lift_result.json', 'f8e335cd8fafec9d98745e89cb207d4e31c220be'],
  loss6: ['research/experiments/n11-boundary-recovery-20261006/output/post-d5136a93-saved-s6-loss-cache-projection.csv', '9d4c4d56e0b8a3ebfaea5271dbaf7895e79ab175'],
  loss8Roots35: ['research/experiments/n11-s8-to-s7-lift238-20261020/roots35.txt', '0e95f941079f256968d72988192a3ca3b55293ec'],
  loss8Cert3: ['research/experiments/n11-s7-terminal-loss12-20261024/certificate.json', '5fa68e34b178f25dac4c4619310199ea75df5812'],
  newWin6: [here + 'shared58_s6_win_strategy.cert', 'a24ee0c9633331671003576a825e070535abd295'],
};
function need(ok, message) { if (!ok) throw Error(message); }
function pinned([name, expected]) {
  const bytes = fs.readFileSync(path.join(root, name));
  const sha = crypto.createHash('sha1')
    .update(Buffer.from('blob ' + bytes.length + '\0')).update(bytes).digest('hex');
  need(sha === expected, 'input Git blob changed: ' + name);
  return bytes.toString('utf8');
}
function keyOf(mask) { return mask.toString(16).padStart(32, '0'); }
function points(key, n) {
  need(/^[0-9a-f]{32}$/.test(key), 'bad 128-bit key');
  const m = BigInt('0x' + key);
  need(m >> 121n === 0n, 'off-board bit');
  const out = [];
  for (let p = 0; p < 121; ++p) if ((m >> BigInt(p)) & 1n) out.push(p);
  need(out.length === n, 'wrong stone count: ' + key);
  return out;
}
const maps = Array.from({length: 8}, (_, mode) =>
  Array.from({length: 121}, (_, p) => {
    const x = p % 11, y = Math.floor(p / 11);
    const [a,b] = [[x,y],[10-y,x],[10-x,10-y],[y,10-x],
                   [10-x,y],[10-y,10-x],[x,10-y],[y,x]][mode];
    return a + 11*b;
  }));
function canonical(ps) {
  let best = null;
  for (const map of maps) {
    let mask = 0n;
    for (const p of ps) mask |= 1n << BigInt(map[p]);
    if (best === null || mask < best) best = mask;
  }
  return keyOf(best);
}
// 3x3 difference determinant, distinct from the 4x4 Bareiss swap verifier.
function forbidden(a,b,c,d) {
  const x = d % 11, y = Math.floor(d / 11);
  const [A,B,C] = [a,b,c].map(p => {
    const u = p % 11, v = Math.floor(p / 11);
    return [u-x, v-y, u*u+v*v-x*x-y*y];
  });
  return A[0]*(B[1]*C[2]-B[2]*C[1])
       - A[1]*(B[0]*C[2]-B[2]*C[0])
       + A[2]*(B[0]*C[1]-B[1]*C[0]) === 0;
}
function triples(ps) {
  const out = [];
  for (let i=0;i<ps.length;i++)
    for (let j=i+1;j<ps.length;j++)
      for (let k=j+1;k<ps.length;k++) out.push([ps[i],ps[j],ps[k]]);
  return out;
}
function safe(ps) {
  for (let i=0;i<ps.length;i++)
    for (let j=i+1;j<ps.length;j++)
      for (let k=j+1;k<ps.length;k++)
        for (let l=k+1;l<ps.length;l++)
          if (forbidden(ps[i],ps[j],ps[k],ps[l])) return false;
  return true;
}
function selected(source, swaps) {
  const doc = JSON.parse(source);
  need(doc.schema === 'n11-central49-conditional46-repaired-exclude-certified-win6-v1'
       && doc.evidence_level === 'GEOMETRY_ONLY_CONDITIONAL_REPAIR_NOT_S6_LOSS'
       && Object.values(doc.outcomes).every(v => v === 'UNKNOWN'),
       'conditional source provenance/polarity changed');
  const initial = doc.selected_s6_classes;
  need(initial.length === 46 && initial.join() === [...new Set(initial)].sort().join(),
       'invalid initial 46-S6 list');
  const current = new Set(initial);
  const lines = swaps.trim().split(/\r?\n/);
  need(lines.length === 23 && lines[0] === '# n11-central49-repaired-46-s6-18-two-swap-v1'
       && lines[2].includes('s6:UNKNOWN'), 'wrong swap chain');
  for (const [index,line] of lines.slice(5).entries()) {
    const f = line.split(/\s+/);
    need(f.length === 6 && f.slice(0,2).join() === f.slice(0,2).sort().join()
         && f.slice(2,4).join() === f.slice(2,4).sort().join(),
         'malformed swap ' + index);
    need(f[0] !== f[1] && f[2] !== f[3] && current.delete(f[0])
         && current.delete(f[1]) && !current.has(f[2]) && !current.has(f[3]),
         'invalid swap membership ' + index);
    current.add(f[2]); current.add(f[3]);
    need(current.size === 46, 'changed witness count');
  }
  need(!current.has(doc.excluded_certified_win6), 'refuted WIN6 was selected');
  return [...current].sort();
}
function s7Inventory(text, n) {
  const lines = text.trim().split(/\r?\n/);
  need(lines.length === n && lines.join() === [...new Set(lines)].sort().join(),
       'invalid S7 inventory');
  for (const key of lines) {
    const ps = points(key,7);
    need(canonical(ps) === key && safe(ps), 'bad S7 inventory key');
  }
  return new Set(lines);
}
function oldLoss6(text) {
  const lines = text.trim().split(/\r?\n/).filter(x => !x.startsWith('#'));
  need(lines.length === 172, 'historical LOSS6 count changed');
  const out = new Set();
  for (let i=0;i<lines.length;i++) {
    const f = lines[i].split(',');
    need(f.length === 11 && f[0] === 'replay' && f[1] === String(i)
         && f[2] === '6' && f[4] === '1' && f[5] === '0' && f[6] === '2',
         'unexpected historical LOSS6 format');
    const lo = BigInt(f[9]), hi = BigInt(f[10]);
    need(lo>=0n && hi>=0n && lo < (1n<<64n) && hi < (1n<<64n),
         'invalid cache mask');
    const k = keyOf(lo + (hi<<64n));
    const ps = points(k,6);
    need(canonical(ps) === k && safe(ps), 'invalid cached S6');
    out.add(k);
  }
  need(out.size === 172, 'duplicate cached S6');
  return out;
}
function checkNoWinConflicts(frontier, win7) {
  const conflicts = [...frontier].filter(k => win7.has(k));
  need(conflicts.length === 0, 'known WIN7 conflicts: ' + conflicts.join(','));
}
function audit() {
  const data = Object.fromEntries(Object.entries(files).map(([k,v]) => [k,pinned(v)]));
  const witnesses = selected(data.source, data.swaps);
  // This script is a geometric cross-audit, not a substitute for the
  // independent 4x4 full-terminal verifier of the pinned WIN strategy.
  need(crypto.createHash('sha256').update(data.newWin6).digest('hex')
       === '10e816538fbe6cc0062e2d0dd0fe96930ef294101812701305e1595b531b21da'
       && data.newWin6.startsWith('# n11-original-first-WIN-strategy-v1\nBOARD 11\nROOT 00000000000000203808200000000000\n'),
       'new WIN6 certificate identity changed');
  const cacheLoss7 = s7Inventory(data.loss7,2232);
  const historicalWin7 = s7Inventory(data.win7,17);
  const lift = JSON.parse(data.lift);
  need(lift.schema === 'n11-fixed14-direct37-s7-lift-v1'
       && lift.rows.length === 14 && lift.win7 === 13 && lift.loss7 === 1
       && lift.unknown7 === 0 && lift.winLossConflicts === 0,
       'fixed14 lift provenance changed');
  const terminalLoss7 = new Set(lift.rows.filter(r => r.verdict === 'WIN').map(r => r.s7));
  const extraWin7 = '00000000000100001000000042401008';
  need(canonical(points(extraWin7,7)) === extraWin7 && safe(points(extraWin7,7)),
       'independent 2026-10-26 WIN7 geometry changed');
  const win7 = new Set([...historicalWin7,
    ...lift.rows.filter(r => r.verdict === 'LOSS').map(r => r.s7), extraWin7]);
  need(terminalLoss7.size === 13 && win7.size === 19
       && ![...terminalLoss7].some(k => cacheLoss7.has(k) || win7.has(k)),
       'terminal lift polarity or overlap changed');
  // Independent terminal-backed LOSS7 parents of 35+3 certified LOSS8 roots.
  const roots35 = data.loss8Roots35.trim().split(/\r?\n/);
  const cert3 = JSON.parse(data.loss8Cert3);
  need(roots35.length === 35 && cert3.s8_loss.length === 3,
       'terminal LOSS8 root inventory changed');
  const roots8 = new Set([...roots35, ...cert3.s8_loss]);
  need(roots8.size === 38, 'duplicate terminal LOSS8 root');
  const terminalFromLoss8 = new Set();
  for (const k of roots8) {
    const ps = points(k,8);
    need(canonical(ps) === k && safe(ps), 'invalid terminal LOSS8 root');
    for (let i=0;i<8;i++) {
      const parent = canonical(ps.filter((_,j)=>j!==i));
      need(safe(points(parent,7)), 'unsafe LOSS8-to-LOSS7 parent');
      terminalFromLoss8.add(parent);
    }
  }
  need(terminalFromLoss8.size === 268, 'terminal LOSS8 reverse closure changed');
  const cacheLoss6 = oldLoss6(data.loss6);
  need(!witnesses.some(k => cacheLoss6.has(k) || k === '00000000040004001004000004010000'),
       'historical or terminal LOSS6 overlap changed');

  const incidence = new Map(), local = [];
  let edges = 0;
  for (const k of witnesses) {
    const ps = points(k,6);
    need(canonical(ps) === k && safe(ps), 'bad selected S6');
    const ts = triples(ps), child = new Set();
    for (let p=0;p<121;p++) {
      if (ps.includes(p) || ts.some(t => forbidden(t[0],t[1],t[2],p))) continue;
      child.add(canonical([...ps,p]));
    }
    edges += child.size;
    for (const c of child) incidence.set(c,(incidence.get(c)||0)+1);
    local.push({s6:k,children:child});
  }
  const frontier = new Set(incidence.keys());
  const newWin6A = '00000000000000203808200000000000';
  const newWin6B = '0000000000000020380c000000000000';
  const win7A = canonical([...points(newWin6A,6),70]);
  const win7B = canonical([...points(newWin6B,6),75]);
  need(witnesses.includes(newWin6A) && witnesses.includes(newWin6B)
       && win7A === win7B && frontier.has(win7A)
       && incidence.get(win7A) === 2,
       'new terminal WIN7 does not refute two selected S6 witnesses');
  const terminalFromLoss8Hits = [...frontier].filter(k => terminalFromLoss8.has(k));
  need(terminalFromLoss8Hits.length === 0,
       'repaired frontier overlaps independently certified LOSS8 reverse closure');
  checkNoWinConflicts(frontier,win7);
  const hist = {};
  for (const n of incidence.values()) hist[n] = (hist[n]||0)+1;
  need(edges === 2972 && frontier.size === 1980
       && hist[1] === 988 && hist[2] === 992 && Object.keys(hist).length === 2,
       'repaired frontier count/multiplicity mismatch');
  const cached = [...frontier].filter(k => cacheLoss7.has(k));
  const terminal = [...frontier].filter(k => terminalLoss7.has(k));
  need(cached.length === 6 && terminal.length === 0,
       'known LOSS7 cache overlap changed');
  const stats = local.map(({s6,children}) => ({
    s6, children:children.size,
    shared:[...children].filter(k => incidence.get(k) > 1).length,
    cacheLoss7:[...children].filter(k => cacheLoss7.has(k)).length
  }));
  const shortest = [...stats].sort((a,b)=>a.children-b.children || a.s6.localeCompare(b.s6))[0];
  const shortShared = [...stats].filter(s => s.shared >= 50)
    .sort((a,b)=>a.children-b.children || b.shared-a.shared || a.s6.localeCompare(b.s6))[0];
  need(shortest.s6 === '00000000000200801002000081000000'
       && shortest.children === 55 && shortest.shared === 0
       && shortShared.s6 === '00000000000000203808200000000000'
       && shortShared.children === 58 && shortShared.shared === 53,
       'focus candidates changed');
  const perWitnessCached = stats.reduce((s,x)=>s+x.cacheLoss7,0);
  need(perWitnessCached === 11, 'cached S7 edge multiplicity changed');
  // Negative tests exercise actual guards without changing source artifacts.
  let rejected = 0;
  for (const test of [
    () => selected(data.source, data.swaps.replace(/00000000000000805082002000000000/,
                                                 'ffffffffffffffffffffffffffffffff')),
    () => checkNoWinConflicts(frontier,new Set([frontier.values().next().value])),
    () => s7Inventory(data.loss7 + '\n' + cached[0],2232),
    () => oldLoss6(data.loss6.replace('replay,0,','replay,1,'))
  ]) {
    try { test(); } catch (e) { rejected++; continue; }
    throw Error('tampered input accepted');
  }
  need(rejected === 4, 'negative tests did not run');
  return {
    schema:'n11-central49-repaired1980-s7-cross-inventory-audit-v2',
    selectedS6:46,rawS7Edges:edges,distinctS7:frontier.size,
    s7Multiplicity:hist,sharedS7:hist[2],uniqueS7:hist[1],
    historicalSolverTrustedLoss7Hits:cached.length,
    historicalSolverTrustedLoss7EdgeHits:perWitnessCached,
    terminalBackedLoss7Hits:terminal.length,
    terminalBackedLoss7From38Loss8Roots:terminalFromLoss8.size,
    terminalBackedLoss7From38Loss8Hits:terminalFromLoss8Hits.length,
    knownWin7Conflicts:0,historicalLoss6WitnessOverlap:0,
    newlyCertifiedWin7FrontierHits:1,certifiedWin7Key:win7A,
    certifiedWin6Witnesses:[newWin6A,newWin6B],
    conditionalLossCover:'REFUTED_BY_TWO_TERMINAL_WIN6',
    noHitInTheseInventories:frontier.size-cached.length-terminal.length,
    noHitIncludingNewCertifiedWin7:frontier.size-cached.length-terminal.length-1,
    shortestS6:shortest,shortestS6WithAtLeast50SharedChildren:shortShared,
    negativeTests:rejected,proofBoundary:'GEOMETRY_CACHE_REUSE_AND_PINNED_CERTIFICATE_IDENTITY',
    s6Outcome:'TWO_CERTIFIED_WIN_44_UNKNOWN',twoStoneRootOutcome:'UNKNOWN',emptyBoardOutcome:'UNKNOWN'
  };
}
console.log(JSON.stringify(audit(),null,2));
