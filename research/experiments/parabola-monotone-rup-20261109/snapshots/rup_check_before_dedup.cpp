// Addition-only RUP checker. Deletions are ignored; RAT is NEVER attempted.
// Every accepted addition follows by unit propagation from the original clauses
// and earlier accepted RUP additions. Thus all retained clauses are consequences
// of the original CNF, even if the input DRAT stream deleted them.
// Propagation core copied from fixed checker SHA256
// 34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b.
// Restricted text format: header and one complete clause per line, literals
// within the declared range. Reject malformed input and missing empty clause.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <climits>
#include <charconv>
struct Checker {
    int nvars = 0;
    std::vector<std::vector<int>> clauses;
    std::vector<char> deleted;
    std::vector<std::vector<int>> watch;
    std::vector<signed char> value;      // per var
    std::vector<int> level;              // per var
    std::vector<int> reason;             // per var (clause id, -1 decision, -2 none)
    std::vector<int> trail;              // assigned literals
    std::vector<int> trail_lim;          // start index of each decision level
    size_t qhead = 0;
    std::vector<int> units;

    static inline int idx(int lit) { return lit > 0 ? 2 * (lit - 1) : 2 * (-lit - 1) + 1; }
    static inline int var(int lit) { return lit > 0 ? lit : -lit; }
    static inline int sgn(int lit) { return lit > 0 ? 1 : -1; }

    void init(int n) {
        nvars = n;
        watch.assign(2 * nvars, {});
        value.assign(nvars + 1, 0);
        level.assign(nvars + 1, 0);
        reason.assign(nvars + 1, -2);
    }

    void addClause(const std::vector<int>& c) {
        int id = (int)clauses.size();
        clauses.push_back(c);
        deleted.push_back(0);
        if (c.size() == 1) units.push_back(id);
        else {
            watch[idx(c[0])].push_back(id);
            watch[idx(c[1])].push_back(id);
        }
    }

    void assignLit(int lit, int rsn) {
        int v = var(lit);
        value[v] = (signed char)sgn(lit);
        level[v] = (int)trail_lim.size();
        reason[v] = rsn;
        trail.push_back(lit);
    }

    void backtrack(int target) {
        if ((int)trail_lim.size() <= target) return;
        int cut = trail_lim[target];
        for (int i = (int)trail.size() - 1; i >= cut; --i) {
            int v = var(trail[i]);
            value[v] = 0;
            level[v] = 0;
            reason[v] = -2;
        }
        trail.resize(cut);
        trail_lim.resize(target);
        qhead = trail.size();
    }

    bool propagate() {
        while (qhead < trail.size()) {
            int fal = -trail[qhead++];
            std::vector<int>& ws = watch[idx(fal)];
            size_t i = 0;
            while (i < ws.size()) {
                int id = ws[i];
                if (deleted[id]) { ws[i] = ws.back(); ws.pop_back(); continue; }
                std::vector<int>& c = clauses[id];
                if (c[0] == fal) std::swap(c[0], c[1]);
                if (c[1] != fal) { ++i; continue; }
                int other = c[0];
                if (value[var(other)] != 0 && value[var(other)] * sgn(other) > 0) { ++i; continue; }
                bool moved = false;
                for (size_t k = 2; k < c.size(); ++k) {
                    int l = c[k];
                    if (value[var(l)] == 0 || value[var(l)] * sgn(l) > 0) {
                        std::swap(c[1], c[k]);
                        watch[idx(c[1])].push_back(id);
                        ws[i] = ws.back();
                        ws.pop_back();
                        moved = true;
                        break;
                    }
                }
                if (moved) continue;
                int l = c[0];
                if (value[var(l)] != 0 && value[var(l)] * sgn(l) < 0) return true;   // conflict
                if (value[var(l)] == 0) assignLit(l, id);
                ++i;
            }
        }
        return false;
    }

    bool level0_conflict() {
        backtrack(0);
        qhead = 0;                      // re-propagate the level-0 trail from scratch
        bool conflict = false;
        for (int id : units) {
            if (deleted[id]) continue;
            int l = clauses[id][0];
            if (value[var(l)] != 0 && value[var(l)] * sgn(l) < 0) { conflict = true; break; }
            if (value[var(l)] == 0) assignLit(l, id);
        }
        if (conflict) return true;
        return propagate();
    }

    // RUP test of `clause` at the current database
    bool rup(const std::vector<int>& clause) {
        if (level0_conflict()) return true;
        bool conflict = false;
        for (int lit : clause) {
            int want = -lit;
            int v = var(want);
            if (value[v] != 0 && value[v] * sgn(want) < 0) { conflict = true; break; }
            if (value[v] == 0) {
                trail_lim.push_back((int)trail.size());
                assignLit(want, -1);
                if (propagate()) { conflict = true; break; }
            }
        }
        backtrack(0);
        return conflict;
    }


};

static bool clause(const std::string& line, int nv, std::vector<int>& out) {
    std::istringstream in(line);
    std::string token;
    bool zero = false;
    while (in >> token) {
        long long v;
        auto parsed = std::from_chars(token.data(), token.data()+token.size(), v);
        if (parsed.ec != std::errc() || parsed.ptr != token.data()+token.size() ||
            zero || v > nv || v < -static_cast<long long>(nv)) return false;
        if (!v) zero = true;
        else out.push_back(static_cast<int>(v));
    }
    return zero;

}

int main(int argc, char** argv) {
    if (argc != 3) return 2;
    std::ifstream cnf(argv[1]), proof(argv[2]);
    if (!cnf || !proof) return 2;
    Checker chk;
    std::string line;
    bool header = false, initial_empty = false;
    long long expected = 0, count = 0;
    while (std::getline(cnf, line)) {
        const auto pos = line.find_first_not_of(" \t\r");
        if (pos == std::string::npos || line[pos] == 'c') continue;
        line.erase(0, pos);
        if (line[0] == 'p') {
            std::istringstream in(line);
            std::string p, type, extra;
            int nv;
            if (header || !(in >> p >> type >> nv >> expected) || p != "p" || type != "cnf" ||
                nv < 0 || nv > 10000000 || expected < 0 || (in >> extra)) return 2;
            chk.init(nv);
            header = true;
            continue;
        }
        if (!header) return 2;
        std::vector<int> c;
        if (!clause(line, chk.nvars, c)) return 2;
        ++count;
        if (c.empty()) initial_empty = true;
        else chk.addClause(c);
    }
    if (cnf.bad() || !header || count != expected) return 2;
    long long additions = 0, deletions = 0;
    bool empty = false;
    while (std::getline(proof, line)) {
        const auto pos = line.find_first_not_of(" \t\r");
        if (pos == std::string::npos || line[pos] == 'c') continue;
        line.erase(0, pos);
        bool del = line[0] == 'd';
        if (del) {
            if (line.size() < 2 || (line[1] != ' ' && line[1] != '\t')) return 2;
            line.erase(0, 1);
        }
        std::vector<int> c;
        if (!clause(line, chk.nvars, c)) return 2;
        if (del) { ++deletions; continue; }
        ++additions;
        if (!initial_empty && !chk.rup(c)) {
            std::fprintf(stderr, "non-RUP addition %lld (length %zu); RAT forbidden\n", additions, c.size());
            return 1;
        }
        if (c.empty()) { empty = true; break; }
        chk.addClause(c);
    }
    if (proof.bad() || !empty) return 1;
    std::printf("additions=%lld ignored_deletions=%lld rat=0 empty=1\nRUP_VERIFIED\n", additions, deletions);
    return 0;
}
