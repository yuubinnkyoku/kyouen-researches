#!/usr/bin/env node
// Independent structural preflight for the cost79c depth-10 sweep.
// Node >= 22; zero external dependencies.
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';

const BASE = 'research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/';
const PATHS = {
  claim: BASE + 'output/class2-lane-cost79c-inflight-20261118.json',
  driver: BASE + 'scripts/ev79c_batches_20261118.sh',
  v17: BASE + 'scripts/class4_child1_runner_v17.ts',
  v15: BASE + 'scripts/class4_child1_runner.ts',
  cost73kManifest: BASE + 'output/class2-lane-cost73k-certificates/class2-lane-cost73k-win7-certificates-20261117.json'
};
const read = p => readFileSync(p, 'utf8');
const gitBlobSha = p => {
  const bytes = readFileSync(p);
  const header = Buffer.from('blob ' + bytes.length + String.fromCharCode(0));
  return createHash('sha1').update(Buffer.concat([header, bytes])).digest('hex');
};
const claim = JSON.parse(read(PATHS.claim));
const driver = read(PATHS.driver);
const v17 = read(PATHS.v17);
const v15 = read(PATHS.v15);
const manifest = JSON.parse(read(PATHS.cost73kManifest));
const pins = {
  claim: '6e1f2c909d66d56e19b70404751bc4efa651763e',
  driver: '18252801a78263a5e421e17c4fb18e05bdc2ca4f',
  v17: 'c132cc6425eee3feaeef1d697dd74f968cfedb59',
  v15: '8744fc65b6b7cac6bd561403ce4c749e01c51359',
  cost73kManifest: '0892aed07d187ae2fb3b4b90a21c7adbc1002b62'
};
for (const [name, path] of Object.entries(PATHS)) {
  assert.equal(gitBlobSha(path), pins[name], name + ' Git blob pin');
}
const checks = {};
const check = (name, ok, detail) => {
  checks[name] = { ok, detail };
  assert.ok(ok, name + ': ' + JSON.stringify(detail));
};
const fmt128 = value => value.toString(16).padStart(32, '0');
const bitset = values => values.reduce((acc, bit) => acc | (1n << BigInt(bit)), 0n);
const coords = bit => [bit % 11, Math.floor(bit / 11)];
function det4(points) {
  const rows = points.map(([x, y]) => [BigInt(x*x + y*y), BigInt(x), BigInt(y), 1n]);
  const permutations = [
    [0,1,2,3],[0,1,3,2],[0,2,1,3],[0,2,3,1],[0,3,1,2],[0,3,2,1],
    [1,0,2,3],[1,0,3,2],[1,2,0,3],[1,2,3,0],[1,3,0,2],[1,3,2,0],
    [2,0,1,3],[2,0,3,1],[2,1,0,3],[2,1,3,0],[2,3,0,1],[2,3,1,0],
    [3,0,1,2],[3,0,2,1],[3,1,0,2],[3,1,2,0],[3,2,0,1],[3,2,1,0]
  ];
  let sum = 0n;
  for (const permutation of permutations) {
    let inversions = 0;
    for (let i=0; i<4; i++) for (let j=i+1; j<4; j++)
      if (permutation[i] > permutation[j]) inversions++;
    let product = 1n;
    for (let i=0; i<4; i++) product *= rows[i][permutation[i]];
    sum += inversions % 2 ? -product : product;
  }
  return sum;
}
function transform(x, y, t) {
  switch (t) {
    case 0: return [x,y];
    case 1: return [10-y,x];
    case 2: return [10-x,10-y];
    case 3: return [y,10-x];
    case 4: return [10-x,y];
    case 5: return [x,10-y];
    case 6: return [y,x];
    default: return [10-y,10-x];
  }
}
function canon(hex) {
  const value = BigInt('0x' + hex);
  const images = [];
  for (let t=0; t<8; t++) {
    let transformed = 0n;
    for (let bit=0; bit<121; bit++) if ((value >> BigInt(bit)) & 1n) {
      const [x,y] = transform(...coords(bit), t);
      transformed |= 1n << BigInt(y*11+x);
    }
    images.push(transformed);
  }
  images.sort((a,b) => a<b ? -1 : a>b ? 1 : 0);
  return fmt128(images[0]);
}
const parent = claim.child_stones_bit_indices;
const basePoints = parent.map(coords);
check('six_bit_reconstruction', fmt128(bitset(parent)) === claim.s6_child,
  {computed:fmt128(bitset(parent)), claimed:claim.s6_child});
