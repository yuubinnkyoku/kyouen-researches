#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const EXP = 'research/experiments/n11-s2-5960-ms5-s7-reuse-20261113';
const OUT = path.join(process.cwd(), EXP, 'output');
const BAND = path.join(OUT, 'class2-lane-cost73l-certificates');
const readJson = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const assert = (condition, message) => { if (!condition) throw new Error(message); };
const hex32 = value => value.toString(16).padStart(32, '0');

function det3([[a,b,c],[d,e,f],[g,h,i]]) {
  return a * (e*i - f*h) - b * (d*i - f*g) + c * (d*h - e*g);
}
function tripleCoefficients(a, b, c) {
  const rows = [a,b,c].map(p => {
    const x = BigInt(p % 11), y = BigInt(Math.floor(p / 11));
    return [x*x + y*y, x, y, 1n];
  });
  return Array.from({length:4}, (_, column) => {
    const minor = rows.map(row => row.filter((_, j) => j !== column));
    const d = det3(minor);
    return column % 2 === 0 ? -d : d;
  });
}
function determinant4(a, b, c, d) {
  const q = tripleCoefficients(a,b,c);
  const x = BigInt(d % 11), y = BigInt(Math.floor(d / 11));
  return q[0]*(x*x+y*y) + q[1]*x + q[2]*y + q[3];
}
function pointsOf(hex) {
  const mask = BigInt('0x' + hex), points = [];
  for (let p=0; p<121; p++) if ((mask >> BigInt(p)) & 1n) points.push(p);
  return points;
}
function legalMoves(rootHex) {
  const points = pointsOf(rootHex);
  assert(points.length === 7, 'root must have 7 stones: ' + rootHex);
  for (let a=0; a<7; a++) for (let b=a+1; b<7; b++)
    for (let c=b+1; c<7; c++) for (let d=c+1; d<7; d++)
      assert(determinant4(points[a],points[b],points[c],points[d]) !== 0n,
        'unsafe 7-stone root: ' + rootHex);
  const moves=[];
  for (let p=0; p<121; p++) {
    if (points.includes(p)) continue;
    const x=BigInt(p%11), y=BigInt(Math.floor(p/11));
    let legal=true;
    for (let a=0; a<7 && legal; a++) for (let b=a+1; b<7 && legal; b++)
      for (let c=b+1; c<7; c++) {
        const q=tripleCoefficients(points[a],points[b],points[c]);
        if (q[0]*(x*x+y*y)+q[1]*x+q[2]*y+q[3] === 0n) { legal=false; break; }
      }
    if (legal) moves.push(p);
  }
  return moves;
}
function d4Canon(rootHex) {
  const points=pointsOf(rootHex);
  let best=null;
  for (let xf=0; xf<2; xf++) for (let yf=0; yf<2; yf++) for (let swap=0; swap<2; swap++) {
    let mask=0n;
    for (const p of points) {
      let x=p%11, y=Math.floor(p/11);
      if (xf) x=10-x;
      if (yf) y=10-y;
      if (swap) [x,y]=[y,x];
      mask |= 1n << BigInt(y*11+x);
    }
    const h=hex32(mask);
    if (best===null || h<best) best=h;
  }
  return best;
}

const manifestPath=path.join(BAND,'class2-lane-cost73l-win7-certificates-20261117.json');
const claimPath=path.join(OUT,'class2-lane-cost73l-inflight-20261117.json');
const rawAuditPath=path.join(OUT,'class2-lane-cost73l-raw-sweep-audit-20261117.json');
const statsPath=path.join(BAND,'stats.json');
const detPath=path.join(BAND,'det-reextraction.json');
const pinsPath=path.join(OUT,'class2-lane-cost73l-pins-20261117.txt');
const priorJPath=path.join(OUT,'class2-lane-cost73j-certificates/class2-lane-cost73j-win7-certificates-20261117.json');
const priorKPath=path.join(OUT,'class2-lane-cost73k-certificates/class2-lane-cost73k-win7-certificates-20261117.json');
const manifest=readJson(manifestPath), claim=readJson(claimPath), rawAudit=readJson(rawAuditPath);
const stats=readJson(statsPath), det=readJson(detPath);
const priorJ=readJson(priorJPath), priorK=readJson(priorKPath);
const records=manifest.certificates;
const child=BigInt('0x'+manifest.s6_child_hex);

