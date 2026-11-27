/* Brute-force caps of size 1..5 by direct subset iteration (independent of DFS).
 * Counts caps, maximal caps, and the |addable| histogram for each size.
 * Usage: brute_small <boardfile>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

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

static int read_board(const char *path)
{
    FILE *f = fopen(path, "r");
    if (!f) { fprintf(stderr, "cannot open %s\n", path); return 0; }
    if (fscanf(f, "%d %d", &N, &NL) != 2) return 0;
    int deg[MAXP];
    memset(deg, 0, sizeof deg);
    int line_size = -1;
    for (int li = 0; li < NL; li++) {
        int k;
        if (fscanf(f, "%d", &k) != 1) return 0;
        if (line_size < 0) line_size = k;
        u128 m = 0;
        for (int t = 0; t < k; t++) {
            int p;
            if (fscanf(f, "%d", &p) != 1) return 0;
            m |= (u128)1 << p;
            deg[p]++;
        }
        lmask[li] = m;
    }
    fclose(f);
    for (int p = 0; p < N; p++) if (deg[p] != line_size) return 0;
    for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) lid[a][b] = -1;
    for (int li = 0; li < NL; li++) {
        int pts[MAXP], c = 0;
        for (int p = 0; p < N; p++) if ((lmask[li] >> p) & 1) pts[c++] = p;
        for (int i = 0; i < c; i++) for (int j = i + 1; j < c; j++)
            lid[pts[i]][pts[j]] = lid[pts[j]][pts[i]] = li;
    }
    ALL = ((u128)1 << N) - 1;
    return 1;
}

static long long cnt, maxc, extsum, exthist[128];

static void check_cap(const int *p, int k)
{
    u128 m = 0;
    for (int i = 0; i < k; i++) m |= (u128)1 << p[i];
    u128 blocked = 0;
    for (int i = 0; i < k; i++)
        for (int j = i + 1; j < k; j++) {
            int l = lid[p[i]][p[j]];
            u128 pair = ((u128)1 << p[i]) | ((u128)1 << p[j]);
            if ((lmask[l] & m) != pair) return;
            blocked |= lmask[l];
        }
    cnt++;
    u128 add = ALL & ~blocked;
    int e = pc(add);
    exthist[e]++;
    extsum += e;
    if (e == 0) maxc++;
}

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: %s boardfile\n", argv[0]); return 2; }
    if (!read_board(argv[1])) return 2;
    printf("brute-force caps by size (direct subset iteration), N=%d\n", N);
    int p[5];
    for (int k = 1; k <= 5; k++) {
        cnt = maxc = extsum = 0;
        memset(exthist, 0, sizeof exthist);
        if (k == 1) {
            for (p[0] = 0; p[0] < N; p[0]++) check_cap(p, 1);
        } else if (k == 2) {
            for (p[0] = 0; p[0] < N; p[0]++)
             for (p[1] = p[0] + 1; p[1] < N; p[1]++) check_cap(p, 2);
        } else if (k == 3) {
            for (p[0] = 0; p[0] < N; p[0]++)
             for (p[1] = p[0] + 1; p[1] < N; p[1]++)
              for (p[2] = p[1] + 1; p[2] < N; p[2]++) check_cap(p, 3);
        } else if (k == 4) {
            for (p[0] = 0; p[0] < N; p[0]++)
             for (p[1] = p[0] + 1; p[1] < N; p[1]++)
              for (p[2] = p[1] + 1; p[2] < N; p[2]++)
               for (p[3] = p[2] + 1; p[3] < N; p[3]++) check_cap(p, 4);
        } else {
            for (p[0] = 0; p[0] < N; p[0]++)
             for (p[1] = p[0] + 1; p[1] < N; p[1]++)
              for (p[2] = p[1] + 1; p[2] < N; p[2]++)
               for (p[3] = p[2] + 1; p[3] < N; p[3]++)
                for (p[4] = p[3] + 1; p[4] < N; p[4]++) check_cap(p, 5);
        }
        printf("k=%d caps=%lld maximal=%lld extsum=%lld exthist:",
               k, cnt, maxc, extsum);
        for (int e = 0; e < 128; e++) if (exthist[e]) printf(" %d:%lld", e, exthist[e]);
        printf("\n");
    }
    return 0;
}
