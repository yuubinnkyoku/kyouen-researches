function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b){[a,b]=[b,a%b];}return a||1;}
function census(W,M){
  const N=W*M,xs=new Int32Array(N),ys=new Int32Array(N);
  for(let y=0;y<W;y++)for(let x=0;x<M;x++){xs[x+M*y]=x;ys[x+M*y]=y;}
  let nC=0;const seen=new Set();const buf=new Int32Array(64);const hist={};
  for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)for(let k=j+1;k<N;k++){
    const ax=xs[i],ay=ys[i],bx=xs[j],by=ys[j],cx=xs[k],cy=ys[k];
    const d=2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by));if(d===0)continue;
    const a2=ax*ax+ay*ay,b2=bx*bx+by*by,c2=cx*cx+cy*cy;
    const ux=a2*(by-cy)+b2*(cy-ay)+c2*(ay-by),uy=a2*(cx-bx)+b2*(ax-cx)+c2*(bx-ax);
    let g=gcd(gcd(Math.abs(d),Math.abs(ux)),Math.abs(uy));if(d<0)g=-g;
    const D=d/g,Ux=ux/g,Uy=uy/g,R2n=(ax*D-Ux)**2+(ay*D-Uy)**2,R2d=D*D,g2=gcd(R2n,R2d);
    const key=Ux+','+Uy+','+D+','+(R2n/g2)+'/'+(R2d/g2);if(seen.has(key))continue;
    let m=0;for(let p=0;p<N;p++){const vx=xs[p]*D-Ux,vy=ys[p]*D-Uy;if(vx*vx+vy*vy===R2n)buf[m++]=p;}
    if(m>=7){seen.add(key);nC++;hist[m]=(hist[m]||0)+1;}
  }
  return {nC,hist};
}
const out={};
for(const M of [18,19,20])out["5x"+M]=census(5,M);
require('fs').writeFileSync('output/census.json',JSON.stringify(out,null,1));
console.log(JSON.stringify(out));
