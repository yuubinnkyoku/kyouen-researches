#!/usr/bin/env node
'use strict';
// Cross-source conflict audit only. Historical S6 cache LOSS entries are not
// promoted to terminal certificates by this check.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../../..');
const sources = {
  win7: ['research/experiments/n11-targeted-terminal-lift-20261015/data/all_s7_win_17.txt',
         '677e962f3f70be73abcd77037df8822880927b22'],
  lift: ['research/experiments/n11-s8-fixed37-terminal-closure-20261030/lift_result.json',
         'f8e335cd8fafec9d98745e89cb207d4e31c220be'],
  loss6: ['research/experiments/n11-boundary-recovery-20261006/output/post-d5136a93-saved-s6-loss-cache-projection.csv',
          '9d4c4d56e0b8a3ebfaea5271dbaf7895e79ab175'],
};
const independentFirstWin7 = '00000000000100001000000042401008';
const independentlyCertifiedLoss6 = '00000000040004001004000004010000';
function need(ok, message) { if (!ok) throw Error(message); }
function pinned([file, sha]) {
  const raw = fs.readFileSync(path.join(root, file));
  const header = Buffer.from('blob ' + raw.length + '\0');
  const got = crypto.createHash('sha1').update(header).update(raw).digest('hex');
  need(got === sha, 'source Git blob changed: ' + file);
  return raw.toString('utf8');
}
function points(key) {
  need(/^[0-9a-f]{32}$/.test(key), 'invalid 128-bit board key');
  const mask = BigInt('0x' + key);
  need(mask >> 121n === 0n, 'outside 11x11');
  const out = [];
  for (let i = 0; i < 121; ++i) if ((mask >> BigInt(i)) & 1n) out.push(i);
  return out;
}
const maps = Array.from({length: 8}, (_, mode) =>
  Array.from({length: 121}, (_, i) => {
    const x = i % 11, y = Math.floor(i / 11);
    const [a,b] = [[x,y], [10-y,x], [10-x,10-y], [y,10-x],
                   [10-x,y], [10-y,10-x], [x,10-y], [y,x]][mode];
    return 11*b+a;
  }));