assert(claim.schema==='n11-class2-lane-cost73l-inflight-20261117-v3','claim schema');
assert(manifest.schema==='n11-class2-lane-cost73l-win7-certificates-20261117-v1','manifest schema');
assert(manifest.s6_child_hex==='00000000000000c09002000000400000','child hex');
assert(manifest.s6_s7_edge_cost===73,'edge cost');
assert(records.length===32 && manifest.totals.certificates===32,'certificate count');
const candidates=claim.legal_candidates;
const open=claim.engine_candidate_bits.open_bits;
const confirmations=claim.engine_candidate_bits.confirmation_bits;
const win=claim.actual_execution.results.win7_d10_bits;
const refuted=claim.actual_execution.results.refuted_d10_bits;
assert(candidates.length===73,'candidate count');
assert(open.length===66 && confirmations.length===7,'open/confirmation counts');
assert(new Set([...open,...confirmations]).size===73,'open/confirmation overlap');
assert([...open,...confirmations].every(x=>candidates.includes(x)),'candidate partition');
assert(win.length===34 && refuted.length===39 && claim.actual_execution.results.capped_count===0,'sweep verdict counts');
assert(new Set([...win,...refuted]).size===73,'WIN/REFUTED partition');
assert([...win,...refuted].every(x=>candidates.includes(x)),'verdict candidate membership');
const expectedBits=records.map(x=>x.bit).sort((a,b)=>a-b);
assert(new Set(expectedBits).size===32,'duplicate manifest bit');
assert(expectedBits.every(x=>win.includes(x)),'manifest contains non-WIN bit');
const transferredWin=win.filter(x=>!expectedBits.includes(x)).sort((a,b)=>a-b);
assert(JSON.stringify(transferredWin)==='[106,110]','unexpected uncovered WIN bits');
assert(!expectedBits.some(x=>confirmations.includes(x)),'confirmation bit duplicated in manifest');
assert(claim.certificates.manifest==='class2-lane-cost73l-win7-certificates-20261117.json','claim manifest path');
assert(claim.certificates.manifest_blob_sha==='6e0a94aba212ba54bb5329fbea4643c9dcdb1ec4','claim manifest blob pin');
assert(claim.certificates.totals.rows===manifest.totals.rows,'claim/manifest rows');
assert(claim.certificates.totals.extraction_nodes===manifest.totals.extraction_nodes,'claim/manifest nodes');
assert(claim.certificates.totals.published_bytes===manifest.totals.published_bytes,'claim/manifest bytes');
assert(rawAudit.status.includes('34 WIN7-D10 / 39 REFUTED-D10 / 0 capped'),'raw sweep audit summary');
assert(manifest.unknown_status.includes('UNKNOWN') && claim.unknown_status.includes('UNKNOWN'),'UNKNOWN guard');

