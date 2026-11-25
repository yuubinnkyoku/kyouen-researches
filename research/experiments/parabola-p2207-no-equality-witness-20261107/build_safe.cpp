// Greedy + ruin-and-recreate construction of a large safe set in Q_p.
//
// The forbidden quadruples form a very sparse 4-uniform hypergraph on p points
// (p=2207: 639,621 edges out of C(2207,4) ~ 9.9e11), so a greedy pass that
// rejects any point completing an edge already produces a large safe set, and
// "ruin and recreate" (drop a few points, refill greedily) improves it.
//
// The output is a witness (a safe set), never an optimality proof: a smaller
// result than the truth only means the heuristic stopped early.
//
// Usage: build_safe <p> <edges.txt> <rounds> <ruin> <seed> <out.json>
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <random>
#include <sstream>
#include <string>
#include <vector>

int main(int argc, char** argv) {
    if (argc != 7) {
        std::fprintf(stderr, "usage: %s <p> <edges> <rounds> <ruin> <seed> <out.json>\n", argv[0]);
        return 2;
    }
    const int p = std::atoi(argv[1]);
    const long long rounds = std::atoll(argv[3]);
    const int ruin = std::atoi(argv[4]);
    const uint64_t seed = std::strtoull(argv[5], nullptr, 10);
    std::ifstream in(argv[2]);
    if (!in || p < 5 || ruin < 1) return 2;
    std::vector<std::array<int, 4>> edges;
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        std::istringstream row(line);
        std::array<int, 4> q{};
        if (!(row >> q[0] >> q[1] >> q[2] >> q[3])) return 2;
        for (int k = 0; k < 4; ++k)
            if (q[k] < 0 || q[k] >= p) return 2;
        edges.push_back(q);
    }
    const int m = (int)edges.size();
    std::vector<std::vector<int>> occ(p);
    for (int e = 0; e < m; ++e)
        for (int k = 0; k < 4; ++k) occ[edges[e][k]].push_back(e);

    std::mt19937_64 rng(seed);
    std::vector<char> inS(p, 0);
    std::vector<int> inside(m, 0);
    std::vector<int> S;
    S.reserve(p);
    std::vector<int> order(p);
    for (int i = 0; i < p; ++i) order[i] = i;

    auto add_point = [&](int t) {
        inS[t] = 1;
        S.push_back(t);
        for (int e : occ[t]) ++inside[e];
    };
    auto remove_point = [&](int t) {
        inS[t] = 0;
        for (int e : occ[t]) --inside[e];
    };
    // true if adding t would complete some forbidden quadruple
    auto blocked = [&](int t) {
        for (int e : occ[t])
            if (inside[e] == 3) return true;
        return false;
    };
    auto refill = [&]() {
        std::shuffle(order.begin(), order.end(), rng);
        for (int t : order)
            if (!inS[t] && !blocked(t)) add_point(t);
    };

    refill();
    std::vector<int> bestS = S;
    long long best = (long long)S.size();
    std::printf("greedy %lld\n", best);
    std::fflush(stdout);
    for (long long r = 1; r <= rounds; ++r) {
        std::vector<int> saved = S;
        std::vector<int> saved_inside = inside;
        int k = std::min<int>(ruin, (int)S.size());
        for (int i = 0; i < k; ++i) {
            int idx = (int)(rng() % S.size());
            int t = S[idx];
            remove_point(t);
            S[idx] = S.back();
            S.pop_back();
        }
        refill();
        if ((long long)S.size() > best) {
            best = (long long)S.size();
            bestS = S;
            std::printf("round %lld size %lld\n", r, best);
            std::fflush(stdout);
        } else if ((long long)S.size() < (long long)saved.size()) {
            // revert: rebuild the previous state exactly
            for (int t : S) inS[t] = 0;
            S = saved;
            inside = saved_inside;
            for (int t : S) inS[t] = 1;
        }
    }
    std::sort(bestS.begin(), bestS.end());
    std::ofstream out(argv[6]);
    out << "{\"p\":" << p << ",\"size\":" << bestS.size() << ",\"seed\":" << seed
        << ",\"rounds\":" << rounds << ",\"ruin\":" << ruin << ",\"edges\":" << m
        << ",\"points\":[";
    for (size_t i = 0; i < bestS.size(); ++i) {
        if (i) out << ',';
        out << bestS[i];
    }
    out << "]}\n";
    std::printf("best %zu\n", bestS.size());
    return 0;
}
