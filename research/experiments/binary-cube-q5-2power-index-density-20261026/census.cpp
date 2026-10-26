#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

// Exact modular arithmetic for p < 1e8: products are < 1e16 < 2^64.
static std::uint64_t power(std::uint64_t a, std::uint64_t e, std::uint64_t p) {
    std::uint64_t ans = 1;
    while (e) {
        if (e & 1) ans = ans * a % p;
        a = a * a % p;
        e >>= 1;
    }
    return ans;
}
int main(int argc, char **argv) {
    const int limit = argc > 1 ? std::atoi(argv[1]) : 1000000;
    if (limit < 37 || limit > 100000000) return 2;
    std::vector<std::uint8_t> prime(limit, 1);
    prime[0] = prime[1] = 0;
    for (int i = 2; 1LL * i * i < limit; ++i)
        if (prime[i])
            for (int j = i * i; j < limit; j += i) prime[j] = 0;
    std::uint64_t total = 0, counts[9] = {};
    int first[9] = {};
    for (int p = 37; p < limit; p += 2) {
        if (!prime[p]) continue;
        ++total;
        int v = 0;
        for (int x = p - 1; x % 2 == 0; x /= 2) ++v;
        int max_r = std::min(8, v);
        for (int r = 1; r <= max_r; ++r) {
            bool ok = true;
            for (int a : {2, 3, 5, 7}) {
                if (power(a, (p - 1) / (1 << r), p) != 1) {
                    ok = false;
                    break;
                }
            }
            if (!ok) break;
            ++counts[r];
            if (!first[r]) first[r] = p;
        }
    }
    std::cout << "limit " << limit << " primes " << total << "\n";
    for (int r = 1; r <= 8; ++r)
        std::cout << r << " " << counts[r] << " first " << first[r] << "\n";
    if (limit == 1000000) {
        if (total != 78487 || counts[1] != 4831 || counts[2] != 112 ||
            counts[3] != 6 || counts[4] != 0) return 1;
    }
    if (limit == 100000000) {
        if (total != 5761444 || counts[1] != 359464 || counts[2] != 10846 ||
            counts[3] != 630 || counts[4] != 14 || counts[5] != 0) return 1;
    }
    return 0;
}
