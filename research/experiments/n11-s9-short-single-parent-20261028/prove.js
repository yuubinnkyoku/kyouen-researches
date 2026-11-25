#!/usr/bin/env node
'use strict';
// Reuse the verified 24+ child frontier and prioritize cheaper, still-unproved
// S9 witnesses with 10..21 legal S10 children. All terminal verdicts are
// recomputed by two independent integer geometries; no incomplete cache.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const {source}=require('../n11-s9-n24-priority-20261028/prove.js');
const need=(x,m)=>{if(!x)throw Error(m);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function inventory(){
  const s=source(),c24=read('../n11-s9-n24-priority-20261028/compact-certificate.json');
  const bytes=Buffer.from(c24.witnessBase64,'base64');
  need(c24.selected===s.selected.length&&
    sha(s.selected.map(x=>x.h).join('\n')+'\n')===c24.selectionSha256&&
    sha(bytes)===c24.witnessSha256&&bytes.length===s.selected.length&&
    c24.win9===3&&c24.loss9===29,'24+ certificate integrity');
  const win24=s.selected.filter((_,i)=>bytes[i]===255).map(x=>x.h);
  const secured=new Set([...s.secured,...g.reverse(win24)]);
  need(secured.size===5317&&[...secured].every(h=>!s.loss.has(h)),
    '24+ proof-only coverage changed');
  const missing=new Set([...s.plan8].filter(h=>!secured.has(h)));
  need(missing.size===120,'remaining S8 frontier changed');
  const short=s.shortOptions.map(x=>({...x,
    hits:x.hits.filter(h=>missing.has(h))})).filter(x=>x.hits.length>0);
  short.sort((a,b)=>a.children-b.children||b.hits.length-a.hits.length||
    b.degree-a.degree||(a.h<b.h?-1:a.h>b.h?1:0));
  const selected=[],covered=new Set(),used=new Set();
  // First pass: cover as many different unproved S8 parents as possible,
  // breaking ties by fewer terminal children.
  for(const x of short){
    if(selected.length>=64)break;
    if(!x.hits.some(h=>!covered.has(h)))continue;
    selected.push(x);used.add(x.h);
    for(const h of x.hits)covered.add(h);
  }
  // Second pass: extra independent witnesses for remaining difficult parents.
  for(const x of short){
    if(selected.length>=64)break;
    if(used.has(x.h))continue;
    selected.push(x);used.add(x.h);
    for(const h of x.hits)covered.add(h);
  }
  need(selected.length===64,'fewer than 64 short S9 candidates');
  return {...s,secured,missing,short,selected,covered};
}
function run(){
  const s=inventory(),cache=new Map(),claims=[],win9=[],loss9=[];
  let states=0,attempted=0,winEdges=0;
  function terminal(h){
    if(cache.has(h))return cache.get(h);
    const a=g.solve10(h),b=ind.solve4(h);
    need(a.win===b.win&&a.states===b.states&&a.legal===b.legal,
      'independent terminal geometry mismatch '+h);
    cache.set(h,a);states+=a.states;return a;
  }
  for(const row of s.selected){
    const kids=g.children(g.board(row.h,9));
    need(kids.size===row.children&&same(kids,ind.children4(row.h)),
      'independent S9 child boundary mismatch '+row.h);
    const ordered=[...kids].sort();
    let claim=255;
    for(let i=0;i<ordered.length;i++){
      attempted++;
      if(!terminal(ordered[i]).win){claim=i;break;}
    }
    claims.push(claim);
    if(claim===255){
      win9.push(row.h);winEdges+=ordered.length;
      for(const parent of g.reverse([row.h]))
        need(g.children(g.board(parent,8)).has(row.h)&&ind.children4(parent).has(row.h),
          'S8 reverse incidence mismatch '+row.h);
    }else loss9.push(row.h);
  }
  const derived=g.reverse(win9);
  need([...derived].every(h=>!s.loss.has(h)),'S8 WIN/LOSS conflict');
  const after=new Set([...s.secured,...derived]);
  function coverage(proofs){
    let total=0,secured=0;const missing=new Set();
    for(const h of s.plan)for(const k of g.children(g.board(h,7))){
      total++;if(proofs.has(k))secured++;else missing.add(k);
    }
    return {total,secured,missing:total-secured,distinctMissing:missing.size};
  }
  const previous=coverage(s.secured),updated=coverage(after);
  need(previous.missing===120&&updated.missing<=120,
    'conditional 14-root coverage regression');
  const raw=Buffer.from(claims);
  const result={format:'n11-s9-short-single-parent-terminal-v1',board:11,
    perspective:'original-first-player',emptyBoard:'UNKNOWN',
    candidateCount:s.short.length,selected:s.selected.length,
    potentiallyCoveredS8:s.covered.size,
    selectionSha256:sha(s.selected.map(x=>x.h).join('\n')+'\n'),
    witnessBase64:raw.toString('base64'),witnessSha256:sha(raw),
    win9:win9.length,loss9:loss9.length,win10Edges:winEdges,
    firstLossSearchObligations:attempted,uniqueTerminalLeaves:cache.size,
    terminalStatesPerGeometry:states,derivedWin8:derived.size,
    newProofOnlyWin8:after.size-s.secured.size,
    proofOnlyWin8Before:s.secured.size,proofOnlyWin8After:after.size,
    knownLoss8:s.loss.size,previous,updated,winLossConflicts:0,
    newS7Verdicts:0,newS5Verdicts:0,twoStoneClosures:0};
  if(process.argv.includes('--propose')){
    console.log(JSON.stringify(result,null,2));return result;
  }
  const frozen=read('./compact-certificate.json');
  need(JSON.stringify(frozen)===JSON.stringify(result),'frozen certificate mismatch');
  console.log(JSON.stringify({verified:true,...result},null,2));return result;
}
if(require.main===module)run();
module.exports={run,inventory};