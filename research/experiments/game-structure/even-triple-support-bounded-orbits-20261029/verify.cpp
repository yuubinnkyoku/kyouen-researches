// Complete orbit enumeration for bounded even triple-support deletion in split-graph Node Kayles.
// Build: c++ -std=c++17 -O3 -Wall -Wextra -pedantic verify.cpp -o /tmp/verify
// Run:   /tmp/verify 5 && /tmp/verify 6
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;

struct RemainingSolver {
    vector<uint32_t> closed;
    vector<int8_t> memo;
    int rec(uint32_t alive) {
        if (!alive) return 0;
        int8_t &cached = memo[alive];
        if (cached >= 0) return cached;
        uint32_t seen = 0, todo = alive;
        while (todo) {
            int v = __builtin_ctz(todo);
            todo &= todo - 1;
            seen |= 1u << rec(alive & ~closed[v]);
        }
        return cached = __builtin_ctz(~seen);
    }
    int solve(int k, const vector<int> &supports) {
        int n = k + (int)supports.size();
        assert(n < 31);
        closed.assign(n, 0);
        for (int c = 0; c < k; ++c) closed[c] = (1u << k) - 1;
        for (int j = 0; j < (int)supports.size(); ++j) {
            int v = k + j;
            closed[v] = 1u << v;
            for (int c = 0; c < k; ++c) if (supports[j] & (1 << c)) {
                closed[v] |= 1u << c;
                closed[c] |= 1u << v;
            }
        }
        memo.assign(1u << n, -1);
        return rec((1u << n) - 1);
    }
};

// Independent recurrence: select independent leaves; selecting a compatible
// clique center ends center play, leaving isolated unselected non-neighbors.
struct OccupiedLeafSolver {
    int k, n;
    uint32_t full;
    vector<int> supports;
    vector<uint32_t> nonneighbors;
    vector<int8_t> memo;
    int rec(uint32_t chosen) {
        int8_t &cached = memo[chosen];
        if (cached >= 0) return cached;
        uint32_t seen = 0, todo = full & ~chosen;
        while (todo) {
            int j = __builtin_ctz(todo);
            todo &= todo - 1;
            seen |= 1u << rec(chosen | (1u << j));
        }
        for (int c = 0; c < k; ++c) {
            bool legal = true;
            for (int j = 0; j < n; ++j)
                if ((chosen & (1u << j)) && (supports[j] & (1 << c))) {
                    legal = false;
                    break;
                }
            if (legal) {
                int remaining_isolated = __builtin_popcount(nonneighbors[c] & ~chosen);
                seen |= 1u << (remaining_isolated & 1);
            }
        }
        return cached = __builtin_ctz(~seen);
    }
    int solve(int K, const vector<int> &s) {
        k = K;
        supports = s;
        n = (int)s.size();
        full = (1u << n) - 1;
        nonneighbors.assign(k, 0);
        for (int c = 0; c < k; ++c)
            for (int j = 0; j < n; ++j)
                if (!(supports[j] & (1 << c))) nonneighbors[c] |= 1u << j;
        memo.assign(1u << n, -1);
        return rec(0);
    }
};

int main(int argc, char **argv) {
    if (argc != 2 || (argv[1][0] != '5' && argv[1][0] != '6')) {
        cerr << "usage: verify 5|6\n";
        return 2;
    }
    int k = atoi(argv[1]);
    int bound = k == 5 ? 7 : 5;
    const int triple = 7; // center indices 0,1,2
    vector<int> types;
    for (int s = 1; s < (1 << k); ++s)
        if (__builtin_popcount((unsigned)s) >= 2) types.push_back(s);
    vector<vector<int>> stabilizer;
    vector<int> perm(k);
    iota(perm.begin(), perm.end(), 0);
    do {
        int image = 0;
        for (int c = 0; c < k; ++c) if (triple & (1 << c)) image |= 1 << perm[c];
        if (image != triple) continue;
        vector<int> mapping(types.size());
        for (int j = 0; j < (int)types.size(); ++j) {
            int transformed = 0;
            for (int c = 0; c < k; ++c)
                if (types[j] & (1 << c)) transformed |= 1 << perm[c];
            mapping[j] = lower_bound(types.begin(), types.end(), transformed) - types.begin();
        }
        stabilizer.push_back(mapping);
    } while (next_permutation(perm.begin(), perm.end()));
    assert(stabilizer.size() == (k == 5 ? 12u : 36u));

    RemainingSolver named;
    OccupiedLeafSolver independent;
    uint64_t all = 0, representatives = 0, audited = 0;
    vector<int> odd;
    auto inspect = [&]() {
        uint64_t mask = 0;
        for (int s : odd) mask |= 1ull << (lower_bound(types.begin(), types.end(), s) - types.begin());
        ++all;
        for (const auto &mapping : stabilizer) {
            uint64_t image = 0, todo = mask;
            while (todo) {
                int j = __builtin_ctzll(todo);
                todo &= todo - 1;
                image |= 1ull << mapping[j];
            }
            if (image < mask) return;
        }
        ++representatives;
        vector<int> s;
        for (int c = 0; c < k; ++c) s.push_back(1 << c);
        s.insert(s.end(), odd.begin(), odd.end());
        int before = named.solve(k, s);
        bool audit = k == 5
            ? (odd.size() <= 5 || (odd.size() == 6 && mask % 17 == 0)
               || (odd.size() == 7 && mask % 503 == 0))
            : (odd.size() <= 3 || (odd.size() == 4 && mask % 5 == 0)
               || (odd.size() == 5 && mask % 101 == 0));
        if (audit && independent.solve(k, s) != before) {
            cerr << "independent mismatch before: mask=" << mask << "\n";
            exit(1);
        }
        s.push_back(triple);
        s.push_back(triple);
        int after = named.solve(k, s);
        if (audit) {
            ++audited;
            if (independent.solve(k, s) != after) {
                cerr << "independent mismatch after: mask=" << mask << "\n";
                exit(1);
            }
        }
        if (before != after) {
            cerr << "counterexample: k=" << k << " mask=" << mask
                 << " before=" << before << " after=" << after << "\n";
            exit(1);
        }
    };
    auto choose = [&](auto &&self, int start, int left) -> void {
        if (!left) { inspect(); return; }
        for (int i = start; i <= (int)types.size() - left; ++i) {
            odd.push_back(types[i]);
            self(self, i + 1, left - 1);
            odd.pop_back();
        }
    };
    for (int count = 0; count <= bound; ++count) choose(choose, 0, count);
    assert(all == (k == 5 ? 971712ull : 4613030ull));
    assert(representatives == (k == 5 ? 88954ull : 157754ull));
    assert(audited == (k == 5 ? 9964ull : 6342ull));
    cout << "k=" << k << " all=" << all << " orbits=" << representatives
         << " independent=" << audited << " mismatches=0\n";
}
