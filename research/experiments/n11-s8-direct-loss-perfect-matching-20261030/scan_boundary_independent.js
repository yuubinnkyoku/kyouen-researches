#!/usr/bin/env node
'use strict';
// Independently replay every S10 leaf in the complete S8 boundary.
// The original Python scan is not used as an oracle: both JS integer
// geometries solve each leaf from scratch and must agree per position.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const independent=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const here=__dirname;
const cert=JSON.parse(fs.readFileSync(path.join(here,'certificate.json'),'utf8'));
const frozen=JSON.parse(fs.readFileSync(path.join(here,'full_boundary_scan.json'),'utf8'));
function need(ok,message){if(!ok)throw Error(message);}
function same(a,b){return a.size===b.size&&[...a].every(k=>b.has(k));}
function run(){
  need(cert.schema==='n11-s8-loss-perfect-matching-v1' &&
    cert.emptyBoard==='UNKNOWN' && cert.s8Verdict==='LOSS','certificate header');
  const s9=[...g.children(g.board(cert.s8,8))].sort();
  need(s9.length===36 && same(new Set(s9),independent.children4(cert.s8)),
    'independent S9 boundary mismatch');
  const incidence=new Map();
  for(const parent of s9){
    const a=g.children(g.board(parent,9));
    const b=independent.children4(parent);
    need(same(a,b),'independent S10 boundary mismatch: '+parent);
    for(const child of a){
      if(!incidence.has(child))incidence.set(child,new Set());
      incidence.get(child).add(parent);
    }
  }
  need(incidence.size===480 && [...incidence.values()].every(v=>v.size===2),
    'S10 incidence regression');
  let win10=0,loss10=0,states=0;
  const lossKeys=[],loss9=new Set();
  for(const h of [...incidence.keys()].sort()){
    const a=g.solve10(h),b=independent.solve4(h);
    need(a.win===b.win && a.states===b.states && a.legal===b.legal,
      'independent terminal verdict/count conflict: '+h);
    states+=a.states;
    if(a.win)win10++;
    else {
      loss10++;lossKeys.push(h);
      for(const parent of incidence.get(h))loss9.add(parent);
    }
  }
  need(win10===399 && loss10===81,'full S10 verdict totals changed');
  need(loss9.size===36,'some S9 child lacks a LOSS10 reply');
  const selected=new Set(cert.s10Witnesses.map(x=>x.s10));
  need(selected.size===18 && [...selected].every(h=>lossKeys.includes(h)),
    'selected LOSS10 witness not in independently replayed LOSS set');
  const lossParents=g.reverse(lossKeys);
  const digest=crypto.createHash('sha256').update(lossKeys.join('\n')+'\n').digest('hex');
  const report={schema:'n11-s8-loss-full-s10-independent-js-v1',
    s8:cert.s8,legal9:s9.length,legal10Edges:960,distinct10:incidence.size,
    win10,loss10,loss9Covered:loss9.size,loss9ParentClosure:lossParents.size,
    loss10KeysSha256:digest,terminalStatesPerGeometry:states,
    geometries:['3x3-differences','4x4-Bareiss'],emptyBoard:'UNKNOWN'};
  for(const key of ['s8','legal9','legal10Edges','distinct10','win10','loss10','emptyBoard'])
    need(report[key]===frozen[key],'Python frozen scan mismatch: '+key);
  need(frozen.selectedLoss10===selected.size,'selected count mismatch');
  console.log(JSON.stringify(report,null,2));
  if(process.argv.includes('--emit-closure'))
    console.log('CLOSURE_JSON='+JSON.stringify({loss10Keys:lossKeys,
      loss9ParentKeys:[...lossParents].sort()}));
  return report;
}
if(require.main===module)run();
module.exports={run};
