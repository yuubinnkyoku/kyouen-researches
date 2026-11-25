/* Independent census / six-subset / 6-cap Grundy computation for the board
 * research/experiments/pg2q9-cap-game-20261125/output/board_pg2q9.txt.
 *
 * Written from scratch for the independent verification of the six-cap claims.
 * It does NOT share code with the parent's sixsub.c / sortcount.c.
 *
 * What it computes (all by one exhaustive DFS over caps in increasing point
 * order, exactly once per cap):
 *   - number of caps by size and number of maximal caps by size;
 *   - the |addable| histogram by size (ext[k] sum must equal (k+1)*cnt[k+1]);
 *   - for every 6-cap: |addable|, number of maximal 7-children, and the exact
 *     Grundy value (using the independently checked facts G(10)=0, G(9)=1,
 *     G(8)=0, G(7)=maximal?0:1; see REPORT.md);
 *   - for every maximal 7-arc: the 7 six-subsets, their |addable|, their
 *     combinatorial rank, and a distinctness bitmap over all C(91,6) six-subsets.
 *
 * The bitmap gives |subsets| (total marks) and the number of distinct subsets,
 * hence duplicate count, without sorting.
 *
 * Usage: census <boardfile>
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
static int line_size;
static u128 lmask[MAXL];
static int lid[MAXP][MAXP];
static u128 ALL;
static u128 geq[MAXP + 2];
static int S[16];
static long long binom[128][10];

/* size-indexed counts (sizes 0..12) */
static long long cnt[16];
static long long maxcnt[16];
static long long extSum[16];
static long long extHist[16][128];

/* 6-cap data */
static long long extHist6[128];
static long long joint6[128][2];      /* [|addable|][has maximal 7-child] */
static long long g6[8];
static long long maxChildHist[16];

/* six-subsets of maximal 7-arcs */
static long long extHistSix[128];
static long long sixCount, sixBadInter, arcAllSeven, arcAnyNotSeven;
static long long sbmMarks, sbmDups;
static unsigned char *sbm;
static long long SBMBITS;

static long long totalNodes;

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

static long long rank6(const int *x)
{
    long long r = 0;
    for (int i = 0; i < 6; i++) r += binom[x[i]][i + 1];
    return r;
}

static int bit_set(long long r)
{
    unsigned char b = (unsigned char)(1u << (r & 7));
    unsigned char *p = &sbm[r >> 3];
    int old = (*p & b) != 0;
    *p |= b;
    return old;
}

static int read_board(const char *path)
{
    FILE *f = fopen(path, "r");
    if (!f) { fprintf(stderr, "cannot open %s\n", path); return 0; }
    if (fscanf(f, "%d %d", &N, &NL) != 2) { fprintf(stderr, "bad header\n"); return 0; }
    if (N > MAXP || NL > MAXL || N != NL) { fprintf(stderr, "bad size\n"); return 0; }
    int deg[MAXP];
    memset(deg, 0, sizeof deg);
    for (int li = 0; li < NL; li++) {
        int k;
        if (fscanf(f, "%d", &k) != 1) { fprintf(stderr, "bad line %d\n", li); return 0; }
        if (li == 0) line_size = k;
        if (k != line_size) { fprintf(stderr, "line size mismatch\n"); return 0; }
        u128 m = 0;
        for (int t = 0; t < k; t++) {
            int p;
            if (fscanf(f, "%d", &p) != 1) { fprintf(stderr, "bad point\n"); return 0; }
            if (p < 0 || p >= N) { fprintf(stderr, "point out of range\n"); return 0; }
            if ((m >> p) & 1) { fprintf(stderr, "duplicate point in line\n"); return 0; }
            m |= (u128)1 << p;
            deg[p]++;
        }
        if (m == 0) { fprintf(stderr, "empty line\n"); return 0; }
        lmask[li] = m;
    }
    fclose(f);
    for (int p = 0; p < N; p++)
        if (deg[p] != line_size) { fprintf(stderr, "point degree %d != %d\n", deg[p], line_size); return 0; }
    for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) lid[a][b] = -1;
    for (int li = 0; li < NL; li++) {
        int pts[MAXP], c = 0;
        for (int p = 0; p < N; p++) if ((lmask[li] >> p) & 1) pts[c++] = p;
        for (int i = 0; i < c; i++)
            for (int j = i + 1; j < c; j++) {
                if (lid[pts[i]][pts[j]] != -1) {
                    fprintf(stderr, "pair on two lines\n"); return 0;
                }
                lid[pts[i]][pts[j]] = li;
                lid[pts[j]][pts[i]] = li;
            }
    }
    for (int a = 0; a < N; a++)
        for (int b = a + 1; b < N; b++)
            if (lid[a][b] == -1) { fprintf(stderr, "pair on no line\n"); return 0; }
    ALL = ((u128)1 << N) - 1;
    for (int i = 0; i <= N; i++) geq[i] = ALL & ~(((u128)1 << i) - 1);
    geq[N] = 0;
    memset(binom, 0, sizeof binom);
    for (int n = 0; n < 128; n++) {
        binom[n][0] = 1;
        for (int k = 1; k < 10; k++) {
            if (k > n) binom[n][k] = 0;
            else if (k == n) binom[n][k] = 1;
            else binom[n][k] = binom[n - 1][k - 1] + binom[n - 1][k];
        }
    }
    return 1;
}

