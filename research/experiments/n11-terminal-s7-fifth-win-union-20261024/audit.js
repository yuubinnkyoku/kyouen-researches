#!/usr/bin/env node
'use strict';
// Certificate-only coverage composition. Terminal S10 verdicts are inherited
// from the independently checked fifth-S7 proof, not recomputed here.
const fs=require('node:fs'),path=require('node:path');
const {audit:oldAudit}=require('../n11-terminal-s7-four-win-union-20261024/audit.js');
const B=Array.from({length:121},(_,i)=>1n<<BigInt(i));
const XY=B.map((_,i)=>[i%11,Math.floor(i/11)]);
const T=Array.from({length:8},()=>[]);
for(let p=0;p<121;p++){const [x,y]=XY[p];
  const a=[[x,y],[10-y,x],[10-x,10-y],[y,10-x],[10-x,y],[10-y,10-x],[x,10-y],[y,x]];
  for(let t=0;t<8;t++)T[t][p]=B[11*a[t][1]+a[t][0]];}
function need(x,msg){if(!x)throw Error(msg);}
function key(b){return b.toString(16).padStart(32,'0');}
function pts(b){const p=[];for(let i=0;i<121;i++)if(b&B[i])p.push(i);return p;}
function canon(b){const p=pts(b);let best=null;
  for(const tr of T){let v=0n;for(const i of p)v|=tr[i];if(best===null||v<best)best=v;}
  return best;}
function circle(a,b,c,d){const [x,y]=XY[d];
  const [u,v,w]=[a,b,c].map(p=>{const [i,j]=XY[p];return [i-x,j-y,i*i+j*j-x*x-y*y];});
  return u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])
    +u[2]*(v[0]*w[1]-v[1]*w[0])===0;}
function safe(b){const p=pts(b);
  for(let i=0;i<p.length-3;i++)for(let j=i+1;j<p.length-2;j++)
  for(let k=j+1;k<p.length-1;k++)for(let l=k+1;l<p.length;l++)
    if(circle(p[i],p[j],p[k],p[l]))return false;
  return true;}
function children(b){const p=pts(b),tri=[],moves=[],classes=new Set();
  for(let i=0;i<p.length-2;i++)for(let j=i+1;j<p.length-1;j++)
  for(let k=j+1;k<p.length;k++)tri.push([p[i],p[j],p[k]]);
  for(let i=0;i<121;i++){if(b&B[i]||tri.some(t=>circle(...t,i)))continue;
    moves.push(i);classes.add(key(canon(b|B[i])));}
  return {moves,classes};}
function reverse(keys){const out=new Set();
  for(const k of keys){need(/^[0-9a-f]{32}$/.test(k),'bad reverse key');
    const b=BigInt('0x'+k);for(const p of pts(b))out.add(key(canon(b^B[p])));}
  return out;}
function parseFifth(text){
  need(text.startsWith('# n11-S7-WIN-terminal-v1'),'wrong certificate version');
  const lines=text.trim().split(/\r?\n/).filter(x=>x&&!x.startsWith('#'));
  need(lines.length===38&&lines[0]==='BOARD 11'&&lines[37]==='END','bad fifth certificate frame');
  const m=lines[1].match(/^ROOT ([0-9a-f]{32}) 35$/);need(m,'bad ROOT');
  const root=m[1],b=BigInt('0x'+root);
  need(pts(b).length===7&&key(canon(b))===root&&safe(b),'bad S7 root');
  const required=children(b).classes,wins=new Set(),s9=new Set();
  need(required.size===35,'S7 child count changed');
  for(const line of lines.slice(2,37)){
    const e=line.match(/^EDGE ([0-9a-f]{32}) ([0-9a-f]{32})$/);need(e,'bad EDGE');
    const a=BigInt('0x'+e[1]),w=BigInt('0x'+e[2]);
    need(!wins.has(e[1])&&required.has(e[1]),'duplicate/illegal S8');
    need(pts(a).length===8&&key(canon(a))===e[1]&&safe(a),'bad S8');
    need(pts(w).length===9&&key(canon(w))===e[2]&&safe(w),'bad S9');
    need(children(a).classes.has(e[2]),'illegal S9 witness');
    wins.add(e[1]);s9.add(e[2]);}
  need(wins.size===35&&[...required].every(x=>wins.has(x)),'missing S8 child');
  return {root,wins,s9};}
