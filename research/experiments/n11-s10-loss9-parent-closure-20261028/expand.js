#!/usr/bin/env node
'use strict';
// Expand independently certified LOSS10 leaves to ALL D4-distinct safe S9 parents.
// Perspective is the ORIGINAL first player: at S9 the opponent is to move.
// This is NOT an empty-board verdict and does not imply any S8 LOSS.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const reuse=require('../n11-s10-cross-batch-reuse-20261028/reuse.js');
const need=(x,msg)=>{if(!x)throw Error(msg);};
const source=path.join(__dirname,'../n11-s10-cross-batch-reuse-20261028/derived-loss9.json');
const key=b=>b.toString(16).padStart(32,'0');
function independentCanonical(b){
  const pp=g.pts(b);let best=null;
  for(let t=0;t<8;t++){
    let transformed=0n;
    for(const i of pp){
      const x=i%11,y=Math.floor(i/11);
      const a=[[x,y],[10-y,x],[10-x,10-y],[y,10-x],
        [10-x,y],[10-y,10-x],[x,10-y],[y,x]][t];
      transformed|=1n<<BigInt(a[1]*11+a[0]);
    }
    if(best===null||transformed<best)best=transformed;
  }
  return key(best);
}
function parentsOfLoss10(h){
  const b=g.board(h,10),points=g.pts(b);
  // An independent 4x4 integer determinant checks that the ten-stone
  // witness is safe; the upstream 3x3 check is in g.board.
  for(let a=0;a<7;a++)for(let c=a+1;c<8;c++)
  for(let d=c+1;d<9;d++)for(let e=d+1;e<10;e++)
    need(ind.det4([points[a],points[c],points[d],points[e]])!==0,
      'independent unsafe LOSS10 leaf '+h);
  const out=new Set();
  for(const p of points){
    const parent=b^(1n<<BigInt(p));
    const k=key(g.canonical(parent));
    need(k===independentCanonical(parent),'D4 canonical mismatch '+h);
    // Hereditary safety: a subset of a safe ten-stone board is safe;
    // therefore re-adding the removed stone is a legal S9->S10 move.
    out.add(k);
  }
  return out;
}
function expand(rows){
  need(Array.isArray(rows)&&rows.length===383,'source witness count');
  const cache=new Map(),result=new Map(),input=new Set();
  for(const row of rows){
    need(typeof row.h==='string'&&typeof row.loss10==='string'&&
      typeof row.source==='string','malformed witness');
    need(!input.has(row.h),'duplicate source S9 key');
    input.add(row.h);
    if(!cache.has(row.loss10))cache.set(row.loss10,parentsOfLoss10(row.loss10));
    const parents=cache.get(row.loss10);
    need(parents.has(row.h),'forged S9/LOSS10 witness relation '+row.h);
    for(const h of parents)
      if(!result.has(h)||row.loss10<result.get(h))result.set(h,row.loss10);
  }
  need(cache.size===334&&result.size===3250&&
    [...input].every(h=>result.has(h)),
    'frozen LOSS9 closure census changed');
  return {input,cache,result};
}
function negativeTests(rows){
  let rejected=false;
  try{expand([{...rows[0],loss10:rows[0].h},...rows.slice(1)]);}
  catch(_){rejected=true;}
  need(rejected,'forged nine-stone LOSS10 accepted');
  rejected=false;
  try{expand([{...rows[0],h:'0'.repeat(32)},...rows.slice(1)]);}
  catch(_){rejected=true;}
  need(rejected,'forged parent incidence accepted');
}
function run(){
  // Reconstruct and check every upstream certificate identity and all
  // LOSS10 conflicts before trusting the source witness list.
  const log=console.log;let checked;
  try{console.log=()=>{};checked=reuse.run();}finally{console.log=log;}
  need(checked.freeLoss9===383&&checked.conflicts===0,
    'upstream cross-batch audit changed');
  const rows=JSON.parse(fs.readFileSync(source,'utf8'));
  const {input,cache,result}=expand(rows);
  negativeTests(rows);
  const sorted=[...result.keys()].sort(),manifest=sorted.join('\n')+'\n';
  need(fs.readFileSync(path.join(__dirname,'expanded-loss9.keys'),'ascii')===manifest,
    'frozen expanded LOSS9 manifest changed');
  const plan=JSON.parse(fs.readFileSync(path.join(__dirname,
    '../n11-s10-cross-batch-reuse-20261028/plan.json'),'utf8'));
  const plannedOverlap=plan.selectedKeys.filter(h=>result.has(h));
  const report={schema:'n11-s10-loss9-all-safe-parents-v1',
    emptyBoard:'UNKNOWN',sourceLoss9:input.size,distinctLoss10:cache.size,
    provedLoss9Parents:result.size,additionalVsSourceList:result.size-input.size,
    planned32AlreadyLoss:plannedOverlap.length,plannedOverlap,
    trust:'inherited frozen LOSS10 terminal witnesses; 3x3/4x4 safe geometry and independent D4 parent audit; not a fresh terminal replay',
    twoStoneClosures:0};
  if(process.argv.includes('--frontier')){
    const r7=require('../n11-s9-n24-round7-20261028/prove.js');
    const oldLog=console.log;let inv;
    try{console.log=()=>{};inv=r7.inventory();}finally{console.log=oldLog;}
    const selected=new Set(inv.selected.map(x=>x.h));
    const eligible=inv.options.filter(x=>!selected.has(x.h)&&!input.has(x.h));
    need(eligible.length===1063,'prior eligible census changed');
    const covered=eligible.filter(x=>result.has(x.h));
    report.remainingEligibleBefore=eligible.length;
    report.newlyExcludedFromEligible=covered.length;
    report.remainingEligibleAfter=eligible.length-covered.length;
  }
  if(process.argv.includes('--export')){
    for(const h of sorted)console.log(h+'\t'+result.get(h));
  }else console.log(JSON.stringify(report,null,2));
  return report;
}
if(require.main===module)run();
module.exports={run,expand,parentsOfLoss10};
