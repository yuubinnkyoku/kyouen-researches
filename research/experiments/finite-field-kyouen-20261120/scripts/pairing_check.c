// Check a candidate pairing strategy for the second player.
//
// Input:  circles.txt (as elsewhere in this directory) and a pairing file
//         produced by pairing_candidates.py (n lines: pi[i]).
// Output: how many pi-invariant safe positions there are, and whether every
//         legal first-player move p admits the reply pi(p) (i.e. whether
//         S + p + pi(p) stays safe).  A single failure refutes the pairing.
//
// Only pi-invariant S can arise when the second player answers pi(p) every
// time, so this is exactly the condition for the pairing to be a winning
// strategy.  Since all automorphisms of the Miquelian plane are Moebius maps,
// every fixed-point-free involution is conjugate to z -> c/z (c a non-square),
// and conjugating by a plane automorphism preserves the property: one test
// settles the question for the whole conjugacy class.
//
// Build: gcc -O2 -o pairing_check pairing_check.c
// Run:   ./pairing_check ../output/circles_q7_fast.txt ../output/pairing_q7.txt

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n, b;
static int *clen;
static int **cpts;
static uint64_t *cmask;
static int *adj_off, *adj;
static int *pairing;

static int *cnt;
static int *blk;
static char *inarc;
static int *allowed, *pos, nallowed;
static int *stamp, stampcur;

static long long safe_count = 0;
static long long invariant_count = 0;
static long long checked_moves = 0;
static long long failures = 0;
static int first_fail_size = -1;
static uint64_t first_fail_mask = 0;
static int first_fail_p = -1;

static inline void allow_remove(int p) {
    int i = pos[p];
    int last = allowed[--nallowed];
    allowed[i] = last;
    pos[last] = i;
}
static inline void allow_add(int p) {
    pos[p] = nallowed;
    allowed[nallowed++] = p;
}
static void add_point(int p) {
    inarc[p] = 1;
    allow_remove(p);
    for (int t = adj_off[p]; t < adj_off[p + 1]; t++) {
        int c = adj[t];
        if (++cnt[c] == 3) {
            for (int u = 0; u < clen[c]; u++) {
                int v = cpts[c][u];
                if (!inarc[v] && blk[v]++ == 0) allow_remove(v);
            }
        }
    }
}
static void remove_point(int p) {
    for (int t = adj_off[p]; t < adj_off[p + 1]; t++) {
        int c = adj[t];
        if (cnt[c] == 3) {
            for (int u = 0; u < clen[c]; u++) {
                int v = cpts[c][u];
                if (!inarc[v] && --blk[v] == 0) allow_add(v);
            }
        }
        cnt[c]--;
    }
    inarc[p] = 0;
    if (blk[p] == 0) allow_add(p);
}

// is mask (which contains p and pi(p)) safe?
static int safe_with_pair(uint64_t mask, int p, int pimg) {
    stampcur++;
    for (int t = adj_off[p]; t < adj_off[p + 1]; t++) {
        int c = adj[t];
        stamp[c] = stampcur;
        if (__builtin_popcountll(mask & cmask[c]) > 3) return 0;
    }
    for (int t = adj_off[pimg]; t < adj_off[pimg + 1]; t++) {
        int c = adj[t];
        if (stamp[c] == stampcur) continue;
        if (__builtin_popcountll(mask & cmask[c]) > 3) return 0;
    }
    return 1;
}

static void visit(int size, uint64_t mask) {
    safe_count++;
    // pi-invariance: membership of i and pi(i) must agree
    int inv = 1;
    for (int i = 0; i < n; i++) {
        int a = (mask >> i) & 1;
        int c = (mask >> pairing[i]) & 1;
        if (a != c) { inv = 0; break; }
    }
    if (!inv) return;
    invariant_count++;

    int cand[64];
    int nc = nallowed;
    memcpy(cand, allowed, (size_t)nc * sizeof(int));
    for (int j = 0; j < nc; j++) {
        int p = cand[j];
        if (inarc[p] || blk[p] > 0) continue;
        checked_moves++;
        int pimg = pairing[p];
        uint64_t aug = mask | (((uint64_t)1) << p) | (((uint64_t)1) << pimg);
        if (!safe_with_pair(aug, p, pimg)) {
            failures++;
            if (first_fail_size < 0) {
                first_fail_size = size;
                first_fail_mask = mask;
                first_fail_p = p;
            }
        }
    }
}

