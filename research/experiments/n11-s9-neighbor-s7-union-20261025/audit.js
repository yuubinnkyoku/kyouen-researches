#!/usr/bin/env node
'use strict';
// Proof-only integration of one independently terminal-verified S9 WIN root.
// All verdicts use the original first player's viewpoint. UNKNOWN stays UNKNOWN.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const legacy=require('../n11-s6-legacy29-union-20261025/audit.js');
const previous=require('../n11-terminal-s7-s8-legacy187-union-20261025/audit.js');
const latestLoss=require('../n11-s6-legacy3-loss-union-20261025/audit.js');
const batch=require('../n11-batch-s9-s7-union-20261025/audit.js');
const EXP=path.resolve(__dirname,'..');
const PREFIX='n11-s9-new-neighbor-20261025/';
const BATCH='n11-batch-s9-terminal-20261025/';
const FRONTIER='00000100110002001042100000000010';
const need=(ok,msg)=>{if(!ok)throw Error(msg);};
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8');
function keys(p){
 const a=read(p).trim().split(/\s+/);
 need(a.length>0&&a.every((h,i)=>/^[0-9a-f]{32}$/.test(h)&&
  (i===0||a[i-1]<h)),'unsorted/duplicate key manifest: '+p);
 return a;
}
function verifyManifest(roots,leaves,parents,{terminal=true}={}){
 need(roots.length===1&&leaves.length===22&&parents.length===9,
  'incorrect proof manifest sizes');
 for(const [arr,n] of [[roots,9],[leaves,10],[parents,8]]){
  need(new Set(arr).size===arr.length,'duplicate proof key');
  for(const h of arr)g.board(h,n);
 }
 const actualLeaves=g.children(g.board(roots[0],9));
 need(actualLeaves.size===22&&leaves.every(h=>actualLeaves.has(h)),
  'S9 AND boundary incomplete or contaminated');
 const actualParents=g.reverse(roots);
 need(actualParents.size===9&&parents.every(h=>actualParents.has(h)),
  'S8 parent witness boundary incomplete or contaminated');
 for(const h of parents)
  need(g.children(g.board(h,8)).has(roots[0]),
    'illegal S8 to S9 witness: '+h);
 let states=0;
 if(terminal)for(const h of leaves){
  const result=g.solve10(h);
  need(result.win,'false terminal S10 WIN: '+h);
  states+=result.states;
 }
 need(!terminal||states===2023,'terminal state-count regression');
 return {s9WinRoots:1,s10WinLeaves:22,s8WitnessParents:9,
  terminalChecked:terminal?22:0,terminalStates:terminal?states:null};
}
function audit(){
 const roots=keys(PREFIX+'s9-roots.keys');
 const leaves=keys(PREFIX+'s10-win.keys');
 const parents=keys(PREFIX+'s8-win.keys');
 const source=verifyManifest(roots,leaves,parents);
 const prior=batch.audit();
 need(prior.totalS9Win===137&&prior.totalS8Win===1566&&
  prior.totalS7Parents===6396&&prior.securedS7Moves===12530&&
  prior.securedS7Classes===12528&&prior.newlyClosedS7===0,
  'prior proof-only baseline changed');
 const oldWin8=new Set([...legacy.certifiedWin8(),
  ...previous.sourceEdges().keys(),...g.reverse([FRONTIER]),
  ...keys(BATCH+'s8-win.keys')]);
 need(oldWin8.size===1566,'S8 WIN baseline changed');
 const frozenLoss8=new Set(keys(
  'n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'));
 const provenLoss8=new Set([...previous.certifiedLoss8(),
  ...latestLoss.source().cert.roots]);
 need(frozenLoss8.size===294&&provenLoss8.size===76,
  'S8 LOSS comparison changed');
 need(parents.every(h=>!frozenLoss8.has(h)&&!provenLoss8.has(h)),
  'S8 WIN/LOSS conflict');
 const added8=new Set(parents.filter(h=>!oldWin8.has(h)));
 need(added8.size===8,'S8 proof-only increment changed');
 const allWin8=new Set([...oldWin8,...added8]);
 const old7=g.reverse(oldWin8),affected7=g.reverse(added8);
 const all7=new Set([...old7,...affected7]);
 need(old7.size===6396&&affected7.size===36&&all7.size===6424,
  'S7 parent union changed');
 let addedMoves=0,addedClasses=0,minGap=Infinity;
 const newlyClosed=[];
 for(const h of affected7){
  const b=g.board(h,7),legalClasses=new Set(),secured=new Set(),fresh=new Set();
  for(const p of g.legal(b)){
   const c=g.key(g.canonical(b|(1n<<BigInt(p))));
   legalClasses.add(c);
   if(allWin8.has(c))secured.add(c);
   if(added8.has(c)){addedMoves++;fresh.add(c);}
  }
  addedClasses+=fresh.size;
  const gap=legalClasses.size-secured.size;
  minGap=Math.min(minGap,gap);
  if(gap===0)newlyClosed.push(h);
 }
 need(addedMoves===64&&addedClasses===64&&minGap===47&&
  newlyClosed.length===0,'S7 edge coverage/gap changed');
 return {...source,previousS9Win:137,addedS9Win:1,totalS9Win:138,
  previousS8Win:1566,overlappingS8:1,addedS8Win:8,
  totalS8Win:allWin8.size,previousS7Parents:6396,
  affectedS7Parents:affected7.size,addedS7Parents:all7.size-old7.size,
  totalS7Parents:all7.size,previousSecuredS7Moves:12530,
  addedSecuredS7Moves:addedMoves,securedS7Moves:12530+addedMoves,
  previousSecuredS7Classes:12528,addedSecuredS7Classes:addedClasses,
  securedS7Classes:12528+addedClasses,
  minimumUncoveredAmongAffectedS7:minGap,newlyClosedS7:0,
  provenS8Loss:provenLoss8.size,winLossConflicts:0,
  newlyClosedTwoStoneRoots:0,emptyBoard:'UNKNOWN'};
}
module.exports={audit,verifyManifest};
if(require.main===module){
 console.log(JSON.stringify(audit(),null,2));
 if(process.argv.includes('--negative')){
  const r=keys(PREFIX+'s9-roots.keys'),l=keys(PREFIX+'s10-win.keys'),
    p=keys(PREFIX+'s8-win.keys');
  const mutations=[
   ()=>verifyManifest(r,l.slice(1),p,{terminal:false}),
   ()=>verifyManifest(r,[l[0],...l.slice(0,-1)],p,{terminal:false}),
   ()=>verifyManifest(r,l,p.slice(1),{terminal:false}),
   ()=>verifyManifest(r,l,[p[0],...p.slice(0,-1)],{terminal:false}),
   ()=>verifyManifest(['0'.repeat(32)],l,p,{terminal:false})
  ];
  for(const test of mutations){
   let rejected=false;
   try{test();}catch(_){rejected=true;}
   need(rejected,'tampered certificate accepted');
  }
  console.error('PASS five proof-manifest mutation rejections');
 }
}
