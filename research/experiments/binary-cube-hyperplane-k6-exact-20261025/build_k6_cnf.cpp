// Exhaustive enumeration of affinely dependent subsets of the binary 6-cube
// and CNF construction for the question "does a 10-vertex set exist in
// which every 7-subset is affinely independent?" (i.e. K_6 >= 10?).
//
// A size-s subset (s <= 7) is affinely dependent iff the s x 7 augmented
// matrix with rows (1, x) has rank < s.  The rank is computed modulo the
// prime p = 2^61 - 1.  Every s x s minor of that matrix is a 0/1 matrix
// minor bounded by Hadamard by 7^(7/2) = 907 < p, so a minor vanishes over
// the integers iff it vanishes mod p: the modular rank equals the rational
// rank exactly.  In --count mode every predicate call is cross-checked
// against an independent elimination modulo 1000000007.
//
// Modes:
//   --count           print dependent counts for subset sizes 4..7
//   --cnf K out.cnf   write DIMACS with variables x_0..x_63, one clause
//                     (not q1 ... not q7) per dependent 7-subset, plus a
//                     Sinz sequential-counter encoding of "exactly K"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

namespace {

using u64 = std::uint64_t;
using u128 = unsigned __int128;

constexpr u64 P1 = (1ULL << 61) - 1;
constexpr u64 P2 = 1000000007ULL;

u64 mul(u64 a, u64 b, u64 p) {
    return static_cast<u64>((static_cast<u128>(a) * b) % p);
}

// Rank of the s x 7 augmented matrix modulo p (p odd prime).
int rank_mod(const int* pts, int s, u64 p) {
    u64 a[7][7];
    for (int i = 0; i < s; ++i) {
        a[i][0] = 1;
        for (int c = 0; c < 6; ++c) a[i][c + 1] = (pts[i] >> c) & 1;
    }
    int rank = 0;
    for (int j = 0; j < 7 && rank < s; ++j) {
        int piv = -1;
        for (int i = rank; i < s; ++i)
            if (a[i][j] % p != 0) { piv = i; break; }
        if (piv < 0) continue;
        if (piv != rank)
            for (int k = j; k < 7; ++k) std::swap(a[rank][k], a[piv][k]);
        const u64 g = a[rank][j] % p;
        for (int i = rank + 1; i < s; ++i) {
            const u64 f = a[i][j] % p;
            if (f == 0) continue;
            for (int k = j; k < 7; ++k)
                a[i][k] = (mul(a[i][k], g, p) + p -
                           mul(f, a[rank][k], p)) % p;
        }
        ++rank;
    }
    return rank;
}

bool dependent(const int* pts, int s) {
    return rank_mod(pts, s, P1) < s;
}

bool dependent_check(const int* pts, int s) {
    return rank_mod(pts, s, P2) < s;
}

// Enumerates all size-7 subsets; body receives the vertex array.
template <typename F>
void for_all_7(int n, F&& body) {
    int idx[7];
    for (int i0 = 0; i0 < n; ++i0) {
        idx[0] = i0;
        for (int i1 = i0 + 1; i1 < n; ++i1) {
            idx[1] = i1;
            for (int i2 = i1 + 1; i2 < n; ++i2) {
                idx[2] = i2;
                for (int i3 = i2 + 1; i3 < n; ++i3) {
                    idx[3] = i3;
                    for (int i4 = i3 + 1; i4 < n; ++i4) {
                        idx[4] = i4;
                        for (int i5 = i4 + 1; i5 < n; ++i5) {
                            idx[5] = i5;
                            for (int i6 = i5 + 1; i6 < n; ++i6) {
                                idx[6] = i6;
                                body(idx);
                            }
                        }
                    }
                }
            }
        }
    }
}

template <typename F>
void for_all_size(int n, int s, F&& body) {
    std::vector<int> c(s);
    for (int i = 0; i < s; ++i) c[i] = i;
    int idx[7];
    for (;;) {
        for (int t = 0; t < s; ++t) idx[t] = c[t];
        body(idx);
        int i = s - 1;
        while (i >= 0 && c[i] == n - (s - i)) --i;
        if (i < 0) break;
        c[i]++;
        for (int j = i + 1; j < s; ++j) c[j] = c[j - 1] + 1;
    }
}

// Builds Sinz sequential at-most-k counter clauses for lits.
void at_most_k_clauses(const std::vector<int>& lits, int k, int* next_var,
                       std::vector<std::vector<int>>& out) {
    const int n = (int)lits.size();
    if (k >= n) return;
    std::vector<std::vector<int>> s(n, std::vector<int>(k, 0));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < k; ++j) s[i][j] = (*next_var)++;
    out.push_back({-lits[0], s[0][0]});
    for (int j = 1; j < k; ++j) out.push_back({-s[0][j]});
    for (int i = 1; i < n; ++i) {
        out.push_back({-lits[i], s[i][0]});
        out.push_back({-s[i - 1][0], s[i][0]});
        for (int j = 1; j < k; ++j) {
            out.push_back({-s[i - 1][j], s[i][j]});
            out.push_back({-lits[i], -s[i - 1][j - 1], s[i][j]});
        }
        out.push_back({-lits[i], -s[i - 1][k - 1]});
    }
}

}  // namespace

