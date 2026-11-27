// Independent count of blocking sets and minimal blocking sets in the board.
//
// For a safe set S (|S cap L| <= s = 4 on every line L of AG(2,5)), the
// complement B = P \ S is exactly a *blocking set*: it meets every line
// (if a line missed B it would lie entirely in S, giving |S cap L| = 5).
// Hence
//     #safe sets of size k  ==  #blocking sets of size 25-k,
// and, because S is maximal (no legal move) iff every p in B lies on a line
// meeting B only in p,
//     #maximal safe sets of size k == #minimal blocking sets of size 25-k.
// (Proof of the second equivalence: adding p is illegal iff some line through
// p already has 4 points of S, i.e. that line meets B only in p.)
//
// This enumerates *subsets of the complement*, an entirely different search
// space from the Grundy solvers (which enumerate safe sets by adding points).
//
// Build: gcc -O2 -o count_complements count_complements.c
// Run:   ./count_complements board.txt 4
//
// Output: POINTS / CIRCLES, then for m = 0..14
//   BLOCKING <m> <count>
//   MINIMAL  <m> <count>
// where m is the complement size.  A zero BLOCKING count for m <= 8 proves
// that no safe set of size >= 17 exists; MINIMAL counts for m = 9,10,11 are
// the claimed maximal counts for k = 16,15,14.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n, b, s_cap;
static uint32_t lmask[256];
static int plist[64][64], np[64];
static long long blocking[64], minimal[64];

static int is_blocking(uint32_t B) {
    for (int c = 0; c < b; c++)
        if ((lmask[c] & B) == 0) return 0;
    return 1;
}

// B is a minimal blocking set iff each of its points is the unique point of B
// on some line through it.
static int is_minimal(uint32_t B) {
    for (int p = 0; p < n; p++) {
        if (!(B & (1u << p))) continue;
        int witness = 0;
        for (int j = 0; j < np[p]; j++) {
            if (__builtin_popcount(lmask[plist[p][j]] & B) == 1) {
                witness = 1;
                break;
            }
        }
        if (!witness) return 0;
    }
    return 1;
}

static void process(uint32_t B, int m) {
    if (!is_blocking(B)) return;
    blocking[m]++;
    if (is_minimal(B)) minimal[m]++;
}

static void rec(int start, int need, uint32_t B, int m) {
    if (need == 0) { process(B, m); return; }
    for (int p = start; p <= n - need; p++)
        rec(p + 1, need - 1, B | (1u << p), m);
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s board.txt s\n", argv[0]); return 2; }
    s_cap = atoi(argv[2]);

    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open board"); return 1; }
    if (fscanf(f, "%d %d", &n, &b) != 2) { fprintf(stderr, "bad header\n"); return 1; }
    if (n > 32) { fprintf(stderr, "n too large\n"); return 1; }
    int *clen = malloc((size_t)b * sizeof(int));
    for (int c = 0; c < b; c++) {
        int len;
        if (fscanf(f, "%d", &len) != 1) { fprintf(stderr, "truncated\n"); return 1; }
        clen[c] = len;
        for (int j = 0; j < len; j++) {
            int p;
            if (fscanf(f, "%d", &p) != 1) { fprintf(stderr, "truncated\n"); return 1; }
            lmask[c] |= 1u << p;
        }
    }
    fclose(f);
    for (int c = 0; c < b; c++) {
        if (clen[c] != s_cap + 1) {
            fprintf(stderr, "line %d has %d points, expected s_cap+1 = %d\n",
                    c, clen[c], s_cap + 1);
            return 2;
        }
    }
    for (int c = 0; c < b; c++)
        for (int p = 0; p < n; p++)
            if (lmask[c] & (1u << p)) plist[p][np[p]++] = c;

    if (argc > 3) {
        fprintf(stderr, "optional max complement size argument is not used\n");
    }

    printf("POINTS %d\nCIRCLES %d\n", n, b);
    int maxm = n - 1;   // complements of size 0..14 are the relevant ones
    if (maxm > 14) maxm = 14;
    for (int m = 0; m <= maxm; m++) {
        rec(0, m, 0u, m);
        printf("BLOCKING %d %lld\n", m, blocking[m]);
        printf("MINIMAL %d %lld\n", m, minimal[m]);
    }
    return 0;
}
