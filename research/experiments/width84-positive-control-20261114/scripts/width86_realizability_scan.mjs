// width86_realizability_scan.mjs — 2026-11-14 高速レーン（w=86 正制御・実在性スキャン）
// 目的: (1) w86 掃引で生残した10パターンの REST16 再検査, (2) 11050円10窓の直接検証,
// (3) R'<=1e6 にわたる孤立性スキャン（realizer が 5525 のみであることの数値的裏付け）。
// 注意（w84/w85版からの修正）: 旧 check は窓先頭行 = L 自身を仮定しており、pattern[0]>0 の窓
// （窓開始 x が円の行でないアラインメント）を数え落とす under-approximation だった。
// 本版は窓開始 A = k0 - 2*pat[0] を全キーから試す修正 check を使用し、w84/w85 の
// 生残パターンも同じ窓で再スキャンした（結果は rescan84/85 セクション）。
const PATS86 = {
  p126:  [0,4,5,8,11,18,22,27,29,41,49,54,62,74,76,81,85],
  p169:  [0,4,9,11,23,31,36,44,56,58,63,67,74,77,80,81,85],
  p456:  [0,5,7,19,27,32,40,52,54,59,63,70,73,76,77,81,82],
  p1376: [3,8,10,22,30,35,43,55,57,62,66,73,76,79,80,84,85],
  p1909: [1,6,8,20,28,33,41,53,55,60,64,71,74,77,78,82,83],
  p2612: [1,2,6,7,10,13,20,24,29,31,43,51,56,64,76,78,83],
  p2696: [2,3,7,8,11,14,21,25,30,32,44,52,57,65,77,79,84],
  p3052: [2,7,9,21,29,34,42,54,56,61,65,72,75,78,79,83,84],
  p3119: [0,1,5,6,9,12,19,23,28,30,42,50,55,63,75,77,82],
  p3249: [3,4,8,9,12,15,22,26,31,33,45,53,58,66,78,80,85],
};
const WIN86 = { p126:[1,86], p169:[19,104], p456:[23,108], p1376:[20,105], p1909:[22,107], p2612:[-1,84], p2696:[-2,83], p3052:[21,106], p3119:[0,85], p3249:[-3,82] };
const PATS84 = { p456: PATS86.p456, p1909: PATS86.p1909, p2612: PATS86.p2612, p3119: PATS86.p3119 };
const PATS85 = { p456: PATS86.p456, p1909: PATS86.p1909, p2612: PATS86.p2612, p2696: PATS86.p2696, p3052: PATS86.p3052, p3119: PATS86.p3119 };
const REST16 = [19, 23, 7, 5, 27, 43, 47, 13, 17, 8, 16, 25, 29, 31, 37, 41];
const qrC = {};
const getQR = (m) => { if (!qrC[m]) { const s = new Uint8Array(m); for (let x = 0; x < m; x++) s[(x * x) % m] = 1; qrC[m] = s; } return qrC[m]; };
function rowMaskFor(m, i) {
  const qr = getQR(m); const s = new Set(); const ii4 = (4 * i * i) % m;
  for (let a = 0; a < m; a++) { const am = a - ii4; for (let u = 0; u < m; u++) { let t = (am - u * i) % m; if (t < 0) t += m; if (qr[t]) s.add(a * m + u); } }
  return s;
}
function rest16Check(pat) {
  const per = {}; let allPass = true;
  for (const m of REST16) {
    const masks = pat.map(i => rowMaskFor(m, i));
    let cnt = 0;
    for (const b of masks[0]) { let ok = true; for (let k = 1; k < masks.length; k++) if (!masks[k].has(b)) { ok = false; break; } if (ok) cnt++; }
    per[m] = cnt; if (cnt === 0) allPass = false;
  }
  return { allPass, perModulus: per };
}
function witnessCheck(windowX, pat) {
  const pts = [];
  for (let x = -15; x <= 120; x++) for (let y = -15; y <= 120; y++)
    if ((2 * x - 105) ** 2 + (2 * y - 105) ** 2 === 11050) pts.push([x, y]);
  const inW = pts.filter(p => p[0] >= windowX[0] && p[0] <= windowX[1]);
  const rows = [...new Set(inW.map(p => p[0] - windowX[0]))].sort((a, b) => a - b);
  return { points: inW.length, nRows: rows.length, equalsPattern: JSON.stringify(rows) === JSON.stringify(pat) };
}
function reprPrime(p){for(let a=Math.floor(Math.sqrt(p/2));a>=1;a--){const b2=p-a*a,b=Math.round(Math.sqrt(b2));if(b*b===p-a*a)return[Math.max(a,b),Math.min(a,b)];}throw new Error('no rep '+p);}
function repsOf(pf){
  const factors=[];
  for(const [p,e] of pf){const [a,b]=reprPrime(p);const opts=[];
    for(let j=0;j<=e;j++){let re=1,im=0;for(let t=0;t<j;t++){const nr=re*a-im*b,ni=re*b+im*a;re=nr;im=ni;}for(let t=0;t<e-j;t++){const nr=re*a+im*b,ni=-re*b+im*a;re=nr;im=ni;}opts.push({re,im});}
    factors.push(opts);}
  const out=new Set();
  (function rec(i,re,im){if(i===factors.length){const X=Math.abs(re),Y=Math.abs(im);out.add(Math.max(X,Y)+','+Math.min(X,Y));return;}for(const f of factors[i])rec(i+1,re*f.re-im*f.im,re*f.im+im*f.re);})(0,1,0);
  return [...out].map(s=>{const[a,b]=s.split(',').map(Number);return[a,b];});
}
function rowsFor(qr){
  const mk=()=>new Map();const oo=mk(),it=mk(),mx=mk();const add=(m,k,v)=>m.set(k,(m.get(k)||0)+v);
  for(const [X,Y] of qr){
    if(Y===0){add(oo,X,2);add(oo,-X,2);add(it,0,2);add(mx,0,2);continue;}
    add(oo,X+Y,2);add(oo,-(X+Y),2);add(oo,X-Y,2);add(oo,-(X-Y),2);
    add(it,Y*2,2);add(it,-Y*2,2);add(it,X*2,2);add(it,-X*2,2);
    const ev=(X%2===0)?X:Y;add(mx,ev,2);add(mx,-ev,2);
  }
  return [oo,it,mx];
}
// 修正版check: 窓開始 A を候補キーから逆算して全試行（旧版の数え落としを修正）
function checkFixed(m,pats,rowMax){
  const keys=[...m.keys()].sort((a,b)=>a-b);const kset=new Set(keys);
  const hits=[];
  for(const [name,P] of Object.entries(pats)){
    for(const k0 of keys){
      const A=k0-2*P[0];
      let cnt=0;
      for(let x=A;x<=A+2*rowMax;x+=2){if(kset.has(x))cnt++;}
      if(cnt!==P.length)continue;
      let ok=true;for(let i=0;i<P.length;i++){if(!kset.has(A+2*P[i])){ok=false;break;}}
      if(ok)hits.push({name,A,pts:P.reduce((s,p)=>s+(m.get(A+2*p)||0),0)});
    }
  }
  return hits;
}
function test(R,pf,tag,pats,rowMax,results){
  const qr=repsOf(pf);const forms=rowsFor(qr);const names=['oo','it','mx'];
  for(let f=0;f<3;f++){for(const h of checkFixed(forms[f],pats,rowMax))results.push({R,tag,form:names[f],...h});}
}
function runScan(width,pats){
  const rowMax=width-1;const results=[];
  test(5525,[[5,2],[13,1],[17,1]],'control-11050',pats,rowMax,results);
  const ps=[];const LIMIT=1000;const isC=new Uint8Array(LIMIT+1);
  for(let n=3;n<=LIMIT;n+=2)if(!isC[n]){for(let m2=n*n;m2<=LIMIT;m2+=n)isC[m2]=1;if(n%4===1)ps.push(n);}
  let cnt=0;
  (function dfs(i,prod,pe,pf){
    if(pe>=9){test(prod,pf,'scan',pats,rowMax,results);cnt++;}
    for(let j=i;j<ps.length;j++){const p=ps[j];if(prod*p>1e6)break;
      let q=prod*p;let e=1;
      while(q<=1e6){const npf=pf.slice();npf.push([p,e]);dfs(j+1,q,pe*(e+1),npf.slice());q*=p;e++;}
    }
  })(0,1,1,[]);
  return {processed:cnt,results};
}
const rest16 = {}; for (const k of Object.keys(PATS86)) rest16[k] = rest16Check(PATS86[k]);
const witness = {}; for (const k of Object.keys(PATS86)) witness[k] = witnessCheck(WIN86[k], PATS86[k]);
const scan86 = runScan(86, PATS86);
const rescan84 = runScan(84, PATS84);
const rescan85 = runScan(85, PATS85);
console.log(JSON.stringify({ w: 86, rest16, witness, scan1e6: scan86, rescanFixedCheck: { note: 'w84/w85 パターンの修正check再スキャン（旧width84/85_realizability_scan.mjsのcheckは窓アラインメントの数え落としがあった）', w84: rescan84, w85: rescan85 } }, null, 1));
