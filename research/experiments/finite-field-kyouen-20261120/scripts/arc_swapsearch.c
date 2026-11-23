// Fixed-size swap search for large arcs, to push the lower bounds in K1251.
//
// The greedy "add points until stuck" search (arc_maxsearch.c) explores one
// kind of basin.  This programme uses a different one: keep the set size fixed
// at a target k and allow violations, then minimise
//
//     penalty(S) = sum over circles c of max(0, |S cap c| - 3)
//
// by swapping one point out and one point in.  A move is chosen by picking a
// random violated circle, a random point of the set inside it, and then the
// best partner among a random sample of points outside the set (tabu on points
// that were just removed).  Penalty zero means the set is an arc.
//
// Because a swap only changes the counts of circles through the two points,
// the delta is computed in O(#circles through p + #circles through q) = O(q^2).
//
// Input format is the same as arc_maxsearch.c (circles.txt).
//
// Build:  gcc -O2 -o arc_swapsearch arc_swapsearch.c
// Run:    ./arc_swapsearch ../output/circles_q13.txt --k 11 --iters 300000 --sample 24
//
// Prints "FOUND <k> <points>" when a feasible set of size k is reached and
// "FAILED <k> <best penalty>" otherwise, followed by a machine readable line
// "RESULT <k> <status> <best_penalty>".

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n, b;
static int *clen;
static int **cpts;
static int *adj_off, *adj;

static int *cnt;        // |S cap c|
static char *inS;
static int *violist, *vpos, nviol;
static int *stamp, stampcur;   // for marking circles through p
static uint64_t rng_state;

static inline uint64_t rnd(void) {
    uint64_t x = rng_state;
    x ^= x << 13; x ^= x >> 7; x ^= x << 17;
    return rng_state = x;
}
static inline int rnd_int(int m) { return (int)(rnd() % (uint64_t)m); }

static inline int pen_of(int c) { return cnt[c] > 3 ? cnt[c] - 3 : 0; }

static void viol_add(int c) {
    vpos[c] = nviol;
    violist[nviol++] = c;
}
static void viol_remove(int c) {
    int i = vpos[c];
    int last = violist[--nviol];
    violist[i] = last;
    vpos[last] = i;
}

// change cnt[c] by d and keep the violated list in sync
static inline void touch(int c, int d) {
    int before = cnt[c];
    cnt[c] = before + d;
    int was = before > 3, is = cnt[c] > 3;
    if (!was && is) viol_add(c);
    else if (was && !is) viol_remove(c);
}

static long penalty(void) {
    long s = 0;
    for (int c = 0; c < b; c++) s += pen_of(c);
    return s;
}

// penalty delta of removing p and adding q
//
// Circles through both p and q keep their count, so they must be excluded from
// both one-sided sums.  Because adj_off is a CSR layout we cannot detect
// "contains p as well" by a single mark: mark q-circles with stampA, then mark
// the p-circles that are also q-circles (the shared ones) with stampB.
static long swap_delta(int p, int q) {
    long d = 0;
    int stampA = ++stampcur;
    int stampB = ++stampcur;
    for (int t = adj_off[q]; t < adj_off[q + 1]; t++) stamp[adj[t]] = stampA;
    for (int t = adj_off[p]; t < adj_off[p + 1]; t++) {
        int c = adj[t];
        if (stamp[c] == stampA) { stamp[c] = stampB; continue; }  // shared
        int before = cnt[c];
        int after = before - 1;
        d += (after > 3 ? after - 3 : 0) - (before > 3 ? before - 3 : 0);
    }
    for (int t = adj_off[q]; t < adj_off[q + 1]; t++) {
        int c = adj[t];
        if (stamp[c] != stampA) continue;      // shared circles carry stampB
        int before = cnt[c];
        int after = before + 1;
        d += (after > 3 ? after - 3 : 0) - (before > 3 ? before - 3 : 0);
    }
    return d;
}

