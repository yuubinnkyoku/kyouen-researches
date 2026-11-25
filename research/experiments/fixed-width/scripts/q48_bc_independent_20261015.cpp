// Independent (d1,d2) enumeration of all positive integer 4-row chord patterns.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;
static bool square(int64_t n,int64_t &r){
 if(n<=0)return false;
 r=(int64_t)sqrt((double)n);
 while((r+1)*(r+1)<=n)++r;
 while(r*r>n)--r;
 return r*r==n;
}
static int64_t isqrt_nonnegative(int64_t n){
 int64_t r=(int64_t)sqrt((double)n);
 while((r+1)*(r+1)<=n)++r;
 while(r*r>n)--r;
 return r;
}
int main(int argc,char**argv){
 if(argc<2)return 2;
 const int B=atoi(argv[1]);
 const int M=12096;
 vector<uint8_t> sq(M);
 for(int i=0;i<M;i++)sq[1LL*i*i%M]=1;
 vector<vector<int>> ok(M);
 for(int b=0;b<M;b++)for(int c=b%2;c<M;c+=2){
  int64_t b2=1LL*b*b,c2=1LL*c*c;
  int aa=(int)((2*b2-c2-8)%M);if(aa<0)aa+=M;
  int dd=(int)((2*c2-b2-8)%M);if(dd<0)dd+=M;
  if(sq[aa]&&sq[dd])ok[b].push_back(c);
 }
 vector<array<int,4>> v;
 uint64_t tested=0;
 for(int b=1;b<=B;b++)for(int cr:ok[b%M]){
  if(2LL*b*b<9)continue;
  const int cmin=(int)isqrt_nonnegative((1LL*b*b+8)/2)+1;
  const int cmax=min(B,(int)isqrt_nonnegative(2LL*b*b-9));
  int c=cr?cr:M;
  if(c<cmin)c+=((cmin-c+M-1)/M)*M;
  for(;c<=cmax;c+=M){
  ++tested;
  int64_t a2=2LL*b*b-1LL*c*c-8;
  int64_t d2=2LL*c*c-1LL*b*b-8;
  if(a2<=0||d2<=0||a2>1LL*B*B||d2>1LL*B*B)continue;
  int64_t a,d;
  if(!square(a2,a)||!square(d2,d))continue;
  if(((a^b)|(c^d))&1)continue;
  v.push_back({(int)a,b,c,(int)d});
 }
 }
 sort(v.begin(),v.end());
 cerr<<"B="<<B<<" tested="<<tested<<" patterns="<<v.size()<<"\n";
 for(auto p:v)cout<<p[0]<<","<<p[1]<<","<<p[2]<<","<<p[3]<<"\n";
}
