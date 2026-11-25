#!/usr/bin/env node
'use strict';
// Structural integration of three S8 LOSS roots already independently
// terminal-verified by C++ and Python (K0426). S10 leaves are NOT re-solved.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const prev=require('../n11-terminal-s7-s8-legacy187-union-20261025/audit.js');
const legacy=require('../n11-s6-legacy29-union-20261025/audit.js');
const EXP=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8');
const keys=p=>new Set(read(p).trim().split(/\s+/));
const need=(ok,msg)=>{if(!ok)throw Error(msg);};
const SOURCE='n11-targeted-terminal-lift-20261015/certificates/new_s8_loss_three_terminal.cert';
const HASH='395a9e94b1813a9e6e38a508fc2ba427eeb3da18816439494a20037f9cc43838';

function parseCertificate(raw){
 const lines=raw.trimEnd().split(/\r?\n/);
 need(lines.length===111&&lines[0]==='# n11-S8-LOSS-batch-terminal-v1'&&
  lines[1]==='BOARD 11'&&lines[2]==='ROOTS 3'&&lines.at(-1)==='END',
  'invalid certificate frame');
 const roots=lines.slice(3,6).map(s=>{
  const m=/^ROOT ([0-9a-f]{32})$/.exec(s);
  need(!!m,'invalid S8 root record');return m[1];
 });
 need(new Set(roots).size===3,'duplicate S8 root');
 const witnesses=new Map();
 for(const line of lines.slice(6,-1)){
  const m=/^WITNESS ([0-9a-f]{32}) ([0-9a-f]{32})$/.exec(line);
  need(!!m&&!witnesses.has(m[1]),'invalid/duplicate S9 witness');
  witnesses.set(m[1],m[2]);
 }
 need(witnesses.size===104,'S9 witness count changed');
 return {roots,witnesses};
}
function verifyBoundary({roots,witnesses}){
 const obligations=new Set();let edges=0;
 for(const h of roots){
  const children=g.children(g.board(h,8));
  edges+=children.size;
  for(const c of children)obligations.add(c);
 }
 need(edges===105&&obligations.size===104,'S8 to S9 boundary changed');
 const leaves=new Set();
 for(const [s9,s10] of witnesses){
  need(obligations.has(s9),'extraneous S9 obligation');
  need(g.children(g.board(s9,9)).has(s10),'illegal S9 to S10 witness');
  g.board(s10,10);leaves.add(s10);
 }
 need(leaves.size===63&&[...obligations].every(h=>witnesses.has(h)),
  'S9 obligations not covered by 63 S10 leaves');
 return {s8ToS9Edges:edges,s9Obligations:obligations.size,s10LossLeaves:leaves.size};
}
function source(){
 const raw=read(SOURCE);
 need(crypto.createHash('sha256').update(raw).digest('hex')===HASH,
  'K0426 certificate hash mismatch');
 const cert=parseCertificate(raw);
 return {cert,boundary:verifyBoundary(cert)};
}
function audit(){
 const {cert,boundary}=source(),roots=cert.roots;
 const old8=prev.certifiedLoss8();
 need(old8.size===73&&roots.every(h=>!old8.has(h)),'S8 LOSS overlap');
 const all8=new Set([...old8,...roots]);
 const win8=new Set([...legacy.certifiedWin8(),...prev.sourceEdges().keys()]);
 const frozenWin8=keys('n11-targeted-terminal-lift-20261015/data/lifted_s8_win_51571.txt');
 const frozenLoss8=keys('n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt');
 need(win8.size===1513&&frozenWin8.size===13501&&frozenLoss8.size===294,
  'S8 comparison baseline changed');
 need(roots.every(h=>!win8.has(h)&&!frozenWin8.has(h)&&frozenLoss8.has(h)),
  'S8 WIN/LOSS conflict');
 const old7=g.reverse(old8),new7=g.reverse(roots),all7=new Set([...old7,...new7]);
 const added7=[...new7].filter(h=>!old7.has(h));
 need(old7.size===534&&new7.size===23&&added7.length===20&&all7.size===554,
  'S7 LOSS union changed');
 const frozenWin7=keys('n11-targeted-terminal-lift-20261015/data/all_s7_win_17.txt');
 const frozenLoss7=keys('n11-targeted-terminal-lift-20261015/data/all_s7_loss_2232.txt');
 need(frozenWin7.size===17&&frozenLoss7.size===2232&&
  [...all7].every(h=>!frozenWin7.has(h))&&
  added7.every(h=>frozenLoss7.has(h)),'S7 WIN/LOSS conflict');
 const old6=g.reverse(old7),all6=g.reverse(all7);
 need(old6.size===1653&&all6.size===1710,'S6 reverse union changed');
 let legalEdges=0,securedEdges=0,minOpenGap=Infinity;
 const closed=[];
 for(const h of all6){
  const children=g.children(g.board(h,6));
  let covered=0;
  for(const c of children)if(all7.has(c))covered++;
  legalEdges+=children.size;securedEdges+=covered;
  const gap=children.size-covered;
  if(!gap)closed.push(h);else minOpenGap=Math.min(minOpenGap,gap);
 }
 closed.sort();
 need(legalEdges===132573&&securedEdges===3878&&minOpenGap===37&&
  closed.length===1&&closed[0]==='00000000040004001004000004010000',
  'S6 child coverage changed');
 return {...boundary,previousS8Loss:73,addedS8Loss:3,totalS8Loss:all8.size,
  previousS7Loss:534,addedS7Loss:added7.length,totalS7Loss:all7.size,
  previousS6Parents:1653,addedS6Parents:all6.size-1653,
  totalS6Parents:all6.size,previousSecuredS6Edges:3738,
  addedSecuredS6Edges:securedEdges-3738,securedS6Edges:securedEdges,
  allS6LegalEdges:legalEdges,minimumUncoveredOpenS6Classes:minOpenGap,
  closedS6:closed,winLossConflicts:0,newlyClosedS6:0,
  newlyClosedTwoStoneRoots:0,emptyBoard:'UNKNOWN'};
}
module.exports={parseCertificate,verifyBoundary,source,audit};
if(require.main===module){
 console.log(JSON.stringify(audit(),null,2));
 if(process.argv.includes('--negative')){
  const raw=read(SOURCE),lines=raw.trimEnd().split(/\r?\n/);
  const tests=[
   raw.replace('BOARD 11','BOARD 10'),
   raw.replace('ROOTS 3','ROOTS 4'),
   lines.filter((_,i)=>i!==6).join('\n')+'\n',
   lines.map((s,i)=>i===7?lines[6]:s).join('\n')+'\n',
   lines.map((s,i)=>i===6?s.replace(/ [0-9a-f]{32}$/, ' '+s.split(' ')[1]):s).join('\n')+'\n'
  ];
  for(const tampered of tests){
   let rejected=false;
   try{verifyBoundary(parseCertificate(tampered));}catch(_){rejected=true;}
   need(rejected,'malformed S8 LOSS certificate accepted');
  }
  console.error('PASS five malformed-certificate rejections');
 }
}
