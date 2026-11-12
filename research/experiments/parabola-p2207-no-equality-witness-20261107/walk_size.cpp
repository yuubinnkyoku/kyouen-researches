// Min-conflicts local search for a safe set of prescribed size in Q_p.
//
// State: a set S of `target` parameters.  A "violation" is a forbidden
// quadruple (an edge from forbidden_edges.cpp) fully contained in S.  A move
// replaces one point of S by a point outside S, so the size never changes and
// the class (x, c, e) is free to drift: this searches all classes at once,
// unlike the per-class CNFs.
//
// The output is a witness (a model), never an optimality proof.
//
// Usage: walk_size <p> <edges.txt> <target> <steps> <seed> <out.json>
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
        std::fprintf(stderr, "usage: %s <p> <edges> <target> <steps> <seed> <out.json>\n", argv[0]);
        return 2;
    }
    const int p = std::atoi(argv[1]);
    const long long steps = std::atoll(argv[4]);
    const uint64_t seed = std::strtoull(argv[5], nullptr, 10);
    std::ifstream in(argv[2]);
    if (!in || p < 5) return 2;
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
    const int target = std::atoi(argv[3]);
    if (target < 1 || target > p) return 2;

    std::vector<std::vector<int>> occ(p);          // point -> edge ids
    for (int e = 0; e < m; ++e)
        for (int k = 0; k < 4; ++k) occ[edges[e][k]].push_back(e);

    std::mt19937_64 rng(seed);
    std::vector<char> inS(p, 0);
    std::vector<int> S;
    S.reserve(target);
    // random initial set
    {
        std::vector<int> all(p);
        for (int i = 0; i < p; ++i) all[i] = i;
        std::shuffle(all.begin(), all.end(), rng);
        for (int i = 0; i < target; ++i) { inS[all[i]] = 1; S.push_back(all[i]); }
    }
    std::vector<int> inside(m, 0);                 // how many points of edge e are in S
    std::vector<int> violated;
    std::vector<int> pos(m, -1);
    auto rebuild = [&]() {
        violated.clear();
        std::fill(pos.begin(), pos.end(), -1);
        for (int e = 0; e < m; ++e) {
            int c = 0;
            for (int k = 0; k < 4; ++k) c += inS[edges[e][k]];
            inside[e] = c;
            if (c == 4) { pos[e] = (int)violated.size(); violated.push_back(e); }
        }
    };
    rebuild();
    auto add_point = [&](int t) {
        inS[t] = 1;
        for (int e : occ[t]) {
            if (++inside[e] == 4) { pos[e] = (int)violated.size(); violated.push_back(e); }
        }
    };
    auto remove_point = [&](int t) {
        inS[t] = 0;
        for (int e : occ[t]) {
            if (inside[e] == 4) {
                int i = pos[e], last = violated.back();
                violated[i] = last;
                pos[last] = i;
                violated.pop_back();
                pos[e] = -1;
            }
            --inside[e];
        }
    };
    long long best = (long long)violated.size();
    std::vector<int> bestS = S;
    long long best_step = 0, last_improve = 0, completed = 0;
    auto save = [&](const char* path) {
        std::ofstream out(path);
        out << "{\"p\":" << p << ",\"target\":" << target << ",\"seed\":" << seed
            << ",\"violations\":" << best << ",\"best_step\":" << best_step
            << ",\"completed_steps\":" << completed << ",\"points\":[";
        std::vector<int> sorted = bestS;
        std::sort(sorted.begin(), sorted.end());
        for (size_t i = 0; i < sorted.size(); ++i) {
            if (i) out << ',';
            out << sorted[i];
        }
        out << "]}\n";
    };
    for (long long step = 1; step <= steps; ++step) {
        if (violated.empty()) { best = 0; bestS = S; best_step = step; break; }
        if ((long long)violated.size() < best) {
            best = (long long)violated.size();
            bestS = S;
            best_step = last_improve = step;
            save(argv[6]);
            std::printf("%lld %lld\n", step, best);
            std::fflush(stdout);
        }
        if (step - last_improve > 200000) {          // restart from the best set
            for (int t : S) inS[t] = 0;
            S = bestS;
            for (int t : S) inS[t] = 1;
            rebuild();
            last_improve = step;
            continue;
        }
        int e = violated[rng() % violated.size()];
        int t = edges[e][rng() % 4];
        int u;
        do { u = (int)(rng() % (uint64_t)p); } while (inS[u]);
        remove_point(t);
        add_point(u);
        auto it = std::find(S.begin(), S.end(), t);
        if (it != S.end()) *it = u;
        completed = step;
    }
    if (violated.empty()) { best = 0; bestS = S; }
    save(argv[6]);
    std::printf("done steps=%lld best=%lld\n", completed, best);
    return best == 0 ? 0 : 1;
}
