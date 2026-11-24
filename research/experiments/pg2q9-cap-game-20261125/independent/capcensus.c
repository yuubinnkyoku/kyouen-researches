/* Independent s=2 cap enumerator for projective planes given as a board file.
 *
 * Enumerates every cap (set S with |S ^ L| <= 2 for every line L) exactly once
 * by increasing point sequence, counts sizes, and counts maximal caps.
 *
 * Two independent maximality tests are applied to EVERY cap:
 *   TEST1 (blocked / addable-point mask):
 *       blocked(S) = union of all secant lines of S.  A point can be added iff
 *       it is not on any secant, i.e. iff it is in ~blocked.  S maximal iff
 *       ~blocked == 0.  This is the natural recursive test: the DFS itself only
 *       descends into points outside `blocked`.
 *   TEST2 (secant-through-the-outside-point / inarc test):
 *       for every point q outside S, q is addable iff s -> line(q,s) is
 *       injective on S (no two cap points collinear with q).  S is maximal iff
 *       no outside point is addable.  TEST2 never uses the `blocked` mask.
 *
 * The candidate list is snapshotted (`rest`) before iteration; the recursion
 * never mutates the snapshot it is iterating over (each level recomputes its
 * own copy from its own blocked mask).
 *
 * Usage:
 *   capcensus <boardfile> [--dump9 F] [--dump10 F] [--dump-nonmax8 F]
 *                          [--samples PREFIX] [--quiet]
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

typedef unsigned __int128 u128;

#define MAXN 128
#define MAXK 40

static int N, NL, K;
static int lid[MAXN][MAXN];          /* line id through point pair */
static u128 lmask[MAXN];             /* point mask of a line (NL < MAXN) */
static u128 allmask;
static u128 geq[MAXN + 1];           /* points with index >= i */

static long long cnt[16], mx1[16], mx2[16], ext[16];
static int S[MAXN];
static long long total_nodes;

/* ------------------------------------------------------------------ dumps */
typedef struct {
    u128 *a;
    long long n, cap;
} Dump;

static void dump_push(Dump *d, u128 m)
{
    if (d->n == d->cap) {
        d->cap = d->cap ? d->cap * 2 : 65536;
        d->a = (u128 *)realloc(d->a, (size_t)d->cap * sizeof(u128));
        if (!d->a) { fprintf(stderr, "OOM\n"); exit(2); }
    }
    d->a[d->n++] = m;
}

static void dump_write(const char *path, Dump *d)
{
    FILE *f = fopen(path, "wb");
    if (!f) { fprintf(stderr, "cannot write %s\n", path); exit(2); }
    uint64_t n = (uint64_t)d->n;
    fwrite(&n, 8, 1, f);
    if (n) fwrite(d->a, sizeof(u128), (size_t)n, f);
    fclose(f);
    fprintf(stderr, "wrote %s (%llu masks)\n", path, (unsigned long long)n);
}

/* ---------------------------------------------------------------- samples */
#define NS 50
static const int NCLASS = 5;
static u128 samp[5][NS];
static long long samp_seen[5];
static uint64_t rng_state = 0x9e3779b97f4a7c15ULL;

static uint64_t xorshift64(void)
{
    uint64_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    rng_state = x;
    return x;
}

static void sample_offer(int cls, u128 m)
{
    long long k = ++samp_seen[cls];
    if (k <= NS) {
        samp[cls][k - 1] = m;
    } else {
        uint64_t j = xorshift64() % (uint64_t)k;
        if (j < NS) samp[cls][j] = m;
    }
}

/* ------------------------------------------------------------- test 2 */
/* q addable to cap S iff the lines (q,S[i]) are pairwise distinct. */
static int popcount128(u128 x)
{
    return __builtin_popcountll((uint64_t)x) + __builtin_popcountll((uint64_t)(x >> 64));
}

static int ctz128(u128 x)
{
    uint64_t lo = (uint64_t)x, hi = (uint64_t)(x >> 64);
    if (lo) return __builtin_ctzll(lo);
    return 64 + __builtin_ctzll(hi);
}

