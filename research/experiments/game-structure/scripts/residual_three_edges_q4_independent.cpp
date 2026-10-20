// Independent exhaustive bit-mask verifier: three minimal residual hyperedges of size <= 4.
// Vertices are distinct bits; all safe subsets are evaluated in descending order.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <vector>
using namespace std;
static constexpr int CAP=4;
int k; vector<int> counts;
long long families; map<int,int> root_hist,max_hist,by_n;

void evaluate(){
  const int types=(1<<k)-1;
  int edge_size[3]={};
  for(int t=1;t<=types;t++)for(int i=0;i<k;i++)if(t&(1<<i))edge_size[i]+=counts[t-1];
  for(int i=0;i<k;i++)if(edge_size[i]<1||edge_size[i]>CAP)return;
  for(int i=0;i<k;i++)for(int j=0;j<k;j++)if(i!=j){
    bool private_vertex=false;
    for(int t=1;t<=types;t++)if((t&(1<<i))&&!(t&(1<<j))&&counts[t-1])private_vertex=true;
    if(!private_vertex)return;
  }
  array<uint16_t,3> edges{};
  int n=0;
  for(int t=1;t<=types;t++)for(int r=0;r<counts[t-1];r++){
    for(int i=0;i<k;i++)if(t&(1<<i))edges[i]|=uint16_t(1)<<n;
    n++;
  }
  assert(n<=12);
  const int limit=1<<n;
  vector<int8_t> grundy(limit,-1);
  int local_max=0;
  for(int s=limit-1;s>=0;s--){
    bool safe=true;
    for(int i=0;i<k;i++)if((s&edges[i])==edges[i]){safe=false;break;}
    if(!safe)continue;
    unsigned child_values=0;
    for(int i=0;i<n;i++)if(!(s&(1<<i))){
      int g=grundy[s|(1<<i)];
      if(g>=0)child_values|=1u<<g;
    }
    int g=0;
    while(child_values&(1u<<g))g++;
    grundy[s]=g;
    local_max=max(local_max,g);
  }
  families++;root_hist[grundy[0]]++;max_hist[local_max]++;by_n[n]++;
}
void gen(int t){
  if(t==(int)counts.size()){evaluate();return;}
  for(int c=0;c<=CAP;c++){counts[t]=c;gen(t+1);}
}
void counterexample(const vector<int>& edges,int n,int expected,const vector<int>& child_expected){
  vector<int8_t> g(1<<n,-1);
  for(int s=(1<<n)-1;s>=0;s--){
    bool safe=true;
    for(int e:edges)if((s&e)==e){safe=false;break;}
    if(!safe)continue;
    unsigned values=0;
    for(int i=0;i<n;i++)if(!(s&(1<<i))&&g[s|(1<<i)]>=0)values|=1u<<g[s|(1<<i)];
    int v=0;while(values&(1u<<v))v++;
    g[s]=v;
  }
  assert(g[0]==expected);
  for(int i=0;i<n;i++)assert(g[1<<i]==child_expected[i]);
  cout<<"counterexample n="<<n<<" root="<<int(g[0])<<" child=";
  for(int i=0;i<n;i++)cout<<int(g[1<<i])<<",";
  cout<<"\n";
}
int main(){
  counterexample({0x6a,0x73,0x7c},7,4,{3,1,3,1,2,0,0});
  counterexample({0xd2,0xe3,0xfc},8,5,{2,0,4,4,0,3,1,1});
  for(k=1;k<=3;k++){
    counts.assign((1<<k)-1,0);
    families=0;root_hist.clear();max_hist.clear();by_n.clear();
    gen(0);
    cout<<"k="<<k<<" families="<<families<<" root=";
    for(auto [v,num]:root_hist)cout<<v<<":"<<num<<",";
    cout<<" max=";
    for(auto [v,num]:max_hist)cout<<v<<":"<<num<<",";
    cout<<" by_n=";
    for(auto [v,num]:by_n)cout<<v<<":"<<num<<",";
    cout<<"\n";
  }
}
