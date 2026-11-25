// Decide AG(2,17) size 18 with CROSS-constraint pruning.
//
// q = 17 = 1 mod 4, so -1 is a square and the split coordinates
// (s,t) = (x+iy, x-iy) give q^2 = 289 cross blocks of size 2q-1 = 33.
//
// Cross constraint: a_c + b_r - x_cr <= 3 where a_c = |S cap col c|,
// b_r = |S cap row r|, x_cr = 1 if (c,r) in S.
//
// We proved: at most 2 columns and 2 rows have 2 points; all others <= 1.
// So k <= q+2 = 19.
//
// For k=18: sum a_c = 18 over 17 columns, each <= 2.
//   x2 columns with 2, x1 with 1, x0 with 0: x2+x1+x0=17, 2x2+x1=18
//   => x1 = 18-2x2, x0 = x2-1.  x2 in [1,2] (since |C2| <= 2).
//   x2=1: x1=16, x0=0.  x2=2: x1=14, x0=1.
// Same for rows.
//
// This is a VERY tight structure.  Let me use it as a prune.
//
// Build: g++ -O2 -o ag17cross ag17cross.cpp

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <algorithm>
#include <chrono>

static const int Q = 17;
static const int N = Q * Q;          // 289 points
static const int MAXB = 20000;

static int nblocks = 0;
static std::vector<std::vector<int>> blocks;
static std::vector<std::vector<int>> through;
static std::vector<std::vector<int>> pairBlocks;

static inline int pairIdx(int a, int b) {
    if (a > b) std::swap(a, b);
    return a * N + b;
}

static long long nodes = 0;
static long long nodeCap = 2000000000LL;
static int target = 18;
static std::vector<int> bestSet;
static bool found = false;

static int cnt[MAXB];
static int chosen[4096];

// split coordinates
static int colOf[N], rowOf[N];

static void rec(int start, int sz, unsigned long long pmask,
                int *colcnt, int *rowcnt) {
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

    // CROSS prune: at most 2 columns/rows with 2 points
    {
        int n2c = 0, n2r = 0;
        for (int c = 0; c < Q; ++c) if (colcnt[c] == 2) ++n2c;
        for (int r = 0; r < Q; ++r) if (rowcnt[r] == 2) ++n2r;
        if (n2c > 2 || n2r > 2) return;
        // for k=18: need x2 in [1,2] for columns and rows
        // remaining points must fit: each column can take at most 2
        int capc = 0, capr = 0;
        for (int c = 0; c < Q; ++c) capc += (2 - colcnt[c]);
        for (int r = 0; r < Q; ++r) capr += (2 - rowcnt[r]);
        if (capc < need || capr < need) return;
    }

    // pair budget
    for (int a = 0; a < sz; ++a) {
        for (int b = a + 1; b < sz; ++b) {
            const auto &pb = pairBlocks[pairIdx(chosen[a], chosen[b])];
            int freeCnt = 0;
            for (int bi : pb) if (cnt[bi] < 3) ++freeCnt;
            if (freeCnt < need) return;
        }
    }

    // candidate availability
    {
        int addable = 0;
        for (int p = start; p < N; ++p) {
            if ((pmask >> p) & 1ULL) continue;
            if (colcnt[colOf[p]] >= 2 || rowcnt[rowOf[p]] >= 2) continue;
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
        if (colcnt[colOf[p]] >= 2 || rowcnt[rowOf[p]] >= 2) continue;
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
        colcnt[colOf[p]]++;
        rowcnt[rowOf[p]]++;
        chosen[sz] = p;
        rec(p + 1, sz + 1, pmask | (1ULL << p), colcnt, rowcnt);
        colcnt[colOf[p]]--;
        rowcnt[rowOf[p]]--;
        for (int bi : through[p]) --cnt[bi];
        if (found) return;
    }
}

int main(int argc, char **argv) {
    if (argc > 1) target = atoi(argv[1]);
    if (argc > 2) nodeCap = atoll(argv[2]);

    auto t0 = std::chrono::steady_clock::now();

    // find i with i^2 = -1 mod Q
    int ival = -1;
    for (int i = 0; i < Q; ++i) if ((i * i + 1) % Q == 0) { ival = i; break; }
    if (ival < 0) { fprintf(stderr, "Q is not 1 mod 4\n"); return 1; }
    fprintf(stderr, "i = %d (i^2 = -1)\n", ival);

    // split coordinates
    for (int y = 0; y < Q; ++y)
        for (int x = 0; x < Q; ++x) {
            int p = y * Q + x;
            colOf[p] = ((x + ival * y) % Q + Q) % Q;
            rowOf[p] = ((x - ival * y) % Q + Q) % Q;
        }

    // lines
    std::vector<std::vector<int>> lineList;
    std::vector<std::pair<int,int>> dirs;
    dirs.push_back({1, 0});
    for (int a = 0; a < Q; ++a) dirs.push_back({a, 1});
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
    std::sort(lineList.begin(), lineList.end());
    lineList.erase(std::unique(lineList.begin(), lineList.end()), lineList.end());

    // circles
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
    int colcnt[64] = {0}, rowcnt[64] = {0};
    chosen[0] = 0; chosen[1] = 1;
    for (int i = 0; i < 2; ++i) {
        for (int bi : through[i]) ++cnt[bi];
        colcnt[colOf[i]]++;
        rowcnt[rowOf[i]]++;
    }
    unsigned long long pmask = (1ULL << 0) | (1ULL << 1);

    rec(2, 2, pmask, colcnt, rowcnt);

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
