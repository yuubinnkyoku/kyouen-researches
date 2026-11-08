// Bounded stochastic search. Its output is a model, never an optimality proof.
#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <limits>
#include <random>
#include <sstream>
#include <string>
#include <vector>

int main(int argc, char** argv) {
    if (argc != 5) return 2;
    std::ifstream in(argv[1]);
    if (!in) return 2;
    const long long limit = std::stoll(argv[3]);
    const auto seed = std::stoull(argv[4]);
    if (limit < 0) return 2;
    std::mt19937_64 rng(seed);
    int n = 0, declared = -1;
    std::vector<std::vector<int>> clauses;
    std::vector<int> current;
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty() || line[0] == 'c') continue;
        std::istringstream row(line);
        if (line[0] == 'p') {
            std::string p, kind;
            row >> p >> kind >> n >> declared;
            if (kind != "cnf" || n <= 0 || declared <= 0) return 2;
            continue;
        }
        int lit;
        while (row >> lit) {
            if (lit) {
                if (std::abs(lit) > n) return 2;
                current.push_back(lit);
            } else {
                if (current.empty()) return 2;
                for (int a = 0; a < int(current.size()); ++a)
                    for (int b = 0; b < a; ++b)
                        if (std::abs(current[a]) == std::abs(current[b])) return 2;
                clauses.push_back(current);
                current.clear();
            }
        }
    }
    if (!current.empty() || int(clauses.size()) != declared) return 2;
    std::vector<std::vector<std::pair<int,int>>> occurrence(n+1);
    for (int c = 0; c < declared; ++c)
        for (int lit : clauses[c]) occurrence[std::abs(lit)].push_back({c, lit});
    std::vector<int> assignment(n+1, 0), best_assignment;
    std::vector<int> satisfied(declared), position(declared), unsatisfied;
    auto truth = [&](int lit) { return assignment[std::abs(lit)] == (lit > 0); };
    auto initialize = [&]() {
        unsatisfied.clear();
        std::fill(position.begin(), position.end(), -1);
        for (int c = 0; c < declared; ++c) {
            satisfied[c] = 0;
            for (int lit : clauses[c]) satisfied[c] += truth(lit);
            if (!satisfied[c]) {
                position[c] = int(unsatisfied.size());
                unsatisfied.push_back(c);
            }
        }
    };
    auto flip = [&](int v) {
        for (auto [c, lit] : occurrence[v]) {
            int previous = satisfied[c];
            satisfied[c] += truth(lit) ? -1 : 1;
            if (!previous && satisfied[c]) {
                int index = position[c];
                int last = unsatisfied.back();
                unsatisfied[index] = last;
                position[last] = index;
                unsatisfied.pop_back();
                position[c] = -1;
            } else if (previous && !satisfied[c]) {
                position[c] = int(unsatisfied.size());
                unsatisfied.push_back(c);
            }
        }
        assignment[v] ^= 1;
    };
    auto delta = [&](int v) {
        int value = 0;
        for (auto [c, lit] : occurrence[v]) {
            if (truth(lit) && satisfied[c] == 1) ++value;
            else if (!truth(lit) && !satisfied[c]) --value;
        }
        return value;
    };
    initialize();
    int best = declared+1;
    long long best_step = 0, last_improvement = 0, completed = 0;
    auto save = [&]() {
        std::ofstream out(argv[2]);
        out << "{\"variables\":" << n << ",\"clauses\":" << declared
            << ",\"seed\":" << seed << ",\"violations\":" << best
            << ",\"best_step\":" << best_step << ",\"completed_steps\":" << completed
            << ",\"positive\":[";
        bool first = true;
        for (int v = 1; v <= n; ++v) if (best_assignment[v]) {
            if (!first) out << ',';
            out << v;
            first = false;
        }
        out << "]}\n";
        if (!out) throw std::runtime_error("cannot save model");
    };
    auto checkpoint = [&](long long step) {
        if (int(unsatisfied.size()) >= best) return;
        best = int(unsatisfied.size());
        best_assignment = assignment;
        best_step = last_improvement = step;
        save();
        std::cout << step << ' ' << best << std::endl;
    };
    checkpoint(0);
    for (long long step = 1; step <= limit && best; ++step) {
        if (step-last_improvement > 20000) {
            assignment = best_assignment;
            for (int j = 0; j < std::max(1, n/8); ++j) assignment[1+rng()%n] ^= 1;
            initialize();
            last_improvement = step;
        }
        int c = unsatisfied[rng()%unsatisfied.size()];
        int chosen = 0, score = std::numeric_limits<int>::max(), ties = 0;
        for (int lit : clauses[c]) {
            int v = std::abs(lit), value = delta(v);
            if (value < score) { score = value; chosen = v; ties = 1; }
            else if (value == score && rng()%++ties == 0) chosen = v;
        }
        if (score >= 0 && rng()%100 < 40) chosen = std::abs(clauses[c][rng()%clauses[c].size()]);
        flip(chosen);
        completed = step;
        checkpoint(step);
    }
    // Re-evaluate the saved assignment, independent of incremental bookkeeping.
    assignment = best_assignment;
    initialize();
    if (int(unsatisfied.size()) != best) return 3;
    save();
    return 0;
}
