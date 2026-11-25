// Random-order greedy search for general-position vertex sets of the binary
// d-cube: every (d+1)-subset of the chosen points must be affinely
// independent over the reals, i.e. the game forbidding d+1 coplanar points
// (degenerate cases included) never fires.
//
// The finder works modulo the prime p = 2^61 - 1.  A nonzero minor or dot
// product modulo p is nonzero over the integers, so the greedy never accepts
// a dependent candidate; the converse may reject a usable vertex, which only
// weakens the search.  Every emitted witness is re-proved from scratch by
// the independent exact verifiers (verify_exact.py, verify_mod.cpp).
//
// Modes
//   --find   d m seed retries seconds out.txt
//   --probe  d m_start m_end seed retries seconds out.txt
//            (probe stops after two consecutive failed sizes)
//
// A record appended to out.txt on every success:
//   d m
//   v0 v1 ... v_{m-1}
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <random>
#include <string>
#include <vector>

using u64 = uint64_t;
using u128 = unsigned __int128;

namespace {

constexpr u64 P = (1ULL << 61) - 1;

u64 addm(u64 a, u64 b) { u64 s = a + b; return s >= P ? s - P : s; }
u64 mulm(u64 a, u64 b) { return static_cast<u64>((static_cast<u128>(a) * b) % P); }
u64 powm(u64 a, u64 e) {
    u64 r = 1;
    while (e) {
        if (e & 1) r = mulm(r, a);
        a = mulm(a, a);
        e >>= 1;
    }
    return r;
}
u64 invm(u64 a) { return powm(a, P - 2); }

double now_seconds() {
    using namespace std::chrono;
    return duration<double>(steady_clock::now().time_since_epoch()).count();
}

// The prime p = 2^61 - 1 exceeds the Hadamard bound (d+1)^{(d+1)/2} for all
// d <= 24, so a determinant vanishes mod p iff it vanishes over the
// integers; the greedy is therefore exact, not merely sound, in this range.
constexpr int MAXD = 24;

// Row-reduces a mod-p matrix in place; returns the rank.
int rref(std::vector<std::vector<u64>>& a) {
    const int rows = static_cast<int>(a.size());
    const int cols = rows ? static_cast<int>(a[0].size()) : 0;
    int rank = 0;
    for (int c = 0; c < cols && rank < rows; ++c) {
        int piv = -1;
        for (int i = rank; i < rows; ++i)
            if (a[i][c] != 0) { piv = i; break; }
        if (piv < 0) continue;
        std::swap(a[rank], a[piv]);
        const u64 inv = invm(a[rank][c]);
        for (int j = c; j < cols; ++j)
            a[rank][j] = mulm(a[rank][j], inv);
        for (int i = 0; i < rows; ++i) {
            if (i == rank || a[i][c] == 0) continue;
            const u64 f = a[i][c];
            for (int j = c; j < cols; ++j)
                a[i][j] = addm(a[i][j], P - mulm(f, a[rank][j]));
        }
        ++rank;
    }
    return rank;
}

// Augmented row (1, x) mod p for vertex x with d coordinates.
std::vector<u64> aug_row(int d, u64 x) {
    std::vector<u64> r(d + 1);
    r[0] = 1;
    for (int c = 0; c < d; ++c) r[c + 1] = (x >> c) & 1;
    return r;
}

// Affine independence of a set of points (|pts| <= d+1): rank of the
// augmented matrix must equal |pts|.
bool affinely_independent_mod(int d, const std::vector<u64>& pts) {
    std::vector<std::vector<u64>> a;
    a.reserve(pts.size());
    for (u64 x : pts) a.push_back(aug_row(d, x));
    return rref(a) == static_cast<int>(pts.size());
}

// Hyperplane normal (null vector) of the d x (d+1) matrix with rows
// (1, x), x in the d-point subset, reduced mod p.  A vertex v lies on the
// spanned hyperplane iff dot((1, v), z) == 0 mod p.
std::array<u64, MAXD + 1> hyperplane_normal(
        int d, const std::vector<u64>& pts, const std::vector<int>& idx) {
    std::vector<std::vector<u64>> m(d, std::vector<u64>(d + 1));
    for (int r = 0; r < d; ++r) {
        const u64 x = pts[idx[r]];
        m[r][0] = 1;
        for (int c = 0; c < d; ++c) m[r][c + 1] = (x >> c) & 1;
    }
    const int rank = rref(m);
    std::array<u64, MAXD + 1> z{};
    if (rank < d) return z;  // dependent mod p: reject everything (sound)
    // rref: row r has leading 1 at pivot_cols[r], strictly increasing.
    std::vector<int> pivot_cols(d, -1);
    std::vector<char> is_pivot(d + 1, 0);
    for (int r = 0; r < d; ++r) {
        int c = 0;
        while (c <= d && m[r][c] == 0) ++c;
        pivot_cols[r] = c;
        is_pivot[c] = 1;
    }
    int free_col = 0;
    while (free_col <= d && is_pivot[free_col]) ++free_col;
    z[free_col] = 1;
    for (int r = 0; r < d; ++r)
        z[pivot_cols[r]] = addm(P - m[r][free_col], 0);
    return z;
}

u64 dot_aug(int d, const std::array<u64, MAXD + 1>& z, u64 v) {
    u128 s = z[0];
    for (int c = 0; c < d; ++c)
        if ((v >> c) & 1) s += z[c + 1];
    return static_cast<u64>(s % P);
}

// One random-order greedy pass over all 2^d vertices.  Maintains affine
// general position of the growing set, so a returned set of size m has all
// (d+1)-subsets independent (any failure would be caught by the verifiers).
std::vector<u64> greedy_pass(int d, int m, std::mt19937_64& rng) {
    const int n = 1 << d;
    std::vector<u64> order(n);
    for (int i = 0; i < n; ++i) order[i] = static_cast<u64>(i);
    std::shuffle(order.begin(), order.end(), rng);
    std::vector<char> inS(n, 0);
    std::vector<u64> S;
    S.reserve(m);
    std::vector<std::array<u64, MAXD + 1>> hyps;  // one per d-subset of S
    std::vector<u64> scratch;
    std::vector<int> combo(static_cast<size_t>(std::max(d - 1, 1)));
    for (size_t pos = 0; pos < order.size(); ++pos) {
        const int k = static_cast<int>(S.size());
        if (k >= m) break;
        if (static_cast<int>(order.size() - pos) < m - k) break;
        const u64 v = order[pos];
        if (inS[v]) continue;
        if (k <= 1) {
            S.push_back(v);
            inS[v] = 1;
            continue;
        }
        if (k < d) {
            scratch = S;
            scratch.push_back(v);
            if (affinely_independent_mod(d, scratch)) {
                S.push_back(v);
                inS[v] = 1;
                if (static_cast<int>(S.size()) == d) {
                    hyps.clear();
                    std::vector<int> all(d);
                    for (int i = 0; i < d; ++i) all[i] = i;
                    hyps.push_back(hyperplane_normal(d, S, all));
                }
            }
            continue;
        }
        bool ok = true;
        for (const auto& z : hyps)
            if (dot_aug(d, z, v) == 0) { ok = false; break; }
        if (ok) {
            S.push_back(v);
            inS[v] = 1;
            const int old = k;
            if (d >= 2) {
                for (int i = 0; i < d - 1; ++i) combo[i] = i;
                for (;;) {
                    std::vector<int> idx(d);
                    for (int i = 0; i < d - 1; ++i) idx[i] = combo[i];
                    idx[d - 1] = old;
                    hyps.push_back(hyperplane_normal(d, S, idx));
                    int i = d - 2;
                    while (i >= 0 && combo[i] == old - (d - 1 - i)) --i;
                    if (i < 0) break;
                    combo[i]++;
                    for (int j = i + 1; j <= d - 2; ++j) combo[j] = combo[j - 1] + 1;
                }
            }
        }
    }
    return S;
}

bool attempt(int d, int m, unsigned long long seed, int max_retries,
             double seconds, std::vector<u64>& out, int& used, double& elapsed) {
    const double deadline = now_seconds() + seconds;
    for (int r = 0; r < max_retries; ++r) {
        std::mt19937_64 rng(seed * 1000003ULL + static_cast<unsigned long long>(r));
        std::vector<u64> S = greedy_pass(d, m, rng);
        if (static_cast<int>(S.size()) == m) {
            out = S;
            used = r + 1;
            elapsed = seconds - (deadline - now_seconds());
            return true;
        }
        if (now_seconds() > deadline) break;
    }
    used = max_retries;
    elapsed = seconds - (deadline - now_seconds());
    return false;
}

void append_record(const char* path, int d, int m, const std::vector<u64>& S) {
    FILE* f = fopen(path, "a");
    if (!f) { fprintf(stderr, "cannot open %s\n", path); exit(2); }
    fprintf(f, "%d %d\n", d, m);
    for (size_t i = 0; i < S.size(); ++i)
        fprintf(f, "%llu%c", static_cast<unsigned long long>(S[i]),
                i + 1 == S.size() ? '\n' : ' ');
    fclose(f);
}

void print_status(int d, int m, bool ok, int used, double secs,
                  const std::vector<u64>& S) {
    printf("{\"d\":%d,\"m\":%d,\"ok\":%s,\"retries\":%d,\"seconds\":%.3f",
           d, m, ok ? "true" : "false", used, secs);
    if (ok) {
        printf(",\"witness\":[");
        for (size_t i = 0; i < S.size(); ++i)
            printf("%s%llu", i ? "," : "",
                   static_cast<unsigned long long>(S[i]));
        printf("]");
    }
    printf("}\n");
    fflush(stdout);
}

}  // namespace

