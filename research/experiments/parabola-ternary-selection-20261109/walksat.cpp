// Multivalued WalkSAT over the pair-state space of the fixed-d ternary CNF.
//
// State: each of n pairs is low(0), high(1) or empty(2). A base clause is a
// list of requirements (pair, side); it is violated iff every required pair is
// currently on its required side. The cardinality bound (empty pairs <= bound)
// is a soft clause of weight lambda (penalty lambda * max(0, empties - bound)).
// The seqcounter encoding is never used here: evaluation is over base clauses
// and the empty-pair count only.
//
// Modes:
//   search: --problem P --flips N --seed S (--init FILE | --random)
//   eval  : --problem P --eval STATE   (prints violations/empties for a state)
//
// Restarts (deep stage): --restart-every N reinitialises every N flips,
// alternating warm (the --init state) with random; --stagnation N resets a
// restart early when the global best cost has not improved for N flips.
// The best state is flushed to --best-state on every improvement, so a VM
// restart loses at most the flips since the last improvement.
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

struct Req { int v; int s; };

static int N = 0, M = 0;
static vector<vector<Req>> CL;
static vector<vector<pair<int, int>>> INC;
static vector<int> SZ, CNT, POS;
static vector<int> VIOL;
static vector<char> STATE;
static vector<int> EMPTY_LIST, EPOS;
static long long VIOLCOUNT = 0;
static long long EMPTIES = 0;
static int BOUND = 3;
static double LAM = 1000000.0;

static inline long long penalty(long long e) { return e > BOUND ? e - BOUND : 0; }
static inline long long cost(long long v, long long e) { return v + (long long)llround(LAM * penalty(e)); }

static void remove_viol(int c) {
    int p = POS[c];
    int last = VIOL.back();
    VIOL[p] = last;
    POS[last] = p;
    VIOL.pop_back();
    POS[c] = -1;
}

static void add_viol(int c) {
    POS[c] = (int)VIOL.size();
    VIOL.push_back(c);
}

static void remove_empty(int v) {
    int p = EPOS[v];
    int last = EMPTY_LIST.back();
    EMPTY_LIST[p] = last;
    EPOS[last] = p;
    EMPTY_LIST.pop_back();
    EPOS[v] = -1;
}

static void add_empty(int v) {
    EPOS[v] = (int)EMPTY_LIST.size();
    EMPTY_LIST.push_back(v);
}

// total-cost delta of setting pair v (currently STATE[v]) to val.
static long long delta(int v, int val) {
    long long dv = 0;
    int old = STATE[v];
    for (const auto& [c, s] : INC[v]) {
        int o = (old == s), nw = (val == s);
        if (o == nw) continue;
        bool was = (CNT[c] == SZ[c]);
        int ncnt = CNT[c] + nw - o;
        bool now = (ncnt == SZ[c]);
        if (was != now) dv += now ? 1 : -1;
    }
    long long de = (val == 2) - (old == 2);
    return dv + (long long)llround(LAM * (penalty(EMPTIES + de) - penalty(EMPTIES)));
}

static void apply(int v, int val) {
    int old = STATE[v];
    if (old == val) return;
    for (const auto& [c, s] : INC[v]) {
        int o = (old == s), nw = (val == s);
        if (o == nw) continue;
        bool was = (CNT[c] == SZ[c]);
        CNT[c] += nw - o;
        bool now = (CNT[c] == SZ[c]);
        if (was != now) {
            if (now) { add_viol(c); VIOLCOUNT++; }
            else { remove_viol(c); VIOLCOUNT--; }
        }
    }
    if (old == 2) remove_empty(v);
    if (val == 2) add_empty(v);
    EMPTIES += (val == 2) - (old == 2);
    STATE[v] = (char)val;
}

static bool load_problem(const string& path) {
    ifstream in(path);
    if (!in) return false;
    string tag;
    if (!(in >> tag >> N >> M) || tag != "p") return false;
    CL.assign(M, {});
    for (int i = 0; i < M; i++) {
        int k; in >> k;
        CL[i].resize(k);
        for (int j = 0; j < k; j++) { int v, s; in >> v >> s; CL[i][j] = {v, s}; }
    }
    return (bool)in || in.eof();
}

