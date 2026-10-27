// Exhaustive named-vertex Node Kayles verifier for k=3,4 finite base cases.
// Independent of the Python clique-subset recurrence; requires C++17.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <unordered_map>
#include <vector>

using std::uint32_t;
static int k;
static std::vector<uint32_t> closed;
static std::unordered_map<uint32_t, unsigned char> memo;

static int grundy(uint32_t mask) {
    if (!mask) return 0;
    auto it = memo.find(mask);
    if (it != memo.end()) return it->second;
    unsigned int child_values = 0;
    for (uint32_t remaining = mask; remaining; remaining &= remaining - 1) {
        int v = __builtin_ctz(remaining);
        int child = grundy(mask & ~closed[v]);
        child_values |= 1u << child;
    }
    int result = 0;
    while (child_values & (1u << result)) ++result;
    memo.emplace(mask, static_cast<unsigned char>(result));
    return result;
}

static int predicted(const std::vector<int>& pairs, const std::vector<int>& leaves) {
    std::vector<int> z(k);
    int u = 0;
    for (int i = 0; i < k; ++i) {
        z[i] = leaves[i] & 1;
        u ^= z[i];
    }
    int index = 0;
    for (int i = 0; i < k; ++i) {
        for (int j = i + 1; j < k; ++j) {
            int p = pairs[index++] & 1;
            z[i] ^= p;
            z[j] ^= p;
            u ^= p;
        }
    }
    bool uniform = std::all_of(z.begin(), z.end(), [&](int x) { return x == z[0]; });
    return uniform ? 1 - (u ^ z[0]) : 2 + u;
}

int main() {
    for (k = 3; k <= 4; ++k) {
        const int pair_count = k * (k - 1) / 2;
        const int pair_patterns = 1 << pair_count;
        int leaf_patterns = 1;
        for (int i = 0; i < k; ++i) leaf_patterns *= 3;
        long long states = 0;
        long long cases = 0;
        long long histogram[4] = {0, 0, 0, 0};
        for (int pm = 0; pm < pair_patterns; ++pm) {
            for (int lm = 0; lm < leaf_patterns; ++lm) {
                std::vector<int> pairs(pair_count), leaves(k);
                for (int i = 0; i < pair_count; ++i) pairs[i] = 1 + ((pm >> i) & 1);
                int x = lm;
                for (int i = 0; i < k; ++i) {
                    leaves[i] = x % 3;
                    x /= 3;
                }
                int n = k + std::accumulate(pairs.begin(), pairs.end(), 0)
                          + std::accumulate(leaves.begin(), leaves.end(), 0);
                // n<=24 in the exhaustive base cases.
                closed.assign(n, 0);
                for (int i = 0; i < n; ++i) closed[i] = 1u << i;
                for (int i = 0; i < k; ++i) {
                    for (int j = i + 1; j < k; ++j) {
                        closed[i] |= 1u << j;
                        closed[j] |= 1u << i;
                    }
                }
                int id = k;
                for (int i = 0; i < k; ++i) {
                    for (int j = 0; j < leaves[i]; ++j, ++id) {
                        closed[i] |= 1u << id;
                        closed[id] |= 1u << i;
                    }
                }
                int pi = 0;
                for (int i = 0; i < k; ++i) {
                    for (int j = i + 1; j < k; ++j, ++pi) {
                        for (int h = 0; h < pairs[pi]; ++h, ++id) {
                            closed[i] |= 1u << id;
                            closed[j] |= 1u << id;
                            closed[id] |= (1u << i) | (1u << j);
                        }
                    }
                }
                if (id != n) return 2;
                memo.clear();
                int actual = grundy((1u << n) - 1);
                int expected = predicted(pairs, leaves);
                if (actual != expected) {
                    std::cerr << "FAIL k=" << k << " pair-pattern=" << pm
                              << " leaf-pattern=" << lm << " actual=" << actual
                              << " expected=" << expected << '\n';
                    return 1;
                }
                ++histogram[actual];
                states += memo.size();
                ++cases;
            }
        }
        std::cout << "PASS k=" << k << " cases=" << cases << " nonempty-states=" << states
                  << " g-histogram=" << histogram[0] << ',' << histogram[1] << ','
                  << histogram[2] << ',' << histogram[3] << '\n';
    }
}
