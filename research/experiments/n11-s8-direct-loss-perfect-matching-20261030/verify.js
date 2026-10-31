#!/usr/bin/env node
'use strict';
// Two independent exact integer geometries: 3x3 differences and 4x4 Bareiss.
const fs = require('node:fs'), path = require('node:path'), crypto = require('node:crypto');
const g = require('../n11-gap6-terminal-20261019/verify_js.js');
const ind = require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need = (x, message) => { if (!x) throw Error(message); };
const same = (a,b) => a.size === b.size && [...a].every(x=>b.has(x));
function verify(c) {
  need(c.schema==='n11-s8-loss-perfect-matching-v1' && c.board===11 &&
    c.emptyBoard==='UNKNOWN' && c.s8Verdict==='LOSS','bad certificate header');
  const root=g.board(c.s8,8), s9=[...g.children(root)].sort();
  need(s9.length===c.s9LegalCount && s9.length===36 &&
    same(new Set(s9),ind.children4(c.s8)),'incorrect complete S9 boundary');
  const incidence=new Map();
  for(let i=0;i<s9.length;i++) {
    const h=s9[i], a=g.children(g.board(h,9)), b=ind.children4(h);
    need(same(a,b),'independent S10 boundary mismatch '+h);
    for(const child of a) {
      if(!incidence.has(child))incidence.set(child,new Set());
      incidence.get(child).add(i);
    }
  }
  need(incidence.size===c.s10BoundaryDistinct && incidence.size===480,
    'incorrect distinct S10 boundary');
  need([...incidence.values()].every(v=>v.size===c.s10ParentDegree &&
    v.size===2),'wrong S10 incidence degree');
  need(Array.isArray(c.s10Witnesses) && c.s10Witnesses.length===18 &&
    c.selectedLossLeaves===18,'wrong witness count');
  const seen=new Set(),covered=new Set();let states=0;
  for(const row of c.s10Witnesses) {
    need(!seen.has(row.s10) && incidence.has(row.s10),'invalid LOSS10 witness');
    seen.add(row.s10);
    const a=g.solve10(row.s10),b=ind.solve4(row.s10);
    need(!a.win && !b.win && a.states===b.states && a.legal===b.legal,
      'independent terminal LOSS10 disagreement '+row.s10);
    need(a.states===row.terminalStates && a.legal===row.legalMoves,
      'terminal replay count mismatch '+row.s10);
    for(const i of incidence.get(row.s10)) {
      need(!covered.has(i),'matching overlaps');
      covered.add(i);
    }
    states+=a.states;
  }
  need(covered.size===36 && states===c.selectedTerminalStates && states===5240,
    'uncovered S9 child or terminal-state regression');
  const parents=[...g.reverse([c.s8])].sort();
  need(parents.length===c.s7ParentCount && parents.length===8,
    'wrong S7 parent count');
  for(const h of parents)need(g.children(g.board(h,7)).has(c.s8) &&
    ind.children4(h).has(c.s8),'S7 parent incidence mismatch');
  const digest=crypto.createHash('sha256').update(parents.join('\n')+'\n').digest('hex');
  need(digest===c.s7ParentSha256,'wrong S7 parent digest');
  return {verified:true,independentGeometries:2,s8:c.s8,s8Verdict:'LOSS',
    s9AllChildren:s9.length,loss10Witnesses:seen.size,
    terminalStatesPerGeometry:states,derivedS7LossParents:parents.length,
    emptyBoard:'UNKNOWN'};
}
function negative(c) {
  for(const mutate of [
    x=>x.s10Witnesses[0].s10=x.s10Witnesses[1].s10,
    x=>x.s10Witnesses[0].terminalStates++,
    x=>x.s10Witnesses[0].legalMoves++,
    x=>x.s10Witnesses.pop(),
    x=>x.s8='0'.repeat(32),
    x=>x.s7ParentSha256='0'.repeat(64)
  ]) {
    const forged=structuredClone(c);mutate(forged);
    let rejected=false;try{verify(forged)}catch(_){rejected=true;}
    need(rejected,'forged certificate accepted');
  }
}
if(require.main===module) {
  const cert=JSON.parse(fs.readFileSync(path.join(__dirname,'certificate.json'),'utf8'));
  const result=verify(cert);
  if(process.argv.includes('--negative'))negative(cert);
  console.log(JSON.stringify(result,null,2));
}
module.exports={verify};
