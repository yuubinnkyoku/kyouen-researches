// Exhaustive labeled graph enumeration for independent-set placement Grundy values.
// C++17; g(S) = mex{g(S+v): v not in S, no edge to S}.
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
int main() {
 for(int n=0;n<=7;++n){
  vector<pair<int,int>> E;
  for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)E.emplace_back(i,j);
  uint64_t hist[9]={}, first=UINT64_MAX;int maxg=0;
  const int full=(1<<n)-1, lim=1<<E.size();
  array<unsigned char,128> g{};
  array<unsigned char,128> valid{};
  int adj[7]={};
  for(int graph=0;graph<lim;graph++){
   for(int i=0;i<n;i++)adj[i]=0;
   for(int e=0;e<(int)E.size();e++)if(graph&(1<<e)){
    auto [a,b]=E[e];adj[a]|=1<<b;adj[b]|=1<<a;
   }
   valid[0]=1;
   for(int s=1;s<=full;s++){
    int v=__builtin_ctz((unsigned)s), rest=s^(1<<v);
    valid[s]=valid[rest] && !(adj[v]&rest);
   }
   for(int s=full;s>=0;s--){
    if(!valid[s])continue;
    int children=0;
    for(int v=0;v<n;v++)if(!(s&(1<<v)) && valid[s|(1<<v)]){
      children|=1<<g[s|(1<<v)];
    }
    int mex=0;while(children&(1<<mex))mex++;
    g[s]=mex;
   }
   int x=g[0];hist[x]++;
   if(x>maxg){maxg=x;first=graph;}
  }
  cout<<"n="<<n<<" graphs="<<lim<<" max="<<maxg<<" first="<<first<<" hist=";
  for(int k=0;k<=n;k++)cout<<(k?",":"")<<hist[k];
  cout<<"\n";
  if(n==7){
    for(int e=0;e<(int)E.size();e++)if(first&(1ULL<<e))cout<<"("<<E[e].first<<","<<E[e].second<<") ";cout<<"\n";
  }
 }
}
