// Independent bottom-up subset DP for the 12-vertex split graph.
#include <cassert>
#include <cstdint>
#include <iostream>
using namespace std;
int main() {
    constexpr int N = 12;
    uint16_t closed[N] = {};
    for (int i = 0; i < N; ++i) closed[i] = uint16_t(1u << i);
    auto edge = [&](int u, int v) {
        closed[u] |= uint16_t(1u << v);
        closed[v] |= uint16_t(1u << u);
    };
    for (int i = 0; i < 6; ++i)
        for (int j = i + 1; j < 6; ++j) edge(i, j);
    constexpr int lengths[6] = {4, 3, 1, 2, 3, 3};
    constexpr int sig[6][4] = {
        {0, 2, 4, 5}, {0, 1, 2, -1}, {4, -1, -1, -1},
        {0, 3, -1, -1}, {0, 1, 5, -1}, {0, 3, 4, -1}
    };
    for (int i = 0; i < 6; ++i)
        for (int j = 0; j < lengths[i]; ++j) edge(sig[i][j], 6 + i);
    uint8_t g[1 << N] = {};
    for (int mask = 1; mask < (1 << N); ++mask) {
        unsigned options = 0;
        for (int t = mask; t; t &= t - 1) {
            int v = __builtin_ctz(unsigned(t));
            options |= 1u << g[mask & ~closed[v]];
        }
        g[mask] = uint8_t(__builtin_ctz(~options));
    }
    constexpr int expected[12] = {1, 0, 0, 0, 1, 0, 0, 3, 2, 3, 3, 0};
    assert(g[(1 << N) - 1] == 4);
    cout << "g=4 children=";
    for (int v = 0; v < N; ++v) {
        int child = g[((1 << N) - 1) & ~closed[v]];
        assert(child == expected[v]);
        cout << child << (v + 1 == N ? '\n' : ' ');
    }
}