static bool init_structures() {
    INC.assign(N, {});
    SZ.resize(M); CNT.assign(M, 0); POS.assign(M, -1);
    VIOL.clear(); VIOLCOUNT = 0;
    for (int c = 0; c < M; c++) {
        SZ[c] = (int)CL[c].size();
        for (const auto& r : CL[c]) INC[r.v].push_back({c, r.s});
    }
    STATE.assign(N, 2);
    EMPTY_LIST.clear(); EPOS.assign(N, -1);
    EMPTIES = 0;
    return true;
}

static void recompute() {
    fill(CNT.begin(), CNT.end(), 0);
    POS.assign(M, -1); VIOL.clear(); VIOLCOUNT = 0;
    EMPTY_LIST.clear(); EPOS.assign(N, -1); EMPTIES = 0;
    for (int c = 0; c < M; c++)
        for (const auto& r : CL[c]) if (STATE[r.v] == r.s) CNT[c]++;
    for (int c = 0; c < M; c++) if (CNT[c] == SZ[c]) { add_viol(c); VIOLCOUNT++; }
    for (int v = 0; v < N; v++) if (STATE[v] == 2) { add_empty(v); EMPTIES++; }
}

static void dump_state_vec(const string& path, const vector<char>& st) {
    ofstream out(path);
    for (int v = 0; v < N; v++) out << (int)st[v] << (v + 1 == N ? '\n' : ' ');
}

static bool read_state(const string& path) {
    ifstream in(path);
    if (!in) return false;
    for (int v = 0; v < N; v++) { int x; if (!(in >> x)) return false; STATE[v] = (char)x; }
    return true;
}

