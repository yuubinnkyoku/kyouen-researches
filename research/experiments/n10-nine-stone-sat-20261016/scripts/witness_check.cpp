// Standalone witness checker for a maximal safe set on an n x n board.
//
// Independent of the Python verifier and of kc_core.h:
//   safe      : no 4-subset has det [x^2+y^2, x, y, 1] == 0
//   maximal   : every point outside S completes some 3-subset of S to a
//               det-zero quadruple
// Usage: witness_check <n> <id0> <id1> ... (point id = y*n + x)
// Exit code 0 iff both checks pass; prints a small report.
#include <cstdio>
#include <cstdlib>
#include <utility>
#include <vector>

static __int128 det4(const long long p[4][2]) {
    __int128 m[4][4];
    for (int i = 0; i < 4; ++i) {
        m[i][0] = (__int128)p[i][0] * p[i][0] + (__int128)p[i][1] * p[i][1];
        m[i][1] = p[i][0];
        m[i][2] = p[i][1];
        m[i][3] = 1;
    }
    // Bareiss is overkill; expand along the first column with 3x3 minors.
    __int128 total = 0;
    for (int i = 0; i < 4; ++i) {
        __int128 mm[3][3];
        int r = 0;
        for (int j = 0; j < 4; ++j) {
            if (j == i) continue;
            for (int c = 1; c < 4; ++c) mm[r][c - 1] = m[j][c];
            ++r;
        }
        __int128 d3 = mm[0][0] * (mm[1][1] * mm[2][2] - mm[1][2] * mm[2][1])
                    - mm[0][1] * (mm[1][0] * mm[2][2] - mm[1][2] * mm[2][0])
                    + mm[0][2] * (mm[1][0] * mm[2][1] - mm[1][1] * mm[2][0]);
        total += ((i % 2 == 0) ? d3 : -d3) * m[i][0];
    }
    return total;
}

int main(int argc, char** argv) {
    if (argc < 3) {
        std::fprintf(stderr, "usage: witness_check <n> <id...>\n");
        return 2;
    }
    int n = std::atoi(argv[1]);
    std::vector<long long> pt;
    for (int i = 2; i < argc; ++i) pt.push_back(std::atoll(argv[i]));
    int V = n * n;
    std::vector<char> inS(V, 0);
    for (long long v : pt) {
        if (v < 0 || v >= V) { std::fprintf(stderr, "bad id %lld\n", v); return 2; }
        if (inS[v]) { std::fprintf(stderr, "duplicate id %lld\n", v); return 2; }
        inS[v] = 1;
    }
    int k = (int)pt.size();

    auto coords = [&](long long id) {
        return std::pair<long long, long long>(id % n, id / n);
    };

    long long bad_quads = 0;
    for (int a = 0; a < k; ++a)
    for (int b = a + 1; b < k; ++b)
    for (int c = b + 1; c < k; ++c)
    for (int d = c + 1; d < k; ++d) {
        long long p[4][2];
        int ids[4] = {a, b, c, d};
        for (int i = 0; i < 4; ++i) {
            auto cc = coords(pt[ids[i]]);
            p[i][0] = cc.first; p[i][1] = cc.second;
        }
        if (det4(p) == 0) {
            ++bad_quads;
            std::printf("unsafe quad: %lld %lld %lld %lld\n",
                        pt[a], pt[b], pt[c], pt[d]);
        }
    }

    long long unblocked = 0;
    for (int p = 0; p < V; ++p) {
        if (inS[p]) continue;
        bool blocked = false;
        for (int a = 0; a < k && !blocked; ++a)
        for (int b = a + 1; b < k && !blocked; ++b)
        for (int c = b + 1; c < k && !blocked; ++c) {
            long long q[4][2];
            int ids[3] = {a, b, c};
            for (int i = 0; i < 3; ++i) {
                auto cc = coords(pt[ids[i]]);
                q[i][0] = cc.first; q[i][1] = cc.second;
            }
            auto cc = coords(p);
            q[3][0] = cc.first; q[3][1] = cc.second;
            if (det4(q) == 0) blocked = true;
        }
        if (!blocked) {
            ++unblocked;
            std::printf("unblocked point: %d (%lld,%lld)\n", p, p % n, p / n);
        }
    }

    std::printf("n=%d stones=%d unsafe_quads=%lld unblocked=%lld\n",
                n, k, bad_quads, unblocked);
    bool ok = (bad_quads == 0) && (unblocked == 0);
    std::printf("verdict: %s\n", ok ? "PASS" : "FAIL");
    return ok ? 0 : 1;
}
