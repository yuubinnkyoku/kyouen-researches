// Complete finite scan of unequal-capacity top-h occupancy games, six labeled columns.
// Identical-capacity columns are quotiented by permutation; mex is exact.
// Build: g++ -O3 -std=c++17 scan_six.cpp -o scan_six
// Run: ./scan_six 7
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
constexpr int W=6;
array<int,W> cap{},radix{};
int h, limit;
vector<int8_t> memo;
uint64_t visited;
int max_value;
array<int,W> max_root{};
int top_sum(const array<int,W>& x) {
  auto y=x;sort(y.begin(),y.end(),greater<int>());
  int s=0;for(int i=0;i<h;i++)s+=y[i];return s;
}
int sg(const array<int,W>& x, int idx) {
  if(memo[idx]!=-1)return memo[idx];
  unsigned mask=0;
  for(int i=0;i<W;i++) {
    if(x[i]==cap[i] || (i && cap[i]==cap[i-1] && x[i]==x[i-1]))continue;
    auto y=x; ++y[i];
    // Restore nondecreasing order within the identical-capacity block.
    for(int j=i;j+1<W && cap[j]==cap[j+1] && y[j]>y[j+1];j++)swap(y[j],y[j+1]);
    if(top_sum(y)>limit)continue;
    int child_idx=0;for(int j=0;j<W;j++)child_idx+=radix[j]*y[j];
    mask|=1u<<sg(y,child_idx);
  }
  int g=0;while(mask & (1u<<g))++g;
  memo[idx]=static_cast<int8_t>(g);
  ++visited;
  if(g>max_value){max_value=g;max_root=x;}
  return g;
}
int main(int argc,char**argv){
  const int maxcap=argc>1?atoi(argv[1]):7;
  if(maxcap<1||maxcap>12)return 2;
  uint64_t nconfigs=0, nstates=0;
  array<uint64_t,W+1> config_by_h{}, states_by_h{};
  array<int,W+1> max_by_h{};
  array<array<int,W>,W+1> witness_c{},witness_x{};
  array<int,W+1> witness_r{};
  array<int,W> c{};
  auto visit=[&](){
    cap=c;
    int prod=1;for(int i=0;i<W;i++){radix[i]=prod;prod*=cap[i]+1;}
    for(h=2;h<=5;h++){
      const int max_r=accumulate(cap.end()-h,cap.end(),0);
      // r=0,1 and r>=max_r are parity-only, hence have Grundy <=1.
      for(limit=2;limit<max_r;limit++){
        memo.assign(prod,-1);visited=0;max_value=0;
        const array<int,W> zero{};
        sg(zero,0);
        ++nconfigs; nstates+=visited;
        ++config_by_h[h];states_by_h[h]+=visited;
        if(max_value>max_by_h[h]){
          max_by_h[h]=max_value;witness_c[h]=cap;
          witness_x[h]=max_root;witness_r[h]=limit;
        }
        if(max_value>=6){
          cerr<<"COUNTEREXAMPLE g="<<max_value<<" h="<<h<<" r="<<limit<<" c=";
          for(auto v:cap)cerr<<v<<',';
          cerr<<" x=";for(auto v:max_root)cerr<<v<<',';
          cerr<<'\n';return false;
        }
      }
    }
    return true;
  };
  bool okay=true;
  auto enumerate=[&](auto&& self,int i,int mincap)->void {
    if(!okay)return;
    if(i==W){okay=visit();return;}
    for(int k=mincap;k<=maxcap;k++){c[i]=k;self(self,i+1,k);if(!okay)return;}
  };
  enumerate(enumerate,0,1);
  cout<<"cap_limit="<<maxcap<<"; column_count="<<W
      <<"; configurations="<<nconfigs<<"; canonical_states="<<nstates<<"\n";
  for(int j=2;j<=5;j++){
    cout<<"h="<<j<<"; configurations="<<config_by_h[j]
        <<"; canonical_states="<<states_by_h[j]<<"; max_g="<<max_by_h[j]
        <<"; example_cap=";
    for(auto v:witness_c[j])cout<<v<<',';
    cout<<"; example_r="<<witness_r[j]<<"; example_x=";
    for(auto v:witness_x[j])cout<<v<<',';
    cout<<'\n';
  }
  return okay?0:1;
}
