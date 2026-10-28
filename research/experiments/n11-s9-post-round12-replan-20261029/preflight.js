#!/usr/bin/env node
'use strict';
// Independent exact move-boundary audit for the frozen round13 candidate batch.
// Legal S10 children are not terminal verdicts.
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need=(ok,msg)=>{if(!ok)throw Error(msg)};
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const plan=JSON.parse(fs.readFileSync(path.join(__dirname,'next-plan.json'),'utf8'));
const roots=plan.newSelectedKeys;
need(plan.schema==='n11-post-round12-proof-only-replan-v1'&&
  plan.emptyBoard==='UNKNOWN'&&plan.conditionalUnprovedEdges===64&&
  plan.proofOnlyWin8After===5643&&plan.eligibleUnprovedS9===423&&
  roots.length===32&&new Set(roots).size===32&&
  sha(roots.join('\n')+'\n')===plan.newSelectionSha256,
  'frozen round12 selection mismatch');
let edges=0;
const occurrences=new Map();
for(const root of roots){
  need(/^[0-9a-f]{32}$/.test(root)&&g.pts(BigInt('0x'+root)).length===9,
    'invalid S9 root '+root);
  const first=g.children(g.board(root,9));
  const second=ind.children4(root);
  need(first.size===second.size&&[...first].every(h=>second.has(h)),
    'independent 3x3 / 4x4 geometry mismatch '+root);
  edges+=first.size;
  for(const child of first){
    if(!occurrences.has(child))occurrences.set(child,[]);
    occurrences.get(child).push(root);
  }
}
need(edges===plan.legal10Children,'selected legal S10 edge count mismatch');
const overlaps=[...occurrences].filter(([,parents])=>parents.length>1)
  .map(([child,parents])=>({child,parents}))
  .sort((a,b)=>a.child.localeCompare(b.child));
const result={
  schema:'n11-post-round12-independent-boundary-preflight-v1',
  emptyBoard:'UNKNOWN',
  selectionSha256:plan.newSelectionSha256,
  roots:roots.length,
  legalS10Edges:edges,
  distinctS10Classes:occurrences.size,
  repeatedS10Classes:overlaps.length,
  crossRootSavings:edges-occurrences.size,
  sharedChildren:overlaps,
  geometryChecks:['3x3-difference-determinant','4x4-independent-integer-determinant'],
  terminalVerdicts:0,newTwoStoneClosures:0
};
const frozen=path.join(__dirname,'preflight.json');
if(fs.existsSync(frozen)){
  const expected=JSON.parse(fs.readFileSync(frozen,'utf8'));
  need(JSON.stringify(expected)===JSON.stringify(result),'frozen preflight mismatch');
}
console.log(JSON.stringify(result,null,2));
