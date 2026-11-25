// model_verify.js — decode a kissat SAT model of a class instance and verify with sat.js census-free verifier.
'use strict';
const S=require('./sat.js');
const [w,m,q]=process.argv.slice(2,5).map(Number);
const D=JSON.parse(process.argv[5]); const modelf=process.argv[6];
const {P,n,curves}=S.buildCensus(w,m,q);
class Enc{constructor(){this.nv=0;this.clauses=[];}v(){return ++this.nv;}add(cls){for(let c of cls){c=c.filter(l=>l!==0);if(c.length)this.clauses.push(c);}}}
const counter=null; // class_sat.js must NOT be required here: it executes on load and would clobber files
function counterF(enc,xs,K){ const nE=xs.length; const s=Array.from({length:nE},()=>new Array(K+1).fill(0));
  for(let i=0;i<nE;i++)for(let j=1;j<=Math.min(K,i+1);j++)s[i][j]=enc.v();
  for(let i=0;i<nE;i++)for(let j=1;j<=Math.min(K,i+1);j++){const S2=s[i][j];
    if(i===0){enc.add([[xs[0],-S2]]);enc.add([[-xs[0],S2]]);}
    else{const Sp=(j<=i)?s[i-1][j]:0;const Spp=(j>=2&&j-1<=i)?s[i-1][j-1]:0;
      if(j<=i){enc.add([[-S2,Sp,xs[i]]]);if(Spp)enc.add([[-S2,Sp,Spp]]);enc.add([[-Sp,S2]]);if(Spp)enc.add([[-xs[i],-Spp,S2]]);else enc.add([[-xs[i],S2]]);}
      else{enc.add([[-S2,xs[i]]]);enc.add([[-S2,Spp]]);enc.add([[-xs[i],-Spp,S2]]);}}}
  return s; }
const lines=require('fs').readFileSync(modelf,'utf8').split('\n');
const pos=new Set(); for(const L of lines){if(L[0]==='v'){for(const t of L.slice(2).trim().split(/\s+/)){const v=parseInt(t);if(v>0)pos.add(v);}}}
const enc=new Enc();const cell=new Array(n).fill(0).map(()=>enc.v());const geVars=[];const rowCounters={};
for(const cu of curves){const xs=cu.pts.map(p=>cell[p]);const s=counterF(enc,xs,q);enc.add([[-s[cu.pts.length-1][q]]]);geVars.push(s[cu.pts.length-1][q-1]);
  if(cu.type==='line'&&cu.co[0]===0&&cu.co[1]===1){rowCounters[-cu.co[2]]=s[cu.pts.length-1];}}
const through=Array.from({length:n},()=>[]);
curves.forEach((cu,ci)=>{for(const p of cu.pts)through[p].push(geVars[ci]);});
for(let i=0;i<n;i++)enc.add([[cell[i],...through[i]]]);
const rowGe=[];curves.forEach((cu,ci)=>{if(cu.type==='line'&&cu.co[0]===0&&cu.co[1]===1)rowGe.push(geVars[ci]);});
const Dset=new Set(D);
for(let r=0;r<w;r++){ if(Dset.has(r)) enc.add([[-rowGe[r]]]); else enc.add([[rowGe[r]]]); }
const stones=[];const rowCnt=new Array(w).fill(0);
for(let i=0;i<n;i++)if(pos.has(cell[i])){stones.push(P[i]);rowCnt[P[i][1]]++;}
const v=S.verifyConfig(w,m,q,stones);
console.log(JSON.stringify({w,m,q,defRows:D,stones:stones.length,rowCounts:rowCnt,ok:v.ok,verify:v}));
