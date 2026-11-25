// Independent 4-row eight-point circle census: enumerate (d0,d2).
// g++ -O3 -std=c++17 this.cpp -o /tmp/q48_ac && /tmp/q48_ac 1000000
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
 while(r*r<n)++r;
 while(r*r>n)--r;
 return r*r==n;
}
static int mod(int64_t n,int m){int r=(int)(n%m);return r<0?r+m:r;}
int main(int argc,char**argv){
 int B=argc>1?atoi(argv[1]):1000000;
 if(B<1||B>1000000)return 2;
 constexpr int M=4032,R=2016;
 bool sq[R]={};
 for(int i=0;i<R;i++)sq[1LL*i*i%R]=true;
 vector<vector<int>> good(M);
 for(int a=0;a<M;a++)for(int c=(a&1);c<M;c+=2){
  int64_t a2=1LL*a*a,c2=1LL*c*c;
  int64_t bnum=a2+c2+8,dnum=3*c2-a2-24;
  if((bnum&1)||(dnum&1))continue;
  if(sq[mod(bnum/2,R)]&&sq[mod(dnum/2,R)])good[a].push_back(c);
 }
 vector<array<int,4>> ans;
 uint64_t tested=0,eligible=0;
 int64_t bound=1LL*B*B;
 for(int a=1;a<=B;a++){
  int64_t a2=1LL*a*a;
  for(int residue:good[a%M]){
   for(int c=residue?residue:M;c<=B;c+=M){
    ++tested;
    int64_t c2=1LL*c*c;
    int64_t bnum=a2+c2+8,dnum=3*c2-a2-24;
    if((bnum&1)||(dnum&1))continue;
    int64_t b2=bnum/2,d2=dnum/2;
    if(b2<=0||b2>bound||d2<=0||d2>bound)continue;
    ++eligible;
    int64_t b,d;
    if(!square(b2,b)||!square(d2,d))continue;
    if(((a^b)|(a^c)|(a^d))&1)continue;
    ans.push_back({a,(int)b,c,(int)d});
   }
  }
 }
 sort(ans.begin(),ans.end());
 cerr<<"B="<<B<<" residue-tested="<<tested<<" positive-in-range="<<eligible<<" patterns="<<ans.size()<<"\n";
 for(auto p:ans)cout<<p[0]<<","<<p[1]<<","<<p[2]<<","<<p[3]<<"\n";
}
