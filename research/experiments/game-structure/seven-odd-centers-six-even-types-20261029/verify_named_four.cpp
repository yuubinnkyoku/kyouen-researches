// Exhaustive independent named-vertex check for exactly four even pair types.
// Usage: g++ -O3 -std=c++17 verify_named_four.cpp -o /tmp/seven-named-four
//        /tmp/seven-named-four
#include <bits/stdc++.h>
using namespace std;
constexpr int K=7,E=21,FULL=1<<E;
struct Named{
 vector<uint64_t> adj;unordered_map<uint64_t,uint8_t> memo;
 int sg(uint64_t mask){
  uint64_t iso=0;
  for(uint64_t p=mask;p;p&=p-1){
   int v=__builtin_ctzll(p);if(!(adj[v]&mask))iso|=1ULL<<v;
  }
  int parity=__builtin_popcountll(iso)&1;mask&=~iso;
  if(!mask)return parity;
  auto it=memo.find(mask);if(it!=memo.end())return it->second^parity;
  uint64_t opts=0;
  for(uint64_t p=mask;p;p&=p-1){
   int v=__builtin_ctzll(p);
   opts|=1ULL<<sg(mask&~(adj[v]|(1ULL<<v)));
  }
  int g=__builtin_ctzll(~opts);
  memo.emplace(mask,(uint8_t)g);return g^parity;
 }
 int value(int mask,const vector<pair<int,int>>& edges,uint32_t doubled=0){
  adj.clear();memo.clear();
  auto add=[&](){adj.push_back(0);return (int)adj.size()-1;};
  auto link=[&](int a,int b){adj[a]|=1ULL<<b;adj[b]|=1ULL<<a;};
  for(int i=0;i<K;i++)add();
  for(int i=0;i<K;i++)for(int j=i+1;j<K;j++)link(i,j);
  for(int i=0;i<K;i++){int v=add();link(i,v);}
  for(int e=0;e<E;e++){
   int count=((mask>>e)&1)+(((doubled>>e)&1)?2:0);
   for(int r=0;r<count;r++){
    int v=add();link(v,edges[e].first);link(v,edges[e].second);
   }
  }
  if(adj.size()>63)abort();
  return sg((1ULL<<adj.size())-1);
 }
};
int main(){
 vector<pair<int,int>> edges;int ix[K][K];
 for(int i=0;i<K;i++)for(int j=i+1;j<K;j++){
  ix[i][j]=ix[j][i]=edges.size();edges.emplace_back(i,j);
 }
 int maps[K-1][E];
 for(int t=0;t<K-1;t++){
  int p[K];iota(p,p+K,0);swap(p[t],p[t+1]);
  for(int e=0;e<E;e++)
   maps[t][e]=ix[p[edges[e].first]][p[edges[e].second]];
 }
 vector<uint8_t> seen(FULL,0);vector<int> orbit;orbit.reserve(5040);
 Named solver;long long checked=0,covered=0;
 int classes=0,mismatches=0,max_states=0;
 for(int mask=0;mask<FULL;mask++){
  if(seen[mask])continue;
  orbit.clear();orbit.push_back(mask);seen[mask]=1;
  for(size_t h=0;h<orbit.size();h++){
   int x=orbit[h];
   for(int t=0;t<K-1;t++){
    int y=0;for(int e=0;e<E;e++)if((x>>e)&1)y|=1<<maps[t][e];
    if(!seen[y]){seen[y]=1;orbit.push_back(y);}
   }
  }
  classes++;covered+=orbit.size();
  int g=solver.value(mask,edges);
  vector<int> missing;
  for(int e=0;e<E;e++)if(!(mask>>e&1))missing.push_back(e);
  function<void(int,int,uint32_t)> check=
  [&](int start,int left,uint32_t doubled){
   if(left==0){
    checked++;
    int value=solver.value(mask,edges,doubled);
    max_states=max(max_states,(int)solver.memo.size());
    if(value!=g){
     mismatches++;
     cerr<<"FAIL mask="<<mask<<" doubled="<<doubled
         <<" expected="<<g<<" got="<<value<<"\n";
    }
    return;
   }
   for(int j=start;j<=(int)missing.size()-left;j++)
    check(j+1,left-1,doubled|(1u<<missing[j]));
  };
  if(missing.size()>=4)check(0,4,0);
 }
 cout<<"classes="<<classes<<" labeled="<<covered
     <<" checked4="<<checked<<" mismatches="<<mismatches
     <<" max_states="<<max_states<<"\n";
 return (classes!=1044||covered!=FULL||checked!=457353||mismatches)?1:0;
}
