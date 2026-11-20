// Decide the inversive plane of order q = 17: maximum safe set size.
//
// Points: P^1(F_{q^2}) = P^1(F_289), 290 points.
// Circles: images of P^1(F_17) under PGL(2, F_289).
// Safe set: no circle contains 4 points.
//
// F_289 = F_17[u]/(u^2 - d) with d a non-residue mod 17.
// Elements are pairs (a,b) = a + b*u, encoded as a*17 + b (0..288).
//
// Build: g++ -O2 -o inv17 inv17.cpp

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <algorithm>
#include <chrono>

static const int P = 17;             // prime
static const int Q = 17;             // order
static const int N = Q * Q + 1;      // 290 points
static const int MAXB = 20000;

// F_289 arithmetic: (a,b) = a + b*u, u^2 = D
static int DVAL = 3;                 // non-residue mod 17

static inline int enc(int a, int b) { return ((a % P) + P) % P * P + (((b % P) + P) % P); }
static inline int ea(int x) { return x / P; }
static inline int eb(int x) { return x % P; }

static inline int gf_add(int x, int y) {
    return enc(ea(x) + ea(y), eb(x) + eb(y));
}
static inline int gf_sub(int x, int y) {
    return enc(ea(x) - ea(y), eb(x) - eb(y));
}
static inline int gf_mul(int x, int y) {
    int a = ea(x), b = eb(x), c = ea(y), e = eb(y);
    return enc(a * c + b * e * DVAL, a * e + b * c);
}
static inline int gf_inv(int x) {
    int a = ea(x), b = eb(x);
    int norm = ((a * a - b * b * DVAL) % P + P) % P;
    int ninv = 1;
    for (int k = 1; k < P; ++k) if ((norm * k) % P == 1) { ninv = k; break; }
    return enc(a * ninv, -b * ninv);
}
static inline int gf_div(int x, int y) { return gf_mul(x, gf_inv(y)); }

static int nblocks = 0;
static std::vector<std::vector<int>> blocks;
static std::vector<std::vector<int>> through;

static long long nodes = 0;
static long long nodeCap = 200000000LL;
static int target = 10;
static std::vector<int> bestSet;
static bool found = false;

static int cnt[MAXB];
static int chosen[4096];

static void rec(int start, int sz, unsigned long long pmask) {
    if (found) return;
    if (++nodes > nodeCap) {
        fprintf(stderr, "node cap exceeded\n");
        exit(2);
    }
    if (sz == target) {
        found = true;
        bestSet.assign(chosen, chosen + sz);
        return;
    }
    int need = target - sz;
    if (N - start < need) return;

    {
        int addable = 0;
        for (int p = start; p < N; ++p) {
            if ((pmask >> p) & 1ULL) continue;
            bool ok = true;
            for (int bi : through[p]) {
                if (cnt[bi] >= 3) { ok = false; break; }
            }
            if (ok) {
                ++addable;
                if (addable >= need) break;
            }
        }
        if (addable < need) return;
    }

    long long needTriples = (long long)target * (target - 1) * (target - 2) / 6
                          - (long long)sz * (sz - 1) * (sz - 2) / 6;
    long long available = 0;
    for (int bi = 0; bi < nblocks; ++bi) {
        if (cnt[bi] >= 3) continue;
        int freePts = 0;
        for (int p : blocks[bi]) if (!((pmask >> p) & 1ULL)) ++freePts;
        if (cnt[bi] + freePts >= 3) ++available;
    }
    if (needTriples > available) return;

    std::vector<std::pair<int,int>> cands;
    cands.reserve(N);
    for (int p = start; p < N; ++p) {
        if ((pmask >> p) & 1ULL) continue;
        bool ok = true;
        int cost = 0;
        for (int bi : through[p]) {
            if (cnt[bi] >= 3) { ok = false; break; }
            if (cnt[bi] == 2) ++cost;
        }
        if (ok) cands.push_back({cost, p});
    }
    std::sort(cands.begin(), cands.end());

    for (auto &cp : cands) {
        int p = cp.second;
        for (int bi : through[p]) ++cnt[bi];
        chosen[sz] = p;
        rec(p + 1, sz + 1, pmask | (1ULL << p));
        for (int bi : through[p]) --cnt[bi];
        if (found) return;
    }
}

