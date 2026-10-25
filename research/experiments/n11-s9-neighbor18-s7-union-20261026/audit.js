#!/usr/bin/env node
'use strict';
// Proof-only integration of eighteen terminal-certified N11 S9 WIN roots.
// All WIN/LOSS values use the original first player's viewpoint.
// This audit does not promote frozen verdicts or unfinished searches to proofs.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const legacy=require('../n11-s6-legacy29-union-20261025/audit.js');
const previous=require('../n11-terminal-s7-s8-legacy187-union-20261025/audit.js');
const latestLoss=require('../n11-s6-legacy3-loss-union-20261025/audit.js');
const {ROOTS:BATCH8}=require('../n11-terminal-s7-batch8-union-20261024/audit.js');
const {ROOTS:LEGACY3}=require('../n11-terminal-s7-three-legacy-s9-union-20261024/audit.js');
const EXP=path.resolve(__dirname,'..');
const SOURCE='n11-s9-neighbor18-terminal-20261026/s9-roots.keys';
const FRONTIER='00000100110002001042100000000010';
const GROUPS=[
 'n11-s9-win29-lift-20261023/s9-win29.keys',
 'n11-s9-win27-expansion-20261024/s9-win27.keys',
 'n11-s9-win2-followup-20261024/s9-win2.keys',
 'n11-s9-win10-20261024/s9-win10.keys',
 'n11-s9-win7-expansion-20261024/s9-win7.keys',
 'n11-s9-win20-neighbor-20261024/s9-win20.keys',
 'n11-s8-frontier-13way-20261024/s9-win7.keys'
];
const ROOT_HASH='649790d59fc9d3d74c9e19309cbb66e6db49b57ecd9b7f1e10ea5221b471dd34';
const LEAF_HASH='e68c64ebde426f5210c4c6ab0b5110fa859f0e1e074d6a7a457455f8e084c23c';
const PARENT_HASH='3dbf7d5462f9689231b77a425ca0c4ead5c6b58e25ddd92cd1549c9782d8342c';
const need=(ok,msg)=>{if(!ok)throw Error(msg);};
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8');
const digest=arr=>crypto.createHash('sha256').update([...arr].sort().join('\n')+'\n').digest('hex');
function keys(p,{hash=null}={}){
 const raw=read(p),a=raw.trim().split(/\s+/);
 need(a.length>0&&a.every((h,i)=>/^[0-9a-f]{32}$/.test(h)&&
   (i===0||a[i-1]<h)),'invalid/duplicate/unsorted keys: '+p);
 if(hash)need(crypto.createHash('sha256').update(raw).digest('hex')===hash,
   'source SHA-256 mismatch: '+p);
 return a;
}
function verifyBoundary(roots,leaves,parents){
 need(roots.length===18&&leaves.length===348&&parents.length===151,
   'certificate boundary size changed');
 for(const [arr,n] of [[roots,9],[leaves,10],[parents,8]]){
  need(arr.every((h,i)=>i===0||arr[i-1]<h),
    'duplicate or unsorted certificate boundary');
  for(const h of arr)g.board(h,n);
 }
 need(digest(roots)===ROOT_HASH&&digest(leaves)===LEAF_HASH&&
   digest(parents)===PARENT_HASH,'certificate digest mismatch');
 let incidences=0;const actualLeaves=new Set();
 for(const h of roots){
  const children=g.children(g.board(h,9));
  incidences+=children.size;
  for(const c of children)actualLeaves.add(c);
 }
 need(incidences===355&&actualLeaves.size===348&&
   leaves.every(h=>actualLeaves.has(h)),'incomplete S9 AND boundary');
 const actualParents=g.reverse(roots);
 need(actualParents.size===151&&parents.every(h=>actualParents.has(h)),
   'incomplete S8 witness boundary');
 for(const h of parents){
  const children=g.children(g.board(h,8));
  need(roots.some(r=>children.has(r)),'S8 parent lacks legal S9 WIN witness: '+h);
 }
 return {s9WinRoots:18,s10LegalIncidences:355,s10DistinctWinLeaves:348,
   s8WitnessParents:151,sourceTerminalVerification:
   'n11-s9-neighbor18-terminal-20261026/verify.py'};
}
function audit(){
 const roots=keys(SOURCE,{hash:ROOT_HASH});
 const leaves=new Set(),parents=g.reverse(roots);
 for(const h of roots)for(const c of g.children(g.board(h,9)))leaves.add(c);
 const source=verifyBoundary(roots,[...leaves].sort(),[...parents].sort());
 const oldCert=JSON.parse(read('n11-s7-terminal-loss12-20261024/certificate.json'));
 const oldS9=new Set([...GROUPS.flatMap(p=>keys(p)),...oldCert.new_s9_win,
   ...BATCH8,...LEGACY3,FRONTIER,
   ...keys('n11-batch-s9-terminal-20261025/s9-roots.keys'),
   ...keys('n11-s9-new-neighbor-20261025/s9-roots.keys'),
   ...keys('n11-s9-two-neighbor-20261025/s9-roots.keys'),
   ...keys('n11-s9-batch12-terminal-20261026/s9-roots.keys')]);
 need(oldS9.size===152&&roots.every(h=>!oldS9.has(h)),
   'previous S9 WIN provenance changed or roots overlap');
 const oldWin8=new Set([...legacy.certifiedWin8(),
   ...previous.sourceEdges().keys(),...g.reverse([FRONTIER]),
   ...keys('n11-batch-s9-terminal-20261025/s8-win.keys'),
   ...keys('n11-s9-new-neighbor-20261025/s8-win.keys'),
   ...keys('n11-s9-two-neighbor-20261025/s8-win.keys'),
   ...g.reverse(keys('n11-s9-batch12-terminal-20261026/s9-roots.keys'))]);
 need(oldWin8.size===1684,'previous certified S8 WIN union changed');
 const frozenLoss8=new Set(keys(
   'n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'));
 const provenLoss8=new Set([...previous.certifiedLoss8(),
   ...latestLoss.source().cert.roots]);
 need(frozenLoss8.size===294&&provenLoss8.size===76,
   'S8 LOSS comparison baseline changed');
 need([...parents].every(h=>!frozenLoss8.has(h)&&!provenLoss8.has(h)),
   'S8 WIN/LOSS conflict');
 const fresh8=new Set([...parents].filter(h=>!oldWin8.has(h)));
 const allWin8=new Set([...oldWin8,...fresh8]);
 need(parents.size===151&&fresh8.size>0&&allWin8.size===oldWin8.size+fresh8.size,
   'S8 proof-only overlap or union regression');
 const old7=g.reverse(oldWin8),affected7=g.reverse(fresh8);
 const all7=new Set([...old7,...affected7]);
 need(old7.size===6799&&affected7.size>0&&all7.size>=old7.size,
   'S7 parent coverage regression');
 let addedMoves=0,addedClasses=0,minGap=Infinity;
 const newlyClosed=[];
 for(const h of affected7){
  const b=g.board(h,7),legalClasses=new Set(),secured=new Set(),fresh=new Set();
  for(const p of g.legal(b)){
   const c=g.key(g.canonical(b|(1n<<BigInt(p))));
   legalClasses.add(c);
   if(allWin8.has(c))secured.add(c);
   if(fresh8.has(c)){fresh.add(c);addedMoves++;}
  }
  addedClasses+=fresh.size;
  const gap=legalClasses.size-secured.size;
  minGap=Math.min(minGap,gap);
  if(gap===0)newlyClosed.push(h);
 }
 need(addedMoves>0&&addedClasses>0&&minGap>=0&&
   addedClasses<=addedMoves,'S7 secured-edge or uncovered-gap regression');
 const provenLoss7=g.reverse(provenLoss8);
 need(newlyClosed.every(h=>!provenLoss7.has(h)),
   'S7 WIN/LOSS conflict');
 return {...source,previousS9Win:152,addedS9Win:18,totalS9Win:170,
   previousS8Win:1684,overlappingS8:parents.size-fresh8.size,
   addedS8Win:fresh8.size,totalS8Win:allWin8.size,
   previousS7Parents:6799,affectedS7Parents:affected7.size,
   addedS7Parents:all7.size-old7.size,totalS7Parents:all7.size,
   previousSecuredS7Moves:13474,addedSecuredS7Moves:addedMoves,
   securedS7Moves:13474+addedMoves,
   previousSecuredS7Classes:13472,addedSecuredS7Classes:addedClasses,
   securedS7Classes:13472+addedClasses,
   minimumUncoveredAmongAffectedS7:minGap,
   newlyClosedS7:newlyClosed.sort(),provenS8Loss:provenLoss8.size,
   winLossConflicts:0,newlyClosedTwoStoneRoots:null,emptyBoard:'UNKNOWN'};
}
module.exports={audit,verifyBoundary};
if(require.main===module){
 console.log(JSON.stringify(audit(),null,2));
 if(process.argv.includes('--negative')){
  const roots=keys(SOURCE),leaves=new Set();
  for(const h of roots)for(const c of g.children(g.board(h,9)))leaves.add(c);
  const r=roots,l=[...leaves].sort(),p=[...g.reverse(r)].sort();
  const tests=[
   ()=>verifyBoundary(r.slice(1),l,p),
   ()=>verifyBoundary(r,l.slice(1),p),
   ()=>verifyBoundary(r,l,p.slice(1)),
   ()=>verifyBoundary(r,[l[0],...l.slice(0,-1)],p),
   ()=>verifyBoundary(r,l,[p[0],...p.slice(0,-1)])
  ];
  for(const test of tests){
   let rejected=false;
   try{test();}catch(_){rejected=true;}
   need(rejected,'tampered certificate accepted');
  }
  console.error('PASS five boundary mutation rejections');
 }
}
