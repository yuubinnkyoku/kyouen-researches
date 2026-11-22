// k=8 arc count at q=9 (and beyond), in C for speed.
//
// The inversive plane of order q: points = F_q^2 u {infinity}, circles =
// images of P^1(F_q) under PGL(2, F_{q^2}).
//
// Rather than rebuild the geometry, this program reads the incidence
// structure from a file produced by the Python side (points x circles
// bitmask), then counts 8-arcs by the profile method.
//
// Actually simpler and self-contained: read the circle list (each circle
// is a list of point indices), then enumerate 8-subsets smartly.
//
// The key speedup over Python: represent each circle as a 128-bit mask
// (two uint64), and test "does S contain a 4-circle" by iterating the
// 70 4-subsets of S and checking a hash set of 4-circles.
//
// Build:  gcc -O2 -o arc_k8 arc_k8.c
// Run:    ./arc_k8 <circles.txt>
//
// circles.txt format:
//   line 1: n b
//   next b lines: k p1 p2 ... pk   (0-based point indices)

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 256
#define MAXB 4096
#define MAXS 32

static int n, b;
static int circ_len[MAXB];
static int circ_pts[MAXB][MAXS];

// hash set of 4-circles: key = sorted 4 point indices packed
// we use a simple open-addressing table
#define HSIZE (1 << 22)
static uint64_t *htab;
static int hcount = 0;

static inline uint64_t pack4(int a, int c, int d, int e) {
    // a<c<d<e, each < 256 -> 8 bits each
    return ((uint64_t)a << 24) | ((uint64_t)c << 16) | ((uint64_t)d << 8) | (uint64_t)e;
}

static void hinsert(uint64_t key) {
    uint64_t h = (key * 0x9E3779B97F4A7C15ULL) >> 42;
    while (htab[h] != 0) {
        if (htab[h] == key + 1) return;  // already present
        h = (h + 1) & (HSIZE - 1);
    }
    htab[h] = key + 1;
    hcount++;
}

static int hcontains(uint64_t key) {
    uint64_t h = (key * 0x9E3779B97F4A7C15ULL) >> 42;
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

    // build the 4-circle hash set
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
    fprintf(stderr, "4-circles: %d\n", hcount);

    // count 8-subsets with no 4-circle
    long long arcs = 0, total = 0;
    int S[7];
    for (S[0] = 0; S[0] < n; S[0]++)
    for (S[1] = S[0]+1; S[1] < n; S[1]++)
    for (S[2] = S[1]+1; S[2] < n; S[2]++)
    for (S[3] = S[2]+1; S[3] < n; S[3]++)
    for (S[4] = S[3]+1; S[4] < n; S[4]++)
    for (S[5] = S[4]+1; S[5] < n; S[5]++)
    for (S[6] = S[5]+1; S[6] < n; S[6]++)
    for (int dummy = 0; dummy < 1; dummy++) {
        total++;
        int bad = 0;
        for (int a = 0; a < 4 && !bad; a++)
        for (int c = a+1; c < 5 && !bad; c++)
        for (int d = c+1; d < 6 && !bad; d++)
        for (int e = d+1; e < 7 && !bad; e++)
            if (hcontains(pack4(S[a], S[c], S[d], S[e]))) bad = 1;
        if (!bad) arcs++;
    }

    printf("n=%d b=%d total=%lld arcs=%lld\n", n, b, total, arcs);
    free(htab);
    return 0;
}
