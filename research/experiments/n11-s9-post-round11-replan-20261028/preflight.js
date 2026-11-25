#!/usr/bin/env node
'use strict';
// Exact two-geometry preflight for the frozen next 32 N11 nine-stone roots.
// This checks move boundaries, not terminal outcomes.
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const independent=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const fail=(ok,msg)=>{if(!ok)throw Error(msg)};
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const plan=JSON.parse(fs.readFileSync(path.join(__dirname,'next-plan.json'),'utf8'));
const roots=plan.newSelectedKeys;
fail(plan.schema==='n11-post-round11-proof-only-replan-v1'&&plan.emptyBoard==='UNKNOWN'&&
  plan.conditionalUnprovedEdges===79&&plan.eligibleUnprovedS9===638&&
  roots.length===32&&new Set(roots).size===32&&
  sha(roots.join('\n')+'\n')===plan.newSelectionSha256,'frozen selection mismatch');
const occurrences=new Map();
let edges=0;
for(const root of roots){
  fail(/^[0-9a-f]{32}$/.test(root)&&g.pts(BigInt('0x'+root)).length===9,
    'invalid nine-stone root '+root);
  const first=g.children(g.board(root,9));
  const second=independent.children4(root);
  fail(first.size===second.size&&[...first].every(h=>second.has(h)),
    '3x3 / 4x4 exact geometry mismatch at '+root);
  edges+=first.size;
  for(const child of first){
    if(!occurrences.has(child))occurrences.set(child,[]);
    occurrences.get(child).push(root);
  }
}
const overlaps=[...occurrences].filter(([,r])=>r.length>1)
  .map(([child,r])=>({child,parents:r})).sort((a,b)=>a.child.localeCompare(b.child));
fail(edges===807&&occurrences.size===805&&overlaps.length===2&&
  overlaps.every(x=>x.parents.length===2),'unexpected cross-root S10 overlap');
const result={
  schema:'n11-post-round11-independent-boundary-preflight-v1',
  emptyBoard:'UNKNOWN',selectionSha256:plan.newSelectionSha256,
  roots:roots.length,legalS10Edges:edges,distinctS10Classes:occurrences.size,
  repeatedS10Classes:overlaps.length,sharedChildren:overlaps,
  geometryChecks:['3x3-difference-determinant','4x4-independent-integer-determinant'],
  terminalVerdicts:0,newTwoStoneClosures:0
};
console.log(JSON.stringify(result,null,2));
