// Exact finite bases for missing-graph K5 split Node Kayles.
// Compile: c++ -std=c++17 -O3 -Wall -Wextra -pedantic verify.cpp -o /tmp/verify_missing_k5
// Run: /tmp/verify_missing_k5 5; /tmp/verify_missing_k5 6; /tmp/verify_missing_k5 7
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <utility>
#include <vector>
using namespace std;
struct Type { int mask, qty; };

// No predicted formula is used inside this exact mex recurrence.
// State A: remaining clique vertices; all groups with nonempty
// intersection with A retain their original multiplicities.
// Previously isolated vertices contribute an xor parity separately.
int sg(int k, const vector<Type>& ts) {
    int dp[128] = {}, par[128] = {}, z[7] = {};
    for (auto t : ts)
        for (int i = 0; i < k; ++i)
            if (t.mask & (1 << i)) z[i] ^= t.qty & 1;
    for (int a = 1; a < (1 << k); ++a) {
        int u = 0;
        for (auto t : ts) if (t.mask & a) u ^= t.qty & 1;
        par[a] = u;
        uint32_t options = 0;
        // Clique move: all clique vertices disappear. Surviving
        // independent vertices are isolated.
        for (int i = 0; i < k; ++i)
            if (a & (1 << i)) options |= 1u << (u ^ z[i]);
        // Independent move: remove its remaining clique neighbors.
        // Newly isolated groups have parity par[a] xor par[b];
        // the selected vertex itself must be subtracted.
        for (auto t : ts) if (t.mask & a) {
            int b = a & ~t.mask;
            options |= 1u << (dp[b] ^ u ^ par[b] ^ 1);
        }
        int v = 0;
        while (options & (1u << v)) ++v;
        dp[a] = v;
    }
    return dp[(1 << k) - 1];
}

int main(int argc, char** argv) {
    int k = argc > 1 ? atoi(argv[1]) : 6;
    if (k < 5 || k > 7) return 2;
    vector<pair<int,int>> pairs;
    for (int i = 0; i < k; ++i)
        for (int j = i + 1; j < k; ++j)
            if (!(i < 5 && j < 5)) pairs.push_back({i,j});
    int p = static_cast<int>(pairs.size()), pow3 = 1;
    for (int i = 0; i < k; ++i) pow3 *= 3;
    uint64_t checked = 0, fail = 0, restricted = 0, restrictedFail = 0;
    int minBad = 1000, maxG = 0, minG5 = 1000;
    for (int rb = 0; rb < (1 << p); ++rb)
        for (int lc = 0; lc < pow3; ++lc) {
            vector<Type> ts;
            int n = k, u = 0, z[7] = {};
            for (int j = 0; j < p; ++j) {
                auto [a,b] = pairs[j];
                int v = 1 + ((rb >> j) & 1);
                ts.push_back({(1 << a) | (1 << b), v});
                n += v; u ^= v & 1; z[a] ^= v & 1; z[b] ^= v & 1;
            }
            int q = lc;
            bool positive = true;
            for (int i = 0; i < k; ++i) {
                int v = q % 3; q /= 3;
                if (i < 5 && !v) positive = false;
                if (v) {
                    ts.push_back({1 << i, v});
                    n += v; u ^= v & 1; z[i] ^= v & 1;
                }
            }
            int expected = 1 ^ u ^ z[0];
            for (int i = 1; i < k; ++i)
                if (z[i] != z[0]) { expected = 2 + u; break; }
            int got = sg(k, ts);
            ++checked;
            if (positive) {
                ++restricted;
                if (got != expected) ++restrictedFail;
            }
            if (got != expected) {
                ++fail;
                if (n < minBad) minBad = n;
            }
            if (got > maxG) maxG = got;
            if (got == 5 && n < minG5) minG5 = n;
        }
    cout << "k=" << k << " cases=" << checked
         << " failures=" << fail
         << " restricted_all_K5_leaves_positive=" << restricted
         << " restricted_failures=" << restrictedFail
         << " min_counterexample_vertices=" << minBad
         << " max_grundy=" << maxG
         << " min_g5_vertices=" << minG5 << '\n';
    if (restrictedFail) return 1;
    if (k == 7 && (checked != 4478976 || fail)) return 1;
    if (k == 6 && (checked != 23328 || fail != 211 ||
                   minBad != 16 || maxG != 5 || minG5 != 17)) return 1;
    if (k == 5 && (restricted != 32 || restrictedFail)) return 1;
    return 0;
}
