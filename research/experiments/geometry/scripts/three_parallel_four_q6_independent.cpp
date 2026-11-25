// Independent C++17 audit of the three-circle witness and its finite game.
// Compile: g++ -std=c++17 -O2 -Wall -Wextra -pedantic <this-file> -o /tmp/q6_audit
// /tmp/three_parallel_four_q6_independent
#include <array>
#include <cassert>
#include <iostream>
#include <map>
#include <set>
#include <vector>
using namespace std;

struct Point {int y, sign, x_squared;};
int main() {
    const array<array<int,2>,3> squares = {{{16,18},{15,14},{12,10}}};
    vector<Point> pts;
    for (int y=0;y<3;y++) for (int k : squares[y]) for (int s : {-1,1})
        pts.push_back({y,s,k});
    assert(pts.size()==12);
    const array<array<int,2>,3> circle = {{{0,-16},{1,-16},{2,-18}}};
    vector<int> edges;
    for (auto [b,c] : circle) {
        int mask=0;
        array<int,3> per_row{};
        for (int i=0;i<12;i++) {
            const auto &p=pts[i];
            if (p.x_squared + p.y*p.y + b*p.y + c == 0) {
                mask |= 1<<i;
                ++per_row[p.y];
            }
        }
        assert(__builtin_popcount((unsigned)mask)==6);
        for (int n : per_row) assert(n==2);
        edges.push_back(mask);
    }
    for (int i=0;i<3;i++) for (int j=i+1;j<3;j++)
        assert(__builtin_popcount((unsigned)(edges[i]&edges[j]))==2);

    const int N=1<<12;
    vector<unsigned char> safe(N,1);
    vector<int> grundy(N,-1);
    for (int s=0;s<N;s++) for (int e:edges)
        if ((s&e)==e) safe[s]=0;
    map<int,int> maximal, histogram;
    for (int s=N-1;s>=0;s--) {
        if (!safe[s]) continue;
        bool seen[13]{};
        bool has_move=false;
        for (int i=0;i<12;i++) if (!(s&(1<<i))) {
            int next=s|(1<<i);
            if (safe[next]) {
                has_move=true;
                assert(grundy[next]>=0);
                seen[grundy[next]]=true;
            }
        }
        int mex=0;
        while (seen[mex]) ++mex;
        grundy[s]=mex;
        histogram[mex]++;
        if (!has_move) maximal[__builtin_popcount((unsigned)s)]++;
    }
    assert(grundy[0]==0);
    assert((histogram==map<int,int>{{0,1865},{1,1837},{2,90},{3,123}}));
    assert((maximal==map<int,int>{{9,8},{10,24}}));
    for (int i=0;i<12;i++) assert(grundy[1<<i]==1);
    cout << "PASS circles=3, safe=3915, root=0, maximal={9:8,10:24}, "
         << "nimbers={0:1865,1:1837,2:90,3:123}\n";
}
