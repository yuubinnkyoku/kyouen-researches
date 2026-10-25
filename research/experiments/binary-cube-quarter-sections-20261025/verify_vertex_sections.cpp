// Independent finite check of exact-quarter vertex-section counts.
// Enumerates all signed integer normals with nonzero entries in [-4,4],
// every attainable intercept, and the resulting vertex subsets.
// It does NOT prove completeness for arbitrary real coefficients.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <vector>

int main() {
    const int bound = 4;
    const int expected[] = {0, 0, 4, 16, 92, 80};
    for (int k = 2; k <= 5; ++k) {
        std::set<std::uint32_t> sections;
        std::vector<int> weights(k);
        std::uint64_t normals = 0;
        auto visit = [&](auto&& self, int pos) -> void {
            if (pos == k) {
                ++normals;
                int n = 1 << k;
                std::vector<int> sums(n, 0);
                for (int x = 0; x < n; ++x)
                    for (int i = 0; i < k; ++i)
                        if ((x >> i) & 1) sums[x] += weights[i];
                for (int b : sums) {
                    std::uint32_t mask = 0;
                    for (int x = 0; x < n; ++x)
                        if (sums[x] == b) mask |= (std::uint32_t(1) << x);
                    if (__builtin_popcount(mask) * 4 == n)
                        sections.insert(mask);
                }
                return;
            }
            for (int w = -bound; w <= bound; ++w) {
                if (!w) continue;
                weights[pos] = w;
                self(self, pos + 1);
            }
        };
        visit(visit, 0);
        std::cout << "support=" << k << " normals=" << normals
                  << " quarter_sections=" << sections.size() << '\n';
        if (int(sections.size()) != expected[k])
            throw std::runtime_error("quarter section count mismatch");
    }
}
