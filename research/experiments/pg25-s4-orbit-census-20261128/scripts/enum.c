/* PG(2,q) s-safe maximal set enumerator (DFS with line-count pruning).
 *
 * Points and lines of PG(2,q) built from canonical projective triples over
 * GF(q) (q <= 5, plain int arithmetic mod q). A set S is safe iff every line
 * has |S cap L| <= s; maximal iff additionally every excluded point p lies
 * on some line with exactly s points of S (adding p would exceed s).
 *
 * Output: per-size counts of maximal safe sets + binary dump of masks
 * (uint32 LE, one per maximal set, sorted by DFS order) + complement-side
 * per-size counts (minimal (l-s)-fold blocking; each is checked directly:
 * every line has >= l-s complement points and each complement point lies on
 * a line with exactly l-s complement points).
 *
 * Verification of the complement side is element-level and fail-closed:
 * if a complement fails the direct check the program aborts with exit 1.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int Q, S, N;            /* plane order, safety threshold, #points */
static int linesMask[40];      /* point masks per line */
static int linesSize[40];      /* line size = Q+1 */
static int thr[32][8];         /* point -> line indices */
static int thrN[32];
static int throughPts[40][8];  /* line -> point indices */
static int cnt[40];            /* current S-count per line */
static int wit[32];             /* # full lines through point */
static char inS[32];
static uint32_t curMask;
static long long maxSizeCount[40];
static long long compSizeCount[40];

static int gmul(int a, int b) {          /* field multiplication for q=4 (GF4) or prime q */
    if (Q != 4) return (a * b) % Q;
    static int t[4][4] = {
        {0,0,0,0},{0,1,2,3},{0,2,3,1},{0,3,1,2}};
    return t[a][b];
}

static FILE *dump;
static long long dumped;

static void record_maximal(void) {
    int sz = 0;
    for (int i = 0; i < N; i++) if (inS[i]) sz++;
    maxSizeCount[sz]++;
    compSizeCount[N - sz]++;
    /* direct element-level complement check (fail-closed) */
    for (int L = 0; L < N; L++) {
        int c = linesSize[L] - cnt[L];
        if (c < linesSize[L] - S) { fprintf(stderr, "FAIL blocking line %d\n", L); exit(1); }
    }
    for (int i = 0; i < N; i++) {
        if (inS[i]) continue;
        /* complement point i: need a line through i with exactly l-s complement pts */
        int ok = 0;
        for (int t = 0; t < thrN[i]; t++) {
            int L = thr[i][t];
            if (linesSize[L] - cnt[L] == linesSize[L] - S) { ok = 1; break; }
        }
        if (!ok) { fprintf(stderr, "FAIL complement minimality pt %d\n", i); exit(1); }
    }
    if (dump) { fwrite(&curMask, sizeof(uint32_t), 1, dump); dumped++; }
}

static long long nodes = 0;

static void dfs(int i) {
    nodes++;
    if (i == N) {
        /* maximality: every excluded point has a full line through it */
        for (int p = 0; p < N; p++) {
            if (!inS[p] && wit[p] == 0) return;   /* not maximal */
        }
        record_maximal();
        return;
    }
    /* include point i */
    int fullLines[8], nFull = 0, bad = 0;
    for (int t = 0; t < thrN[i]; t++) {
        int L = thr[i][t];
        cnt[L]++;
        if (cnt[L] > S) bad = 1;
        else if (cnt[L] == S) fullLines[nFull++] = L;
    }
    if (!bad) {
        inS[i] = 1; curMask |= (1u << i);
        for (int f = 0; f < nFull; f++) {
            int L = fullLines[f];
            for (int p = 0; p < linesSize[L]; p++) wit[throughPts[L][p]]++;
        }
        dfs(i + 1);
        for (int f = 0; f < nFull; f++) {
            int L = fullLines[f];
            for (int p = 0; p < linesSize[L]; p++) wit[throughPts[L][p]]--;
        }
        inS[i] = 0; curMask &= ~(1u << i);
    }
    /* undo include attempt */
    for (int t = 0; t < thrN[i]; t++) cnt[thr[i][t]]--;
    /* exclude point i */
    dfs(i + 1);
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s q s [dumpfile]\n", argv[0]); return 2; }
    Q = atoi(argv[1]); S = atoi(argv[2]);
    dump = (argc > 3) ? fopen(argv[3], "wb") : NULL;
    if (argc > 3 && !dump) { fprintf(stderr, "cannot open dump\n"); return 2; }

    /* build points: canonical triples (first nonzero coord == 1) */
    int px[200], py[200], pz[200];
    N = 0;
    for (int a = 0; a < Q; a++)
      for (int b = 0; b < Q; b++)
        for (int c = 0; c < Q; c++) {
            if (!a && !b && !c) continue;
            if (!(a == 1 || (!a && b == 1) || (!a && !b && c == 1))) continue;
            px[N] = a; py[N] = b; pz[N] = c; N++;
        }
    if (N != Q * Q + Q + 1) { fprintf(stderr, "point count %d wrong\n", N); return 1; }

    /* lines: same canonical form; incidence a*x+b*y+c*z == 0 */
    int NL = 0;
    for (int a = 0; a < Q; a++)
      for (int b = 0; b < Q; b++)
        for (int c = 0; c < Q; c++) {
            if (!a && !b && !c) continue;
            if (!(a == 1 || (!a && b == 1) || (!a && !b && c == 1))) continue;
            int x = a, y = b, z = c;
            int m = 0, sz = 0;
            for (int p = 0; p < N; p++)
                { int acc = gmul(x, px[p]);
              acc = (Q == 4) ? (acc ^ gmul(y, py[p])) : ((acc + gmul(y, py[p])) % Q);
              acc = (Q == 4) ? (acc ^ gmul(z, pz[p])) : ((acc + gmul(z, pz[p])) % Q);
              if (acc == 0) { m |= (1 << p); sz++; } }
            if (sz != Q + 1) { fprintf(stderr, "line size %d wrong\n", sz); return 1; }
            linesMask[NL] = m; linesSize[NL] = sz;
            { int k = 0;
              for (int p = 0; p < N; p++) if (m & (1 << p)) throughPts[NL][k++] = p; }
            NL++;
        }
    if (NL != N) { fprintf(stderr, "line count %d wrong\n", NL); return 1; }

    for (int L = 0; L < NL; L++)
        for (int p = 0; p < N; p++)
            if (linesMask[L] & (1 << p)) { thr[p][thrN[p]++] = L; }
    for (int p = 0; p < N; p++) if (thrN[p] != Q + 1) { fprintf(stderr, "thr %d wrong\n", p); return 1; }

    memset(cnt, 0, sizeof cnt); memset(wit, 0, sizeof wit);
    memset(inS, 0, sizeof inS); curMask = 0;
    dfs(0);

    printf("q=%d s=%d N=%d nodes=%lld dumped=%lld\n", Q, S, N, nodes, dumped);
    long long tot = 0, ctot = 0;
    for (int k = 0; k <= N; k++) {
        if (maxSizeCount[k]) { printf("maximal_safe %d: %lld\n", k, maxSizeCount[k]); tot += maxSizeCount[k]; }
        if (compSizeCount[k]) { printf("minimal_blocking %d: %lld\n", k, compSizeCount[k]); ctot += compSizeCount[k]; }
    }
    printf("total maximal=%lld total blocking=%lld\n", tot, ctot);
    if (dump) fclose(dump);
    return 0;
}
