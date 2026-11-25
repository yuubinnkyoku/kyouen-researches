// Independent remaining-vertex recursive mex solver, C++17.
// Usage: g++ -std=c++17 -O2 independent.cpp -o independent && ./independent
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Game {
    int n;
    vector<unsigned> edges;
    vector<int> memo;
    Game(int n_, vector<vector<int>> input) : n(n_), memo(1 << n_, -2) {
        for (auto const &e : input) {
            unsigned mask = 0;
            for (int x : e) mask |= 1u << x;
            edges.push_back(mask);
        }
    }
    int solve(unsigned remaining) {
        int &ans = memo[remaining];
        if (ans != -2) return ans;
        for (unsigned e : edges) if ((remaining & e) == 0) return ans = -1;
        unsigned children = 0;
        for (int v = 0; v < n; ++v) if (remaining & (1u << v)) {
            int child = solve(remaining ^ (1u << v));
            if (child >= 0) children |= 1u << child;
        }
        int mex = 0;
        while (children & (1u << mex)) ++mex;
        return ans = mex;
    }
    void check(const string &name, int expected) {
        unsigned full = (1u << n) - 1;
        assert(solve(full) == expected);
        unsigned first_values = 0;
        for (int v = 0; v < n; ++v) first_values |= 1u << solve(full ^ (1u << v));
        assert(first_values == ((1u << expected) - 1));
        cout << name << " root=" << expected << " spectrum=0.." << expected - 1 << "\n";
        for (unsigned occupied = 0; occupied <= full; ++occupied) {
            if (occupied) cout << ',';
            cout << solve(full ^ occupied);
        }
        cout << '\n';
    }
};
int main() {
    Game c(9, {{1,3,4}, {1,7}, {3,5,7,8}, {2,5,7}, {5,6}});
    c.check("rank_le4_five_edges_9_nimber7", 7);
    Game a(12, {{1,3,4,8}, {3,5,9,10}, {0,1,9,11}, {0,2,7,8}, {6,7,9,11}});
    a.check("rank4_five_edges_12", 6);
    Game b(8, {{1,4}, {2,5,7}, {0,1,5,6}, {6,7}, {1,3,6}});
    b.check("rank_le4_five_edges_8", 6);
}
