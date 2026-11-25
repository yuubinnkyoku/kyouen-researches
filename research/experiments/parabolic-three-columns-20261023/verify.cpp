// Independent determinant-based full-state enumeration, lambda=0, 3 x m.
// Compile: g++ -std=c++17 -O3 verify.cpp -o verify-parabolic
#include <array>
#include <vector>
#include <iostream>
#include <algorithm>
#include <cstdint>
using namespace std;
long long det4(array<array<long long,4>,4> a){
 long long s=0;
 array<int,4> p={0,1,2,3};
 do {long long v=1;int inv=0;for(int i=0;i<4;i++){v*=a[i][p[i]];for(int j=i+1;j<4;j++)inv+=(p[i]>p[j]);}s+=(inv%2?-v:v);}while(next_permutation(p.begin(),p.end()));
 return s;
}
int main(int argc,char**argv){
 int maxm=argc>1?stoi(argv[1]):7;
 if(maxm<1 || maxm>7){cerr<<"use 1<=maxm<=7\n";return 3;}
 for(int m=1;m<=maxm;m++){
  int n=3*m, M=1<<n;
  vector<uint8_t> bad(M,0),g(M,0);
  int fq=0;
  for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)for(int d=c+1;d<n;d++){
   array<int,4> is={a,b,c,d};array<array<long long,4>,4> mat{};
   for(int i=0;i<4;i++){int x=is[i]%3,y=is[i]/3;mat[i]={x*x,x,y,1};}
   if(det4(mat)==0){bad[(1<<a)|(1<<b)|(1<<c)|(1<<d)]=1;fq++;}
  }
  for(int i=0;i<n;i++)for(int s=0;s<M;s++)if(s&(1<<i))bad[s]|=bad[s^(1<<i)];
  long long safe=0;array<long long,5> sizes{};array<long long,5> terminal{};array<array<long long,4>,5> nim{};int violations=0;
  for(int s=M-1;s>=0;s--){if(bad[s])continue;int k=__builtin_popcount((unsigned)s);if(k>4){cerr<<"unsafe size";return 1;}safe++;sizes[k]++;
   unsigned opts=0;bool any=false;
   for(int i=0;i<n;i++)if(!(s&(1<<i))&&!bad[s|(1<<i)]){any=true;opts|=1u<<g[s|(1<<i)];}
   if(!any)terminal[k]++;
   int v=0;while(opts&(1u<<v))v++;g[s]=v;
   if(v>=4){cerr<<"nim too big";return 1;}nim[k][v]++;
   int expected=0;
   if(m==1)expected=(3-k)&1;
   else if(m==2)expected=(k==1||k==3)?1:0;
   else if(k==1)expected=1;
   else if(k==2){int c[3]={};for(int i=0;i<n;i++)if(s&(1<<i))c[i%3]++;expected=(*max_element(c,c+3)==2)?2:0;}
   else if(k==3){int c[3]={};for(int i=0;i<n;i++)if(s&(1<<i))c[i%3]++;expected=(*max_element(c,c+3)==3)?0:1;}
   if(v!=expected)violations++;
  }
  long long choose2=1LL*m*(m-1)/2,choose3=1LL*m*(m-1)*(m-2)/6;
  long long expected_safe=1+3LL*m+1LL*n*(n-1)/2+1LL*n*(n-1)*(n-2)/6+3*choose2*m*m;
  if(safe!=expected_safe||violations||terminal[3]!=(m==1?1:3*choose3)||terminal[4]!=3*choose2*m*m){cerr<<"FAILED m="<<m<<" safe="<<safe<<" expected="<<expected_safe<<" violations="<<violations<<"\n";return 2;}
  cout<<"m="<<m<<" forbidden4="<<fq<<" safe="<<safe<<" root="<<(int)g[0]<<" terminal3="<<terminal[3]<<" terminal4="<<terminal[4]<<" g2="<<nim[2][2]<<" PASS\n";
 }
}
