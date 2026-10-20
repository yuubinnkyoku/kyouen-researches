// Independent C++ checker of the exact cycle Grundy classification.
// g(P_n) is computed by a recurrence with a separate split convention;
// g(C_n) is independently checked by direct state DP for n<=18.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;

static int mex(const vector<int>& a) {
    vector<bool> seen(a.size() + 2, false);
    for (int x : a) if (x >= 0 && x < (int)seen.size()) seen[x] = true;
    for (int k = 0;; ++k) if (!seen[k]) return k;
}

static vector<int> compute_paths(int bound) {
    vector<int> g(bound + 1, 0);
    g[1] = 1;
    for (int n = 2; n <= bound; ++n) {
        vector<int> opts;
        opts.push_back(g[n - 2]); // either endpoint
        for (int left = 0; left <= n - 3; ++left)
            opts.push_back(g[left] ^ g[n - 3 - left]);
        g[n] = mex(opts);
    }
    return g;
}

static int direct_cycle(int n) {
    vector<uint32_t> delete_mask(n);
    for (int i = 0; i < n; ++i)
        delete_mask[i] = (1u << i) | (1u << ((i + 1) % n)) |
                         (1u << ((i + n - 1) % n));
    vector<int> memo(1u << n, -1);
    auto dfs = [&](auto&& self, uint32_t rem) -> int {
        if (memo[rem] >= 0) return memo[rem];
        vector<int> opts;
        for (int i = 0; i < n; ++i)
            if (rem & (1u << i)) opts.push_back(self(self, rem & ~delete_mask[i]));
        return memo[rem] = mex(opts);
    };
    return dfs(dfs, (1u << n) - 1);
}

int main() {
    auto p = compute_paths(800);
    for (int n = 52; n <= 139; ++n) assert(p[n] == p[n + 34]);
    for (int n = 52; n <= 766; ++n) assert(p[n] == p[n + 34]);
    vector<int> c(767, 0);
    for (int n = 3; n <= 766; ++n) c[n] = (p[n - 3] == 0) ? 1 : 0;
    for (int n = 3; n <= 18; ++n) assert(c[n] == direct_cycle(n));
    for (int n = 38; n + 34 <= 766; ++n) assert(c[n] == c[n + 34]);
    assert(c[37] != c[71]);
    for (int n = 38; n < 72; ++n) {
        bool predicted = n % 34 == 7 || n % 34 == 11 || n % 34 == 23 ||
                         n % 34 == 27 || n % 34 == 31;
        assert(bool(c[n]) == predicted);
    }
    for (int d : {1, 2, 17}) {
        bool different = false;
        for (int n = 38; n < 72; ++n) different |= c[n] != c[n + d];
        assert(different);
    }
    cout << "PASS C++: independent recurrence, n<=18 full state DP, "
         << "34-periodic cycles from 38, winning residues 7,11,23,27,31\n";
}
