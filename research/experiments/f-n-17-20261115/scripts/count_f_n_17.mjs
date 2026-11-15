// F_n on the n x n grid: count 4-subsets that are co-circular OR co-linear.
// 系A circles(n): 1-form (r1 x r2) . r3 == 0, excluding (a,b,c) 2D-collinear triples.
//   Those triples give co-LINEAR quads when d is on the line (counted by lines()),
//   and can never be co-circular when d is off the line (3 collinear pts + off-line pt).
// 系D lines(n): primitive-direction maximal-line enumeration, C(t,4) per line.
// 系B total(n): pure 3x3 determinant (cofactor expansion), no skips. Independent cross-check.
// Calibration: n=12 -> C=141272 D=17154 F=158426; n=13 -> C=225022 D=27340 (batch-08 values).
function circles(n){
const px=new Int8Array(n*n),py=new Int8Array(n*n),pw=new Int32Array(n*n);
for(let p=0;p<n*n;p++){px[p]=p%n;py[p]=p/n|0;pw[p]=px[p]*px[p]+py[p]*py[p];}
let C=0;
for(let a=0;a<n*n-3;a++){const wa=pw[a],xa=px[a],ya=py[a];
for(let b=a+1;b<n*n-2;b++){const bw=pw[b]-wa,bx=px[b]-xa,by=py[b]-ya;
for(let c=b+1;c<n*n-1;c++){const cw=pw[c]-wa,cx=px[c]-xa,cy=py[c]-ya;
const c1=bx*cy-by*cx,c2=by*cw-bw*cy,c3=bw*cx-bx*cw;
if(c1===0&&bx*(py[c]-ya)===by*(px[c]-xa))continue;
for(let d=c+1;d<n*n;d++)
if(c1*(pw[d]-wa)+c2*(px[d]-xa)+c3*(py[d]-ya)===0)C++;}}}
return C;}
function lines(n){
const inG=(x,y)=>x>=0&&x<n&&y>=0&&y<n;
let D=0;
for(let a=0;a<n;a++)for(let b=-n+1;b<n;b++){
if(a===0&&b<=0)continue;
let g=a,bb=Math.abs(b);while(bb){const t=g%bb;g=bb;bb=t;}
if(g!==1)continue;
for(let x=0;x<n;x++)for(let y=0;y<n;y++){
if(inG(x-a,y-b))continue;
let t=0,cx=x,cy=y;
while(inG(cx,cy)){t++;cx+=a;cy+=b;}
if(t>=4)D+=t*(t-1)*(t-2)*(t-3)/24;}}
return D;}
function total(n){
const px=new Int8Array(n*n),py=new Int8Array(n*n),pw=new Int32Array(n*n);
for(let p=0;p<n*n;p++){px[p]=p%n;py[p]=p/n|0;pw[p]=px[p]*px[p]+py[p]*py[p];}
let F=0;
for(let a=0;a<n*n-3;a++){const wa=pw[a],xa=px[a],ya=py[a];
for(let b=a+1;b<n*n-2;b++){const r1x=px[b]-xa,r1y=py[b]-ya,r1w=pw[b]-wa;
for(let c=b+1;c<n*n-1;c++){const r2x=px[c]-xa,r2y=py[c]-ya,r2w=pw[c]-wa;
for(let d=c+1;d<n*n;d++){const r3x=px[d]-xa,r3y=py[d]-ya,r3w=pw[d]-wa;
if(r1x*(r2y*r3w-r2w*r3y)-r1y*(r2x*r3w-r2w*r3x)+r1w*(r2x*r3y-r2y*r3x)===0)F++;}}}}
return F;}
const out={};
for(const n of[12,13,17]){const C=circles(n),D=lines(n);out[n]={C,D,F:total(n)};}
out.check_n17=(out[17].C+out[17].D===out[17].F);
console.log(JSON.stringify(out));
