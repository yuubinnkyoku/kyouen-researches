// Complete Grundy values of the inversive-plane kyouen game for q <= 7.
//
// Board: points 0..n-1, circles read from circles.txt (same input format as the
// other programmes in this directory).  A position is a point set S meeting
// every circle in at most three points; a move adds one point and must keep
// that property; a player with no move loses (normal play).  Hence
//
//     grundy(S) = mex { grundy(S + p) : p is a legal move }
//
// and the misere outcome (a player with no move wins) is computed alongside.
//
// Method
// ------
// Phase 1: depth-first enumeration of all safe positions, using the canonical
//   increasing-index order so each set is produced exactly once, bucketed by
//   size.  The incremental blocking counters keep this O(q^2) per node.
// Phase 2: process the buckets from the largest size downwards.  For each set
//   the legal moves are found from the circle bitmasks (a circle carrying three
//   of its points makes all of its points illegal), the children's values are
//   looked up in the bucket of size+1 (an open-addressing hash keyed by mask),
//   and the mex is stored in the bucket of size.  Only two buckets are alive at
//   any time.
//
// Masks are 64-bit, so this handles n <= 64, i.e. q <= 7 (n = q^2+1 = 50).
// For q = 8 (65 points) the masks would need a second word; q = 9 is out of
// reach anyway (about 8.8e7 safe positions).
//
// Build:  gcc -O2 -o grundy_full grundy_full.c
// Run:    ./grundy_full ../output/circles_q7.txt
//
// Output:
//   POINTS / CIRCLES
//   SAFE <total>            number of safe positions
//   ROOT <grundy> <misere_win_of_player_to_move>
//   SIZE <k> <count> <maximal> <grundy0>
//   GRUNDY <value> <count>
//   MISERE root outcome and per size counts

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define EMPTY 0xFFFFu

static int n, b;
static int *clen;
static int **cpts;
static uint64_t *cmask;          // circle bitmasks
static int *adj_off, *adj;

static int *cnt;
static int *blk;
static char *inarc;
static int *allowed, *pos, nallowed;

static uint64_t *bucket[64];     // safe-position masks by size
static long long first_g[64];
static int probe_g[4] = {-1, -1, -1, -1};
static long long probe_children[64];
static long long bcount[64];

/* ----------------------------- phase 1 ----------------------------- */

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
}

static void enumerate(int size, uint64_t mask, int last) {
    if (bcount[size] % 65536 == 0) {
        bucket[size] = (uint64_t *)realloc(bucket[size],
                                           (size_t)(bcount[size] + 65536) * sizeof(uint64_t));
    }
    bucket[size][bcount[size]++] = mask;
    int cand[64];
    int nc = nallowed;
    memcpy(cand, allowed, (size_t)nc * sizeof(int));
    for (int j = 0; j < nc; j++) {
        int p = cand[j];
        if (p <= last) continue;
        if (inarc[p] || blk[p] > 0) continue;
        add_point(p);
        enumerate(size + 1, mask | (1ULL << p), p);
        remove_point(p);
    }
}

/* ----------------------------- phase 2 ----------------------------- */

typedef struct {
    uint64_t *keys;
    uint16_t *vals;
    size_t cap, used;
} Map;

static void map_init(Map *m, size_t cap) {
    m->cap = cap;
    m->used = 0;
    m->keys = (uint64_t *)calloc(cap, sizeof(uint64_t));
    m->vals = (uint16_t *)malloc(cap * sizeof(uint16_t));
    memset(m->vals, 0xFF, cap * sizeof(uint16_t));
}
static void map_free(Map *m) { free(m->keys); free(m->vals); }

