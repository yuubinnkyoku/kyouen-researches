#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <tuple>
#include <vector>
using namespace std;
using ll = long long;

// Exact square test, with floating approximation corrected by integer comparisons.
ll exact_root(ll x) {
    if (x < 0) return -1;
    ll r = sqrtl((long double)x);
    while (r*r > x) --r;
    while ((r+1)*(r+1) <= x) ++r;
    return r*r == x ? r : -1;
}
int main() {
    const int bound = 2773;
    vector<tuple<int,int,int,int>> patterns;
    // Independent order: enumerate middle two chords, solve both outer squares.
    for (int b=1;b<=bound;b++) for (int c=1;c<=bound;c++) {
        ll a = exact_root(2LL*b*b-c*c-8);
        ll d = exact_root(2LL*c*c-b*b-8);
        if (a<=0 || d<=0 || a>bound || d>bound) continue;
        if (((a-b)&1) || ((b-c)&1) || ((c-d)&1)) continue;
        patterns.emplace_back(a,b,c,d);
    }
    sort(patterns.begin(),patterns.end());
    for (auto [a,b,c,d]:patterns)
        cout << a << "," << b << "," << c << "," << d << "\n";
    assert(patterns.size() == 5);
    assert(patterns[0] == make_tuple(1,3,3,1));
    assert(patterns[1] == make_tuple(35,51,63,73));
    assert(patterns[2] == make_tuple(73,63,51,35));
    assert(patterns[3] == make_tuple(1331,1935,2391,2773));
    assert(patterns[4] == make_tuple(2773,2391,1935,1331));
}
