#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
// Independent recurrence: a state is the REMAINING vertex mask. Move removes one bit.
// A move is legal if it does not complete any of the five forbidden 4-sets.
int main(int argc,char**argv){
 const int n=argc>1?atoi(argv[1]):9;
 if(n<5||n>11) return 2;
 const int all=(1<<n)-1;
 vector<int> masks;
 for(int mask=0;mask<=all;mask++)if(__builtin_popcount((unsigned)mask)==4)masks.push_back(mask);
 assert(masks[0]==15);
 array<int,5> e={15,0,0,0,0};
 array<uint64_t,16> hist{},lineHist{};
 uint64_t count=0,cover=0,linearCount=0;
 vector<uint8_t> dp(1<<n,255);
 int maxg=-1, maxlin=-1;
 array<int,5> maxw{}, linw{};
 for(int a=1;a<(int)masks.size()-3;a++)for(int b=a+1;b<(int)masks.size()-2;b++)for(int c=b+1;c<(int)masks.size()-1;c++)for(int d=c+1;d<(int)masks.size();d++){
  e[1]=masks[a];e[2]=masks[b];e[3]=masks[c];e[4]=masks[d];count++;
  if((e[0]|e[1]|e[2]|e[3]|e[4])!=all)continue;
  cover++;
  bool lin=true;
  for(int i=0;i<5;i++)for(int j=0;j<i;j++)if(__builtin_popcount((unsigned)(e[i]&e[j]))>2)lin=false;
  if(lin)linearCount++;
  // Remaining mask 0..all, each move decreases mask. Compute in increasing order.
  for(int rem=0;rem<=all;rem++){
   const int occ=all^rem;
   bool bad=false;
   for(int k=0;k<5;k++)if((occ&e[k])==e[k]){bad=true;break;}
   if(bad){dp[rem]=255;continue;}
   unsigned int children=0;
   for(int bits=rem;bits;bits&=bits-1){
     int child=dp[rem^(bits&-bits)];
     if(child!=255)children|=1u<<child;
   }
   int mex=0;while(children&(1u<<mex))mex++;
   dp[rem]=(uint8_t)mex;
  }
  int g=dp[all];hist[g]++;
  if(g>maxg){maxg=g;maxw=e;}
  if(lin){lineHist[g]++;if(g>maxlin){maxlin=g;linw=e;}}
 }
 cout<<"n="<<n<<" all="<<count<<" cover="<<cover<<" linear-cover="<<linearCount<<" max="<<maxg<<" linear-max="<<maxlin<<"\n";
 for(int i=0;i<16;i++)if(hist[i]||lineHist[i])cout<<"g="<<i<<" cover="<<hist[i]<<" linear="<<lineHist[i]<<"\n";
 cout<<"witness=";for(int v:maxw)cout<<v<<",";cout<<"\nlinear-witness=";for(int v:linw)cout<<v<<",";cout<<"\n";
}
