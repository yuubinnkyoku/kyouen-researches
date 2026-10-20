// Independent C++ verification of the strong-core terminal-spectrum formula.
// g++ -std=c++17 -O2 strong_core_terminal_independent.cpp -o audit && ./audit
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <random>
#include <set>
#include <vector>
using namespace std;

static bool legal(int s, const vector<int>& h) {
  for (int e : h) if ((s & e) == e) return false;
  return true;
}

static map<int,int> full_enumeration(int n, const vector<int>& h) {
  map<int,int> out;
  for (int s=0;s<(1<<n);s++) {
    if (!legal(s,h)) continue;
    bool terminal=true;
    for(int i=0;i<n;i++) if (!(s&(1<<i)) && legal(s|(1<<i),h)) {terminal=false;break;}
    if(terminal) out[__builtin_popcount((unsigned)s)]++;
  }
  return out;
}

static map<int,int> core_enumeration(int n, const vector<int>& h, int core) {
  int outside=((1<<n)-1)^core;
  for(int e:h) assert(__builtin_popcount((unsigned)(e&outside))<=1);
  map<int,int> out;
  for(int a=core;;a=(a-1)&core) {
    if(legal(a,h)) {
      int b=0;
      for(int i=0;i<n;i++) if((outside&(1<<i)) && legal(a|(1<<i),h)) b|=1<<i;
      int t=a|b;
      bool terminal=true;
      for(int i=0;i<n;i++) if(!(t&(1<<i)) && legal(t|(1<<i),h)) {terminal=false;break;}
      if(terminal) {assert(legal(t,h));out[__builtin_popcount((unsigned)t)]++;}
    }
    if(!a) break;
  }
  return out;
}

int main(){
  long long exhaustive=0, random_checks=0;
  for(int n=0;n<=4;n++){
    vector<int> possible;
    for(int h=1;h<(1<<n);h++) if(__builtin_popcount((unsigned)h)>=2) possible.push_back(h);
    for(int bits=0;bits<(1<<(int)possible.size());bits++) {
      vector<int> edges;
      for(int j=0;j<(int)possible.size();j++) if(bits&(1<<j)) edges.push_back(possible[j]);
      auto want=full_enumeration(n,edges);
      for(int c=0;c<(1<<n);c++) {
        bool ok=true;
        for(int e:edges) if(__builtin_popcount((unsigned)(e&(((1<<n)-1)^c)))>1) ok=false;
        if(ok) {assert(core_enumeration(n,edges,c)==want);exhaustive++;}
      }
    }
  }
  mt19937 rng(20261019);
  for(int n=1;n<=9;n++) for(int z=0;z<600;z++) {
    int c=(int)(rng()%(1u<<n));
    vector<int> edges;
    for(int h=1;h<(1<<n);h++) if(__builtin_popcount((unsigned)(h&(((1<<n)-1)^c)))<=1)
      if(rng()%11==0) edges.push_back(h);
    assert(core_enumeration(n,edges,c)==full_enumeration(n,edges));
    random_checks++;
  }
  cout<<"exhaustive="<<exhaustive<<" random="<<random_checks<<" PASS\n";
}
