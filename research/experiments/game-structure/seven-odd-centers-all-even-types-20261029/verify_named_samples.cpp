// Independent named-vertex closed-neighborhood mex verifier.
// For each 7-center odd-edge orbit and d=7..21, checks the first and every
// 200th even-edge selection in lexicographic order. Not a full second enumeration.
#include <bits/stdc++.h>
using namespace std;
using U=uint64_t;
static constexpr int N=1<<21;
static constexpr long long expected[22]={
 0,0,0,0,0,0,0,9129,10073,9750,8215,6035,4005,2279,
 1141,487,173,53,15,5,2,1
};
vector<pair<int,int>> edges;
int idx[7][7],swmap[6][21];
uint32_t permute(uint32_t x,int t){
 uint32_t y=0;
 while(x){int b=__builtin_ctz(x);x&=x-1;y|=1u<<swmap[t][b];}
 return y;
}
vector<uint32_t> representatives(){
 vector<uint8_t>seen(N);vector<uint32_t>orbit,reps;
 for(uint32_t mask=0;mask<N;mask++){
  if(seen[mask])continue;
  orbit.clear();orbit.push_back(mask);seen[mask]=1;
  for(size_t j=0;j<orbit.size();j++)for(int t=0;t<6;t++){
   uint32_t x=permute(orbit[j],t);
   if(!seen[x]){seen[x]=1;orbit.push_back(x);}
  }
  reps.push_back(mask);
 }
 return reps;
}
struct Solver{
 U adj[56];int n=0;unordered_map<U,uint8_t>memo;
 void edge(int i,int j){adj[i]|=U(1)<<j;adj[j]|=U(1)<<i;}
 int solve(U state){
  int iso=0;U tmp=state;
  while(tmp){
   int v=__builtin_ctzll(tmp);tmp&=tmp-1;
   if(!(adj[v]&state)){iso^=1;state&=~(U(1)<<v);}
  }
  if(!state)return iso;
  auto it=memo.find(state);
  if(it!=memo.end())return it->second^iso;
  uint64_t opts=0;tmp=state;
  while(tmp){
   int v=__builtin_ctzll(tmp);tmp&=tmp-1;
   U child=state&~(adj[v]|(U(1)<<v));
   opts|=U(1)<<solve(child);
  }
  int g=__builtin_ctzll(~opts);
  memo.emplace(state,g);
  return g^iso;
 }
 int evaluate(uint32_t mask,const vector<int>&selected){
  n=14;fill(adj,adj+56,0);memo.clear();
  for(int i=0;i<7;i++)for(int j=i+1;j<7;j++)edge(i,j);
  for(int i=0;i<7;i++)edge(i,7+i);
  bool even[21]={};for(int x:selected)even[x]=true;
  for(int e=0;e<21;e++){
   int count=((mask>>e)&1)?1:even[e]?2:0;
   auto [i,j]=edges[e];
   while(count--){int v=n++;edge(i,v);edge(j,v);}
  }
  if(n>56)abort();
  return solve((U(1)<<n)-1);
 }
};
int main(){
 for(int i=0;i<7;i++)for(int j=i+1;j<7;j++){
  idx[i][j]=idx[j][i]=edges.size();edges.emplace_back(i,j);
 }
 for(int t=0;t<6;t++)for(int e=0;e<21;e++){
  auto [i,j]=edges[e];
  if(i==t)i=t+1;else if(i==t+1)i=t;
  if(j==t)j=t+1;else if(j==t+1)j=t;
  swmap[t][e]=idx[i][j];
 }
 auto reps=representatives();
 if(reps.size()!=1044)return 1;
 Solver solver;long long checked[22]={};
 for(auto mask:reps){
  vector<int>missing;
  for(int e=0;e<21;e++)if(!(mask>>e&1))missing.push_back(e);
  int base=solver.evaluate(mask,{});
  for(int d=7;d<=21;d++)if((int)missing.size()>=d){
   long long within=0;vector<int>selected;
   function<void(int,int)>rec=[&](int start,int left){
    if(!left){
     if(within%200==0){
      int g=solver.evaluate(mask,selected);checked[d]++;
      if(g!=base){cerr<<"FAIL mask="<<mask<<" d="<<d<<" got="<<g<<" base="<<base<<"\n";exit(1);}
     }
     within++;return;
    }
    for(int x=start;x<=(int)missing.size()-left;x++){
     selected.push_back(missing[x]);rec(x+1,left-1);selected.pop_back();
    }
   };
   rec(0,d);
  }
 }
 long long total=0;
 for(int d=7;d<=21;d++){
  cout<<"d="<<d<<" named_checked="<<checked[d]<<"\n";
  if(checked[d]!=expected[d])return 1;
  total+=checked[d];
 }
 cout<<"total="<<total<<" mismatches=0\n";
 return total==51363?0:1;
}
