// Independent named-vertex closed-neighborhood recursion; 5/6-type samples.
// Generates all 1,044 S7 orbit representatives and their exact base nimbers.
// Usage: g++ -O3 -std=c++17 verify_named_samples.cpp -o /tmp/seven-named-samples
//        /tmp/seven-named-samples /tmp/seven-representatives.tsv
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
int main(int argc,char**argv){
 if(argc!=2){cerr<<"usage: verify_named_samples representatives.tsv\n";return 2;}
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
 Named solver;long long checked[7]={},covered=0;
 int classes=0,mismatches=0,max_states=0;
 ofstream out(argv[1]);if(!out)return 2;
 out<<"mask\torbit\tg\tmissing_edges\n";
 auto comb=[](int n,int k)->uint64_t{
  uint64_t x=1;for(int i=1;i<=k;i++)x=x*(n-i+1)/i;return x;
 };
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
  int g=solver.value(mask,edges);checked[0]++;
  vector<int> missing;
  for(int e=0;e<E;e++)if(!(mask>>e&1))missing.push_back(e);
  uint64_t rank=0,total=0;
  function<void(int,int,uint32_t,int)> check=
  [&](int start,int left,uint32_t doubled,int count){
   if(left==0){
    uint64_t idx=rank++;
    if(idx!=0 && idx!=total/2 && idx!=total-1)return;
    checked[count]++;
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
    check(j+1,left-1,doubled|(1u<<missing[j]),count);
  };
  for(int d=5;d<=6;d++)if((int)missing.size()>=d){
   rank=0;total=comb((int)missing.size(),d);check(0,d,0,d);
  }
  out<<mask<<'\t'<<orbit.size()<<'\t'<<g<<'\t'<<missing.size()<<'\n';
 }
 cout<<"classes="<<classes<<" labeled="<<covered
     <<" sampled5="<<checked[5]<<" sampled6="<<checked[6]
     <<" mismatches="<<mismatches<<" max_states="<<max_states<<"\n";
 return (classes!=1044||covered!=FULL||checked[5]!=3033||
         checked[6]!=2930||mismatches)?1:0;
}
