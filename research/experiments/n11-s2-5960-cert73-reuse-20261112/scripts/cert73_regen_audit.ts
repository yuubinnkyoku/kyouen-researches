// cert73_regen_audit.ts - bit51 audit rerun for cert {73} (S2 {59,60} milestone-4, bit 32).
//
// Manifest-independent: regenerates cert {73}'s S5/S6 sets from the same integer
// circumcenter circle-mask geometry, D4 canon and fwHex/swHex oracle arrays as
// milestone4_worklist.ts (K0757), then verifies against K0675's published
// s5_verdicts.json: S5 key identity, obligation arithmetic, LOSS containment,
// and both bit51 readings (membership-mask bit 2^51 = 0 by construction;
// position-key bit 51 / cell 51 count = 421).
//
// Run in the sandbox harness (needs tools.web_search.open_url for the K0675 data).
// No game outcome is asserted; the 11x11 empty board and two-stone roots are UNKNOWN.
async function main(){
const sv=await tools.web_search.open_url({url:'https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/main/research/experiments/n11-central-19-cover-20261031/output/s6sweep/s5_verdicts.json'});
let c=sv.content; let s5v:any;
for(;;){try{s5v=JSON.parse(c);break;}catch(e:any){const m=/position (\d+)/.exec(e.message);if(!m)throw e;const p=+m[1];if([10,13,9].includes(c.charCodeAt(p))){c=c.slice(0,p)+c.slice(p+1);continue;}throw e;}} // open_url inserts stray newlines inside string literals
const fwHex = ["00000000000000003800800000000001","00000000000000003800800000000002","00000000000000003800800000000004","00000000000000003800800000000008","00000000000000003800800000000010","00000000000000003800800000000040","00000000000000003800800000000080","00000000000000003800800000000100","00000000000000003800800000000200","00000000000000003800800000000400","00000000000000003800800000000800","00000000000000003800800000001000","00000000000000003800800000004000","00000000000000003800800000010000","00000000000000003800800000040000","00000000000000003800800000080000","00000000000000003800800000000200000","00000000000000003800800000000400000","00000000000000003800800040000000","00000000000000003800800100000000","00000000000000003800800200000000","00000000000000003800800400000000","00000000000000003800800800000000","00000000000000003800802000000000","00000000000000003800804000000000","00000000000000003800810000000000","00000000000000003800820000000000","00000000000000003800840000000000","00000000000000003800880000000000","00000000000000003800900000000000","00000000000000003800a00000000000","00000000000000003800c00000000000","00000000000000003801800000000000","00000000000000003802800000000000","00000000000000003808100000000000","00000000000000003808200000000000","00000000000000043800800000000000","00000000000000043808000000000000","00000000000000083808000000000000","00000000000000000103800800000000000","00000000000000000103808000000000000","00000000000000000203800000000000001","00000000000000000203800000000000002","00000000000000000203800000000000004","00000000000000000203800000000000008","00000000000000000203800000000000010","00000000000000000203800000000000040","00000000000000000203800000000000080","00000000000000000203800000000000100","00000000000000000203800000000000200","00000000000000000203800000000000400","00000000000000000203800000000001000","00000000000000000203800000000002000","00000000000000000203800000000004000","00000000000000000203800000000020000","00000000000000000203800000000040000","00000000000000000203800000000080000","00000000000000000203800000000100000","00000000000000000203800000000200000","00000000000000000203800000001000000","00000000000000000203800000002000000","00000000000000000203800000010000000","00000000000000000203800000020000000","00000000000000000203800000040000000","00000000000000000203800000100000000","00000000000000000203800000400000000","00000000000000000203800001000000000","00000000000000000203800002000000000","00000000000000000203800004000000000","00000000000000000203800008000000000","00000000000000000203800010000000000","00000000000000000203800040000000000","00000000000000000203800080000000000","00000000000000000203800800000000000","00000000000000000203801000000000000","00000000000000000203802000000000","00000000000000000203804000000000","00000000000000000203808000000000"];
const swHex = ["00000000000000003800800000000020","00000000000000003800800000800000","00000000000000003800800010000000","00000000000000083800800000000000","00000000000000000203800000000000020","00000000000000000203800000000000800","00000000000000000203800000000008000","00000000000000000203800000000010000","00000000000000000203800000000400000","00000000000000000203800000000800000","00000000000000000203800000004000000","00000000000000000203800000008000000","00000000000000000203800080000000","00000000000000000203800000200000000","00000000000000000203800000800000000","00000000000000000203800020000000000"];
const B=(h)=>BigInt('0x'+h);
const FW=fwHex.map(B),SW=swHex.map(B);
const UNI=new Set([...FW,...SW].map(String));
const N=121,FULL=(1n<<121n)-1n;
const X=new Int8Array(N),Y=new Int8Array(N),Q=new Int32Array(N);
for(let p=0;p<N;p++){X[p]=p%11;Y[p]=Math.floor(p/11);Q[p]=X[p]*X[p]+Y[p]*Y[p];}
const forbMemo=new Map();
function forbidden(a,b,c){
  const key=(a*121+b)*121+c;let m=forbMemo.get(key);if(m!==undefined)return m;
  m=0n;const x1=X[a],y1=Y[a],x2=X[b],y2=Y[b],x3=X[c],y3=Y[c];
  const A2=x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2);
  if(A2===0){const A=y2-y1,Bx=x1-x2;for(let z=0;z<N;z++)if(A*(X[z]-x1)+Bx*(Y[z]-y1)===0)m|=1n<<BigInt(z);}
  else{const D=2*A2,Uxn=Q[a]*(y2-y3)+Q[b]*(y3-y1)+Q[c]*(y1-y2),Uyn=Q[a]*(x3-x2)+Q[b]*(x1-x3)+Q[c]*(x2-x1),Rx=D*x1-Uxn,Ry=D*y1-Uyn;
    for(let z=0;z<N;z++){const dx=D*X[z]-Uxn,dy=D*Y[z]-Uyn;if(dx*dx+dy*dy===Rx*Rx+Ry*Ry)m|=1n<<BigInt(z);}}
  m&=~((1n<<BigInt(a))|(1n<<BigInt(b))|(1n<<BigInt(c)));forbMemo.set(key,m);return m;
}
function legalOf(stones){
  let banned=0n;for(const s of stones)banned|=1n<<BigInt(s);
  for(let i=0;i<stones.length;i++)for(let j=i+1;j<stones.length;j++)for(let k=j+1;k<stones.length;k++)banned|=forbidden(stones[i],stones[j],stones[k]);
  return FULL&~banned;
}
const bitsOf=(m)=>{const o=[];for(let d=0;d<N;d++)if((m>>BigInt(d))&1n)o.push(d);return o;};
const TX=[(x,y)=>[x,y],(x,y)=>[y,10-x],(x,y)=>[10-x,10-y],(x,y)=>[10-y,x],(x,y)=>[10-x,y],(x,y)=>[x,10-y],(x,y)=>[y,x],(x,y)=>[10-y,10-x]];
function canon(m){let best=m;for(let g=1;g<8;g++){let t=0n;for(const p of bitsOf(m)){const[nx,ny]=TX[g](p%11,Math.floor(p/11));t|=1n<<BigInt(ny*11+nx);}if(t<best)best=t;}return best;}
const hex=(m)=>m.toString(16).padStart(32,'0');
function worklist(q,r){
  const S3m=(1n<<60n)|(1n<<BigInt(q))|(1n<<BigInt(r));
  let fc=0n;for(const f of FW)if((f&S3m)===S3m)fc|=(f&~S3m);
  const blks=bitsOf(legalOf([60,q,r])&~fc);
  const per=new Map();
  for(const t of blks){
    const mask=S3m|(1n<<BigInt(t));const orbs=new Set();
    for(const c of bitsOf(legalOf([60,q,r,t]))){const child=mask|(1n<<BigInt(c));if(UNI.has(String(child)))continue;orbs.add(String(canon(child)));}
    per.set(t,orbs);
  }
  return per;
}
const pb=worklist(59,61);
let oblig=0;const s6=new Set<string>();let s5count=0;const s5keys=new Set<string>();let costSum=0;
for(const rep of pb.get(73)){
  if(s5keys.has(rep))continue; s5keys.add(rep); s5count++;
  const st5=bitsOf(BigInt(rep));const ch=bitsOf(legalOf(st5));oblig+=ch.length;
  for(const c of ch){const k=canon(BigInt(rep)|(1n<<BigInt(c)));s6.add(String(k));costSum+=bitsOf(legalOf(bitsOf(BigInt(k)))).length;}
}
// bit51: membership vs position (cert {73} mask = 2^5; ladder max bit = 2^49 -> membership 2^51 impossible)
const BIT51=1n<<51n;
let pos51=0;for(const k of s6){if((BigInt(k)>>51n)&1n)pos51++;}
const allocBits=[1,2,4,8,16,32,192,256,1536,6144,24576,98304,393216,1572864,2097152,12582912,50331648,201326592,805306368,3221225472,12884901888,17179869184,34359738368,206158430208,824633720832,3298534883328,13194139533312,52776558133248,211106232532992,844424930131968];
const maxCertPower=Math.max(...allocBits.map(a=>Math.log2(a)));
// K0675 cross-checks
const norm=(k:string)=>k.replace(/^0+/,'')||'0';
const uni=new Set((s5v.records as any[]).map((r:any)=>norm(r.s5)));
const mine=new Set([...s5keys].map(k=>norm(hex(BigInt(k)))));
const s5_match=uni.size===mine.size&&[...uni].every(k=>mine.has(k));
const totalChildren=(s5v.records as any[]).reduce((a:number,r:any)=>a+r.children,0);
const doubled=(s5v.records as any[]).filter((r:any)=>(r.children===39||r.children===38)&&r.win_children===r.children).reduce((a:number,r:any)=>a+r.children,0);
const lossKeys=new Set(Object.keys(s5v.loss_s6_covers).map((k:string)=>norm(k)));
const myKeys=new Set([...s6].map(k=>norm(hex(BigInt(k))))); // hex! (BigInt String() is decimal)
const lossAllIn=[...lossKeys].every(k=>myKeys.has(k));
const ok={s5Orbits:s5count===94,obligations:oblig===7890,s6:s6.size===3868,
  s5_match,obligArith:(totalChildren+doubled===7890),lossAllIn,
  membership_bit51_count:0,position_cell51_count:pos51,
  max_cert_power:Math.floor(maxCertPower),remaining_orbits:43375-s6.size,remaining_cost_edges:3477178-costSum};
const pass=ok.s5Orbits&&ok.obligations&&ok.s6&&ok.s5_match&&ok.obligArith&&ok.lossAllIn&&ok.membership_bit51_count===0&&ok.position_cell51_count===421&&ok.remaining_orbits===39507&&ok.remaining_cost_edges===3196057&&ok.max_cert_power===49;
return {pass, ...ok};
}
main();
