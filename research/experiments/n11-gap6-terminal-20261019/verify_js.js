#!/usr/bin/env node
'use strict';
// Exact, cache-free recheck of the 2026-10-19 gap6 S8 certificate.
// The zero determinant is the repository's forbidden-four definition.
const fs=require('node:fs'),path=require('node:path');
const B=Array.from({length:121},(_,i)=>1n<<BigInt(i));
const XY=B.map((_,i)=>[i%11,Math.floor(i/11)]);
const TR=Array.from({length:8},()=>[]);
for(let p=0;p<121;p++){
  const [x,y]=XY[p],a=[[x,y],[10-y,x],[10-x,10-y],[y,10-x],
    [10-x,y],[10-y,10-x],[x,10-y],[y,x]];
  for(let t=0;t<8;t++)TR[t][p]=B[11*a[t][1]+a[t][0]];
}
function check(x,msg){if(!x)throw Error(msg);}
function key(b){return b.toString(16).padStart(32,'0');}
function board(h,n){
  check(typeof h==='string'&&/^[0-9a-f]{32}$/.test(h),'invalid board key');
  const b=BigInt('0x'+h);
  check((b>>121n)===0n&&pts(b).length===n&&key(canonical(b))===h&&safe(b),
    'unsafe/noncanonical board '+h);
  return b;
}
function pts(b){const a=[];for(let i=0;i<121;i++)if(b&B[i])a.push(i);return a;}
function canonical(b){
  const pp=pts(b);let best=null;
  for(const tr of TR){let v=0n;for(const i of pp)v|=tr[i];if(best===null||v<best)best=v;}
  return best;
}
function circle(a,b,c,d){
  const [x,y]=XY[d],r=[a,b,c].map(p=>{
    const [u,v]=XY[p];return [u-x,v-y,u*u+v*v-x*x-y*y];});
  const [u,v,w]=r;
  return u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])
    +u[2]*(v[0]*w[1]-v[1]*w[0])===0;
}
function safe(b){
  const p=pts(b);
  for(let i=0;i<p.length-3;i++)for(let j=i+1;j<p.length-2;j++)
  for(let k=j+1;k<p.length-1;k++)for(let l=k+1;l<p.length;l++)
    if(circle(p[i],p[j],p[k],p[l]))return false;
  return true;
}
function legal(b){
  const p=pts(b),tri=[],out=[];
  for(let i=0;i<p.length-2;i++)for(let j=i+1;j<p.length-1;j++)
  for(let k=j+1;k<p.length;k++)tri.push([p[i],p[j],p[k]]);
  for(let i=0;i<121;i++)if(!(b&B[i])&&!tri.some(t=>circle(...t,i)))out.push(i);
  return out;
}
function children(b){return new Set(legal(b).map(i=>key(canonical(b|B[i]))));}
function reverse(keys){
  const out=new Set();
  for(const h of keys){const b=BigInt('0x'+h);
    for(const p of pts(b))out.add(key(canonical(b^B[p])));}
  return out;
}
function solve10(h){
  const b=board(h,10),base=pts(b),moves=legal(b),n=moves.length;
  check(n<=31,'terminal state bitmask overflow');
  const bad=[],hasSub=mask=>bad.some(v=>(mask&v)===v);
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
    let forbidden=false;
    for(let a=0;a<base.length&&!forbidden;a++)
      for(let c=a+1;c<base.length;c++)
        if(circle(base[a],base[c],moves[i],moves[j])){forbidden=true;break;}
    if(forbidden)bad.push((1<<i)|(1<<j));
  }
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let k=j+1;k<n;k++){
    const mask=(1<<i)|(1<<j)|(1<<k);
    if(!hasSub(mask)&&base.some(p=>circle(p,moves[i],moves[j],moves[k])))
      bad.push(mask);
  }
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)
  for(let k=j+1;k<n;k++)for(let l=k+1;l<n;l++){
    const mask=(1<<i)|(1<<j)|(1<<k)|(1<<l);
    if(!hasSub(mask)&&circle(moves[i],moves[j],moves[k],moves[l]))bad.push(mask);
  }
  const bans=Array.from({length:n},()=>[]);
  for(const mask of bad)for(let i=0;i<n;i++)if(mask&(1<<i))bans[i].push(mask^(1<<i));
  const memo=new Map();
  function win(state){
    if(memo.has(state))return memo.get(state);
    for(let i=0;i<n;i++){
      const bit=1<<i;
      if(state&bit||bans[i].some(v=>(state&v)===v))continue;
      if(!win(state|bit)){memo.set(state,true);return true;}
    }
    memo.set(state,false);return false;
  }
  return {win:win(0),states:memo.size,legal:n};
}
function verify(cert,{terminal=true}={}){
  check(cert.format==='n11-s8-gap6-terminal-certificate-v1','wrong format');
  check(Array.isArray(cert.s8_win_roots)&&cert.s8_win_roots.length===18,'wrong WIN8 count');
  const win8=new Set(),win10=new Set(),s9=new Set();
  for(const row of cert.s8_win_roots){
    const root=board(row.root,8),w=board(row.s9_witness,9);
    check(!win8.has(row.root),'duplicate WIN8');
    win8.add(row.root);
    check(children(root).has(row.s9_witness),'illegal WIN8 witness');
    const actual=children(w),listed=row.s10_win_children;
    check(Array.isArray(listed)&&listed.length===actual.size&&
      new Set(listed).size===actual.size&&listed.every(h=>actual.has(h)),
      'incomplete S10 WIN boundary '+row.root);
    s9.add(row.s9_witness);
    for(const h of listed)win10.add(h);
  }
  check(win10.size===337,'WIN leaf union changed');
  const lossRoot=board(cert.s8_loss_root,8);
  check(!win8.has(cert.s8_loss_root),'WIN/LOSS root conflict');
  const obligations=children(lossRoot),stored=cert.s8_loss_s9_obligations;
  check(obligations.size===26&&Array.isArray(stored)&&stored.length===26&&
    new Set(stored).size===26&&stored.every(h=>obligations.has(h)),
    'LOSS8 S9 obligations incomplete');
  const boundary=new Set(),covers=new Map();
  for(const h of obligations){
    const s=children(board(h,9));covers.set(h,s);
    for(const k of s)boundary.add(k);
  }
  check(boundary.size===243,'LOSS8 S10 boundary changed');
  const selected=new Set(cert.s8_loss_s10_leaves);
  check(selected.size===15&&Array.isArray(cert.s8_loss_s10_leaves)&&
    cert.s8_loss_s10_leaves.length===15&&
    [...selected].every(h=>boundary.has(h)),'invalid LOSS leaf selection');
  check([...covers.values()].every(s=>[...s].some(h=>selected.has(h))),
    'uncovered LOSS8 obligation');
  const weights=cert.s8_loss_dual_weights_halves;
  check(Array.isArray(weights)&&weights.length===26&&
    weights.every(x=>Number.isInteger(x)&&x>=0)&&
    weights.reduce((a,b)=>a+b,0)===30,'invalid dual lower bound');
  const parents=reverse([cert.s8_loss_root]);
  check(parents.size===8&&new Set(cert.new_s7_loss_parents).size===8&&
    cert.new_s7_loss_parents.every(h=>parents.has(h)),'LOSS7 parents mismatch');
  let states=0,lossCandidates=0,winCandidates=0;
  if(terminal){
    const all=new Set([...win10,...boundary]),verdict=new Map();
    check(all.size===580,'S10 verification union changed');
    for(const h of all){
      const result=solve10(h);states+=result.states;verdict.set(h,result.win);
    }
    check([...win10].every(h=>verdict.get(h)),'false S10 WIN leaf');
    check([...selected].every(h=>!verdict.get(h)),'false S10 LOSS leaf');
    for(const h of boundary){
      if(verdict.get(h)){winCandidates++;continue;}
      lossCandidates++;
      const weight=stored.reduce((s,o,i)=>s+(covers.get(o).has(h)?weights[i]:0),0);
      check(weight<=2,'dual violated by legal LOSS boundary '+h);
    }
    check(lossCandidates===43&&winCandidates===200&&states===53256,
      'terminal verification regression');
  }
  return {win8:win8.size,loss8:1,win9Witnesses:s9.size,win10Leaves:win10.size,
    loss9Obligations:obligations.size,loss10Boundary:boundary.size,
    loss10Selected:selected.size,loss10Candidates:terminal?lossCandidates:null,
    dualMinimumLeaves:15,loss7Parents:parents.size,
    terminalStates:terminal?states:null,terminalVerified:terminal?580:0,
    win8Keys:[...win8],loss8Key:cert.s8_loss_root,emptyBoard:'UNKNOWN'};
}
module.exports={verify,solve10,board,pts,key,canonical,circle,safe,legal,children,reverse};
if(require.main===module){
  const cert=JSON.parse(fs.readFileSync(path.join(__dirname,'gap6-terminal-cert.json'),'utf8'));
  console.log(JSON.stringify(verify(cert),null,2));
  if(process.env.NEGATIVE==='1'){
    const bad=[
      c=>c.s8_win_roots[0].s10_win_children.pop(),
      c=>c.s8_win_roots[0].s9_witness=c.s8_win_roots[0].root,
      c=>c.s8_loss_s10_leaves.pop(),
      c=>c.s8_loss_dual_weights_halves[0]++
    ];
    for(const mutate of bad){
      const c=structuredClone(cert);mutate(c);let rejected=false;
      try{verify(c,{terminal:false});}catch(_){rejected=true;}
      check(rejected,'mutated certificate accepted');
    }
    console.error('PASS four mutation rejections');
  }
}
