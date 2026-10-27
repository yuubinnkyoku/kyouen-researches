#!/usr/bin/env node
'use strict';
// Verify frozen 24+ child S9 claims with only the necessary terminal leaves:
// all children for WIN9, one fixed LOSS10 witness for LOSS9.
// Upstream certificates are integrity-checked by source(); their own terminal
// verification remains an independent prerequisite.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const {source}=require('./prove.js');
const need=(x,m)=>{if(!x)throw Error(m);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function verify(negative=false){
  const s=source();
  const cert=JSON.parse(fs.readFileSync(path.join(__dirname,'compact-certificate.json'),'utf8'));
  const bytes=Buffer.from(cert.witnessBase64,'base64');
  need(cert.format==='n11-s9-n24-targeted-terminal-v1'&&cert.board===11&&
    cert.perspective==='original-first-player'&&cert.emptyBoard==='UNKNOWN'&&
    cert.selected===s.selected.length&&cert.candidateCount===s.options.length&&
    cert.potentiallyCoveredS8===s.covered.size&&
    JSON.stringify(cert.childHistogram)===JSON.stringify(s.hist)&&
    sha(s.selected.map(x=>x.h).join('\n')+'\n')===cert.selectionSha256&&
    bytes.length===s.selected.length&&bytes.toString('base64')===cert.witnessBase64&&
    sha(bytes)===cert.witnessSha256,'frozen candidate/witness integrity');
  const cache=new Map(),win9=[],loss9=[];
  let obligations=0,states=0,winEdges=0;
  function terminal(h){
    if(cache.has(h))return cache.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
      'independent terminal disagreement '+h);
    cache.set(h,a);states+=a.states;return a;
  }
  function checkClaim(i,claim){
    const h=s.selected[i].h;
    const kids=g.children(g.board(h,9));
    need(kids.size===s.selected[i].children&&same(kids,ind.children4(h)),
      'independent S9 child boundary mismatch '+h);
    const ordered=[...kids].sort();
    if(claim===255){
      for(const leaf of ordered){
        obligations++;
        need(terminal(leaf).win,'false WIN10 leaf '+leaf);
      }
      for(const parent of g.reverse([h]))
        need(g.children(g.board(parent,8)).has(h)&&ind.children4(parent).has(h),
          'S8 reverse incidence mismatch '+h);
      return true;
    }
    need(Number.isInteger(claim)&&claim>=0&&claim<ordered.length,
      'invalid LOSS witness index');
    obligations++;
    need(!terminal(ordered[claim]).win,'false LOSS10 leaf '+ordered[claim]);
    return false;
  }
  for(let i=0;i<s.selected.length;i++){
    if(checkClaim(i,bytes[i])){
      win9.push(s.selected[i].h);
      winEdges+=s.selected[i].children;
    }else loss9.push(s.selected[i].h);
  }
  const positive={obligations,leaves:cache.size,states};
  need(win9.length===cert.win9&&loss9.length===cert.loss9&&
    winEdges===cert.win10Edges&&win9.length===3&&loss9.length===29,
    'frozen S9 verdict census');
  const derived=g.reverse(win9);
  need(derived.size===cert.derivedWin8&&[...derived].every(h=>!s.loss.has(h)),
    'S8 WIN/LOSS conflict');
  const after=new Set([...s.secured,...derived]);
  need(after.size===cert.proofOnlyWin8After&&
    after.size-s.secured.size===cert.newProofOnlyWin8,
    'proof-only S8 WIN census');
  function coverage(proofs){
    let total=0,secured=0;const missing=new Set();
    for(const h of s.plan)for(const k of g.children(g.board(h,7))){
      total++;if(proofs.has(k))secured++;else missing.add(k);
    }
    return {total,secured,missing:total-secured,distinctMissing:missing.size};
  }
  need(JSON.stringify(coverage(s.secured))===JSON.stringify(cert.previous)&&
    JSON.stringify(coverage(after))===JSON.stringify(cert.updated)&&
    cert.updated.missing===120,'14-root proof-only coverage');
  if(negative){
    const w=bytes.indexOf(255),l=bytes.findIndex(x=>x!==255);
    need(w>=0&&l>=0,'both polarities required');
    for(const [i,claim] of [[w,0],[l,255]]){
      let rejected=false;
      try{checkClaim(i,claim);}catch(_){rejected=true;}
      need(rejected,'forged terminal polarity accepted');
    }
  }
  return {verified:true,selectedS9:s.selected.length,win9:win9.length,
    loss9:loss9.length,win10Edges:winEdges,
    minimalTerminalObligations:positive.obligations,
    uniqueTerminalLeaves:positive.leaves,
    terminalStatesPerGeometry:positive.states,
    originalProbeObligations:cert.terminalObligations,
    proofOnlyWin8:after.size,unprovedPlanEdges:cert.updated.missing,
    winLossConflicts:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module)
  console.log(JSON.stringify(verify(process.argv.includes('--negative')),null,2));
module.exports={verify};