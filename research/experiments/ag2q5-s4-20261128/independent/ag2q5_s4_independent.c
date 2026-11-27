// Independent solver for the s=4 kyouen (cap) game on the AG(2,5) board.
//
// Deliberately independent of research/experiments/pg2q7-cap-game-20261125/
// scripts/grundy_s_stats.c:
//   * that engine enumerates with incremental line counters, stores every
//     position in size buckets and computes Grundy bottom-up with hash maps;
//   * this engine stores positions implicitly and computes Grundy top-down
//     with memoisation on a direct 2^25 table, testing move legality by
//     comparing point-removed line masks (no popcount needed: for p not in S
//     the line through p can only be overfull if all four other points are in S).
//
// Game: S is safe iff |S cap L| <= s for every board line L (here s = 4).
// A move adds one point keeping safety; no move loses (normal play), so
//     g(S) = mex { g(S + p) : p a legal move }.
//
// Build:  gcc -O2 -o ag2q5_s4_independent ag2q5_s4_independent.c
// Run:    ./ag2q5_s4_independent ../../s-parameter-kyouen-20261125/output/board_ag2q5.txt 4
//
// Output: POINTS / CIRCLES / SAFE / MAXSIZE / ROOT, then
//   SIZE <k> <count> <maximal> <g0>
//   GRUNDY <g> <total>
//   GSIZE <k> <g> <count>
//   MAXIMAL <k> <count>        (same numbers as the SIZE maximal column)
//   FIRSTMOVE <g> <count>      (Grundy histogram of the 25 root children)

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n, b, s_cap;
static uint32_t lmask[256];
static uint32_t lrest[64][64];   // lrest[p][j] = (line through p) minus p
static int npl[64];              // lines through each point
static uint8_t *memo;            // 0xFF = unvisited; else Grundy value
static long long *N;             // count by size
static long long Ng[65][64];     // count by size and Grundy value
static long long maximal[65];
static long long total;
static int maxk;
static int first_g[64];
static int root_g = -1;

static uint8_t grundy(uint32_t S) {
    uint8_t cached = memo[S];
    if (cached != 0xFF) return cached;

    int k = __builtin_popcount(S);
    uint32_t seen = 0;
    int nmoves = 0;
    for (int p = 0; p < n; p++) {
        if (S & (1u << p)) continue;
        int legal = 1;
        for (int j = 0; j < npl[p]; j++) {
            uint32_t rest = lrest[p][j];
            if ((S & rest) == rest) { legal = 0; break; }
        }
        if (!legal) continue;
        nmoves++;
        uint8_t cg = grundy(S | (1u << p));
        if (cg >= 32) { fprintf(stderr, "grundy %u too large\n", cg); exit(1); }
        seen |= (1u << cg);
    }
    int g = 0;
    while (seen & (1u << g)) g++;

    memo[S] = (uint8_t)g;
    total++;
    N[k]++;
    Ng[k][g]++;
    if (nmoves == 0) maximal[k]++;
    if (k > maxk) maxk = k;
    return (uint8_t)g;
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "usage: %s board.txt s\n", argv[0]);
        return 2;
    }
    s_cap = atoi(argv[2]);
    if (s_cap < 1 || s_cap > 5) { fprintf(stderr, "bad s\n"); return 2; }

    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open board"); return 1; }
    if (fscanf(f, "%d %d", &n, &b) != 2) { fprintf(stderr, "bad header\n"); return 1; }
    if (n > 32) { fprintf(stderr, "n=%d needs 32-bit masks\n", n); return 1; }
    if (b > 256) { fprintf(stderr, "b=%d too many lines\n", b); return 1; }

    int *clen = malloc((size_t)b * sizeof(int));
    int deg[64] = {0};
    for (int c = 0; c < b; c++) {
        int len;
        if (fscanf(f, "%d", &len) != 1) { fprintf(stderr, "truncated\n"); return 1; }
        clen[c] = len;
        for (int j = 0; j < len; j++) {
            int p;
            if (fscanf(f, "%d", &p) != 1) { fprintf(stderr, "truncated\n"); return 1; }
            if (p < 0 || p >= n) { fprintf(stderr, "bad point\n"); return 1; }
            lmask[c] |= 1u << p;
            deg[p]++;
        }
    }
    fclose(f);
    // The AND-compare legality test below is exactly "line becomes overfull"
    // only when every line has s_cap + 1 points (AG(2,5): 5 points, s=4).
    for (int c = 0; c < b; c++) {
        if (clen[c] != s_cap + 1) {
            fprintf(stderr, "line %d has %d points; this verifier requires "
                    "s_cap+1 = %d\n", c, clen[c], s_cap + 1);
            return 2;
        }
    }
    for (int p = 0; p < n; p++) {
        if (deg[p] > 64) { fprintf(stderr, "degree too high\n"); return 1; }
        npl[p] = 0;
    }
    for (int c = 0; c < b; c++) {
        for (int p = 0; p < n; p++) {
            if (!(lmask[c] & (1u << p))) continue;
            lrest[p][npl[p]++] = lmask[c] & ~(1u << p);
        }
    }

    size_t memo_size = (size_t)1 << n;
    memo = malloc(memo_size);
    if (!memo) { fprintf(stderr, "memo allocation failed\n"); return 1; }
    memset(memo, 0xFF, memo_size);
    N = calloc(65, sizeof(long long));

    root_g = grundy(0u);
    for (int p = 0; p < n; p++) {
        if ((0u & (1u << p))) continue;
        int legal = 1;
        for (int j = 0; j < npl[p]; j++)
            if ((0u & lrest[p][j]) == lrest[p][j]) { legal = 0; break; }
        if (legal) first_g[grundy(1u << p)]++;
    }

    printf("POINTS %d\nCIRCLES %d\nSAFE %lld\nMAXSIZE %d\nROOT %d\n",
           n, b, total, maxk, root_g);

    for (int k = 0; k <= maxk; k++)
        printf("SIZE %d %lld %lld %lld\n", k, N[k], maximal[k], Ng[k][0]);
    for (int g = 0; g < 64; g++) {
        long long s = 0;
        for (int k = 0; k <= maxk; k++) s += Ng[k][g];
        if (s) printf("GRUNDY %d %lld\n", g, s);
    }
    for (int k = 0; k <= maxk; k++)
        for (int g = 0; g < 64; g++)
            if (Ng[k][g]) printf("GSIZE %d %d %lld\n", k, g, Ng[k][g]);
    for (int k = 0; k <= maxk; k++)
        if (maximal[k]) printf("MAXIMAL %d %lld\n", k, maximal[k]);
    for (int g = 0; g < 64; g++)
        if (first_g[g]) printf("FIRSTMOVE %d %d\n", g, first_g[g]);

    return 0;
}
