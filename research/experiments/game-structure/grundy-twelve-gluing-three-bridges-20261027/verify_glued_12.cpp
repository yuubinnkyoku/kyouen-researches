// Exhaustive audit of the one-vertex gluing H8 vee H4 with <=3 cross edges,
// conditional on independence number >=12. No external dependencies.
// g is Node Kayles: g(G)=mex{g(G-N[v])}.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
using Edge=pair<int,int>;
static const vector<Edge> E8={{0,2},{0,7},{0,8},{0,9},{1,3},{1,4},{1,5},{1,7},{2,4},{2,5},{2,7},{3,4},{3,6},{4,11},{8,11},{10,11},{11,12}};
static const vector<Edge> E4={{0,3},{0,6},{1,4},{1,5},{1,6},{2,3},{2,4},{2,5},{2,6}};
static uint16_t seen[1<<19];
static uint8_t values[1<<19];
static uint16_t epoch=0;
static int grundy(const array<uint32_t,19>& adj){
  ++epoch;
  if(!epoch){fill(begin(seen),end(seen),0);++epoch;}
  auto rec=[&](auto&& self,uint32_t mask)->int{
    if(!mask)return 0;
    if(seen[mask]==epoch)return values[mask];
    uint32_t outcomes=0,rest=mask;
    while(rest){int v=__builtin_ctz(rest);rest&=rest-1;
      int child=self(self,mask&~(adj[v]|(1u<<v)));
      assert(child<32);outcomes|=1u<<child;
    }
    int result=__builtin_ctz(~outcomes);
    seen[mask]=epoch;values[mask]=result;return result;
  };
  return rec(rec,(1u<<19)-1);
}
static void add(array<uint32_t,19>& a,int x,int y){assert(x!=y);a[x]|=1u<<y;a[y]|=1u<<x;}
int main(){
  array<long long,32> histogram{};
  array<array<long long,32>,4> by_bridge{};
  array<long long,4> cases_by_bridges{};
  int alpha12_gluings=0,other_gluings=0,max_g=-1;
  vector<Edge> best_edges;
  for(int u=0;u<13;u++)for(int v=0;v<7;v++){
    array<int,7> mapped{};int next=13;
    for(int k=0;k<7;k++)mapped[k]=(k==v?u:next++);
    assert(next==19);
    array<uint32_t,19> base{};
    for(auto [a,b]:E8)add(base,a,b);
    for(auto [a,b]:E4)add(base,mapped[a],mapped[b]);
    // A 12-independent set in the gluing must be a 12-subset of 19 vertices.
    vector<uint32_t> independent12;
    for(uint32_t s=0;s<(1u<<19);s++){
      if(__builtin_popcount(s)!=12)continue;
      bool independent=true;
      for(uint32_t t=s;t;t&=t-1){int k=__builtin_ctz(t);
        if(base[k]&s){independent=false;break;}
      }
      if(independent)independent12.push_back(s);
    }
    if(independent12.empty()){other_gluings++;continue;}
    alpha12_gluings++;
    assert(independent12.size()==1); // verified for these specific H8 and H4
    uint32_t independent=independent12[0];
    vector<Edge> bridges;
    // A bridge has endpoints in the two EXCLUSIVE vertex sets.
    for(int a=0;a<13;a++)if(a!=u)
      for(int b=13;b<19;b++){
        // The unique 12-set must remain independent.
        if((independent&(1u<<a))&&(independent&(1u<<b)))continue;
        assert(!(base[a]&(1u<<b)));
        bridges.emplace_back(a,b);
      }
    assert(bridges.size()==40);
    auto audit=[&](const vector<int>& selected){
      auto graph=base;
      for(int k:selected)add(graph,bridges[k].first,bridges[k].second);
      int g=grundy(graph);
      histogram[g]++;by_bridge[selected.size()][g]++;cases_by_bridges[selected.size()]++;
      if(g>max_g){max_g=g;best_edges.clear();for(int a=0;a<19;a++)for(int b=a+1;b<19;b++)if(graph[a]&(1u<<b))best_edges.emplace_back(a,b);}
    };
    audit({});
    for(int a=0;a<40;a++)audit({a});
    for(int a=0;a<40;a++)for(int b=a+1;b<40;b++)audit({a,b});
    for(int a=0;a<40;a++)for(int b=a+1;b<40;b++)for(int c=b+1;c<40;c++)audit({a,b,c});
  }
  assert(alpha12_gluings==15&&other_gluings==76);
  assert(cases_by_bridges[0]==15);
  assert(cases_by_bridges[1]==600);
  assert(cases_by_bridges[2]==11700);
  assert(cases_by_bridges[3]==148200);
  assert(max_g<=10); // tested assertion, not assumed in generation
  cout<<"gluings_alpha12="<<alpha12_gluings<<" gluings_alpha_le11="<<other_gluings<<"\n";
  cout<<"cases_by_bridges=";for(auto n:cases_by_bridges)cout<<n<<" ";cout<<"\n";
  cout<<"histogram=";for(int k=0;k<=max_g;k++)cout<<k<<":"<<histogram[k]<<" ";cout<<"\n";
  for(int t=0;t<4;t++){cout<<"histogram_bridges_"<<t<<"=";for(int k=0;k<=max_g;k++)cout<<k<<":"<<by_bridge[t][k]<<" ";cout<<"\n";}
  cout<<"max_g="<<max_g<<" example_edges=";
  for(auto [a,b]:best_edges)cout<<"("<<a<<","<<b<<")";
  cout<<"\n";
}
