// Corrected inversive-plane search with a multi-word bitset.
//
// Fixes the 64-bit mask overflow in inv16.cpp / inv17.cpp / inv19.cpp.
//
// Build: g++ -O2 -o inv_fixed inv_fixed.cpp
// Usage: ./inv_fixed <q> <target> <nodeCap>

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <algorithm>
#include <chrono>

static int P = 17;                   // prime
static int Q = 17;                   // order
static int N = 0;                    // q^2 + 1
static const int MAXB = 20000;
static const int MAXW = 16;          // 1024 points

static int DVAL = 3;

struct Mask {
    unsigned long long w[MAXW];
    void clear() { memset(w, 0, sizeof(w)); }
    bool get(int i) const { return (w[i >> 6] >> (i & 63)) & 1ULL; }
    void set(int i) { w[i >> 6] |= (1ULL << (i & 63)); }
};

// F_{p^2} = F_p[u]/(u^2 - DVAL)
static inline int enc(int a, int b) {
    return (((a % P) + P) % P) * P + (((b % P) + P) % P);
}
static inline int ea(int x) { return x / P; }
static inline int eb(int x) { return x % P; }
static inline int gf_add(int x, int y) { return enc(ea(x) + ea(y), eb(x) + eb(y)); }
static inline int gf_sub(int x, int y) { return enc(ea(x) - ea(y), eb(x) - eb(y)); }
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

static bool canAdd(int i, const Mask &m) {
    for (int bi : through[i]) {
        int c = 0;
        for (int j : blocks[bi]) {
            if (m.get(j)) {
                if (++c >= 3) return false;
            }
        }
    }
    return true;
}

static void rec(int start, int sz, Mask &m) {
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
            if (m.get(p)) continue;
            if (canAdd(p, m)) {
                if (++addable >= need) break;
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
        for (int p : blocks[bi]) if (!m.get(p)) ++freePts;
        if (cnt[bi] + freePts >= 3) ++available;
    }
    if (needTriples > available) return;

    std::vector<std::pair<int,int>> cands;
    cands.reserve(N);
    for (int p = start; p < N; ++p) {
        if (m.get(p)) continue;
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
        m.set(p);
        chosen[sz] = p;
        rec(p + 1, sz + 1, m);
        for (int bi : through[p]) --cnt[bi];
        if (found) return;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "usage: %s <q> <target> <nodeCap>\n", argv[0]);
        return 1;
    }
    Q = atoi(argv[1]);
    P = Q;
    target = atoi(argv[2]);
    if (argc > 3) nodeCap = atoll(argv[3]);
    N = Q * Q + 1;
    if (N > MAXW * 64) {
        fprintf(stderr, "N=%d exceeds mask capacity\n", N);
        return 1;
    }

    auto t0 = std::chrono::steady_clock::now();

    // find a non-residue
    for (int d = 2; d < P; ++d) {
        bool sq = false;
        for (int i = 0; i < P; ++i) if ((i * i) % P == d) { sq = true; break; }
        if (!sq) { DVAL = d; break; }
    }

    std::vector<int> subfield;
    for (int a = 0; a < P; ++a) subfield.push_back(enc(a, 0));

    std::vector<int> base;
    for (int x : subfield) base.push_back(x);
    base.push_back(N - 1);

    auto apply = [](int z, int kind, int param) -> int {
        if (kind == 0) {
            if (z == N - 1) return N - 1;
            return gf_add(z, param);
        } else if (kind == 1) {
            if (z == N - 1) return N - 1;
            return gf_mul(z, param);
        } else {
            if (z == N - 1) return 0;
            if (z == 0) return N - 1;
            return gf_inv(z);
        }
    };

    std::vector<std::pair<int,int>> gens;
    gens.push_back({0, enc(1, 0)});
    gens.push_back({0, enc(0, 1)});
    int prim = -1;
    for (int mm = 1; mm < P * P; ++mm) {
        if (mm == 0) continue;
        int y = enc(1, 0);
        bool ok = true;
        for (int k = 1; k < P * P - 1; ++k) {
            y = gf_mul(y, mm);
            if (y == enc(1, 0)) { ok = false; break; }
        }
        if (ok) { prim = mm; break; }
    }
    gens.push_back({1, prim});
    gens.push_back({2, 0});

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
    fprintf(stderr, "inversive q=%d: %d points, %zu circles (expected %d)\n",
            Q, N, seen.size(), Q * (Q * Q + 1));

    blocks = seen;
    nblocks = (int)blocks.size();

    through.assign(N, {});
    for (int bi = 0; bi < nblocks; ++bi)
        for (int p : blocks[bi]) through[p].push_back(bi);

    memset(cnt, 0, sizeof(cnt));
    Mask m;
    m.clear();
    chosen[0] = 0; chosen[1] = 1; chosen[2] = 2;
    for (int i = 0; i < 3; ++i) {
        for (int bi : through[i]) ++cnt[bi];
        m.set(i);
    }
    rec(3, 3, m);

    auto t1 = std::chrono::steady_clock::now();
    double secs = std::chrono::duration<double>(t1 - t0).count();

    if (found) {
        printf("FOUND size %d:", target);
        for (int p : bestSet) printf(" %d", p);
        printf("\n");
    } else {
        printf("NO safe set of size %d (exhausted)\n", target);
    }
    printf("nodes=%lld time=%.2fs\n", nodes, secs);
    return 0;
}
