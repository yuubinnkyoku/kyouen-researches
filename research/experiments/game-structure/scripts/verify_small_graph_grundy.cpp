// Independent bitmask dynamic programming for exact Node Kayles values.
// g(M) = mex { g(M \ N[v]) : v in M }.
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;

int solve(int n, uint64_t edge_mask, vector<int>* root_children = nullptr) {
    array<unsigned, 8> closed{};
    for (int i = 0; i < n; ++i) closed[i] = 1u << i;
    int edge = 0;
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j, ++edge)
            if (edge_mask & (uint64_t{1} << edge)) {
                closed[i] |= 1u << j;
                closed[j] |= 1u << i;
            }
    const unsigned full = (1u << n) - 1;
    vector<int> g(full + 1, 0);
    for (unsigned mask = 1; mask <= full; ++mask) {
        unsigned options = 0;
        for (unsigned t = mask; t; t &= t - 1) {
            int v = __builtin_ctz(t);
            options |= 1u << g[mask & ~closed[v]];
        }
        g[mask] = __builtin_ctz(~options);
    }
    if (root_children)
        for (int i = 0; i < n; ++i)
            root_children->push_back(g[full & ~closed[i]]);
    return g[full];
}

int main() {
    for (int n = 1; n <= 6; ++n) {
        array<uint64_t, 8> count{};
        const int m = n * (n - 1) / 2;
        for (uint64_t mask = 0; mask < (uint64_t{1} << m); ++mask)
            ++count[solve(n, mask)];
        cout << "n=" << n;
        for (int g = 0; g < 8; ++g)
            if (count[g]) cout << " " << g << ":" << count[g];
        cout << '\n';
        assert(count[4] == 0);
    }
    // Edges: (0,4),(0,5),(0,6),(1,2),(1,4),(1,5),(2,3).
    uint64_t witness = 0;
    const int pairs[][2] = {{0,4},{0,5},{0,6},{1,2},{1,4},{1,5},{2,3}};
    for (const auto& p : pairs) {
        int k = 0;
        for (int i = 0; i < 7; ++i)
            for (int j = i + 1; j < 7; ++j, ++k)
                if (i == p[0] && j == p[1]) witness |= uint64_t{1} << k;
    }
    vector<int> children;
    assert(solve(7, witness, &children) == 4);
    cout << "n=7 witness edge-mask=" << witness << " children=";
    for (int g : children) cout << g << ',';
    cout << '\n';
    uint64_t witness8 = 0;
    for (const auto& p : pairs) {
        int k = 0;
        for (int i = 0; i < 8; ++i)
            for (int j = i + 1; j < 8; ++j, ++k)
                if (i == p[0] && j == p[1]) witness8 |= uint64_t{1} << k;
    }
    assert(solve(8, witness8) == 5); // eighth vertex isolated

    uint64_t fewer = 0;
    for (uint64_t mask = 0; mask < (uint64_t{1} << 21); ++mask) {
        if (__builtin_popcountll(mask) >= 7) continue;
        ++fewer;
        assert(solve(7, mask) != 4);
    }
    cout << "n=7 graphs with <=6 edges and g!=4: " << fewer << '\n';
}
