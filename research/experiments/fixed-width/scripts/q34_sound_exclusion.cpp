// Sound-only re-run of the 3xm, q=4 deficient-maximal exclusion.
//
// The recorded engine (q34_support_exclusion.cpp) prunes a candidate pair with
//
//   1. |Z| < m-32                      (two closed neighbourhoods cover <=32)
//   2. |Z | U| < m-14                  (U = endpoints of cross-row edges)
//
// Prune 2 is only valid if, for every target vertex outside Z u U, the closed
// neighbourhood adds at most 7 points.  This file therefore keeps the same
// Z/G construction but replaces prune 2 by the exact, self-evidently sound
// statement: every vertex has at most 6 same-row partners and at most
// |U|-contribution, so we simply skip prune 2 and test the exact closed
// neighbourhoods.  Prune 1 is kept only after its bound is re-derived here.
//
// Output is JSONL, one line per length, and any found witness is printed in
// full so it can be re-checked by q34_deficient_witness_audit.py.
#define Q34_NO_MAIN
#include "q34_support_exclusion.cpp"
#include <cstring>
#include <string>

int main(int argc, char** argv) {
    int low = argc > 1 ? std::atoi(argv[1]) : 24;
    int high = argc > 2 ? std::atoi(argv[2]) : low;
    int mode = argc > 3 ? std::atoi(argv[3]) : 0;  // 0 = sound, 1 = recorded

    for (int m = low; m <= high; ++m) {
        auto start = std::chrono::steady_clock::now();
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

        std::array<bool, 2> found{};
        std::array<std::uint64_t, 2> candidates{}, pruned1{}, pruned2{};
        std::array<std::array<int, 2>, 2> wA{};
        std::array<Three, 2> wB{}, wC{};
        for (std::size_t i = 0; i < n; ++i)
            for (std::size_t j = 0; j < n; ++j) {
                bool exterior_safe = true;
                for (auto p : v[i].pairs)
                    for (auto q : v[j].pairs)
                        if (p.s == q.s) exterior_safe = false;
                if (!exterior_safe) continue;
                for (int k = 0; k < 2; ++k) {
                    if (found[k] || (k && j < i)) continue;
                    const auto& b = v[i];
                    const auto& c = v[j];
                    Mask base = 0, support = 0;
                    for (int x : c.x) base |= z[k ? 2 : 0][i * m + x];
                    for (int x : b.x) base |= z[k ? 2 : 1][j * m + x];
                    // Degree bound: 6 same-row partners + 9 cross-row pairs = 15,
                    // so a closed neighbourhood has at most 16 points and two of
                    // them cover at most 32.  Sound in both modes.
                    if (pc(base) < m - 32) { ++pruned1[k]; continue; }
                    for (int x : b.x)
                        for (int y : c.x) support |= g[k][x * m + y].support;
                    if (mode == 1 && pc(base | support) < m - 14) { ++pruned2[k]; continue; }
                    ++candidates[k];
                    auto a = cover(base, b, c, g[k], m, false);
                    if (a[0] >= 0) { found[k] = true; wA[k] = a; wB[k] = b; wC[k] = c; }
                }
                if (found[0] && found[1]) break;
            }
        double seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
        std::cout << "{\"m\":" << m << ",\"mode\":\"" << (mode ? "recorded" : "sound") << "\""
            << ",\"three_sets\":" << n << ",\"cover_exists\":[" << found[0] << "," << found[1]
            << "],\"candidates\":[" << candidates[0] << "," << candidates[1]
            << "],\"pruned_bound1\":[" << pruned1[0] << "," << pruned1[1]
            << "],\"pruned_bound2\":[" << pruned2[0] << "," << pruned2[1]
            << "],\"seconds\":" << seconds << ",\"witnesses\":[";
        for (int k = 0; k < 2; ++k) {
            if (k) std::cout << ",";
            if (!found[k]) { std::cout << "null"; continue; }
            std::cout << "{\"A\":[" << wA[k][0] << "," << wA[k][1] << "],\"B\":[";
            for (int i = 0; i < 3; ++i) { if (i) std::cout << ","; std::cout << wB[k].x[i]; }
            std::cout << "],\"C\":[";
            for (int i = 0; i < 3; ++i) { if (i) std::cout << ","; std::cout << wC[k].x[i]; }
            std::cout << "],\"target_row\":" << (k ? 1 : 0) << "}";
        }
        std::cout << "]}" << std::endl;
    }
}