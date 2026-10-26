#!/usr/bin/env node
'use strict';
// Conditional S5 proof plan. The selected S7 roots are NOT asserted WIN.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const g=require('../n11-gap6-terminal-20261019/verify_js.js');
const FROZEN=path.join(__dirname,'../n11-targeted-terminal-lift-20261015/data/all_s7_win_17.txt');
const FROZEN_SHA='17282f84fd65ad20ac58ef794449a52bcc796d8129a1a3a58d726a305fbeb21e';
const ROOT='00000000000000821080000000000020';
const NEW7='00000000000100001000000042401008';
const check=(v,m)=>{if(!v)throw Error(m);};
const key=b=>b.toString(16).padStart(32,'0');
const children=h=>[...g.children(BigInt('0x'+h))].sort();
const pts=b=>g.pts(b);
function circle4(a,b,c,d){
  const m=[a,b,c,d].map(p=>{const x=p%11,y=Math.floor(p/11);return [x,y,x*x+y*y,1];});
  let sum=0;
  for(let i=0;i<4;i++)for(let j=0;j<4;j++)if(j!==i)
    for(let k=0;k<4;k++)if(k!==i&&k!==j)for(let l=0;l<4;l++)if(l!==i&&l!==j&&l!==k){
      const p=[i,j,k,l];let inv=0;
      for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)if(p[u]>p[v])inv++;
      sum+=(inv%2?-1:1)*m[0][i]*m[1][j]*m[2][k]*m[3][l];
    }
  return sum===0;
}
function independentChildren(h){
  const b=BigInt('0x'+h),a=pts(b),triples=[],occupied=new Set(a);
  for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++)for(let k=j+1;k<a.length;k++)triples.push([a[i],a[j],a[k]]);
  const out=new Set();
  for(let p=0;p<121;p++)if(!occupied.has(p)&&!triples.some(t=>circle4(...t,p)))
    out.add(key(g.canonical(b|(1n<<BigInt(p)))));
  return [...out].sort();
}
function audit(negative=false){
  const raw=fs.readFileSync(FROZEN);
  check(crypto.createHash('sha256').update(raw).digest('hex')===FROZEN_SHA,'frozen S7 source changed');
  const frozen=raw.toString('ascii').trim().split(/\s+/);
  check(frozen.length===17&&frozen.every((x,i)=>/^[0-9a-f]{32}$/.test(x)&&(i===0||frozen[i-1]<x)), 'invalid S7 frozen inventory');
  const roots=frozen.concat([NEW7]);
  for(const h of roots)check(pts(BigInt('0x'+h)).length===7&&key(g.canonical(BigInt('0x'+h)))===h,'invalid S7 WIN source');
  const known6=g.reverse(roots),all6=children(ROOT),missing=all6.filter(h=>!known6.has(h));
  check(known6.size===110&&all6.length===32&&missing.length===27,'S5 baseline changed');
  const byS7=new Map();
  for(let i=0;i<missing.length;i++)for(const h of children(missing[i])){
    if(!byS7.has(h))byS7.set(h,new Set());byS7.get(h).add(i);
  }
  const counts={1:0,2:0},pairs=new Map();
  for(const [h,covered] of byS7){
    check(covered.size===1||covered.size===2,'S7 witness covers more than two S6');
    counts[covered.size]++;
    if(covered.size===2){const id=[...covered].sort((a,b)=>a-b).join(':');
      if(!pairs.has(id))pairs.set(id,[]);pairs.get(id).push(h);}
  }
  check(byS7.size===853&&counts[1]===232&&counts[2]===621&&pairs.size===346,'S7 incidence census changed');
  const adj=Array.from({length:27},()=>[]);
  for(const id of pairs.keys()){const [i,j]=id.split(':').map(Number);adj[i].push(j);adj[j].push(i);}
  adj.forEach(a=>a.sort((a,b)=>a-b));
  const used=new Set(),groups=[];
  for(let i=0;i<27;i++)if(!used.has(i)){
    const j=adj[i].find(j=>!used.has(j));
    if(j!==undefined){used.add(i);used.add(j);groups.push([i,j]);}
  }
  check(groups.length===13,'failed to construct thirteen disjoint pairs');
  groups.push([missing.findIndex((_,i)=>!used.has(i))]);
  const plan=groups.map(ids=>{
    const options=ids.length===2?pairs.get(ids.join(':')):
      [...byS7].filter(([_,s])=>s.has(ids[0])).map(([h])=>h);
    const selected=options.map(h=>({h,children:children(h)}))
      .sort((a,b)=>a.children.length-b.children.length||a.h.localeCompare(b.h))[0];
    return {s7:selected.h,covers:ids.map(i=>missing[i]),legal_s8:selected.children.length};
  });
  function validate(rows){
    const covered=new Set();
    for(const row of rows){
      check(byS7.has(row.s7)&&row.legal_s8===children(row.s7).length,'invalid S7 candidate');
      for(const h of row.covers){
        check(missing.includes(h)&&byS7.get(row.s7).has(missing.indexOf(h)),'illegal S6 witness');
        check(!covered.has(h),'duplicate S6 coverage');covered.add(h);
      }
    }
    check(covered.size===27,'incomplete S6 coverage');
  }
  validate(plan);
  const s8=new Set();
  for(const row of plan)for(const h of children(row.s7))s8.add(h);
  check(plan.length===14&&plan.reduce((s,r)=>s+r.legal_s8,0)===585&&s8.size===584,'plan regression');
  for(const h of [ROOT,...missing,...plan.map(r=>r.s7)])
    check(independentChildren(h).join(',')===children(h).join(','),'4x4 geometry disagrees with 3x3 geometry: '+h);
  if(negative){for(const bad of [plan.slice(1),
    plan.map((r,i)=>i? r:{...r,covers:[...r.covers,ROOT]}),
    plan.map((r,i)=>i? r:{...r,legal_s8:r.legal_s8+1})]){
    let rejected=false;try{validate(bad);}catch(_){rejected=true;}
    check(rejected,'tampered conditional plan accepted');
  }}
  return {schema:'n11-s5-conditional-s7-pair-cover-v1',s5:ROOT,
    legal_s6_classes:32,secured_by_existing_s7_win:5,uncovered_s6_classes:27,
    s7_candidate_classes:853,cover_one:232,cover_two:621,compatible_s6_pairs:346,
    maximum_missing_s6_covered_by_one_s7:2,
    minimum_new_s7_win_certificates_if_s5_is_win:14,
    plan,plan_s7_count:14,plan_s7_to_s8_edges:585,plan_distinct_s8_children:584,
    trust:'Existing 17 S7 WIN roots are a frozen comparison; NEW7 is independently terminal-proved elsewhere. No candidate in plan is proven WIN here.',
    new_s5_verdicts:0,new_two_stone_root_closures:0,empty_board:'UNKNOWN'};
}
if(require.main===module)console.log(JSON.stringify(audit(process.argv.includes('--negative')),null,2));
module.exports={audit};
