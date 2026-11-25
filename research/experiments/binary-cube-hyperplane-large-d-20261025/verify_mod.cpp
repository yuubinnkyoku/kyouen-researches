// Independent modular verifier for general-position witnesses in the binary
// d-cube.  Reads the same witnesses.txt as verify_exact.py and checks, for
// every record and every (d+1)-subset of the m listed vertices, that the
// augmented matrix is nonsingular modulo the prime p = 2^61 - 1.
//
// Why a single prime is enough here: every entry of the augmented matrix is
// 0 or 1, so each row has Euclidean norm at most sqrt(d+1) and Hadamard's
// bound gives |det| <= (d+1)^{(d+1)/2}.  For d <= 24 this is at most
// 25^12.5 < 3.1e17 < p = 2.3e18, so det == 0 over the integers is
// EQUIVALENT to det == 0 mod p.  The check is therefore a complete proof of
// the same property that verify_exact.py proves by exact integer Bareiss
// elimination, via an independent algorithm.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

namespace {

using u64 = std::uint64_t;
using u128 = unsigned __int128;

constexpr u64 P = (1ULL << 61) - 1;

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

bool independent_mod(const std::vector<int>& subset, int d) {
    // augmented (d+1) x (d+1) matrix, rows (1, x)
    std::vector<std::vector<u64>> a(d + 1, std::vector<u64>(d + 1));
    for (int i = 0; i <= d; ++i) {
        a[i][0] = 1;
        for (int j = 0; j < d; ++j) a[i][j + 1] = (subset[i] >> j) & 1;
    }
    for (int j = 0; j <= d; ++j) {
        int piv = j;
        while (piv <= d && a[piv][j] == 0) ++piv;
        if (piv > d) return false;
        if (piv != j) std::swap(a[j], a[piv]);
        u64 inv = powm(a[j][j], P - 2);
        for (int i = j + 1; i <= d; ++i) {
            u64 f = mulm(a[i][j], inv);
            if (f == 0) continue;
            for (int k = j; k <= d; ++k)
                a[i][k] = static_cast<u64>(
                    (static_cast<u128>(a[i][k]) +
                     (static_cast<u128>(P) * P - static_cast<u128>(f) * a[j][k])) % P);
        }
    }
    return true;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: verify_mod witnesses.txt\n");
        return 2;
    }
    FILE* f = fopen(argv[1], "r");
    if (!f) {
        fprintf(stderr, "cannot open %s\n", argv[1]);
        return 2;
    }
    int records = 0;
    for (;;) {
        int d = 0, m = 0;
        if (fscanf(f, "%d %d", &d, &m) != 2) break;
        std::vector<int> pts(m);
        for (int i = 0; i < m; ++i)
            if (fscanf(f, "%d", &pts[i]) != 1) {
                fprintf(stderr, "truncated record\n");
                return 1;
            }
        if (d < 3 || d > 24) {
            fprintf(stderr, "d=%d outside the certified range 3..24\n", d);
            return 1;
        }
        for (int i = 0; i < m; ++i) {
            if (pts[i] < 0 || pts[i] >= (1 << d)) {
                fprintf(stderr, "d=%d m=%d: vertex out of range\n", d, m);
                return 1;
            }
            for (int j = i + 1; j < m; ++j)
                if (pts[i] == pts[j]) {
                    fprintf(stderr, "d=%d m=%d: duplicate vertex\n", d, m);
                    return 1;
                }
        }
        std::vector<int> subset;
        subset.reserve(d + 1);
        long long tested = 0;
        std::vector<int> idx(d + 1);
        for (int i = 0; i <= d; ++i) idx[i] = i;
        for (;;) {
            subset.clear();
            for (int i = 0; i <= d; ++i) subset.push_back(pts[idx[i]]);
            if (!independent_mod(subset, d)) {
                fprintf(stderr, "FAIL d=%d m=%d\n", d, m);
                return 1;
            }
            ++tested;
            int i = d;
            while (i >= 0 && idx[i] == m - (d + 1 - i)) --i;
            if (i < 0) break;
            idx[i]++;
            for (int j = i + 1; j <= d; ++j) idx[j] = idx[j - 1] + 1;
        }
        printf("d=%d m=%d subsets=%lld nonzero_mod_2p61m1 OK\n", d, m, tested);
        ++records;
    }
    fclose(f);
    if (records == 0) {
        fprintf(stderr, "no records\n");
        return 1;
    }
    return 0;
}
