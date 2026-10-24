#!/usr/bin/env node
'use strict';
// Structural composition of previously terminal-verified certificates.
// No verdict is inferred from an unfinished search or a frozen verdict cache.
const fs = require('node:fs');
const path = require('node:path');
const N=11, P=121, BITS=Array.from({length:P},(_,i)=>1n<<BigInt(i));
const XY=Array.from({length:P},(_,i)=>[i%N,Math.floor(i/N)]);
const TRANS=Array.from({length:8},()=>[]);
for(let p=0;p<P;p++){
  const [x,y]=XY[p];
  const a=[[x,y],[10-y,x],[10-x,10-y],[y,10-x],[10-x,y],[10-y,10-x],[x,10-y],[y,x]];
  for(let t=0;t<8;t++)TRANS[t][p]=BITS[11*a[t][1]+a[t][0]];
}
function need(ok,msg){if(!ok)throw Error(msg);}
function key(b){return b.toString(16).padStart(32,'0');}
function points(b){const a=[];for(let p=0;p<P;p++)if(b&BITS[p])a.push(p);return a;}
function canonical(b){
  const pp=points(b);let best=null;
  for(const tr of TRANS){let v=0n;for(const p of pp)v|=tr[p];if(best===null||v<best)best=v;}
  return best;
}
function circle(a,b,c,d){
  const [x,y]=XY[d];
  const v=[a,b,c].map(p=>{const [u,w]=XY[p];return [u-x,w-y,u*u+w*w-x*x-y*y];});
  const [u,w,z]=v;
  return u[0]*(w[1]*z[2]-w[2]*z[1])-u[1]*(w[0]*z[2]-w[2]*z[0])
       +u[2]*(w[0]*z[1]-w[1]*z[0])===0;
}
function safe(b){
  const pp=points(b);
  for(let i=0;i<pp.length-3;i++)for(let j=i+1;j<pp.length-2;j++)
  for(let k=j+1;k<pp.length-1;k++)for(let l=k+1;l<pp.length;l++)
    if(circle(pp[i],pp[j],pp[k],pp[l]))return false;
  return true;
}
function children(b){
  const pp=points(b),tri=[];
  for(let i=0;i<pp.length-2;i++)for(let j=i+1;j<pp.length-1;j++)
    for(let k=j+1;k<pp.length;k++)tri.push([pp[i],pp[j],pp[k]]);
  const moves=[],classes=new Set();
  for(let p=0;p<P;p++){
    if((b&BITS[p])||tri.some(q=>circle(q[0],q[1],q[2],p)))continue;
    moves.push(p);classes.add(key(canonical(b|BITS[p])));
  }
  return {moves,classes};
}
function readKeys(s,n,stones,label,sorted=true){
  const rows=s.trim().split(/\s+/);
  need(rows.length===n && rows.every(x=>/^[0-9a-f]{32}$/.test(x)),label+' bad count/keys');
  need(new Set(rows).size===n,label+' duplicate');
  if(sorted)need(rows.every((x,i)=>i===0||rows[i-1]<x),label+' unsorted');
  const out=rows.map(x=>BigInt('0x'+x));
  for(const b of out)need(points(b).length===stones&&canonical(b)===b&&safe(b),label+' invalid '+key(b));
  return out;
}
function reverse(boards){
  const out=new Map();
  for(const b of boards)for(const p of points(b)){
    const v=canonical(b^BITS[p]);out.set(key(v),v);
  }
  return out;
}
// Read and check each WIN root's complete S9 witness -> S10 boundary.
// The original experiments separately prove S10 terminal verdicts.
function proofWins(text,nRoots,nWins,label){
  const blocks=[];
  for(const line of text.trim().split(/\r?\n/)){
    const a=line.split('\t');
    if(a[0]==='ROOT'){
      need(a.length===5&&/^[0-9a-f]{32}$/.test(a[1])&&['WIN','LOSS'].includes(a[2]),label+' bad ROOT');
      blocks.push({root:a[1],verdict:a[2],legal:Number(a[3]),rows:[]});
    }else{
      need(blocks.length>0,label+' evidence before ROOT');
      blocks[blocks.length-1].rows.push(a);
    }
  }
  need(blocks.length===nRoots,label+' wrong root count');
  const seen=new Set(),wins=[];
  for(const block of blocks){
    const b=BigInt('0x'+block.root);
    need(!seen.has(block.root)&&points(b).length===8&&canonical(b)===b&&safe(b),label+' invalid root');
    seen.add(block.root);
    const c9=children(b).classes;
    need(c9.size===block.legal,label+' root legal class mismatch '+block.root);
    if(block.verdict==='WIN'){
      need(block.rows.length>1&&block.rows[0][0]==='S9_LOSS'&&block.rows[0].length===2,label+' missing S9 witness');
      const witness=block.rows[0][1],s9=BigInt('0x'+witness);
      need(c9.has(witness),label+' S9 witness not legal');
      const leaves=block.rows.slice(1);
      need(leaves.every(x=>x.length===2&&x[0]==='S10_WIN'&&/^[0-9a-f]{32}$/.test(x[1])),label+' invalid S10 rows');
      const actual=new Set(leaves.map(x=>x[1]));
      need(actual.size===leaves.length,label+' duplicate S10');
      const required=children(s9).classes;
      need(actual.size===required.size&&[...actual].every(k=>required.has(k)),label+' incomplete S10 boundary');
      wins.push(b);
    }else{
      need(block.rows.length===c9.size&&block.rows.every(x=>x.length===3&&x[0]==='S9_WIN'),label+' incomplete LOSS S9 rows');
      const rows=new Map(block.rows.map(x=>[x[1],x[2]]));
      need(rows.size===c9.size&&[...rows.keys()].every(k=>c9.has(k)),label+' bad LOSS S9 obligations');
      for(const [k,v] of rows)need(children(BigInt('0x'+k)).classes.has(v),label+' invalid LOSS witness');
    }
  }
  need(wins.length===nWins,label+' wrong WIN count');
  return wins;
}
function evaluate(parents,wins,loss7){
  let legal=0,covered=0,distinctLegal=0,distinctCovered=0;
  const closed=[],rows=[];let knownLoss=0;
  for(const b of parents.values()){
    const {moves,classes}=children(b),coveredClasses=new Set();
    let coveredMoves=0;
    for(const p of moves){
      const k=key(canonical(b|BITS[p]));
      if(wins.has(k)){coveredMoves++;coveredClasses.add(k);}
    }
    legal+=moves.length;covered+=coveredMoves;
    distinctLegal+=classes.size;distinctCovered+=coveredClasses.size;
    const k=key(b),isLoss=loss7.has(k);
    if(isLoss)knownLoss++;
    if(coveredMoves===moves.length)closed.push(k);
    rows.push({key:k,legal:moves.length,covered:coveredMoves,
      distinctLegal:classes.size,distinctCovered:coveredClasses.size,
      distinctGap:classes.size-coveredClasses.size,knownLoss:isLoss});
  }
  const active=rows.filter(x=>!x.knownLoss&&!closed.includes(x.key)).sort((a,b)=>
    a.distinctGap-b.distinctGap||b.distinctCovered-a.distinctCovered||a.key.localeCompare(b.key));
  return {parents:parents.size,legal,covered,distinctLegal,distinctCovered,knownLoss,
    closed:closed.sort(),topUnclosed:active.slice(0,5)};
}
function audit(data){
  need(data.winGroups.length===7,'seven WIN9 proof groups required');
  const sizes=[29,27,2,10,7,20,7];
  const old=JSON.parse(data.oldCert);
  const win9=data.winGroups.flatMap((s,i)=>readKeys(s,sizes[i],9,'WIN9 group '+i))
    .concat(old.new_s9_win.map(x=>BigInt('0x'+x)));
  need(win9.length===120&&new Set(win9.map(key)).size===120,'WIN9 union changed');
  for(const b of old.new_s9_win.map(x=>BigInt('0x'+x)))
    need(points(b).length===9&&canonical(b)===b&&safe(b),'old WIN9 invalid');
  const old8=reverse(win9);
  need(old8.size===961,'old WIN8 union changed');
  const loss8=readKeys(data.loss35,35,8,'LOSS8 35')
    .concat(old.s8_loss.map(x=>BigInt('0x'+x)));
  need(loss8.length===38&&new Set(loss8.map(key)).size===38,'LOSS8 union changed');
  for(const b of loss8)need(points(b).length===8&&canonical(b)===b&&safe(b),'bad LOSS8');
  const loss7=reverse(loss8);
  const s7root=BigInt('0x00000000100100009001010000001000');
  const s7Children=children(s7root).classes;
  const direct38=readKeys(data.direct38,38,8,'direct38',false);
  need(s7Children.size===38&&new Set(direct38.map(key)).size===38&&
    direct38.every(b=>s7Children.has(key(b))),'38-child WIN7 certificate boundary mismatch');
  const p38=proofWins(data.proof38,38,38,'S7-38 proof');
  need(new Set(p38.map(key)).size===38&&p38.every(b=>s7Children.has(key(b))),'38 proof roots mismatch');
  const p24=proofWins(data.proof24,24,20,'round8 proof');
  const p22=proofWins(data.proof22,22,16,'round9 proof');
  const direct=[...p38,...p24,...p22];
  need(direct.length===74&&new Set(direct.map(key)).size===74,'direct WIN8 duplicates');
  const win8=new Map(old8);
  for(const b of direct)win8.set(key(b),b);
  need(win8.size===1025,'WIN8 union count changed');
  const loss8Keys=new Set(loss8.map(key));
  need(![...win8.keys()].some(k=>loss8Keys.has(k)),'WIN8/LOSS8 conflict');
  const before=evaluate(reverse(old8.values()),old8,loss7);
  const after=evaluate(reverse(win8.values()),win8,loss7);
  need(before.parents===3337&&before.legal===209225&&before.covered===7690&&
    before.distinctLegal===209205&&before.distinctCovered===7688&&
    before.knownLoss===15&&before.closed.length===0,'baseline regression');
  need(after.parents===3786&&after.legal===232986&&after.covered===8202&&
    after.distinctLegal===232966&&after.distinctCovered===8200&&
    after.knownLoss===24&&after.closed.length===1&&
    after.closed[0]===key(s7root),'direct8 union regression');
  need(after.topUnclosed[0].key==='00000010001000009200001000100000'&&
    after.topUnclosed[0].distinctGap===18,'minimum gap changed');
  need(!loss7.has(after.closed[0]),'closed WIN7 conflicts with LOSS7');
  return {independentWin9Roots:win9.length,directWin8Roots:direct.length,
    win8Old:old8.size,win8Union:win8.size,win8Added:win8.size-old8.size,
    before,after,delta:{s7Candidates:after.parents-before.parents,
      securedMoveEdges:after.covered-before.covered,
      securedClassEdges:after.distinctCovered-before.distinctCovered},
    trustBoundary:'structural composition of prior terminal certificates; terminal leaves not rerun',
    emptyBoard:'UNKNOWN'};
}
module.exports={audit};
if(require.main===module){
  const exp=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(exp,p),'utf8');
  const groups=[
    'n11-s9-win29-lift-20261023/s9-win29.keys',
    'n11-s9-win27-expansion-20261024/s9-win27.keys',
    'n11-s9-win2-followup-20261024/s9-win2.keys',
    'n11-s9-win10-20261024/s9-win10.keys',
    'n11-s9-win7-expansion-20261024/s9-win7.keys',
    'n11-s9-win20-neighbor-20261024/s9-win20.keys',
    'n11-s8-frontier-13way-20261024/s9-win7.keys'];
  const data={winGroups:groups.map(read),
    oldCert:read('n11-s7-terminal-loss12-20261024/certificate.json'),
    loss35:read('n11-s8-compact385-pruned1946-20261020/loss_roots35.txt'),
    direct38:read('n11-s7-38-terminal-20261019/s8_38_children.txt'),
    proof38:read('n11-s7-38-terminal-20261019/s8_38_win_proof.tsv'),
    proof24:read('n11-s8-neighbor24-round8-20261020/proof24_optimized.tsv'),
    proof22:read('n11-s8-round9-global78-20261020/round9_proof_optimized.tsv')};
  const result=audit(data);
  need(result.delta.securedClassEdges===512,'unexpected coverage delta');
  console.log(JSON.stringify(result,null,2));
  if(process.env.NEGATIVE==='1'){
    for(const field of ['direct38','proof38','proof24','proof22']){
      const mutated={...data,[field]:data[field].split('\n').slice(1).join('\n')};
      let rejected=false;try{audit(mutated);}catch(_){rejected=true;}
      need(rejected,'mutation not rejected: '+field);
    }
    console.error('PASS negative controls');
  }
}
