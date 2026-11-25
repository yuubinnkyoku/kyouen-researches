// Independent audit: use 0-based chosen vertices, not the split-length recurrence.
// c++ -std=c++17 -O2 -Wall -Wextra verify_path_period_independent.cpp -o /tmp/path_audit && /tmp/path_audit
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;

int mex(const vector<int>& x) {
    vector<bool> seen(x.size() + 1, false);
    for (int v : x) if (v >= 0 && v < (int)seen.size()) seen[v] = true;
    int ans = 0;
    while (seen[ans]) ++ans;
    return ans;
}

int solve_direct_graph(const vector<uint32_t>& closed, uint32_t free,
                       unordered_map<uint32_t,int>& cache) {
    if (free == 0) return 0;
    auto it = cache.find(free);
    if (it != cache.end()) return it->second;
    vector<int> values;
    for (uint32_t b = free; b; b &= b - 1) {
        int i = __builtin_ctz(b);
        values.push_back(solve_direct_graph(closed, free & ~closed[i], cache));
    }
    return cache[free] = mex(values);
}

int main() {
    const int M = 2000;
    vector<int> g(M + 1, 0);
    for (int n = 1; n <= M; ++n) {
        vector<int> children;
        for (int i = 0; i < n; ++i) {
            const int left = max(0, i - 1);
            const int right = max(0, n - i - 2);
            children.push_back(g[left] ^ g[right]);
        }
        g[n] = mex(children);
    }
    for (int n = 52; n + 34 <= M; ++n) assert(g[n] == g[n + 34]);
    assert(g[51] == 2 && g[85] == 9);
    int mx = *max_element(g.begin(), g.end());
    assert(mx == 9);
    // Independently derive least component size per nimber, then Bellman-Ford
    // on the 16-state XOR Cayley graph (not Python's heap-based Dijkstra).
    vector<int> cost(16, 1000000);
    for (int n = 0; n <= 85; ++n) cost[g[n]] = min(cost[g[n]], n);
    assert(cost[6] == 1000000 && cost[8] == 68 && cost[9] == 85);
    vector<int> dist(16, 1000000);
    dist[0] = 0;
    for (int step = 0; step < 16; ++step) {
        bool changed = false;
        for (int x = 0; x < 16; ++x) for (int v = 1; v < 16; ++v) {
            if (cost[v] >= 1000000) continue;
            int y = x ^ v;
            if (dist[x] + cost[v] < dist[y]) {
                dist[y] = dist[x] + cost[v];
                changed = true;
            }
        }
        if (!changed) break;
    }
    assert((dist == vector<int>{0,1,3,4,13,14,16,17,68,69,71,72,81,82,84,85}));
    assert((g[68] ^ g[13] ^ g[3] ^ g[1]) == 15);
    int checked = 0;
    for (int n = 0; n <= 19; ++n) {
        vector<uint32_t> closed(n);
        for (int i = 0; i < n; ++i) {
            closed[i] = (1u << i);
            if (i) closed[i] |= 1u << (i - 1);
            if (i + 1 < n) closed[i] |= 1u << (i + 1);
        }
        unordered_map<uint32_t,int> cache;
        int exact = solve_direct_graph(closed, (1u << n) - 1, cache);
        assert(exact == g[n]);
        ++checked;
    }
    for (int n = 3; n <= 16; ++n) {
        vector<uint32_t> closed(n);
        for (int i = 0; i < n; ++i)
            closed[i] = (1u << i) | (1u << ((i + n - 1) % n)) | (1u << ((i + 1) % n));
        unordered_map<uint32_t,int> cache;
        int exact = solve_direct_graph(closed, (1u << n) - 1, cache);
        assert(exact == (g[n - 3] == 0 ? 1 : 0));
        ++checked;
    }
    cout << "PASS: independent vertex-choice recurrence n<=2000, direct path n<=19, "
         << "direct cycle n<=16; cases=" << checked << "; max nimber=" << mx << "\n";
}
