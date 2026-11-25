#include <bits/stdc++.h>
using namespace std;
using ll=long long;
struct P{ll x,y;};
ll det(P a,P b,P c,P d){
 auto v=[](P p){return array<ll,3>{p.x*p.x+p.y*p.y,p.x,p.y};};
 auto A=v(a),B=v(b),C=v(c),D=v(d);
 for(int i=0;i<3;i++){B[i]-=A[i];C[i]-=A[i];D[i]-=A[i];}
 return B[0]*(C[1]*D[2]-C[2]*D[1])-B[1]*(C[0]*D[2]-C[2]*D[0])+B[2]*(C[0]*D[1]-C[1]*D[0]);
}
int main(){
 for(int m=1;m<=9;m++){
  int n=2*m,N=1<<n;vector<P> p;
  for(int x=0;x<m;x++)for(int y=0;y<2;y++)p.push_back({x,y});
  vector<unsigned char> ok(N,1),g(N,0),h(N,0);
  int nf=0;
  for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++)for(int l=k+1;l<n;l++){
   if(det(p[i],p[j],p[k],p[l]))continue;
   nf++;int s=(1<<i)|(1<<j)|(1<<k)|(1<<l),free=(N-1)^s;
   for(int t=free;;t=(t-1)&free){ok[s|t]=0;if(!t)break;}
  }
  int states=0,bad=0;map<int,int> hist;
  for(int s=N-1;s>=0;s--){
   if(!ok[s])continue;states++;unsigned gs=0,hs=0;int moves=0;
   for(int i=0;i<n;i++)if(!(s>>i&1)&&ok[s|(1<<i)]){
    moves++;gs|=1u<<g[s|(1<<i)];hs|=1u<<h[s|(1<<i)];
   }
   if(!moves){g[s]=0;h[s]=1;}
   else{while((gs>>g[s])&1u)g[s]++;while((hs>>h[s])&1u)h[s]++;}
   int expected=g[s]==0?1:g[s]==1?0:g[s];
   if(h[s]!=expected){bad++;hist[__builtin_popcount((unsigned)s)]++;}
  }
  cout<<"m="<<m<<" forbidden="<<nf<<" states="<<states<<" mismatches="<<bad
      <<" empty=("<<int(g[0])<<","<<int(h[0])<<")";
  for(auto [k,v]:hist)cout<<" size"<<k<<"="<<v;
  cout<<"\n";
 }
}
