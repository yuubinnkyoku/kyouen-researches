// Independent C++20 finite checker for exchangeable-class terminal polynomials.
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    constexpr int k=3, h=2, n=k+h;
    vector<pair<int,int>> orbit;
    for (int s=0;s<=k;s++) for (int a=0;a<(1<<h);a++)
        if(s || a) orbit.push_back({s,a});
    assert(orbit.size()==15);
    uint64_t comparisons=0;
    for(int family=0;family<(1<<15);family++) {
        vector<int> edges;
        for(int i=0;i<15;i++) if((family>>i)&1) {
            auto [s,a]=orbit[i];
            for(int subset=0;subset<(1<<k);subset++)
                if(__builtin_popcount((unsigned)subset)==s)
                    edges.push_back(subset|(a<<k));
        }
        array<uint64_t,n+1> brute{},compressed{};
        auto safe=[&](int mask) {
            for(int e:edges) if((mask&e)==e) return false;
            return true;
        };
        for(int mask=0;mask<(1<<n);mask++) {
            if(!safe(mask)) continue;
            bool maximal=true;
            for(int i=0;i<n;i++) if(!(mask&(1<<i)) && safe(mask|(1<<i))) {
                maximal=false; break;
            }
            if(maximal) brute[__builtin_popcount((unsigned)mask)]++;
        }
        array<int,1<<h> cap{};
        for(int t=0;t<(1<<h);t++) {
            int c=k;
            for(int i=0;i<15;i++) if((family>>i)&1) {
                auto [s,a]=orbit[i];
                if((a&t)==a) c=min(c,s-1);
            }
            cap[t]=c;
        }
        auto choose=[&](int n,int r)->uint64_t {
            uint64_t x=1;
            for(int i=1;i<=r;i++) x=x*(n-i+1)/i;
            return x;
        };
        for(int t=0;t<(1<<h);t++) {
            int c=cap[t];
            if(c<0) continue;
            bool maximal=true;
            for(int y=0;y<h;y++) if(!(t&(1<<y)) && cap[t|(1<<y)]>=c) {
                maximal=false; break;
            }
            if(maximal) compressed[__builtin_popcount((unsigned)t)+c]+=choose(k,c);
        }
        if(brute!=compressed) {
            cerr<<"FAIL family="<<family<<'\n';return 1;
        }
        comparisons++;
    }
    cout<<"PASS C++ exhaustive exchangeable hypergraph families="<<comparisons<<" k=3 h=2\n";
}