let parentSafe = true;
for (let a=0; a<6; a++) for (let b=a+1; b<6; b++)
  for (let c=b+1; c<6; c++) for (let d=c+1; d<6; d++)
    if (det4([basePoints[a],basePoints[b],basePoints[c],basePoints[d]]) === 0n)
      parentSafe = false;
check('parent_safety', parentSafe, {stones:6, quadruples:15});
const legal = [];
for (let p=0; p<121; p++) {
  if (parent.includes(p)) continue;
  let survives = true;
  const candidate = coords(p);
  for (let a=0; a<6 && survives; a++) for (let b=a+1; b<6 && survives; b++)
    for (let c=b+1; c<6 && survives; c++)
      if (det4([basePoints[a],basePoints[b],basePoints[c],candidate]) === 0n)
        survives = false;
  if (survives) legal.push(p);
}
check('independent_legal_candidate_enumeration',
  JSON.stringify(legal) === JSON.stringify(claim.legal_candidates),
  {computed:legal.length, claimed:claim.legal_candidates.length,
   missing:legal.filter(x=>!claim.legal_candidates.includes(x)),
   extra:claim.legal_candidates.filter(x=>!legal.includes(x))});
const open = claim.engine_candidate_bits.open_bits;
const confirmation = claim.engine_candidate_bits.confirmation_bits;
check('open_confirmation_partition',
  open.length===68 && confirmation.length===11 &&
  new Set([...open,...confirmation]).size===79 &&
  [...open,...confirmation].every(x=>legal.includes(x)),
  {open:open.length,confirmation:confirmation.length,union:new Set([...open,...confirmation]).size});
const batches = {};
for (const match of driver.matchAll(/^B([1-9])=([0-9,]+)$/gm))
  batches[Number(match[1])] = match[2].split(',').map(Number);
const openBatch = Object.keys(batches).filter(k=>Number(k)<9)
  .sort((a,b)=>a-b).flatMap(k=>batches[k]);
check('batch_1_to_8_exact_cover',
  openBatch.length===68 && new Set(openBatch).size===68 &&
  JSON.stringify([...openBatch].sort((a,b)=>a-b))===JSON.stringify([...open].sort((a,b)=>a-b)),
  {sizes:Object.fromEntries(Object.entries(batches).map(([k,v])=>[k,v.length])),
   unique:new Set(openBatch).size});
check('batch_9_confirmation_exact',
  batches[9].length===11 && JSON.stringify(batches[9])===JSON.stringify(confirmation),
  {bits:batches[9]});
check('runner_parameters',
  claim.s6_s7_edge_cost===79 && claim.candidate_count===79 &&
  driver.includes('CAP=1000000000') &&
  driver.includes('--depth 10 --cap $CAP --andclose 1 --child $CHILD') &&
  driver.includes('CHILD='+claim.s6_child),
  {edge_cost:claim.s6_s7_edge_cost,candidate_count:claim.candidate_count,
   depth:10,cap:1000000000,andclose:1});
check('pilot_control_enforced',
  !driver.includes('--nocontrol') &&
  v17.includes("runControl: !args.includes('--nocontrol')") &&
  v17.includes('c.nodes === 3402') && v17.includes('if (cfg.runControl)'),
  'all nine run17 batches retain pilot_d6');
check('fresh_engine_per_candidate',
  v17.includes('for (const bit of cfg.bits)') && v17.includes('const eng = freshEngine();'),
  'fresh engine state per candidate bit');
