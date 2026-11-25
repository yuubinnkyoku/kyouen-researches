// Faster incremental DRAT proof checker (RUP + RAT), same semantics as
// drat_check_incremental.cpp, with three optimisations:
//
//  1. Deletion lookup by Zobrist hash + exact multiset compare instead of a
//     backward linear scan over every clause (the old scan was quadratic).
//  2. A clause only invalidates the level-0 trail when it is the reason of some
//     currently assigned literal.  Deleting a clause that is not a reason
//     leaves every reason chain intact, so the trail stays sound (this is the
//     K0707 deletion-soundness requirement applied precisely instead of
//     wholesale).
//  3. The level-0 propagation state stays closed across proof steps; the old
//     checker reset qhead to 0 and re-propagated the whole level-0 trail before
//     every single RUP test.
//
// Usage: drat_check_fast <cnf> <proof>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <unordered_map>

struct Checker {
    int nvars = 0;
    std::vector<std::vector<int>> clauses;
    std::vector<char> deleted;
    std::vector<std::vector<int>> watch;
    std::vector<signed char> value;      // per var
    std::vector<int> level;              // per var
    std::vector<int> reason;             // per var (clause id, -1 decision, -2 none)
    std::vector<int> use;                // per clause: trail literals using it as reason
    std::vector<int> trail;              // assigned literals
    std::vector<int> trail_lim;          // start index of each decision level
    size_t qhead = 0;
    std::vector<int> units;
    std::vector<uint64_t> zob;           // per literal index
    std::unordered_map<uint64_t, std::vector<int>> index;

    static inline int idx(int lit) { return lit > 0 ? 2 * (lit - 1) : 2 * (-lit - 1) + 1; }
    static inline int var(int lit) { return lit > 0 ? lit : -lit; }
    static inline int sgn(int lit) { return lit > 0 ? 1 : -1; }

    void init(int n) {
        nvars = n;
        watch.assign(2 * nvars, {});
        value.assign(nvars + 1, 0);
        level.assign(nvars + 1, 0);
        reason.assign(nvars + 1, -2);
        zob.resize(2 * nvars);
        uint64_t s = 0x9e3779b97f4a7c15ULL;
        for (size_t i = 0; i < zob.size(); ++i) {
            s ^= s << 13; s ^= s >> 7; s ^= s << 17;
            zob[i] = s;
        }
    }

    uint64_t hashOf(const std::vector<int>& c) const {
        uint64_t h = 0;
        for (int l : c) h ^= zob[idx(l)];
        return h;
    }

    void addClause(const std::vector<int>& c) {
        int id = (int)clauses.size();
        clauses.push_back(c);
        deleted.push_back(0);
        use.push_back(0);
        index[hashOf(c)].push_back(id);
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
        if (rsn >= 0) ++use[rsn];
        trail.push_back(lit);
    }

    void backtrack(int target) {
        if ((int)trail_lim.size() <= target) return;
        int cut = trail_lim[target];
        for (int i = (int)trail.size() - 1; i >= cut; --i) {
            int v = var(trail[i]);
            if (reason[v] >= 0) --use[reason[v]];
            value[v] = 0;
            level[v] = 0;
            reason[v] = -2;
        }
        trail.resize(cut);
        trail_lim.resize(target);
        qhead = trail.size();
    }

