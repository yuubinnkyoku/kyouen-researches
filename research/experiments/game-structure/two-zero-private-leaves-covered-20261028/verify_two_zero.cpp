// Exhaustive parity-quotient Node Kayles check for at most two zero private-leaf counts.
// Each clique vertex must have a nonempty neighborhood in the independent set.
// Counts 0,1,2 suffice by the proved independent-twin parity theorem (K0336).
// c++ -std=c++17 -O3 -Wall -Wextra -pedantic verify_two_zero.cpp -o /tmp/two_zero
// /tmp/two_zero [max_k]     (default max_k=5)
#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdlib>
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>
using namespace std;

int main(int argc, char** argv) {
    const int maxk = argc > 1 ? atoi(argv[1]) : 5;
    const long long expected[] = {0, 0, 0, 636, 50400, 11164608};
    for (int k = 3; k <= maxk; ++k) {
        vector<pair<int, int>> pairs;
        for (int i = 0; i < k; ++i)
            for (int j = i + 1; j < k; ++j) pairs.emplace_back(i, j);
        long long pairmax = 1, leafmax = 1;
        for (size_t j = 0; j < pairs.size(); ++j) pairmax *= 3;
        for (int i = 0; i < k; ++i) leafmax *= 3;
        long long tested = 0, skipped = 0, bad = 0;
        int maxg = 0;
        auto start = chrono::steady_clock::now();
        for (long long L = 0; L < leafmax; ++L) {
            int t[10] = {};
            long long y = L;
            int zeros = 0;
            for (int i = 0; i < k; ++i) {
                t[i] = int(y % 3); y /= 3;
                zeros += t[i] == 0;
            }
            for (long long P = 0; P < pairmax; ++P) {
                int types[80], counts[80], degree[10] = {}, ntypes = 0;
                for (int i = 0; i < k; ++i) if (t[i]) {
                    types[ntypes] = 1 << i;
                    counts[ntypes++] = t[i];
                    degree[i]++;
                }
                long long x = P;
                for (auto [i, j] : pairs) {
                    int r = int(x % 3); x /= 3;
                    if (r) {
                        types[ntypes] = (1 << i) | (1 << j);
                        counts[ntypes++] = r;
                        degree[i]++; degree[j]++;
                    }
                }
                bool covered = true;
                for (int i = 0; i < k; ++i) covered &= degree[i] > 0;
                if (zeros > 2 || !covered) { ++skipped; continue; }
                const int states = 1 << k;
                int active[128] = {}, incident[10] = {}, grundy[128] = {};
                for (int j = 0; j < ntypes; ++j) {
                    for (int i = 0; i < k; ++i)
                        if (types[j] & (1 << i)) incident[i] ^= counts[j] & 1;
                    for (int S = 1; S < states; ++S)
                        if (types[j] & S) active[S] ^= counts[j] & 1;
                }
                // Direct mex on every surviving-clique mask; no formula in recurrence.
                for (int S = 1; S < states; ++S) {
                    uint32_t seen = 0;
                    for (int i = 0; i < k; ++i) if (S & (1 << i))
                        seen |= 1u << (active[S] ^ incident[i]);
                    for (int j = 0; j < ntypes; ++j) if (types[j] & S) {
                        int T = S & ~types[j];
                        int child = grundy[T] ^ (active[S] ^ active[T] ^ 1);
                        assert(child < 31);
                        seen |= 1u << child;
                    }
                    while (seen & (1u << grundy[S])) ++grundy[S];
                }
                int u = active[states - 1];
                bool uniform = true;
                for (int i = 1; i < k; ++i) uniform &= incident[i] == incident[0];
                int predicted = uniform ? (1 ^ u ^ incident[0]) : (2 + u);
                int actual = grundy[states - 1];
                maxg = max(maxg, actual);
                ++tested;
                if (actual != predicted) {
                    ++bad;
                    if (bad <= 5) cerr << "FAIL k=" << k << " L=" << L << " P=" << P
                                       << " actual=" << actual << " predicted=" << predicted << '\n';
                }
            }
        }
        cout << "k=" << k << " tested=" << tested << " skipped=" << skipped
             << " mismatches=" << bad << " maxGrundy=" << maxg
             << " seconds=" << chrono::duration<double>(chrono::steady_clock::now()-start).count() << '\n';
        if (k <= 5) assert(tested == expected[k]);
        assert(bad == 0 && maxg == 3);
    }
}
