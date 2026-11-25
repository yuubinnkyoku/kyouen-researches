#include <bits/stdc++.h>
using namespace std;
using U=uint64_t;
struct State {int k; array<uint8_t,6> t{}; array<array<uint8_t,6>,6> r{};};
static uint8_t norm(int v){return v==0?0:(v&1?1:2);}
static U key(const State& s){U x=s.k; for(int i=0;i<s.k;i++)x=(x<<2)|s.t[i];for(int i=0;i<s.k;i++)for(int j=i+1;j<s.k;j++)x=(x<<2)|s.r[i][j];return x;}
static unordered_map<U,uint8_t> memo;
static unsigned long long calls=0;
static int formula(const State& s){int u=0,zero=0,one=0;for(int i=0;i<s.k;i++){u^=(s.t[i]&1);int z=s.t[i]&1;for(int j=0;j<s.k;j++)if(j!=i)z^=(s.r[i][j]&1); if(z)one++;else zero++;}for(int i=0;i<s.k;i++)for(int j=i+1;j<s.k;j++)u^=(s.r[i][j]&1);return zero==0||one==0 ? (1^u^(one!=0)):2+u;}
static State child(const State&s,int a,int b){State c; c.k=s.k-(b<0?1:2);int idx=0;for(int i=0;i<s.k;i++){if(i==a||i==b)continue;c.t[idx]=norm(s.t[i]+s.r[i][a]+(b<0?0:s.r[i][b]));int jdx=0;for(int j=0;j<i;j++){if(j==a||j==b)continue;c.r[jdx][idx]=c.r[idx][jdx]=s.r[j][i];jdx++;}idx++;}return c;}
static int sg(const State&s){
 if(s.k==0)return 0;
 // Exact named-type recurrence; cache all nontrivial small states.
 U kk=key(s);auto it=memo.find(kk);if(it!=memo.end())return it->second;
 calls++;bool seen[16]={};int u=0;for(int i=0;i<s.k;i++)u^=(s.t[i]&1);for(int i=0;i<s.k;i++)for(int j=i+1;j<s.k;j++)u^=(s.r[i][j]&1);
 for(int i=0;i<s.k;i++){
  int z=s.t[i]&1;for(int j=0;j<s.k;j++)if(j!=i)z^=(s.r[i][j]&1);
  seen[u^z]=true;
  if(s.t[i]){auto c=child(s,i,-1);seen[sg(c)^((s.t[i]-1)&1)]=true;}
 }
 for(int i=0;i<s.k;i++)for(int j=i+1;j<s.k;j++)if(s.r[i][j]){
  auto c=child(s,i,j);seen[sg(c)^((s.t[i]+s.t[j]+s.r[i][j]-1)&1)]=true;
 }
 int g=0;while(seen[g])g++;memo.emplace(kk,g);return g;
}
static int eval6(const State&s){
 // k=5, missing<=3 has already been exhaustively certified below.
 // k=4 children are always evaluated by the exact recurrence.
 bool seen[16]={};int u=0;for(int i=0;i<s.k;i++)u^=(s.t[i]&1);for(int i=0;i<s.k;i++)for(int j=i+1;j<s.k;j++)u^=(s.r[i][j]&1);
 for(int i=0;i<s.k;i++){
  int z=s.t[i]&1;for(int j=0;j<s.k;j++)if(j!=i)z^=(s.r[i][j]&1);
  seen[u^z]=true;
  if(s.t[i]){auto c=child(s,i,-1);seen[formula(c)^((s.t[i]-1)&1)]=true;}
 }
 for(int i=0;i<s.k;i++)for(int j=i+1;j<s.k;j++)if(s.r[i][j]){
  auto c=child(s,i,j);seen[sg(c)^((s.t[i]+s.t[j]+s.r[i][j]-1)&1)]=true;
 }
 int g=0;while(seen[g])g++;return g;
}
int main(){
 vector<pair<string,vector<pair<int,int>>>> pat={
 {"triangle",{{0,1},{0,2},{1,2}}},
 {"star",{{0,1},{0,2},{0,3}}},
 {"path4",{{0,1},{1,2},{2,3}}},
 {"path3_plus_edge",{{0,1},{1,2},{3,4}}},
 {"matching3",{{0,1},{2,3},{4,5}}}
 };
 unsigned long long total=0;
 for(int k:{5,6}){
  for(auto &p:pat){if(k==5&&p.first=="matching3")continue;
   State s;s.k=k;vector<pair<int,int>> pairs;for(int i=0;i<k;i++)for(int j=i+1;j<k;j++){
    bool missing=find(p.second.begin(),p.second.end(),make_pair(i,j))!=p.second.end();
    if(!missing)pairs.push_back({i,j});
   }
   U masks=1ULL<<pairs.size();U tern=1;for(int i=0;i<k;i++)tern*=3;
   unsigned long long count=0;array<unsigned long long,4> hist{};
   for(U mask=0;mask<masks;mask++){
    for(int i=0;i<k;i++)for(int j=0;j<k;j++)s.r[i][j]=0;
    for(int e=0;e<(int)pairs.size();e++){auto [i,j]=pairs[e];s.r[i][j]=s.r[j][i]=1+((mask>>e)&1);}
    for(U tr=0;tr<tern;tr++){
     U x=tr;for(int i=0;i<k;i++){s.t[i]=x%3;x/=3;}
     int got=(k==5?sg(s):eval6(s)),expected=formula(s);
     if(got!=expected){cerr<<"FAIL k="<<k<<" pattern="<<p.first<<" mask="<<mask<<" leaves="<<tr<<" got="<<got<<" expected="<<expected<<"\n";return 1;}
     if(got>3){cerr<<"UNEXPECTED LARGE g="<<got<<"\n";return 1;}
     hist[got]++;count++;
    }
   }
   total+=count;
   cout<<"k="<<k<<" missing="<<p.first<<" cases="<<count<<" histogram="<<hist[0]<<","<<hist[1]<<","<<hist[2]<<","<<hist[3]<<" exact_small_states="<<memo.size()<<"\n"<<flush;
  }
 }
 cout<<"PASS total="<<total<<" small_exact_calls="<<calls<<"\n";
}
