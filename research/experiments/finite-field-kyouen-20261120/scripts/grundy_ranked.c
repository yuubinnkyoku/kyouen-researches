// Complete Grundy values with rank-indexed tables, so q = 9 (82 points,
// about 8.8e7 safe positions) becomes reachable.
//
// Same recursion as grundy_full.c / grundy_full128.c
//
//     grundy(S) = mex { grundy(S + p) : p legal }        (normal play)
//
// plus the misere outcome.  The difference is the child lookup:
//
//   * for a size s with C(n,s) small enough, the values of the size-s
//     positions are stored in a flat byte array indexed by the combinatorial
//     rank  rank(S) = sum_i C(p_i, i)  (p_1 < ... < p_s), which is a bijection
//     onto [0, C(n,s)),
//   * otherwise (the large sizes) a hash map from rank to value is used, which
//     is much smaller than an index of all subsets.
//
// Thus at most two tables are alive at a time, each of a few hundred MB, while
// the positions themselves are kept as 128-bit masks (8.8e7 * 16 B = 1.4 GB).
//
// Build: gcc -O2 -o grundy_ranked grundy_ranked.c
// Run:   ./grundy_ranked ../output/circles_q9.txt [probe-file]
//
// Output is the same format as grundy_full.c (SAFE / ROOT / SIZE / GRUNDY /
// FIRSTMOVE plus optional PROBE lines).

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef unsigned __int128 u128;

#define EMPTY 0xFFu
#define RANKED_LIMIT 400000000ULL   // index at most this many subsets

static int n, b;
static int *clen;
static int **cpts;
static u128 *cmask;
static int *adj_off, *adj;

static int *cnt;
static int *blk;
static char *inarc;
static int *allowed, *pos, nallowed;

static double **binom;              // binom[n+1][n+1] as doubles (exact for our range)
static u128 **level_mask;           // safe positions by size
static long long *level_count;
static long long level_cap[128];
static int maxk;

static int probe_g[4] = {-1, -1, -1, -1};
static long long probe_children[128];
static u128 *p4_masks = NULL;
static int p4_count = 0, *p4_values = NULL;

static long long first_g[128];
static long long ghist[128];
static long long maximal[128], g0[128];
static uint16_t root_val = EMPTY;

static inline int popcount128(u128 x) {
    return __builtin_popcountll((uint64_t)x) + __builtin_popcountll((uint64_t)(x >> 64));
}

static inline double binom_of(int a, int k) {
    if (k < 0 || k > a) return 0.0;
    return binom[a][k];
}

// colex rank of the set of points in mask
static inline uint64_t rank_of(u128 mask) {
    uint64_t r = 0;
    int i = 0;
    for (int p = 0; p < n; p++) {
        if ((mask >> p) & 1) {
            i++;
            r += (uint64_t)binom_of(p, i);
        }
    }
    return r;
}

/* ------------------------------ enumeration ------------------------------ */

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

static void record(int size, u128 mask) {
    if (level_count[size] == level_cap[size]) {
        level_cap[size] = level_cap[size] * 2 + 1024;
        level_mask[size] = (u128 *)realloc(level_mask[size], (size_t)level_cap[size] * sizeof(u128));
        if (!level_mask[size]) { fprintf(stderr, "out of memory at size %d\n", size); exit(1); }
    }
    level_mask[size][level_count[size]++] = mask;
}