function canonical(ps) {
  let best = null;
  for (const map of maps) {
    let mask = 0n;
    for (const p of ps) mask |= 1n << BigInt(map[p]);
    if (best === null || mask < best) best = mask;
  }
  return best.toString(16).padStart(32, '0');
}
function forbidden(a,b,c,d) {
  const x=d%11, y=Math.floor(d/11);
  const r=[a,b,c].map(i=>{
    const u=i%11, v=Math.floor(i/11);
    return [u-x,v-y,u*u+v*v-x*x-y*y];
  });
  const [A,B,C]=r;
  return A[0]*(B[1]*C[2]-B[2]*C[1])
       - A[1]*(B[0]*C[2]-B[2]*C[0])
       + A[2]*(B[0]*C[1]-B[1]*C[0]) === 0;
}
function safe(ps) {
  for(let a=0;a<ps.length;a++)
    for(let b=a+1;b<ps.length;b++)
      for(let c=b+1;c<ps.length;c++)
        for(let d=c+1;d<ps.length;d++)
          if(forbidden(ps[a],ps[b],ps[c],ps[d])) return false;
  return true;
}
function checkBoard(key, count) {
  const ps=points(key);
  need(ps.length===count && canonical(ps)===key && safe(ps),
       'unsafe, noncanonical or wrong-size board: '+key);
  return ps;
}
function lossCacheKeys(text) {
  const lines=text.trim().split(/\r?\n/).filter(s=>s && !s.startsWith('#'));
  const out=[];
  for(let i=0;i<lines.length;i++) {
    const f=lines[i].split(',');
    need(f.length===11 && f[0]==='replay' && f[1]===String(i) &&
         f[2]==='6' && f[4]==='1' && f[5]==='0' && f[6]==='2',
         'unexpected exact-cache projection row '+i);
    const lo=BigInt(f[9]),hi=BigInt(f[10]);
    need(lo>=0n && lo<(1n<<64n) && hi>=0n && hi<(1n<<64n),
         'invalid S6 bitmask halves');
    out.push((lo+(hi<<64n)).toString(16).padStart(32,'0'));
  }
  need(out.length===172 && new Set(out).size===172,
       'historical S6 cache count/uniqueness changed');
  out.forEach(h=>checkBoard(h,6));
  return new Set(out);
}
function audit(win7, cacheLoss6) {
  need(win7.length===19 && new Set(win7).size===19,
       'expected 17 historical and two independently backed WIN7 roots');
  const win6=new Set();
  for(const h of win7) {
    const ps=checkBoard(h,7);
    for(const removed of ps) {
      const key=canonical(ps.filter(p=>p!==removed));
      checkBoard(key,6);
      win6.add(key);
    }
  }
  need(win6.size===117,'WIN6 reverse incidence changed');
  checkBoard(independentlyCertifiedLoss6,6);
  need(!cacheLoss6.has(independentlyCertifiedLoss6),
       'historical cache/certified S6 LOSS overlap changed');
  const comparisonLoss6=new Set([...cacheLoss6,independentlyCertifiedLoss6]);
  const conflicts=[...win6].filter(h=>comparisonLoss6.has(h));
  need(conflicts.length===0,'WIN6/LOSS6 CONFLICT: '+conflicts.join(','));
  return {win7Witnesses:win7.length,securedWin6:win6.size,
    historicalCacheLoss6:cacheLoss6.size,terminalCertifiedLoss6:1,
    comparisonLoss6:comparisonLoss6.size,winLossConflicts:conflicts.length,
    historicalCacheTrustBoundary:'hash-pinned exact solver cache projection; not terminal-replayed here',
    proofTrustBoundary:'S7 WIN7 certificates are independently checked by existing pipelines, not replayed here',
    twoStoneRootClosed:false,emptyBoard:'UNKNOWN'};
}
function main() {
  const old=pinned(sources.win7).trim().split(/\r?\n/);
  need(old.length===17 && old.join('\n')===[...new Set(old)].sort().join('\n'),
       'historical WIN7 list malformed');
  const lift=JSON.parse(pinned(sources.lift));
  need(lift.schema==='n11-fixed14-direct37-s7-lift-v1' &&
       lift.sourceFixed37==='n11-fixed14-37-s8-direct-terminal-v1' &&
       lift.win7===13 && lift.loss7===1 && lift.unknown7===0 &&
       lift.emptyBoard==='UNKNOWN' && lift.winLossConflicts===0,
       'fixed14 S7 lift provenance changed');
  const firstWin=lift.rows.filter(r=>r.verdict==='LOSS').map(r=>r.s7);
  need(firstWin.length===1 &&
       firstWin[0]==='00020000000000821080200000000020',
       'S7 side-to-move polarity changed');
  const win7=[...old,...firstWin,independentFirstWin7];
  const cacheLoss6=lossCacheKeys(pinned(sources.loss6));
  const result=audit(win7,cacheLoss6);
  // Exercise the actual conflict check, not merely compare fixture strings.
  const forged=new Set(cacheLoss6);
  forged.delete(forged.values().next().value);
  const ps=points(win7[0]);
  forged.add(canonical(ps.filter(p=>p!==ps[0])));
  let rejected=false;
  try { audit(win7,forged); } catch(e) {
    need(e.message.includes('WIN6/LOSS6 CONFLICT'), 'wrong negative-test failure: '+e);
    rejected=true;
  }
  need(rejected,'forged WIN6-as-LOSS6 cache row was accepted');
  console.log(JSON.stringify(result,null,2));
}
if(require.main===module) main();
module.exports={audit,lossCacheKeys};
