// Independent exhaustive enumeration with direct integer 3x3 determinant.
#include <bits/stdc++.h>
using namespace std;
using U=uint64_t;
struct P {int x,y,z;};
int det(P a,P b,P c,P d) {
  int x=b.x-a.x,y=b.y-a.y,z=b.z-a.z;
  int u=c.x-a.x,v=c.y-a.y,w=c.z-a.z;
  int r=d.x-a.x,s=d.y-a.y,t=d.z-a.z;
  return x*(v*t-w*s)-y*(u*t-w*r)+z*(u*s-v*r);
}
void check(int k,int m) {
  int n=2*k*m;
  vector<P> pts;
  for(int x=0;x<2;++x) for(int y=0;y<k;++y) for(int z=0;z<m;++z)
    pts.push_back({x,y,z});
  vector<vector<U>> levels(7); levels[0]={0};
  for(int s=0;s<6;++s) for(U mask:levels[s]) {
    int start=mask?64-__builtin_clzll(mask):0;
    int ids[6],cnt=0;
    for(int j=0;j<n;++j) if(mask>>j&1) ids[cnt++]=j;
    for(int i=start;i<n;++i) {
      bool safe=true;
      for(int a=0;a<cnt && safe;++a)
        for(int b=a+1;b<cnt && safe;++b)
          for(int c=b+1;c<cnt;++c)
            if(!det(pts[ids[a]],pts[ids[b]],pts[ids[c]],pts[i])) {
              safe=false; break;
            }
      if(safe) levels[s+1].push_back(mask|(U(1)<<i));
    }
  }
  unordered_map<U,unsigned char> next,now;
  array<int,8> fg{},fh{};
  int rg=-1,rh=-1;
  for(int s=6;s>=0;--s) {
    now.clear(); now.reserve(levels[s].size()*2+1);
    for(U mask:levels[s]) {
      unsigned ug=0,uh=0; bool has=false;
      for(int j=0;j<n;++j) if(!(mask>>j&1)) {
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
  for(auto [k,m]:vector<pair<int,int>>{{2,2},{3,3},{3,4},{3,5},{4,4},{3,6},{4,5}})
    check(k,m);
}
