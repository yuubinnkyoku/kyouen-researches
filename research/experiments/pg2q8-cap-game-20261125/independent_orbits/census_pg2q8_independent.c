/* Independent census of caps in PG(2,8): counts every cap by size and counts
 * the maximal ones.  Reads the board file (73 points, 73 lines of 9 points)
 * whose line set is first validated (each of 73 lines distinct; every pair of
 * points on exactly one line).
 *
 * Build:  gcc -O2 -o census_census census_pg2q8_independent.c
 * Run:    ./census_census ../output/board_pg2q8.txt
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define NP 73
#define MAXL 73

static int lof[NP][NP];       /* index of the line through points p,q */
static uint64_t lmask[2 * 128][2]; /* point set of each line (lo,hi words) */
static int nlines = 0;
static uint64_t full[2] = {0, 0};

static long long cnt[20];
static long long mcnt[20];
static long long nodes = 0;

static inline void above_mask(int last, uint64_t *al, uint64_t *ah)
{
    uint64_t lo, hi;
    if (last < 0) { lo = ~0ULL; hi = ~0ULL; }
    else if (last < 63) { lo = ~0ULL << (last + 1); hi = ~0ULL; }
    else if (last == 63) { lo = 0ULL; hi = ~0ULL; }
    else { lo = 0ULL; hi = ~0ULL << (last + 1 - 64); }
    *al = lo & full[0];
    *ah = hi & full[1];
}

static void dfs(int last, int size, uint64_t cl, uint64_t ch,
                uint64_t bl, uint64_t bh)
{
    nodes++;
    cnt[size]++;
    if (((cl | bl) == full[0]) && ((ch | bh) == full[1]))
        mcnt[size]++;
    if (size >= 12)
        return;

    uint64_t al, ah;
    above_mask(last, &al, &ah);
    al &= ~(cl | bl);
    ah &= ~(ch | bh);

    while (al) {
        int q = __builtin_ctzll(al);
        al &= al - 1;
        uint64_t nbl = bl, nbh = bh, t = cl;
        while (t) {
            int p = __builtin_ctzll(t);
            t &= t - 1;
            int L = lof[p][q];
            nbl |= lmask[L][0];
            nbh |= lmask[L][1];
        }
        t = ch;
        while (t) {
            int p = 64 + __builtin_ctzll(t);
            t &= t - 1;
            int L = lof[p][q];
            nbl |= lmask[L][0];
            nbh |= lmask[L][1];
        }
        dfs(q, size + 1, cl | (1ULL << q), ch, nbl, nbh);
    }
    while (ah) {
        int r = __builtin_ctzll(ah);
        ah &= ah - 1;
        int q = 64 + r;
        uint64_t nbl = bl, nbh = bh, t = cl;
        while (t) {
            int p = __builtin_ctzll(t);
            t &= t - 1;
            int L = lof[p][q];
            nbl |= lmask[L][0];
            nbh |= lmask[L][1];
        }
        t = ch;
        while (t) {
            int p = 64 + __builtin_ctzll(t);
            t &= t - 1;
            int L = lof[p][q];
            nbl |= lmask[L][0];
            nbh |= lmask[L][1];
        }
        dfs(q, size + 1, cl, ch | (1ULL << r), nbl, nbh);
    }
}

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: %s boardfile\n", argv[0]); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    int n, b;
    if (fscanf(f, "%d %d", &n, &b) != 2) { fprintf(stderr, "bad header\n"); return 1; }
    if (n != NP || b != NP) { fprintf(stderr, "unexpected board dims %d %d\n", n, b); return 1; }
    int linepts[MAXL][MAXL];
    int lens[MAXL];
    for (int i = 0; i < b; i++) {
        int k;
        if (fscanf(f, "%d", &k) != 1) { fprintf(stderr, "bad line %d\n", i); return 1; }
        lens[i] = k;
        if (k > MAXL) { fprintf(stderr, "line too long\n"); return 1; }
        for (int j = 0; j < k; j++) {
            if (fscanf(f, "%d", &linepts[i][j]) != 1) { fprintf(stderr, "bad point\n"); return 1; }
            if (linepts[i][j] < 0 || linepts[i][j] >= n) { fprintf(stderr, "point out of range\n"); return 1; }
        }
    }
    fclose(f);

    for (int p = 0; p < NP; p++) for (int q = 0; q < NP; q++) lof[p][q] = -1;
    nlines = b;
    for (int i = 0; i < b; i++) {
        uint64_t lo = 0, hi = 0;
        for (int j = 0; j < lens[i]; j++) {
            int p = linepts[i][j];
            if (p < 64) lo |= 1ULL << p; else hi |= 1ULL << (p - 64);
        }
        lmask[i][0] = lo; lmask[i][1] = hi;
        for (int a = 0; a < lens[i]; a++)
            for (int c = a + 1; c < lens[i]; c++) {
                int p = linepts[i][a], q = linepts[i][c];
                if (lof[p][q] != -1) {
                    fprintf(stderr, "FAIL: pair (%d,%d) on two lines (%d,%d)\n", p, q, lof[p][q], i);
                    return 2;
                }
                lof[p][q] = lof[q][p] = i;
            }
    }
    int bad = 0;
    for (int p = 0; p < NP; p++) for (int q = p + 1; q < NP; q++)
        if (lof[p][q] < 0) { fprintf(stderr, "FAIL: pair (%d,%d) on no line\n", p, q); bad++; }
    for (int i = 0; i < b; i++) if (lens[i] != 9) { fprintf(stderr, "FAIL: line %d has %d points\n", i, lens[i]); bad++; }
    if (bad) return 2;
    full[0] = ~0ULL; full[1] = (1ULL << (NP - 64)) - 1;
    /* integrity: full covered by the plane */
    printf("BOARD OK n=%d b=%d pairs=%d\n", n, b, NP * (NP - 1) / 2);

    memset(cnt, 0, sizeof cnt);
    memset(mcnt, 0, sizeof mcnt);
    dfs(-1, 0, 0, 0, 0, 0);

    long long tot = 0, mtot = 0, mtot_pos = 0;
    for (int k = 0; k <= 12; k++) {
        tot += cnt[k];
        mtot += mcnt[k];
        if (mcnt[k] > 0) mtot_pos += mcnt[k];
        if (cnt[k] > 0 || mcnt[k] > 0)
            printf("SIZE %2d total %10lld maximal %10lld\n", k, cnt[k], mcnt[k]);
    }
    printf("TOTAL caps %lld maximal %lld (nodes %lld)\n", tot, mtot, nodes);
    return 0;
}
