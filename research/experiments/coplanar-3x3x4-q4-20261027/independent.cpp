// Independent check: 3D cross-product determinant, root DFS with memoised mex.
// Generalisation of ../coplanar-3x3xm-q4-20261024/independent.cpp from
// uint32_t masks (N<=27) to uint64_t masks (N<=45), so m=4 and m=5 run.
// Point order differs from verify.py on purpose (z,y,x here; x,y,z there).
#include <bits/stdc++.h>
using namespace std;
using U=uint64_t;
struct P{int x,y,z;};
P p[64];int N;
U forbidden[64][64][64];
int det(P a,P b,P c,P d){int x=b.x-a.x,y=b.y-a.y,z=b.z-a.z;int X=c.x-a.x,Y=c.y-a.y,Z=c.z-a.z;int xx=d.x-a.x,yy=d.y-a.y,zz=d.z-a.z;return x*(Y*zz-Z*yy)-y*(X*zz-Z*xx)+z*(X*yy-Y*xx);}
struct Val {uint8_t g,h;};
unordered_map<U,Val> memo;
uint64_t layer[64]={}, terminals[64]={}, histg[32]={}, histh[32]={};
int maxK=0,minS=100;
U blocked(U s){int a[64],n=0;for(U t=s;t;t&=t-1)a[n++]=__builtin_ctzll(t);U r=0;for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++)r|=forbidden[a[i]][a[j]][a[k]];return r;}
Val dfs(U s){auto it=memo.find(s);if(it!=memo.end())return it->second;int n=__builtin_popcountll(s);U legal=((N==64)?~U(0):((U(1)<<N)-1))&~(s|blocked(s));bool gseen[64]={},hseen[64]={};if(!legal){terminals[n]++;minS=min(minS,n);maxK=max(maxK,n);}else{for(U t=legal;t;t&=t-1){U bit=t&-t;auto v=dfs(s|bit);gseen[v.g]=1;hseen[v.h]=1;}}int g=0,h=0;while(gseen[g])g++;if(!legal)h=1;else while(hseen[h])h++;memo.emplace(s,Val{uint8_t(g),uint8_t(h)});layer[n]++;histg[g]++;histh[h]++;return {uint8_t(g),uint8_t(h)};}
int main(int argc,char**argv){if(argc!=2)return 2;int m=atoi(argv[1]);if(m<1||m>6)return 2;int n=9*m;N=n;int i=0;for(int z=0;z<m;z++)for(int y=0;y<3;y++)for(int x=0;x<3;x++)p[i++]={x,y,z};long long cnt=0;for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)for(int d=c+1;d<n;d++)if(det(p[a],p[b],p[c],p[d])==0){cnt++;for(int j:{a,b,c,d}){int q[3],k=0;for(int t:{a,b,c,d})if(t!=j)q[k++]=t;sort(q,q+3);forbidden[q[0]][q[1]][q[2]]|=U(1)<<j;}}auto root=dfs(0);cout<<"m="<<m<<" forbidden="<<cnt<<" states="<<memo.size()<<" K="<<maxK<<" s="<<minS<<" g(empty)="<<int(root.g)<<" h(empty)="<<int(root.h)<<"\n";for(int k=0;k<=n;k++)if(layer[k])cout<<"layer "<<k<<" states "<<layer[k]<<" terminal "<<terminals[k]<<"\n";for(int k=0;k<32;k++)if(histg[k]||histh[k])cout<<"nimber "<<k<<" normal "<<histg[k]<<" misere "<<histh[k]<<"\n";cout<<"first_moves:";for(int j=0;j<n;j++){auto v=dfs(U(1)<<j);cout<<" ("<<p[j].x<<","<<p[j].y<<","<<p[j].z<<")=["<<int(v.g)<<","<<int(v.h)<<"]";}cout<<"\n";}
