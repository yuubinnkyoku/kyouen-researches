#!/usr/bin/env node
'use strict';
// Certified S10 verdicts only: no inference from incomplete search.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const read=d=>JSON.parse(fs.readFileSync(path.join(__dirname,'..',d,'compact-certificate.json')));
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function memo(m,k){const f=m[k];let ready=false,value;m[k]=()=>{if(!ready){value=f();ready=true;}return value;};}
const n22=require('../n11-s9-n22-complete-20261027/verify.js');
memo(n22,'inventory');memo(n22,'priorProofs');
const p=require('../n11-s9-n24-priority-20261028/prove.js');memo(p,'source');
const short=require('../n11-s9-short-single-parent-20261028/prove.js');memo(short,'inventory');
const r2=require('../n11-s9-n24-round2-20261028/prove.js');memo(r2,'selection');
const r3=require('../n11-s9-n24-round3-20261028/prove.js');memo(r3,'inventory');
const r4=require('../n11-s9-n24-round4-20261028/prove.js');memo(r4,'inventory');
const r5=require('../n11-s9-n24-round5-20261028/prove.js');memo(r5,'inventory');
const r6=require('../n11-s9-n24-round6-20261028/prove.js');memo(r6,'inventory');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');memo(r7,'inventory');
function add(cache,h,win,source){
  const old=cache.get(h);
  if(old&&old.win!==win)throw Error('WIN/LOSS CONFLICT '+h+' '+old.source+' '+source);
  if(!old)cache.set(h,{win,source});
}
function ingest(cache,dir,keys,expected,known9){
  const c=read(dir),w=Buffer.from(c.witnessBase64,'base64');
  need(c.board===11&&c.perspective==='original-first-player'&&c.emptyBoard==='UNKNOWN',
    'certificate header '+dir);
  need(keys.length===expected&&w.length===keys.length&&
    sha(w)===c.witnessSha256&&
    sha(keys.join('\n')+'\n')===(c.selectionSha256||c.candidateSha256),
    'certificate identity '+dir);
  let wins=0,losses=0;
  for(let i=0;i<keys.length;i++){
    if(known9)add(known9,keys[i],w[i]===255,dir+':root:'+i);
    const children=[...g.children(g.board(keys[i],9))].sort();
    if(w[i]===255){wins++;for(const h of children)add(cache,h,true,dir+':'+i);}
    else{need(w[i]<children.length,'bad witness index '+dir+':'+i);
      losses++;add(cache,children[w[i]],false,dir+':'+i);}
  }
  need((c.win9??c.winRoots)===wins&&(c.loss9??c.lossRoots)===losses,
    'certificate verdict count '+dir);
  return {batch:dir,win9:wins,loss9:losses};
}
function n23Selections(inv){
  const w22=Buffer.from(read('n11-s9-n22-complete-20261027').witnessBase64,'base64');
  const before=n22.priorProofs().before;
  const secured22=new Set([...before,...g.reverse(inv.candidates.filter((_,i)=>w22[i]===255))]);
  need(secured22.size===4944,'n23 prior S8');
  const choices=[];
  for(const [h,parents] of inv.by9){
    if(parents.size<2||g.children(g.board(h,9)).size!==23)continue;
    const gaps=[...parents].filter(x=>inv.plan8.has(x)&&!secured22.has(x)).length;
    choices.push({h,degree:parents.size,gaps});
  }
  choices.sort((a,b)=>b.gaps-a.gaps||b.degree-a.degree||a.h.localeCompare(b.h));
  const pos=choices.filter(x=>x.gaps>0);
  need(choices.length===877&&pos.length===445,'n23 census');
  const first=pos.slice(0,256).map(x=>x.h);
  const c23=read('n11-s9-n23-priority-20261027'),w23=Buffer.from(c23.witnessBase64,'base64');
  need(sha(first.join('\n')+'\n')===c23.selectionSha256,'n23 first identity');
  const secured23=new Set([...secured22,...g.reverse(first.filter((_,i)=>w23[i]===255))]);
  need(secured23.size===5120,'n23 secured S8');
  const fresh=pos.slice(256).map(x=>({...x,gaps2:[...inv.by9.get(x.h)]
    .filter(h=>inv.plan8.has(h)&&!secured23.has(h)).length}))
    .filter(x=>x.gaps2>0);
  fresh.sort((a,b)=>b.gaps2-a.gaps2||b.degree-a.degree||a.h.localeCompare(b.h));
  need(fresh.length===157,'n23 remaining census');
  return [first,fresh.map(x=>x.h)];
}
function classify(options,cache,known){
  const rows=options.filter(x=>!known.has(x.h)),lookup=new Map(rows.map(x=>[x.h,x]));
  const W=new Map(),L=new Map();
  for(const [leaf,v] of cache)for(const parent of g.reverse([leaf])){
    if(!lookup.has(parent))continue;
    const m=v.win?W:L;
    if(!m.has(parent))m.set(parent,new Set());
    m.get(parent).add(leaf);
  }
  const freeLoss=[],freeWin=[];let partial=0,winEdges=0,touched=0;
  for(const x of rows){
    const w=W.get(x.h)||new Set(),l=L.get(x.h)||new Set();
    need(w.size+l.size<=x.children,'S9 incidence exceeds child count '+x.h);
    winEdges+=w.size;if(w.size||l.size)touched++;
    if(l.size)freeLoss.push({h:x.h,leaf:[...l][0]});
    else if(w.size===x.children)freeWin.push({h:x.h,leaves:[...w]});
    else if(w.size)partial++;
  }
  return {rows,freeLoss,freeWin,partial,winEdges,touched};
}
function test(){
  const c=new Map();add(c,'x',true,'a');add(c,'x',true,'b');
  let fail=false;try{add(c,'x',false,'c');}catch(e){fail=/CONFLICT/.test(e.message);}
  need(fail,'conflict rejection regression');
  const x=classify([{h:'0'.repeat(31)+'1',children:2}],new Map(),new Set());
  need(!x.freeWin.length&&!x.freeLoss.length,'UNKNOWN must not be promoted');
}
function run(){
  test();let inv,source,si,s2,s3,s4,s5,s6,s7;
  const original=console.log;
  try{console.log=()=>{};
    inv=n22.inventory();source=p.source();si=short.inventory();
    s2=r2.selection();s3=r3.inventory();s4=r4.inventory();
    s5=r5.inventory();s6=r6.inventory();s7=r7.inventory();
  }finally{console.log=original;}
  const cache=new Map(),known9=new Map(),batches=[];
  const addBatch=(d,keys,n)=>batches.push(ingest(cache,d,keys,n,known9));
  addBatch('n11-s9-n22-complete-20261027',inv.candidates,890);
  const [first,remaining]=n23Selections(inv);
  addBatch('n11-s9-n23-priority-20261027',first,256);
  addBatch('n11-s9-n23-remaining-20261027',remaining,157);
  const sets=[
    ['n11-s9-n24-priority-20261028',source.selected],
    ['n11-s9-short-single-parent-20261028',si.selected],
    ['n11-s9-n24-round2-20261028',s2.selected],
    ['n11-s9-n24-round3-20261028',s3.selected],
    ['n11-s9-n24-round4-20261028',s4.selected],
    ['n11-s9-n24-round5-20261028',s5.selected],
    ['n11-s9-n24-round6-20261028',s6.selected],
    ['n11-s9-n24-round7-20261028',s7.selected]
  ];
  for(const [d,rows] of sets)addBatch(d,rows.map(x=>x.h),rows.length);
  const known=new Set([...inv.candidates,...first,...remaining,
    ...sets.flatMap(x=>x[1].map(y=>y.h))]);
  const a=classify(s7.options,cache,known),secured=new Set(s7.secured);
  for(const {h,leaf} of a.freeLoss){
    need(g.children(g.board(h,9)).has(leaf)&&ind.children4(h).has(leaf),
      'reverse LOSS incidence failed '+h);
  }
  for(const {h,leaves} of a.freeWin){
    const children=g.children(g.board(h,9));
    need(same(children,new Set(leaves))&&same(children,ind.children4(h)),
      'WIN universal boundary failed '+h);
    for(const parent of g.reverse([h])){
      need(g.children(g.board(parent,8)).has(h)&&ind.children4(parent).has(h),
        'WIN reverse S8 incidence failed '+h);
      need(!s7.s.loss.has(parent),'S8 WIN/LOSS CONFLICT '+parent);
      secured.add(parent);
    }
  }
  const missing=[...s7.s.plan8].filter(h=>!secured.has(h)).length;
  need(missing<=100,'conditional coverage regression');
  const win10=[...cache.values()].filter(x=>x.win).length;
  const result={schema:'n11-s10-cross-batch-reuse-v1',emptyBoard:'UNKNOWN',
    trust:'terminal witnesses from previously verified frozen certificates; independently checked reverse geometry, not all terminal recursions',
    batches,distinctS10:cache.size,win10,loss10:cache.size-win10,conflicts:0,
    remainingS9:a.rows.length,freeLoss9:a.freeLoss.length,freeWin9:a.freeWin.length,
    partialWin10Candidates:a.partial,candidatesTouched:a.touched,
    knownWin10Edges:a.winEdges,newS8Win:secured.size-s7.secured.size,
    proofOnlyS8Win:secured.size,unprovedConditionalEdges:missing,
    twoStoneClosures:0,
    examplesFreeLoss9:a.freeLoss.slice(0,6),examplesFreeWin9:a.freeWin.slice(0,6).map(x=>x.h)};
  const saved=path.join(__dirname,'report.json');
  if(fs.existsSync(saved))need(
    JSON.stringify(JSON.parse(fs.readFileSync(saved)))===JSON.stringify(result),
    'frozen cross-batch summary differs');
  const derivedLoss9=a.freeLoss.map(({h,leaf})=>({
    h,loss10:leaf,source:cache.get(leaf).source
  })).sort((a,b)=>a.h.localeCompare(b.h));
  const fixed=path.join(__dirname,'derived-loss9.json');
  if(fs.existsSync(fixed))need(
    JSON.stringify(JSON.parse(fs.readFileSync(fixed)))===JSON.stringify(derivedLoss9),
    'frozen derived LOSS9 witnesses differ');
  if(process.argv.includes('--export-loss10')){
    const loss10=[...cache].filter(([,v])=>!v.win).map(([h,v])=>({h,source:v.source}))
      .sort((a,b)=>a.h.localeCompare(b.h));
    const knownWin9=[...known9].filter(([,v])=>v.win).map(([h])=>h).sort();
    need(loss10.length===result.loss10,'certified LOSS10 export count');
    console.log(JSON.stringify({schema:'n11-certified-loss10-export-v1',
      emptyBoard:'UNKNOWN',loss10,knownWin9,distinctS10:cache.size,
      conflicts:0}));
    return result;
  }
  const output=process.argv.includes('--export')?{report:result,derivedLoss9}:result;
  console.log(JSON.stringify(output,null,2));return result;
}
if(require.main===module)run();
module.exports={run,add,classify,test};
