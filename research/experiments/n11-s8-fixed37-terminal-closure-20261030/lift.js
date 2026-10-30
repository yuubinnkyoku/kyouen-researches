#!/usr/bin/env node
'use strict';
// Lift the independently verified fixed37 S8 verdicts to the conditional
// fourteen S7 roots. No partial search state or inferred S9 verdict is used.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const r7=require('../n11-s9-n24-round7-20261028/prove.js');
const batch=require('./verify.js');
const need=(x,msg)=>{if(!x)throw Error(msg)};
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),'utf8'));
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');

function run(){
  const cert=read('certificate.json');
  const checked=batch.verify(cert,false);
  need(checked.verified&&checked.win8===8&&checked.loss8===29,
       'new S8 proof verification failed');
  const inv=r7.inventory(),s=inv.s;
  const win9=new Set();
  for(let n=9;n<=27;n++){
    const day=n<=12?'20261028':'20261029';
    const p=n===9?
      read('../n11-s9-post-s10-reuse-round8-20261028/next-plan.json'):
      read('../n11-s9-post-round'+(n-1)+'-replan-'+day+'/next-plan.json');
    const c=read('../n11-s9-post-round'+(n-1)+'-round'+n+'-'+day+'/certificate.json');
    const raw=Buffer.from(c.witnessBase64,'base64');
    need(raw.length===p.newSelectedKeys.length&&
         sha(raw)===c.witnessSha256&&
         sha(p.newSelectedKeys.join('\n')+'\n')===c.selectionSha256,
         'historical certificate identity '+n);
    for(let i=0;i<raw.length;i++)if(raw[i]===255)win9.add(p.newSelectedKeys[i]);
  }
  const secured=new Set([...inv.secured,...g.reverse([...win9])]);
  need(secured.size===5859,'historical WIN8 count');
  const missing=[...s.plan8].filter(h=>!secured.has(h)).sort();
  need(missing.length===37&&JSON.stringify(missing)===
       JSON.stringify(cert.rows.map(r=>r[0])),'fixed37 mismatch');
  const newWin=new Set(cert.rows.filter(r=>r[1]==='W').map(r=>r[0]));
  const newLoss=new Set(cert.rows.filter(r=>r[1]==='L').map(r=>r[0]));
  need(newWin.size===8&&newLoss.size===29,'new verdict counts');
  need([...newWin].every(h=>!s.loss.has(h))&&
       [...newLoss].every(h=>!secured.has(h))&&
       [...newWin].every(h=>!newLoss.has(h)),'S8 WIN/LOSS conflict');
  const allWin=new Set([...secured,...newWin]);
  const allLoss=new Set([...s.loss,...newLoss]);
  need([...allWin].every(h=>!allLoss.has(h)),'merged S8 conflict');
  const rows=[];
  for(const h of s.plan){
    const kids=g.children(g.board(h,7));
    const losing=[...kids].filter(k=>allLoss.has(k)).sort();
    const unknown=[...kids].filter(k=>!allLoss.has(k)&&!allWin.has(k)).sort();
    let verdict='UNKNOWN',witness=null;
    if(losing.length){verdict='WIN';witness=losing[0];}
    else if(!unknown.length){verdict='LOSS';}
    rows.push({s7:h,legal8:kids.size,knownLoss8Children:losing.length,
               unproved8Children:unknown.length,verdict,witness});
  }
  const counts={win7:rows.filter(r=>r.verdict==='WIN').length,
                loss7:rows.filter(r=>r.verdict==='LOSS').length,
                unknown7:rows.filter(r=>r.verdict==='UNKNOWN').length};
  need(rows.length===14&&counts.win7+counts.loss7+counts.unknown7===14,
       'conditional fourteen roots');
  const result={schema:'n11-fixed14-direct37-s7-lift-v1',emptyBoard:'UNKNOWN',
    sourceFixed37:cert.schema,historicalWin8:secured.size,
    newWin8:newWin.size,newLoss8:newLoss.size,
    mergedWin8:allWin.size,mergedLoss8:allLoss.size,
    knownLoss8Before:s.loss.size,remainingUnknown8Of37:0,
    ...counts,rows,winLossConflicts:0,twoStoneRootClosureChecked:false};
  const fixed=path.join(__dirname,'lift_result.json');
  if(fs.existsSync(fixed))need(JSON.stringify(read('lift_result.json'))===
      JSON.stringify(result),'frozen lift mismatch');
  console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)run();
module.exports={run};