static inline size_t hash64(uint64_t x) {
    x ^= x >> 33; x *= 0xff51afd7ed558ccdULL;
    x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ULL;
    x ^= x >> 33;
    return (size_t)x;
}
static void map_put(Map *m, uint64_t key, uint16_t val) {
    size_t h = hash64(key) & (m->cap - 1);
    while (m->vals[h] != EMPTY && m->keys[h] != key) h = (h + 1) & (m->cap - 1);
    if (m->vals[h] == EMPTY) { m->keys[h] = key; m->used++; }
    m->vals[h] = val;
}
static uint16_t map_get(const Map *m, uint64_t key) {
    size_t h = hash64(key) & (m->cap - 1);
    while (m->vals[h] != EMPTY) {
        if (m->keys[h] == key) return m->vals[h];
        h = (h + 1) & (m->cap - 1);
    }
    return EMPTY;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s circles.txt\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
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
            cmask[c] |= 1ULL << cpts[c][j];
            deg[cpts[c][j]]++;
        }
    }
    fclose(f);

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
    nallowed = n;
    for (int i = 0; i < n; i++) { allowed[i] = i; pos[i] = i; }

    enumerate(0, 0ULL, -1);
    long long total = 0;
    int maxk = 0;
    for (int s = 0; s < 64; s++) {
        total += bcount[s];
        if (bcount[s]) maxk = s;
    }
    printf("POINTS %d\nCIRCLES %d\nSAFE %lld\n", n, b, total);

    // process sizes from maxk downwards
    uint16_t root_val = EMPTY;
    long long ghist[64] = {0};
    long long maximal[64] = {0}, g0[64] = {0};
    Map nextmap = {0}, curmap = {0};
    for (int s = maxk; s >= 0; s--) {
        size_t cap = 1;
        while (cap < (size_t)bcount[s] * 3 + 16) cap <<= 1;
        map_free(&curmap);
        map_init(&curmap, cap);
        for (long long i = 0; i < bcount[s]; i++) {
            uint64_t mask = bucket[s][i];
            // illegal points: every point of a circle that already holds three
            uint64_t illegal = 0;
            for (int c = 0; c < b; c++) {
                if (__builtin_popcountll(mask & cmask[c]) >= 3) illegal |= cmask[c];
            }
            uint64_t seen_g = 0;   // bit g set when a child has grundy g
            int nmoves = 0, misere_win = 0;
            for (int p = 0; p < n; p++) {
                if ((mask >> p) & 1ULL) continue;
                if ((illegal >> p) & 1ULL) continue;
                uint16_t v = map_get(&nextmap, mask | (1ULL << p));
                if (v == EMPTY) { fprintf(stderr, "child missing (s=%d p=%d)\n", s, p); return 1; }
                int g = v & 0xFF;
                int child_misere = (v >> 8) & 1;
                if (g < 64) seen_g |= (1ULL << g);
                nmoves++;
                if (s == 0) first_g[g]++;
                if (s == 3 && mask == 7ULL) probe_children[g]++;
                if (!child_misere) misere_win = 1;
            }
            int g = 0;
            while (g < 64 && ((seen_g >> g) & 1ULL)) g++;
            if (nmoves == 0) { maximal[s]++; misere_win = 1; }
            if (g == 0) g0[s]++;
            ghist[g]++;
            map_put(&curmap, mask, (uint16_t)(g | (misere_win << 8)));
            if (s == 0) root_val = (uint16_t)(g | (misere_win << 8));
            if (s >= 1 && s <= 3) {
                uint64_t probe = (s == 1) ? 1ULL : (s == 2) ? 3ULL : 7ULL;
                if (mask == probe) probe_g[s] = g;
            }
        }
        // swap: current becomes the child map for the next (smaller) size
        map_free(&nextmap);
        nextmap = curmap;
        curmap = (Map){0, 0, 0, 0};
    }
    map_free(&nextmap);

    printf("ROOT %d %d\n", root_val & 0xFF, (root_val >> 8) & 1);
    for (int s = 0; s <= maxk; s++)
        printf("SIZE %d %lld %lld %lld\n", s, bcount[s], maximal[s], g0[s]);
    for (int g = 0; g < 64; g++)
        if (ghist[g]) printf("GRUNDY %d %lld\n", g, ghist[g]);
    for (int g = 0; g < 64; g++)
        if (first_g[g]) printf("FIRSTMOVE %d %lld\n", g, first_g[g]);
    printf("PROBE %d %d %d\n", probe_g[1], probe_g[2], probe_g[3]);
    for (int g = 0; g < 64; g++)
        if (probe_children[g]) printf("PROBE_CHILDREN %d %lld\n", g, probe_children[g]);
    return 0;
}
