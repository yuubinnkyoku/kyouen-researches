// Exact fixed-order cotree-signature enumeration, n<=400.
// g(G) = mex O(G), O(G) = {g(G-N[v]) : v in V(G)}.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <stdexcept>
#include <unordered_set>
#include <vector>
using U = std::uint64_t;
int mex(U x) {
    if (~x == 0) throw std::runtime_error("option mask overflow");
    return __builtin_ctzll(~x);
}
U xor_shift(U s, int k) {
    U r = 0;
    while (s) {
        int x = __builtin_ctzll(s);
        s &= s - 1;
        if ((x ^ k) >= 64) throw std::runtime_error("option nimber >=64");
        r |= U(1) << (x ^ k);
    }
    return r;
}
int main(int argc, char** argv) {
    const int N = argc > 1 ? std::atoi(argv[1]) : 400;
    const bool dump = argc > 2 && std::string(argv[2]) == "--dump";
    if (N < 1 || N > 400) return 2;
    std::vector<std::vector<U>> D(N + 1);
    D[1] = {1}; // singleton has O={0}
    std::vector<int> first(64, -1);
    for (int n = 1; n <= N; ++n) {
        if (n > 1) {
            std::unordered_set<U> seen;
            for (int a = 1; a <= n / 2; ++a) {
                int b = n - a;
                for (U sa : D[a]) for (U sb : D[b]) {
                    seen.insert(sa | sb); // complete join
                    int ga = mex(sa), gb = mex(sb);
                    seen.insert(xor_shift(sa, gb) | xor_shift(sb, ga)); // disjoint union
                }
            }
            D[n].assign(seen.begin(), seen.end());
            std::sort(D[n].begin(), D[n].end());
        }
        for (U options : D[n]) {
            int g = mex(options);
            if (first[g] < 0) first[g] = n;
            if (dump) std::cout << n << " " << options << "\n";
        }
        if (!dump) std::cout << n << " " << D[n].size() << "\n";
    }
    std::cerr << "minima";
    for (int g = 0; g < 64; ++g)
        if (first[g] >= 0) std::cerr << " " << g << ":" << first[g];
    std::cerr << "\n";
}
