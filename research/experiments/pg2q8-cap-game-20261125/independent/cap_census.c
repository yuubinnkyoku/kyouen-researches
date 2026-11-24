/*
 * cap_census.c -- independent s=2 cap census for PG(2,8) / AG(2,8)
 *
 * Enumerates every cap (subset of points with at most 2 points on every line)
 * exactly once by an increasing-point DFS.  For every cap node it computes
 *
 *   TEST 1 ("inarc" / blocked array):  pc[q] = number of secant pairs {a,b} of S
 *           with q on line(a,b), maintained incrementally.  S is maximal iff
 *           zero_count == |S| (the only unblocked points are the points of S).
 *   TEST 2 (recomputed union of secants): U = union over pairs {a,b} of S of the
 *           line(a,b); S maximal iff (U | S) == all points.
 *
 * It also reservoir-samples caps for spot checks (50 per requested class).
 *
 * usage: cap_census <board-file> [seed]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

typedef unsigned __int128 u128;

#define MAXN 80
#define MAXL 100
#define MAXK 16
#define NSAMP 50

static int n, b;
static int lines[MAXL][MAXK];
static int lsize[MAXL];
static int pair_line[MAXN][MAXN];
static u128 line_mask[MAXL];
static u128 FULL;

static int Sarr[MAXK];
static unsigned char pc[MAXN];
static int zero_count;
static u128 S_mask;

static long long cnt_size[MAXK];
static long long max1_cnt[MAXK];
static long long max2_cnt[MAXK];
static long long add_hist[MAXK][MAXN + 1]; /* [size][exact number of addable points] */
static int max_size = 0;
static long long total_nodes = 0;
static long long disagree = 0;

typedef struct {
    int size;
    int status; /* 0 = non-maximal, 1 = maximal, 2 = either */
    const char *label;
    long long count;
    int stored;
    int caps[NSAMP][MAXK];
} Res;

static Res res[16];
static int nres = 0;

static uint64_t rng_state = 0x9e3779b97f4a7c15ULL;

static uint64_t rnd64(void)
{
    uint64_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    rng_state = x;
    return x;
}

static int parse_board(const char *path)
{
    FILE *f = fopen(path, "r");
    if (!f) {
        fprintf(stderr, "cannot open %s\n", path);
        return -1;
    }
    if (fscanf(f, "%d %d", &n, &b) != 2) {
        fprintf(stderr, "bad header\n");
        fclose(f);
        return -1;
    }
    if (n > MAXN || b > MAXL) {
        fprintf(stderr, "board too large\n");
        fclose(f);
        return -1;
    }
    for (int i = 0; i < b; i++) {
        int k;
        if (fscanf(f, "%d", &k) != 1 || k > MAXK) {
            fprintf(stderr, "bad line %d\n", i);
            fclose(f);
            return -1;
        }
        lsize[i] = k;
        for (int j = 0; j < k; j++) {
            if (fscanf(f, "%d", &lines[i][j]) != 1) {
                fprintf(stderr, "bad point in line %d\n", i);
                fclose(f);
                return -1;
            }
        }
    }
    fclose(f);
    return 0;
}

static void build_structures(void)
{
    FULL = (((u128)1) << n) - 1;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            pair_line[i][j] = -1;
    for (int i = 0; i < b; i++) {
        u128 m = 0;
        for (int x = 0; x < lsize[i]; x++) {
            int p = lines[i][x];
            if (p < 0 || p >= n) {
                fprintf(stderr, "point out of range in line %d\n", i);
                exit(1);
            }
            m |= ((u128)1) << p;
            for (int y = x + 1; y < lsize[i]; y++) {
                int q = lines[i][y];
                if (pair_line[p][q] != -1) {
                    fprintf(stderr, "pair (%d,%d) on two lines: %d %d\n",
                            p, q, pair_line[p][q], i);
                    exit(1);
                }
                pair_line[p][q] = i;
                pair_line[q][p] = i;
            }
        }
        line_mask[i] = m;
    }
    for (int p = 0; p < n; p++)
        for (int q = p + 1; q < n; q++)
            if (pair_line[p][q] < 0) {
                fprintf(stderr, "pair (%d,%d) on no line\n", p, q);
                exit(1);
            }
    zero_count = n;
    memset(pc, 0, sizeof(pc));
}

/* add point p (pc[p] must be 0) at index "depth" */
static void add_point(int p, int depth)
{
    Sarr[depth] = p;
    for (int i = 0; i < depth; i++) {
        int a = Sarr[i];
        int li = pair_line[a][p];
        for (int t = 0; t < lsize[li]; t++) {
            int q = lines[li][t];
            if (q == a || q == p)
                continue;
            if (pc[q] == 0)
                zero_count--;
            pc[q]++;
        }
    }
}

static void remove_point(int p, int depth)
{
    for (int i = 0; i < depth; i++) {
        int a = Sarr[i];
        int li = pair_line[a][p];
        for (int t = 0; t < lsize[li]; t++) {
            int q = lines[li][t];
            if (q == a || q == p)
                continue;
            pc[q]--;
            if (pc[q] == 0)
                zero_count++;
        }
    }
}

