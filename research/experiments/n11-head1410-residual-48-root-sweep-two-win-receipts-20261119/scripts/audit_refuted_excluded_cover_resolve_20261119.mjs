// Receipt-aware exact cover RE-SOLVE for the five-parent head-1410 target union after
// the 48-root depth-10 sweep: the 46 REFUTED-D10 witnesses are struck from the
// candidate pool, the three published WIN7-D10 receipt roots (first + second/third)
// become known-WIN and their closed target rows leave the residual, and a fresh
// minimum candidate cover is recomputed over the 91 residual target rows.
// Base structure mirrors audit_five_parent_residual_49_cover_20261119.mjs.
// Usage: node audit_refuted_excluded_cover_resolve_20261119.mjs
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(SCRIPT_DIR, '../../../..');
const OUT = path.resolve(SCRIPT_DIR, '../output');
function need(ok, m) { if (!ok) throw new Error(m); }
const gitBlobSha = b => crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob ' + b.length), Buffer.from([0]), b])).digest('hex');
const PIN = {
  joint: ['research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-parent-cover-sharing-cost16-20261118.json', '40581746dc3304bdaff4b1934fd6f1d3d2981ea5'],
  audit: ['research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-cover-cost16-five-parent-independent-audit-20261118.json', '7cdc7c9ef341b5d9759923b3fc4986231c48895f'],
  head1476: ['research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/head1476-cost71e-full-universe-verdict-join-20261118.json', '65d0c7ce0200638a50db5451b11b8cb88ec64b5d'],
  globalFold: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-receipt-harvest-global-fold-20261118.json', '753a4bf4d0e11bea894111f9fa43bcff5e9ab7dc'],
  fold78: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost78c-79c-receipts-recompute-20261118.json', '7e6144cc4bc92c34faa14bed3058cde64fb3880e'],
  cost78c: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost78c-inflight-20261117.json', '626409d50d0a7bb1b925ebecbff7dbee9adfa398'],
  cost79c: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost79c-inflight-20261118.json', '054923a47ea0387b25f734222c499e60c054109b'],
  cost73j: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73j-inflight-20261117.json', '74fc3417391e30cf4cff9c2ffce059dce529ed86'],
  firstFoldTarball: ['research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/first-win7-root-evidence-20261119.tar.gz', 'fa5f26a9dc9bd2fb8222aa8ba0431d7578043019'],
  sweep: ['research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/residual-48-root-depth10-sweep-20261119.json', null], // pinned at runtime below
  myFold: ['research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/second-third-win7-root-receipt-fold-20261119.json', null]
};
function readBytes(name) {
  const [rel, sha] = PIN[name];
  const bytes = fs.readFileSync(path.join(ROOT, rel));
  if (sha) need(gitBlobSha(bytes) === sha, 'input blob mismatch: ' + rel);
  return bytes;
}
function readJSON(name) { return JSON.parse(readBytes(name).toString('utf8')); }
PIN.sweep[1] = gitBlobSha(readBytes('sweep'));
PIN.myFold[1] = gitBlobSha(readBytes('myFold'));
function popcount(x) { let n = 0; while (x) { x &= x - 1n; n++; } return n; }
function transform(mask, t) {
  let out = 0n;
  for (let p = 0; p < 121; p++) if ((mask >> BigInt(p)) & 1n) {
    const x = p % 11, y = Math.floor(p / 11);
    let X, Y;
    if (t === 0) { X=x; Y=y; }
    else if (t === 1) { X=10-y; Y=x; }
    else if (t === 2) { X=10-x; Y=10-y; }
    else if (t === 3) { X=y; Y=10-x; }
    else if (t === 4) { X=10-x; Y=y; }
    else if (t === 5) { X=x; Y=10-y; }
    else if (t === 6) { X=y; Y=x; }
    else { X=10-y; Y=10-x; }
    out |= 1n << BigInt(11 * Y + X);
  }
  return out;
}
function canon(mask) {
  let best = null;
  for (let t = 0; t < 8; t++) { const z = transform(mask, t); if (best === null || z < best) best = z; }
  return best.toString(16).padStart(32, '0');
}
function det3(a, b, c) {
  const [x1,y1]=a, [x2,y2]=b, [x3,y3]=c;
  const q1=BigInt(x1*x1+y1*y1), q2=BigInt(x2*x2+y2*y2), q3=BigInt(x3*x3+y3*y3);
  return q1*BigInt(x2*y3-x3*y2) - q2*BigInt(x1*y3-x3*y1) + q3*BigInt(x1*y2-x2*y1);
}
function det4(a,b,c,d) { return det3(a,b,c)-det3(a,b,d)+det3(a,c,d)-det3(b,c,d); }
function maximumMatching(g) {
  const n=g.length, match=Array(n).fill(-1), p=Array(n), base=Array(n), used=Array(n), blossom=Array(n);
  function lca(a,b) {
    const seen=Array(n).fill(false);
    while (true) { a=base[a]; seen[a]=true; if (match[a]===-1) break; a=p[match[a]]; }
    while (true) { b=base[b]; if (seen[b]) return b; b=p[match[b]]; }
  }
  function markPath(v,b,child) {
    while (base[v]!==b) {
      blossom[base[v]]=true; blossom[base[match[v]]]=true;
      p[v]=child; child=match[v]; v=p[match[v]];
    }
  }
  function findPath(root) {
    used.fill(false); p.fill(-1); for (let i=0;i<n;i++) base[i]=i;
    const q=[root]; used[root]=true;
    for (let qi=0;qi<q.length;qi++) {
      const v=q[qi];
      for (const u of g[v]) {
        if (base[v]===base[u] || match[v]===u) continue;
        if (u===root || (match[u]!==-1 && p[match[u]]!==-1)) {
          const b=lca(v,u); blossom.fill(false); markPath(v,b,u); markPath(u,b,v);
          for (let i=0;i<n;i++) if (blossom[base[i]]) {
            base[i]=b; if (!used[i]) { used[i]=true; q.push(i); }
          }
        } else if (p[u]===-1) {
          p[u]=v;
          if (match[u]===-1) return u;
          const m=match[u]; used[m]=true; q.push(m);
        }
      }
    }
    return -1;
  }
  for (let i=0;i<n;i++) if (match[i]===-1) {
    let v=findPath(i);
    if (v!==-1) while (v!==-1) {
      const pv=p[v], nv=pv===-1 ? -1 : match[pv];
      match[v]=pv; if (pv!==-1) match[pv]=v; v=nv;
    }
  }
  return { size: match.filter(x=>x!==-1).length/2, match };
}
// --- original verdict join (verbatim gates) ---
const joint=readJSON('joint'), audit=readJSON('audit'), head=readJSON('head1476');
const globalFold=readJSON('globalFold'), fold78=readJSON('fold78');
const c78=readJSON('cost78c'), c79=readJSON('cost79c'), c73=readJSON('cost73j');
need(audit.all_pass===true && audit.check_count===23 && audit.derived.maximum_root_span===2, 'independent audit gate');
need(joint.derived.joint_results.length===31 && joint.all_pass===true, 'joint gate');
const targetRows=[...new Set(audit.derived.witness_pairs.flatMap(x=>x.rows))].sort();
need(targetRows.length===112, 'target rows');
const listOf=a=>[a].flat();
const globalRows=globalFold.receipts_by_row.map(x=>x.row_hex);
const laterRows=fold78.new_receipt_coverage.receipts_by_row.map(x=>x.row_hex);
const globalHits=targetRows.filter(x=>globalRows.includes(x));
const laterHits=targetRows.filter(x=>laterRows.includes(x));
const closedSet=new Set([...globalHits,...laterHits]);
need(globalHits.length===13 && laterHits.length===2, 'previous receipt overlap 13+2');
const knownRefuted=new Set(), knownWin=new Set();
for (const x of head.candidate_root_universe.matched_roots) {
  if (x.verdict==='REFUTED-D10') knownRefuted.add(x.d4_canon_root);
  else if (x.verdict==='WIN7-D10') knownWin.add(x.d4_canon_root);
}
for (const c of [c78,c79]) {
  for (const x of Object.values(c.transfers||{})) {
    if (x.verdict==='REFUTED-D10') knownRefuted.add(x.root_canon);
    else if (x.verdict==='WIN7-D10') knownWin.add(x.root_canon);
  }
  for (const bit of c.actual_execution.refuted_d10_bits||[]) knownRefuted.add(canon(BigInt('0x'+c.s6_child)|(1n<<BigInt(bit))));
  for (const bit of c.actual_execution.win7_d10_bits||[]) knownWin.add(canon(BigInt('0x'+c.s6_child)|(1n<<BigInt(bit))));
}
for (const x of Object.values(c73.transfers||{})) {
  if (x.verdict==='REFUTED-D10') knownRefuted.add(x.root_canon);
  else if (x.verdict==='WIN7-D10') knownWin.add(x.root_canon);
}
const c73Wins=new Set(c73.actual_execution.results.win7_d10_bits);
for (const bit of c73.engine_candidate_bits.open_bits) {
  const root=canon(BigInt('0x'+c73.s6_child)|(1n<<BigInt(bit)));
  if (c73Wins.has(bit)) knownWin.add(root); else knownRefuted.add(root);
}
for (const row of globalFold.receipts_by_row) for (const x of row.receipts) knownWin.add(canon(BigInt('0x'+x.root)));
for (const row of fold78.new_receipt_coverage.receipts_by_row) for (const x of row.receipts) knownWin.add(canon(BigInt('0x'+x.root)));
for (const x of fold78.new_receipt_coverage.marginal_by_root) knownWin.add(canon(BigInt('0x'+x.root)));
const extRefutedBefore=knownRefuted.size, extWinBefore=knownWin.size;
// --- NEW verdict sources: 48-root sweep (46 REFUTED + 2 WIN) and the first receipt root ---
const sweep=readJSON('sweep');
need(sweep.status==='sweep-complete' && sweep.classification.counted_roots===48, 'sweep json gate');
need(sweep.classification.ordering_conflicts.length===0, 'sweep conflicts');
for (const r of sweep.classification.refuted_d10.roots) knownRefuted.add(r);
for (const r of sweep.classification.win7_d10.roots) knownWin.add(r);
// first WIN receipt root (published separately in the first evidence tarball)
function untarEntry(gzBytes, wantedSuffix) {
  const t = zlib.gunzipSync(gzBytes);
  let off = 0;
  while (off + 512 <= t.length) {
    const hdr = t.subarray(off, off + 512);
    if (hdr.every(x => x === 0)) break;
    const name = hdr.subarray(0, 100).toString('utf8').replace(/\0.*$/, '');
    const sizeField = hdr.subarray(124, 136).toString('utf8').replace(/\0.*$/, '').trim();
    let size = 0;
    if (sizeField) size = parseInt(sizeField, 8);
    const data = t.subarray(off + 512, off + 512 + size);
    if (name.endsWith(wantedSuffix)) return data;
    off += 512 + Math.ceil(size / 512) * 512;
  }
  throw new Error('entry not found: ' + wantedSuffix);
}
const firstFoldBytes = untarEntry(readBytes('firstFoldTarball'), 'output/first-win7-root-receipt-fold-20261119.json');
const firstFold = JSON.parse(firstFoldBytes.toString('utf8'));
const firstRoot = firstFold.root.hex;
knownWin.add(canon(BigInt('0x'+firstRoot)));
const myFold = readJSON('myFold');
need(myFold.status==='fold-complete' && myFold.receipt_count===2, 'my fold gate');
for (const r of myFold.receipts) knownWin.add(canon(BigInt('0x'+r.root)));
const extRefutedAfter=knownRefuted.size, extWinAfter=knownWin.size;
// --- residual after all three receipts ---
const oldRefuted=236;
need(extRefutedBefore===oldRefuted && extWinBefore===156, 'enumerated verdict-source totals changed: '+extRefutedBefore+'/'+extWinBefore);
const firstTarget=[...firstFold.root.covered_five_parent_target_rows];
need(firstTarget.length===2, 'first fold target rows');
const myTarget=myFold.receipts.flatMap(r=>r.covered_five_parent_target_rows);
need(myTarget.length===4, 'my fold target rows');
for (const h of firstTarget) need(targetRows.includes(h), 'first fold target row not in target union: '+h);
for (const h of myTarget) need(targetRows.includes(h), 'my fold target row not in target union: '+h);
const closedAll=new Set([...closedSet, ...firstTarget, ...myTarget]);
need(closedAll.size===21, 'total closed target rows must be 15+2+4=21, got '+closedAll.size);
const residualRows=targetRows.filter(x=>!closedAll.has(x));
need(residualRows.length===91, 'residual rows after three receipts: '+residualRows.length);
const residualSet=new Set(residualRows);
// --- pool: original 117 candidates minus new verdicts ---
const pool=new Set(audit.derived.witness_pairs.map(x=>canon(BigInt('0x'+x.root))));
for (const subset of joint.derived.joint_results) for (const root of subset.witness_roots) pool.add(canon(BigInt('0x'+root)));
need(pool.size===117, 'pool size');
const coverBytes=fs.readFileSync(path.join(ROOT,'research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/five-parent-residual-49-cover-20261119.json'));
PIN.cover=['research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/five-parent-residual-49-cover-20261119.json', gitBlobSha(coverBytes)];
const cover=JSON.parse(coverBytes.toString('utf8'));
const publishedWitness=new Set(cover.witness.map(x=>x.root));
for (const r of publishedWitness) need(pool.has(r), 'witness root not in pool: '+r);
const poolRefutedNow=[...pool].filter(x=>knownRefuted.has(x)).sort();
const poolWinNow=[...pool].filter(x=>knownWin.has(x)).sort();
need(poolWinNow.length===3, 'three WIN receipt roots in pool, got '+poolWinNow.length);
need(poolRefutedNow.length===5+46, '5 previously-known plus 46 swept refuted, got '+poolRefutedNow.length);
const candidates=[...pool].filter(x=>!knownRefuted.has(x)&&!knownWin.has(x)).sort();
need(candidates.length===117-5-46-3, 'candidate count: '+candidates.length);
// --- coverage over residual rows ---
const pairRoots=new Map(), singleRoots=new Map(), zeroCover=[];
for (const root of candidates) {
  const mask=BigInt('0x'+root), covered=new Set();
  for (let t=0;t<8;t++) {
    const image=transform(mask,t);
    for (let bit=0;bit<121;bit++) if ((image>>BigInt(bit))&1n) {
      const row=canon(image^(1n<<BigInt(bit)));
      if (residualSet.has(row)) covered.add(row);
    }
  }
  const rows=[...covered].sort();
  if (rows.length===2) {
    const key=rows.join('|'); if (!pairRoots.has(key)) pairRoots.set(key,[]); pairRoots.get(key).push(root);
  } else if (rows.length===1) {
    if (!singleRoots.has(rows[0])) singleRoots.set(rows[0],[]); singleRoots.get(rows[0]).push(root);
  } else zeroCover.push({root, residual_covered: rows});
}
const rowIndex=new Map(residualRows.map((x,i)=>[x,i]));
const graph=Array.from({length:residualRows.length},()=>[]);
for (const key of pairRoots.keys()) {
  const [a,b]=key.split('|'), i=rowIndex.get(a), j=rowIndex.get(b);
  graph[i].push(j); graph[j].push(i);
}
for (const edges of graph) edges.sort((a,b)=>a-b);
const matching=maximumMatching(graph);
const matchedRows=residualRows.filter((_,i)=>matching.match[i]!==-1);
const unmatched=residualRows.filter((_,i)=>matching.match[i]===-1);
const unmatchedWithSingleton=unmatched.filter(h=>singleRoots.has(h));
const strandedRows=unmatched.filter(h=>!singleRoots.has(h));
const witness=[];
for (let i=0;i<residualRows.length;i++) {
  const j=matching.match[i];
  if (j>i) { const key=[residualRows[i],residualRows[j]].sort().join('|'); witness.push({root:pairRoots.get(key).sort()[0], rows:key.split('|')}); }
}
for (const h of unmatchedWithSingleton) witness.push({root:singleRoots.get(h).sort()[0], rows:[h]});
witness.sort((a,b)=>a.root.localeCompare(b.root));
const coveredByWitness=new Set(witness.flatMap(w=>w.rows));
const witnessCoversAllWithSingletons = coveredByWitness.size===residualRows.length && witness.every(w=>w.rows.every(r=>residualSet.has(r)));
// root geometry checks for every witness root
const rootChecks=[];
for (const item of witness) {
  const mask=BigInt('0x'+item.root), points=[];
  for (let p=0;p<121;p++) if ((mask>>BigInt(p))&1n) points.push([p%11,Math.floor(p/11)]);
  let unsafe=0;
  for (let a=0;a<7;a++) for (let b=a+1;b<7;b++) for (let c=b+1;c<7;c++) for (let d=c+1;d<7;d++)
    if (det4(points[a],points[b],points[c],points[d])===0n) unsafe++;
  const covered=new Set();
  for (let t=0;t<8;t++) {
    const image=transform(mask,t);
    for (let bit=0;bit<121;bit++) if ((image>>BigInt(bit))&1n) {
      const row=canon(image^(1n<<BigInt(bit)));
      if (residualSet.has(row)) covered.add(row);
    }
  }
  need(popcount(mask)===7 && canon(mask)===item.root && unsafe===0, 'unsafe/noncanonical root '+item.root);
  need(JSON.stringify([...covered].sort())===JSON.stringify(item.rows), 'coverage mismatch '+item.root);
  rootChecks.push({root:item.root, stones:7, d4_canonical:true, unsafe_quadruples:unsafe, covered_residual_rows:item.rows});
}
const rowUse=new Map();
for (const item of witness) for (const row of item.rows) rowUse.set(row,(rowUse.get(row)||0)+1);
const lowerBound=Math.ceil(residualRows.length/2);
const fullyCovered = witnessCoversAllWithSingletons && strandedRows.length===0;
const result={
  schema:'n11-five-parent-refuted-excluded-cover-resolve-20261119-v1',
  date:'2026-11-19',
  status: fullyCovered ? 'exact-residual-candidate-cover' : 'residual-rows-uncoverable-by-remaining-candidates',
  source_main_head:'c8e974a26629a8b91662f479e1d84e10cae6ddcd',
  input_pins:Object.fromEntries(Object.entries(PIN).map(([k,v])=>[k,{path:v[0],git_blob_sha1:v[1]}])),
  target:{parents:5, rows:112, maximum_candidate_root_span:2},
  receipts:{
    global_fold_rows:globalRows.length, global_hits:globalHits.length,
    cost78c_79c_rows:laterRows.length, first_win7_rows:firstFold.new_receipt_coverage.unique_s6_rows,
    closed_target_rows:closedAll.size, first_win7_target_rows:firstTarget, second_third_win7_target_rows:myTarget,
    residual_rows:residualRows.length, residual_row_hex:residualRows
  },
  verdict_pool:{
    known_refuted_roots:knownRefuted.size, known_win_roots:knownWin.size,
    refuted_before_sweep:extRefutedBefore, win_before_sweep:extWinBefore,
    sweep_added_refuted:sweep.classification.refuted_d10.count, sweep_added_win:sweep.classification.win7_d10.count,
    first_receipt_win_added:1, pool_roots:pool.size, pool_refuted:poolRefutedNow.length, pool_win:poolWinNow.length,
    eligible_candidates:candidates.length, zero_residual_cover_in_pool:zeroCover.length,
    limitation:'the known-verdict join uses the explicitly pinned sweep/receipt sources (originals plus the 2026-11-19 48-root depth-10 sweep and the three published WIN7-D10 receipts); it is not the full 8,964-entry cache join'
  },
  resolve:{
    pair_edges:pairRoots.size, singleton_eligible_rows:singleRoots.size, maximum_matching:matching.size,
    matched_rows:matchedRows.length, unmatched_rows:unmatched.length,
    unmatched_with_singleton:unmatchedWithSingleton.length, stranded_rows:strandedRows.length,
    stranded_row_hex:strandedRows,
    witness_size:witness.length, lower_bound:lowerBound,
    covered_rows:coveredByWitness.size
  },
  witness, root_checks:rootChecks,
  checks:[
    {name:'original 236/156 enumerated totals reproduce', pass:extRefutedBefore===236&&extWinBefore===156},
    {name:'sweep adds exactly 46 REFUTED-D10 pool roots', pass:sweep.classification.refuted_d10.count===46},
    {name:'receipt roots are the only pool WINs (3)', pass:poolWinNow.length===3},
    {name:'total closed target rows 21 (13+2+2+4)', pass:closedAll.size===21},
    {name:'91 residual rows remain', pass:residualRows.length===91},
    {name:'candidate pool = 117 - 51 refuted - 3 win = 63', pass:candidates.length===63},
    {name:'witness rows are open residual rows', pass:[...coveredByWitness].every(x=>residualSet.has(x))},
    {name:'stranded rows have no candidate (informational when zero)', pass:true}
  ],
  all_pass:true,
  interpretation_guard:[
    'This re-solve strikes the 46 REFUTED-D10 witness roots and recomputes a candidate cover; witness roots still require actual sweeps and independently verified certificates.',
    'A stranded row (if any) cannot be closed by ANY remaining depth-10 WIN7 candidate in the 117-root pool; it then needs a candidate beyond this pool, a deeper search, or a different closure mechanism.',
    fullyCovered ? 'The resolved witness is a conditional plan, not a set of certificates.' : 'The residual target has stranded rows; the candidate pool alone cannot close the five-parent target at depth 10.',
    'REFUTED-D10 is not a LOSS proof.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.'
  ]
};
fs.writeFileSync(path.join(OUT,'five-parent-refuted-excluded-cover-resolve-20261119.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:result.status, residual_rows:91, eligible_candidates:candidates.length, pair_edges:pairRoots.size, singleton_rows:singleRoots.size, matching:matching.size, unmatched:unmatched.length, stranded:strandedRows.length, witness:witness.length, lower_bound:lowerBound, witnessCoversAll:witnessCoversAllWithSingletons},null,2));
