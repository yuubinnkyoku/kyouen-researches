#!/usr/bin/env node
'use strict';
// Structural integration of 187 previously C++/Python terminal-verified S8 WIN roots.
// The S9 witness outcomes are inherited from K0426, not re-solved here.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const old=require('../n11-s6-legacy29-union-20261025/audit.js');
const EXP=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8');
const keys=p=>read(p).trim().split(/\s+/);
const need=(x,msg)=>{if(!x)throw Error(msg);};
const SOURCES=[
 ['n11-targeted-terminal-lift-20261015/certificates/new_s8_171_terminal.cert',
  'e4df1151dc591753855145e9b9909e53ee618a5086d9adb8c88ac8c624e54171',171],
 ['n11-targeted-terminal-lift-20261015/certificates/new_s8_win_sixteen_terminal.cert',
  '1f2e5ce2416fa50559d7d97f34455542c8a11385c3f7184a9d3eea3eb7b49b7c',16]
];
function parseBatch(raw,n) {
 const lines=raw.trimEnd().split(/\r?\n/);
 need(lines[0]==='# n11-S8-WIN-batch-terminal-v1'&&lines[1]==='BOARD 11'&&
  lines[2]==='ROOTS '+n&&lines.at(-1)==='END'&&lines.length===n+4,'certificate frame');
 const edges=new Map();
 for(const line of lines.slice(3,-1)){
  const m=/^EDGE ([0-9a-f]{32}) ([0-9a-f]{32})$/.exec(line);
  need(!!m&&!edges.has(m[1]),'invalid/duplicate S8 root');
  edges.set(m[1],m[2]);
 }
 need(edges.size===n,'missing S8 root');
 return edges;
}
function sourceEdges(){
 const edges=new Map();
 for(const [p,hash,n] of SOURCES){
  const raw=read(p);
  need(crypto.createHash('sha256').update(raw).digest('hex')===hash,'source SHA-256 mismatch');
  for(const [root,witness] of parseBatch(raw,n)){
   need(!edges.has(root),'batch root overlap');
   edges.set(root,witness);
  }
 }
 need(edges.size===187,'unexpected number of certified roots');
 for(const [root,witness] of edges){
  const b=g.board(root,8);
  g.board(witness,9);
  need(g.children(b).has(witness),'illegal certified witness '+root);
 }
 return edges;
}
function certifiedLoss8(){
 const cert=JSON.parse(read('n11-s7-terminal-loss12-20261024/certificate.json'));
 const gap=JSON.parse(read('n11-gap6-terminal-20261019/gap6-terminal-cert.json'));
 const roots=new Set([
  ...keys('n11-s8-compact385-pruned1946-20261020/loss_roots35.txt'),
  ...cert.s8_loss,gap.s8_loss_root,
  '00000000000040001000044400830000',
  ...keys('n11-four-s8-joint-terminal52-20261023/roots4.keys'),
  ...old.extractCertificate().roots
 ]);
 need(roots.size===73,'previous S8 LOSS proof union changed');
 return roots;
}
function coverage(win8){
 const parents=g.reverse(win8);
 let securedMoves=0,securedClasses=0,legalClasses=0;
 const closed=[];
 for(const h of parents){
  const b=g.board(h,7),classes=new Set();
  for(const p of g.legal(b)){
   const c=g.key(g.canonical(b|(1n<<BigInt(p))));
   classes.add(c);
   if(win8.has(c))securedMoves++;
  }
  let covered=0;
  for(const c of classes)if(win8.has(c))covered++;
  securedClasses+=covered;
  legalClasses+=classes.size;
  if(covered===classes.size)closed.push(h);
 }
 return {parents:parents.size,securedMoves,securedClasses,legalClasses,closed:closed.sort()};
}
function audit(){
 const previous=old.certifiedWin8(),sources=sourceEdges(),loss8=certifiedLoss8();
 const frozenLoss=new Set(keys('n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'));
 need(previous.size===1326&&frozenLoss.size===294,'previous S8 source counts changed');
 for(const h of sources.keys())
  need(!previous.has(h)&&!loss8.has(h)&&!frozenLoss.has(h),'S8 WIN/LOSS conflict or duplicate');
 const combined=new Set([...previous,...sources.keys()]);
 need(combined.size===1513,'S8 WIN union changed');
 const c=coverage(combined);
 need(c.parents===6199&&c.securedMoves===12106&&c.securedClasses===12104&&
  c.legalClasses===377422,'S7 coverage changed');
 const known=[
  '00000000041000001000501000100000',
  '00000000041000021000401000100000',
  '00000000100100009001010000001000',
  '00000000041000001000401080100000',
  '00000000041002001000401000100000',
  '00000000000400001000401108400000'
 ];
 need(c.closed.length===6&&known.every(h=>c.closed.includes(h)),'unexpected S7 closure');
 const loss7=g.reverse(loss8);
 need(loss7.size===534&&c.closed.every(h=>!loss7.has(h)),'S7 WIN/LOSS conflict');
 return {previousS8Win:1326,addedS8Win:187,totalS8Win:1513,
  previousS7Parents:5492,addedS7Parents:707,totalS7Parents:c.parents,
  previousSecuredS7Moves:10610,addedSecuredS7Moves:1496,
  securedS7Moves:c.securedMoves,previousSecuredS7Classes:10608,
  addedSecuredS7Classes:1496,securedS7Classes:c.securedClasses,
  allS7LegalClassEdges:c.legalClasses,closedS7:c.closed.length,
  independentlyProvedS8Loss:loss8.size,independentlyProvedS7Loss:loss7.size,
  winLossConflicts:0,newlyClosedS7:0,newlyClosedTwoStoneRoots:0,
  emptyBoard:'UNKNOWN'};
}
module.exports={audit,parseBatch,sourceEdges,certifiedLoss8,coverage};
if(require.main===module){
 console.log(JSON.stringify(audit(),null,2));
 if(process.argv.includes('--negative')){
  const [p,,n]=SOURCES[0],raw=read(p),lines=raw.trimEnd().split(/\r?\n/);
  const bad=[
   lines.filter((_,i)=>i!==3).join('\n')+'\n',
   lines.map((s,i)=>i===4?lines[3]:s).join('\n')+'\n',
   raw.replace('BOARD 11','BOARD 10'),
   raw.replace('ROOTS 171','ROOTS 170')
  ];
  for(const x of bad){
   let rejected=false;
   try{parseBatch(x,n);}catch(_){rejected=true;}
   need(rejected,'malformed certificate accepted');
  }
  console.error('PASS four malformed-certificate rejections');
 }
}
