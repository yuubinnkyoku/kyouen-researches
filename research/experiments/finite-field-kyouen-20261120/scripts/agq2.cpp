// Decide AG(2,13) size 14 with a fast C++ search.
//
// Board: AG(2,13) = F_13^2, 169 points.
// Blocks: circles (x^2+y^2+Dx+Ey+F=0) and lines.
// Safe set: no block contains 4 points.
//
// Pruning:
//   1. symmetry breaking (fix first 2 points),
//   2. pair budget: for each pair in S, the number of non-full blocks through
//      it must be >= the number of points still to add,
//   3. block budget: need_triples <= available blocks,
//   4. fail-first ordering.
//
// Build: g++ -O2 -o ag13 ag13.cpp

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <array>
#include <algorithm>
#include <chrono>

static int Q = 13;
static int N = Q * Q;                // points
static const int MAXB = 20000;       // max blocks

static int nblocks = 0;
static std::vector<std::vector<int>> blocks;      // block -> points
static std::vector<std::vector<int>> through;     // point -> blocks
static std::vector<std::vector<int>> pairBlocks;  // pair index -> blocks

static inline int pairIdx(int a, int b) {
    if (a > b) std::swap(a, b);
    return a * N + b;
}

static long long nodes = 0;
static long long nodeCap = 200000000LL;
static int target = 14;
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

    // pair budget
    for (int a = 0; a < sz; ++a) {
        for (int b = a + 1; b < sz; ++b) {
            const auto &pb = pairBlocks[pairIdx(chosen[a], chosen[b])];
            int freeCnt = 0;
            for (int bi : pb) if (cnt[bi] < 3) ++freeCnt;
            if (freeCnt < need) return;
        }
    }

    // NEW: candidate availability prune.
    // Each remaining point must be addable.  Count how many points are addable
    // and prune if fewer than `need`.
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

    // NEW: for each pair in S, the blocks through it that are NOT yet full must
    // be able to receive a point.  A block B through p,q can receive a third
    // point r only if r is addable.  Count the blocks through p,q that have at
    // least one addable point outside S.
    // (This is a refinement of the pair budget.)
    for (int a = 0; a < sz; ++a) {
        for (int b = a + 1; b < sz; ++b) {
            const auto &pb = pairBlocks[pairIdx(chosen[a], chosen[b])];
            int usable = 0;
            for (int bi : pb) {
                if (cnt[bi] >= 3) continue;
                bool hasFree = false;
                for (int r : blocks[bi]) {
                    if ((pmask >> r) & 1ULL) continue;
                    // r must be addable
                    bool ok = true;
                    for (int bj : through[r]) {
                        if (cnt[bj] >= 3) { ok = false; break; }
                    }
                    if (ok) { hasFree = true; break; }
                }
                if (hasFree) ++usable;
            }
            if (usable < need) return;
        }
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

    // candidates with cost
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
    if (argc > 1) Q = atoi(argv[1]);
    if (argc > 2) target = atoi(argv[2]);
    if (argc > 3) nodeCap = atoll(argv[3]);
    N = Q * Q;

    auto t0 = std::chrono::steady_clock::now();

    // build points
    std::vector<std::pair<int,int>> pts;
    for (int y = 0; y < Q; ++y)
        for (int x = 0; x < Q; ++x)
            pts.push_back({x, y});

    // lines: for each direction (dx,dy) up to scaling, and each offset
    std::vector<std::vector<int>> lineList;
    {
        std::vector<std::pair<int,int>> dirs;
        for (int dy = 0; dy < Q; ++dy)
            for (int dx = 0; dx < Q; ++dx) {
                if (dx == 0 && dy == 0) continue;
                // canonical: first nonzero component = 1
                int a = dx, b = dy;
                bool canon = false;
                if (a != 0) {
                    int inv = 1;
                    for (int k = 1; k < Q; ++k) if ((a * k) % Q == 1) { inv = k; break; }
                    if ((a * inv) % Q == 1 && (b * inv) % Q == (b * inv) % Q) {
                        // check canonical form
                        if (a == 1) canon = true;
                    }
                } else {
                    if (b == 1) canon = true;
                }
                if (canon) dirs.push_back({dx, dy});
            }
        for (auto &d : dirs) {
            for (int y0 = 0; y0 < Q; ++y0)
                for (int x0 = 0; x0 < Q; ++x0) {
                    std::vector<int> line;
                    for (int t = 0; t < Q; ++t) {
                        int x = (x0 + t * d.first) % Q;
                        int y = (y0 + t * d.second) % Q;
                        line.push_back(y * Q + x);
                    }
                    std::sort(line.begin(), line.end());
                    line.erase(std::unique(line.begin(), line.end()), line.end());
                    if ((int)line.size() == Q) lineList.push_back(line);
                }
        }
        // dedupe
        std::sort(lineList.begin(), lineList.end());
        lineList.erase(std::unique(lineList.begin(), lineList.end()), lineList.end());
    }

    // circles: x^2+y^2+Dx+Ey+F = 0
    std::vector<std::vector<int>> circList;
    for (int D = 0; D < Q; ++D)
        for (int E = 0; E < Q; ++E)
            for (int F = 0; F < Q; ++F) {
                std::vector<int> c;
                for (int y = 0; y < Q; ++y)
                    for (int x = 0; x < Q; ++x) {
                        int v = (x*x + y*y + D*x + E*y + F) % Q;
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

    fprintf(stderr, "AG(2,%d): %d points, %d blocks (%zu circles, %zu lines)\n",
            Q, N, nblocks, circList.size(), lineList.size());

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
