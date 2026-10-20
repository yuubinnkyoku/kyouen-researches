// Independent subset DP: occupied vertices are the state (not residual graphs).
// Input: each line: n followed by n adjacency bitmasks; n=0 terminates.
#include <iostream>
#include <vector>
#include <cstdint>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n;
    while (cin >> n && n) {
        vector<unsigned> adj(n);
        for (auto &x: adj) cin >> x;
        unsigned full = (1u<<n)-1;
        vector<int8_t> memo(1u<<n, -1);
        auto dfs = [&](auto &&self, unsigned chosen) -> int {
            auto &ans = memo[chosen];
            if (ans >= 0) return ans;
            unsigned blocked = chosen, tmp=chosen;
            while (tmp) {
                unsigned bit = tmp & -tmp;
                tmp -= bit;
                blocked |= adj[__builtin_ctz(bit)];
            }
            unsigned avail = full & ~blocked;
            unsigned long long found=0;
            while (avail) {
                unsigned bit = avail & -avail;
                avail -= bit;
                int child = self(self, chosen | bit);
                if (child < 64) found |= 1ull << child;
            }
            int g=0;
            while ((found>>g)&1ull) ++g;
            ans = (int8_t)g;
            return g;
        };
        cout << dfs(dfs, 0) << '\n';
    }
}
