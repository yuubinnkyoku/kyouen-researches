// Exhaustive mex for every induced subgraph of the 22-vertex witness.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    constexpr int k = 7;
    const vector<int> s = {3,3,4,4,5,9,9,16,33,33,64,64,68,80,84};
    const int n = k + static_cast<int>(s.size());
    vector<uint32_t> adj(n, 0);
    for (int i = 0; i < k; ++i)
        adj[i] = ((1u << k) - 1u) ^ (1u << i);
    for (int j = 0; j < static_cast<int>(s.size()); ++j) {
        int v = k + j;
        adj[v] = static_cast<uint32_t>(s[j]);
        for (int i = 0; i < k; ++i)
            if (s[j] & (1 << i)) adj[i] |= 1u << v;
    }

    const int limit = 1 << n;
    vector<uint8_t> g(limit, 0);
    int count8 = 0, maxg = 0;
    for (int mask = 1; mask < limit; ++mask) {
        uint32_t options = 0;
        unsigned bits = static_cast<unsigned>(mask);
        while (bits) {
            int v = __builtin_ctz(bits);
            bits &= bits - 1;
            int child = mask & ~static_cast<int>(adj[v] | (1u << v));
            options |= 1u << g[child];
        }
        int value = __builtin_ctz(~options);
        g[mask] = static_cast<uint8_t>(value);
        maxg = max(maxg, value);
        if (value == 8) ++count8;
    }
    cout << "all_induced_subgraphs=" << limit
         << " root=" << static_cast<int>(g[limit - 1])
         << " max=" << maxg << " count_g8=" << count8 << '\n';
    if (g[limit - 1] != 8 || maxg != 8 || count8 != 1) return 1;
    cout << "all checks passed\n";
}
