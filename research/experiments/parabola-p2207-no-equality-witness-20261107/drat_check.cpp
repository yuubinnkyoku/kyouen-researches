// Minimal DRAT proof checker: RUP with watched literals, RAT on the pivot.
//
// Usage: drat_check <cnf> <proof>
// The proof is accepted only if every addition checks out and the empty clause
// is derived.  Deletions are honoured (lazily).  Unit clauses in the database
// are propagated before the assumptions of each RUP test.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>

struct Checker {
    int nvars = 0;
    std::vector<std::vector<int>> clauses;
    std::vector<char> deleted;
    std::vector<std::vector<int>> watch;
    std::vector<signed char> value;
    std::vector<int> touched;
    std::vector<int> units;

    static inline int idx(int lit) { return lit > 0 ? 2 * (lit - 1) : 2 * (-lit - 1) + 1; }

    void init(int n) {
        nvars = n;
        watch.assign(2 * nvars, {});
        value.assign(nvars + 1, 0);
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

    void assign(int lit) {
        int v = lit > 0 ? lit : -lit;
        if (value[v] == 0) touched.push_back(v);
        value[v] = lit > 0 ? 1 : -1;
    }

    // propagate over current assignments; sets contradiction on conflict
    bool propagate(bool& contradiction) {
        size_t head = 0;
        while (head < touched.size()) {
            int v = touched[head++];
            int fal = value[v] > 0 ? -v : v;
            std::vector<int>& ws = watch[idx(fal)];
            size_t i = 0;
            while (i < ws.size()) {
                int id = ws[i];
                if (deleted[id]) { ws[i] = ws.back(); ws.pop_back(); continue; }
                std::vector<int>& c = clauses[id];
                if (c[0] == fal) std::swap(c[0], c[1]);
                if (c[1] != fal) { ++i; continue; }          // stale watch entry
                int other = c[0];
                int oval = value[other > 0 ? other : -other];
                if (oval != 0 && oval * (other > 0 ? 1 : -1) > 0) { ++i; continue; }
                bool moved = false;
                for (size_t k = 2; k < c.size(); ++k) {
                    int l = c[k];
                    int val = value[l > 0 ? l : -l];
                    if (val == 0 || val * (l > 0 ? 1 : -1) > 0) {
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
                int val = value[l > 0 ? l : -l];
                if (val != 0 && val * (l > 0 ? 1 : -1) < 0) { contradiction = true; return true; }
                if (val == 0) assign(l);
                ++i;
            }
        }
        return false;
    }
    void clearAssignments() {
        for (int v : touched) value[v] = 0;
        touched.clear();
    }

    // RUP test of `clause`: assume the negations, propagate, expect conflict
    bool rup(const std::vector<int>& clause) {
        clearAssignments();
        bool contradiction = false;
        for (int id : units) {
            if (deleted[id]) continue;
            int l = clauses[id][0];
            int val = value[l > 0 ? l : -l];
            if (val != 0 && val * (l > 0 ? 1 : -1) < 0) { contradiction = true; break; }
            if (val == 0) assign(l);
        }
        if (!contradiction) propagate(contradiction);
        if (!contradiction) {
            for (int lit : clause) {
                int want = lit > 0 ? -1 : 1;
                int v = lit > 0 ? lit : -lit;
                if (value[v] == 0) {
                    assign(want > 0 ? v : -v);
                    if (propagate(contradiction)) break;
                } else if (value[v] != want) { contradiction = true; break; }
            }
        }
        clearAssignments();
        return contradiction;
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
    long long steps = 0, rup_steps = 0, rat_steps = 0, rat_checks = 0, dels = 0;
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
            for (int id = (int)chk.clauses.size() - 1; id >= 0; --id) {
                if (chk.deleted[id]) continue;
                if (chk.clauses[id] == c) { chk.deleted[id] = 1; ++dels; break; }
            }
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
    }
    std::fclose(f);
    std::printf("steps=%lld rup=%lld rat=%lld rat_checks=%lld deletions=%lld empty=%d ok=%d\n",
                steps, rup_steps, rat_steps, rat_checks, dels, (int)empty_derived, (int)ok);
    delete[] buf;
    if (!ok) return 1;
    if (!empty_derived) { std::fprintf(stderr, "no empty clause derived\n"); return 1; }
    std::printf("VERIFIED\n");
    return 0;
}
