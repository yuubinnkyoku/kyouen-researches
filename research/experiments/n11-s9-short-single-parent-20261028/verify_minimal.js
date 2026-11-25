#!/usr/bin/env node
'use strict';
// Independent minimal replay of the 64 frozen short-child S9 LOSS claims.
// Exactly one terminal LOSS10 witness is necessary for each S9 LOSS.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const {inventory}=require('./prove.js');
const need=(x,m)=>{if(!x)throw Error(m);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function verify(negative=false){
  const s=inventory(),cert=JSON.parse(fs.readFileSync(
    path.join(__dirname,'compact-certificate.json'),'utf8'));
  const bytes=Buffer.from(cert.witnessBase64,'base64');
  need(cert.format==='n11-s9-short-single-parent-terminal-v1'&&
    cert.board===11&&cert.emptyBoard==='UNKNOWN'&&
    cert.candidateCount===s.short.length&&cert.selected===64&&
    cert.potentiallyCoveredS8===s.covered.size&&
    sha(s.selected.map(x=>x.h).join('\n')+'\n')===cert.selectionSha256&&
    bytes.length===64&&bytes.toString('base64')===cert.witnessBase64&&
    sha(bytes)===cert.witnessSha256,'frozen certificate integrity');
  const cache=new Map();let states=0,obligations=0;
  function terminal(h){
    if(cache.has(h))return cache.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
      'independent terminal geometry mismatch '+h);
    cache.set(h,a);states+=a.states;return a;
  }
  function check(i,claim){
    const h=s.selected[i].h;
    const kids=g.children(g.board(h,9));
    need(kids.size===s.selected[i].children&&same(kids,ind.children4(h)),
      'independent S9 boundary mismatch '+h);
    const ordered=[...kids].sort();
    if(claim===255){
      for(const leaf of ordered){
        obligations++;
        need(terminal(leaf).win,'false WIN9 '+h);
      }
      return true;
    }
    need(Number.isInteger(claim)&&claim>=0&&claim<ordered.length,
      'invalid LOSS witness');
    obligations++;
    need(!terminal(ordered[claim]).win,'false LOSS9 '+h);
    return false;
  }
  for(let i=0;i<64;i++)need(check(i,bytes[i])===false,
    'unexpected WIN9 claim');
  const positive={obligations,leaves:cache.size,states};
  need(cert.win9===0&&cert.loss9===64&&cert.proofOnlyWin8Before===5317&&
    cert.proofOnlyWin8After===5317&&cert.newProofOnlyWin8===0&&
    cert.previous.missing===120&&cert.updated.missing===120,
    'unexpected frontier changes');
  if(negative){
    let rejected=false;
    try{check(0,255);}catch(_){rejected=true;}
    need(rejected,'forged WIN9 accepted');
  }
  return {verified:true,selectedS9:64,loss9:64,
    minimalTerminalObligations:positive.obligations,
    uniqueTerminalLeaves:positive.leaves,
    terminalStatesPerGeometry:positive.states,
    firstLossSearchObligations:cert.firstLossSearchObligations,
    proofOnlyWin8:5317,unprovedPlanEdges:120,
    winLossConflicts:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module)
  console.log(JSON.stringify(verify(process.argv.includes('--negative')),null,2));
module.exports={verify};