// Independent verifier for four distinct forbidden 4-sets.
// Uses counts of *unplayed* vertices by incidence type, not vertex bit masks.
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <unordered_map>
using namespace std;

using A = array<int,15>;
A initial{}, state{};
array<int,4> caps{{4,4,4,4}};
map<int, map<int,long long>> root_hist, max_hist;
map<int,long long> patterns;
map<int,long long> all_patterns;
map<int, map<int,long long>> all_root_hist, all_max_hist;

bool distinct_edges() {
  for(int i=0;i<4;i++)for(int j=0;j<i;j++) {
    bool diff=false;
    for(int t=1;t<=15;t++)if(initial[t-1]>0 && (((t>>i)&1)!=((t>>j)&1))) {diff=true;break;}
    if(!diff)return false;
  }
  return true;
}

struct Game {
  unordered_map<uint64_t, unsigned char> memo;
  int maximum=0;
  static uint64_t pack(const A& a) {
    uint64_t z=0;
    for(int i=0;i<15;i++) z |= uint64_t(a[i]) << (3*i);
    return z;
  }
  int grundy(A &x, array<int,4>& rem) {
    uint64_t key=pack(x);
    auto it=memo.find(key);
    if(it!=memo.end())return it->second;
    unsigned int seen=0;
    for(int t=1;t<=15;t++)if(x[t-1]>0) {
      bool legal=true;
      for(int j=0;j<4;j++)if((t>>j)&1) {
        --rem[j];
        if(rem[j]==0)legal=false;
      }
      --x[t-1];
      if(legal) seen |= 1u << grundy(x,rem);
      ++x[t-1];
      for(int j=0;j<4;j++)if((t>>j)&1)++rem[j];
    }
    int g=0;
    while(seen&(1u<<g))++g;
    memo[key]=g;
    if(g>maximum)maximum=g;
    return g;
  }
};

void rec(int t,int n) {
  if(t==16) {
    if(caps != array<int,4>{{0,0,0,0}})return;
    Game game;
    A x=initial;
    array<int,4> rem{{4,4,4,4}};
    int g=game.grundy(x,rem);
    ++all_patterns[n]; ++all_root_hist[n][g]; ++all_max_hist[n][game.maximum];
    if(distinct_edges()) {++patterns[n]; ++root_hist[n][g]; ++max_hist[n][game.maximum];}
    return;
  }
  int lim=4;
  for(int j=0;j<4;j++)if((t>>j)&1)lim=min(lim,caps[j]);
  for(int c=0;c<=lim;c++) {
    initial[t-1]=c;
    for(int j=0;j<4;j++)if((t>>j)&1)caps[j]-=c;
    rec(t+1,n+c);
    for(int j=0;j<4;j++)if((t>>j)&1)caps[j]+=c;
  }
  initial[t-1]=0;
}

int main() {
  rec(1,0);
  for(auto [n,total]:all_patterns) {
    cout<<"all "<<n<<" "<<total<<" root";
    for(auto [g,c]:all_root_hist[n])cout<<" "<<g<<":"<<c;
    cout<<" max";
    for(auto [g,c]:all_max_hist[n])cout<<" "<<g<<":"<<c;
    cout<<"\n";
  }
  for(auto [n,total]:patterns) {
    cout<<n<<" "<<total<<" root";
    for(auto [g,c]:root_hist[n])cout<<" "<<g<<":"<<c;
    cout<<" max";
    for(auto [g,c]:max_hist[n])cout<<" "<<g<<":"<<c;
    cout<<"\n";
  }
}
