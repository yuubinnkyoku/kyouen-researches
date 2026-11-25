/* Independent cap census for PG(2,8): enumerate every cap (independent set of
 * the collinearity hypergraph) exactly once by increasing point order, count by
 * size, and count maximal caps by size.
 *
 * Reads the board (73 lines of 9 point indices) from the path given on the
 * command line.  Uses 73-bit masks in unsigned __int128.
 *
 * Build: gcc -O2 -o cap_census.exe cap_census.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define NP 73

static unsigned __int128 LINE[NP];
static int LINEID[NP][NP];
static unsigned __int128 MASK_GE[NP + 1];
static unsigned __int128 FULL;

static int cap[16];
static unsigned long long cnt[16];
static unsigned long long maxcnt[16];

static inline int ctz128(unsigned __int128 x) {
    uint64_t lo = (uint64_t)x;
    if (lo) return __builtin_ctzll(lo);
    return 64 + __builtin_ctzll((uint64_t)(x >> 64));
}

static void dfs(int start, unsigned __int128 forbidden, unsigned __int128 capmask,
                int size) {
    cnt[size]++;
    /* maximal iff every point outside the cap is forbidden (not addable) */
    if (((capmask | forbidden) & FULL) == FULL) maxcnt[size]++;

    unsigned __int128 cand = MASK_GE[start] & ~forbidden;
    while (cand) {
        int p = ctz128(cand);
        cand &= cand - 1;
        unsigned __int128 nf = forbidden;
        for (int i = 0; i < size; i++) {
            nf |= LINE[LINEID[p][cap[i]]];
        }
        cap[size] = p;
        dfs(p + 1, nf, capmask | (((unsigned __int128)1) << p), size + 1);
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s board.txt\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("fopen"); return 2; }
    int n1, n2;
    if (fscanf(f, "%d %d", &n1, &n2) != 2 || n1 != NP || n2 != NP) {
        fprintf(stderr, "bad header\n"); return 2;
    }
    int lines = 0;
    while (lines < NP) {
        int k;
        if (fscanf(f, "%d", &k) != 1) break;
        if (k != 9) { fprintf(stderr, "bad line length %d\n", k); return 2; }
        int pts[9];
        for (int i = 0; i < 9; i++) {
            if (fscanf(f, "%d", &pts[i]) != 1) { fprintf(stderr, "truncated\n"); return 2; }
        }
        unsigned __int128 m = 0;
        for (int i = 0; i < 9; i++) m |= ((unsigned __int128)1) << pts[i];
        LINE[lines] = m;
        for (int i = 0; i < 9; i++)
            for (int j = i + 1; j < 9; j++) {
                LINEID[pts[i]][pts[j]] = lines;
                LINEID[pts[j]][pts[i]] = lines;
            }
        lines++;
    }
    fclose(f);
    if (lines != NP) { fprintf(stderr, "expected %d lines, got %d\n", NP, lines); return 2; }

    FULL = (((unsigned __int128)1) << NP) - 1;
    for (int s = 0; s < NP; s++) {
        MASK_GE[s] = FULL & ~((((unsigned __int128)1) << s) - 1);
    }
    MASK_GE[NP] = 0;

    memset(cnt, 0, sizeof(cnt));
    memset(maxcnt, 0, sizeof(maxcnt));
    dfs(0, 0, 0, 0);

    unsigned long long total = 0;
    for (int k = 0; k <= 10; k++) {
        printf("caps k=%2d : %llu   maximal: %llu\n", k, cnt[k], maxcnt[k]);
        total += cnt[k];
    }
    printf("TOTAL (including empty) = %llu\n", total);
    printf("TOTAL non-empty = %llu\n", total - 1);
    return 0;
}
