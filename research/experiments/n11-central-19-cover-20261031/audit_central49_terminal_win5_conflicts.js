#!/usr/bin/env node
'use strict';
// Cross-snapshot terminal-WIN5 audit for the historical {49,60} 31-S4 plan.
// The original pinned-cache geometric checks remain valid, but two selected
// S4 LOSS *candidates* have independently certified WIN5 children.
// This is a plan refutation, NOT a verdict for the S2 root or empty board.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const ROOT = path.resolve(__dirname, '../../..');
const cert = JSON.parse(fs.readFileSync(path.join(__dirname,
  'win4-safe-31-loss4-reuse-49.json'), 'utf8'));
const frontier = JSON.parse(fs.readFileSync(path.join(__dirname,
  'central49-frontier-ownership.json'), 'utf8'));
assert.deepEqual(cert.root_stones, [49, 60]);
assert.equal(cert.root_outcome, 'UNKNOWN');
assert.deepEqual(frontier.rootStones, [49, 60]);
assert.equal(frontier.rootOutcome, 'UNKNOWN');
assert.deepEqual(cert.selected_s4_classes, frontier.witnesses.map(w => w.s4));
assert.equal(cert.selected_s4_classes.length, 31);
const maps = Array.from({length:8}, (_,j) => Array.from({length:121}, (_,i) => {
  const x=i%11, y=Math.floor(i/11);
  const [u,v]=[[x,y],[10-y,x],[10-x,10-y],[y,10-x],
    [10-x,y],[10-y,10-x],[x,10-y],[y,x]][j];
  return 11*v+u;
}));
function canonical(p) {
  let best=null;
  for(const m of maps) {
    let n=0n;
    for(const x of p) n|=1n<<BigInt(m[x]);
    if(best===null||n<best) best=n;
  }
  return best.toString(16).padStart(32,'0');
}
function points(key) {
  assert.match(key,/^[0-9a-f]{32}$/);
  const n=BigInt('0x'+key);
  assert.equal(n>>121n,0n);
  return Array.from({length:121},(_,i)=>i).filter(i=>Boolean(n&(1n<<BigInt(i))));
}
function det4(four) {
  const a=four.map(i=>{const x=i%11,y=Math.floor(i/11);return [x*x+y*y,x,y]});
  const b=a.slice(1).map(row=>row.map((v,j)=>v-a[0][j]));
  return b[0][0]*(b[1][1]*b[2][2]-b[1][2]*b[2][1])
    -b[0][1]*(b[1][0]*b[2][2]-b[1][2]*b[2][0])
    +b[0][2]*(b[1][0]*b[2][1]-b[1][1]*b[2][0]);
}
function safe(p) {
  for(let a=0;a<p.length;a++) for(let b=a+1;b<p.length;b++)
    for(let c=b+1;c<p.length;c++) for(let d=c+1;d<p.length;d++)
      if(det4([p[a],p[b],p[c],p[d]])===0) return false;
  return true;
}
function blobSha(raw) {
  return crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');
}
const terminalWin5 = [
  {index:126017, stones:[1,49,59,60,61],
   receipt:'research/experiments/n11-night-batch1-20261014/output/nightb10m-126017-receipt.json',
   receiptBlob:'a16a89e94f6e18d18191284d3489b9c2b78662a5',
   certificateSha256:'29eb8689474b4c203fb631431ba6f40e6cc4da25f6bf8a2affd8c5c676983492',
   parent:'00000000000000003800000000000002',
   child:'00000000000000003802000000000002'},
  {index:162106, stones:[14,49,59,60,61],
   receipt:'research/experiments/n11-night-batch5-20261014/output/nighta25m-162106-receipt.json',
   receiptBlob:'9e687e5ec961254d6ea8dc2f33e1c62291bfe19b',
   certificateSha256:'d996a6821abfa5e21c7c04fff178a84f6d3a7b5f1dfb27b19fc7fc6d36a633e9',
   parent:'00000000000000003800000000004000',
   child:'00000000000000003802000000004000'},
];
function checkReceipt(item, receipt) {
  assert.equal(receipt.s5_index,item.index);
  assert.equal(receipt.board_size,11);
  assert.equal(receipt.verdict,1,'terminal WIN5 verdict changed');
  assert.equal(receipt.trusted_leaves,0,'non-terminal proof cannot be promoted');
  assert.equal(receipt.evidence_class,'independent-terminal-only-verification');
  assert.equal(receipt.certificate_sha256,item.certificateSha256);
  const mask=item.stones.reduce((v,x)=>v|(1n<<BigInt(x)),0n);
  assert.equal(BigInt(receipt.root_mask),mask,'terminal root does not match stones');
}
const frequency = new Map();
for(const w of frontier.witnesses)
  for(const x of w.thirdMoves) frequency.set(x,(frequency.get(x)||0)+1);