static int addable2(const int *cap, int size, int q)
{
    const int *row = lid[q];
    for (int i = 0; i < size; i++) {
        int li = row[cap[i]];
        for (int j = 0; j < i; j++)
            if (row[cap[j]] == li) return 0;
    }
    return 1;
}

static int maximal2(const int *cap, int size, u128 inS)
{
    for (int q = 0; q < N; q++) {
        if ((inS >> q) & 1) continue;
        if (addable2(cap, size, q)) return 0;
    }
    return 1;
}

static u128 mask_of(const int *cap, int size)
{
    u128 m = 0;
    for (int i = 0; i < size; i++) m |= (u128)1 << cap[i];
    return m;
}

/* ------------------------------------------------------------------ DFS */
static Dump d9, d10, dnonmax8;
static int want9, want10, want_nonmax8, want_samples;

static void dfs(u128 blocked, int last, int size)
{
    total_nodes++;
    cnt[size]++;

    u128 avail = (~blocked) & allmask;      /* every addable point */
    int is_max = (avail == 0);
    u128 inS = mask_of(S, size);

    if (is_max) mx1[size]++;
    if (maximal2(S, size, inS)) mx2[size]++;
    ext[size] += popcount128(avail);
    if (size == 9) {
        if (want9) dump_push(&d9, inS);
        if (want_samples) sample_offer(0, inS);
    } else if (size == 10 && want10) {
        dump_push(&d10, inS);
    }
    if (want_samples) {
        if (size == 6 && is_max) sample_offer(1, inS);
        else if (size == 7 && is_max) sample_offer(2, inS);
        else if (size == 8) {
            if (is_max) sample_offer(3, inS);
            else { sample_offer(4, inS); if (want_nonmax8) dump_push(&dnonmax8, inS); }
        }
    } else if (want_nonmax8 && size == 8 && !is_max) {
        dump_push(&dnonmax8, inS);
    }

    /* snapshot of the candidate list BEFORE iterating; never mutated below */
    u128 rest = avail & geq[last + 1];
    while (rest) {
        int p = ctz128(rest);
        u128 bit = (u128)1 << p;
        rest &= ~bit;                       /* consume from the snapshot only */
        u128 nb = blocked;
        for (int i = 0; i < size; i++) nb |= lmask[lid[p][S[i]]];
        S[size] = p;
        dfs(nb, p, size + 1);
    }
}

/* ------------------------------------------------------------------ main */
static int read_board(const char *path)
{
    FILE *f = fopen(path, "r");
    if (!f) { fprintf(stderr, "cannot open %s\n", path); return 0; }
    if (fscanf(f, "%d %d", &N, &NL) != 2) { fprintf(stderr, "bad header\n"); return 0; }
    if (N > MAXN || NL > MAXN) { fprintf(stderr, "board too large\n"); return 0; }
    for (int li = 0; li < NL; li++) {
        int k;
        if (fscanf(f, "%d", &k) != 1) { fprintf(stderr, "bad line %d\n", li); return 0; }
        if (k > MAXK) { fprintf(stderr, "line too long\n"); return 0; }
        u128 m = 0;
        for (int t = 0; t < k; t++) {
            int p;
            if (fscanf(f, "%d", &p) != 1) { fprintf(stderr, "bad point\n"); return 0; }
            if (p < 0 || p >= N) { fprintf(stderr, "point out of range\n"); return 0; }
            m |= (u128)1 << p;
        }
        lmask[li] = m;
    }
    fclose(f);
    K = 0;
    for (int li = 0; li < NL; li++) {
        int c = 0;
        u128 m = lmask[li];
        while (m) { c++; m &= m - 1; }
        if (li == 0) K = c;
        else if (c != K) { fprintf(stderr, "line sizes differ\n"); return 0; }
    }
    /* build pair -> line id table */
    for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) lid[a][b] = -1;
    for (int li = 0; li < NL; li++) {
        int pts[MAXN], c = 0;
        for (int p = 0; p < N; p++) if (((lmask[li] >> p) & 1)) pts[c++] = p;
        for (int i = 0; i < c; i++)
            for (int j = i + 1; j < c; j++) {
                lid[pts[i]][pts[j]] = li;
                lid[pts[j]][pts[i]] = li;
            }
    }
    allmask = ((u128)1 << N) - 1;
    for (int i = 0; i <= N; i++) geq[i] = allmask & ~(((u128)1 << i) - 1);
    geq[N] = 0;
    return 1;
}

