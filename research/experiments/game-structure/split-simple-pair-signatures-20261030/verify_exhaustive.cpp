#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
using namespace std;
constexpr int MAXK=7, MAXX=1<<MAXK, MAXE=MAXK*(MAXK-1)/2;
void run(int K){
 const int X=1<<K, E=K*(K-1)/2;
 int sig[MAXE],next[MAXX][MAXE]{};
 uint32_t incident[MAXX]{};
 uint64_t aff[MAXE][2]{};
 int e=0;
 for(int u=0;u<K;u++)for(int v=u+1;v<K;v++)sig[e++]=(1<<u)|(1<<v);
 for(int x=0;x<X;x++)for(int i=0;i<E;i++){
  next[x][i]=x&~sig[i];
  if(x&sig[i]){incident[x]|=1u<<i;aff[i][x/64]|=1ULL<<(x%64);}
 }
 uint64_t p0=0,p1=0;
 unsigned char par[MAXX]{},val[MAXX]{};
 uint64_t dist[16]{};
 int maxg=0;uint32_t maxmask=0;uint64_t cnt=0;
 for(uint32_t it=0;it<(1u<<E);it++){
  // Consecutive Gray codes differ at bit ctz(it).
  if(it){int changed=__builtin_ctz(it);p0^=aff[changed][0];p1^=aff[changed][1];}
  uint32_t sel=it^(it>>1);
  for(int x=0;x<X;x++)par[x]=(x<64? (p0>>x)&1:(p1>>(x-64))&1);
  val[0]=0;
  for(int x=1;x<X;x++){
   unsigned opts=0;
   int bs=x;
   while(bs){int c=__builtin_ctz((unsigned)bs);bs&=bs-1;opts|=1u<<(par[x]^par[1<<c]);}
   bs=sel&incident[x];
   while(bs){int i=__builtin_ctz((unsigned)bs);bs&=bs-1;int y=next[x][i];opts|=1u<<(val[y]^par[x]^par[y]^1);}
   val[x]=__builtin_ctz(~opts);
  }
  int g=val[X-1];dist[g]++;cnt++;
  if(g>maxg){maxg=g;maxmask=sel;}
 }
 printf("k=%d edge-types=%d graphs=%llu max=%d first-mask=%u\n",K,E,(unsigned long long)cnt,maxg,maxmask);
 for(int i=0;i<16;i++)if(dist[i])printf("g=%d count=%llu\n",i,(unsigned long long)dist[i]);
 static const uint64_t expected[8][4] = {
  {0,0,0,0},{0,1,0,0},{0,2,0,0},{1,1,6,0},
  {8,8,18,30},{32,32,490,470},{1024,1024,15345,15375},
  {16384,16384,1032213,1032171}};
 for(int i=0;i<4;i++)if(dist[i]!=expected[K][i])abort();
 for(int i=4;i<16;i++)if(dist[i])abort();
}
int main(){for(int k=2;k<=MAXK;k++)run(k);puts("all exhaustive checks passed");}
