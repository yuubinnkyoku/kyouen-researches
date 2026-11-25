// Enumerate labelled C4-free graphs of a fixed size containing edge 0--1.
// Every nonempty unlabelled graph has such a labelling.
#include <array>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <utility>
#include <vector>

using namespace std;
vector<pair<int,int>> edges;
array<unsigned, 9> adj{};
uint64_t leaves = 0, saturated = 0, nodes = 0;
map<vector<int>, uint64_t> degree_counts;
int n, wanted;

bool creates_c4(int u, int v) {
    unsigned a = adj[u], b = adj[v];
    while (a) {
        int x = __builtin_ctz(a); a &= a - 1;
        if (adj[x] & b) return true;
    }
    return false;
}

void visit(int start, int count) {
    ++nodes;
    if (count == wanted) {
        ++leaves;
        for (int i = 0; i < n; ++i) if (!adj[i]) return;
        for (auto [u,v] : edges)
            if (!(adj[u] & (1U << v)) && !creates_c4(u,v)) return;
        ++saturated;
        vector<int> degrees;
        for (int i=0; i<n; ++i) degrees.push_back(__builtin_popcount(adj[i]));
        sort(degrees.begin(), degrees.end());
        ++degree_counts[degrees];
        return;
    }
    int need = wanted - count;
    for (int i = start; i <= int(edges.size()) - need; ++i) {
        auto [u,v] = edges[i];
        if (creates_c4(u,v)) continue;
        adj[u] |= 1U << v; adj[v] |= 1U << u;
        visit(i+1, count+1);
        adj[u] &= ~(1U << v); adj[v] &= ~(1U << u);
    }
}

int main(int argc, char **argv) {
    if (argc != 3) return 2;
    n = atoi(argv[1]); wanted = atoi(argv[2]);
    if (n < 4 || n > 9 || wanted < 1 || wanted > n*(n-1)/2) return 2;
    for (int u=0; u<n; ++u) for (int v=u+1; v<n; ++v) edges.emplace_back(u,v);
    adj[0] |= 1U << 1; adj[1] |= 1U;
    visit(1, 1);
    cout << "n=" << n << " edges=" << wanted << " fixed_edge=0-1"
         << " nodes=" << nodes << " c4_free=" << leaves
         << " saturated=" << saturated << '\n';
    for (const auto &[degrees, count] : degree_counts) {
        cout << "degrees=";
        for (size_t i=0; i<degrees.size(); ++i) cout << (i ? "," : "") << degrees[i];
        cout << " fixed_edge_count=" << count << '\n';
    }
}
