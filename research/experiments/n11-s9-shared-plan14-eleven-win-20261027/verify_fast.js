#!/usr/bin/env node
'use strict';
// Fast independent terminal proof: 3x3 determinant (upstream) versus 4x4 Bareiss.
// No verdict cache, pn/dn or incomplete search is used as a terminal leaf.
const fs=require('node:fs'),path=require('node:path');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const cert=JSON.parse(fs.readFileSync(path.join(__dirname,'certificate.json'),'utf8'));
const need=(x,msg)=>{if(!x)throw Error(msg);};
const XY=Array.from({length:121},(_,i)=>[i%11,Math.floor(i/11)]);
function det4(q){
  const m=q.map(i=>{const [x,y]=XY[i];return [x,y,x*x+y*y,1];});
  let sign=1,prev=1;
  for(let k=0;k<3;k++){
    if(!m[k][k]){
      let j=k+1;while(j<4&&!m[j][k])j++;
      if(j===4)return 0;
      [m[k],m[j]]=[m[j],m[k]];sign=-sign;
    }
    const pivot=m[k][k];
    for(let i=k+1;i<4;i++)for(let j=k+1;j<4;j++){
      const v=m[i][j]*pivot-m[i][k]*m[k][j];
      need(v%prev===0,'non-exact Bareiss division');
      m[i][j]=v/prev;
    }
    for(let i=k+1;i<4;i++)m[i][k]=0;
    prev=pivot;
  }
  return sign*m[3][3];
}
function legal4(b){
  const pp=g.pts(b),tri=[],moves=[];
  for(let i=0;i<pp.length;i++)for(let j=i+1;j<pp.length;j++)
    for(let k=j+1;k<pp.length;k++)tri.push([pp[i],pp[j],pp[k]]);
  for(let p=0;p<121;p++){
    if((b>>BigInt(p))&1n)continue;
    if(!tri.some(t=>det4([...t,p])===0))moves.push(p);
  }
  return moves;
}
function children4(h){
  const b=BigInt('0x'+h);
  return new Set(legal4(b).map(p=>g.key(g.canonical(b|(1n<<BigInt(p))))));
}
function solve4(h){
  const b=g.board(h,10),pp=g.pts(b),moves=legal4(b);
  need(moves.length<=30,'terminal bitmask overflow');
  const bad=[];
  for(let i=0;i<moves.length;i++)for(let j=i+1;j<moves.length;j++){
    let forbidden=false;
    for(let a=0;a<pp.length&&!forbidden;a++)for(let c=a+1;c<pp.length;c++){
      if(det4([pp[a],pp[c],moves[i],moves[j]])===0){
        forbidden=true;break;
      }
    }
    if(forbidden)bad.push((1<<i)|(1<<j));
  }
  const hasSub=x=>bad.some(y=>(x&y)===y);
  for(let i=0;i<moves.length;i++)for(let j=i+1;j<moves.length;j++)
    for(let k=j+1;k<moves.length;k++){
      const mask=(1<<i)|(1<<j)|(1<<k);
      if(!hasSub(mask)&&pp.some(a=>det4([a,moves[i],moves[j],moves[k]])===0))
        bad.push(mask);
    }
  for(let i=0;i<moves.length;i++)for(let j=i+1;j<moves.length;j++)
    for(let k=j+1;k<moves.length;k++)for(let l=k+1;l<moves.length;l++){
      const mask=(1<<i)|(1<<j)|(1<<k)|(1<<l);
      if(!hasSub(mask)&&det4([moves[i],moves[j],moves[k],moves[l]])===0)
        bad.push(mask);
    }
  const bans=Array.from({length:moves.length},()=>[]);
  for(const mask of bad)for(let i=0;i<moves.length;i++)
    if(mask&(1<<i))bans[i].push(mask^(1<<i));
  const memo=new Map();
  function win(state){
    if(memo.has(state))return memo.get(state);
    for(let i=0;i<moves.length;i++){
      const bit=1<<i;
      if(state&bit||bans[i].some(v=>(state&v)===v))continue;
      if(!win(state|bit)){memo.set(state,true);return true;}
    }
    memo.set(state,false);return false;
  }
  return {win:win(0),states:memo.size,legal:moves.length};
}
const same=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
function structure(c){
  need(c.format==='n11-s9-shared-plan14-eleven-win-v1'&&c.board===11&&
    c.perspective==='original-first-player'&&c.empty_board==='UNKNOWN',
    'invalid certificate header');
  need(Array.isArray(c.witnesses)&&c.witnesses.length===11,'wrong root count');
  const plan=fs.readFileSync(path.join(__dirname,
    '../n11-s5-pair-cover-20261026/s7-plan14-remaining.keys'),'ascii')
    .trim().split(/\s+/);
  need(plan.length===14,'plan changed');
  const plan8=new Set(plan.flatMap(h=>[...g.children(BigInt('0x'+h))]));
  const union8=new Set(),touched=new Set(),rootKeys=new Set();
  let leaves=0,claimedStates=0;
  for(const row of c.witnesses){
    const b=g.board(row.s9_win,9);
    need(!rootKeys.has(row.s9_win),'duplicate S9 root');
    rootKeys.add(row.s9_win);
    const children=g.children(b),listed=new Set(row.s10_win_children);
    need(Array.isArray(row.s10_win_children)&&
      listed.size===row.s10_win_children.length&&same(children,listed),
      'incomplete universal S10 boundary');
    const all=g.reverse([row.s9_win]),stored=new Set(row.s8_all_parents);
    const selected=new Set(row.s8_plan_parents);
    need(all.size===9&&stored.size===9&&same(all,stored),
      'incomplete reverse S8 parents');
    need(selected.size>=3&&selected.size<=4&&
      same(selected,new Set([...all].filter(h=>plan8.has(h)))),
      'incorrect plan-parent boundary');
    for(const h of all){
      need(g.children(BigInt('0x'+h)).has(row.s9_win),
        'invalid S8->S9 witness');
      union8.add(h);
      if(plan8.has(h))touched.add(h);
    }
    need(Number.isInteger(row.terminal_states)&&row.terminal_states>0,
      'invalid terminal-state field');
    leaves+=children.size;claimedStates+=row.terminal_states;
  }
  need(leaves===225&&claimedStates===24952&&union8.size===96&&
    touched.size===38,'certificate union regression');
  return {leaves,claimedStates,union8,touched};
}
function verify(c,negative=false){
  const manifest=structure(c);
  let leaves=0,states=0;
  for(const row of c.witnesses){
    const independent=children4(row.s9_win);
    need(same(independent,new Set(row.s10_win_children)),
      '3x3 vs independent 4x4 S9 children differ');
    for(const h of row.s8_all_parents){
      need(children4(h).has(row.s9_win),
        'independent 4x4 S8->S9 incidence differs');
    }
    let subtotal=0;
    for(const h of row.s10_win_children){
      const a=g.solve10(h),b=solve4(h);
      need(a.win&&b.win,'false S10 WIN terminal leaf: '+h);
      need(a.states===b.states&&a.legal===b.legal,
        'independent terminal disagreement: '+h);
      subtotal+=a.states;leaves++;
    }
    need(subtotal===row.terminal_states,
      'terminal state count differs: '+row.s9_win);
    states+=subtotal;
  }
  need(leaves===225&&states===24952,'total terminal state regression');
  if(negative){
    const reject=mutate=>{
      const altered=structuredClone(c);mutate(altered);
      let rejected=false;
      try{structure(altered);}catch(_){rejected=true;}
      need(rejected,'modified manifest accepted');
    };
    reject(x=>x.witnesses[0].s10_win_children.pop());
    reject(x=>x.witnesses[0].s8_plan_parents.pop());
    reject(x=>x.witnesses[0].terminal_states=0);
    reject(x=>x.witnesses[0].s9_win=x.witnesses[1].s9_win);
    reject(x=>x.empty_board='WIN');
  }
  return {independentGeometries:2,s9WinWitnesses:c.witnesses.length,
    s10WinLeaves:leaves,terminalStatesPerGeometry:states,
    derivedS8Win:manifest.union8.size,planS8Touched:manifest.touched.size,
    newS7Verdicts:0,newS5Verdicts:0,emptyBoard:'UNKNOWN'};
}
if(require.main===module)console.log(JSON.stringify(verify(cert,process.argv.includes('--negative'))));
module.exports={verify,solve4,det4,legal4,children4};
