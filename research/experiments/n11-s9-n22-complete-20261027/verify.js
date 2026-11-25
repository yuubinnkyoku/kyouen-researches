#!/usr/bin/env node
'use strict';
// Complete terminal certificate for the 890 shared S9 classes with 22 S10 children.
// 255 encodes universal WIN (all children WIN); 0..21 encodes an existential
// LOSS witness.  Both integer geometries are replayed to the actual terminal.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const base=require('../n11-s5-pair-cover-20261026/audit_remaining_matching.js');
const p14=require('../n11-s9-degree2-terminal-20261027/verify.js');
const p13=require('../n11-s9-degree2-short-terminal-20261027/verify.js');
const p46=require('../n11-s9-short46-terminal-20261027/verify.js');
const p12=require('../n11-s9-short18-terminal-20261027/verify.js');
const p55=require('../n11-s9-n19-terminal-20261027/verify.js');
const p80=require('../n11-s9-n20-terminal-20261027/verify.js');
const target=require('../n11-s9-targeted-gap266-20261027/verify.js');
const EXP=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(EXP,p),'utf8');
const keys=p=>read(p).trim().split(/\s+/);
const need=(ok,msg)=>{if(!ok)throw Error(msg);};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
const cert=JSON.parse(fs.readFileSync(path.join(__dirname,'compact-certificate.json'),'utf8'));
function inventory(){
 const plan=keys('n11-s5-pair-cover-20261026/s7-plan14-remaining.keys');
 need(plan.length===14&&new Set(plan).size===14,'saved plan changed');
 const plan8=new Set(plan.flatMap(h=>[...g.children(g.board(h,7))]));
 need(plan8.size===547,'S8 plan boundary changed');
 const by9=new Map();
 for(const s8 of plan8)for(const s9 of g.children(g.board(s8,8))){
  if(!by9.has(s9))by9.set(s9,new Set());
  by9.get(s9).add(s8);
 }
 need(by9.size===8375,'S9 candidate census changed');
 const candidates=[...by9].filter(([h,parents])=>parents.size>=2&&
  g.children(g.board(h,9)).size===22).map(([h])=>h).sort();
 need(candidates.length===890,'shared 22-child S9 candidate census changed');
 need(sha(candidates.join('\n')+'\n')===cert.candidateSha256,
  'candidate set or ordering changed');
 return {plan,plan8,by9,candidates};
}
function priorProofs(){
 const c5=JSON.parse(read('n11-s9-shared-plan14-20261027/certificate.json'));
 const c11=JSON.parse(read('n11-s9-shared-plan14-eleven-win-20261027/certificate.json'));
 const old9=[...c5.witnesses,...c11.witnesses].map(x=>x.s9_win).concat(
  p14.parse(read('n11-s9-degree2-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  p13.parse(read('n11-s9-degree2-short-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  p46.parse(read('n11-s9-short46-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  p12.parse(read('n11-s9-short18-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  p55.parse(read('n11-s9-n19-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  p80.parse(read('n11-s9-n20-terminal-20261027/certificate.tsv')).map(x=>x.s9),
  target.parse(read('n11-s9-targeted-gap266-20261027/certificate.tsv')).map(x=>x.s9));
 need(new Set(old9).size===245,'earlier selected S9 proof census changed');
 const {win,loss}=base.inventory();
 need(win.size===2176&&loss.size===338,'upstream terminal-only S8 inventory changed');
 const before=new Set([...win,'00000000000000821090a00000000020',...g.reverse(old9)]);
 need(before.size===4089&&[...before].every(h=>!loss.has(h)),
  'prior proof-only S8 WIN coverage changed');
 return {old9:new Set(old9),before,loss};
}
// Replay each claimed verdict from independent terminal leaves. The negative
// controls exercise this same path, not merely a checksum inequality.
function checkedTerminal(leaf,expectedWin){
 const a=g.solve10(leaf),z=ind.solve4(leaf);
 need(a.win===expectedWin&&z.win===expectedWin&&
  a.states===z.states&&a.legal===z.legal,
  'false '+(expectedWin?'WIN':'LOSS')+'10 leaf / geometry disagreement '+leaf);
 return a;
}
function replayRoot(ordered,index){
 need(ordered.length===22,'invalid S9 child boundary');
 if(index===255){
  let subtotal=0;
  for(const leaf of ordered)subtotal+=checkedTerminal(leaf,true).states;
  return subtotal;
 }
 need(Number.isInteger(index)&&index>=0&&index<22,'invalid LOSS witness index');
 return checkedTerminal(ordered[index],false).states;
}
function verify({negative=false}={}){
 need(cert.format==='n11-s9-n22-shared-terminal-compact-v1'&&
  cert.board===11&&cert.perspective==='original-first-player'&&
  cert.emptyBoard==='UNKNOWN'&&cert.roots===890&&
  cert.winRoots===115&&cert.lossRoots===775,'bad certificate header');
 const {plan,plan8,candidates}=inventory();
 const witness=Buffer.from(cert.witnessBase64,'base64');
 need(witness.length===890&&witness.toString('base64')===cert.witnessBase64&&
  sha(witness)===cert.witnessSha256,'invalid compact witness bytes');
 if(negative){
  const bad=Buffer.from(witness);bad[0]^=1;
  need(sha(bad)!==cert.witnessSha256,'witness mutation escaped digest');
  need(sha(candidates.slice(1).join('\n')+'\n')!==cert.candidateSha256,
   'candidate deletion escaped digest');
  need(cert.emptyBoard!=='WIN','header mutation escaped');
 }
 const win9=[],loss9=[],win10=new Set(),loss10=new Set(),derived8=new Set();
 const expanded=[];let winStates=0,lossStates=0,winEdges=0,knownWin9=0;
 const prior=priorProofs();
 for(let j=0;j<candidates.length;j++){
  const h=candidates[j],b=g.board(h,9),children=g.children(b);
  need(children.size===22&&same(children,ind.children4(h)),
   'independent 9->10 boundary mismatch '+h);
  const ordered=[...children].sort(),index=witness[j];
  if(index===255){
   win9.push(h);if(prior.old9.has(h))knownWin9++;
   const subtotal=replayRoot(ordered,index);
   for(const leaf of ordered){win10.add(leaf);winEdges++;}
   winStates+=subtotal;expanded.push(h+' WIN - '+subtotal);
   for(const parent of g.reverse([h])){
    need(g.children(g.board(parent,8)).has(h)&&
     ind.children4(parent).has(h),'invalid S8->S9 WIN witness '+h);
    derived8.add(parent);
   }
  }else{
   const states=replayRoot(ordered,index),leaf=ordered[index];
   loss9.push(h);loss10.add(leaf);lossStates+=states;
   expanded.push(h+' LOSS '+leaf+' '+states);
  }
 }
 if(negative){
  // A forged witness can carry newly calculated digests. The terminal
  // verifier must reject the false verdict even without any digest check.
  const reject=(h,index,expected)=>{
   const ordered=[...g.children(g.board(h,9))].sort();
   let error=null;
   try{replayRoot(ordered,index);}catch(e){error=e;}
   need(error&&error.message.startsWith('false '+expected+'10 leaf'),
    'forged '+expected+'10 terminal claim was not rejected');
  };
  // A WIN root cannot be re-labelled LOSS via a 0..21 witness byte;
  // a LOSS root cannot be re-labelled WIN via the 255 witness byte.
  reject(win9[0],0,'LOSS');
  reject(loss9[0],255,'WIN');
 }
 need(sha(expanded.join('\n')+'\n')===cert.expandedSha256,
  'expanded certificate digest mismatch');
 need(win9.length===115&&loss9.length===775&&
  winEdges===2530&&win10.size===2478&&loss10.size===737&&
  winStates===321133&&lossStates===163139&&derived8.size===984,
  'terminal proof census changed');
 need([...loss10].every(h=>!win10.has(h)),'S10 WIN/LOSS conflict');
 need([...derived8].every(h=>!prior.loss.has(h)),
  'certified S8 WIN/LOSS conflict');
 const after=new Set([...prior.before,...derived8]);
 const evaluate=proofs=>{
  let total=0,secured=0;const missing=new Set();
  for(const h of plan)for(const c of g.children(g.board(h,7))){
   total++;if(proofs.has(c))secured++;else missing.add(c);
  }
  return {total,secured,missing:total-secured,distinctMissing:missing.size};
 };
 const previous=evaluate(prior.before),updated=evaluate(after);
 need(previous.total===548&&previous.secured===298&&previous.missing===250,
  'prior conditional 14-root frontier changed');
 need(updated.missing<=250,'proof-only coverage regressed');
 const touched=[...derived8].filter(h=>plan8.has(h)).length;
 return {schema:'n11-s9-n22-shared-terminal-compact-v1',
  candidates:candidates.length,win9:win9.length,loss9:loss9.length,
  previouslyCertifiedWin9InSelectedPlan:knownWin9,
  win10Edges:winEdges,distinctWin10:win10.size,distinctLoss10:loss10.size,
  winTerminalStatesPerGeometry:winStates,lossTerminalStatesPerGeometry:lossStates,
  independentGeometries:2,derivedWin8Parents:derived8.size,
  proofOnlyWin8Before:prior.before.size,proofOnlyWin8After:after.size,
  newProofOnlyWin8:after.size-prior.before.size,
  planS8Touched:touched,previous,updated,winLossConflicts:0,
  newS7Verdicts:0,newS5Verdicts:0,twoStoneClosures:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module)console.log(JSON.stringify(verify({negative:process.argv.includes('--negative')}),null,2));
module.exports={verify,inventory,priorProofs};
