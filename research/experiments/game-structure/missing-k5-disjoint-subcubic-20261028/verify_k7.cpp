// Exact k=7 base: missing graph D=K5 disjoint K2.
// Other base D=K5 disjoint 2K1 is covered by the previous K5 theorem.
// All positive pair types have multiplicity 1 or 2; private leaves 0,1,2.
// No proposed Grundy formula is used in the recursive mex calculation.
// Compile: g++ -std=c++17 -O3 -Wall -Wextra verify_k7.cpp -o verify_k7
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
using U64 = uint64_t;
using U128 = __uint128_t;
constexpr int K = 7, N = 1 << K;

int main() {
    vector<int> sig;
    for (int i = 0; i < K; ++i) sig.push_back(1 << i);
    for (int i = 0; i < K; ++i)
        for (int j = i + 1; j < K; ++j)
            if (!(i < 5 && j < 5) && !(i == 5 && j == 6))
                sig.push_back((1 << i) | (1 << j));
    if (sig.size() != 17) return 2; // 7 leaf types, 10 pair types
    array<U128, N> hit{};
    for (int a = 1; a < N; ++a)
        for (int s = 1; s < N; ++s)
            if (s & a) hit[a] |= U128(1) << s;

    constexpr U64 CASES = 2187ULL * (1ULL << 10);
    U64 failures = 0;
    int maxg = 0;
    array<int, N> dp{};
    for (U64 code = 0; code < CASES; ++code) {
        U64 q = code;
        U128 odd = 0;
        int z[K] = {}, u = 0;
        vector<int> present;
        present.reserve(sig.size());
        for (int j = 0; j < (int)sig.size(); ++j) {
            int v;
            if (j < K) { v = int(q % 3); q /= 3; }
            else { v = 1 + int(q & 1); q >>= 1; }
            if (v) present.push_back(sig[j]);
            if (v & 1) {
                odd ^= hit[sig[j]];
                u ^= 1;
                for (int i = 0; i < K; ++i)
                    if (sig[j] & (1 << i)) z[i] ^= 1;
            }
        }
        dp[0] = 0;
        for (int a = 1; a < N; ++a) {
            int ua = int((odd >> a) & 1), seen = 0;
            // Clique move leaves only isolated independent vertices.
            for (int i = 0; i < K; ++i)
                if (a & (1 << i)) seen |= 1 << (ua ^ z[i]);
            // Independent move: delete the currently adjacent clique points.
            // Account for newly isolated groups and the selected vertex.
            for (int s : present) if (s & a) {
                int b = a & ~s;
                int child = dp[b] ^ ua ^ int((odd >> b) & 1) ^ 1;
                seen |= 1 << child;
            }
            int g = 0;
            while (seen & (1 << g)) ++g;
            dp[a] = g;
        }
        int expected = 1 ^ u ^ z[0];
        for (int i = 1; i < K; ++i)
            if (z[i] != z[0]) { expected = 2 + u; break; }
        int actual = dp[N - 1];
        if (actual != expected) {
            ++failures;
            cerr << "mismatch code=" << code << " expected=" << expected
                 << " actual=" << actual << '\n';
            return 1;
        }
        if (actual > maxg) maxg = actual;
    }
    cout << "k=7 D=K5+K2 cases=" << CASES
         << " mismatches=" << failures << " max_grundy=" << maxg << '\n';
    return failures ? 1 : 0;
}
