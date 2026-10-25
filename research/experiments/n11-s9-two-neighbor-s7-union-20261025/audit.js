#!/usr/bin/env node
'use strict';
// Proof-only union: two independently terminal-proved S9 WIN roots.
// WIN/LOSS are always from the original first player's viewpoint.
// This audit does not treat frozen verdict tables as proof.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const legacy=require('../n11-s6-legacy29-union-20261025/audit.js');
const previous=require('../n11-terminal-s7-s8-legacy187-union-20261025/audit.js');
const latestLoss=require('../n11-s6-legacy3-loss-union-20261025/audit.js');
const {ROOTS:BATCH8}=require('../n11-terminal-s7-batch8-union-20261024/audit.js');
const {ROOTS:LEGACY3}=require('../n11-terminal-s7-three-legacy-s9-union-20261024/audit.js');
const EXP=path.resolve(__dirname,'..');
const PREFIX='n11-s9-two-neighbor-20261025/';
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
const HASHES={
 's9-roots.keys':'6822e87666c33b4e194d4a390cc94258518331a36c8811d5862dea75fe54a94d',
 's10-win.keys':'aec2ee7b08b720296d9f68ccd7e657b10b6be3539c32f23585224d9a36b9066c',
 's8-win.keys':'b73b8f9fee6309532e592d0a1cbe9c998536f039dc3ca8f0b08684f282c6f1b1'
};
const need=(ok,msg)=>{if(!ok)throw Error(msg);};
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8');
function keys(p,{hash=null}={}){
 const raw=read(p),a=raw.trim().split(/\s+/);
 need(a.length>0&&a.every((h,i)=>/^[0-9a-f]{32}$/.test(h)&&
   (i===0||a[i-1]<h)),'invalid/duplicate/unsorted keys: '+p);
 if(hash)need(crypto.createHash('sha256').update(raw).digest('hex')===hash,
   'manifest SHA-256 mismatch: '+p);
 return a;
}
function checkManifest(roots,leaves,parents,{terminal=true}={}){
 need(roots.length===2&&leaves.length===58&&parents.length===17,
   'incorrect source manifest sizes');
 for(const [a,n] of [[roots,9],[leaves,10],[parents,8]]){
   for(let i=1;i<a.length;i++)
     need(a[i-1]<a[i],'non-unique or unsorted certificate keys');
   for(const h of a)g.board(h,n);
 }
 const actualLeaves=new Set();let incidences=0;
 for(const h of roots){
   const children=g.children(g.board(h,9));
   incidences+=children.size;
   for(const c of children)actualLeaves.add(c);
 }
 need(incidences===59&&actualLeaves.size===58&&
   leaves.every(h=>actualLeaves.has(h)),'S9 AND boundary incomplete/contaminated');
 const actualParents=g.reverse(roots);
 need(actualParents.size===17&&parents.every(h=>actualParents.has(h)),
   'S8 witness parent boundary incomplete/contaminated');
 for(const h of parents)
   need(roots.some(r=>g.children(g.board(h,8)).has(r)),
     'S8 parent lacks legal S9 WIN witness: '+h);
 let states=0;
 if(terminal)for(const h of leaves){
   const x=g.solve10(h);
   need(x.win,'false terminal S10 WIN: '+h);
   states+=x.states;
 }
 return {s9WinRoots:roots.length,s10WinIncidences:incidences,
   distinctS10WinLeaves:leaves.length,s8WitnessParents:parents.length,
   independentlyRecheckedLeaves:terminal?leaves.length:0,
   jsTerminalStates:terminal?states:null};
}
function audit({terminal=true}={}){
 const roots=keys(PREFIX+'s9-roots.keys',{hash:HASHES['s9-roots.keys']});
 const leaves=keys(PREFIX+'s10-win.keys',{hash:HASHES['s10-win.keys']});
 const parents=keys(PREFIX+'s8-win.keys',{hash:HASHES['s8-win.keys']});
 const source=checkManifest(roots,leaves,parents,{terminal});
 const oldCert=JSON.parse(read('n11-s7-terminal-loss12-20261024/certificate.json'));
 const previousS9=new Set([...GROUPS.flatMap(p=>keys(p)),...oldCert.new_s9_win,
   ...BATCH8,...LEGACY3,FRONTIER,
   ...keys('n11-batch-s9-terminal-20261025/s9-roots.keys'),
   ...keys('n11-s9-new-neighbor-20261025/s9-roots.keys')]);
 need(previousS9.size===138,'previous certified S9 WIN root count changed');
 need(roots.every(h=>!previousS9.has(h)),'S9 root already certified');
 const oldWin8=new Set([...legacy.certifiedWin8(),
   ...previous.sourceEdges().keys(),...g.reverse([FRONTIER]),
   ...keys('n11-batch-s9-terminal-20261025/s8-win.keys'),
   ...keys('n11-s9-new-neighbor-20261025/s8-win.keys')]);
 need(oldWin8.size===1574,'previous certified S8 WIN union changed');
 const frozenLoss8=new Set(keys(
   'n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'));
 const provenLoss8=new Set([...previous.certifiedLoss8(),
   ...latestLoss.source().cert.roots]);
 need(frozenLoss8.size===294&&provenLoss8.size===76,
   'S8 LOSS comparison changed');
 need(parents.every(h=>!frozenLoss8.has(h)&&!provenLoss8.has(h)),
   'S8 WIN/LOSS conflict');
 const fresh8=new Set(parents.filter(h=>!oldWin8.has(h)));
 need(fresh8.size>0,'no new S8 WIN classes');
 const allWin8=new Set([...oldWin8,...fresh8]);
 const old7=g.reverse(oldWin8),affected7=g.reverse(fresh8);
 const all7=new Set([...old7,...affected7]);
 need(old7.size===6424,'previous S7 parent coverage changed');
 let addedMoves=0,addedClasses=0,minGap=Infinity;
 const newlyClosed=[];
 for(const h of affected7){
   const b=g.board(h,7),legalClasses=new Set(),secured=new Set(),fresh=new Set(),oldSecured=new Set();
   for(const p of g.legal(b)){
     const c=g.key(g.canonical(b|(1n<<BigInt(p))));
     legalClasses.add(c);
     if(allWin8.has(c))secured.add(c);
     if(oldWin8.has(c))oldSecured.add(c);
     if(fresh8.has(c)){fresh.add(c);addedMoves++;}
   }
   addedClasses+=fresh.size;
   const gap=legalClasses.size-secured.size;
   minGap=Math.min(minGap,gap);
   if(gap===0&&oldSecured.size<legalClasses.size)newlyClosed.push(h);
 }
 const provenLoss7=g.reverse(provenLoss8);
 need(newlyClosed.every(h=>!provenLoss7.has(h)),
   'new S7 WIN/LOSS conflict');
 return {...source,previousS9Win:138,addedS9Win:roots.length,
   totalS9Win:previousS9.size+roots.length,
   previousS8Win:1574,overlappingS8:parents.length-fresh8.size,
   addedS8Win:fresh8.size,totalS8Win:allWin8.size,
   previousS7Parents:old7.size,affectedS7Parents:affected7.size,
   addedS7Parents:all7.size-old7.size,totalS7Parents:all7.size,
   previousSecuredS7Moves:12594,addedSecuredS7Moves:addedMoves,
   securedS7Moves:12594+addedMoves,
   previousSecuredS7Classes:12592,addedSecuredS7Classes:addedClasses,
   securedS7Classes:12592+addedClasses,
   minimumUncoveredAmongAffectedS7:minGap,
   newlyClosedS7:newlyClosed.sort(),provenS8Loss:provenLoss8.size,
   winLossConflicts:0,newlyClosedTwoStoneRoots:0,emptyBoard:'UNKNOWN'};
}
module.exports={audit,checkManifest};
if(require.main===module){
 console.log(JSON.stringify(audit(),null,2));
 if(process.argv.includes('--negative')){
   const r=keys(PREFIX+'s9-roots.keys'),l=keys(PREFIX+'s10-win.keys'),
     p=keys(PREFIX+'s8-win.keys');
   const mutations=[
     ()=>checkManifest(r.slice(1),l,p,{terminal:false}),
     ()=>checkManifest(r,l.slice(1),p,{terminal:false}),
     ()=>checkManifest(r,l,p.slice(1),{terminal:false}),
     ()=>checkManifest(r,[l[0],...l.slice(0,-1)],p,{terminal:false}),
     ()=>checkManifest(r,l,[p[0],...p.slice(0,-1)],{terminal:false})
   ];
   for(const test of mutations){
     let rejected=false;
     try{test();}catch(_){rejected=true;}
     need(rejected,'tampered certificate accepted');
   }
   console.error('PASS five proof-manifest mutation rejections');
 }
}
