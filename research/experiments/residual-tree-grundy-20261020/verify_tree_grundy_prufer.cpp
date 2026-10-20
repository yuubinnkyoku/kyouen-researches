// Exact exhaustive labelled-tree check, independent of NetworkX tree generation.
// Compile: g++ -O2 -std=c++17 verify_tree_grundy_prufer.cpp -o verify_tree_grundy_prufer
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <vector>
using namespace std;

int grundy_tree(int n, const vector<pair<int,int>>& edges) {
  array<int,8> closed{};
  for (int i=0;i<n;++i) closed[i]=1<<i;
  for (auto [u,v]:edges) {closed[u]|=1<<v;closed[v]|=1<<u;}
  vector<int> dp(1<<n,-1);
  dp[0]=0;
  for (int mask=1;mask<(1<<n);++mask) {
    int seen=0;
    for(int v=0;v<n;++v) if(mask&(1<<v)) {
      int sub=mask&~closed[v];
      assert(sub<mask);
      seen|=1<<dp[sub];
    }
    int mex=0;
    while(seen&(1<<mex))++mex;
    dp[mask]=mex;
  }
  return dp[(1<<n)-1];
}

vector<pair<int,int>> decode_prufer(int n, uint64_t index) {
  vector<int> p(n-2),deg(n,1);
  for(int i=0;i<n-2;++i) {p[i]=index%n;index/=n;++deg[p[i]];}
  vector<pair<int,int>> edges;
  for(int x:p) {
    int leaf=0;
    while(deg[leaf]!=1) ++leaf;
    edges.push_back({leaf,x});
    --deg[leaf];--deg[x];
  }
  int a=-1,b=-1;
  for(int v=0;v<n;++v) if(deg[v]==1) {if(a==-1)a=v;else b=v;}
  edges.push_back({a,b});
  return edges;
}

int main(){
  for(int n=1;n<=8;++n){
    uint64_t total=1;
    for(int i=0;i<n-2;++i)total*=n;
    map<int,uint64_t> hist;
    uint64_t witness=UINT64_MAX;
    for(uint64_t id=0;id<total;++id){
      auto edges=(n==1?vector<pair<int,int>>{}:decode_prufer(n,id));
      int g=grundy_tree(n,edges);
      ++hist[g];
      if(g==4&&witness==UINT64_MAX)witness=id;
    }
    cout<<"n="<<n<<" labelled="<<total<<" nimbers:";
    for(auto [g,c]:hist)cout<<" "<<g<<":"<<c;
    cout<<"\n";
    if(witness!=UINT64_MAX){
      cout<<"  first g=4 prufer_id="<<witness<<" edges=";
      for(auto [u,v]:decode_prufer(n,witness))cout<<"("<<u<<","<<v<<")";
      cout<<"\n";
    }
  }
}
