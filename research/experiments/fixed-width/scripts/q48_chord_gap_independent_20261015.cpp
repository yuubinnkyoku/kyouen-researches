// Independent integer-square census using middle chords d1,d2, not d0,d1.
// Exhaustive for 1<=d0,d1<=3000, odd; no floating-point decisions.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using ll=long long;
ll root(ll n){
    if(n<0) return -1;
    ll lo=0,hi=1;
    while(hi*hi<n) hi*=2;
    while(lo<hi){ ll mid=lo+(hi-lo)/2; if(mid*mid<n) lo=mid+1; else hi=mid; }
    return lo*lo==n?lo:-1;
}
int main(){
    const ll N=3000;
    std::vector<std::array<ll,4>> out;
    // d2 may exceed N for d0,d1<=N, but d2^2<2*N^2.
    for(ll d1=1;d1<=N;d1+=2){
        for(ll d2=1;d2<=4243;d2+=2){
            ll s0=2*d1*d1-d2*d2-8;
            ll s3=2*d2*d2-d1*d1-8;
            ll d0=root(s0),d3=root(s3);
            if(d0<1 || d0>N || d3<1 || !(d0&1) || !(d3&1)) continue;
            out.push_back({d0,d1,d2,d3});
        }
    }
    std::sort(out.begin(),out.end());
    const std::vector<std::array<ll,4>> expected={
        {1,3,3,1},{35,51,63,73},{73,63,51,35},
        {1331,1935,2391,2773},{2773,2391,1935,1331}
    };
    assert(out==expected);
    for(const auto& d:out){
        if(d==expected[0]) continue;
        assert((d[0]<d[1] && d[1]<d[2] && d[2]<d[3]) ||
               (d[0]>d[1] && d[1]>d[2] && d[2]>d[3]));
        for(int i=0;i<3;i++) assert(std::llabs(d[i+1]-d[i])>=10);
        for(auto x:d) std::cout<<x<<" ";
        std::cout<<"\n";
    }
    std::cout<<"PASS independent middle-chord enumeration: "<<out.size()<<" profiles\n";
}
