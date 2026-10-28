#!/usr/bin/env node
'use strict';
// Independent move-boundary audit for the frozen round15 S9 batch.
// Legal S10 edges are not terminal WIN/LOSS verdicts.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const plan=read('next-plan.json'),roots=plan.newSelectedKeys;
need(plan.schema==='n11-post-round14-proof-only-replan-v1'&&
  plan.emptyBoard==='UNKNOWN'&&plan.conditionalUnprovedEdges===55&&
  plan.proofOnlyWin8After===5715&&plan.eligibleUnprovedS9===269&&
  plan.undominatedS9===34&&plan.potentialCoverage===32&&
  roots.length===32&&new Set(roots).size===32&&
  sha(roots.join('\n')+'\n')===plan.newSelectionSha256,
  'frozen round14 replan mismatch');
let edges=0;
const occurrences=new Map();
for(const root of roots){
  g.board(root,9);
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
need(edges===plan.legal10Children,'selected S10 edge count mismatch');
const overlaps=[...occurrences].filter(([,parents])=>parents.length>1)
  .map(([child,parents])=>({child,parents}))
  .sort((a,b)=>a.child.localeCompare(b.child));
const result={
  schema:'n11-post-round14-independent-boundary-preflight-v1',
  emptyBoard:'UNKNOWN',selectionSha256:plan.newSelectionSha256,
  roots:roots.length,legalS10Edges:edges,
  distinctS10Classes:occurrences.size,repeatedS10Classes:overlaps.length,
  crossRootSavings:edges-occurrences.size,sharedChildren:overlaps,
  geometryChecks:['3x3-difference-determinant','4x4-independent-integer-determinant'],
  terminalVerdicts:0,newTwoStoneClosures:0
};
const frozen=read('preflight.json');
need(JSON.stringify(result)===JSON.stringify(frozen),
  'frozen round15 preflight mismatch');
console.log(JSON.stringify(result,null,2));
