// Corrected AG(2,q) search with a multi-word bitset (no 64-bit overflow).
//
// Fixes the bug in agq.cpp/agq2.cpp where `unsigned long long pmask` aliased
// points i and i-64 for boards with more than 64 points.
//
// Build: g++ -O2 -o agq_fixed agq_fixed.cpp
// Usage: ./agq_fixed <q> <target> <nodeCap>

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <algorithm>
#include <chrono>

static int Q = 13;
static int N = 0;
static const int MAXB = 20000;
static const int MAXW = 16;          // up to 16*64 = 1024 points

struct Mask {
    unsigned long long w[MAXW];
    void clear() { memset(w, 0, sizeof(w)); }
    bool get(int i) const { return (w[i >> 6] >> (i & 63)) & 1ULL; }
    void set(int i) { w[i >> 6] |= (1ULL << (i & 63)); }
    void reset(int i) { w[i >> 6] &= ~(1ULL << (i & 63)); }
};

static int nblocks = 0;
static std::vector<std::vector<int>> blocks;
static std::vector<std::vector<int>> through;

static long long nodes = 0;
static long long nodeCap = 200000000LL;
static int target = 13;
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

    // candidate availability
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

    // block budget
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
        m.reset(p);
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
    target = atoi(argv[2]);
    if (argc > 3) nodeCap = atoll(argv[3]);
    N = Q * Q;
    if (N > MAXW * 64) {
        fprintf(stderr, "N=%d exceeds mask capacity\n", N);
        return 1;
    }

    auto t0 = std::chrono::steady_clock::now();

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

    fprintf(stderr, "AG(2,%d): %d points, %d blocks (%zu circles, %zu lines)\n",
            Q, N, nblocks, circList.size(), lineList.size());

    memset(cnt, 0, sizeof(cnt));
    Mask m;
    m.clear();
    // symmetry breaking: fix first 2 points
    chosen[0] = 0; chosen[1] = 1;
    for (int i = 0; i < 2; ++i) {
        for (int bi : through[i]) ++cnt[bi];
        m.set(i);
    }
    rec(2, 2, m);

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