check('v17_fbt_saturation_repair',
  v17.includes('v17 repair: probe chain exhausted') &&
  v17.includes('cB0|=m0; cB1|=m1; cB2|=m2; cB3|=m3; return;'),
  'probe exhaustion computes and applies the blocking mask directly');
check('v17_engine_pin', gitBlobSha(PATHS.v17)===claim.engine.blob_sha,
  {fetched:gitBlobSha(PATHS.v17),claimed:claim.engine.blob_sha});
const v15Pin = claim.planned_controls.v15_crosscheck.match(/blob ([0-9a-f]{40})/);
check('v15_engine_pin', !!v15Pin && gitBlobSha(PATHS.v15)===v15Pin[1],
  {fetched:gitBlobSha(PATHS.v15),claimed:v15Pin?.[1]});
const targetCanons = [];
for (const [bit, record] of Object.entries(claim.transfers)) {
  const root = fmt128(BigInt('0x'+claim.s6_child) | (1n << BigInt(bit)));
  const actual = canon(root);
  targetCanons.push({bit:Number(bit),root,canon:actual,expected:record.root_canon,ok:actual===record.root_canon});
}
check('11_confirmation_target_canons', targetCanons.every(x=>x.ok),
  {count:targetCanons.length,failed:targetCanons.filter(x=>!x.ok)});
const allCanons = legal.map(bit => canon(fmt128(BigInt('0x'+claim.s6_child) | (1n << BigInt(bit)))));
check('all_79_candidate_roots_d4_distinct', new Set(allCanons).size===79,
  {roots:79,unique:new Set(allCanons).size});
const stabilizer = [];
for (let t=0; t<8; t++) {
  let transformed = 0n;
  for (const bit of parent) {
    const [x,y] = transform(...coords(bit),t);
    transformed |= 1n << BigInt(y*11+x);
  }
  if (transformed===BigInt('0x'+claim.s6_child)) stabilizer.push(t);
}
check('parent_d4_stabilizer_trivial', stabilizer.length===1, {transforms:stabilizer});
const sourceBit87 = manifest.certificates.find(x=>x.bit===87);
check('bit110_source_cost73k_bit87_canon',
  !!sourceBit87 && sourceBit87.verdict==='WIN7' &&
  sourceBit87.d4_canon_root===claim.transfers['110'].root_canon,
  {source_root:sourceBit87?.root,source_canon:sourceBit87?.d4_canon_root,
   target_canon:claim.transfers['110'].root_canon});
const predicted = Object.values(claim.engine_candidate_bits.confirmation_verdicts_predicted);
check('confirmation_expected_verdict_mix',
  predicted.filter(x=>x==='REFUTED-D10').length===10 &&
  predicted.filter(x=>x==='WIN7-D10').length===1,
  {refuted:predicted.filter(x=>x==='REFUTED-D10').length,
   win:predicted.filter(x=>x==='WIN7-D10').length});
const result = {
  schema:'n11-cost79c-preflight-structural-audit-20261118-v1',
  date:'2026-11-18',
  input_pins:Object.fromEntries(Object.entries(PATHS).map(([name,path])=>
    [name,{path,git_blob_sha:gitBlobSha(path)}])),
  target:{s5:claim.s5,s6:claim.s6_child,stone_bits:parent,
    legal_candidates:legal.length,open_bits:open.length,confirmation_bits:confirmation.length},
  checks,confirmation_target_canonicalizations:targetCanons,
  d4_candidate_orbits:{legal_roots:79,unique:new Set(allCanons).size,parent_stabilizer:stabilizer},
  verdict_boundary:'Structural preflight only. No depth-10 search, new certificate verification, or receipt fold. The other ten transfer source roots were not re-fetched by this audit. REFUTED-D10 is not a LOSS proof.',
  all_pass:true,failures:[]
};
process.stdout.write(JSON.stringify(result,null,2)+String.fromCharCode(10));
