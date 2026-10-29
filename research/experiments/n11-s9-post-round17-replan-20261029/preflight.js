#!/usr/bin/env node
'use strict';
// Independent, exact 3x3 vs 4x4 geometry audit of round18's frozen S9 roots.
// Neither legal move counts nor prospective coverage imply any WIN/LOSS verdict.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const plan=read('next-plan.json'),roots=plan.newSelectedKeys;
const prior=read('../n11-s9-post-round16-round17-20261029/certificate.json');
need(plan.schema==='n11-post-round17-proof-only-replan-v1'&&
  plan.emptyBoard==='UNKNOWN'&&plan.conditionalUnprovedEdges===45&&
  plan.proofOnlyWin8After===5795&&plan.eligibleBeforeRound17===158&&
  plan.excludedByRound17Proof===22&&plan.noLongerTouchesUnprovedS8===20&&
  plan.eligibleUnprovedS9===116&&plan.undominatedS9===14&&
  plan.potentialCoverage===14&&plan.selectedCount===14&&roots.length===14&&
  plan.sourceSelectionSha256===prior.selectionSha256&&
  plan.sourceWitnessSha256===prior.witnessSha256&&
  new Set(roots).size===14&&
  sha(roots.join('\n')+'\n')===plan.newSelectionSha256,
  'round18 selection/certificate mismatch');
let edges=0;
const occurrences=new Map();
for(const root of roots){
  const b=g.board(root,9),first=g.children(b),second=ind.children4(root);
  need(first.size===second.size&&[...first].every(h=>second.has(h)),
    'independent 3x3/4x4 boundary mismatch '+root);
  edges+=first.size;
  for(const child of first){
    if(!occurrences.has(child))occurrences.set(child,[]);
    occurrences.get(child).push(root);
  }
}
need(edges===plan.legal10Children,'round18 S10 child count mismatch');
const overlaps=[...occurrences].filter(([,parents])=>parents.length>1)
  .map(([child,parents])=>({child,parents:parents.sort()}))
  .sort((a,b)=>a.child.localeCompare(b.child));
const result={
  schema:'n11-post-round17-independent-boundary-preflight-v1',
  emptyBoard:'UNKNOWN',selectionSha256:plan.newSelectionSha256,
  roots:roots.length,legalS10Edges:edges,
  distinctS10Classes:occurrences.size,repeatedS10Classes:overlaps.length,
  crossRootSavings:edges-occurrences.size,sharedChildren:overlaps,
  geometryChecks:['3x3-difference-determinant','4x4-independent-integer-determinant'],
  terminalVerdicts:0,newTwoStoneClosures:0
};
need(JSON.stringify(result)===JSON.stringify(read('preflight.json')),
  'frozen round18 independent boundary mismatch');
console.log(JSON.stringify(result,null,2));
module.exports={result};
