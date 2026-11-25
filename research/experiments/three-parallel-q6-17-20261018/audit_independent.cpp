// Independent finite audit. C++17, no Python imports or generated inputs.
#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <map>
#include <vector>
using namespace std;
using Five = array<int,5>;
struct Circle {int bm,cm,s,delta,p;};

map<int,int> sums(const Five &a) {
    map<int,int> r;
    for(int i=0;i<5;i++) for(int j=i+1;j<5;j++) ++r[a[i]+a[j]];
    return r;
}
int h(const Five &a) {int z=0;for(auto [s,c]:sums(a))z+=c*c;return z;}
int e(const Five &a,const Five &b) {
    auto x=sums(a),y=sums(b);int z=0;
    for(auto [s,c]:x)z+=c*y[s];
    return z;
}
vector<Circle> make_circles(const Five &a,const Five &b) {
    vector<Circle> out;
    for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)
      for(int k=0;k<5;k++)for(int l=k+1;l<5;l++)
        if(a[i]+a[j]==b[k]+b[l])
          out.push_back({(1<<i)|(1<<j),(1<<k)|(1<<l),
                         a[i]+a[j],b[k]*b[l]-a[i]*a[j],a[i]*a[j]});
    return out;
}
bool pair_ok(const Circle &a,const Circle &b) {
    return __builtin_popcount(unsigned(a.bm&b.bm))+
           __builtin_popcount(unsigned(a.cm&b.cm))==1;
}
vector<array<Circle,4>> possible_four(const Five &a,const Five &b) {
    auto c=make_circles(a,b);
    vector<array<Circle,4>> out;
    for(int i=0;i<(int)c.size();i++)for(int j=i+1;j<(int)c.size();j++)
      for(int k=j+1;k<(int)c.size();k++)for(int l=k+1;l<(int)c.size();l++) {
        int id[4]={i,j,k,l};bool ok=true;
        for(int x=0;x<4;x++)for(int y=x+1;y<4;y++)
          if(!pair_ok(c[id[x]],c[id[y]]))ok=false;
        if(ok)out.push_back({c[i],c[j],c[k],c[l]});
      }
    return out;
}
long long determinant(const array<Circle,4> &q) {
    long long a[3][3];
    for(int i=1;i<4;i++){
      a[i-1][0]=q[0].s-q[i].s;
      a[i-1][1]=q[i].delta-q[0].delta;
      a[i-1][2]=q[0].p-q[i].p;
    }
    return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
         - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
         + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]);
}
int main() {
    Five ap={0,2,4,6,8};
    vector<Five> hits;
    int tested=0;
    for(int parity=0;parity<=1;parity++) {
      vector<int> pool;
      for(int x=parity==0?-4:-3;x<=(parity==0?12:11);x+=2)pool.push_back(x);
      int n=pool.size();
      for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)
       for(int c=b+1;c<n;c++)for(int d=c+1;d<n;d++)
        for(int f=d+1;f<n;f++) {
          Five B={pool[a],pool[b],pool[c],pool[d],pool[f]};
          tested++;
          if(h(B)==14 && e(B,ap)==14) {
            hits.push_back(B);
            assert(make_circles(B,ap).size()==14);
            assert(possible_four(B,ap).empty());
          }
        }
    }
    assert(tested==182);
    assert(hits.size()==2);
    assert((hits[0]==Five{-2,2,4,6,8}));
    assert((hits[1]==Five{0,2,4,6,10}));
    Five offset={1,3,5,7,9};
    assert(e(ap,offset)==14);
    auto q=possible_four(ap,offset);
    assert(q.size()==2);
    vector<long long> ds;
    for(auto &z:q)ds.push_back(determinant(z));
    sort(ds.begin(),ds.end());
    assert((ds==vector<long long>{-320,320}));
    assert(e(ap,ap)==16 && possible_four(ap,ap).empty());
    cout << "candidates=" << tested << " mixed_hits=" << hits.size()
         << " mixed_compatible_four=0 offset_compatible_four=" << q.size()
         << " offset_determinants=" << ds[0] << "," << ds[1]
         << " same_AP_compatible_four=0 PASS\n";
}
