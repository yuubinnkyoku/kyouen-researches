#!/usr/bin/env node
'use strict';
// Cross-snapshot S5 evidence reuse, not an independent terminal minimax proof.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const ROOT = path.resolve(__dirname, '../../..');
const HERE = __dirname;
const MANIFEST = JSON.parse(fs.readFileSync(path.join(HERE, 'manifest.json'), 'utf8'));
const LOSS6_PATH = 'research/experiments/n11-boundary-recovery-20261006/output/post-d5136a93-saved-s6-loss-cache-projection.csv';
const LOSS6_BLOB = '9d4c4d56e0b8a3ebfaea5271dbaf7895e79ab175';
const CERTIFIED_LOSS6 = '00000000040004001004000004010000';
function need(x, msg) { if (!x) throw Error(msg); }
function pinned(spec) {
  const raw = fs.readFileSync(path.join(ROOT, spec.path));
  const sha = crypto.createHash('sha1')
    .update(Buffer.from('blob ' + raw.length + '\0')).update(raw).digest('hex');
  need(sha === spec.gitBlob, 'pinned Git blob changed: ' + spec.path);
  return raw.toString('utf8');
}
function points(k) {
  need(/^[0-9a-f]{32}$/.test(k), 'invalid key: ' + k);
  const n = BigInt('0x' + k);
  need(n >> 121n === 0n, 'out-of-board key: ' + k);
  const p = [];
  for (let i = 0; i < 121; i++) if ((n >> BigInt(i)) & 1n) p.push(i);
  return p;
}
const maps = Array.from({length:8}, (_,mode) =>
  Array.from({length:121}, (_,i) => {
    const x=i%11, y=Math.floor(i/11);
    const [u,v]=[[x,y],[10-y,x],[10-x,10-y],[y,10-x],
      [10-x,y],[10-y,10-x],[x,10-y],[y,x]][mode];
    return 11*v+u;
  }));