function verify(d){
  const old=oldAudit({winGroups:d.groups,oldCert:d.oldCert,loss35:d.loss35,
    direct38:d.direct38,proof38:d.proof38,proof24:d.proof24,
    proof22:d.proof22,fourCert:d.fourCert}).fourWinExtension;
  need(old.win8Total===1175&&old.s7Candidates===4725&&old.securedMoveEdges===9402&&
    old.securedClassEdges===9400&&old.closed7.length===5&&
    old.topUnclosed[0].distinctGap===18,'baseline changed');
  const lossCert=JSON.parse(d.oldCert),four=JSON.parse(d.fourCert);
  const s9=new Set(d.groups.flatMap(x=>x.trim().split(/\s+/)).concat(lossCert.new_s9_win));
  need(s9.size===120,'baseline S9 changed');
  const old8=reverse(s9);
  const counts=[];
  for(const s of [d.proof38,d.proof24,d.proof22]){
    const keys=s.split(/\r?\n/).filter(x=>x.startsWith('ROOT\t'))
      .map(x=>x.split('\t')).filter(x=>x[2]==='WIN').map(x=>x[1]);
    counts.push(keys.length);for(const k of keys)old8.add(k);}
  need(counts.join(',')==='38,20,16','direct S8 count changed');
  for(const k of Object.keys(four.s8_witness))old8.add(k);
  need(old8.size===1175&&reverse(old8).size===4725,'baseline S8/parent union changed');
  const fifth=parseFifth(d.fifth),loss8=new Set(d.loss35.trim().split(/\s+/).concat(lossCert.s8_loss));
  need(loss8.size===38,'LOSS8 count changed');
  need([...fifth.wins].every(k=>!old8.has(k)&&!loss8.has(k)),'S8 overlap/conflict');
  const oldParents=reverse(old8),parents=reverse(fifth.wins),loss7=reverse(loss8);
  need(parents.size===246&&[...parents].every(k=>!oldParents.has(k)&&!loss7.has(k)),
    'new parent count/overlap/LOSS conflict changed');
  let moves=0,classes=0;const closed=[],open=[];
  for(const k of parents){const b=BigInt('0x'+k),ch=children(b);
    need(![...ch.classes].some(x=>old8.has(x)),'old WIN8 in new parent');
    const covered=[...ch.classes].filter(x=>fifth.wins.has(x)).length;
    classes+=covered;
    for(const p of ch.moves)if(fifth.wins.has(key(canon(b|B[p]))))moves++;
    if(covered===ch.classes.size)closed.push(k);
    else open.push({key:k,gap:ch.classes.size-covered,covered});}
  open.sort((a,b)=>a.gap-b.gap||b.covered-a.covered||a.key.localeCompare(b.key));
  need(moves===280&&classes===280&&closed.length===1&&closed[0]===fifth.root&&
    open[0].gap===33,'fifth extension regression');
  return {newWin8:35,totalWin8:1210,newS7Parents:246,totalS7Parents:4971,
    newSecuredMoveEdges:moves,totalSecuredMoveEdges:old.securedMoveEdges+moves,
    newSecuredClassEdges:classes,totalSecuredClassEdges:old.securedClassEdges+classes,
    certifiedFifthRoot:fifth.root,certifiedFifthChildren:fifth.wins.size,
    distinctS9Witnesses:fifth.s9.size,closedS7:6,
    newlySolvedS7:0,minimumUnknownClassGap:Math.min(18,open[0].gap),
    winLossConflicts:0,emptyBoard:'UNKNOWN'};}
module.exports={verify,parseFifth};
if(require.main===module){
  const dir=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(dir,p),'utf8');
  const d={groups:[
    'n11-s9-win29-lift-20261023/s9-win29.keys',
    'n11-s9-win27-expansion-20261024/s9-win27.keys',
    'n11-s9-win2-followup-20261024/s9-win2.keys',
    'n11-s9-win10-20261024/s9-win10.keys',
    'n11-s9-win7-expansion-20261024/s9-win7.keys',
    'n11-s9-win20-neighbor-20261024/s9-win20.keys',
    'n11-s8-frontier-13way-20261024/s9-win7.keys'].map(read),
    oldCert:read('n11-s7-terminal-loss12-20261024/certificate.json'),
    loss35:read('n11-s8-compact385-pruned1946-20261020/loss_roots35.txt'),
    direct38:read('n11-s7-38-terminal-20261019/s8_38_children.txt'),
    proof38:read('n11-s7-38-terminal-20261019/s8_38_win_proof.tsv'),
    proof24:read('n11-s8-neighbor24-round8-20261020/proof24_optimized.tsv'),
    proof22:read('n11-s8-round9-global78-20261020/round9_proof_optimized.tsv'),
    fourCert:read('n11-s7-four-win-terminal-20261020/s7_win_four_min_certificate.json'),
    fifth:read('n11-s7-fifth-terminal-20261015/fifth-s7-win-terminal.cert')};
  console.log(JSON.stringify(verify(d),null,2));
  if(process.env.NEGATIVE==='1'){
    const lines=d.fifth.trimEnd().split('\n'),idx=lines.findIndex(x=>x.startsWith('EDGE '));
    const bad=[lines.filter((_,i)=>i!==idx).join('\n'),
      lines.map((x,i)=>i===idx?x.split(' ').slice(0,2).join(' ')+' '+x.split(' ')[1]:x).join('\n'),
      lines.map((x,i)=>i===idx+1?lines[idx]:x).join('\n'),
      d.fifth.replace('BOARD 11','BOARD 10')];
    for(const s of bad){let rejected=false;try{parseFifth(s);}catch(_){rejected=true;}
      need(rejected,'mutation accepted');}
    console.error('PASS four fifth-certificate negative controls');
  }
}
