// Randomised search for a maximum arc in a 3-(n, s, 1) inversive plane.
//
// An "arc" is a point set in which no circle carries 4 of the points.
// The programme reads the circle list written by inversive_fast.py:
//
//     line 1 : n b
//     next b : len  p1 ... plen        (0-based point indices)
//
// and runs an iterated local search:
//
//   * randomised greedy: repeatedly add a uniformly random still-playable
//     point until every remaining point is blocked,
//   * perturbation: delete r random arc points and refill greedily,
//   * keep the result only if it is at least as large as before.
//
// The state is maintained incrementally.  For a point p let
//     cnt[c]  = |arc & c|                for every circle c,
//     blk[p]  = #{ circles c : p in c, cnt[c] = 3 }
// so p is playable exactly when blk[p] = 0 and p is not in the arc.  Adding p
// only touches the (q+1)*q circles through p, and when one of them reaches
// three arc points each of its q+1 points must have blk incremented; hence a
// single add costs O(q^3) at worst and the whole search is cheap even for
// q = 60.
//
// Build:  gcc -O2 -o arc_maxsearch arc_maxsearch.c
// Run:    ./arc_maxsearch ../output/circles_q13.txt --trials 2000 --ils 200
//
// Exit status is 0 when the run completes; the best arc found is printed as
// a single line "BEST <size> <p1> <p2> ..." so callers can parse it.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXP 65536

static int n, b;
static int *clen;              // circle lengths
static int **cpts;             // circle point lists
static int *adj_off;           // CSR: circle ids per point
static int *adj;

static int *cnt;               // |arc & c|
static int *blk;               // blocked-ness of p
static char *inarc;
static int *allowed, *pos, nallowed;
static int *arc, asz;
static int *best_arc, best_sz;

static uint64_t rng_state;

static inline uint64_t rnd(void) {
    uint64_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    rng_state = x;
    return x;
}

static inline int rnd_int(int m) { return (int)(rnd() % (uint64_t)m); }

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

static void reset_state(void) {
    memset(cnt, 0, (size_t)b * sizeof(int));
    memset(blk, 0, (size_t)n * sizeof(int));
    memset(inarc, 0, (size_t)n * sizeof(char));
    nallowed = n;
    for (int i = 0; i < n; i++) { allowed[i] = i; pos[i] = i; }
    asz = 0;
}

static void add_point(int p) {
    inarc[p] = 1;
    allow_remove(p);
    arc[asz++] = p;
    for (int t = adj_off[p]; t < adj_off[p + 1]; t++) {
        int c = adj[t];
        if (++cnt[c] == 3) {
            const int *cp = cpts[c];
            int len = clen[c];
            for (int u = 0; u < len; u++) {
                int v = cp[u];
                if (!inarc[v] && blk[v]++ == 0) allow_remove(v);
            }
        }
    }
}

static void remove_point(int p) {
    for (int t = adj_off[p]; t < adj_off[p + 1]; t++) {
        int c = adj[t];
        if (cnt[c] == 3) {
            const int *cp = cpts[c];
            int len = clen[c];
            for (int u = 0; u < len; u++) {
                int v = cp[u];
                if (!inarc[v] && --blk[v] == 0) allow_add(v);
            }
        }
        cnt[c]--;
    }
    inarc[p] = 0;
    if (blk[p] == 0) allow_add(p);
    asz--;
}

// add uniformly random playable points until none is playable
//
// With --sample S > 0 the next point is the best of S random playable
// candidates, "best" meaning it completes the fewest almost-full blocks
// (blocks with cnt == 2 through it), which is the cheapest useful proxy for
// "how many points does adding it kill".  Costs a factor ~S in time.
static int sample_size = 0;

static int pressure(int p) {
    int t = 0;
    for (int k = adj_off[p]; k < adj_off[p + 1]; k++)
        if (cnt[adj[k]] == 2) t++;
    return t;
}

static void greedy_fill(void) {
    while (nallowed > 0) {
        if (sample_size <= 1) {
            add_point(allowed[rnd_int(nallowed)]);
            continue;
        }
        int best = -1, best_score = 0;
        for (int s = 0; s < sample_size; s++) {
            int cand = allowed[rnd_int(nallowed)];
            int sc = pressure(cand);
            if (best < 0 || sc < best_score) { best = cand; best_score = sc; }
        }
        add_point(best);
    }
}

static void restore(const int *pts, int k) {
    reset_state();
    for (int i = 0; i < k; i++) add_point(pts[i]);
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s circles.txt [--trials T] [--ils I] [--seed S]\n", argv[0]); return 2; }
    long trials = 200;
    long ils = 300;
    uint64_t seed = 0x243F6A8885A308D3ULL;
    for (int i = 2; i + 1 < argc; i += 2) {
        if (!strcmp(argv[i], "--trials")) trials = atol(argv[i + 1]);
        else if (!strcmp(argv[i], "--ils")) ils = atol(argv[i + 1]);
        else if (!strcmp(argv[i], "--seed")) seed = (uint64_t)strtoull(argv[i + 1], NULL, 10);
        else if (!strcmp(argv[i], "--sample")) sample_size = atoi(argv[i + 1]);
    }
    rng_state = seed ? seed : 1;

    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    if (fscanf(f, "%d %d", &n, &b) != 2) { fprintf(stderr, "bad header\n"); return 1; }
    if (n > MAXP) { fprintf(stderr, "n=%d exceeds MAXP\n", n); return 1; }

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

    cnt = (int *)malloc((size_t)b * sizeof(int));
    blk = (int *)malloc((size_t)n * sizeof(int));
    inarc = (char *)malloc((size_t)n * sizeof(char));
    allowed = (int *)malloc((size_t)n * sizeof(int));
    pos = (int *)malloc((size_t)n * sizeof(int));
    arc = (int *)malloc((size_t)n * sizeof(int));
    best_arc = (int *)malloc((size_t)n * sizeof(int));
    int *cur = (int *)malloc((size_t)n * sizeof(int));

    reset_state();
    best_sz = 0;
    long total_restarts = 0;

    for (long t = 0; t < trials; t++) {
        reset_state();
        greedy_fill();
        memcpy(cur, arc, (size_t)asz * sizeof(int));
        int cur_sz = asz;
        if (cur_sz > best_sz) {
            best_sz = cur_sz;
            memcpy(best_arc, arc, (size_t)asz * sizeof(int));
        }
        for (long it = 0; it < ils; it++) {
            // perturbation: delete r random points
            int r = 1 + rnd_int(4);
            if (r > cur_sz) r = cur_sz;
            int removed[4];
            for (int k = 0; k < r; k++) {
                int idx = rnd_int(asz);
                int p = arc[idx];
                removed[k] = p;
                remove_point(p);
                if (idx < asz) arc[idx] = arc[asz];
            }
            greedy_fill();
            if (asz >= cur_sz) {
                cur_sz = asz;
                memcpy(cur, arc, (size_t)asz * sizeof(int));
                if (asz > best_sz) {
                    best_sz = asz;
                    memcpy(best_arc, arc, (size_t)asz * sizeof(int));
                }
            } else {
                restore(cur, cur_sz);
            }
        }
        total_restarts++;
    }

    printf("n=%d b=%d trials=%ld ils=%ld\n", n, b, total_restarts, ils);
    printf("BEST %d", best_sz);
    for (int i = 0; i < best_sz; i++) printf(" %d", best_arc[i]);
    printf("\n");
    return 0;
}
