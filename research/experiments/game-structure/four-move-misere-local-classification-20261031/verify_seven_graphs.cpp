// Independent labeled graph enumeration for the sharp 7-vertex common-winning-move boundary.
#include <array>
#include <cstdint>
#include <cstdio>
#include <utility>

static int mex(unsigned seen) {
    int k = 0;
    while (seen & (1u << k)) ++k;
    return k;
}

static std::pair<int, int> eval(int mask, const std::array<int, 7>& adj,
                                std::array<std::pair<int, int>, 128>& memo) {
    if (memo[mask].first >= 0) return memo[mask];
    if (!mask) return memo[mask] = {0, 1};
    unsigned normal = 0, misere = 0;
    for (int m = mask; m; m &= m - 1) {
        int v = __builtin_ctz(static_cast<unsigned>(m));
        auto [g, h] = eval(mask & ~(adj[v] | (1 << v)), adj, memo);
        normal |= 1u << g;
        misere |= 1u << h;
    }
    return memo[mask] = {mex(normal), mex(misere)};
}

int main() {
    std::array<std::pair<int, int>, 21> edges{};
    int z = 0;
    for (int i = 0; i < 7; ++i)
        for (int j = i + 1; j < 7; ++j) edges[z++] = {i, j};
    std::uint64_t any_isolated = 0, common_graphs = 0, total_common_moves = 0, cycle_witnesses = 0, paths_witnesses = 0;
    for (std::uint32_t graph = 0; graph < (1u << 21); ++graph) {
        std::array<int, 7> adj{};
        for (int i = 0; i < 21; ++i)
            if (graph & (1u << i)) {
                auto [a, b] = edges[i];
                adj[a] |= 1 << b;
                adj[b] |= 1 << a;
            }
        bool has_isolated = false, has_common = false;
        std::array<std::pair<int, int>, 128> memo;
        memo.fill({-1, -1});
        for (int v = 0; v < 7; ++v) if (!adj[v]) {
            has_isolated = true;
            auto [g, h] = eval(127 ^ (1 << v), adj, memo);
            if (g == 0 && h == 0) {
                has_common = true;
                ++total_common_moves;
                int ones = 0, twos = 0, edges_count = 0;
                for (int u = 0; u < 7; ++u) if (u != v) {
                    int d = __builtin_popcount(static_cast<unsigned>(adj[u]));
                    ones += (d == 1);
                    twos += (d == 2);
                    edges_count += d;
                }
                int unvisited = 127 ^ (1 << v);
                int comps = 0;
                std::array<int, 2> sizes{};
                while (unvisited) {
                    if (comps >= 2) return std::fprintf(stderr, "too many components!\n"), 1;
                    int start = __builtin_ctz(static_cast<unsigned>(unvisited));
                    int reached = 1 << start, frontier = reached;
                    while (frontier) {
                        int next = 0;
                        for (int f = frontier; f; f &= f - 1)
                            next |= adj[__builtin_ctz(static_cast<unsigned>(f))];
                        next &= ~reached;
                        reached |= next;
                        frontier = next;
                    }
                    sizes[comps++] = __builtin_popcount(static_cast<unsigned>(reached));
                    unvisited &= ~reached;
                }
                if (ones == 0 && twos == 6 && edges_count == 12 && comps == 1)
                    ++cycle_witnesses;
                else if (ones == 4 && twos == 2 && edges_count == 8 && comps == 2
                         && sizes[0] == 3 && sizes[1] == 3)
                    ++paths_witnesses;
                else return std::fprintf(stderr, "unexpected 6-vertex residual!\n"), 1;
            }
        }
        any_isolated += has_isolated;
        common_graphs += has_common;
    }
    std::printf("all 2^21 labeled 7-vertex graphs checked; with isolated vertex: %llu; common-winning graph count: %llu; total common-winning moves: %llu; C6: %llu; 2P3: %llu\n",
        (unsigned long long)any_isolated, (unsigned long long)common_graphs,
        (unsigned long long)total_common_moves, (unsigned long long)cycle_witnesses, (unsigned long long)paths_witnesses);
    return (common_graphs == 1050 && total_common_moves == 1050 && cycle_witnesses == 420 && paths_witnesses == 630) ? 0 : 1;
}
