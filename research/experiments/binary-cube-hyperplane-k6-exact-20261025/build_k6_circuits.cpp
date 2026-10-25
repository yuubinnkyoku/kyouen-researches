// Counts and lists the circuits (inclusion-minimal affinely dependent
// subsets) of the binary 6-cube of sizes 4..7.  Non-minimal dependent
// subsets are implied by smaller circuits, so a CNF banning only circuits
// is equivalent to the full dependent-set CNF and much smaller.
//
// Dependency of a size-s subset (s <= 7): the s x 7 augmented matrix with
// rows (1, x) has rank < s mod p = 2^61-1.  Hadamard bound 7^3.5 < p makes
// this equivalent to rational dependency.
//
// Circuits of size s are found by keeping hash sets of dependent subsets
// of size s-1: a dependent s-subset is a circuit iff none of its s subsets
// of size s-1 is dependent.
//
// Modes:
//   --count                  print circuit counts per size
//   --cnf K out.cnf [fix0]   exactly-K CNF banning circuits of sizes 4..7;
//                            'fix0' adds the unit clause x_0, justified by
//                            the transitivity of the affine symmetry group
//                            of the cube: if any 10-point general-position
//                            set exists, one containing vertex 0 exists.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <unordered_set>
#include <vector>

namespace {

using u64 = std::uint64_t;
using u128 = unsigned __int128;

constexpr u64 P = (1ULL << 61) - 1;

u64 mulm(u64 a, u64 b) {
    return static_cast<u64>((static_cast<u128>(a) * b) % P);
}

int rank_mod(const int* pts, int s) {
    u64 a[7][7];
    for (int i = 0; i < s; ++i) {
        a[i][0] = 1;
        for (int c = 0; c < 6; ++c) a[i][c + 1] = (pts[i] >> c) & 1;
    }
    int rank = 0;
    for (int j = 0; j < 7 && rank < s; ++j) {
        int piv = -1;
        for (int i = rank; i < s; ++i)
            if (a[i][j] != 0) { piv = i; break; }
        if (piv < 0) continue;
        if (piv != rank)
            for (int k = j; k < 7; ++k) std::swap(a[rank][k], a[piv][k]);
        const u64 g = a[rank][j];
        for (int i = rank + 1; i < s; ++i) {
            const u64 f = a[i][j];
            if (f == 0) continue;
            for (int k = j; k < 7; ++k)
                a[i][k] = (mulm(a[i][k], g) + P - mulm(f, a[rank][k])) % P;
        }
        ++rank;
    }
    return rank;
}

bool dependent(const int* pts, int s) { return rank_mod(pts, s) < s; }

// Key for an s-subset of {0..63}: packed vertices.
u64 subset_key(const int* pts, int s) {
    u64 key = 0;
    for (int i = 0; i < s; ++i) key = key * 64 + (u64)pts[i];
    return key;
}

void unpack_key(u64 key, int s, int* pts) {
    for (int i = s - 1; i >= 0; --i) { pts[i] = (int)(key % 64); key /= 64; }
}

// True iff at least one (s-1)-subset of pts is dependent.
bool has_dependent_subset(const int* pts, int s,
                          const std::unordered_set<u64>& dep_prev) {
    int sub[7];
    for (int skip = 0; skip < s; ++skip) {
        int t = 0;
        for (int i = 0; i < s; ++i)
            if (i != skip) sub[t++] = pts[i];
        if (dep_prev.count(subset_key(sub, s - 1))) return true;
    }
    return false;
}

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
    // Pass 1: dependent sets of sizes 4 and 5 (small enough to hash).
    std::unordered_set<u64> dep4, dep5;
    long long cnt_dep4 = 0, cnt_dep5 = 0, cnt_dep6 = 0;
    for_all_size(n, 4, [&](const int* p) {
        if (dependent(p, 4)) {
            ++cnt_dep4;
            dep4.insert(subset_key(p, 4));
        }
    });
    for_all_size(n, 5, [&](const int* p) {
        if (dependent(p, 5)) {
            ++cnt_dep5;
            dep5.insert(subset_key(p, 5));
        }
    });
    long long circuits4 = cnt_dep4;  // all size-4 dependent sets are circuits
    long long circuits5 = 0;
    for_all_size(n, 5, [&](const int* p) {
        if (dependent(p, 5) && !has_dependent_subset(p, 5, dep4))
            ++circuits5;
    });
    // Pass over 6-subsets: dependent ones that avoid dependent 5-subsets are
    // circuits.  Store dependent 6-subsets for the 7-pass.
    std::unordered_set<u64> dep6;
    dep6.reserve(1 << 25);
    long long circuits6 = 0;
    for_all_size(n, 6, [&](const int* p) {
        if (dependent(p, 6)) {
            ++cnt_dep6;
            dep6.insert(subset_key(p, 6));
            if (!has_dependent_subset(p, 6, dep5)) ++circuits6;
        }
    });
    dep4.clear();
    dep5.clear();
    long long circuits7 = 0;
    for_all_7(n, [&](const int* p) {
        if (dependent(p, 7) && !has_dependent_subset(p, 7, dep6))
            ++circuits7;
    });
    printf("dependent: 4->%lld 5->%lld 6->%lld\n", cnt_dep4, cnt_dep5, cnt_dep6);
    printf("circuits:  4->%lld 5->%lld 6->%lld 7->%lld\n",
           circuits4, circuits5, circuits6, circuits7);
    if (argc >= 4 && std::string(argv[1]) == "--cnf") {
        const int K = atoi(argv[2]);
        if (K < 0 || K > n) { fprintf(stderr, "bad K\n"); return 2; }
        const bool fix0 = (argc == 5 && std::string(argv[4]) == "fix0");
        if (argc > 5 || (argc == 5 && !fix0)) {
            fprintf(stderr, "bad extra args\n");
            return 2;
        }
        // Re-run the circuit filters, streaming clauses.
        FILE* f = fopen(argv[3], "w");
        if (!f) { fprintf(stderr, "cannot open %s\n", argv[3]); return 2; }
        // Collect all circuits first (they are few) to know the clause count.
        std::vector<std::vector<int>> circuits;
        for_all_size(n, 4, [&](const int* p) {
            if (dependent(p, 4))
                circuits.push_back({p[0], p[1], p[2], p[3]});
        });
        for_all_size(n, 5, [&](const int* p) {
            if (dependent(p, 5) && !has_dependent_subset(p, 5, dep4)) {}
        });
        // dep4/dep5 were cleared; rebuild what is needed.
        std::unordered_set<u64> d4, d5;
        for_all_size(n, 4, [&](const int* p) {
            if (dependent(p, 4)) d4.insert(subset_key(p, 4));
        });
        for_all_size(n, 5, [&](const int* p) {
            if (dependent(p, 5)) d5.insert(subset_key(p, 5));
        });
        for_all_size(n, 5, [&](const int* p) {
            if (dependent(p, 5) && !has_dependent_subset(p, 5, d4))
                circuits.push_back({p[0], p[1], p[2], p[3], p[4]});
        });
        std::unordered_set<u64> d6;
        d6.reserve(1 << 25);
        for_all_size(n, 6, [&](const int* p) {
            if (dependent(p, 6)) {
                d6.insert(subset_key(p, 6));
                if (!has_dependent_subset(p, 6, d5))
                    circuits.push_back({p[0], p[1], p[2], p[3], p[4], p[5]});
            }
        });
        for_all_7(n, [&](const int* p) {
            if (dependent(p, 7) && !has_dependent_subset(p, 7, d6))
                circuits.push_back({p[0], p[1], p[2], p[3], p[4], p[5], p[6]});
        });
        // exactly-K counters
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
        const long long total =
            (long long)counter_clauses.size() + (long long)circuits.size()
            + (fix0 ? 1 : 0);
        fprintf(f, "p cnf %d %lld\n", next_var - 1, total);
        if (fix0) fprintf(f, "1 0\n");
        for (const auto& c : counter_clauses) {
            for (int lit : c) fprintf(f, "%d ", lit);
            fprintf(f, "0\n");
        }
        for (const auto& c : circuits) {
            for (int v : c) fprintf(f, "%d ", -(v + 1));
            fprintf(f, "0\n");
        }
        fclose(f);
        fprintf(stderr, "cnf: %d vars, %lld clauses, %zu circuits\n",
                next_var - 1, total, circuits.size());
    }
    return 0;
}
