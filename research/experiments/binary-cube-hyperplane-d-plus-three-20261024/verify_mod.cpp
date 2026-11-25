// Independent modular-rank verifier for d+3 binary hypercube witnesses.
// Nonzero determinant modulo 1009 implies nonzero integer determinant.
#include <cassert>
#include <iostream>
#include <map>
#include <utility>
#include <vector>
using namespace std;
static constexpr int P = 1009;
int modpow(int x, int n) {
    int y = 1;
    while (n) {
        if (n & 1) y = y * x % P;
        x = x * x % P;
        n >>= 1;
    }
    return y;
}
bool independent(const vector<int>& subset, int d) {
    int a[12][12] = {};
    for (int i = 0; i <= d; ++i) {
        a[i][0] = 1;
        for (int j = 0; j < d; ++j) a[i][j + 1] = (subset[i] >> j) & 1;
    }
    for (int j = 0; j <= d; ++j) {
        int pivot = j;
        while (pivot <= d && a[pivot][j] == 0) ++pivot;
        if (pivot > d) return false;
        for (int k = j; k <= d; ++k) swap(a[j][k], a[pivot][k]);
        int inv = modpow(a[j][j], P - 2);
        for (int i = j + 1; i <= d; ++i) {
            int factor = a[i][j] * inv % P;
            for (int k = j; k <= d; ++k)
                a[i][k] = (a[i][k] - factor * a[j][k] % P + P) % P;
        }
    }
    return true;
}
int main() {
    map<int, vector<int>> witnesses = {
        {6, {0, 54, 40, 39, 21, 2, 62, 59, 14}},
        {7, {0, 56, 109, 70, 72, 117, 87, 97, 35, 13}},
        {8, {0, 118, 145, 79, 161, 210, 125, 237, 195, 166, 42}},
        {9, {0, 479, 220, 421, 240, 205, 445, 167, 150, 458, 359, 1}},
        {10, {0, 398, 511, 619, 457, 220, 766, 879, 868, 966, 886, 1000, 917}},
    };
    for (const auto& [d, points] : witnesses) {
        assert(static_cast<int>(points.size()) == d + 3);
        int tested = 0;
        for (int i = 0; i < static_cast<int>(points.size()); ++i)
            for (int j = i + 1; j < static_cast<int>(points.size()); ++j) {
                vector<int> subset;
                for (int k = 0; k < static_cast<int>(points.size()); ++k)
                    if (k != i && k != j) subset.push_back(points[k]);
                if (!independent(subset, d)) {
                    cerr << "FAIL d=" << d << " omitted=" << i << "," << j << "\n";
                    return 1;
                }
                ++tested;
            }
        cout << "d=" << d << " points=" << points.size()
             << " nonzero_mod1009=" << tested << "\n";
    }
}
