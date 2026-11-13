// handicap_deficient_machine.ts — 行capハンディキャップ貪欲による欠損極大witness探索機（2026-11-13 高速レーン・K0809）
// 目的: K0808 の貪欲（全行自由）では発見できなかった m での欠損witness（石数 < w(q-1) の極大安全配置）を発見する。
//
// 手法: 極大化の際に「一部の行の石数を q-2 以下に制限」し、その行の空点を円・斜線の
//   q-1石曲線でblockさせることを強制する（K0761式blocker分岐の貪欲近似・class-DFS の軽量版）。
//   満容量 w(q-1) は「全行がちょうど q-1 石」でしか達成されないため、行capが機能すれば
//   成功時の配置は自動的に石数 <= w(q-1)-1 となり欠損witnessになる。
//   制限行の選び方（1行/2行/3行・cap深さ）をパターン列としてrestartごとにローテーション。
//   近接解（leftover<=3）には1石移動ヒルクライム修復も試みたが本セッションでは決め手にならず。
//
// 重要な実装教訓（本機のバグ1件・制御で捕捉）:
//   free リストの保守フィルタで行capを再チェックしないと、cap行が q-1 石まで埋まり
//   満容量の「偽witness」（30石・極大だが欠損でない）が成功と誤計上される。
//   cap判定は free リスト構築時だけでなく addStone 後のフィルタでも毎回必要。
//
// 本セッションの結果（witnessは全て census不使用の独立検証で safe+maximal PASS）:
//   制御: (6,6) m=15 → 29石（K0808 witness域の再発見・機械健全性確認）
//   (6,5) m=20 → 23石 witness（1/1800 restarts）→ M_{6,5} >= 21
//   (6,5) m=21 → 23石 witness（49/1800）→ M_{6,5} >= 22
//   (6,6) m=16 → 29石 witness（1/1200）→ M_{6,6} >= 17
//   抵抗（非発見・不在証明ではない）: (6,5) m=22（minLeftover=3・1500 restarts）,
//     (6,6) m=17（minLeftover=1・4000）, (6,8) m=12（def1..4・8500・minLeftover=1..2）,
//     (5,6) m=16（def1..3・4700・minLeftover=1..3）, (5,7) m=19（def1..3・3200・minLeftover=8）
//   (6,8) m=12 は6行の中に行以外の >=8点直線が存在しない（nC=92・ほぼ全て円）構造的特徴あり。
//   抵抗5件はいずれも「M がこの値ちょうど」の候補を示唆するが、あくまでヒューリスティック。
//
// buildCurves / verifyIndependent は K0808 機（deficient_maximal_machine.ts）と同一ロジック。
//   円censusは3点組外心完全列挙・接線時二重追加なし・r^2 は g^2 で正規化（K0808 の修正済み仕様）。
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
    lineKeys.add('L'+dx+','+dy+','+(px[i]*dy-py[i]*dx));
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
    dd/=g;uu/=g;vv/=g;rr/=(g*g);
    if(dd<0){dd=-dd;uu=-uu;vv=-vv;}
    const key=dd+','+uu+','+vv+','+rr;
    if(keptC.has(key))continue;
    const pts:number[]=[];
    for(let y=0;y<w;y++){
      const dy=y*dd-vv;const rem=rr-dy*dy;if(rem<0)continue;
      const r=isqrt(rem);
      if(r*r===rem){
        const dxs=r===0?[0]:[r,-r];
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
// 行capパターン付きハンディキャップ貪欲。patterns[r % len] が各リスタートの行cap。
// 成功条件: leftover=0（全空点block）→ 自動的に |S| <= sum(caps) < w(q-1)（cap<q-1の行がある限り）。
function greedyHandicap2(w:number,m:number,q:number,Ctx:any,patterns:Int32Array[],restarts:number,shake:number,seed0:number,sampleK=24){
  const {N,curves,pcOff,pcArr}=Ctx;const nC=curves.length;
  const cnt=new Int32Array(nC),stone=new Uint8Array(N),unsafe=new Uint8Array(N);
  const rowCount=new Int32Array(w);
  let caps=patterns[0];
  let seed=seed0;function rnd(){seed=(seed*1103515245+12345)&0x7fffffff;return seed/0x80000000;}
  function capped(p:number){const ry=Math.floor(p/m);return rowCount[ry]>=caps[ry];}
  function addStone(p:number){stone[p]=1;rowCount[Math.floor(p/m)]++;
    for(let oi=pcOff[p];oi<pcOff[p+1];oi++){const ci=pcArr[oi];cnt[ci]++;
      if(cnt[ci]===q-1){const c=curves[ci];for(let t=0;t<c.length;t++)unsafe[c[t]]=1;}}}
  function rebuildAll(){cnt.fill(0);rowCount.fill(0);unsafe.fill(0);
    for(let p=0;p<N;p++)if(stone[p]){rowCount[Math.floor(p/m)]++;
      for(let oi=pcOff[p];oi<pcOff[p+1];oi++){const ci=pcArr[oi];cnt[ci]++;}}
    for(let ci=0;ci<nC;ci++)if(cnt[ci]===q-1){const c=curves[ci];for(let t=0;t<c.length;t++)unsafe[c[t]]=1;}}
  const free:number[]=[];
  function maximalize(){
    free.length=0;
    for(let p=0;p<N;p++){if(stone[p]||unsafe[p]||capped(p))continue;free.push(p);}
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
      // 教訓: cap再チェックはこの保守フィルタでも毎回行う（しないとcap行がq-1石まで埋まる）
      let w2=0;
      for(let t=0;t<free.length;t++){const f=free[t];
        if(f===bestP)continue;
        if(!stone[f]&&!unsafe[f]&&!capped(f))free[w2++]=f;}
      free.length=w2;
    }
  }
  function leftover(){let c=0;for(let p=0;p<N;p++)if(!stone[p]&&!unsafe[p])c++;return c;}
  let bestSet:Int32Array|null=null;let minLeft=1e9;let successes=0;let bestFull=1e9;
  for(let r=0;r<restarts;r++){
    caps=patterns[r%patterns.length];
    cnt.fill(0);stone.fill(0);unsafe.fill(0);rowCount.fill(0);
    maximalize();
    for(let s=0;s<shake;s++){
      const stones:number[]=[];for(let p=0;p<N;p++)if(stone[p])stones.push(p);
      if(stones.length<=q)break;
      const nrm=Math.max(2,Math.floor(stones.length/4));
      for(let t=0;t<nrm;t++){const p=stones[Math.floor(rnd()*stones.length)];stone[p]=0;}
      rebuildAll();maximalize();
    }
    const lo=leftover();
    if(lo<minLeft)minLeft=lo;
    if(lo===0){
      successes++;
      const st:number[]=[];for(let p=0;p<N;p++)if(stone[p])st.push(p);
      if(st.length<bestFull){bestFull=st.length;bestSet=Int32Array.from(st);}
    }
  }
  return {bestSet,successes,minLeft,bestFull};
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
    const key=dx+','+dy+','+c0;
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
    const key=dd+','+uu+','+vv;
    if(circSeen.has(key))continue;circSeen.add(key);
    const qx=x1*dd-uu,qy=y1*dd-vv,rr=qx*qx+qy*qy;
    let c=0;for(let t=0;t<n;t++){const dx=xs[t]*dd-uu,dy=ys[t]*dd-vv;if(dx*dx+dy*dy===rr)c++;}
    if(c>worstCirc)worstCirc=c;
  }
  const safe=(worstLine<q)&&(worstCirc<q);
  const stoneSet=new Set<string>();for(let i=0;i<n;i++)stoneSet.add(xs[i]+','+ys[i]);
  const unblocked:number[][]=[];
  for(let x=0;x<m;x++)for(let y=0;y<w;y++){
    if(stoneSet.has(x+','+y))continue;
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
  return {n,worstLine,worstCirc,safe,maximal:unblocked.length===0,unblockedCount:unblocked.length};
}
async function main(){
  // 実行例: [w, m, q, patterns, restarts, shake, seed]
  // patterns は行ごとの石数cap（例: (6,6) 欠損1 = 1行だけ4・他5）。
  const out:any[]=[];
  const w=6,m=16,q=6;
  const ctx=buildCurves(w,m,q);
  const full=Int32Array.from([5,5,5,5,5,5]);
  const pats:Int32Array[]=[];
  for(let a=0;a<6;a++){const p=Int32Array.from(full);p[a]=4;pats.push(p);}
  const r=greedyHandicap2(w,m,q,ctx,pats,1200,10,555);
  const rec:any={w,m,q,restarts:1200,successes:r.successes,minLeftover:r.minLeft,bestFull:r.bestFull,nC:ctx.nC};
  if(r.bestSet&&r.bestSet.length<w*(q-1)){
    const wit=[...r.bestSet].map(p=>[p%m,Math.floor(p/m)]);
    rec.witness=wit;rec.independent=verifyIndependent(w,m,q,wit);
  }
  out.push(rec);
  return JSON.stringify(out);
}
