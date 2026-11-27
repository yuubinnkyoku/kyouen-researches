/* Independent enumeration of ALL caps of PG(2,8) (task: independent check of
 * the total number 2,060,352 of maximal 6-caps and that every maximal 6-cap
 * lies in one of the three PGL orbits computed by orbit_bfs.py).
 *
 * Board geometry is read from board_pg2q8.txt.  A cap is a set of points with
 * no three collinear.  Enumerate every cap exactly once as an increasing
 * sequence of point indices (DFS).  For a cap S let F(S) be the union of the
 * lines through pairs of points of S.  A point can be added to S iff it is
 * outside S union F(S).  Hence S is maximal iff S union F(S) is all 73 points.
 *
 * For k >= 3, S and F(S) are disjoint (no 3 collinear), so a k-cap is maximal
 * iff |F(S)| = 73-k.  We use the general test popcount(S | F(S)) == 73.
 *
 * Also loads the caps of the three saved PGL orbits (6 bytes each) into a hash
 * set and counts how many maximal 6-caps are covered.
 *
 * Build:  gcc -O2 -o maxcaps maxcaps.c
 * Run:    ./maxcaps ../output/board_pg2q8.txt .
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef unsigned __int128 u128;

static int LOP[73][73];      /* line index through a pair of points */
static u128 LM[73];          /* 73-bit incidence mask of each line */

static int cap[12];
static long long cap_count[12];
static long long maximal[12];

static long long max6 = 0;
static long long max6_in_union = 0;
static long long max6_not_in_union = 0;
static int shown = 0;

/* ---------------- hash set of packed 6-caps (48-bit keys) ---------------- */
#define HBITS 23
#define HSIZE (1u << HBITS)
static uint64_t *htab;
static long long h_entries = 0, h_dups = 0;

static inline uint64_t pack6(const int *c) {
    uint64_t k = 0;
    for (int i = 0; i < 6; i++) k |= ((uint64_t)(unsigned char)c[i]) << (8 * i);
    return k;
}
static inline uint64_t hash64(uint64_t k) {
    return (k * 11400714819323198485ULL) >> (64 - HBITS);
}
static void h_insert(uint64_t k) {
    uint64_t h = hash64(k);
    while (htab[h]) {
        if (htab[h] == k) { h_dups++; return; }
        h = (h + 1) & (HSIZE - 1);
    }
    htab[h] = k;
    h_entries++;
}
static int h_contains(uint64_t k) {
    uint64_t h = hash64(k);
    while (htab[h]) {
        if (htab[h] == k) return 1;
        h = (h + 1) & (HSIZE - 1);
    }
    return 0;
}

static inline int pc128(u128 x) {
    return __builtin_popcountll((uint64_t)x) + __builtin_popcountll((uint64_t)(x >> 64));
}

