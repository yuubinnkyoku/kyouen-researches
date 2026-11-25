#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
static int cnt[32],rem[5]={4,4,4,4,4},n=0;
static uint64_t count_all[21],count_distinct[21],hist[21][16];
static int maxg[21];
int solve(vector<int> es,int m){
 int limit=1<<m;
 vector<unsigned char> g(limit,255);
 for(int r=0;r<limit;r++){
  bool safe=true;
  for(int e:es)if(!(r&e)){safe=false;break;}
  if(!safe)continue;
  unsigned children=0;
  for(int v=r;v;v&=v-1){int sub=r^(v&-v);if(g[sub]!=255)children|=1u<<g[sub];}
  g[r]=__builtin_ctz(~children);
 }
 return g[limit-1];
}
int score(array<int,5> edges,int nv){
 // Find vertex components via direct point adjacency, not via edge DSU.
 int adj[20]={};
 for(int e:edges)for(int a=e;a;a&=a-1){int b=a&-a;adj[__builtin_ctz((unsigned)b)]|=e;}
 int remaining=(1<<nv)-1,ans=0;
 while(remaining){
  int component=remaining&-remaining;
  while(true){
   int expanded=component;
   for(int b=component;b;b&=b-1)expanded|=adj[__builtin_ctz((unsigned)(b&-b))];
   if(expanded==component)break;
   component=expanded;
  }
  remaining &= ~component;
  vector<int> local_edges;
  for(int e:edges)if(e&component){
   assert((e&component)==e);
   int compressed=0,k=0;
   for(int b=component;b;b&=b-1,k++)if(e&(b&-b))compressed|=1<<k;
   local_edges.push_back(compressed);
  }
  ans ^= solve(local_edges,__builtin_popcount((unsigned)component));
 }
 return ans;
}
void leaf(){
 if(rem[0]||rem[1]||rem[2]||rem[3]||rem[4])return;
 count_all[n]++;
 array<int,5> e{};
 int v=0;
 for(int t=31;t>=1;t--)for(int j=0;j<cnt[t];j++){
  for(int i=0;i<5;i++)if(t&(1<<i))e[i]|=1<<v;
  v++;
 }
 assert(v==n);
 for(int i=0;i<5;i++)for(int j=0;j<i;j++)if(e[i]==e[j])return;
 count_distinct[n]++;
 int g=score(e,n);
 hist[n][g]++;
 maxg[n]=max(maxg[n],g);
}
void visit(int t){
 if(t==0){leaf();return;}
 int bound=20-n;
 for(int i=0;i<5;i++)if(t&(1<<i))bound=min(bound,rem[i]);
 for(int k=bound;k>=0;k--){
  cnt[t]=k;n+=k;
  for(int i=0;i<5;i++)if(t&(1<<i))rem[i]-=k;
  visit(t-1);
  for(int i=0;i<5;i++)if(t&(1<<i))rem[i]+=k;
  n-=k;
 }
 cnt[t]=0;
}
int main(){fill(maxg,maxg+21,-1);visit(31);
 for(int i=4;i<=20;i++)if(count_all[i]){
  cout<<"n="<<i<<" patterns="<<count_all[i]<<" distinct="<<count_distinct[i]<<" max="<<maxg[i]<<" hist=";
  for(int g=0;g<16;g++)if(hist[i][g])cout<<g<<":"<<hist[i][g]<<",";
  cout<<"\n";
 }
}