function canonical(p) {
  let best = null;
  for (const m of maps) {
    let b = 0n;
    for (const x of p) b |= 1n << BigInt(m[x]);
    if (best === null || b < best) best = b;
  }
  return best.toString(16).padStart(32,'0');
}
// A second geometry formula: full 4x4 determinant, not the difference
// determinant used by the existing S6 cross-source verifier.
function determinant(a) {
  let ans=0;
  function perm(depth,used,prod,sign) {
    if(depth===4) { ans += sign*prod; return; }
    for(let j=0;j<4;j++) if(!(used & (1<<j))) {
      let inversions=0;
      for(let k=j+1;k<4;k++) if(used & (1<<k)) inversions++;
      perm(depth+1,used|(1<<j),prod*a[depth][j],
        inversions%2 ? -sign : sign);
    }
  }
  perm(0,0,1,1);
  return ans;
}
function safe(p) {
  for(let a=0;a<p.length;a++)
    for(let b=a+1;b<p.length;b++)
      for(let c=b+1;c<p.length;c++)
        for(let d=c+1;d<p.length;d++) {
          const rows=[p[a],p[b],p[c],p[d]].map(i=>{
            const x=i%11,y=Math.floor(i/11);
            return [x*x+y*y,x,y,1];
          });
          if(determinant(rows)===0) return false;
        }
  return true;
}
function checkBoard(k,n) {
  const p=points(k);
  need(p.length===n && canonical(p)===k && safe(p),
    'unsafe, noncanonical or wrong-size board: ' + k);
  return p;
}
function parseCache(raw) {
  const cache=new Map();
  for(const line of raw.split(/\r?\n/)) {
    if(!line || line.startsWith('#')) continue;
    const f=line.split(',');
    need(f.length===6 && f[0]==='s5verdict' && f[3]==='5' &&
      (f[4]==='1'||f[4]==='2') && /^\d+$/.test(f[5]),
      'malformed exact S5 cache row');
    const lo=BigInt(f[1]),hi=BigInt(f[2]);
    need(lo>=0n && lo<(1n<<64n) && hi>=0n && hi<(1n<<64n),
      'invalid 64-bit key halves');
    const k=(lo+(hi<<64n)).toString(16).padStart(32,'0');
    checkBoard(k,5);
    need(!cache.has(k), 'duplicate S5 key: ' + k);
    cache.set(k,Number(f[4]));
  }
  return cache;
}
function parents(k) {
  const p=checkBoard(k,5), out=new Set();
  for(const x of p) out.add(canonical(p.filter(y=>x!==y)));
  return out;
}
function validateWitness(row, corpus) {
  need(corpus.get(row.win5)===1,
    'S4 WIN witness is not a corpus WIN5: ' + row.win5);
  checkBoard(row.s4,4);
  need(parents(row.win5).has(row.s4),
    'S4 is not a legal deletion parent of WIN5: ' + row.s4);
}
function compareCaches(frozen, corpus) {
  const extraWin=[], extraLoss=[], conflicts=[];
  for(const [k,v] of corpus) {
    if(frozen.has(k)) {
      if(frozen.get(k)!==v) conflicts.push(k);
    } else (v===1?extraWin:extraLoss).push(k);
  }
  need(conflicts.length===0, 'WIN/LOSS CONFLICT: ' + conflicts.join(','));
  return {extraWin:extraWin.sort(),extraLoss:extraLoss.sort()};
}
function main() {
  need(MANIFEST.schema==='n11-cross-snapshot-win5-to-win4-witness-v1' &&
    MANIFEST.outcome==='UNKNOWN', 'manifest schema/outcome changed');
  const frozen=parseCache(pinned(MANIFEST.provenance.frozen));
  const corpus=parseCache(pinned(MANIFEST.provenance.corpus));
  const count=(m,v)=>[...m.values()].filter(x=>x===v).length;
  need(frozen.size===5851 && count(frozen,1)===159 &&
    count(frozen,2)===5692 && corpus.size===5700 &&
    count(corpus,1)===151 && count(corpus,2)===5549,
    'snapshot inventories changed');
  const delta=compareCaches(frozen,corpus);
  const expectedExtraWin=[
    '00000000000000809100000000000800',
    '00000000200000001000040200010000'];
  need(JSON.stringify(delta.extraWin)===JSON.stringify(expectedExtraWin) &&
    delta.extraLoss.length===0, 'cross-snapshot delta changed');
  const oldWin4=new Map(), combinedWin4=new Map();
  for(const [k,v] of frozen) if(v===1) for(const p of parents(k))
    oldWin4.set(p,k);
  for(const [k,v] of frozen) if(v===1) for(const p of parents(k))
    combinedWin4.set(p,k);
  for(const k of delta.extraWin) for(const p of parents(k))
    combinedWin4.set(p,k);
  const newWin4=[...combinedWin4].filter(([p])=>!oldWin4.has(p))
    .map(([s4,win5])=>({s4,win5})).sort((a,b)=>a.s4.localeCompare(b.s4));
  need(oldWin4.size===549 && combinedWin4.size===555 &&
    newWin4.length===6, 'S4 WIN witness coverage changed');
  const reps=[16,38,49,24,0,26,48,12,25,3,13,2,14,5,15,4,1,37,36];
  const rows=newWin4.map(({s4,win5})=>{
    const p=checkBoard(s4,4),center=p.includes(60);
    return {s4,win5,center,openingReps:center ?
      reps.filter(r=>p.some(x=>maps.some(m=>m[r]===x))) : []};
  });
  need(JSON.stringify(rows)===JSON.stringify(MANIFEST.rows),
    'manifest is not the exact derived S4 WIN witness set');
  for(const row of MANIFEST.rows) validateWitness(row,corpus);
  need(rows.filter(r=>r.center).length===4 &&
    new Set(rows.flatMap(r=>r.openingReps)).size===5,
    'central opening incidence changed');
  // Existing LOSS5 delta improves 112 other S4 classes. Do not claim
  // these six WIN4 witnesses prune those 112 if their sets are disjoint.
  const raw=pinned({path:LOSS6_PATH,gitBlob:LOSS6_BLOB});
  const loss6=new Set();
  for(const line of raw.trim().split(/\r?\n/)) {
    if(line.startsWith('#') || !line) continue;
    const f=line.split(',');
    need(f.length===11 && f[0]==='replay' && f[2]==='6' &&
      f[4]==='1' && f[5]==='0' && f[6]==='2',
      'malformed historical LOSS6 row');
    const k=(BigInt(f[9])+(BigInt(f[10])<<64n)).toString(16).padStart(32,'0');
    checkBoard(k,6);
    need(!loss6.has(k),'duplicate historical LOSS6');
    loss6.add(k);
  }
  need(loss6.size===172 && !loss6.has(CERTIFIED_LOSS6),
    'LOSS6 source overlap changed');
  loss6.add(CERTIFIED_LOSS6);
  const loss5=new Set();
  for(const k of loss6) {
    const p=checkBoard(k,6);
    for(const x of p) loss5.add(canonical(p.filter(y=>x!==y)));
  }
  const extraLoss5=[...loss5].filter(k=>!frozen.has(k));
  const extraLoss4Parents=new Set();
  for(const k of extraLoss5) for(const p of parents(k))
    extraLoss4Parents.add(p);
  const overlap=newWin4.filter(r=>extraLoss4Parents.has(r.s4));
  need(loss5.size===903 && extraLoss5.length===30 &&
    extraLoss4Parents.size===112 && overlap.length===0,
    'S4 LOSS-candidate overlap changed');
  // Negative controls exercise the actual conflict and witness guards.
  const forged=new Map(corpus);
  forged.set(delta.extraWin[0],2);
  assert.throws(()=>compareCaches(frozen,forged), /WIN\/LOSS CONFLICT|cross-snapshot delta changed/);
  assert.throws(()=>validateWitness(
    {s4:rows[0].s4,win5:[...frozen].find(([,v])=>v===2)[0]},corpus),
    /not a corpus WIN5/);
  assert.throws(()=>validateWitness(
    {s4:rows[0].s4,win5:rows[1].win5},corpus),
    /not a legal deletion parent/);
  const report={
    schema:MANIFEST.schema, frozenS5:frozen.size,corpusS5:corpus.size,
    importedWIN5:delta.extraWin.length, importedLOSS5:delta.extraLoss.length,
    conflicts:0, combinedS5:frozen.size+delta.extraWin.length,
    frozenWin4:oldWin4.size, combinedWin4:combinedWin4.size,
    additionalWin4RelativeToFrozen:newWin4.length,
    centralAdditionalWin4:4, affectedUnresolvedOpeningOrbits:5,
    overlapsPrior112S4LossCoverageCandidates:overlap.length,
    independentlyVerifiedWitnessIncidence:rows.length,
    trust:'solver-trusted exact S5 labels; independent 4x4 geometry and D4; no terminal replay',
    twoStoneRootClosed:false,emptyBoard:'UNKNOWN'};
  console.log(JSON.stringify(report,null,2));
}
main();