static void apply_swap(int p, int q) {
    for (int t = adj_off[p]; t < adj_off[p + 1]; t++) touch(adj[t], -1);
    inS[p] = 0;
    for (int t = adj_off[q]; t < adj_off[q + 1]; t++) touch(adj[t], +1);
    inS[q] = 1;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s circles.txt --k K [--iters N] [--sample S] [--seed X]\n", argv[0]);
        return 2;
    }
    int k = 0;
    long iters = 200000;
    int sample = 24;
    uint64_t seed = 0x9E3779B97F4A7C15ULL;
    for (int i = 2; i + 1 < argc; i += 2) {
        if (!strcmp(argv[i], "--k")) k = atoi(argv[i + 1]);
        else if (!strcmp(argv[i], "--iters")) iters = atol(argv[i + 1]);
        else if (!strcmp(argv[i], "--sample")) sample = atoi(argv[i + 1]);
        else if (!strcmp(argv[i], "--seed")) seed = (uint64_t)strtoull(argv[i + 1], NULL, 10);
    }
    rng_state = seed ? seed : 1;

    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    if (fscanf(f, "%d %d", &n, &b) != 2) { fprintf(stderr, "bad header\n"); return 1; }
    clen = (int *)malloc((size_t)b * sizeof(int));
    cpts = (int **)malloc((size_t)b * sizeof(int *));
    int *deg = (int *)calloc((size_t)n, sizeof(int));
    for (int c = 0; c < b; c++) {
        int len;
        if (fscanf(f, "%d", &len) != 1) { fprintf(stderr, "truncated\n"); return 1; }
        clen[c] = len;
        cpts[c] = (int *)malloc((size_t)len * sizeof(int));
        for (int j = 0; j < len; j++) {
            if (fscanf(f, "%d", &cpts[c][j]) != 1) { fprintf(stderr, "truncated\n"); return 1; }
            deg[cpts[c][j]]++;
        }
    }
    fclose(f);

    adj_off = (int *)malloc((size_t)(n + 1) * sizeof(int));
    adj_off[0] = 0;
    for (int p = 0; p < n; p++) adj_off[p + 1] = adj_off[p] + deg[p];
    adj = (int *)malloc((size_t)adj_off[n] * sizeof(int));
    int *fill = (int *)calloc((size_t)n, sizeof(int));
    for (int c = 0; c < b; c++)
        for (int j = 0; j < clen[c]; j++) {
            int p = cpts[c][j];
            adj[adj_off[p] + fill[p]++] = c;
        }
    free(fill); free(deg);

    cnt = (int *)calloc((size_t)b, sizeof(int));
    inS = (char *)calloc((size_t)n, sizeof(char));
    violist = (int *)malloc((size_t)b * sizeof(int));
    vpos = (int *)malloc((size_t)b * sizeof(int));
    stamp = (int *)calloc((size_t)b, sizeof(int));
    stampcur = 0;
    nviol = 0;

    if (k <= 3 || k > n) { fprintf(stderr, "bad k=%d\n", k); return 2; }

    // initialisation: random order, take every point that keeps the penalty 0
    // (i.e. keeps every circle at <= 3 chosen points); if that stalls before k
    // points, fill the rest at random so the set has exactly size k.
    int *S = (int *)malloc((size_t)k * sizeof(int));
    int *posS = (int *)malloc((size_t)n * sizeof(int));
    int *perm = (int *)malloc((size_t)n * sizeof(int));
    for (int i = 0; i < n; i++) { perm[i] = i; posS[i] = -1; }
    for (int i = n - 1; i > 0; i--) {
        int j = rnd_int(i + 1);
        int t = perm[i]; perm[i] = perm[j]; perm[j] = t;
    }
    int sz = 0;
    for (int i = 0; i < n && sz < k; i++) {
        int p = perm[i];
        int ok = 1;
        for (int t = adj_off[p]; t < adj_off[p + 1] && ok; t++)
            if (cnt[adj[t]] >= 3) ok = 0;
        if (!ok) continue;
        inS[p] = 1; posS[p] = sz; S[sz++] = p;
        for (int t = adj_off[p]; t < adj_off[p + 1]; t++) touch(adj[t], +1);
    }
    for (int i = 0; i < n && sz < k; i++) {
        int p = perm[i];
        if (inS[p]) continue;
        inS[p] = 1; posS[p] = sz; S[sz++] = p;
        for (int t = adj_off[p]; t < adj_off[p + 1]; t++) touch(adj[t], +1);
    }
    free(perm);

    long best_pen = penalty();
    long cur_pen = best_pen;
    int *tabu = (int *)calloc((size_t)n, sizeof(int));
    long *tabu_until = (long *)calloc((size_t)n, sizeof(long));

    for (long it = 1; it <= iters && cur_pen > 0; it++) {
        int c = violist[rnd_int(nviol)];
        // pick a random point of S inside c
        int p = -1, seen = 0;
        for (int j = 0; j < clen[c]; j++) {
            int u = cpts[c][j];
            if (inS[u]) { seen++; if (rnd_int(seen) == 0) p = u; }
        }
        if (p < 0) continue;
        int best_q = -1;
        long best_d = 0;
        for (int s = 0; s < sample; s++) {
            int q = rnd_int(n);
            if (inS[q]) continue;
            if (tabu[q] && tabu_until[q] > it) continue;
            long d = swap_delta(p, q);
            if (best_q < 0 || d < best_d) { best_d = d; best_q = q; }
        }
        if (best_q < 0) continue;
        // remove p from S, insert best_q
        apply_swap(p, best_q);
        S[posS[p]] = best_q;
        posS[best_q] = posS[p];
        posS[p] = -1;
        tabu[p] = 1;
        tabu_until[p] = it + 8 + rnd_int(8);
        cur_pen += best_d;
        if (cur_pen < best_pen) best_pen = cur_pen;
    }

    int feasible = (penalty() == 0);
    if (feasible) {
        printf("FOUND %d", k);
        for (int i = 0; i < k; i++) printf(" %d", S[i]);
        printf("\n");
        printf("RESULT %d OK 0\n", k);
    } else {
        printf("RESULT %d FAILED %ld\n", k, best_pen);
    }
    return feasible ? 0 : 3;
}
