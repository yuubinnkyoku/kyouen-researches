// Same as grundy_full.c but with 128-bit masks, so q = 8 (65 points) is reachable.
//
// Only the mask type and the hashing change; the algorithm, the incremental
// enumeration and the output format are identical.  grundy_full.c is the
// validated version (it reproduces K1058's q=3 and q=5 values exactly); this
// one is checked against it on q=5 and q=7 before being used for q=8.
//
// Build: gcc -O2 -o grundy_full128 grundy_full128.c   (GCC __int128 needed)
// Run:   ./grundy_full128 ../output/circles_q8.txt

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef unsigned __int128 u128;

#define EMPTY 0xFFFFu

static int n, b;
static int *clen;
static int **cpts;
static u128 *cmask;
static int *adj_off, *adj;

static int *cnt;
static int *blk;
static char *inarc;
static int *allowed, *pos, nallowed;

static u128 *bucket[128];
static long long bcount[128];
static long long first_g[128];
static int probe_g[4] = {-1, -1, -1, -1};
static long long probe_children[128];

static inline int popcount128(u128 x) {
    return __builtin_popcountll((uint64_t)x) + __builtin_popcountll((uint64_t)(x >> 64));
}

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

static void enumerate(int size, u128 mask, int last) {
    if (bcount[size] % 65536 == 0) {
        bucket[size] = (u128 *)realloc(bucket[size],
                                       (size_t)(bcount[size] + 65536) * sizeof(u128));
        if (!bucket[size]) { fprintf(stderr, "out of memory at size %d\n", size); exit(1); }
    }
    bucket[size][bcount[size]++] = mask;
    int cand[128];
    int nc = nallowed;
    memcpy(cand, allowed, (size_t)nc * sizeof(int));
    for (int j = 0; j < nc; j++) {
        int p = cand[j];
        if (p <= last) continue;
        if (inarc[p] || blk[p] > 0) continue;
        add_point(p);
        enumerate(size + 1, mask | (((u128)1) << p), p);
        remove_point(p);
    }
}

typedef struct {
    u128 *keys;
    uint16_t *vals;
    size_t cap, used;
} Map;

static void map_init(Map *m, size_t cap) {
    m->cap = cap;
    m->used = 0;
    m->keys = (u128 *)calloc(cap, sizeof(u128));
    m->vals = (uint16_t *)malloc(cap * sizeof(uint16_t));
    if (!m->keys || !m->vals) { fprintf(stderr, "map alloc failed (%zu)\n", cap); exit(1); }
    memset(m->vals, 0xFF, cap * sizeof(uint16_t));
}
static void map_free(Map *m) { free(m->keys); free(m->vals); m->keys = NULL; m->vals = NULL; }

static inline size_t hash128(u128 x) {
    uint64_t lo = (uint64_t)x;
    uint64_t hi = (uint64_t)(x >> 64);
    uint64_t h = lo * 0x9E3779B97F4A7C15ULL ^ (hi + 0x165667B19E3779F9ULL);
    h ^= h >> 33; h *= 0xff51afd7ed558ccdULL;
    h ^= h >> 29; h *= 0xc4ceb9fe1a85ec53ULL;
    h ^= h >> 32;
    return (size_t)h;
}
static void map_put(Map *m, u128 key, uint16_t val) {
    size_t h = hash128(key) & (m->cap - 1);
    while (m->vals[h] != EMPTY && m->keys[h] != key) h = (h + 1) & (m->cap - 1);
    if (m->vals[h] == EMPTY) { m->keys[h] = key; m->used++; }
    m->vals[h] = val;
}
static uint16_t map_get(const Map *m, u128 key) {
    size_t h = hash128(key) & (m->cap - 1);
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
    if (n > 128) { fprintf(stderr, "n=%d needs more than 128 mask bits\n", n); return 1; }
    clen = (int *)malloc((size_t)b * sizeof(int));
    cpts = (int **)malloc((size_t)b * sizeof(int *));
    cmask = (u128 *)calloc((size_t)b, sizeof(u128));
    int *deg = (int *)calloc((size_t)n, sizeof(int));
    for (int c = 0; c < b; c++) {
        int len;
        if (fscanf(f, "%d", &len) != 1) { fprintf(stderr, "truncated\n"); return 1; }
        clen[c] = len;
        cpts[c] = (int *)malloc((size_t)len * sizeof(int));
        for (int j = 0; j < len; j++) {
            if (fscanf(f, "%d", &cpts[c][j]) != 1) { fprintf(stderr, "truncated\n"); return 1; }
            cmask[c] |= ((u128)1) << cpts[c][j];
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

    enumerate(0, 0, -1);
    long long total = 0;
    int maxk = 0;
    for (int s = 0; s < 128; s++) {
        total += bcount[s];
        if (bcount[s]) maxk = s;
    }
    printf("POINTS %d\nCIRCLES %d\nSAFE %lld\n", n, b, total);
    fflush(stdout);

    uint16_t root_val = EMPTY;
    long long ghist[128] = {0};
    long long maximal[128] = {0}, g0[128] = {0};
    Map nextmap = {NULL, NULL, 0, 0}, curmap = {NULL, NULL, 0, 0};
    for (int s = maxk; s >= 0; s--) {
        size_t cap = 1;
        while (cap < (size_t)bcount[s] * 2 + 16) cap <<= 1;
        map_free(&curmap);
        map_init(&curmap, cap);
        for (long long i = 0; i < bcount[s]; i++) {
            u128 mask = bucket[s][i];
            u128 illegal = 0;
            for (int c = 0; c < b; c++)
                if (popcount128(mask & cmask[c]) >= 3) illegal |= cmask[c];
            uint64_t seen_g = 0;
            int nmoves = 0, misere_win = 0;
            for (int p = 0; p < n; p++) {
                if ((mask >> p) & 1) continue;
                if ((illegal >> p) & 1) continue;
                uint16_t v = map_get(&nextmap, mask | (((u128)1) << p));
                if (v == EMPTY) { fprintf(stderr, "child missing (s=%d p=%d)\n", s, p); return 1; }
                int g = v & 0xFF;
                int child_misere = (v >> 8) & 1;
                if (g < 64) seen_g |= (1ULL << g);
                nmoves++;
                if (s == 0) first_g[g]++;
                if (s == 3 && mask == 7) probe_children[g]++;
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
                u128 probe = (s == 1) ? 1 : (s == 2) ? 3 : 7;
                if (mask == probe) probe_g[s] = g;
            }
        }
        map_free(&nextmap);
        nextmap = curmap;
        curmap = (Map){NULL, NULL, 0, 0};
    }
    map_free(&nextmap);

    printf("ROOT %d %d\n", root_val & 0xFF, (root_val >> 8) & 1);
    for (int s = 0; s <= maxk; s++)
        printf("SIZE %d %lld %lld %lld\n", s, bcount[s], maximal[s], g0[s]);
    for (int g = 0; g < 128; g++)
        if (ghist[g]) printf("GRUNDY %d %lld\n", g, ghist[g]);
    for (int g = 0; g < 128; g++)
        if (first_g[g]) printf("FIRSTMOVE %d %lld\n", g, first_g[g]);
    printf("PROBE %d %d %d\n", probe_g[1], probe_g[2], probe_g[3]);
    for (int g = 0; g < 128; g++)
        if (probe_children[g]) printf("PROBE_CHILDREN %d %lld\n", g, probe_children[g]);
    return 0;
}
