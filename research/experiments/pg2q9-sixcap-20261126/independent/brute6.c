/* Brute-force check of the PG(2,9) 6-cap counts by direct subset iteration.
 *
 * Completely different algorithm from census.c: instead of a DFS over caps it
 * loops over ALL C(91,6) = 666,563,898 six-subsets of points and tests each
 * one for being a cap with 15 explicit line-contains-exactly-two-points tests.
 * It then reproduces the 6-cap statistics:
 *   - number of 6-subsets scanned (must equal C(91,6)),
 *   - number of 6-caps, number of maximal 6-caps,
 *   - |addable| histogram,
 *   - number of maximal 7-children histogram,
 *   - Grundy distribution (using G(7-cap)=maximal?0:1, see REPORT.md).
 *
 * Usage: brute6 <boardfile>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

typedef unsigned __int128 u128;
typedef unsigned long long ull;

#define MAXP 128
#define MAXL 128

static int N, NL;
static u128 lmask[MAXL];
static int lid[MAXP][MAXP];
static u128 ALL;

static inline int pc(u128 x)
{
    return __builtin_popcountll((ull)x) + __builtin_popcountll((ull)(x >> 64));
}

static inline int ctz128(u128 x)
{
    ull lo = (ull)x;
    if (lo) return __builtin_ctzll(lo);
    return 64 + __builtin_ctzll((ull)(x >> 64));
}

static int read_board(const char *path)
{
    FILE *f = fopen(path, "r");
    if (!f) { fprintf(stderr, "cannot open %s\n", path); return 0; }
    if (fscanf(f, "%d %d", &N, &NL) != 2) { fprintf(stderr, "bad header\n"); return 0; }
    if (N > MAXP || NL > MAXL || N != NL) { fprintf(stderr, "bad size\n"); return 0; }
    int deg[MAXP];
    memset(deg, 0, sizeof deg);
    int line_size = -1;
    for (int li = 0; li < NL; li++) {
        int k;
        if (fscanf(f, "%d", &k) != 1) { fprintf(stderr, "bad line\n"); return 0; }
        if (line_size < 0) line_size = k;
        if (k != line_size) { fprintf(stderr, "line size mismatch\n"); return 0; }
        u128 m = 0;
        for (int t = 0; t < k; t++) {
            int p;
            if (fscanf(f, "%d", &p) != 1) { fprintf(stderr, "bad point\n"); return 0; }
            if (p < 0 || p >= N || ((m >> p) & 1)) { fprintf(stderr, "bad point\n"); return 0; }
            m |= (u128)1 << p;
            deg[p]++;
        }
        lmask[li] = m;
    }
    fclose(f);
    for (int p = 0; p < N; p++)
        if (deg[p] != line_size) { fprintf(stderr, "point degree\n"); return 0; }
    for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) lid[a][b] = -1;
    for (int li = 0; li < NL; li++) {
        int pts[MAXP], c = 0;
        for (int p = 0; p < N; p++) if ((lmask[li] >> p) & 1) pts[c++] = p;
        for (int i = 0; i < c; i++) for (int j = i + 1; j < c; j++) {
            if (lid[pts[i]][pts[j]] != -1) { fprintf(stderr, "pair twice\n"); return 0; }
            lid[pts[i]][pts[j]] = li;
            lid[pts[j]][pts[i]] = li;
        }
    }
    ALL = ((u128)1 << N) - 1;
    return 1;
}

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: %s boardfile\n", argv[0]); return 2; }
    if (!read_board(argv[1])) return 2;
    long long total6 = 1;
    for (int i = 0; i < 6; i++) total6 = total6 * (N - i) / (i + 1);

    printf("board %s N=%d lines=%d\n", argv[1], N, NL);
    printf("expected C(%d,6) = %lld\n", N, total6);

    long long scanned = 0;
    long long caps = 0, maximal = 0;
    long long extHist[128];
    long long maxChildHist[16];
    long long g[8];
    memset(extHist, 0, sizeof extHist);
    memset(maxChildHist, 0, sizeof maxChildHist);
    memset(g, 0, sizeof g);
    long long t0 = (long long)clock();

    int p[6];    for (p[0] = 0; p[0] < N - 5; p[0]++)
     for (p[1] = p[0] + 1; p[1] < N - 4; p[1]++)
      for (p[2] = p[1] + 1; p[2] < N - 3; p[2]++)
       for (p[3] = p[2] + 1; p[3] < N - 2; p[3]++)
        for (p[4] = p[3] + 1; p[4] < N - 1; p[4]++)
         for (p[5] = p[4] + 1; p[5] < N; p[5]++) {
            scanned++;
            u128 m = ((u128)1 << p[0]) | ((u128)1 << p[1]) | ((u128)1 << p[2]) |
                     ((u128)1 << p[3]) | ((u128)1 << p[4]) | ((u128)1 << p[5]);
            u128 blocked = 0;
            int iscap = 1;
            for (int i = 0; i < 6 && iscap; i++)
                for (int j = i + 1; j < 6; j++) {
                    int l = lid[p[i]][p[j]];
                    u128 lm = lmask[l];
                    u128 pair = ((u128)1 << p[i]) | ((u128)1 << p[j]);
                    if ((lm & m) != pair) { iscap = 0; break; }
                    blocked |= lm;
                }
            if (!iscap) continue;
            caps++;
            u128 add = ALL & ~blocked;
            int e = pc(add);
            extHist[e]++;
            if (e == 0) maximal++;
            int nMax = 0;
            u128 a = add;
            while (a) {
                int q = ctz128(a);
                a &= ~((u128)1 << q);
                u128 nb = blocked;
                for (int i = 0; i < 6; i++) nb |= lmask[lid[q][p[i]]];
                if (nb == ALL) nMax++;
            }
            maxChildHist[nMax > 15 ? 15 : nMax]++;
            if (e == 0) g[0]++;
            else if (nMax == e) g[1]++;
            else if (nMax > 0) g[2]++;
            else g[0]++;
        }

    double secs = (double)((long long)clock() - t0) / CLOCKS_PER_SEC;
    printf("scanned %lld (expected %lld) %s\n", scanned, total6,
           scanned == total6 ? "OK" : "MISMATCH");
    printf("6-caps %lld  maximal6 %lld  seconds %.3f\n", caps, maximal, secs);
    printf("ext histogram:");
    for (int e = 0; e < 128; e++) if (extHist[e]) printf(" %d:%lld", e, extHist[e]);
    printf("\nmax-child histogram:");
    for (int e = 0; e < 16; e++) if (maxChildHist[e]) printf(" %d:%lld", e, maxChildHist[e]);
    printf("\nGrundy: g0=%lld g1=%lld g2=%lld g3+=%lld sum=%lld\n",
           g[0], g[1], g[2], g[3], g[0] + g[1] + g[2] + g[3]);
    printf("#6-caps with a maximal 7-child = %lld\n", g[1] + g[2]);
    printf("#6-caps with ext==1 = %lld\n", extHist[1]);
    return 0;
}
