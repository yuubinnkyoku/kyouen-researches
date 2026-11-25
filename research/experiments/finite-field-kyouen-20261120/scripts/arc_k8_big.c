// k=8 arc count at q=11 (and beyond) via the PROFILE method in C.
//
// Brute enumeration of C(122,8) = 9.6e11 is too slow.  The profile method
// is much cheaper:
//
//   For each 4-subset T of the base circle C (C(s,4) of them) and each
//   4-subset {w,x,y,z} of the points outside C (C(n-s,4) of them),
//   compute the profile of S = T u {w,x,y,z} and accumulate.
//
//   Then #8-arcs = C(n,8) - sum over profiles of (tuples / #4-circles) * b
//   ... but that requires the multiplicity theorem to hold for k=8, which
//   is NOT yet established.
//
// SAFER: count 8-arcs directly but with a much better algorithm.
//
// KEY IDEA: an 8-set is an arc iff it contains NO 4-circle.  Equivalently,
// for each 4-circle D, the 8-sets containing D are "bad".  So
//
//   #arcs = C(n,8) - |union over D of {S : D subset S}|
//
// Inclusion-exclusion over 154,980 (q=9) or 1.1M (q=11) sets is too much.
//
// BETTER: use the fact that a 4-circle is determined by 4 points, and
// count arcs by EXTENDING 7-arcs.  A 7-arc has 17,003,520 instances at
// q=9.  For each, try adding each of the n-7 remaining points and check
// whether the result is an 8-arc.  That is 17M * 75 = 1.3e9 checks, each
// cheap (does the new point complete a 4-circle with 3 of the 7?).
//
// At q=11: #7-arcs is unknown but likely ~1e9, times 115 = 1.2e11 -- too slow.
//
// PRAGMATIC CHOICE: run the brute-force k=8 at q=11 in the background and
// accept ~6 hours.  Meanwhile record what we have.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 512
#define MAXB 8192
#define MAXS 64

static int n, b;
static int circ_len[MAXB];
static int circ_pts[MAXB][MAXS];

#define HSIZE (1 << 24)
static uint64_t *htab;

static inline uint64_t pack4(int a, int c, int d, int e) {
    return ((uint64_t)a << 24) | ((uint64_t)c << 16) | ((uint64_t)d << 8) | (uint64_t)e;
}

static void hinsert(uint64_t key) {
    uint64_t h = (key * 0x9E3779B97F4A7C15ULL) >> 40;
    while (htab[h] != 0) {
        if (htab[h] == key + 1) return;
        h = (h + 1) & (HSIZE - 1);
    }
    htab[h] = key + 1;
}

static inline int hcontains(uint64_t key) {
    uint64_t h = (key * 0x9E3779B97F4A7C15ULL) >> 40;
    while (htab[h] != 0) {
        if (htab[h] == key + 1) return 1;
        h = (h + 1) & (HSIZE - 1);
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s circles.txt\n", argv[0]); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    if (fscanf(f, "%d %d", &n, &b) != 2) { fprintf(stderr, "bad header\n"); return 1; }
    for (int i = 0; i < b; i++) {
        int k;
        if (fscanf(f, "%d", &k) != 1) { fprintf(stderr, "bad line %d\n", i); return 1; }
        circ_len[i] = k;
        for (int j = 0; j < k; j++) {
            if (fscanf(f, "%d", &circ_pts[i][j]) != 1) { fprintf(stderr, "bad pt\n"); return 1; }
        }
    }
    fclose(f);

    fprintf(stderr, "n=%d b=%d\n", n, b);

    htab = calloc(HSIZE, sizeof(uint64_t));
    if (!htab) { fprintf(stderr, "oom\n"); return 1; }
    for (int i = 0; i < b; i++) {
        int k = circ_len[i];
        for (int a = 0; a < k; a++)
            for (int c = a + 1; c < k; c++)
                for (int d = c + 1; d < k; d++)
                    for (int e = d + 1; e < k; e++)
                        hinsert(pack4(circ_pts[i][a], circ_pts[i][c],
                                      circ_pts[i][d], circ_pts[i][e]));
    }
    fprintf(stderr, "4-circles built\n");

    long long arcs = 0, total = 0;
    int S[8];
    for (S[0] = 0; S[0] < n; S[0]++)
    for (S[1] = S[0]+1; S[1] < n; S[1]++)
    for (S[2] = S[1]+1; S[2] < n; S[2]++)
    for (S[3] = S[2]+1; S[3] < n; S[3]++)
    for (S[4] = S[3]+1; S[4] < n; S[4]++)
    for (S[5] = S[4]+1; S[5] < n; S[5]++)
    for (S[6] = S[5]+1; S[6] < n; S[6]++)
    for (S[7] = S[6]+1; S[7] < n; S[7]++) {
        total++;
        int bad = 0;
        for (int a = 0; a < 5 && !bad; a++)
        for (int c = a+1; c < 6 && !bad; c++)
        for (int d = c+1; d < 7 && !bad; d++)
        for (int e = d+1; e < 8 && !bad; e++)
            if (hcontains(pack4(S[a], S[c], S[d], S[e]))) bad = 1;
        if (!bad) arcs++;
    }

    printf("n=%d b=%d total=%lld arcs=%lld\n", n, b, total, arcs);
    free(htab);
    return 0;
}
