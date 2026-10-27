#!/usr/bin/env node
'use strict';
// Minimal independent terminal replay of a frozen 32-position S9 certificate.
// WIN9: all legal S10 children WIN. LOSS9: one fixed S10 LOSS child.
// Uses independent 3x3 and 4x4 integer geometry; no solver verdict cache.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const {inventory,coverage}=require('./prove.js');
const need=(v,m)=>{if(!v)throw Error(m);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function verify(){
  const {s,p,selected,secured}=inventory();
  const cert=JSON.parse(fs.readFileSync(path.join(__dirname,
    'compact-certificate.json'),'utf8'));
  need(cert.format==='n11-s9-n24-round3-terminal-v1'&&
    cert.board===11&&cert.perspective==='original-first-player'&&
    cert.emptyBoard==='UNKNOWN'&&cert.selected===32,
    'invalid certificate header');
  const raw=Buffer.from(cert.witnessBase64,'base64');
  need(raw.length===selected.length&&sha(raw)===cert.witnessSha256&&
    sha(selected.map(x=>x.h).join('\n')+'\n')===cert.selectionSha256&&
    p.selectedKeysSha256===cert.plannerSelectedKeysSha256,
    'certificate order/digest mismatch');
  const terminalCache=new Map();
  let states=0,obligations=0,winEdges=0;
  function terminal(h){
    if(terminalCache.has(h))return terminalCache.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
      'independent terminal disagreement '+h);
    terminalCache.set(h,a);states+=a.states;
    return a;
  }
  function verifyOne(row,claim){
    const children=g.children(g.board(row.h,9));
    need(children.size===row.children&&
      same(children,ind.children4(row.h)),
      'independent legal S9 child boundary mismatch '+row.h);
    const ordered=[...children].sort();
    if(claim===255){
      for(const h of ordered)need(terminal(h).win,
        'false WIN9 universal child '+row.h);
      return {win:true,obligations:ordered.length};
    }
    need(Number.isInteger(claim)&&claim>=0&&claim<ordered.length,
      'invalid LOSS9 witness index');
    need(!terminal(ordered[claim]).win,
      'false LOSS9 witness '+row.h);
    return {win:false,obligations:1};
  }
  const win9=[];
  for(let i=0;i<selected.length;i++){
    const result=verifyOne(selected[i],raw[i]);
    obligations+=result.obligations;
    if(result.win){
      win9.push(selected[i].h);winEdges+=result.obligations;
    }
  }
  need(win9.length===cert.win9&&selected.length-win9.length===cert.loss9&&
    winEdges===cert.win10Edges&&obligations===winEdges+cert.loss9,
    'minimal witness count mismatch');
  for(const h of win9)for(const parent of g.reverse([h]))
    need(g.children(g.board(parent,8)).has(h)&&
      ind.children4(parent).has(h),
      'independent reverse S8 incidence mismatch '+h);
  const derived=g.reverse(win9);
  need([...derived].every(h=>!s.loss.has(h)),'WIN8/LOSS8 conflict');
  const after=new Set([...secured,...derived]);
  const before=coverage(s.plan,secured),updated=coverage(s.plan,after);
  need(before.total===548&&before.missing===118&&
    JSON.stringify(before)===JSON.stringify(cert.previous)&&
    JSON.stringify(updated)===JSON.stringify(cert.updated)&&
    derived.size===cert.derivedWin8&&
    after.size-secured.size===cert.newProofOnlyWin8&&
    after.size===cert.proofOnlyWin8After,
    'proof-only propagation/coverage mismatch');
  if(process.argv.includes('--negative')){
    const wi=raw.indexOf(255),li=raw.findIndex(x=>x!==255);
    if(wi>=0){
      let rejected=false;
      try{verifyOne(selected[wi],0);}catch(_){rejected=true;}
      need(rejected,'forged LOSS9 accepted');
    }
    if(li>=0){
      let rejected=false;
      try{verifyOne(selected[li],255);}catch(_){rejected=true;}
      need(rejected,'forged WIN9 accepted');
    }
    let rejected=false;
    try{verifyOne(selected[0],254);}catch(_){rejected=true;}
    need(rejected,'out-of-range witness accepted');
  }
  const result={verified:true,emptyBoard:'UNKNOWN',
    checkedS9:selected.length,win9:win9.length,loss9:selected.length-win9.length,
    minimalTerminalObligations:obligations,
    distinctTerminalLeaves:terminalCache.size,
    terminalStatesPerGeometry:states,
    newProofOnlyWin8:after.size-secured.size,
    updated,winLossConflicts:0,twoStoneClosures:0};
  console.log(JSON.stringify(result,null,2));
  return result;
}
if(require.main===module)verify();
module.exports={verify};