static void dfs(int k, int last, u128 forb, u128 capmask) {
    cap_count[k]++;
    if (k >= 3 && pc128(forb | capmask) == 73) {
        maximal[k]++;
        if (k == 6) {
            max6++;
            uint64_t key = pack6(cap);
            if (h_contains(key)) max6_in_union++;
            else {
                max6_not_in_union++;
                if (shown < 10) {
                    printf("  maximal 6-cap NOT in union:");
                    for (int i = 0; i < 6; i++) printf(" %d", cap[i]);
                    printf("\n");
                    shown++;
                }
            }
        }
    }
    for (int p = last + 1; p < 73; p++) {
        if ((forb >> p) & 1) continue;          /* p would create a collinearity */
        u128 nf = forb;
        for (int i = 0; i < k; i++) nf |= LM[LOP[cap[i]][p]];
        cap[k] = p;
        dfs(k + 1, p, nf, capmask | ((u128)1 << p));
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s board [orbit_dir]\n", argv[0]); return 2; }
    const char *board = argv[1];
    const char *odir = (argc > 2) ? argv[2] : ".";

    FILE *f = fopen(board, "r");
    if (!f) { perror(board); return 2; }
    int np, nl;
    if (fscanf(f, "%d %d", &np, &nl) != 2 || np != 73 || nl != 73) {
        fprintf(stderr, "bad header\n"); return 2;
    }
    for (int i = 0; i < 73; i++) {
        int m;
        if (fscanf(f, "%d", &m) != 1 || m != 9) { fprintf(stderr, "bad line %d\n", i); return 2; }
        LM[i] = 0;
        for (int j = 0; j < 9; j++) {
            int p;
            if (fscanf(f, "%d", &p) != 1) { fprintf(stderr, "bad point\n"); return 2; }
            if (p < 0 || p > 72) { fprintf(stderr, "point out of range\n"); return 2; }
            LM[i] |= ((u128)1 << p);
        }
        if (pc128(LM[i]) != 9) { fprintf(stderr, "line %d not 9 distinct points\n", i); return 2; }
    }
    fclose(f);

    for (int p = 0; p < 73; p++)
        for (int q = 0; q < 73; q++)
            LOP[p][q] = -1;
    for (int li = 0; li < 73; li++) {
        for (int p = 0; p < 73; p++) if ((LM[li] >> p) & 1)
            for (int q = 0; q < 73; q++) if (q != p && ((LM[li] >> q) & 1)) {
                if (LOP[p][q] != -1 && LOP[p][q] != li) {
                    fprintf(stderr, "pair %d,%d on two lines\n", p, q); return 2;
                }
                LOP[p][q] = li;
            }
    }
    for (int p = 0; p < 73; p++)
        for (int q = 0; q < 73; q++)
            if (p != q && LOP[p][q] < 0) { fprintf(stderr, "pair %d,%d not covered\n", p, q); return 2; }

    /* ---- load the three orbit files ---- */
    htab = calloc(HSIZE, sizeof(uint64_t));
    if (!htab) { fprintf(stderr, "oom\n"); return 2; }
    const char *names[3] = {"orbit_A.bin", "orbit_B.bin", "orbit_C.bin"};
    long long loaded = 0;
    for (int oi = 0; oi < 3; oi++) {
        char path[1024];
        snprintf(path, sizeof(path), "%s/%s", odir, names[oi]);
        FILE *g = fopen(path, "rb");
        if (!g) { perror(path); return 2; }
        unsigned char buf[6];
        long long n = 0, bad = 0;
        while (fread(buf, 1, 6, g) == 6) {
            long long key = 0;
            for (int i = 0; i < 6; i++) key |= (long long)buf[i] << (8 * i);
            /* validate increasing order */
            if (!(buf[0] < buf[1] && buf[1] < buf[2] && buf[2] < buf[3] &&
                  buf[3] < buf[4] && buf[4] < buf[5])) bad++;
            h_insert((uint64_t)key);
            n++;
            loaded++;
        }
        fclose(g);
        printf("orbit file %-12s : %lld caps (%lld not increasing)\n", names[oi], n, bad);
    }
    printf("loaded entries %lld, unique %lld, duplicates %lld\n", loaded, h_entries, h_dups);
    if (h_entries != 2060352) {
        printf("WARNING: union of orbit files has %lld unique caps, expected 2060352\n", h_entries);
    }

    /* ---- full cap census ---- */
    dfs(0, -1, 0, 0);

    long long total = 0;
    printf("\ncap census by size:\n");
    for (int k = 0; k <= 11; k++) {
        if (cap_count[k]) {
            total += cap_count[k];
            printf("  size %2d : %12lld caps, %10lld maximal\n", k, cap_count[k], maximal[k]);
        }
    }
    printf("  total caps: %lld\n", total);
    printf("\nmaximal 6-caps: %lld\n", max6);
    printf("  in the union of the three PGL orbits: %lld\n", max6_in_union);
    printf("  NOT in the union:                     %lld\n", max6_not_in_union);

    int ok = (total == 19550350LL) && (max6 == 2060352LL) &&
             (max6_in_union == max6) && (h_entries == 2060352LL);
    printf("\n%s\n", ok ? "CENSUS OK" : "CENSUS MISMATCH");
    free(htab);
    return ok ? 0 : 1;
}