    // A deleted clause can only break the trail if it is the reason of some
    // assigned literal; then every level-0 implication must be re-derived.
    void invalidateAssignments() {
        for (int lit : trail) {
            int v = var(lit);
            if (reason[v] >= 0) --use[reason[v]];
            value[v] = 0;
            level[v] = 0;
            reason[v] = -2;
        }
        trail.clear();
        trail_lim.clear();
        qhead = 0;
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

    // Level-0 closure is maintained across steps, so this only has to handle
    // newly added unit clauses.
    bool level0_conflict() {
        backtrack(0);
        qhead = 0;
        for (int id : units) {
            if (deleted[id]) continue;
            int l = clauses[id][0];
            if (value[var(l)] != 0) {
                if (value[var(l)] * sgn(l) < 0) return true;
                continue;
            }
            assignLit(l, id);
        }
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

    // After adding a clause, propagate it if it is unit at level 0.
    void level0_update(int id) {
        const std::vector<int>& c = clauses[id];
        int unassigned = 0, unit = 0;
        for (int l : c) {
            int v = var(l);
            if (value[v] == 0) { ++unassigned; unit = l; if (unassigned > 1) return; }
            else if (value[v] * sgn(l) > 0) return;     // already satisfied at level 0
        }
        if (unassigned != 1) return;
        trail_lim.clear();
        assignLit(unit, id);
        propagate();
    }

    bool rat(const std::vector<int>& clause, long long& rat_checks) {
        if (clause.empty()) return false;
        int pivot = clause[0];
        for (int id = 0; id < (int)clauses.size(); ++id) {
            if (deleted[id]) continue;
            const std::vector<int>& d = clauses[id];
            bool has = false;
            for (int l : d) if (l == -pivot) { has = true; break; }
            if (!has) continue;
            std::vector<int> resolvent(clause.begin(), clause.end());
            bool taut = false;
            for (int l : d) {
                if (l == -pivot) continue;
                bool dup = false, neg = false;
                for (int m : resolvent) {
                    if (m == l) { dup = true; break; }
                    if (m == -l) { neg = true; break; }
                }
                if (neg) { taut = true; break; }
                if (!dup) resolvent.push_back(l);
            }
            if (taut) continue;
            ++rat_checks;
            if (!rup(resolvent)) return false;
        }
        return true;
    }

    // Exact multiset equality of a stored clause (possibly reordered by watch
    // moves) with a proof line.
    bool sameMultiset(int id, const std::vector<int>& c) const {
        const std::vector<int>& d = clauses[id];
        if (d.size() != c.size()) return false;
        for (int l : c) {
            bool found = false;
            for (int m : d) if (m == l) { found = true; break; }
            if (!found) return false;
        }
        return true;
    }

    bool deleteClause(const std::vector<int>& c, long long& dels) {
        auto it = index.find(hashOf(c));
        if (it == index.end()) return false;
        for (int id : it->second) {
            if (deleted[id]) continue;
            if (!sameMultiset(id, c)) continue;
            if (use[id] > 0) invalidateAssignments();
            deleted[id] = 1;
            ++dels;
            return true;
        }
        return false;
    }
};

static bool readDimacs(const char* path, Checker& chk) {
    FILE* f = std::fopen(path, "r");
    if (!f) return false;
    char* line = new char[1 << 22];
    int nv = 0;
    std::vector<std::vector<int>> cs;
    while (std::fgets(line, 1 << 22, f)) {
        if (line[0] == 'c' || line[0] == '\n' || line[0] == '\r') continue;
        if (line[0] == 'p') { std::sscanf(line, "p cnf %d", &nv); continue; }
        std::vector<int> c;
        char* p = line;
        while (true) {
            char* e;
            long v = std::strtol(p, &e, 10);
            if (e == p) break;
            p = e;
            if (v == 0) break;
            c.push_back((int)v);
        }
        if (!c.empty()) cs.push_back(c);
    }
    std::fclose(f);
    delete[] line;
    chk.init(nv);
    for (auto& c : cs) chk.addClause(c);
    return true;
}

int main(int argc, char** argv) {
    if (argc != 3) { std::fprintf(stderr, "usage: %s <cnf> <proof>\n", argv[0]); return 2; }
    Checker chk;
    if (!readDimacs(argv[1], chk)) { std::fprintf(stderr, "cannot read CNF\n"); return 2; }
    FILE* f = std::fopen(argv[2], "r");
    if (!f) { std::fprintf(stderr, "cannot read proof\n"); return 2; }
    char* buf = new char[1 << 23];
    long long steps = 0, rup_steps = 0, rat_steps = 0, rat_checks = 0, dels = 0, del_miss = 0;
    bool empty_derived = false, ok = true;
    while (std::fgets(buf, 1 << 23, f)) {
        if (buf[0] == 'c' || buf[0] == '\n' || buf[0] == '\r') continue;
        bool del = (buf[0] == 'd' && (buf[1] == ' ' || buf[1] == '\t'));
        std::vector<int> c;
        char* p = buf + (del ? 1 : 0);
        while (true) {
            char* e;
            long v = std::strtol(p, &e, 10);
            if (e == p) break;
            p = e;
            if (v == 0) break;
            c.push_back((int)v);
        }
        if (del) {
            if (!chk.deleteClause(c, dels)) ++del_miss;
            continue;
        }
        ++steps;
        if (c.empty()) {
            if (chk.rup(c)) { empty_derived = true; ++rup_steps; }
            else { ok = false; std::fprintf(stderr, "empty clause is not RUP\n"); }
            break;
        }
        if (chk.rup(c)) { ++rup_steps; }
        else if (chk.rat(c, rat_checks)) { ++rat_steps; }
        else { ok = false; std::fprintf(stderr, "step %lld failed (len %zu)\n", steps, c.size()); break; }
        chk.addClause(c);
        chk.level0_update((int)chk.clauses.size() - 1);
    }
    std::fclose(f);
    std::printf("steps=%lld rup=%lld rat=%lld rat_checks=%lld deletions=%lld delete_misses=%lld "
                "empty=%d ok=%d\n",
                steps, rup_steps, rat_steps, rat_checks, dels, del_miss,
                (int)empty_derived, (int)ok);
    delete[] buf;
    if (!ok) return 1;
    if (!empty_derived) { std::fprintf(stderr, "no empty clause derived\n"); return 1; }
    std::printf("VERIFIED\n");
    return 0;
}