static void enumerate(int size, uint64_t mask, int last) {
    visit(size, mask);
    int cand[64];
    int nc = nallowed;
    memcpy(cand, allowed, (size_t)nc * sizeof(int));
    for (int j = 0; j < nc; j++) {
        int p = cand[j];
        if (p <= last) continue;
        if (inarc[p] || blk[p] > 0) continue;
        add_point(p);
        enumerate(size + 1, mask | (((uint64_t)1) << p), p);
        remove_point(p);
    }
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "usage: %s circles.txt pairing.txt\n", argv[0]);
        return 2;
    }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("circles"); return 1; }
    if (fscanf(f, "%d %d", &n, &b) != 2) { fprintf(stderr, "bad header\n"); return 1; }
    if (n > 64) { fprintf(stderr, "n=%d needs more than 64 mask bits\n", n); return 1; }
    clen = (int *)malloc((size_t)b * sizeof(int));
    cpts = (int **)malloc((size_t)b * sizeof(int *));
    cmask = (uint64_t *)calloc((size_t)b, sizeof(uint64_t));
    int *deg = (int *)calloc((size_t)n, sizeof(int));
    for (int c = 0; c < b; c++) {
        int len;
        if (fscanf(f, "%d", &len) != 1) { fprintf(stderr, "truncated\n"); return 1; }
        clen[c] = len;
        cpts[c] = (int *)malloc((size_t)len * sizeof(int));
        for (int j = 0; j < len; j++) {
            if (fscanf(f, "%d", &cpts[c][j]) != 1) { fprintf(stderr, "truncated\n"); return 1; }
            cmask[c] |= ((uint64_t)1) << cpts[c][j];
            deg[cpts[c][j]]++;
        }
    }
    fclose(f);

    FILE *g = fopen(argv[2], "r");
    if (!g) { perror("pairing"); return 1; }
    int pn;
    if (fscanf(g, "%d", &pn) != 1 || pn != n) { fprintf(stderr, "pairing size mismatch\n"); return 1; }
    pairing = (int *)malloc((size_t)n * sizeof(int));
    for (int i = 0; i < n; i++)
        if (fscanf(g, "%d", &pairing[i]) != 1) { fprintf(stderr, "pairing truncated\n"); return 1; }
    fclose(g);

    adj_off = (int *)malloc((size_t)(n + 1) * sizeof(int));
    adj_off[0] = 0;
    for (int p = 0; p < n; p++) adj_off[p + 1] = adj_off[p] + deg[p];
    adj = (int *)malloc((size_t)adj_off[n] * sizeof(int));
    int *fillv = (int *)calloc((size_t)n, sizeof(int));
    for (int c = 0; c < b; c++)
        for (int j = 0; j < clen[c]; j++) {
            int p = cpts[c][j];
            adj[adj_off[p] + fillv[p]++] = c;
        }
    free(fillv); free(deg);

    cnt = (int *)calloc((size_t)b, sizeof(int));
    blk = (int *)calloc((size_t)n, sizeof(int));
    inarc = (char *)calloc((size_t)n, sizeof(char));
    allowed = (int *)malloc((size_t)n * sizeof(int));
    pos = (int *)malloc((size_t)n * sizeof(int));
    stamp = (int *)calloc((size_t)b, sizeof(int));
    stampcur = 0;
    nallowed = n;
    for (int i = 0; i < n; i++) { allowed[i] = i; pos[i] = i; }

    enumerate(0, 0, -1);

    printf("SAFE %lld\n", safe_count);
    printf("INVARIANT %lld\n", invariant_count);
    printf("CHECKED %lld\n", checked_moves);
    printf("FAILURES %lld\n", failures);
    if (failures) {
        printf("FIRSTFAIL size=%d p=%d mask=%llu\n", first_fail_size, first_fail_p,
               (unsigned long long)first_fail_mask);
        printf("VERDICT PAIRING-FAILS\n");
    } else {
        printf("VERDICT PAIRING-WORKS\n");
    }
    return failures ? 1 : 0;
}
