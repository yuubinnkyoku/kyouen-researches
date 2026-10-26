#!/usr/bin/env node
'use strict';
// Certificate-only S10 LOSS -> S9 LOSS propagation. No unfinished search/cache verdicts.
// Independent terminal solvers: 3x3 integer determinant and 4x4 Bareiss determinant.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const independent=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const EXP=path.resolve(__dirname,'..');
const need=(ok,msg)=>{if(!ok)throw Error(msg);};
const readKeys=p=>fs.readFileSync(p,'ascii').trim().split(/\s+/);
const hex=/^[0-9a-f]{32}$/;
function load(){
  const lines=fs.readFileSync(path.join(__dirname,'certificate.tsv'),'utf8')
    .split(/\r?\n/).filter(s=>s.trim()&&!s.startsWith('#'));
  return lines.map(line=>{
    const fields=line.trim().split(/\s+/);
    need(fields.length===4&&fields.slice(0,2).every(x=>hex.test(x)),
      'invalid certificate row');
    return {s9:fields[0],s10:fields[1],
      states:Number(fields[2]),legal:Number(fields[3])};
  });
}
function verify(rows,{terminal=true}={}){
  need(Array.isArray(rows)&&rows.length===57,'wrong S9 certificate count');
  const plan=readKeys(path.join(EXP,'n11-s5-pair-cover-20261026/s7-plan14-remaining.keys'));
  need(plan.length===14&&new Set(plan).size===14,'plan changed');
  const plan8=new Set(plan.flatMap(h=>[...g.children(g.board(h,7))]));
  need(plan8.size===547,'S8 plan boundary changed');
  const seen9=new Set(),new10=new Set();let incidences=0,states=0;
  for(const row of rows){
    need(!seen9.has(row.s9),'duplicate S9 LOSS root');seen9.add(row.s9);
    need(Number.isSafeInteger(row.states)&&row.states>0&&
      Number.isSafeInteger(row.legal)&&row.legal>=0,'invalid leaf metadata');
    const s9=g.board(row.s9,9),s10=g.board(row.s10,10);
    need(g.children(s9).has(row.s10),'illegal S9 -> S10 LOSS witness');
    const parents=g.reverse([row.s9]);
    let n=0;for(const p of parents)if(plan8.has(p))n++;
    need(n===3||n===4,'root is not a 3/4-way shared witness');
    incidences+=n;new10.add(row.s10);
    if(terminal){
      const a=g.solve10(row.s10),b=independent.solve4(row.s10);
      need(!a.win&&!b.win,'S10 LOSS leaf is not terminal LOSS: '+row.s10);
      need(a.states===b.states&&a.legal===b.legal&&
        a.states===row.states&&a.legal===row.legal,
        'independent terminal/metadata mismatch: '+row.s10);
      states+=a.states;
    }
  }
  need(incidences===210&&new10.size===55,'shared witness union changed');
  const oldCert=JSON.parse(fs.readFileSync(path.join(EXP,
    'n11-s7-terminal-loss12-20261024/certificate.json'),'utf8'));
  const old10=new Set([...readKeys(path.join(EXP,
    'n11-s8-to-s7-lift238-20261020/selected385.txt')),
    ...oldCert.s10_loss_cover39,...oldCert.s10_loss_cover12,
    ...readKeys(path.join(EXP,'n11-s9-loss12-frontier-20261024/s10-loss12.keys'))]);
  need(old10.size===439&&[...new10].every(h=>!old10.has(h)),
    'existing LOSS leaf overlap or census changed');
  const before9=g.reverse([...old10]),after9=g.reverse([...old10,...new10]);
  need(before9.size===4273&&after9.size===4807&&
    [...seen9].every(h=>!before9.has(h)&&after9.has(h)),
    'S9 LOSS proof-only closure mismatch');
  const oldWinFiles=[
    'n11-s9-win29-lift-20261023/s9-win29.keys',
    'n11-s9-win27-expansion-20261024/s9-win27.keys',
    'n11-s9-win2-followup-20261024/s9-win2.keys',
    'n11-s9-win10-20261024/s9-win10.keys',
    'n11-s9-win7-expansion-20261024/s9-win7.keys',
    'n11-s9-win20-neighbor-20261024/s9-win20.keys'
  ];
  const win9=new Set(oldWinFiles.flatMap(p=>readKeys(path.join(EXP,p))));
  for(const name of ['n11-s9-shared-plan14-20261027',
    'n11-s9-shared-plan14-eleven-win-20261027']){
    const cert=JSON.parse(fs.readFileSync(path.join(EXP,name,'certificate.json'),'utf8'));
    for(const w of cert.witnesses)win9.add(w.s9_win);
  }
  win9.add('00020000000000821090200000400020');
  need([...win9].every(h=>!after9.has(h)),'S9 WIN/LOSS conflict');
  let oldEdges=0,newEdges=0,affected8=0;
  const degrees=new Map();
  for(const h of plan8){
    let a=0,b=0;
    for(const c of g.children(g.board(h,8))){
      degrees.set(c,(degrees.get(c)||0)+1);
      if(before9.has(c))a++;
      if(after9.has(c))b++;
    }
    oldEdges+=a;newEdges+=b;if(b>a)affected8++;
  }
  need(oldEdges===12&&newEdges===594,'plan S8->S9 LOSS edge audit mismatch');
  const shared=[...degrees].filter(([_,degree])=>degree>=3);
  const sharedWin=shared.filter(([h])=>win9.has(h)).length;
  const sharedLoss=shared.filter(([h])=>after9.has(h)).length;
  need(shared.length===75&&sharedWin===18&&sharedLoss===57&&
    shared.every(([h])=>win9.has(h)!==after9.has(h)),
    'shared S9 candidates not fully classified');
  if(terminal)need(states===7337,'terminal state count changed');
  return {certifiedS9Loss:seen9.size,newS10LossLeaves:new10.size,
    oldS9Loss:before9.size,newS9Loss:after9.size,gainedS9Loss:after9.size-before9.size,
    sharedS8ToS9Edges:incidences,plan8:plan8.size,
    plan8S9LossEdgesBefore:oldEdges,plan8S9LossEdgesAfter:newEdges,
    affectedPlan8:affected8,sharedS9Candidates:shared.length,
    sharedS9Win:sharedWin,sharedS9Loss:sharedLoss,sharedS9Unknown:0,
    terminalStatesPerGeometry:terminal?states:null,
    independentGeometries:terminal?2:0,newS8Verdicts:0,
    newTwoStoneClosures:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module){
  const rows=load(),report=verify(rows);console.log(JSON.stringify(report,null,2));
  if(process.argv.includes('--negative')){
    const reject=(fn,full=false)=>{
      const bad=rows.map(r=>({...r}));fn(bad);let failed=false;
      try{verify(bad,{terminal:full});}catch(_){failed=true;}
      need(failed,'tampered certificate accepted');
    };
    reject(r=>r.pop());
    reject(r=>r[1].s9=r[0].s9);
    reject(r=>r[0].s10=r[0].s9);
    reject(r=>r[0].states=0);
    reject(r=>r[0].states++,true);
    console.error('PASS five certificate mutation rejections');
  }
}
module.exports={verify,load};
