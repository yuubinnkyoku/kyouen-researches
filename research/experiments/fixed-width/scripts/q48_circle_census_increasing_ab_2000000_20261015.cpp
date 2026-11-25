// Exact 4-row q=8 chord census: increasing odd quadruples only.
// Compile: g++ -O3 -std=c++17 census_ab.cpp -o census_ab
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;
static bool square(int64_t n, int64_t &r){
 if(n<=0)return false;
 r=(int64_t)sqrt((double)n);
 while(r*r<n)++r;
 while(r*r>n)--r;
 return r*r==n;
}
int main(int argc,char**argv){
 int B=argc>1?atoi(argv[1]):4100000;
 if(B<1||B>4100000)return 2;
 constexpr int M=4032;
 bool sq[M]={};
 for(int i=0;i<M;i++)sq[1LL*i*i%M]=true;
 vector<vector<int>> good(M);
 for(int a=1;a<M;a+=2)for(int b=1;b<M;b+=2){
  int64_t a2=1LL*a*a,b2=1LL*b*b;
  int c=(int)((2*b2-a2-8+4LL*M*M)%M);
  int d=(int)((3*b2-2*a2-24+4LL*M*M)%M);
  if(sq[c]&&sq[d])good[a].push_back(b);
 }
 vector<array<int,4>> ans;
 uint64_t tested=0,eligible=0;
 int64_t bound=1LL*B*B;
 for(int a=1;a<=B;a+=2){
  int64_t a2=1LL*a*a;
  for(int residue:good[a%M]){
   for(int b=residue;b<=B;b+=M){
    if(b<=a)continue;
    int64_t b2=1LL*b*b;
    int64_t c2=2*b2-a2-8,d2=3*b2-2*a2-24;
    if(d2>bound)break;
    if(c2<=b2||d2<=c2)continue;
    ++tested;
    int64_t c,d;
    if(!square(c2,c)||!square(d2,d))continue;
    if(c<=b||d<=c||d>B||((a^c)|(a^d))&1)continue;
    ++eligible;
    ans.push_back({a,b,(int)c,(int)d});
   }
  }
 }
 sort(ans.begin(),ans.end());
 cerr<<"B="<<B<<" tested="<<tested<<" patterns="<<ans.size()<<"\n";
 for(auto p:ans)cout<<p[0]<<","<<p[1]<<","<<p[2]<<","<<p[3]<<"\n";
}
