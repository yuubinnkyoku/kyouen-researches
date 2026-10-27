#!/usr/bin/env node
'use strict';
// Exhaust the remaining shared 23-child S9 candidates touching the saved
// 14-root proof-only S8 frontier. All verdicts are terminal-replayed in two
// integer geometries; a missing certificate is allowed ONLY with --propose.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const n22=require('../n11-s9-n22-complete-20261027/verify.js');
const n23=require('../n11-s9-n23-priority-20261027/prove.js');
const need=(x,m)=>{if(!x)throw Error(m);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function run(){
  const prev=n23.run(); // Replays n22 and n23 terminal proofs before adoption.
  need(prev.win9===21&&prev.loss9===235&&
    prev.proofOnlyWin8After===5120&&prev.updated.missing===144,
    'upstream n23 proof changed');
  const {plan,plan8,by9,candidates}=n22.inventory();
  const {before,loss}=n22.priorProofs();
  const n22Cert=JSON.parse(fs.readFileSync(path.join(__dirname,
    '../n11-s9-n22-complete-20261027/compact-certificate.json'),'utf8'));
  const n22Bytes=Buffer.from(n22Cert.witnessBase64,'base64');
  need(n22Bytes.length===candidates.length,'n22 witness length changed');
  const win22=candidates.filter((_,i)=>n22Bytes[i]===255);
  const secured22=new Set([...before,...g.reverse(win22)]);
  need(secured22.size===4944,'n22 proof-only coverage changed');
  const choices=[];
  for(const [h,parents] of by9){
    if(parents.size<2||g.children(g.board(h,9)).size!==23)continue;
    const gaps=[...parents].filter(p=>plan8.has(p)&&!secured22.has(p)).length;
    choices.push({h,degree:parents.size,gaps});
  }
  choices.sort((a,b)=>b.gaps-a.gaps||b.degree-a.degree||
    (a.h<b.h?-1:a.h>b.h?1:0));
  const positive=choices.filter(x=>x.gaps>0);
  const first=positive.slice(0,256),remaining=positive.slice(256);
  need(choices.length===877&&positive.length===445&&
    first.length===256&&remaining.length===189,
    '23-child candidate boundary changed');
  need(sha(first.map(x=>x.h).join('\n')+'\n')===prev.selectionSha256,
    'n23 selected candidate order changed');
  const n23Cert=JSON.parse(fs.readFileSync(path.join(__dirname,
    '../n11-s9-n23-priority-20261027/compact-certificate.json'),'utf8'));
  const bytes=Buffer.from(n23Cert.witnessBase64,'base64');
  need(bytes.length===first.length,'n23 witness length changed');
  const win23=first.filter((_,i)=>bytes[i]===255).map(x=>x.h);
  const secured23=new Set([...secured22,...g.reverse(win23)]);
  need(secured23.size===5120&&[...secured23].every(x=>!loss.has(x)),
    'n23 WIN8 coverage conflict');
  const fresh=remaining.map(x=>({...x,
    currentGaps:[...by9.get(x.h)].filter(p=>plan8.has(p)&&!secured23.has(p)).length
  })).filter(x=>x.currentGaps>0);
  fresh.sort((a,b)=>b.currentGaps-a.currentGaps||
    b.degree-a.degree||(a.h<b.h?-1:a.h>b.h?1:0));
  const leafCache=new Map(),witness=[],win9=[],loss9=[];
  let states=0,winEdges=0;
  function terminal(h){
    if(leafCache.has(h))return leafCache.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
      'terminal geometry mismatch '+h);
    leafCache.set(h,a);return a;
  }
  for(const {h} of fresh){
    const kids=g.children(g.board(h,9));
    need(kids.size===23&&same(kids,ind.children4(h)),
      'S9 geometry mismatch '+h);
    const ordered=[...kids].sort();
    let firstLoss=-1;
    for(let i=0;i<ordered.length;i++){
      const r=terminal(ordered[i]);states+=r.states;
      if(!r.win&&firstLoss<0)firstLoss=i;
    }
    if(firstLoss<0){
      win9.push(h);winEdges+=23;witness.push(255);
      for(const p of g.reverse([h]))
        need(g.children(g.board(p,8)).has(h)&&ind.children4(p).has(h),
          'reverse geometry mismatch '+h);
    }else{loss9.push(h);witness.push(firstLoss);}
  }
  const derived=g.reverse(win9);
  need([...derived].every(x=>!loss.has(x)),'S8 WIN/LOSS conflict');
  const after=new Set([...secured23,...derived]);
  const evaluate=proof=>{
    let total=0,secured=0;const missing=new Set();
    for(const h of plan)for(const c of g.children(g.board(h,7))){
      total++;if(proof.has(c))secured++;else missing.add(c);
    }
    return {total,secured,missing:total-secured,distinctMissing:missing.size};
  };
  const previous=evaluate(secured23),updated=evaluate(after);
  need(previous.total===548&&previous.secured===404&&previous.missing===144&&
    updated.missing<=144,'14-root frontier changed or regressed');
  const raw=Buffer.from(witness);
  const cert={format:'n11-s9-n23-remaining-terminal-v1',board:11,
    perspective:'original-first-player',emptyBoard:'UNKNOWN',
    originalCandidates:choices.length,originalPositive:positive.length,
    previouslySelected:first.length,remainingCandidates:remaining.length,
    currentPositive:fresh.length,
    selectionSha256:sha(fresh.map(x=>x.h).join('\n')+'\n'),
    witnessBase64:raw.toString('base64'),witnessSha256:sha(raw),
    win9:win9.length,loss9:loss9.length,win10Edges:winEdges,
    independentTerminalLeaves:leafCache.size,
    terminalStatesPerGeometry:states,derivedWin8:derived.size,
    newProofOnlyWin8:after.size-secured23.size,
    proofOnlyWin8Before:secured23.size,proofOnlyWin8After:after.size,
    knownLoss8:loss.size,previous,updated,winLossConflicts:0,
    newS7Verdicts:0,newS5Verdicts:0,twoStoneClosures:0};
  const certPath=path.join(__dirname,'compact-certificate.json');
  if(process.argv.includes('--propose')){
    console.log(JSON.stringify(cert,null,2));
  }else{
    const frozen=JSON.parse(fs.readFileSync(certPath,'utf8'));
    need(JSON.stringify(frozen)===JSON.stringify(cert),
      'frozen terminal certificate differs from independently replayed results');
    if(process.argv.includes('--negative')){
      const check=arr=>{
        for(let i=0;i<fresh.length;i++){
          const kids=[...g.children(g.board(fresh[i].h,9))].sort();
          const index=arr[i];
          if(index===255)need(kids.every(k=>leafCache.get(k)?.win),
            'false WIN10 leaf');
          else need(index<23&&leafCache.get(kids[index])?.win===false,
            'false LOSS10 leaf');
        }
      };
      check(raw);
      const w=witness.findIndex(x=>x===255),l=witness.findIndex(x=>x!==255);
      need(w>=0&&l>=0,'negative test requires both verdicts');
      for(const [i,b,expected] of [[w,0,'false LOSS10 leaf'],
        [l,255,'false WIN10 leaf']]){
        const bad=Buffer.from(raw);bad[i]=b;
        let err=null;try{check(bad);}catch(e){err=e;}
        need(err&&err.message===expected,'forged verdict not rejected');
      }
    }
    console.log(JSON.stringify({verified:true,...cert},null,2));
  }
  return cert;
}
if(require.main===module)run();
module.exports={run};
