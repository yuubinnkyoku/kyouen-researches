// Strong solution of the binary 5-cube hyperplane game (v4, rank-check DFS).
//
// Game: V_5={0,1}^5, 32 vertices.  Forbidden: 6 points lying on a common
// real affine hyperplane (degenerate included), i.e. a position is safe iff
// EVERY 6-subset of it is affinely independent.  Dependencies of fewer than
// 6 points are legal positions, so the minimal banned sets are exactly all
// dependent 6-subsets (no circuit reduction is possible).
//
// DFS over increasing vertex indices; when adding v to a mask of popcount
// k, only the C(k,5) 6-subsets containing v can newly violate safety, and
// each is checked by one exact rank computation (mod 2^61-1 with a
// Hadamard-bound equivalence).  Normal Grundy by popcount-ordered DP over
// recorded children; misere outcomes in the same sweep.
#include <algorithm>
#include <array>
#include <cstdio>
#include <cstdint>
#include <unordered_map>
#include <vector>

namespace {

using u64 = std::uint64_t;
using u128 = unsigned __int128;
using u32 = std::uint32_t;
using Mask = u32;

constexpr u64 P = (1ULL << 61) - 1;
constexpr int D = 5;
constexpr int N = 1 << D;  // 32

u64 mulm(u64 a, u64 b) {
    return static_cast<u64>((static_cast<u128>(a) * b) % P);
}

// rank of the s x 6 augmented matrix with rows (1, x), s <= 6.
int rank_aug(const int* pts, int s) {
    u64 a[6][7];
    for (int i = 0; i < s; ++i) {
        a[i][0] = 1;
        for (int c = 0; c < D; ++c) a[i][c + 1] = (pts[i] >> c) & 1;
    }
    int rank = 0;
    for (int j = 0; j <= D && rank < s; ++j) {
        int piv = -1;
        for (int i = rank; i < s; ++i)
            if (a[i][j] != 0) { piv = i; break; }
        if (piv < 0) continue;
        if (piv != rank)
            for (int k = j; k <= D; ++k) std::swap(a[rank][k], a[piv][k]);
        const u64 g = a[rank][j];
        for (int i = rank + 1; i < s; ++i) {
            const u64 f = a[i][j];
            if (f == 0) continue;
            for (int k = j; k <= D; ++k)
                a[i][k] = (mulm(a[i][k], g) + P - mulm(f, a[rank][k])) % P;
        }
        ++rank;
    }
    return rank;
}

// m (popcount k) plus vertex v: check only 6-subsets containing v.
bool adding_keeps_safe(Mask m, int v) {
    int pts[8];
    int k = 0;
    for (int i = 0; i < N; ++i)
        if (m & (1u << i)) pts[k++] = i;
    pts[k++] = v;
    // 6-subsets containing v: v + 5 of the k-1 old points
    std::array<int, 5> comb;
    const int n = k - 1;  // old points available (indices 0..n-1 of pts)
    if (n < 5) return true;  // fewer than 6 points total: cannot violate
    for (int i = 0; i < 5; ++i) comb[i] = i;
    for (;;) {
        int six[6];
        for (int i = 0; i < 5; ++i) six[i] = pts[comb[i]];
        six[5] = v;
        if (rank_aug(six, 6) < 6) return false;
        int i = 4;
        while (i >= 0 && comb[i] == n - (5 - i)) --i;
        if (i < 0) break;
        comb[i]++;
        for (int j = i + 1; j < 5; ++j) comb[j] = comb[j - 1] + 1;
    }
    return true;
}

std::vector<Mask> order;
std::unordered_map<Mask, int> index_of;

void dfs(Mask m, int last) {
    index_of[m] = (int)order.size();
    order.push_back(m);
    for (int v = last + 1; v < N; ++v)
        if (adding_keeps_safe(m, v)) dfs(m | (1u << v), v);
}

}  // namespace

int main() {
    dfs(0, -1);
    printf("safe positions: %zu\n", order.size());
    std::array<long long, 40> by_pop{};
    for (Mask m : order) ++by_pop[__builtin_popcount(m)];
    for (int k = 0; k < 40; ++k)
        if (by_pop[k]) printf("  popcount %d: %lld\n", k, by_pop[k]);
    std::vector<int> idx_by_pop(order.size());
    for (size_t i = 0; i < order.size(); ++i) idx_by_pop[i] = (int)i;
    std::sort(idx_by_pop.begin(), idx_by_pop.end(), [&](int a, int b) {
        return __builtin_popcount(order[a]) > __builtin_popcount(order[b]);
    });
    std::vector<int> grundy(order.size(), 0);
    std::vector<char> outcome(order.size(), 0);
    long long p_wins = 0;
    for (int i : idx_by_pop) {
        // game children: add any unused vertex keeping safety
        const Mask m = order[i];
        int seen[9] = {0};
        bool any_p = false;
        bool has_move = false;
        for (int v = 0; v < N; ++v) {
            if (m & (1u << v)) continue;
            if (!adding_keeps_safe(m, v)) continue;
            has_move = true;
            const int ci = index_of[m | (1u << v)];
            if (grundy[ci] < 9) seen[grundy[ci]] = 1;
            if (outcome[ci]) any_p = true;
        }
        int g = 0;
        while (g < 9 && seen[g]) ++g;
        grundy[i] = g;
        outcome[i] = (!has_move || any_p) ? 0 : 1;
        if (outcome[i]) ++p_wins;
    }
    std::array<long long, 10> ghist{};
    for (size_t i = 0; i < order.size(); ++i)
        if (grundy[i] < 10) ++ghist[grundy[i]];
    for (int g = 0; g < 10; ++g)
        if (ghist[g]) printf("  g=%d: %lld\n", g, ghist[g]);
    printf("empty-board normal Grundy: %d\n", grundy[index_of[0]]);
    printf("winning first moves (child g=0):");
    for (int v = 0; v < N; ++v)
        if (grundy[index_of[1u << v]] == 0) printf(" %d", v);
    printf("\n");
    printf("misere: empty board %s; P positions %lld\n",
           outcome[index_of[0]] ? "P (second-player-win)"
                                : "N (first-player-win)",
           p_wins);
    printf("winning first moves misere (child P):");
    for (int v = 0; v < N; ++v)
        if (outcome[index_of[1u << v]]) printf(" %d", v);
    printf("\n");
    return 0;
}
