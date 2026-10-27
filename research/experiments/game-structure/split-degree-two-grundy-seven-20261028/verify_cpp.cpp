// Independent all-2^n-subsets dynamic programming for Node Kayles.
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;

void verify(int k, const vector<int>& signatures, int expected) {
    int n = k + (int)signatures.size();
    assert(n <= 24);
    vector<uint32_t> closed(n);
    for (int i = 0; i < k; ++i) {
        for (int j = 0; j < k; ++j) closed[i] |= uint32_t(1) << j;
        for (int j = 0; j < (int)signatures.size(); ++j)
            if (signatures[j] & (1 << i)) {
                closed[i] |= uint32_t(1) << (k + j);
                closed[k + j] |= uint32_t(1) << i;
            }
    }
    for (int i = k; i < n; ++i) closed[i] |= uint32_t(1) << i;
    uint32_t limit = uint32_t(1) << n;
    vector<uint8_t> dp(limit);
    for (uint32_t mask = 1; mask < limit; ++mask) {
        uint32_t possible = 0;
        uint32_t remaining = mask;
        while (remaining) {
            int v = __builtin_ctz(remaining);
            remaining &= remaining - 1;
            int value = dp[mask & ~closed[v]];
            assert(value < 32);
            possible |= uint32_t(1) << value;
        }
        int mex = 0;
        while (possible & (uint32_t(1) << mex)) ++mex;
        dp[mask] = mex;
    }
    uint32_t full = limit - 1;
    assert(dp[full] == expected);
    uint32_t possible = 0;
    cout << "k=" << k << " n=" << n << " g=" << int(dp[full])
         << " full-subsets=" << limit << "\nchildren:";
    for (int i = 0; i < n; ++i) {
        int child = dp[full & ~closed[i]];
        possible |= uint32_t(1) << child;
        cout << " " << child;
    }
    cout << "\n";
    assert((possible & ((uint32_t(1) << expected) - 1)) ==
           ((uint32_t(1) << expected) - 1));
    assert(!(possible & (uint32_t(1) << expected)));
}

int main() {
    verify(7, {3, 3, 5, 9, 9, 20, 20, 32, 36, 36, 48, 65, 65}, 7);
    verify(6, {3, 3, 4, 4, 5, 9, 9, 16, 20, 20, 33, 33}, 6);
}