int main(int argc, char** argv) {
    if (argc < 8) {
        fprintf(stderr,
                "usage: search --find d m seed retries seconds out.txt\n"
                "       search --probe d m_start m_end seed retries seconds out.txt\n");
        return 2;
    }
    const std::string mode = argv[1];
    int d = 0, m = 0, m_end = 0;
    unsigned long long seed = 0;
    int retries = 100;
    double seconds = 60.0;
    const char* out = nullptr;
    if (mode == "--find" && argc == 8) {
        d = atoi(argv[2]); m = atoi(argv[3]); seed = strtoull(argv[4], nullptr, 10);
        retries = atoi(argv[5]); seconds = atof(argv[6]); out = argv[7];
        m_end = m;
    } else if (mode == "--probe" && argc == 9) {
        d = atoi(argv[2]); m = atoi(argv[3]); m_end = atoi(argv[4]);
        seed = strtoull(argv[5], nullptr, 10);
        retries = atoi(argv[6]); seconds = atof(argv[7]); out = argv[8];
    } else {
        fprintf(stderr, "bad arguments\n");
        return 2;
    }
    if (d < 3 || d > MAXD || m < d + 3 || m > 64) {
        fprintf(stderr, "unsupported d or m\n");
        return 2;
    }
    if (mode == "--find") {
        std::vector<u64> S;
        int used = 0;
        double secs = 0;
        const bool ok = attempt(d, m, seed, retries, seconds, S, used, secs);
        print_status(d, m, ok, used, secs, S);
        if (ok) append_record(out, d, m, S);
        return ok ? 0 : 1;
    }
    int consecutive_fail = 0;
    for (int mm = m; mm <= m_end && consecutive_fail < 2; ++mm) {
        std::vector<u64> S;
        int used = 0;
        double secs = 0;
        const bool ok = attempt(d, mm, seed + 7919ULL * mm, retries, seconds, S, used, secs);
        print_status(d, mm, ok, used, secs, S);
        if (ok) {
            append_record(out, d, mm, S);
            consecutive_fail = 0;
        } else {
            ++consecutive_fail;
        }
    }
    return 0;
}