int main(int argc, char **argv) {
    if (argc > 1) target = atoi(argv[1]);
    if (argc > 2) nodeCap = atoll(argv[2]);

    auto t0 = std::chrono::steady_clock::now();

    // find a non-residue mod P
    for (int d = 2; d < P; ++d) {
        bool sq = false;
        for (int i = 0; i < P; ++i) if ((i * i) % P == d) { sq = true; break; }
        if (!sq) { DVAL = d; break; }
    }
    fprintf(stderr, "non-residue D = %d\n", DVAL);

    // subfield F_17 = {(a,0)}
    std::vector<int> subfield;
    for (int a = 0; a < P; ++a) subfield.push_back(enc(a, 0));

    // base circle: subfield plus infinity (index N-1 = 289)
    std::vector<int> base;
    for (int x : subfield) base.push_back(x);
    base.push_back(N - 1);

    auto apply = [](int z, int kind, int param) -> int {
        if (kind == 0) { // translate
            if (z == N - 1) return N - 1;
            return gf_add(z, param);
        } else if (kind == 1) { // dilate
            if (z == N - 1) return N - 1;
            return gf_mul(z, param);
        } else { // invert
            if (z == N - 1) return 0;
            if (z == 0) return N - 1;
            return gf_inv(z);
        }
    };

    // generators: translations by a basis of F_289 over F_17, dilation by a
    // primitive element, inversion.
    std::vector<std::pair<int,int>> gens;
    gens.push_back({0, enc(1, 0)});
    gens.push_back({0, enc(0, 1)});
    // primitive element
    int prim = -1;
    for (int m = 1; m < P * P; ++m) {
        if (m == 0) continue;
        // check order = 288
        int y = enc(1, 0);
        bool ok = true;
        for (int k = 1; k < P * P - 1; ++k) {
            y = gf_mul(y, m);
            if (y == enc(1, 0)) { ok = false; break; }
        }
        if (ok) { prim = m; break; }
    }
    fprintf(stderr, "primitive element: %d\n", prim);
    gens.push_back({1, prim});
    gens.push_back({2, 0});

    // BFS
    std::vector<std::vector<int>> seen;
    auto key = [](std::vector<int> v) {
        std::sort(v.begin(), v.end());
        return v;
    };
    std::vector<std::vector<int>> queue;
    std::vector<int> b0 = key(base);
    queue.push_back(b0);
    seen.push_back(b0);
    size_t head = 0;
    while (head < queue.size()) {
        auto cur = queue[head++];
        for (auto &g : gens) {
            std::vector<int> img;
            img.reserve(cur.size());
            for (int z : cur) img.push_back(apply(z, g.first, g.second));
            auto k2 = key(img);
            if ((int)k2.size() != Q + 1) continue;
            if (!std::binary_search(seen.begin(), seen.end(), k2)) {
                seen.push_back(k2);
                std::sort(seen.begin(), seen.end());
                queue.push_back(k2);
            }
        }
    }
    fprintf(stderr, "circles found: %zu (expected %d)\n", seen.size(),
            Q * (Q * Q + 1));

    blocks = seen;
    nblocks = (int)blocks.size();

    through.assign(N, {});
    for (int bi = 0; bi < nblocks; ++bi)
        for (int p : blocks[bi]) through[p].push_back(bi);

    memset(cnt, 0, sizeof(cnt));
    chosen[0] = 0; chosen[1] = 1; chosen[2] = 2;
    for (int i = 0; i < 3; ++i)
        for (int bi : through[i]) ++cnt[bi];
    unsigned long long pmask = (1ULL << 0) | (1ULL << 1) | (1ULL << 2);

    rec(3, 3, pmask);

    auto t1 = std::chrono::steady_clock::now();
    double secs = std::chrono::duration<double>(t1 - t0).count();

    if (found) {
        printf("FOUND size %d: ", target);
        for (int p : bestSet) printf("%d ", p);
        printf("\n");
    } else {
        printf("NO safe set of size %d (exhausted)\n", target);
    }
    printf("nodes=%lld time=%.2fs\n", nodes, secs);
    return 0;
}
