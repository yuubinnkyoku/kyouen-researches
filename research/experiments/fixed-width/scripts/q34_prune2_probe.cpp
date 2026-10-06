// Diagnostic probe for the recorded prune #2 of q34_support_exclusion.cpp.
//
// Prune #2 discards a candidate (B,C) pair when |Z u U| < m-14, where U is
// the set of endpoints of cross-row target edges.  The recorded justification
// is: outside Z u U, a closed neighbourhood contributes only same-row edges
// (<=6) plus its own point, hence at most 7 new points per vertex.
//
// This probe measures, per surviving candidate, the true maximum coverage
// achievable by two target points, and separately reports how much room the
// justification leaves.  It does not change the engine's verdict.
#define Q34_NO_MAIN
#include "q34_support_exclusion.cpp"
#include <cstdio>

int main(int argc, char** argv) {
    int m = argc > 1 ? std::atoi(argv[1]) : 24;
    long long limit = argc > 2 ? std::atoll(argv[2]) : 300000;
    auto v = threes(m);
    std::size_t n = v.size();
    std::array<std::vector<Mask>, 3> z;
    for (int kind = 0; kind < 3; ++kind) {
        z[kind].resize(n * m);
        for (std::size_t i = 0; i < n; ++i)
            for (int c = 0; c < m; ++c)
                for (auto p : v[i].pairs) z[kind][i * m + c] |= triple(p, c, kind, m);
    }
    std::array<std::vector<Cross>, 2> g;
    for (int k = 0; k < 2; ++k)
        for (int b = 0; b < m; ++b)
            for (int c = 0; c < m; ++c) g[k].push_back(cross(b, c, m, k));

    long long examined = 0, would_cover = 0;
    int maxZU = 0;
    for (std::size_t i = 0; i < n && examined < limit; ++i)
        for (std::size_t j = 0; j < n && examined < limit; ++j) {
            bool ok = true;
            for (auto p : v[i].pairs)
                for (auto q : v[j].pairs)
                    if (p.s == q.s) ok = false;
            if (!ok) continue;
            for (int k = 0; k < 2; ++k) {
                const auto& b = v[i];
                const auto& c = v[j];
                Mask base = 0, support = 0;
                for (int x : c.x) base |= z[k ? 2 : 0][i * m + x];
                for (int x : b.x) base |= z[k ? 2 : 1][j * m + x];
                if (pc(base) < m - 32) continue;   // prune 1 already applied
                for (int x : b.x)
                    for (int y : c.x) support |= g[k][x * m + y].support;
                int zu = pc(base | support);
                if (zu > maxZU) maxZU = zu;
                bool pruned2 = zu < m - 14;
                auto a = cover(base, b, c, g[k], m, false);
                bool exact_cover = a[0] >= 0;
                ++examined;
                if (exact_cover) ++would_cover;
                if (exact_cover && pruned2) {
                    printf("UNSOUND-PRUNE-HIT m=%d ZU=%d A=%d,%d B/C=...\n", m, zu, a[0], a[1]);
                    return 3;
                }
            }
        }
    printf("m=%d examined=%lld max_ZU=%d threshold_m-14=%d exact_covers=%lld pruned2_hits=0\n",
           m, examined, maxZU, m - 14, would_cover);
    return 0;
}