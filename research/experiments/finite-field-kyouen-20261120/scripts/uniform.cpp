// Decide whether a board is UNIFORM (all maximal safe sets have size K),
// by searching for a maximal safe set of size < K.
//
// If none exists, the parity law gives g(empty) = K mod 2, i.e. the winner.
//
// This is much cheaper than computing the full Grundy table.
//
// Build: g++ -O2 -o uniform uniform.cpp
// Usage: ./uniform <q> <K> <nodeCap> [inv|ag]

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <algorithm>
#include <chrono>

static int Q = 13;
static int N = 0;
static const int MAXB = 20000;

static int nblocks = 0;
static std::vector<std::vector<int>> blocks;
static std::vector<std::vector<int>> through;

static long long nodes = 0;
static long long nodeCap = 200000000LL;
static int target = 5;
static std::vector<int> foundSet;
static bool found = false;

static int chosen[4096];

static bool canAdd(int i, unsigned long long pmask) {
    for (int bi : through[i]) {
        int cnt = 0;
        for (int j : blocks[bi]) {
            if ((pmask >> j) & 1ULL) {
                if (++cnt >= 3) return false;
            }
        }
    }
    return true;
}

static void rec(int start, int sz, unsigned long long pmask) {
    if (found) return;
    if (++nodes > nodeCap) {
        fprintf(stderr, "node cap exceeded\n");
        exit(2);
    }
    if (sz == target) {
        // check maximality
        for (int i = 0; i < N; ++i) {
            if ((pmask >> i) & 1ULL) continue;
            if (canAdd(i, pmask)) return;   // not maximal
        }
        found = true;
        foundSet.assign(chosen, chosen + sz);
        return;
    }
    int need = target - sz;
    if (N - start < need) return;
    for (int i = start; i < N; ++i) {
        if ((pmask >> i) & 1ULL) continue;
        if (!canAdd(i, pmask)) continue;
        chosen[sz] = i;
        rec(i + 1, sz + 1, pmask | (1ULL << i));
        if (found) return;
    }
}

// ---- board builders ----

static void buildAG(int q) {
    N = q * q;
    std::vector<std::vector<int>> lineList;
    std::vector<std::pair<int,int>> dirs;
    dirs.push_back({1, 0});
    for (int a = 0; a < q; ++a) dirs.push_back({a, 1});
    for (auto &d : dirs) {
        for (int y0 = 0; y0 < q; ++y0)
            for (int x0 = 0; x0 < q; ++x0) {
                std::vector<int> line;
                for (int t = 0; t < q; ++t) {
                    int x = (x0 + t * d.first) % q;
                    int y = (y0 + t * d.second) % q;
                    line.push_back(y * q + x);
                }
                std::sort(line.begin(), line.end());
                line.erase(std::unique(line.begin(), line.end()), line.end());
                if ((int)line.size() == q) lineList.push_back(line);
            }
    }
    std::sort(lineList.begin(), lineList.end());
    lineList.erase(std::unique(lineList.begin(), lineList.end()), lineList.end());

    std::vector<std::vector<int>> circList;
    for (int D = 0; D < q; ++D)
        for (int E = 0; E < q; ++E)
            for (int F = 0; F < q; ++F) {
                std::vector<int> c;
                for (int y = 0; y < q; ++y)
                    for (int x = 0; x < q; ++x) {
                        int v = (x*x + y*y + D*x + E*y + F) % q;
                        if (v == 0) c.push_back(y * q + x);
                    }
                if ((int)c.size() >= 3) circList.push_back(c);
            }
    std::sort(circList.begin(), circList.end());
    circList.erase(std::unique(circList.begin(), circList.end()), circList.end());

    blocks = circList;
    for (auto &l : lineList) blocks.push_back(l);
    nblocks = (int)blocks.size();
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "usage: %s <q> <K> <nodeCap> [inv|ag]\n", argv[0]);
        return 1;
    }
    Q = atoi(argv[1]);
    target = atoi(argv[2]);
    if (argc > 3) nodeCap = atoll(argv[3]);
    const char *mode = (argc > 4) ? argv[4] : "ag";

    auto t0 = std::chrono::steady_clock::now();

    if (strcmp(mode, "ag") == 0) {
        buildAG(Q);
    } else {
        fprintf(stderr, "inv mode not implemented in this binary\n");
        return 1;
    }

    through.assign(N, {});
    for (int bi = 0; bi < nblocks; ++bi)
        for (int p : blocks[bi]) through[p].push_back(bi);

    fprintf(stderr, "AG(2,%d): %d points, %d blocks, K=%d\n",
            Q, N, nblocks, target);

    // search for a maximal set of size < K
    bool smaller = false;
    int smallerSize = -1;
    const int K = target;
    for (int t = 1; t < K; ++t) {
        target = t;              // rec() reads the global target
        found = false;
        foundSet.clear();
        nodes = 0;
        rec(0, 0, 0ULL);
        fprintf(stderr, "  size %d: exists=%s nodes=%lld\n",
                t, found ? "YES" : "no", nodes);
        if (found) {
            smaller = true;
            smallerSize = t;
            break;
        }
    }
    target = K;

    auto t1 = std::chrono::steady_clock::now();
    double secs = std::chrono::duration<double>(t1 - t0).count();

    if (smaller) {
        printf("NON-UNIFORM: maximal set of size %d exists\n", smallerSize);
        printf("  witness:");
        for (int p : foundSet) printf(" %d", p);
        printf("\n");
    } else {
        printf("UNIFORM: no maximal set smaller than K=%d\n", target);
        printf("  => g(empty) = %d mod 2 = %d\n", target, target % 2);
    }
    printf("time=%.2fs\n", secs);
    return 0;
}