int main(int argc, char** argv) {
    const int n = 64;
    if (argc == 2 && std::string(argv[1]) == "--count") {
        long long dep[8] = {0, 0, 0, 0, 0, 0, 0, 0};
        for (int s = 4; s <= 6; ++s) {
            for_all_size(n, s, [&](const int* p) {
                const bool a = dependent(p, s);
                if (a != dependent_check(p, s)) {
                    fprintf(stderr, "PREDICATE MISMATCH size %d\n", s);
                    exit(1);
                }
                if (a) ++dep[s];
            });
            printf("size %d dependent: %lld\n", s, dep[s]);
            fflush(stdout);
        }
        for_all_7(n, [&](const int* p) {
            const bool a = dependent(p, 7);
            if (a != dependent_check(p, 7)) {
                fprintf(stderr, "PREDICATE MISMATCH size 7 on %d %d %d %d "
                                "%d %d %d\n", p[0], p[1], p[2], p[3], p[4],
                        p[5], p[6]);
                exit(1);
            }
            if (a) ++dep[7];
        });
        printf("size 7 dependent: %lld of C(64,7)=74973686\n", dep[7]);
        return 0;
    }
    if (argc == 4 && std::string(argv[1]) == "--cnf") {
        const int K = atoi(argv[2]);
        if (K < 0 || K > n) { fprintf(stderr, "bad K\n"); return 2; }
        long long dep7 = 0;
        for_all_7(n, [&](const int* p) {
            if (dependent(p, 7)) ++dep7;
        });
        FILE* f = fopen(argv[3], "w");
        if (!f) { fprintf(stderr, "cannot open %s\n", argv[3]); return 2; }
        int next_var = n + 1;
        std::vector<std::vector<int>> counter_clauses;
        {
            std::vector<int> lits;
            for (int i = 0; i < n; ++i) lits.push_back(i + 1);
            at_most_k_clauses(lits, K, &next_var, counter_clauses);
        }
        {
            std::vector<int> lits;
            for (int i = 0; i < n; ++i) lits.push_back(-(i + 1));
            at_most_k_clauses(lits, n - K, &next_var, counter_clauses);
        }
        const long long total = (long long)counter_clauses.size() + dep7;
        fprintf(f, "p cnf %d %lld\n", next_var - 1, total);
        for (const auto& c : counter_clauses) {
            for (int lit : c) fprintf(f, "%d ", lit);
            fprintf(f, "0\n");
        }
        for_all_7(n, [&](const int* p) {
            if (dependent(p, 7)) {
                fprintf(f, "%d %d %d %d %d %d %d 0\n", -(p[0] + 1),
                        -(p[1] + 1), -(p[2] + 1), -(p[3] + 1), -(p[4] + 1),
                        -(p[5] + 1), -(p[6] + 1));
            }
        });
        fclose(f);
        fprintf(stderr, "cnf: %d vars, %lld clauses (dep7=%lld)\n",
                next_var - 1, total, dep7);
        return 0;
    }
    fprintf(stderr, "usage: build_k6_cnf --count | --cnf K out.cnf\n");
    return 2;
}
