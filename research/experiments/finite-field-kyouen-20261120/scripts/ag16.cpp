// Decide AG(2,16) K with a fast C++ search over F_16.
//
// F_16 = F_2[t]/(t^4 + t + 1).  Elements are 4-bit integers.
// Points are (x, y) in F_16^2, 256 points.
// Blocks: circles x^2+y^2+Dx+Ey+F=0 and lines.
//
// In characteristic 2, x^2+y^2 = (x+y)^2, so circles degenerate.
//
// Build: g++ -O2 -o ag16 ag16.cpp

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <array>
#include <algorithm>
#include <chrono>

static const int Q = 16;
static const int N = Q * Q;          // 256 points
static const int MAXB = 20000;

// F_16 arithmetic: elements are 4-bit ints, t^4 = t + 1
static inline int gf_add(int a, int b) { return a ^ b; }
static inline int gf_mul(int a, int b) {
    int r = 0;
    while (b) {
        if (b & 1) r ^= a;
        a <<= 1;
        if (a & 0x10) a ^= 0x13;   // t^4 = t + 1  => 0b10011
        b >>= 1;
    }
    return r & 0xF;
}
static inline int gf_sq(int a) { return gf_mul(a, a); }

static int nblocks = 0;
static std::vector<std::vector<int>> blocks;
static std::vector<std::vector<int>> through;
static std::vector<std::vector<int>> pairBlocks;

static inline int pairIdx(int a, int b) {
    if (a > b) std::swap(a, b);
    return a * N + b;
}

static long long nodes = 0;
static long long nodeCap = 200000000LL;
static int target = 13;
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

    for (int a = 0; a < sz; ++a) {
        for (int b = a + 1; b < sz; ++b) {
            const auto &pb = pairBlocks[pairIdx(chosen[a], chosen[b])];
            int freeCnt = 0;
            for (int bi : pb) if (cnt[bi] < 3) ++freeCnt;
            if (freeCnt < need) return;
        }
    }

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

    // lines: directions (1,0) and (a,1) for a in F_16
    std::vector<std::vector<int>> lineList;
    std::vector<std::pair<int,int>> dirs;
    dirs.push_back({1, 0});
    for (int a = 0; a < Q; ++a) dirs.push_back({a, 1});
    for (auto &d : dirs) {
        for (int y0 = 0; y0 < Q; ++y0)
            for (int x0 = 0; x0 < Q; ++x0) {
                std::vector<int> line;
                for (int t = 0; t < Q; ++t) {
                    int x = gf_add(x0, gf_mul(t, d.first));
                    int y = gf_add(y0, gf_mul(t, d.second));
                    line.push_back(y * Q + x);
                }
                std::sort(line.begin(), line.end());
                line.erase(std::unique(line.begin(), line.end()), line.end());
                if ((int)line.size() == Q) lineList.push_back(line);
            }
    }
    std::sort(lineList.begin(), lineList.end());
    lineList.erase(std::unique(lineList.begin(), lineList.end()), lineList.end());

    // circles: x^2+y^2+Dx+Ey+F = 0
    std::vector<std::vector<int>> circList;
    for (int D = 0; D < Q; ++D)
        for (int E = 0; E < Q; ++E)
            for (int F = 0; F < Q; ++F) {
                std::vector<int> c;
                for (int y = 0; y < Q; ++y)
                    for (int x = 0; x < Q; ++x) {
                        int v = gf_add(gf_add(gf_add(gf_sq(x), gf_sq(y)),
                                              gf_mul(D, x)),
                                       gf_add(gf_mul(E, y), F));
                        if (v == 0) c.push_back(y * Q + x);
                    }
                if ((int)c.size() >= 3) circList.push_back(c);
            }
    std::sort(circList.begin(), circList.end());
    circList.erase(std::unique(circList.begin(), circList.end()), circList.end());

    blocks = circList;
    for (auto &l : lineList) blocks.push_back(l);
    nblocks = (int)blocks.size();

    through.assign(N, {});
    for (int bi = 0; bi < nblocks; ++bi)
        for (int p : blocks[bi]) through[p].push_back(bi);

    pairBlocks.assign(N * N, {});
    for (int bi = 0; bi < nblocks; ++bi) {
        auto &b = blocks[bi];
        for (size_t i = 0; i < b.size(); ++i)
            for (size_t j = i + 1; j < b.size(); ++j)
                pairBlocks[pairIdx(b[i], b[j])].push_back(bi);
    }

    fprintf(stderr, "AG(2,16): %d points, %d blocks (%zu circles, %zu lines)\n",
            N, nblocks, circList.size(), lineList.size());

    memset(cnt, 0, sizeof(cnt));
    chosen[0] = 0; chosen[1] = 1;
    for (int bi : through[0]) ++cnt[bi];
    for (int bi : through[1]) ++cnt[bi];
    unsigned long long pmask = (1ULL << 0) | (1ULL << 1);

    rec(2, 2, pmask);

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
