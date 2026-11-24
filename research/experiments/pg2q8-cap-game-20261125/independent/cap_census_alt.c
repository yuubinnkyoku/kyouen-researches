/*
 * cap_census_alt.c -- second, structurally different s=2 cap enumeration.
 *
 * No blocked-counter array: the set of addable points is carried down the
 * recursion as a 73-bit candidate mask.  When p is appended to the cap S,
 *
 *   cand' = (cand \ {p})  \  union_{a in S} line(a,p)
 *
 * because the only points that become non-addable are those lying on a new
 * secant line(a,p).  Consequently S is maximal iff cand == 0, and the size
 * distribution / maximal counts are obtained with a completely different data
 * structure and recursion invariant than in cap_census.c.
 *
 * usage: cap_census_alt <board-file>
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

static int n, b;
static int lines[MAXL][MAXK];
static int lsize[MAXL];
static int pair_line[MAXN][MAXN];
static u128 line_mask[MAXL];
static u128 FULL;

static int Sarr[MAXK];
static long long cnt_size[MAXK];
static long long max_cnt[MAXK];
static int max_size = 0;
static long long total = 0;

static int parse_board(const char *path)
{
    FILE *f = fopen(path, "r");
    if (!f) {
        fprintf(stderr, "cannot open %s\n", path);
        return -1;
    }
    if (fscanf(f, "%d %d", &n, &b) != 2) {
        fclose(f);
        return -1;
    }
    if (n > MAXN || b > MAXL) {
        fclose(f);
        return -1;
    }
    for (int i = 0; i < b; i++) {
        int k;
        if (fscanf(f, "%d", &k) != 1 || k > MAXK) {
            fclose(f);
            return -1;
        }
        lsize[i] = k;
        for (int j = 0; j < k; j++)
            if (fscanf(f, "%d", &lines[i][j]) != 1) {
                fclose(f);
                return -1;
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
                fprintf(stderr, "point out of range\n");
                exit(1);
            }
            m |= ((u128)1) << p;
            for (int y = x + 1; y < lsize[i]; y++) {
                int q = lines[i][y];
                if (pair_line[p][q] != -1) {
                    fprintf(stderr, "pair on two lines\n");
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
                fprintf(stderr, "pair on no line\n");
                exit(1);
            }
}

static void dfs(int depth, int last, u128 cand)
{
    cnt_size[depth]++;
    total++;
    if (depth > max_size)
        max_size = depth;
    if (cand == 0)
        max_cnt[depth]++;

    for (int p = last + 1; p < n; p++) {
        if (((cand >> p) & 1) == 0)
            continue;
        u128 newcand = cand & ~(((u128)1) << p);
        for (int i = 0; i < depth; i++)
            newcand &= ~line_mask[pair_line[Sarr[i]][p]];
        Sarr[depth] = p;
        dfs(depth + 1, p, newcand);
    }
}

int main(int argc, char **argv)
{
    if (argc < 2) {
        fprintf(stderr, "usage: %s <board-file>\n", argv[0]);
        return 2;
    }
    if (parse_board(argv[1]) != 0)
        return 2;
    build_structures();
    clock_t t0 = clock();
    dfs(0, -1, FULL);
    double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
    long long sum = 0;
    for (int k = 0; k <= max_size; k++)
        sum += cnt_size[k];
    printf("BOARD %s\n", argv[1]);
    printf("N %d B %d\n", n, b);
    for (int k = 0; k <= max_size; k++)
        printf("SIZE %d %lld %lld\n", k, cnt_size[k], max_cnt[k]);
    printf("TOTAL %lld\n", sum);
    printf("NODES %lld\n", total);
    printf("MAXSIZE %d\n", max_size);
    printf("SECONDS %.3f\n", secs);
    printf("MAXSIZES");
    for (int k = 0; k <= max_size; k++)
        if (max_cnt[k] > 0)
            printf(" %d(%lld)", k, max_cnt[k]);
    printf("\n");
    return 0;
}
