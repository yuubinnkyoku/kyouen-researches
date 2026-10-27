#!/usr/bin/env node
'use strict';
// Independent minimal terminal replay: all children of a WIN9 and one
// explicit LOSS10 child of each LOSS9. Never trusts the exploratory census.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const {selection}=require('./prove.js');
const need=(v,m)=>{if(!v)throw Error(m);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function verify(negative=false){
  const s=selection();
  const cert=JSON.parse(fs.readFileSync(path.join(__dirname,
    'compact-certificate.json'),'utf8'));
  const witness=Buffer.from(cert.witnessBase64,'base64');
  need(cert.format==='n11-s9-n24-round2-terminal-v1'&&cert.board===11&&
    cert.perspective==='original-first-player'&&cert.emptyBoard==='UNKNOWN'&&
    cert.currentCandidateCount===s.currentCandidateCount&&
    cert.selected===s.selected.length&&cert.potentiallyCoveredS8===s.covered.size&&
    sha(s.selected.map(x=>x.h).join('\n')+'\n')===cert.selectionSha256&&
    witness.length===s.selected.length&&
    witness.toString('base64')===cert.witnessBase64&&
    sha(witness)===cert.witnessSha256,'frozen selection/witness integrity');
  const cache=new Map(),wins=[],losses=[];
  let obligations=0,states=0,winEdges=0;
  function terminal(h){
    if(cache.has(h))return cache.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
      'independent terminal geometry disagreement '+h);
    cache.set(h,a);states+=a.states;return a;
  }
  function checkClaim(i,claim){
    const h=s.selected[i].h;
    const kids=g.children(g.board(h,9));
    need(kids.size===s.selected[i].children&&same(kids,ind.children4(h)),
      'independent S9 child boundary disagreement '+h);
    const ordered=[...kids].sort();
    if(claim===255){
      for(const leaf of ordered){
        obligations++;
        need(terminal(leaf).win,'false WIN9 claim '+h);
      }
      for(const p of g.reverse([h]))
        need(g.children(g.board(p,8)).has(h)&&ind.children4(p).has(h),
          'independent reverse incidence disagreement '+h);
      return true;
    }
    need(Number.isInteger(claim)&&claim>=0&&claim<ordered.length,
      'invalid LOSS9 witness index');
    obligations++;
    need(!terminal(ordered[claim]).win,'false LOSS9 claim '+h);
    return false;
  }
  for(let i=0;i<s.selected.length;i++){
    if(checkClaim(i,witness[i])){
      wins.push(s.selected[i].h);winEdges+=s.selected[i].children;
    }else losses.push(s.selected[i].h);
  }
  const positive={obligations,leaves:cache.size,states};
  need(wins.length===cert.win9&&losses.length===cert.loss9&&
    winEdges===cert.win10Edges&&wins.length===1&&losses.length===31&&
    positive.obligations===55&&
    positive.obligations<=cert.firstLossSearchObligations&&
    positive.leaves<=cert.uniqueTerminalLeaves&&
    positive.states<=cert.terminalStatesPerGeometry,
    'frozen proof-only census');
  const derived=g.reverse(wins);
  need(derived.size===cert.derivedWin8&&[...derived].every(h=>!s.loss.has(h)),
    'WIN8/LOSS8 conflict');
  const after=new Set([...s.secured,...derived]);
  need(after.size===cert.proofOnlyWin8After&&
    after.size-s.secured.size===cert.newProofOnlyWin8,
    'derived WIN8 census');
  function coverage(proofs){
    let total=0,secured=0;const absent=new Set();
    for(const h of s.plan)for(const k of g.children(g.board(h,7))){
      total++;if(proofs.has(k))secured++;else absent.add(k);
    }
    return {total,secured,missing:total-secured,distinctMissing:absent.size};
  }
  need(JSON.stringify(coverage(s.secured))===JSON.stringify(cert.previous)&&
    JSON.stringify(coverage(after))===JSON.stringify(cert.updated)&&
    cert.updated.missing===118,'conditional 14-root coverage');
  if(negative){
    const w=witness.indexOf(255),l=witness.findIndex(x=>x!==255);
    need(w>=0&&l>=0,'both terminal polarities required');
    for(const [i,claim] of [[w,0],[l,255],[l,254]]){
      let rejected=false;
      try{checkClaim(i,claim);}catch(_){rejected=true;}
      need(rejected,'forged terminal claim accepted');
    }
  }
  return {verified:true,selectedS9:s.selected.length,win9:wins.length,
    loss9:losses.length,minimalTerminalObligations:positive.obligations,
    uniqueTerminalLeaves:positive.leaves,terminalStatesPerGeometry:positive.states,
    originalProbeObligations:cert.firstLossSearchObligations,
    proofOnlyWin8:after.size,unprovedPlanEdges:cert.updated.missing,
    winLossConflicts:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module)
  console.log(JSON.stringify(verify(process.argv.includes('--negative')),null,2));
module.exports={verify};
