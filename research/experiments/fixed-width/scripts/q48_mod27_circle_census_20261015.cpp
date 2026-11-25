// Exact four-row eight-point circle census via quadratic-residue wheel.
// Build: g++ -O3 -std=c++17 q48_mod27_census.cpp -o census
// Usage: census MAX_CHORD MODULUS [EXTRA_MODULUS]
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;
static bool positive_square(int64_t n, int64_t &r){
 if(n<=0)return false;
 r=(int64_t)sqrt((double)n);
 while((r+1)*(r+1)<=n)++r;
 while(r*r>n)--r;
 return r*r==n;
}
int main(int argc,char**argv){
 if(argc<3){cerr<<"usage: census B M [p]\n";return 2;}
 const int B=atoi(argv[1]),M=atoi(argv[2]),p=argc>3?atoi(argv[3]):1;
 if(B<1||B>3000000||M<1||M>15000||p<1||p>1000)return 2;
 auto t0=chrono::steady_clock::now();
 vector<unsigned char> sq(M), sqp(p);
 for(int i=0;i<M;i++)sq[1LL*i*i%M]=1;
 for(int i=0;i<p;i++)sqp[1LL*i*i%p]=1;
 vector<vector<int>> good(M);
 uint64_t residues=0;
 for(int a=0;a<M;a++)for(int b=a%2;b<M;b+=2){
  int64_t aa=1LL*a*a,bb=1LL*b*b;
  int c=(int)((2*bb-aa-8)%M);if(c<0)c+=M;
  if(!sq[c])continue;
  int d=(int)((3*bb-2*aa-24)%M);if(d<0)d+=M;
  if(!sq[d])continue;
  good[a].push_back(b);residues++;
 }
 auto t1=chrono::steady_clock::now();
 vector<array<int,4>> patterns;
 uint64_t tested=0,passedp=0,eligible=0,passedc=0;
 int64_t bound=1LL*B*B;
 for(int a=1;a<=B;a++){
  int64_t aa=1LL*a*a;
  for(int br:good[a%M])for(int b=br?br:M;b<=B;b+=M){
   tested++;
   int64_t bb=1LL*b*b;
   int64_t cc=2*bb-aa-8,dd=3*bb-2*aa-24;
   if(cc<=0||cc>bound||dd<=0||dd>bound)continue;
   eligible++;
   if(p>1){
    int c=(int)(cc%p),d=(int)(dd%p);
    if(!sqp[c]||!sqp[d])continue;
   }
   passedp++;
   int64_t c,d;
   if(!positive_square(cc,c))continue;
   passedc++;
   if(!positive_square(dd,d))continue;
   if(((a^c)|(a^d))&1)continue;
   patterns.push_back({a,b,(int)c,(int)d});
  }
 }
 sort(patterns.begin(),patterns.end());
 auto t2=chrono::steady_clock::now();
 cerr<<"B="<<B<<" M="<<M<<" p="<<p<<" residues="<<residues<<" tested="<<tested<<" eligible="<<eligible<<" passedp="<<passedp<<" passedc="<<passedc<<" patterns="<<patterns.size()<<" prep="<<chrono::duration<double>(t1-t0).count()<<" run="<<chrono::duration<double>(t2-t1).count()<<"\n";
 for(auto v:patterns)cout<<v[0]<<","<<v[1]<<","<<v[2]<<","<<v[3]<<"\n";
}
