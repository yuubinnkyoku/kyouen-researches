// Independent exact-integer circle census. No modular bound is used.
// Compile: g++ -std=c++17 -O2 anisotropic_circle_independent_20261016.cpp -o /tmp/anisotropic_circle
#include <algorithm>
#include <array>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <unordered_set>
#include <vector>
using namespace std;
using ll=long long;
using Key=array<ll,4>;
struct H {size_t operator()(const Key& a) const {size_t h=0;for(auto x:a) h^=std::hash<ll>{}(x)+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);return h;}};
struct Point{ll x,y;};
ll norm_gcd(Key k){ll g=0;for(auto x:k)g=gcd(g,llabs(x));return g;}
Key circle(Point p,Point q,Point r){
    ll dx1=q.x-p.x,dy1=q.y-p.y,dx2=r.x-p.x,dy2=r.y-p.y;
    ll a=dx1*dy2-dx2*dy1;
    if(a==0)return {0,0,0,0};
    ll s0=p.x*p.x+p.y*p.y,s1=q.x*q.x+q.y*q.y,s2=r.x*r.x+r.y*r.y;
    ll b=-(s1-s0)*dy2+(s2-s0)*dy1;
    ll c=-dx1*(s2-s0)+dx2*(s1-s0);
    ll d=-a*s0-b*p.x-c*p.y;
    Key k={a,b,c,d};ll g=norm_gcd(k);
    for(ll& x:k)x/=g;
    if(k[0]<0)for(ll& x:k)x=-x;
    return k;
}
bool lies(const Key& k,Point p){return k[0]*(p.x*p.x+p.y*p.y)+k[1]*p.x+k[2]*p.y+k[3]==0;}
int main(){
    vector<array<int,4>> cases={
       {5,10,1,1},{6,10,1,1},{7,9,1,1},{8,8,1,1},{9,8,1,1},
       {5,10,3,1},{6,10,3,1},{7,9,3,1},{8,8,3,1},
       {5,9,9,1},{6,9,9,1},{5,10,2,2},{6,9,2,5},{7,8,3,3},
       {5,9,6,3},{6,9,6,3},{7,8,6,3}
    };
    for(auto [w,m,h,d]:cases){
        vector<Point> pts;
        for(int i=0;i<w;i++)for(int j=0;j<m;j++)pts.push_back({-23+h*j,17+d*i});
        unordered_set<Key,H> seen;
        int maximum=0,violations=0;long long count=0;
        for(size_t i=0;i<pts.size();i++)for(size_t j=i+1;j<pts.size();j++)for(size_t k=j+1;k<pts.size();k++){
            Key c=circle(pts[i],pts[j],pts[k]);if(c[0]==0||!seen.insert(c).second)continue;
            int hits=0;for(auto p:pts)hits+=lies(c,p);
            maximum=max(maximum,hits);count++;
            if(hits>2*((2*w+2)/3))violations++;
        }
        cout<<"w="<<w<<" m="<<m<<" h="<<h<<" d="<<d
            <<" distinct_circles="<<count<<" max_points="<<maximum
            <<" modular_bound="<<2*((2*w+2)/3)<<" violations="<<violations<<"\n";
        if(violations){cerr<<"FAIL\n";return 1;}
    }
    cout<<"PASS\n";
}
