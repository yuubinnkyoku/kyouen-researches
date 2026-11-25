// Independent audit: occupancy-count DAG, no explicit forbidden transversals.
#include <bits/stdc++.h>
using namespace std;
struct Check {
 int k; vector<int> sz,edge,mult,dp,core; long long safe_states=0,terminal=0; int root=0;
 Check(int kk, vector<int> sizes, vector<int> edges):k(kk),sz(move(sizes)),edge(move(edges)){}
 bool safe(int A) const {for(int e:edge) if((A&e)==e) return false; return true;}
 int mex(const vector<int>& vals) const {int m=0; while(find(vals.begin(),vals.end(),m)!=vals.end()) ++m;return m;}
 int f(int A){int &ret=core[A]; if(ret>=0)return ret;vector<int> ch;
  for(int i=0;i<k;i++)if(!(A>>i&1)&&safe(A|(1<<i)))ch.push_back(((sz[i]-1)&1)^f(A|(1<<i)));
  return ret=mex(ch);
 }
 int dfs(int key){int &ret=dp[key];if(ret>=0)return ret;int A=0,free=0;vector<int>ch;
  for(int i=0;i<k;i++){
   int c=(key/mult[i])%(sz[i]+1);
   if(c)A|=1<<i,free+=(sz[i]-c);
  }
  if(!safe(A))return ret=-2;
  for(int i=0;i<k;i++){
   int c=(key/mult[i])%(sz[i]+1);
   if(c<sz[i] && safe(A|(1<<i)))ch.push_back(dfs(key+mult[i]));
  }
  ret=mex(ch);
  if(ret!=((free&1)^f(A))) {cerr<<"MISMATCH key="<<key<<" g="<<ret<<" expected="<<((free&1)^f(A))<<"\n";exit(1);}
  ++safe_states;if(ch.empty())++terminal;
  return ret;
 }
 void run(){mult.assign(k,1);int N=1;for(int i=0;i<k;i++){mult[i]=N;N*=sz[i]+1;}dp.assign(N,-1);core.assign(1<<k,-1);root=dfs(0);
  // Need visit all safe count states, including ones unreachable from empty? all safe states reachable.
  for(int j=0;j<N;j++){
   int A=0;for(int i=0;i<k;i++)if((j/mult[i])%(sz[i]+1))A|=1<<i;
   if(safe(A)&&dp[j]<0){cerr<<"missed reachable safe state\n";exit(1);}
  }
  long long expect=0;
  for(int A=0;A<(1<<k);A++)if(safe(A)){
   bool maximal=true;for(int i=0;i<k;i++)if(!(A>>i&1)&&safe(A|(1<<i)))maximal=false;
   if(maximal)expect++;
  }
  if(expect!=terminal){cerr<<"terminal mismatch "<<expect<<" "<<terminal<<"\n";exit(1);}
 }
};
int main(){long long cases=0,states=0,terminal=0;map<int,long long>hist;
 for(int k=2;k<=4;k++){
  vector<int> elig;for(int e=1;e<(1<<k);e++)if(__builtin_popcount((unsigned)e)>=2)elig.push_back(e);
  int size_options=(k<=3)?3:2;
  int num_sizes=1;for(int i=0;i<k;i++)num_sizes*=size_options;
  for(int sc=0;sc<num_sizes;sc++){
   vector<int>sz(k);int t=sc;for(int i=0;i<k;i++)sz[i]=1+t%size_options,t/=size_options;
   for(int mask=0;mask<(1<<(int)elig.size());mask++){
    vector<int> edges;for(int i=0;i<(int)elig.size();i++)if(mask>>i&1)edges.push_back(elig[i]);
    Check c{k,sz,edges};c.run();cases++;states+=c.safe_states;terminal+=c.terminal;hist[c.root]++;
   }
  }
 }
 // Additional deterministic pseudorandom cases with k=5, unlike Python's generator.
 mt19937 rng(20261019);for(int i=0;i<1000;i++){
  int k=5;vector<int>sz(k);for(int j=0;j<k;j++)sz[j]=1+(rng()%3);
  vector<int> edges;for(int e=1;e<(1<<k);e++)if(__builtin_popcount((unsigned)e)>=2 && rng()%5==0)edges.push_back(e);
  Check c{k,sz,edges};c.run();cases++;states+=c.safe_states;terminal+=c.terminal;hist[c.root]++;
 }
 cout<<"{\"cases\":"<<cases<<",\"safe_count_states\":"<<states<<",\"maximal_count_states\":"<<terminal<<",\"root_histogram\":{";
 bool first=true;for(auto [g,c]:hist){if(!first)cout<<",";first=false;cout<<"\""<<g<<"\":"<<c;}cout<<"},\"status\":\"all matched\"}\n";
}
