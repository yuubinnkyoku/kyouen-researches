// Exact two-layer direction-set census. Independent of determinant_audit.cpp.
#include <bits/stdc++.h>
using namespace std;
using U=uint64_t;
struct Option { U mask; vector<pair<int,int>> dirs; bool collinear; };
void check(int k,int m) {
  int n=k*m, N=2*n;
  vector<Option> options[4];
  for(int mask=0;mask<(1<<n);++mask) {
    int s=__builtin_popcount((unsigned)mask);
    if(s>3) continue;
    Option o{(U)mask,{},false};
    for(int a=0;a<n;++a) if(mask>>a&1)
      for(int b=a+1;b<n;++b) if(mask>>b&1) {
        int dy=b/m-a/m, dz=b%m-a%m, d=gcd(abs(dy),abs(dz));
        dy/=d; dz/=d;
        if(dy<0 || (dy==0 && dz<0)) {dy=-dy;dz=-dz;}
        o.dirs.emplace_back(dy,dz);
      }
    if(s==3 && o.dirs[0]==o.dirs[1] && o.dirs[1]==o.dirs[2]) o.collinear=true;
    options[s].push_back(move(o));
  }
  vector<vector<U>> levels(7);
  for(int a=0;a<=3;++a) for(int b=0;b<=3;++b)
    for(const auto &x:options[a]) for(const auto &y:options[b]) {
      if((a && y.collinear)||(b && x.collinear)) continue;
      bool forbidden=false;
      for(auto dx:x.dirs) for(auto dy:y.dirs) if(dx==dy) forbidden=true;
      if(!forbidden) levels[a+b].push_back(x.mask|(y.mask<<n));
    }
  unordered_map<U,unsigned char> next,now;
  array<int,8> fg{},fh{};
  int rg=-1,rh=-1;
  for(int s=6;s>=0;--s) {
    now.clear(); now.reserve(levels[s].size()*2+1);
    for(U mask:levels[s]) {
      unsigned ug=0,uh=0; bool has=false;
      for(int j=0;j<N;++j) if(!(mask>>j&1)) {
        auto it=next.find(mask|(U(1)<<j));
        if(it==next.end()) continue;
        has=true; int v=it->second;
        ug|=1u<<(v&15); uh|=1u<<(v>>4);
      }
      int g=0,h=has?0:1;
      while((ug>>g)&1) ++g;
      while((uh>>h)&1) ++h;
      now.emplace(mask,(unsigned char)(g|(h<<4)));
      if(s==1) { ++fg[g]; ++fh[h]; }
      if(s==0) { rg=g; rh=h; }
    }
    next.swap(now);
  }
  cout<<k<<"x"<<m<<" safe=";
  for(auto &v:levels) cout<<v.size()<<",";
  cout<<" root="<<rg<<","<<rh<<" firstG=";
  for(int x:fg) cout<<x<<",";
  cout<<" firstH=";
  for(int x:fh) cout<<x<<",";
  cout<<endl;
}
int main() {
  for(auto [k,m]:vector<pair<int,int>>{{1,1},{1,2},{1,3},{2,2},{2,3},
    {3,3},{3,4},{3,5},{4,4},{3,6},{4,5}}) check(k,m);
}
