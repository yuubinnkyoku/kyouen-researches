#include <bits/stdc++.h>
using namespace std;

// Independent named-vertex Node Kayles verifier, not the clique-mask recurrence.
struct Graph {
 int n=0,k; vector<uint64_t> closed;
 Graph(int k_): k(k_) {for(int i=0;i<k;i++)closed.push_back((1ULL<<k)-1);n=k;}
 void add(int sig) {uint64_t b=1ULL<<n;closed.push_back(b | (uint64_t)sig);for(int i=0;i<k;i++)if(sig>>i&1)closed[i]|=b; n++;}
};
struct Direct {
 const Graph &g; unordered_map<uint64_t,unsigned char> memo;
 Direct(const Graph &gg):g(gg){memo.reserve(128);}
 int solve(uint64_t m){
  if(!m)return 0;
  // Strip isolated vertices; isolated Node Kayles vertices xor their parity.
  uint64_t isolated=0;
  for(uint64_t t=m;t;t&=t-1){int v=__builtin_ctzll(t);if(!(g.closed[v]&m&~(1ULL<<v)))isolated|=1ULL<<v;}
  if(isolated)return (__builtin_popcountll(isolated)&1)^solve(m&~isolated);
  auto it=memo.find(m);if(it!=memo.end())return it->second;
  unsigned seen=0;
  for(uint64_t t=m;t;t&=t-1){int v=__builtin_ctzll(t);seen|=1u<<solve(m&~g.closed[v]);}
  int ans=0;while(seen&(1u<<ans))ans++;
  memo.emplace(m,ans);return ans;
 }
};

int main(){
 long long total=0, directStates=0; int maxg=0;long long dist[4]={};
 for(int k:{4,5})for(int pattern=0;pattern<3;pattern++){
  vector<pair<int,int>> missing={{0,1}};
  if(pattern==1)missing.emplace_back(0,2);
  if(pattern==2)missing.emplace_back(2,3);
  vector<pair<int,int>> pairs;
  for(int i=0;i<k;i++)for(int j=i+1;j<k;j++){
   if(find(missing.begin(),missing.end(),make_pair(i,j))==missing.end())pairs.emplace_back(i,j);
  }
  int rp=1<<pairs.size();int tp=1;for(int i=0;i<k;i++)tp*=3;
  for(int rmask=0;rmask<rp;rmask++)for(int tmask=0;tmask<tp;tmask++){
   int t=tmask,u=0;vector<int> z(k,0);
   Graph graph(k);
   for(int j=0;j<(int)pairs.size();j++){
    auto [a,b]=pairs[j];int mult=1+((rmask>>j)&1);
    u^=(mult&1);z[a]^=(mult&1);z[b]^=(mult&1);
    for(int v=0;v<mult;v++)graph.add((1<<a)|(1<<b));
   }
   for(int i=0;i<k;i++){
    int mult=t%3;t/=3;u^=(mult&1);z[i]^=(mult&1);
    for(int v=0;v<mult;v++)graph.add(1<<i);
   }
   bool uniform=all_of(z.begin(),z.end(),[&](int a){return a==z[0];});
   int expected=uniform?(1^u^z[0]):2+u;
   Direct direct(graph);
   int got=direct.solve((1ULL<<graph.n)-1);
   if(got!=expected){cerr<<"MISMATCH k="<<k<<" pattern="<<pattern<<" r="<<rmask<<" t="<<tmask<<" got="<<got<<" expected="<<expected<<"\n";return 1;}
   if(got>3){cerr<<"OUT OF RANGE\n";return 1;}
   dist[got]++;total++;maxg=max(maxg,got);directStates+=direct.memo.size();
  }
  cerr<<"OK k="<<k<<" pattern="<<pattern<<" cases="<<rp*tp<<" total="<<total<<" states="<<directStates<<"\n";
 }
 cout<<"ALL_OK cases="<<total<<" max_g="<<maxg<<" distribution="<<dist[0]<<","<<dist[1]<<","<<dist[2]<<","<<dist[3]<<" direct_memo_states="<<directStates<<"\n";
}