// Independent direct-modulus audit (not CRT masks).
// c++ -O2 -std=c++17 verify_circle_band_max_5_63_independent_20261016.cpp -o /tmp/verify_band && /tmp/verify_band
#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <iostream>
using namespace std;

int main() {
    constexpr int M = 5040;
    const array<int, 13> ends = {6,7,10,11,21,22,24,25,42,43,45,47,63};
    const array<int, 13> T = {4,5,6,7,8,9,10,11,12,13,14,15,16};
    array<bool, M> qr{};
    for (int z=0; z<M; ++z) qr[(z*z)%M] = true;
    array<array<int, 4>, 64> best{};
    for (int g=1; g<=3; ++g) {
        for (int k=0; k<63; ++k) {
            for (int s=0; s<M; ++s) {
                int count=0;
                for (int y=0; y<63; ++y) {
                    int j=y-k;
                    if (j && j%g==0) {
                        int t=j/g;
                        int a=(t*(s-g*g*t))%M;
                        if (a<0) a+=M;
                        count+=qr[a];
                    }
                    if (y>=k) best[y+1][g]=max(best[y+1][g], count);
                }
            }
        }
    }
    for (size_t i=0; i<ends.size(); ++i) {
        int w=ends[i];
        assert(best[w][1]<T[i] && best[w][2]<T[i] && best[w][3]<T[i]);
        cout << w << " T=" << T[i] << " g1=" << best[w][1]
             << " g2=" << best[w][2] << " g3=" << best[w][3] << "\n";
    }
    cout << "PASS: all 13 endpoints, all three denominator cases, full modulus 5040\n";
}