static void enumerate(int size, u128 mask, int last) {
    record(size, mask);
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

/* ------------------------------ value tables ------------------------------ */

typedef struct {
    uint64_t *keys;
    uint8_t *vals;
    size_t cap, used;
} HMap;

static void hmap_init(HMap *m, size_t cap) {
    m->cap = cap;
    m->used = 0;
    m->keys = (uint64_t *)calloc(cap, sizeof(uint64_t));
    m->vals = (uint8_t *)malloc(cap);
    if (!m->keys || !m->vals) { fprintf(stderr, "hmap alloc failed (%zu)\n", cap); exit(1); }
    memset(m->vals, 0xFF, cap);
}
static void hmap_free(HMap *m) { free(m->keys); free(m->vals); m->keys = NULL; m->vals = NULL; }

static inline size_t hash64(uint64_t x) {
    x ^= x >> 33; x *= 0xff51afd7ed558ccdULL;
    x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ULL;
    x ^= x >> 33;
    return (size_t)x;
}
static void hmap_put(HMap *m, uint64_t key, uint8_t val) {
    size_t h = hash64(key) & (m->cap - 1);
    while (m->vals[h] != EMPTY && m->keys[h] != key) h = (h + 1) & (m->cap - 1);
    if (m->vals[h] == EMPTY) { m->keys[h] = key; m->used++; }
    m->vals[h] = val;
}
static inline uint8_t hmap_get(const HMap *m, uint64_t key) {
    size_t h = hash64(key) & (m->cap - 1);
    while (m->vals[h] != EMPTY) {
        if (m->keys[h] == key) return m->vals[h];
        h = (h + 1) & (m->cap - 1);
    }
    return EMPTY;
}

typedef struct {
    int ranked;          // 1: use idx[], 0: use map
    uint8_t *idx;        // indexed by rank
    HMap map;
} Table;

static void table_init(Table *t, int size) {
    double total = binom_of(n, size);
    if (total <= (double)RANKED_LIMIT) {
        t->ranked = 1;
        t->idx = (uint8_t *)malloc((size_t)total);
        if (!t->idx) { fprintf(stderr, "index alloc failed for level %d (%g)\n", size, total); exit(1); }
        memset(t->idx, 0xFF, (size_t)total);
        t->map.keys = NULL; t->map.vals = NULL;
    } else {
        t->ranked = 0;
        t->idx = NULL;
        size_t cap = 1;
        while (cap < (size_t)level_count[size] * 3 + 16) cap <<= 1;
        hmap_init(&t->map, cap);
    }
}
static void table_free(Table *t) {
    if (t->ranked) free(t->idx);
    else hmap_free(&t->map);
    t->idx = NULL;
}
static inline uint8_t table_get(const Table *t, uint64_t rank) {
    if (t->ranked) return t->idx[rank];
    return hmap_get(&t->map, rank);
}
static inline void table_put(Table *t, uint64_t rank, uint8_t v) {
    if (t->ranked) t->idx[rank] = v;
    else hmap_put(&t->map, rank, v);
}

/* --------------------------------- main --------------------------------- */

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s circles.txt [probe-file]\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    if (fscanf(f, "%d %d", &n, &b) != 2) { fprintf(stderr, "bad header\n"); return 1; }
    if (n > 128) { fprintf(stderr, "n=%d too large\n", n); return 1; }
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

    if (argc > 2) {
        FILE *pf = fopen(argv[2], "r");
        if (!pf) { perror("probe file"); return 1; }
        if (fscanf(pf, "%d", &p4_count) != 1) { fprintf(stderr, "bad probe file\n"); return 1; }
        p4_masks = (u128 *)malloc((size_t)p4_count * sizeof(u128));
        p4_values = (int *)malloc((size_t)p4_count * sizeof(int));
        for (int z = 0; z < p4_count; z++) {
            unsigned long long lo;
            if (fscanf(pf, "%llu", &lo) != 1) { fprintf(stderr, "probe truncated\n"); return 1; }
            p4_masks[z] = (u128)lo;
            p4_values[z] = -1;
        }
        fclose(pf);
    }

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

    binom = (double **)malloc((size_t)(n + 1) * sizeof(double *));
    for (int a = 0; a <= n; a++) {
        binom[a] = (double *)calloc((size_t)(n + 1), sizeof(double));
        binom[a][0] = 1.0;
        for (int k = 1; k <= a; k++)
            binom[a][k] = binom[a - 1][k - 1] + (k <= a - 1 ? binom[a - 1][k] : 0.0);
    }

    cnt = (int *)calloc((size_t)b, sizeof(int));
    blk = (int *)calloc((size_t)n, sizeof(int));
    inarc = (char *)calloc((size_t)n, sizeof(char));
    allowed = (int *)malloc((size_t)n * sizeof(int));
    pos = (int *)malloc((size_t)n * sizeof(int));
    nallowed = n;
    for (int i = 0; i < n; i++) { allowed[i] = i; pos[i] = i; }

    level_mask = (u128 **)calloc(128, sizeof(u128 *));
    level_count = (long long *)calloc(128, sizeof(long long));
    enumerate(0, 0, -1);

    long long total = 0;
    for (int s = 0; s < 128; s++) {
        total += level_count[s];
        if (level_count[s]) maxk = s;
    }
    printf("POINTS %d\nCIRCLES %d\nSAFE %lld\nMAXK %d\n", n, b, total, maxk);
    for (int s = 0; s <= maxk; s++)
        printf("COUNTS %d %lld\n", s, level_count[s]);
    fflush(stdout);

    Table next = {0}, cur = {0};
    for (int s = maxk; s >= 0; s--) {
        table_init(&cur, s);
        uint64_t seen_values = 0;
        for (long long i = 0; i < level_count[s]; i++) {
            u128 mask = level_mask[s][i];
            u128 illegal = 0;
            for (int c = 0; c < b; c++)
                if (popcount128(mask & cmask[c]) >= 3) illegal |= cmask[c];
            seen_values = 0;
            int nmoves = 0, misere_win = 0;
            for (int p = 0; p < n; p++) {
                if ((mask >> p) & 1) continue;
                if ((illegal >> p) & 1) continue;
                u128 child = mask | (((u128)1) << p);
                uint8_t v = table_get(&next, rank_of(child));
                if (v == EMPTY) { fprintf(stderr, "child missing s=%d p=%d\n", s, p); return 1; }
                int g = v & 0x0F;
                int child_misere = (v >> 4) & 1;
                if (g < 64) seen_values |= (1ULL << g);
                nmoves++;
                if (s == 0) first_g[g]++;
                if (s == 3 && (mask >> 0 & 1) && (mask >> 1 & 1) && (mask >> 2 & 1)
                    && popcount128(mask) == 3) probe_children[g]++;
                if (!child_misere) misere_win = 1;
            }
            int g = 0;
            while (g < 64 && ((seen_values >> g) & 1ULL)) g++;
            if (g >= 16) { fprintf(stderr, "grundy %d does not fit the 4-bit packing\n", g); return 1; }
            if (nmoves == 0) { maximal[s]++; misere_win = 1; }
            if (g == 0) g0[s]++;
            ghist[g]++;
            table_put(&cur, rank_of(mask), (uint8_t)(g | (misere_win << 4)));
            if (s == 0) root_val = (uint16_t)(g | (misere_win << 4));
            if (s >= 1 && s <= 3) {
                u128 probe = (s == 1) ? 1 : (s == 2) ? 3 : 7;
                if (mask == probe) probe_g[s] = g;
            }
            if (s == 4 && p4_masks) {
                for (int z = 0; z < p4_count; z++)
                    if (p4_masks[z] == mask) p4_values[z] = g;
            }
        }
        table_free(&next);
        next = cur;
        cur = (Table){0};
        free(level_mask[s]);           // no longer needed
        level_mask[s] = NULL;
    }
    table_free(&next);

    printf("ROOT %d %d\n", root_val & 0x0F, (root_val >> 4) & 1);
    for (int s = 0; s <= maxk; s++)
        printf("SIZE %d %lld %lld %lld\n", s, level_count[s], maximal[s], g0[s]);
    for (int g = 0; g < 128; g++)
        if (ghist[g]) printf("GRUNDY %d %lld\n", g, ghist[g]);
    for (int g = 0; g < 128; g++)
        if (first_g[g]) printf("FIRSTMOVE %d %lld\n", g, first_g[g]);
    printf("PROBE %d %d %d\n", probe_g[1], probe_g[2], probe_g[3]);
    for (int g = 0; g < 128; g++)
        if (probe_children[g]) printf("PROBE_CHILDREN %d %lld\n", g, probe_children[g]);
    for (int z = 0; z < p4_count; z++)
        printf("PROBE4 %llu %d\n", (unsigned long long)(uint64_t)p4_masks[z], p4_values[z]);
    return 0;
}
