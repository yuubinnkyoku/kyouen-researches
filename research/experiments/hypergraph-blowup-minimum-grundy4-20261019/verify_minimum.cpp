// Complete antichain enumeration of all minimal forbidden hypergraphs on n<=5 vertices.
// Direct labelled-subset Sprague-Grundy DP, independent of group quotient recurrence.
#include <bits/stdc++.h>
using namespace std;
struct Enumerator {
 int n;vector<int> edge;vector<uint64_t> comparable;map<int,uint64_t> hist;
 uint64_t families=0;
 explicit Enumerator(int nn):n(nn){
  for(int s=1;s<(1<<n);s++)if(__builtin_popcount((unsigned)s)>=2)edge.push_back(s);
  for(int a:edge){uint64_t m=0;for(int j=0;j<(int)edge.size();j++){
   int b=edge[j];if((a&b)==a || (a&b)==b)m|=1ULL<<j;
  }comparable.push_back(m);}
 }
 int root(const vector<int>& chosen){
  vector<int> g(1<<n,0);
  for(int s=(1<<n)-1;s>=0;s--){
   bool safe=true;for(int e:chosen)if((s&e)==e){safe=false;break;}
   if(!safe)continue;
   unsigned child=0;
   for(int i=0;i<n;i++)if(!(s>>i&1)){
    int t=s|(1<<i);bool ok=true;for(int e:chosen)if((t&e)==e){ok=false;break;}
    if(ok)child|=1U<<g[t];
   }
   while(child&(1U<<g[s]))++g[s];
  }
  return g[0];
 }
 void dfs(uint64_t rem,vector<int>& chosen){
  if(!rem){++families;++hist[root(chosen)];return;}
  int i=__builtin_ctzll(rem);
  dfs(rem&~(1ULL<<i),chosen);
  chosen.push_back(edge[i]);dfs(rem&~comparable[i],chosen);chosen.pop_back();
 }
 void run(){vector<int> chosen;dfs((1ULL<<edge.size())-1,chosen);}
};
int main(){
 cout<<"{\"exhaustive_by_n\":{";
 for(int n=1;n<=5;n++){
  Enumerator e(n);e.run();if(n>1)cout<<",";
  cout<<"\""<<n<<"\":{\"antichains\":"<<e.families<<",\"root_histogram\":{";
  bool first=true;for(auto [g,c]:e.hist){if(!first)cout<<",";first=false;cout<<"\""<<g<<"\":"<<c;}
  cout<<"}}";
  if(e.hist.rbegin()->first>3){cerr<<"n<=5 bound failed\n";return 1;}
 }
 // n=6 witness: group sizes (1,1,1,1,2), base forbidden groups
 // {0,1},{0,2},{1,4},{2,3,4}, expanded to six point masks.
 vector<int> witness={(1<<0)|(1<<1),(1<<0)|(1<<2),(1<<1)|(1<<4),
 (1<<1)|(1<<5),(1<<2)|(1<<3)|(1<<4),(1<<2)|(1<<3)|(1<<5)};
 Enumerator e(6);int g=e.root(witness);
 if(g!=4){cerr<<"witness failed\n";return 1;}
 cout<<"},\"six_vertex_witness_grundy\":"<<g<<",\"status\":\"all exhaustive antichains checked\"}\n";
}
