#!/usr/bin/env node
'use strict';
// Full legal S8->S9 incidence audit for the fixed fourteen-root N11 plan.
// Unlike the limited coordinator inventory, this visits every legal child.
// Only independently replayed terminal certificates count as verdicts.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const ind=require('../n11-s9-shared-plan14-eleven-win-20261027/verify_fast.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const replan=require('../n11-s9-post-round27-replan-20261030/replan.js');
const need=(x,m)=>{if(!x)throw Error(m)};
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function run(){
  // The replan independently checks all 19 terminal batches and WIN/LOSS
  // consistency before the present audit can use any of their claims.
  let plan;const log=console.log;
  try{console.log=()=>{};plan=replan.run();}
  finally{console.log=log;}
  need(plan.emptyBoard==='UNKNOWN'&&plan.proofOnlyWin8After===5859&&
    plan.conditionalUnprovedEdges===37&&plan.winLossConflicts===0,
    'unverified source frontier');
  const win9=new Set(),loss9=new Set();
  for(let n=9;n<=27;n++){
    const day=n<=11?'20261028':'20261029';
    const p=n===9?
      read('../n11-s9-post-s10-reuse-round8-20261028/next-plan.json'):
      read('../n11-s9-post-round'+(n-1)+'-replan-'+day+'/next-plan.json');
    const c=read('../n11-s9-post-round'+(n-1)+'-round'+n+'-'+day+'/certificate.json');
    const ws=Buffer.from(c.witnessBase64,'base64');
    need(ws.length===p.newSelectedKeys.length,'witness length '+n);
    for(let i=0;i<ws.length;i++){
      const h=p.newSelectedKeys[i],w=ws[i];
      if(w===255){win9.add(h);continue;}
      const ordered=[...g.children(g.board(h,9))].sort();
      need(w<ordered.length,'invalid witness '+n);
      const leaf=BigInt('0x'+ordered[w]);
      for(const pt of g.pts(leaf)){
        const par=g.key(g.canonical(leaf^(1n<<BigInt(pt))));
        loss9.add(par);
      }
    }
  }
  need([...win9].every(h=>!loss9.has(h)),'certified WIN9/LOSS9 conflict');
  const inv=r7.inventory(),s=inv.s,secured=new Set(inv.secured);
  for(const h of g.reverse([...win9]))secured.add(h);
  need(secured.size===5859,'secured S8 count mismatch');
  const missing=[...s.plan8].filter(h=>!secured.has(h)).sort();
  need(missing.length===37,'fixed plan frontier mismatch');
  const incidence=new Map(),rows=[];
  for(const h of missing){
    const kids=g.children(g.board(h,8));
    need(same(kids,ind.children4(h)),'independent S8 geometry disagreement '+h);
    const knownWin=[...kids].filter(k=>win9.has(k));
    need(knownWin.length===0,'missing S8 already has certified WIN9 '+h);
    const knownLoss=[...kids].filter(k=>loss9.has(k));
    const unknown=[...kids].filter(k=>!win9.has(k)&&!loss9.has(k));
    for(const k of unknown){
      if(!incidence.has(k))incidence.set(k,[]);
      incidence.get(k).push(h);
    }
    rows.push({h,legal9:kids.size,certifiedLoss9:knownLoss.length,
      unknown9:unknown.length});
  }
  const ranked=[...incidence].map(([h,parents])=>({h,missing8Parents:parents.length}))
    .sort((a,b)=>b.missing8Parents-a.missing8Parents||a.h.localeCompare(b.h));
  const top9=ranked.slice(0,20).map(x=>({
    ...x,legal10:g.children(g.board(x.h,9)).size
  }));
  const zeros=rows.filter(x=>x.unknown9===0);
  const result={
    schema:'n11-fixed14-complete-s8-s9-incidence-v1',
    emptyBoard:'UNKNOWN',
    sourceReplanSelectionSha256:plan.newSelectionSha256,
    sourceRound27WitnessSha256:plan.sourceWitnessSha256,
    proofOnlyWin8:secured.size,
    fixedPlanUnprovedS8:missing.length,
    certifiedWin9:win9.size,certifiedLoss9:loss9.size,
    distinctUnknown9:incidence.size,
    completeS8ToS9Edges:rows.reduce((n,x)=>n+x.legal9,0),
    certifiedLoss9Edges:rows.reduce((n,x)=>n+x.certifiedLoss9,0),
    unknown9Edges:rows.reduce((n,x)=>n+x.unknown9,0),
    newProvenLoss8:zeros.length,
    provenLoss8Keys:zeros.map(x=>x.h),
    minUnknown9:Math.min(...rows.map(x=>x.unknown9)),
    maxUnknown9:Math.max(...rows.map(x=>x.unknown9)),
    topUnknown9ByPotentialWIN8Coverage:top9,
    s8Rows:rows,
    newTwoStoneClosures:0,
    winLossConflicts:0
  };
  const fixed=path.join(__dirname,'incidence.json');
  if(fs.existsSync(fixed))need(
    JSON.stringify(read('incidence.json'))===JSON.stringify(result),
    'fixed incidence audit mismatch');
  console.log(JSON.stringify(result,null,2));
  return result;
}
if(require.main===module)run();
module.exports={run};