assert.equal(frequency.size,119);
const impacts=[];
for(const item of terminalWin5) {
  const raw=fs.readFileSync(path.join(ROOT,item.receipt));
  assert.equal(blobSha(raw),item.receiptBlob,'terminal receipt changed');
  const receipt=JSON.parse(raw.toString('utf8'));
  checkReceipt(item,receipt);
  assert.equal(item.stones.length,5);
  assert.equal(new Set(item.stones).size,5);
  assert(safe(item.stones),'terminal S5 illegal');
  assert.equal(canonical(item.stones),item.child,'terminal S5 canonical mismatch');
  const parents=item.stones.map((removed,j)=>({
    removed,key:canonical(item.stones.filter((_,i)=>i!==j))
  }));
  const selected=parents.filter(p=>cert.selected_s4_classes.includes(p.key));
  assert.equal(selected.length,1,'unexpected selected S4 parents');
  assert.equal(selected[0].removed,49);
  assert.equal(selected[0].key,item.parent);
  assert(!cert.known_loss4_classes.includes(item.parent),
    'independently proven WIN4 conflicts with pinned LOSS4');
  const witness=frontier.witnesses[cert.selected_s4_classes.indexOf(item.parent)];
  assert.equal(witness.status,'UNKNOWN');
  const s4=points(item.parent);
  assert.equal(s4.length,4);
  assert(safe(s4));
  const children=new Set();
  for(let x=0;x<121;x++) if(!s4.includes(x)&&safe([...s4,x]))
    children.add(canonical([...s4,x]));
  assert(children.has(item.child),'terminal WIN5 not a legal S4 child');
  assert.equal(children.size,witness.legalS5Children);
  const third=new Set();
  for(const m of maps) {
    const transformed=s4.map(x=>m[x]);
    if(transformed.includes(49)&&transformed.includes(60))
      for(const x of transformed) if(x!==49&&x!==60) third.add(x);
  }
  assert.deepEqual([...third].sort((a,b)=>a-b),witness.thirdMoves);
  const exclusive=[...third].filter(x=>frequency.get(x)===1).sort((a,b)=>a-b);
  assert.deepEqual(exclusive,witness.exclusiveThirdMoves);
  impacts.push({terminal_s5_index:item.index,certified_win5:item.child,
    refuted_s4_loss_candidate:item.parent,
    third_moves:witness.thirdMoves,exclusively_covered_third_moves:exclusive,
    former_unknown_s5_children:witness.unknownS5});
}
// Mutation controls: an unsupported terminal label or mismatched root must fail.
const receipt=JSON.parse(fs.readFileSync(path.join(ROOT,terminalWin5[0].receipt)));
assert.throws(()=>checkReceipt(terminalWin5[0],{...receipt,verdict:2}));
assert.throws(()=>checkReceipt(terminalWin5[0],{...receipt,trusted_leaves:1}));
assert.throws(()=>checkReceipt(terminalWin5[0],{...receipt,root_mask:'0'}));
// Count historical pending S5 keys attached only to the refuted S4 pair.
const allOwners=new Map();
for(let i=0;i<frontier.witnesses.length;i++) {
  const s4=points(frontier.witnesses[i].s4);
  const cs=new Set();
  for(let x=0;x<121;x++) if(!s4.includes(x)&&safe([...s4,x]))
    cs.add(canonical([...s4,x]));
  assert.equal(cs.size,frontier.witnesses[i].legalS5Children);
  for(const child of cs) {
    if(!allOwners.has(child)) allOwners.set(child,new Set());
    allOwners.get(child).add(i);
  }
}
const refutedIndices=new Set(impacts.map(x=>
  cert.selected_s4_classes.indexOf(x.refuted_s4_loss_candidate)));
const touched=[...allOwners].filter(([k,indices])=>
  [...indices].some(i=>refutedIndices.has(i)));
const exclusiveToRefuted=touched.filter(([k,indices])=>
  [...indices].every(i=>refutedIndices.has(i)));
assert.equal(touched.length,204);
assert.equal(exclusiveToRefuted.length,119);
assert.equal(new Set(impacts.flatMap(x=>x.exclusively_covered_third_moves)).size,8);
assert.equal(new Set(impacts.map(x=>x.refuted_s4_loss_candidate)).size,2);
console.log(JSON.stringify({
  schema:'n11-central49-terminal-win5-plan-refutation-v1',
  root:[49,60],root_outcome:'UNKNOWN',empty_board:'UNKNOWN',
  historical_plan_s4:31,certified_win5_conflicts:2,
  invalidated_s4_loss_candidates:2,exclusive_third_moves_requiring_repair:8,\n  historical_pending_s5_touching_refuted_witnesses:touched.length,\n  historical_pending_s5_only_under_refuted_witnesses:exclusiveToRefuted.length,
  impacts,
  trust:'Both WIN5 labels have stored independent terminal-only receipts with zero trusted leaves. Receipt integrity and geometric incidence are rechecked here; full large terminal DAGs are not replayed by this small audit.',
  consequence:'Historical 31-S4 plan cannot close {49,60} as LOSS without replacing these two S4 classes; the 2525-S5 worker list is stale as an actionable LOSS proof plan.'
},null,2));
