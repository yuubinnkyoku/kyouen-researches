#!/usr/bin/env node
'use strict';
// Conditional S5 WIN plan: minimize remaining *proof-only* S7->S8 AND edges.
// Every selected S7 candidate remains UNKNOWN. No frozen WIN label is used.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const legacy=require('../n11-s6-legacy29-union-20261025/audit.js');
const union=require('../n11-terminal-s7-s8-legacy187-union-20261025/audit.js');
const threeLoss=require('../n11-s6-legacy3-loss-union-20261025/audit.js');
const EXP=path.resolve(__dirname,'..');
const ROOT='00000000000000821080000000000020';
const NEW7='00000000000100001000000042401008';
const SHARED8='00020000000000821090200000000020';
const FRONTIER9='00000100110002001042100000000010';
const FROZEN_SHA='17282f84fd65ad20ac58ef794449a52bcc796d8129a1a3a58d726a305fbeb21e';
const MORE_LOSS=[
 '000000100010a0011000000001004000',
 '00000410000000821080000002000020',
 '00004000000000821080000040400020'
];
const need=(x,m)=>{if(!x)throw Error(m);};
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8');
const keys=p=>read(p).trim().split(/\s+/);
const children=h=>g.children(BigInt('0x'+h));
const reverse=a=>g.reverse(a);
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function inventory(){
 const raw=read('n11-targeted-terminal-lift-20261015/data/all_s7_win_17.txt');
 need(crypto.createHash('sha256').update(raw).digest('hex')===FROZEN_SHA,'S7 frozen provenance changed');
 const known6=reverse([...keys('n11-targeted-terminal-lift-20261015/data/all_s7_win_17.txt'),NEW7]);
 const missing=[...children(ROOT)].filter(h=>!known6.has(h)).sort();
 need(known6.size===110&&missing.length===27,'S5 boundary changed');
 const frozenLoss=new Set(keys('n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'));
 need(frozenLoss.size===294,'S8 frozen LOSS inventory changed');
 const loss=new Set([...frozenLoss,...union.certifiedLoss8(),
  ...threeLoss.source().cert.roots,...MORE_LOSS]);
 need(loss.size>=337,'S8 LOSS exclusion unexpectedly shrank');
 // Rebuild the same terminal-proved S8 WIN union used by neighbor23's
 // reverse-coverage auditor, without promoting the frozen WIN cache.
 const win=new Set([...legacy.certifiedWin8(),...union.sourceEdges().keys(),
  ...reverse([FRONTIER9]),
  ...keys('n11-batch-s9-terminal-20261025/s8-win.keys'),
  ...keys('n11-s9-new-neighbor-20261025/s8-win.keys'),
  ...keys('n11-s9-two-neighbor-20261025/s8-win.keys'),
  ...reverse(keys('n11-s9-batch12-terminal-20261026/s9-roots.keys')),
  ...reverse(keys('n11-s9-neighbor18-terminal-20261026/s9-roots.keys')),
  ...reverse(keys('n11-s9-neighbor19-terminal-20261026/s9-roots.keys')),
  ...reverse(keys('n11-s9-neighbor23-terminal-20261026/s9-roots.keys'))]);
 need(win.size===2154,'neighbor23 proof-only S8 WIN union changed');
 for(const h of children(NEW7))win.add(h); // separately terminal-proved S7 WIN
 win.add(SHARED8); // separately terminal-proved S8 WIN16
 need([...win].every(h=>!loss.has(h)),'proof-only WIN/LOSS conflict');
 const by7=new Map();
 for(let i=0;i<missing.length;i++)for(const h of children(missing[i])){
  if(!by7.has(h))by7.set(h,new Set());
  by7.get(h).add(i);
 }
 need(by7.size===853,'S7 candidate boundary changed');
 return {missing,loss,win,by7};
}
function audit(negative=false){
 const {missing,loss,win,by7}=inventory();
 const valid=new Map(),pairOptions=new Map(),singleOptions=Array(27).fill(null);
 let excluded=0;
 const better=(a,b)=>!b||a.missing<b.missing||
  (a.missing===b.missing&&(a.total<b.total||
  (a.total===b.total&&a.s7<b.s7)));
 for(const [s7,covers] of by7){
  const s8=children(s7);
  if([...s8].some(h=>loss.has(h))){excluded++;continue;}
  const secured=[...s8].filter(h=>win.has(h)).length;
  const row={s7,covers:[...covers].sort((a,b)=>a-b),
   total:s8.size,secured,missing:s8.size-secured};
  need(row.missing>=0,'negative remaining obligation');
  valid.set(s7,row);
  for(const i of row.covers)if(better(row,singleOptions[i]))singleOptions[i]=row;
  if(row.covers.length===2){
   const id=row.covers.join(':');
   if(better(row,pairOptions.get(id)))pairOptions.set(id,row);
  }
 }
 need(excluded===67&&valid.size===786&&pairOptions.size===343,
  'known-LOSS candidate filtering changed');
 need(singleOptions.every(Boolean),'some S6 has no remaining S7 witness candidate');
 const selected=keys('n11-s5-pair-cover-20261026/s7-plan14-matching.keys');
 const optimized=keys('n11-s5-pair-cover-20261026/s7-plan14-remaining.keys');
 function evaluate(plan){
  need(plan.length===14&&new Set(plan).size===14,'invalid plan cardinality');
  const covered=new Set(),distinct=new Set(),unprovedDistinct=new Set(),securedDistinct=new Set();
  let total=0,secured=0,missingEdges=0;
  for(const h of plan){
   need(valid.has(h),'refuted or invalid S7 candidate '+h);
   const row=valid.get(h);
   for(const i of row.covers)covered.add(i);
   total+=row.total;secured+=row.secured;missingEdges+=row.missing;
   for(const c of children(h)){
    distinct.add(c);
    if(win.has(c))securedDistinct.add(c);else unprovedDistinct.add(c);
   }
  }
  need(covered.size===27,'incomplete S6 coverage');
  return {total,secured,missing:missingEdges,distinct:distinct.size,
   unprovedDistinct:unprovedDistinct.size,securedDistinct:securedDistinct.size};
 }
 const baseline=evaluate(selected),improved=evaluate(optimized);
 need(baseline.total===546&&baseline.distinct===545&&baseline.missing===541,
  'previous minimum-total plan changed');
 need(improved.total===548&&improved.secured===12&&improved.missing===536,
  'minimum remaining-obligation plan changed');
 if(negative){
  for(const bad of [selected.slice(1),
   selected.map((h,i)=>i?h:ROOT),
   selected.map((h,i)=>i?h:'00004000000000821080000040000020')]){
   let rejected=false;try{evaluate(bad);}catch(_){rejected=true;}
   need(rejected,'mutated plan accepted');
  }
 }
 return {schema:'n11-s5-remaining-proof-only-matching-v1',
  sourceS5:ROOT,missingS6:missing,knownWin8:win.size,knownLoss8:loss.size,
  candidates:by7.size,excluded,allowed:valid.size,
  pairOptions:[...pairOptions].map(([id,row])=>{const [i,j]=id.split(':').map(Number);
   return {i,j,s7:row.s7,total:row.total,secured:row.secured,missing:row.missing};
  }).sort((a,b)=>a.i-b.i||a.j-b.j),
  singleOptions:singleOptions.map((row,i)=>({i,s7:row.s7,
   total:row.total,secured:row.secured,missing:row.missing})),
  baseline,baselineRoots:selected,improved,improvedRoots:optimized,emptyBoard:'UNKNOWN',
  trust:'Terminal-proved S8 WIN only; S8 LOSS is exclusion only; candidate S7 verdicts UNKNOWN.'};
}
if(require.main===module)console.log(JSON.stringify(audit(process.argv.includes('--negative'))));
module.exports={audit};
