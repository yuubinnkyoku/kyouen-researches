// Decide the inversive plane of order q: maximum safe set size.
//
// Points: P^1(F_{q^2}), q^2+1 points.
// Circles: images of P^1(F_q) under PGL(2, F_{q^2}).
// Safe set: no circle contains 4 points.
//
// For q = 16: F_256 = F_2[t]/(t^8 + t^4 + t^3 + t^2 + 1) (a primitive poly).
// Points: 257.  Circles: 16*257 = 4112, each of size 17.
//
// Build: g++ -O2 -o inv16 inv16.cpp

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <algorithm>
#include <chrono>

static const int Q = 16;             // order
static const int E = 8;              // F_{q^2} = F_2^8
static const int N = Q * Q + 1;      // 257 points
static const int MAXB = 20000;

// F_256 arithmetic: elements are 8-bit ints, modulus x^8+x^4+x^3+x^2+1
static inline int gf_add(int a, int b) { return a ^ b; }
static inline int gf_mul(int a, int b) {
    int r = 0;
    while (b) {
        if (b & 1) r ^= a;
        a <<= 1;
        if (a & 0x100) a ^= 0x11D;   // x^8 = x^4+x^3+x^2+1  => 0b100011101
        b >>= 1;
    }
    return r & 0xFF;
}
static inline int gf_inv(int a) {
    if (a == 0) return 0;
    // a^(254)
    int r = 1, base = a, e = 254;
    while (e) {
        if (e & 1) r = gf_mul(r, base);
        base = gf_mul(base, base);
        e >>= 1;
    }
    return r;
}
static inline int gf_div(int a, int b) { return gf_mul(a, gf_inv(b)); }

// points: 0..Q*Q-1 are affine (a,b) with a,b in F_Q (embedded in F_256 as
// elements with high bits zero), and Q*Q is infinity.
// We represent a point as an int: 0..255 for affine a*16+b, 256 for infinity.

static int nblocks = 0;
static std::vector<std::vector<int>> blocks;
static std::vector<std::vector<int>> through;

static long long nodes = 0;
static long long nodeCap = 200000000LL;
static int target = 12;
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

    // candidate availability
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

    // block budget
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

    // P^1(F_256): affine a/b for a,b in F_256, b != 0, plus infinity.
    // We index affine points by their normalised value a/b (0..255), and
    // infinity by 256.
    // The base circle P^1(F_16) = {a/b : a,b in F_16, b != 0} union {inf}.
    // F_16 is the subfield {x : x^16 = x}.

    std::vector<int> subfield;
    for (int x = 0; x < 256; ++x) {
        // x^16 == x ?
        int y = x;
        for (int k = 0; k < 4; ++k) y = gf_mul(y, y);
        if (y == x) subfield.push_back(x);
    }
    fprintf(stderr, "subfield size: %zu\n", subfield.size());

    // base circle: subfield values plus infinity
    std::vector<int> base;
    for (int x : subfield) base.push_back(x);
    base.push_back(256);

    // Mobius maps: z -> (a z + b)/(c z + d) with ad-bc != 0.
    // We generate circles by BFS from the base circle using generators:
    //   z -> z + t  (t in F_256)
    //   z -> m * z  (m a primitive element)
    //   z -> 1/z
    // Applying these to the base circle and closing gives all circles.

    auto apply = [](int z, int kind, int param) -> int {
        if (kind == 0) { // translate
            if (z == 256) return 256;
            return gf_add(z, param);
        } else if (kind == 1) { // dilate
            if (z == 256) return 256;
            return gf_mul(z, param);
        } else { // invert
            if (z == 256) return 0;
            if (z == 0) return 256;
            return gf_inv(z);
        }
    };

    // generators: translations by a basis of F_256 over F_2, dilation by a
    // primitive element, inversion.
    std::vector<std::pair<int,int>> gens;
    for (int i = 0; i < 8; ++i) gens.push_back({0, 1 << i});
    // primitive element: find one
    int prim = -1;
    for (int m = 2; m < 256; ++m) {
        int y = 1;
        bool ok = true;
        for (int k = 1; k < 255; ++k) {
            y = gf_mul(y, m);
            if (y == 1) { ok = false; break; }
        }
        if (ok) { prim = m; break; }
    }
    fprintf(stderr, "primitive element: %d\n", prim);
    gens.push_back({1, prim});
    gens.push_back({2, 0});

    // BFS
    std::vector<std::vector<int>> circles;
    std::vector<std::vector<int>> seen;   // sorted point lists
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
    circles = seen;
    fprintf(stderr, "circles found: %zu (expected %d)\n", circles.size(),
            Q * (Q * Q + 1));

    blocks = circles;
    nblocks = (int)blocks.size();

    through.assign(N, {});
    for (int bi = 0; bi < nblocks; ++bi)
        for (int p : blocks[bi]) through[p].push_back(bi);

    memset(cnt, 0, sizeof(cnt));
    // PGL(2,q^2) is 3-transitive: fix first 3 points
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
