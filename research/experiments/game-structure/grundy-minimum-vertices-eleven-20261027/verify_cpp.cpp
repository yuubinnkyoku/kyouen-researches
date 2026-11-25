// Independent bottom-up exact Node Kayles verification, C++17.
// c++ -std=c++17 -O2 -Wall -Wextra verify_cpp.cpp -o /tmp/verify_g8 && /tmp/verify_g8
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>
using namespace std;

static const vector<pair<int,int>> base = {
    {0,2},{0,7},{0,8},{0,9},{1,3},{1,4},{1,5},{1,7},
    {2,4},{2,5},{2,7},{3,4},{3,6},{4,11},{8,11},{10,11},{11,12}
};

void verify(int n, int expected) {
    vector<pair<int,int>> edges = base;
    if (n >= 16) { edges.emplace_back(13,14); edges.emplace_back(14,15); }
    vector<int> closed(n);
    for (int v=0;v<n;v++) closed[v]=1<<v;
    for (auto [u,v]:edges) {closed[u]|=1<<v;closed[v]|=1<<u;}
    int all=1<<n;
    vector<uint8_t> g(all),independent(all);
    independent[0]=1;
    int alpha=0;
    for (int state=1;state<all;state++) {
        unsigned options=0;
        int v=__builtin_ctz((unsigned)state);
        int rest=state & (state-1);
        independent[state]=independent[rest] && !(closed[v]&rest);
        if (independent[state]) alpha=max(alpha,__builtin_popcount((unsigned)state));
        for (int bits=state;bits;bits&=bits-1) {
            int w=__builtin_ctz((unsigned)bits);
            int next=state&~closed[w];
            assert(next<state);
            options|=1u<<g[next];
        }
        g[state]=__builtin_ctz(~options);
    }
    assert(g[all-1]==expected);
    assert(alpha==expected);
    assert(n==expected+(expected+2)/2);
    if (n==13) {
        vector<int> values;
        for(int v=0;v<n;v++)values.push_back(g[(all-1)&~closed[v]]);
        assert((values==vector<int>{1,0,2,2,1,4,6,3,5,5,7,2,7}));
    }
    cout << "n="<<n<<" edges="<<edges.size()<<" g="<<int(g[all-1])
         <<" alpha="<<alpha<<" tau="<<n-alpha<<" verified-subsets="<<all<<'\n';
}
int main() {
    verify(13,8);verify(14,9);verify(16,10);verify(17,11);
}