int main(int argc, char **argv)
{
    if (argc < 2) {
        fprintf(stderr, "usage: %s board [--dump9 F] [--dump10 F] "
                        "[--dump-nonmax8 F] [--samples PREFIX] [--seed S]\n", argv[0]);
        return 2;
    }
    const char *dump9p = NULL, *dump10p = NULL, *dumpn8p = NULL, *samprefix = NULL;
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "--dump9") && i + 1 < argc) dump9p = argv[++i];
        else if (!strcmp(argv[i], "--dump10") && i + 1 < argc) dump10p = argv[++i];
        else if (!strcmp(argv[i], "--dump-nonmax8") && i + 1 < argc) dumpn8p = argv[++i];
        else if (!strcmp(argv[i], "--samples") && i + 1 < argc) samprefix = argv[++i];
        else if (!strcmp(argv[i], "--seed") && i + 1 < argc) rng_state = strtoull(argv[++i], NULL, 10) | 1;
        else { fprintf(stderr, "unknown arg %s\n", argv[i]); return 2; }
    }
    want9 = dump9p != NULL; want10 = dump10p != NULL;
    want_nonmax8 = dumpn8p != NULL; want_samples = samprefix != NULL;

    if (!read_board(argv[1])) return 2;
    fprintf(stderr, "board %s: n=%d lines=%d k=%d\n", argv[1], N, NL, K);

    long long t0 = (long long)clock();
    dfs(0, -1, 0);
    double secs = (double)((long long)clock() - t0) / CLOCKS_PER_SEC;

    long long tot = 0, totmax = 0;
    printf("board %s\n", argv[1]);
    printf("n %d\nlines %d\nk %d\n", N, NL, K);
    printf("nodes %lld\nseconds %.3f\n", total_nodes, secs);
    for (int k = 0; k <= 12; k++) {
        printf("cnt %d %lld\n", k, cnt[k]);
        printf("max1 %d %lld\n", k, mx1[k]);
        printf("max2 %d %lld\n", k, mx2[k]);
        printf("ext %d %lld\n", k, ext[k]);
        tot += cnt[k];
        totmax += mx1[k];
    }
    printf("total %lld\nmax_total %lld\n", tot, totmax);

    if (want9) dump_write(dump9p, &d9);
    if (want10) dump_write(dump10p, &d10);
    if (want_nonmax8) dump_write(dumpn8p, &dnonmax8);

    if (want_samples) {
        const char *names[5] = {"caps9", "max6", "max7", "max8", "nonmax8"};
        for (int c = 0; c < NCLASS; c++) {
            char path[1024];
            snprintf(path, sizeof path, "%s_%s.txt", samprefix, names[c]);
            FILE *f = fopen(path, "w");
            if (!f) { fprintf(stderr, "cannot write %s\n", path); return 2; }
            long long n = samp_seen[c] < NS ? samp_seen[c] : NS;
            fprintf(f, "# class %s  population %lld  sampled %lld  seed fixed\n",
                    names[c], samp_seen[c], n);
            for (long long i = 0; i < n; i++) {
                for (int p = 0; p < N; p++)
                    if ((samp[c][i] >> p) & 1)
                        fprintf(f, "%d ", p);
                fprintf(f, "\n");
            }
            fclose(f);
            fprintf(stderr, "samples %s: population %lld\n", names[c], samp_seen[c]);
        }
    }
    return 0;
}