int main(int argc, char** argv) {
    string problem, init, evalState, bestState, jsonOut;
    long long flips = 1000000, seed = 1;
    bool useRandom = false;
    double noise = 0.1;
    long long traceEvery = 0;
    long long restartEvery = 0, stagnation = 0;

    for (int i = 1; i < argc; i++) {
        string a = argv[i];
        auto next = [&]() -> string { return (i + 1 < argc) ? string(argv[++i]) : string(); };
        if (a == "--problem") problem = next();
        else if (a == "--init") init = next();
        else if (a == "--random") useRandom = true;
        else if (a == "--eval") evalState = next();
        else if (a == "--flips") flips = stoll(next());
        else if (a == "--seed") seed = stoll(next());
        else if (a == "--lambda") LAM = stod(next());
        else if (a == "--noise") noise = stod(next());
        else if (a == "--bound") BOUND = stoi(next());
        else if (a == "--best-state") bestState = next();
        else if (a == "--json") jsonOut = next();
        else if (a == "--trace-every") traceEvery = stoll(next());
        else if (a == "--restart-every") restartEvery = stoll(next());
        else if (a == "--stagnation") stagnation = stoll(next());
        else { cerr << "unknown arg " << a << "\n"; return 2; }
    }
    if (problem.empty() || !load_problem(problem)) { cerr << "problem load failed\n"; return 2; }
    if (!init_structures()) return 2;

    if (!evalState.empty()) {
        if (!read_state(evalState)) { cerr << "state load failed\n"; return 2; }
        recompute();
        printf("{\"base_violations\": %lld, \"empties\": %lld, \"penalty\": %lld, \"cost\": %lld}\n",
               VIOLCOUNT, EMPTIES, penalty(EMPTIES), cost(VIOLCOUNT, EMPTIES));
        return 0;
    }

    mt19937_64 rng((uint64_t)seed);
    vector<char> warmState;
    bool haveWarm = false;
    if (!useRandom) {
        if (!read_state(init)) { cerr << "init load failed\n"; return 2; }
        warmState = STATE;
        haveWarm = true;
    }
    // validate init
    for (int v = 0; v < N; v++) if (STATE[v] < 0 || STATE[v] > 2) { cerr << "bad init value\n"; return 2; }
    if (haveWarm) STATE = warmState;
    else for (int v = 0; v < N; v++) STATE[v] = (char)(rng() % 3);
    recompute();

    auto t0 = chrono::steady_clock::now();
    long long bestV = VIOLCOUNT, bestE = EMPTIES, bestStep = 0;
    long long bestCost = cost(VIOLCOUNT, EMPTIES);
    vector<char> bestStateVec = STATE;
    uniform_real_distribution<double> uni(0.0, 1.0);
    long long flipsRun = 0;
    int restarts = 0;
    long long lastImproveStep = 0;
    string initPerRestart;
    bool solvedNow = (VIOLCOUNT == 0 && EMPTIES <= BOUND);

    while (!solvedNow && flipsRun < flips) {
        // reinitialise: restart 0 warm (when available), then alternate
        bool useWarm = haveWarm && (restarts % 2 == 0);
        if (restarts > 0) {
            if (useWarm) STATE = warmState;
            else for (int v = 0; v < N; v++) STATE[v] = (char)(rng() % 3);
            recompute();
        }
        initPerRestart += useWarm ? 'W' : 'R';
        if (restarts > 0 && traceEvery)
            printf("restart %d %lld %lld %lld %c\n", restarts, flipsRun, VIOLCOUNT, EMPTIES,
                   useWarm ? 'W' : 'R');
        restarts++;
        long long budgetEnd = flips;
        if (restartEvery > 0) budgetEnd = min(flips, flipsRun + restartEvery);
        // A stagnation reset re-initialises and continues within the same flip
        // budget, so the window must restart with the segment. Without this the
        // next segment breaks on its first flip and the outer loop spins.
        lastImproveStep = flipsRun;

        for (; flipsRun < budgetEnd; ) {
            if (VIOLCOUNT == 0 && EMPTIES <= BOUND) { solvedNow = true; break; }
            long long step = ++flipsRun;
            bool cardViol = EMPTIES > BOUND;
            int v = -1;
            double totalw = (double)VIOLCOUNT + (cardViol ? LAM : 0.0);
            double r = uni(rng) * totalw;
            if (r < (double)VIOLCOUNT) {
                int c = VIOL[(size_t)(rng() % VIOL.size())];
                const auto& req = CL[c];
                const Req& rr = req[rng() % req.size()];
                v = rr.v;
            } else {
                v = EMPTY_LIST[rng() % EMPTY_LIST.size()];
            }

            int nval;
            if (uni(rng) < noise) {
                nval = (int)(rng() % 3);
            } else {
                long long bd = INT64_MAX; int bvals[3]; int bn = 0; int cur = STATE[v];
                for (int val = 0; val < 3; val++) {
                    long long d = delta(v, val);
                    if (d < bd) { bd = d; bn = 0; bvals[bn++] = val; }
                    else if (d == bd) bvals[bn++] = val;
                }
                if (bn == 1) nval = bvals[0];
                else {
                    // prefer a value different from the current one when possible
                    int alt[3]; int an = 0;
                    for (int k = 0; k < bn; k++) if (bvals[k] != cur) alt[an++] = bvals[k];
                    nval = an ? alt[rng() % an] : bvals[rng() % bn];
                }
            }
            apply(v, nval);

            long long cnow = cost(VIOLCOUNT, EMPTIES);
            if (cnow < bestCost) {
                bestCost = cnow; bestV = VIOLCOUNT; bestE = EMPTIES; bestStep = step;
                bestStateVec = STATE; lastImproveStep = flipsRun;
                if (!bestState.empty()) dump_state_vec(bestState, bestStateVec);
            }
            if (traceEvery && (step % traceEvery == 0))
                printf("trace %lld %lld %lld\n", step, VIOLCOUNT, EMPTIES);
            if (stagnation > 0 && flipsRun - lastImproveStep >= stagnation) break;
        }
    }
    auto t1 = chrono::steady_clock::now();
    double secs = chrono::duration<double>(t1 - t0).count();

    bool solved = solvedNow;
    long long rv = VIOLCOUNT; long long re = EMPTIES;
    STATE = bestStateVec;
    if (!bestState.empty()) dump_state_vec(bestState, bestStateVec);

    long long outV = solved ? 0 : bestV;
    long long outE = solved ? re : bestE;
    printf("{\"base_violations_best\": %lld, \"empties_at_best\": %lld, \"best_step\": %lld, "
           "\"final_violations\": %lld, \"final_empties\": %lld, \"flips\": %lld, "
           "\"flips_run\": %lld, \"restarts\": %d, \"init_per_restart\": \"%s\", "
           "\"lambda\": %.6g, \"bound\": %d, \"noise\": %.4g, "
           "\"seconds\": %.6f, \"solved\": %s}\n",
           outV, outE, bestStep, rv, re, flips, flipsRun, restarts, initPerRestart.c_str(),
           LAM, BOUND, noise, secs, solved ? "true" : "false");
    return 0;
}