static void offer_sample(int s, int depth)
{
    Res *R = &res[s];
    R->count++;
    long long idx;
    if (R->count <= NSAMP) {
        idx = R->count - 1;
        R->stored++;
    } else {
        uint64_t j = rnd64() % (uint64_t)R->count;
        if (j >= NSAMP)
            return;
        idx = (long long)j;
    }
    for (int i = 0; i < depth; i++)
        R->caps[idx][i] = Sarr[i];
}

static void dfs(int depth, int start)
{
    total_nodes++;
    cnt_size[depth]++;
    if (depth > max_size)
        max_size = depth;

    int max1 = (zero_count == depth);

    /* TEST 2: recompute the union of all secants from scratch */
    u128 U = 0;
    for (int i = 0; i < depth; i++)
        for (int j = i + 1; j < depth; j++)
            U |= line_mask[pair_line[Sarr[i]][Sarr[j]]];
    int max2 = (((U | S_mask) & FULL) == FULL);

    if (max1 != max2) {
        disagree++;
        if (disagree <= 5) {
            printf("DISAGREE at size %d cap:", depth);
            for (int i = 0; i < depth; i++)
                printf(" %d", Sarr[i]);
            printf("  max1=%d max2=%d zero_count=%d\n", max1, max2, zero_count);
        }
    }
    if (max1)
        max1_cnt[depth]++;
    if (max2)
        max2_cnt[depth]++;
    {
        int addable = zero_count - depth;
        if (addable < 0 || addable > MAXN)
            addable = MAXN;
        add_hist[depth][addable]++;
    }

    for (int s = 0; s < nres; s++) {
        if (res[s].size == depth &&
            (res[s].status == 2 || res[s].status == max1))
            offer_sample(s, depth);
    }

    for (int p = start; p < n; p++) {
        if (pc[p] != 0)
            continue;
        u128 bit = ((u128)1) << p;
        add_point(p, depth);
        S_mask |= bit;
        dfs(depth + 1, p + 1);
        S_mask &= ~bit;
        remove_point(p, depth);
    }
}

int main(int argc, char **argv)
{
    if (argc < 2) {
        fprintf(stderr, "usage: %s <board-file> [seed]\n", argv[0]);
        return 2;
    }
    if (parse_board(argv[1]) != 0)
        return 2;
    if (argc >= 3)
        rng_state = (uint64_t)strtoull(argv[2], NULL, 10);

    build_structures();

    /* sampling plan */
    if (n == 73) { /* PG(2,8) */
        res[nres++] = (Res){6, 1, "PG6max", 0, 0, {{0}}};
        res[nres++] = (Res){6, 0, "PG6non", 0, 0, {{0}}};
        res[nres++] = (Res){7, 2, "PG7", 0, 0, {{0}}};
        res[nres++] = (Res){8, 2, "PG8", 0, 0, {{0}}};
        res[nres++] = (Res){9, 2, "PG9", 0, 0, {{0}}};
        res[nres++] = (Res){10, 1, "PG10max", 0, 0, {{0}}};
    } else if (n == 64) { /* AG(2,8) */
        res[nres++] = (Res){6, 1, "AG6max", 0, 0, {{0}}};
        res[nres++] = (Res){6, 0, "AG6non", 0, 0, {{0}}};
        res[nres++] = (Res){7, 2, "AG7", 0, 0, {{0}}};
        res[nres++] = (Res){8, 1, "AG8max", 0, 0, {{0}}};
        res[nres++] = (Res){8, 0, "AG8non", 0, 0, {{0}}};
        res[nres++] = (Res){9, 2, "AG9", 0, 0, {{0}}};
    }

    clock_t t0 = clock();
    dfs(0, 0);
    double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;

    long long sum = 0;
    for (int k = 0; k <= max_size; k++)
        sum += cnt_size[k];

    printf("BOARD %s\n", argv[1]);
    printf("N %d B %d FULLBITS %d\n", n, b, n);
    for (int k = 0; k <= max_size; k++)
        printf("SIZE %d %lld %lld %lld\n", k, cnt_size[k], max1_cnt[k], max2_cnt[k]);
    printf("TOTAL %lld\n", sum);
    printf("NODES %lld\n", total_nodes);
    printf("MAXSIZE %d\n", max_size);
    printf("DISAGREE %lld\n", disagree);
    printf("SECONDS %.3f\n", secs);
    printf("RNGSEED %llu\n", (unsigned long long)rng_state);
    printf("MAXSIZES");
    for (int k = 0; k <= max_size; k++)
        if (max1_cnt[k] > 0)
            printf(" %d(%lld)", k, max1_cnt[k]);
    printf("\n");
    for (int k = 0; k <= max_size; k++)
        for (int a = 0; a <= MAXN; a++)
            if (add_hist[k][a])
                printf("ADDHIST %d %d %lld\n", k, a, add_hist[k][a]);
    for (int s = 0; s < nres; s++) {
        printf("RES %s size=%d status=%d count=%lld stored=%d\n",
               res[s].label, res[s].size, res[s].status, res[s].count,
               res[s].stored);
        for (int i = 0; i < res[s].stored && i < NSAMP; i++) {
            printf("SAMPLE %s %d", res[s].label, res[s].size);
            for (int j = 0; j < res[s].size; j++)
                printf(" %d", res[s].caps[i][j]);
            printf("\n");
        }
    }
    return 0;
}