static void dfs(u128 blocked, int last, int size)
{
    totalNodes++;
    cnt[size]++;
    u128 avail = ALL & ~blocked;
    int e = pc(avail);
    extHist[size][e]++;
    extSum[size] += e;
    if (e == 0) maxcnt[size]++;

    if (size == 6) {
        extHist6[e]++;
        int nMax = 0;
        u128 a = avail;
        while (a) {
            int q = ctz128(a);
            a &= ~((u128)1 << q);
            u128 nb = blocked;
            for (int i = 0; i < 6; i++) nb |= lmask[lid[q][S[i]]];
            if (nb == ALL) nMax++;
        }
        maxChildHist[nMax > 15 ? 15 : nMax]++;
        joint6[e][nMax > 0 ? 1 : 0]++;
        if (e == 0) g6[0]++;
        else if (nMax == e) g6[1]++;   /* only terminal children -> mex{0}=1 */
        else if (nMax > 0) g6[2]++;    /* both terminal and non-terminal -> mex{0,1}=2 */
        else g6[0]++;                  /* only non-terminal children (G=1) -> mex{1}=0 */
    }

    if (size == 7 && e == 0) {
        u128 Amask = 0;
        for (int i = 0; i < 7; i++) Amask |= (u128)1 << S[i];
        int all7 = 1;
        for (int skip = 0; skip < 7; skip++) {
            int xs[6], m = 0;
            u128 X = 0;
            for (int j = 0; j < 7; j++)
                if (j != skip) { xs[m++] = S[j]; X |= (u128)1 << S[j]; }
            u128 blockedX = 0;
            for (int i = 0; i < 6; i++)
                for (int j = i + 1; j < 6; j++)
                    blockedX |= lmask[lid[xs[i]][xs[j]]];
            u128 add = ALL & ~blockedX;
            int ex = pc(add);
            extHistSix[ex]++;
            if (ex != 7) all7 = 0;
            sixCount++;
            if ((add & Amask) != ((u128)1 << S[skip])) sixBadInter++;
            long long r = rank6(xs);
            int dup = bit_set(r);
            sbmMarks++;
            if (dup) sbmDups++;
        }
        if (all7) arcAllSeven++;
        else arcAnyNotSeven++;
    }

    u128 rest = avail & geq[last + 1];
    while (rest) {
        int p = ctz128(rest);
        rest &= ~((u128)1 << p);
        u128 nb = blocked;
        for (int i = 0; i < size; i++) nb |= lmask[lid[p][S[i]]];
        S[size] = p;
        dfs(nb, p, size + 1);
    }
}

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: %s boardfile\n", argv[0]); return 2; }
    if (!read_board(argv[1])) return 2;
    printf("board %s\n", argv[1]);
    printf("N %d lines %d line_size %d\n", N, NL, line_size);

    /* C(91,6) bitmap */
    long long total6 = 1;
    for (int i = 0; i < 6; i++) total6 = total6 * (N - i) / (i + 1);
    SBMBITS = total6;
    long long bytes = (total6 + 7) / 8;
    sbm = (unsigned char *)calloc((size_t)bytes, 1);
    if (!sbm) { fprintf(stderr, "cannot allocate %lld bytes\n", bytes); return 2; }
    printf("C(%d,6) = %lld, bitmap bytes = %lld\n", N, total6, bytes);

    long long t0 = (long long)clock();
    dfs(0, -1, 0);
    double secs = (double)((long long)clock() - t0) / CLOCKS_PER_SEC;

    printf("nodes %lld\nseconds %.3f\n", totalNodes, secs);
    printf("size cnt maxcnt extsum\n");
    long long tc = 0, tm = 0, te = 0;
    for (int k = 0; k <= 12; k++) {
        printf("%d %lld %lld %lld\n", k, cnt[k], maxcnt[k], extSum[k]);
        tc += cnt[k]; tm += maxcnt[k]; te += extSum[k];
    }
    printf("total caps %lld\nmaximal total %lld\next total %lld\n", tc, tm, te);

    /* check sum ext[k] = (k+1)*cnt[k+1] */
    printf("extension-identity:\n");
    for (int k = 0; k <= 12; k++)
        printf("  ext[%d]=%lld  (k+1)*cnt[%d]=%lld\n",
               k, extSum[k], k + 1, (long long)(k + 1) * cnt[k + 1]);

    printf("ext histogram by size:\n");
    for (int k = 0; k <= 12; k++) {
        printf("  k=%d:", k);
        for (int e = 0; e < 128; e++) if (extHist[k][e]) printf(" %d:%lld", e, extHist[k][e]);
        printf("\n");
    }

    printf("six-subsets of maximal 7-arcs:\n");
    printf("  arcs %lld  six_subsets %lld  bad_add_inter %lld\n",
           maxcnt[7], sixCount, sixBadInter);
    printf("  arcAllSeven %lld  arcAnyNotSeven %lld\n", arcAllSeven, arcAnyNotSeven);
    printf("  ext histogram:");
    for (int e = 0; e < 128; e++) if (extHistSix[e]) printf(" %d:%lld", e, extHistSix[e]);
    printf("\n");
    long long bits = 0;
    for (long long i = 0; i < bytes; i++) bits += __builtin_popcount((unsigned)sbm[i]);
    printf("  marks %lld  distinct(sbm popcount) %lld  dups %lld\n",
           sbmMarks, bits, sbmDups);
    printf("  marks == 7*maxcnt7 ? %s\n",
           sbmMarks == 7 * maxcnt[7] ? "yes" : "NO");
    printf("  distinct == marks ? %s\n", bits == sbmMarks ? "yes" : "NO");

    printf("6-cap data:\n");
    printf("  ext histogram:");
    for (int e = 0; e < 128; e++) if (extHist6[e]) printf(" %d:%lld", e, extHist6[e]);
    printf("\n");
    printf("  max-child-count histogram:");
    for (int e = 0; e < 16; e++) if (maxChildHist[e]) printf(" %d:%lld", e, maxChildHist[e]);
    printf("\n");
    printf("  joint (ext,hasMaxChild):");
    for (int e = 0; e < 128; e++)
        if (joint6[e][0] || joint6[e][1])
            printf(" (%d,%d):%lld (%d,%d):%lld", e, 0, joint6[e][0], e, 1, joint6[e][1]);
    printf("\n");
    printf("  Grundy distribution g6[0]=%lld g6[1]=%lld g6[2]=%lld g6[3+]=%lld sum=%lld\n",
           g6[0], g6[1], g6[2], g6[3], g6[0] + g6[1] + g6[2] + g6[3]);
    printf("  g6 sum == cnt[6] ? %s\n",
           g6[0] + g6[1] + g6[2] + g6[3] == cnt[6] ? "yes" : "NO");
    printf("  #6-caps with a maximal 7-child = %lld\n",
           g6[1] + g6[2]);
    printf("  #6-caps with |addable|==1 = %lld, of which with max child = %lld\n",
           extHist6[1], joint6[1][1]);
    free(sbm);
    return 0;
}