const priorRecords=[...priorJ.certificates,...priorK.certificates];
const priorCanons=new Set(priorRecords.map(x=>d4Canon(x.root)));
assert(priorRecords.length===38 && priorCanons.size===38,'prior 73j/73k root population');
const roots=new Set(), canons=new Set();
const perBit=[];
let totalRows=0,totalNodes=0,totalBytes=0,totalSubroots=0;
for (const rec of records) {
  assert(rec.verdict==='WIN7' && rec.depth===10,'record verdict/depth');
  const expectedRoot=hex32(child | (1n << BigInt(rec.bit)));
  assert(rec.root===expectedRoot,'bit ' + rec.bit + ': root != child|bit');
  const canon=d4Canon(rec.root);
  assert(canon===rec.d4_canon_root,'bit ' + rec.bit + ': D4 canon');
  assert(rec.raw_is_canon===(canon===rec.root),'bit ' + rec.bit + ': raw_is_canon');
  assert(!roots.has(rec.root) && !canons.has(canon),'bit ' + rec.bit + ': duplicate root/canon');
  assert(!priorCanons.has(canon),'bit ' + rec.bit + ': D4 overlap with 73j/73k');
  roots.add(rec.root); canons.add(canon);
  const mobility=legalMoves(rec.root).length;
  assert(mobility===rec.loser_mobility,'bit ' + rec.bit + ': independent mobility');
  assert(rec.subroots===mobility && rec.subroots_pass===mobility,'bit ' + rec.bit + ': subroot count');
  assert(rec.union_missing===0 && rec.union_extra===0,'bit ' + rec.bit + ': row-union flags');
  assert(rec.fbt_drops===0 && rec.fatal===null,'bit ' + rec.bit + ': extraction flags');
  assert(JSON.stringify(rec.terminal_stone_range)==='[13,17]','bit ' + rec.bit + ': terminal range');
  const s=stats[String(rec.bit)];
  assert(s && s.root===rec.root && s.rows===rec.rows && s.nodes===rec.extraction_nodes && s.moves===mobility,'bit ' + rec.bit + ': stats fields');
  assert(s.md5===rec.md5 && s.sha256===rec.sha256,'bit ' + rec.bit + ': stats hashes');
  totalRows+=rec.rows; totalNodes+=rec.extraction_nodes; totalBytes+=s.size; totalSubroots+=mobility;
  perBit.push({bit:rec.bit,root:rec.root,d4_canon:canon,mobility,rows:rec.rows,extraction_nodes:rec.extraction_nodes,certificate_bytes:s.size});
}
assert(roots.size===32 && canons.size===32,'D4 uniqueness');
assert(totalRows===manifest.totals.rows,'manifest row total');
assert(totalNodes===manifest.totals.extraction_nodes,'manifest extraction-node total');
assert(totalBytes===manifest.totals.published_bytes,'manifest byte total');
assert(stats && Object.keys(stats).length===32,'stats record count');
assert(det.all_byte_identical===true && det.bits.length===6,'determinism sample count');
for (const bit of det.bits) {
  const d=det.details[String(bit)], r=records.find(x=>x.bit===bit), s=stats[String(bit)];
  assert(d && d.identical && r && d.md5===r.md5 && d.rows===r.rows && d.size===s.size,'determinism bit ' + bit);
}
const transferChecks={};
for (const [bit,source] of [[106,priorJ.certificates.find(x=>x.bit===118)],[110,priorK.certificates.find(x=>x.bit===98)]]) {
  const canon=d4Canon(hex32(child | (1n<<BigInt(bit))));
  assert(canon===claim.transfers[String(bit)].root_canon,'transfer ' + bit + ': claim canon');
  assert(source && d4Canon(source.root)===canon,'transfer ' + bit + ': source certificate canon');
  transferChecks[String(bit)]={canon,source_bit:bit===106?118:98,source_band:bit===106?'cost73j':'cost73k'};
}
assert(claim.transfers['106'].source.includes('cost73j bit 118'),'transfer 106 source');
assert(claim.transfers['110'].source.includes('cost73k bit 98'),'transfer 110 source');

const pinLines=fs.readFileSync(pinsPath,'utf8').trim().split(/\r?\n/);
assert(pinLines.length===159,'pin table row count');
const pinNames=new Set();
for (const line of pinLines) {
  const [name,sha,size]=line.split('|');
  assert(name && /^[0-9a-f]{40}$/.test(sha) && /^\d+$/.test(size),'malformed pin row');
  assert(!pinNames.has(name),'duplicate pin filename');
  pinNames.add(name);
}

const report={
  schema:'n11-class2-lane-cost73l-publication-geometry-audit-20261117-v1',
  date:'2026-11-17',
  result:'PASS',
  scope:'Independent exact-integer geometry, D4 canonicalization, claim/manifest/stat arithmetic, prior-band disjointness, transfer identity and pin-table structure. Does not traverse certificate strategy bodies.',
  checks:{
    sweep:{candidates:73,open:66,confirmations:7,win7_d10:34,refuted_d10:39,capped:0},
    roots:{count:32,safe:32,child_or_bit:32,d4_canon_match:32,independent_mobility_match:32,unique_d4:32,overlap_with_73j_73k:0},
    transfers:transferChecks,
    manifest_totals:{certificates:32,rows:totalRows,extraction_nodes:totalNodes,published_bytes:totalBytes,subroots:totalSubroots},
    deterministic_reextractions:{all_byte_identical:det.all_byte_identical,bits:det.bits},
    pin_table:{rows:pinLines.length,unique_names:pinNames.size}
  },
  per_bit:perBit,
  interpretation_guard:[
    'The 32 WIN7-D10 records concern individual seven-stone roots only.',
    'REFUTED-D10 is not a LOSS proof.',
    'This audit does not independently traverse the certificate strategy bodies; third-implementation BigInt re-verification remains pending.',
    '11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.'
  ]
};
const outPath=path.join(OUT,'class2-lane-cost73l-publication-geometry-audit-20261117.json');
fs.writeFileSync(outPath,JSON.stringify(report,null,1)+'\n');
console.log(JSON.stringify(report.checks,null,2));
