// deficient_maximal_machine.ts — 汎用 (w,m,q) 欠損極大安全配置探索機（2026-11-13 高速レーン）
// 目的: M_{w,q} の下界となる「石数 < w(q-1) の極大安全配置」(欠損witness) を貪欲+shakeで発見し、
//       census不使用の独立検証器で safe+maximal を厳密確認する。
//
// 危険曲線: 盤上に q 点以上の格子点を含む全直線・全円（行も一般直線として統一処理）。
//   - 円のcensusは3点組外心の完全列挙（弦対をもたない円も取りこぼさない。q>=5 では必須）。
//   - 円スキャンは行ごとの平方剰余判定（各3点組 O(w)）。接線時 [0,-0] 二重追加を防止。
//   - 外心正規化は (d,ux,uy) を g で割り r^2 は g^2 で割る（g で割ると別円になる — 実装バグ2件目、
//     独立検証器が6x16の非極大witnessで実際に捕捉した）。
//
// 探索: サンプル評価ハイブリッド貪欲（空き点からランダム<=24点を q-2カウント曲線数で評価して最良を置く）
//   + shake（石の1/4を乱数削除して再極大化）を restarts 回反復し最小石数の極大配置を保持。
//   純ランダム版は6x15 q=5の欠損witnessを発見できない（制御済み）— スコア評価が本質。
//
// 検証: verifyIndependent は census不使用。石ペアの直線・石3点組の円を全列挙して
//   safety（最大曲線石数 < q）と maximality（全空点が何らかの q-1石曲線でblock）を厳密整数演算で判定。
//   q>=4 なら block に必要な q-1>=3 石は必ず2石以上を含むためペア/3点組列挙で完全。
//
// 本セッションの主要結果（すべて独立検証 PASS）:
//   q=5, w=6: m=8..19 に欠損witness（m=19 で23石 < 満容量24）→ M_{6,5} >= 20
//   q=6, w=6: m=8..15 に欠損witness（m=15 で29石 < 30）→ M_{6,6} >= 16
//   q=8, w=6: m=9..11 に欠損witness（m=11 で41石 < 42）→ M_{6,8} >= 12
//   (5,6) m=16..18, (5,7) m=19..21 は貪欲では発見できず（非発見は不在の証明ではない）。
//
// 制御（修正census・全PASS）:
//   2x8 q=4 → min 5（K0796 witness を再発見）
//   2x9, 2x12 q=4 → min 6（K0796/K0069 の満容量と一致）
//   5x19 q=7 → min 30（K0759 完全列挙「全極大30石」と一致）
//   K0761 6x19 q=7 witness（35石）・K0796 2x8 witness（5石）が独立検証で safe+maximal PASS
//
// 実行手順: main の RUNS を編集して run_typescript で単独実行。m<=20 程度・restarts<=1000 が
// sandbox 1回の安全圏。census は m=26, w=6, q=5 でも数十ms程度（行ごと平方剰余判定）。
function gcdN(a:number,b:number){a=Math.abs(a);b=Math.abs(b);while(b){const t=a%b;a=b;b=t;}return a||1;}
function isqrt(n:number){if(n<0)return -1;let r=Math.floor(Math.sqrt(n));while(r*r>n)r--;while((r+1)*(r+1)<=n)r++;return r;}
function buildCurves(w:number,m:number,q:number){
  const N=w*m; const px=new Int32Array(N), py=new Int32Array(N);
  for(let y=0;y<w;y++)for(let x=0;x<m;x++){px[x+m*y]=x;py[x+m*y]=y;}
  const lineKeys=new Set<string>();
  for(let i=0;i<N;i++)for(let j=i+1;j<N;j++){
    let dx=px[j]-px[i],dy=py[j]-py[i];
    const g=gcdN(dx,dy);dx/=g;dy/=g;
    if(dy<0||(dy===0&&dx<0)){dx=-dx;dy=-dy;}
    lineKeys.add(`L${dx},${dy},${px[i]*dy-py[i]*dx}`);
  }
  const lines:Int32Array[]=[];
  for(const key of lineKeys){
    const p=key.slice(1).split(',').map(Number);
    const dx=p[0],dyy=p[1],c=p[2];
    const pts:number[]=[];
    for(let i=0;i<N;i++){if(px[i]*dyy-py[i]*dx===c)pts.push(i);}
    if(pts.length>=q)lines.push(Int32Array.from(pts));
  }
  const keptC=new Map<string,Int32Array>();
  for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)for(let k=j+1;k<N;k++){
    const x1=px[i],y1=py[i],x2=px[j],y2=py[j],x3=px[k],y3=py[k];
    const d=2*(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2));if(d===0)continue;
    const s1=x1*x1+y1*y1,s2=x2*x2+y2*y2,s3=x3*x3+y3*y3;
    const ux=s1*(y2-y3)+s2*(y3-y1)+s3*(y1-y2), uy=s1*(x3-x2)+s2*(x1-x3)+s3*(x2-x1);
    const qx=x1*d-ux,qy=y1*d-uy;const r2=qx*qx+qy*qy;
    let dd=d,uu=ux,vv=uy,rr=r2;
    const g=gcdN(gcdN(Math.abs(dd),Math.abs(uu)),Math.abs(vv));
    dd/=g;uu/=g;vv/=g;rr/=(g*g);   // r^2 は g^2 で割る
    if(dd<0){dd=-dd;uu=-uu;vv=-vv;}
    const key=`${dd},${uu},${vv},${rr}`;
    if(keptC.has(key))continue;
    const pts:number[]=[];
    for(let y=0;y<w;y++){
      const dy=y*dd-vv;const rem=rr-dy*dy;if(rem<0)continue;
      const r=isqrt(rem);
      if(r*r===rem){
        const dxs=r===0?[0]:[r,-r];  // 接線時の二重追加防止
        for(const dx of dxs){
          const num=dx+uu;if(num%dd!==0)continue;
          const x=num/dd;if(x>=0&&x<m)pts.push(x+m*y);}}
    }
    if(pts.length>=q)keptC.set(key,Int32Array.from(pts));
  }
  const curves=lines.concat([...keptC.values()]);
  const pcCount=new Int32Array(N);
  for(const c of curves)for(const p of c)pcCount[p]++;
  const pcOff=new Int32Array(N+1);for(let p=0;p<N;p++)pcOff[p+1]=pcOff[p]+pcCount[p];
  const pcArr=new Int32Array(pcOff[N]);{let t=0;const fl=new Int32Array(N);
  for(let ci=0;ci<curves.length;ci++)for(const p of curves[ci]){pcArr[pcOff[p]+fl[p]]=ci;fl[p]++;}}
  return {N,px,py,nC:curves.length,nLines:lines.length,nCirc:keptC.size,curves,pcOff,pcArr};
}
function minimizeMachine(Ctx:any,q:number,restarts:number,shake:number,seed0:number,sampleK=24){
  const {N,curves,pcOff,pcArr}=Ctx;const nC=curves.length;
  const cnt=new Int32Array(nC),stone=new Uint8Array(N),unsafe=new Uint8Array(N);
  let seed=seed0;function rnd(){seed=(seed*1103515245+12345)&0x7fffffff;return seed/0x80000000;}
  function addStone(p:number){stone[p]=1;
    for(let oi=pcOff[p];oi<pcOff[p+1];oi++){const ci=pcArr[oi];cnt[ci]++;
      if(cnt[ci]===q-1){const c=curves[ci];for(let t=0;t<c.length;t++)unsafe[c[t]]=1;}}}
  const free:number[]=[];
  function maximalize(){
    free.length=0;for(let p=0;p<N;p++)if(!stone[p]&&!unsafe[p])free.push(p);
    while(free.length>0){
      if(free.length===1){addStone(free[0]);free.length=0;break;}
      const k=Math.min(sampleK,free.length);
      let bestP=-1,bestSc=-1;
      for(let t=0;t<k;t++){
        const i=Math.floor(rnd()*free.length);const p=free[i];
        let sc=0;
        for(let oi=pcOff[p];oi<pcOff[p+1];oi++)if(cnt[pcArr[oi]]===q-2)sc++;
        sc+=rnd()*0.5;
        if(sc>bestSc){bestSc=sc;bestP=p;}
      }
      addStone(bestP);
      let w2=0;
      for(let t=0;t<free.length;t++){const f=free[t];
        if(f===bestP)continue;
        if(!stone[f]&&!unsafe[f])free[w2++]=f;}
      free.length=w2;
    }
  }
  function rebuildFromMask(){cnt.fill(0);unsafe.fill(0);
    for(let p=0;p<N;p++)if(stone[p]){
      for(let oi=pcOff[p];oi<pcOff[p+1];oi++){const ci=pcArr[oi];cnt[ci]++;
        if(cnt[ci]===q-1){const c=curves[ci];for(let t=0;t<c.length;t++)unsafe[c[t]]=1;}}}}
  let bestSet:Int32Array|null=null;
  for(let r=0;r<restarts;r++){
    cnt.fill(0);stone.fill(0);unsafe.fill(0);
    maximalize();
    for(let s=0;s<shake;s++){
      const stones:number[]=[];for(let p=0;p<N;p++)if(stone[p])stones.push(p);
      if(stones.length<=q)break;
      const nrm=Math.max(2,Math.floor(stones.length/4));
      for(let t=0;t<nrm;t++){const p=stones[Math.floor(rnd()*stones.length)];stone[p]=0;}
      rebuildFromMask();maximalize();
    }
    const st:number[]=[];for(let p=0;p<N;p++)if(stone[p])st.push(p);
    if(bestSet===null||st.length<bestSet.length)bestSet=Int32Array.from(st);
  }
  return bestSet!;
}
function verifyIndependent(w:number,m:number,q:number,W:number[][]){
  const n=W.length;const xs=W.map(s=>s[0]),ys=W.map(s=>s[1]);
  let worstLine=0,worstCirc=0;
  const lineSeen=new Set<string>();
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
    let dx=xs[j]-xs[i],dy=ys[j]-ys[i];
    const g=gcdN(dx,dy);dx/=g;dy/=g;
    if(dy<0||(dy===0&&dx<0)){dx=-dx;dy=-dy;}
    const c0=xs[i]*dy-ys[i]*dx;
    const key=`${dx},${dy},${c0}`;
    if(lineSeen.has(key))continue;lineSeen.add(key);
    let c=0;for(let t=0;t<n;t++){if(xs[t]*dy-ys[t]*dx===c0)c++;}
    if(c>worstLine)worstLine=c;
  }
  const circSeen=new Set<string>();
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let k2=j+1;k2<n;k2++){
    const x1=xs[i],y1=ys[i],x2=xs[j],y2=ys[j],x3=xs[k2],y3=ys[k2];
    const d=2*(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2));if(d===0)continue;
    const s1=x1*x1+y1*y1,s2=x2*x2+y2*y2,s3=x3*x3+y3*y3;
    const ux=s1*(y2-y3)+s2*(y3-y1)+s3*(y1-y2), uy=s1*(x3-x2)+s2*(x1-x3)+s3*(x2-x1);
    let dd=d,uu=ux,vv=uy;
    const g=gcdN(gcdN(Math.abs(dd),Math.abs(uu)),Math.abs(vv));
    dd/=g;uu/=g;vv/=g;
    if(dd<0){dd=-dd;uu=-uu;vv=-vv;}
    const key=`${dd},${uu},${vv}`;
    if(circSeen.has(key))continue;circSeen.add(key);
    const qx=x1*dd-uu,qy=y1*dd-vv,rr=qx*qx+qy*qy;
    let c=0;for(let t=0;t<n;t++){const dx=xs[t]*dd-uu,dy=ys[t]*dd-vv;if(dx*dx+dy*dy===rr)c++;}
    if(c>worstCirc)worstCirc=c;
  }
  const safe=(worstLine<q)&&(worstCirc<q);
  const stoneSet=new Set<string>();for(let i=0;i<n;i++)stoneSet.add(xs[i]+","+ys[i]);
  const unblocked:number[][]=[];
  for(let x=0;x<m;x++)for(let y=0;y<w;y++){
    if(stoneSet.has(x+","+y))continue;
    let blocked=false;
    for(let i=0;i<n&&!blocked;i++){
      let dx=xs[i]-x,dy=ys[i]-y;
      const g=gcdN(dx,dy);dx/=g;dy/=g;
      if(dy<0||(dy===0&&dx<0)){dx=-dx;dy=-dy;}
      const c0=x*dy-y*dx;
      let c=0;for(let t=0;t<n;t++){if(xs[t]*dy-ys[t]*dx===c0)c++;}
      if(c>=q-1)blocked=true;
    }
    for(let i=0;i<n&&!blocked;i++)for(let j=i+1;j<n&&!blocked;j++){
      const x1=x,y1=y,x2=xs[i],y2=ys[i],x3=xs[j],y3=ys[j];
      const d=2*(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2));if(d===0)continue;
      const s1=x1*x1+y1*y1,s2=x2*x2+y2*y2,s3=x3*x3+y3*y3;
      const ux=s1*(y2-y3)+s2*(y3-y1)+s3*(y1-y2), uy=s1*(x3-x2)+s2*(x1-x3)+s3*(x2-x1);
      const qx=x1*d-ux,qy=y1*d-uy,r2=qx*qx+qy*qy;
      let c=0;for(let t=0;t<n;t++){const dx=xs[t]*d-ux,dy=ys[t]*d-uy;if(dx*dx+dy*dy===r2)c++;}
      if(c>=q-1)blocked=true;
    }
    if(!blocked)unblocked.push([x,y]);
  }
  return {n,worstLine,worstCirc,safe,maximal:unblocked.length===0,unblockedCount:unblocked.length,unblocked:unblocked.slice(0,3)};
}
async function main(){
  // RUNS: [w, m, q, restarts, shake, seed]
  const RUNS:[number,number,number,number,number,number][]=[
    [6,19,5,400,10,8000+19*41],
  ];
  const out:any[]=[];
  for(const [w,m,q,restarts,shake,seed] of RUNS){
    const ctx=buildCurves(w,m,q);
    const b=minimizeMachine(ctx,q,restarts,shake,seed);
    const witness=[...b].map(p=>[p%m,Math.floor(p/m)]);
    const full=w*(q-1);
    const r:any={w,m,q,min:b.length,full,nC:ctx.nC};
    if(b.length<full){
      r.witness=witness;
      r.independent=verifyIndependent(w,m,q,witness);
    }
    out.push(r);
  }
  return JSON.stringify(out);
}
