// Exhaustive three-state signature census for a fixed g=7 split graph
// extended by one clique vertex and independent vertices incident to it.
#include <array>
#include <cassert>
#include <iostream>
#include <vector>
using namespace std;
constexpr int K=8, N=1<<K;
constexpr array<int,13> BASE={3,3,5,9,9,20,20,32,36,36,48,65,65};
constexpr array<int,8> EXT={128,129,130,132,136,144,160,192};
struct Answer {int grundy; unsigned long long options;};
Answer solve(const array<int,256>& multiplicity){
  vector<int> signatures;
  int degpar[K]={};
  for(int s=1;s<N;s++) if(multiplicity[s]){
    signatures.push_back(s);
    if(multiplicity[s]&1) for(int c=0;c<K;c++)
      if(s&(1<<c)) degpar[c]^=1;
  }
  int activepar[N]={},g[N]={};
  for(int x=1;x<N;x++){
    for(int s:signatures) if(s&x) activepar[x]^=(multiplicity[s]&1);
    unsigned long long children=0;
    for(int c=0;c<K;c++) if(x&(1<<c))
      children|=1ULL<<(activepar[x]^degpar[c]);
    for(int s:signatures) if(s&x){
      int y=x&~s;
      int child=g[y]^activepar[x]^activepar[y]^1;
      assert(child<63);
      children|=1ULL<<child;
    }
    g[x]=__builtin_ctzll(~children);
  }
  unsigned long long options=0;
  for(int c=0;c<K;c++) options|=1ULL<<(activepar[N-1]^degpar[c]);
  for(int s:signatures){
    int y=(N-1)&~s;
    int child=g[y]^activepar[N-1]^activepar[y]^1;
    options|=1ULL<<child;
  }
  return {g[N-1],options};
}
int main(){
  array<int,256> counts{};
  for(int s:BASE)counts[s]++;
  array<int,12> histogram{};
  int has7=0,has6and7=0;
  for(int code=0;code<6561;code++){
    int digits=code;
    for(int s:EXT){counts[s]=digits%3;digits/=3;}
    assert(digits==0);
    auto r=solve(counts);
    assert(r.grundy<12);
    histogram[r.grundy]++;
    if(r.options&(1ULL<<7)){
      has7++;
      if(r.options&(1ULL<<6))has6and7++;
    }
  }
  assert((histogram==array<int,12>{24,0,3257,3191,24,18,8,39,0,0,0,0}));
  assert(has7==44 && has6and7==0);
  cout<<"histogram:";
  for(int v:histogram)cout<<' '<<v;
  cout<<"\nchild7="<<has7<<" child6_and_7="<<has6and7<<"\n";
}
