// class_sat.js — class-split deficiency encoding for the 5x20 cross-check (controls: 5x18/5x19).
// Uses K0810 sat.js verbatim census (circleABC integer triples) + sequential >=-counter (copied from K0810 encode).
// Class D (nonempty subset of rows): rows in D have <= q-2 stones (assert NOT >=q-1),
// rows not in D have exactly q-1 stones (assert >= q-1; safety already caps at q-1).
// Safety (<= q-1 per curve), maximality (empty cell -> some curve through it has >= q-1) as in K0810.
// No total counter: with |D|>=1, total <= w(q-1)-1 is implied.
// Optional k (argv[7]): fix the stone count of the first deficient row Y0=D[0] to exactly k (>=k and NOT >=k+1).
// Optional minpos (argv[8]): sound column-mirror symmetry break - the leftmost stone of row Y0 is at column
//   minpos (cells left of it forced empty, cell at minpos forced stone). Any config mirrors to one with minpos in 0..floor((m-1)/2),
//   so enumerating minpos=0..9 covers class [1] k=5 completely.
'use strict';
const S = require('./sat.js');
class Enc { constructor(){this.nv=0;this.clauses=[];} v(){return ++this.nv;} add(cls){for(let c of cls){c=c.filter(l=>l!==0);if(c.length)this.clauses.push(c);}} }
function counter(enc, xs, K){ const nE=xs.length; const s=Array.from({length:nE},()=>new Array(K+1).fill(0));
  for(let i=0;i<nE;i++)for(let j=1;j<=Math.min(K,i+1);j++)s[i][j]=enc.v();
  for(let i=0;i<nE;i++)for(let j=1;j<=Math.min(K,i+1);j++){const S2=s[i][j];
    if(i===0){enc.add([[xs[0],-S2]]);enc.add([[-xs[0],S2]]);}
    else{const Sp=(j<=i)?s[i-1][j]:0;const Spp=(j>=2&&j-1<=i)?s[i-1][j-1]:0;
      if(j<=i){enc.add([[-S2,Sp,xs[i]]]);if(Spp)enc.add([[-S2,Sp,Spp]]);enc.add([[-Sp,S2]]);if(Spp)enc.add([[-xs[i],-Spp,S2]]);else enc.add([[-xs[i],S2]]);}
      else{enc.add([[-S2,xs[i]]]);enc.add([[-S2,Spp]]);enc.add([[-xs[i],-Spp,S2]]);}}}
  return s; }
function encodeClass(w,m,q,D,k,minpos){
  const {P,n,curves}=S.buildCensus(w,m,q);
  const enc=new Enc(); const cell=new Array(n).fill(0).map(()=>enc.v()); const geVars=[]; const rowCounters={};
  for(const cu of curves){const xs=cu.pts.map(p=>cell[p]);const s=counter(enc,xs,q);enc.add([[-s[cu.pts.length-1][q]]]);geVars.push(s[cu.pts.length-1][q-1]);
    if(cu.type==='line'&&cu.co[0]===0&&cu.co[1]===1){rowCounters[-cu.co[2]]=s[cu.pts.length-1];}}
  const through=Array.from({length:n},()=>[]);
  curves.forEach((cu,ci)=>{for(const p of cu.pts)through[p].push(geVars[ci]);});
  for(let i=0;i<n;i++)enc.add([[cell[i],...through[i]]]);
  const rowGe=[];curves.forEach((cu,ci)=>{if(cu.type==='line'&&cu.co[0]===0&&cu.co[1]===1)rowGe.push(geVars[ci]);});
  if(rowGe.length!==w)throw new Error('row curves miscount '+rowGe.length);
  const Dset=new Set(D);
  for(let r=0;r<w;r++){ if(Dset.has(r)) enc.add([[-rowGe[r]]]); else enc.add([[rowGe[r]]]); }
  if(k!==null&&k!==undefined){const Y0=D[0];const sc=rowCounters[Y0];
    if(k>=1) enc.add([[sc[k]]]);
    enc.add([[-sc[k+1]]]); }
  if(minpos!==null&&minpos!==undefined){const Y0=D[0];enc.add([[cell[minpos+m*Y0]]]);for(let x=0;x<minpos;x++)enc.add([[-cell[x+m*Y0]]]);}
  return {enc,cell,P,curves,n};
}
const [w,m,q]=process.argv.slice(2,5).map(Number);
const D=JSON.parse(process.argv[5]); const out=process.argv[6];
const k=process.argv[7]!==undefined?+process.argv[7]:null;
const minpos=process.argv[8]!==undefined?+process.argv[8]:null;
const t0=Date.now();
const {enc,cell,P,curves,n}=encodeClass(w,m,q,D,k,minpos);
require('fs').writeFileSync(out,S.toDimacs(enc));
console.log(JSON.stringify({w,m,q,defRows:D,k,minpos,vars:enc.nv,clauses:enc.clauses.length,curves:curves.length,n,ms:Date.now()-t0}));
