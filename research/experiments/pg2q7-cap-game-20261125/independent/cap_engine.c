/*
 * Independent cap-game solver for s=2 (no three points on a line).
 *
 * Input : board file, first line "<n> <b>", then b lines "<k> p1 ... pk".
 * Output: stats on stdout (parsed by compare_claims.py).
 *
 * Phase 1: DFS in increasing point order enumerates every safe set exactly
 *          once, bucketed by size.  During the DFS two *independent*
 *          maximality tests are evaluated for every safe set:
 *            A) incremental blocked-point mask: p is blocked iff some line
 *               through p already carries 2 chosen points; S is maximal iff
 *               every point outside S is blocked.
 *            B) from scratch: U = union of all lines carrying exactly 2
 *               points of S; S is maximal iff (S | U) covers all points.
 *          Both tests are run on every safe set, not just sampled ones.
 *
 * Phase 2: bottom-up DP by size.  Legal moves of S are exactly the points
 *          outside S and outside U (the union of its bisecants).  Children
 *          (size+1) have already been assigned Grundy values; mex is taken.
 *          Misere win flag: terminal => win (no move wins), otherwise win
 *          iff some child is a misere loss.
 *
 * Masks: unsigned __int128 (n <= 57 here; __int128 supports n <= 127).
 * Build: gcc -O2 -std=c11 -o cap_engine cap_engine.c
 * Run  : ./cap_engine <board> <tag>
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

typedef unsigned __int128 u128;

#define MAXN 128
#define MAXB 512

static int n = 0, b = 0;
static u128 full_mask = 0;
static u128 line_mask[MAXB];
static int line_len[MAXB];
static int line_pts[MAXB][16];
static int point_deg[MAXN];
static int point_lines[MAXN][MAXB];

/* Phase 1 state */
static int cnt_line[MAXB];
static int cover_pt[MAXN];      /* number of saturated lines through point */
static u128 blocked_mask = 0;

static long long size_count[MAXN];
static long long maxA_count[MAXN];
static long long maxB_count[MAXN];
static uint64_t max_chk_A[MAXN];
static uint64_t max_chk_B[MAXN];

static u128 *bucket[MAXN];
static long long bucket_len[MAXN];
static long long bucket_cap[MAXN];

static int max_size = 0;

static void die(const char *msg) {
    fprintf(stderr, "FATAL: %s\n", msg);
    exit(1);
}

static inline int pop128(u128 x) {
    return __builtin_popcountll((uint64_t)x) +
           __builtin_popcountll((uint64_t)(x >> 64));
}

static inline int ctz128(u128 x) {
    uint64_t lo = (uint64_t)x;
    if (lo) return __builtin_ctzll(lo);
    return 64 + __builtin_ctzll((uint64_t)(x >> 64));
}

static inline uint64_t sm64(uint64_t x) {
    x += 0x9E3779B97F4A7C15ULL;
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ULL;
    x = (x ^ (x >> 27)) * 0x94D049BB133111EBULL;
    return x ^ (x >> 31);
}

static void bucket_push(int sz, u128 S) {
    if (bucket_len[sz] == bucket_cap[sz]) {
        long long nc = bucket_cap[sz] ? bucket_cap[sz] * 2 : 4096;
        u128 *p = (u128 *)realloc(bucket[sz], (size_t)nc * sizeof(u128));
        if (!p) die("out of memory (bucket)");
        bucket[sz] = p;
        bucket_cap[sz] = nc;
    }
    bucket[sz][bucket_len[sz]++] = S;
}

static void dfs(int start, u128 S, int sz) {
    size_count[sz]++;
    bucket_push(sz, S);

    /* Test A: every outside point blocked by an already saturated line. */
    if (((S | blocked_mask) & full_mask) == full_mask) {
        maxA_count[sz]++;
        max_chk_A[sz] += sm64((uint64_t)S);
    }

    /* Test B: recompute the union of bisecant lines from scratch. */
    u128 U = 0;
    for (int l = 0; l < b; l++) {
        if (pop128(line_mask[l] & S) == 2) U |= line_mask[l];
    }
    if (((S | U) & full_mask) == full_mask) {
        maxB_count[sz]++;
        max_chk_B[sz] += sm64((uint64_t)S);
    }

    for (int p = start; p < n; p++) {
        u128 bit = (u128)1 << p;
        if (S & bit) continue;
        if (blocked_mask & bit) continue;
        /* add p */
        for (int j = 0; j < point_deg[p]; j++) {
            int l = point_lines[p][j];
            if (++cnt_line[l] == 2) {
                u128 lm = line_mask[l];
                while (lm) {
                    int q = ctz128(lm);
                    lm &= lm - 1;
                    if (cover_pt[q]++ == 0) blocked_mask |= (u128)1 << q;
                }
            }
        }
        dfs(p + 1, S | bit, sz + 1);
        /* remove p */
        for (int j = 0; j < point_deg[p]; j++) {
            int l = point_lines[p][j];
            if (cnt_line[l] == 2) {
                u128 lm = line_mask[l];
                while (lm) {
                    int q = ctz128(lm);
                    lm &= lm - 1;
                    if (--cover_pt[q] == 0) blocked_mask &= ~((u128)1 << q);
                }
            }
            cnt_line[l]--;
        }
    }
}

/* ---------------- hash table: 128-bit mask -> byte ---------------- */

static size_t ht_cap = 0, ht_mask = 0;
static u128 *ht_key = NULL;
static unsigned char *ht_val = NULL;
static const u128 HT_EMPTY = ~(u128)0;

static inline size_t hash128(u128 x) {
    uint64_t lo = (uint64_t)x;
    uint64_t hi = (uint64_t)(x >> 64);
    uint64_t h = lo * 0x9E3779B97F4A7C15ULL;
    h ^= hi * 0xC2B2AE3D27D4EB4FULL;
    h ^= h >> 29;
    h *= 0xBF58476D1CE4E5B9ULL;
    h ^= h >> 32;
    h *= 0x94D049BB133111EBULL;
    h ^= h >> 31;
    return (size_t)h;
}

static void ht_init(size_t cap) {
    ht_cap = cap;
    ht_mask = cap - 1;
    ht_key = (u128 *)malloc(cap * sizeof(u128));
    ht_val = (unsigned char *)malloc(cap);
    if (!ht_key || !ht_val) die("out of memory (hash table)");
    for (size_t i = 0; i < cap; i++) ht_key[i] = HT_EMPTY;
    memset(ht_val, 0, cap);
}

static void ht_put(u128 key, unsigned char val) {
    size_t i = hash128(key) & ht_mask;
    while (ht_key[i] != HT_EMPTY) {
        if (ht_key[i] == key) { ht_val[i] = val; return; }
        i = (i + 1) & ht_mask;
    }
    ht_key[i] = key;
    ht_val[i] = val;
}

static unsigned char ht_get(u128 key) {
    size_t i = hash128(key) & ht_mask;
    while (ht_key[i] != HT_EMPTY) {
        if (ht_key[i] == key) return ht_val[i];
        i = (i + 1) & ht_mask;
    }
    die("hash lookup failed");
    return 0;
}

static size_t next_pow2(size_t x) {
    size_t p = 1;
    while (p < x) p <<= 1;
    return p;
}

int main(int argc, char **argv) {
    if (argc < 2) die("usage: cap_engine <board> [tag]");
    const char *tag = (argc >= 3) ? argv[2] : "board";
    FILE *f = fopen(argv[1], "r");
    if (!f) die("cannot open board");

    if (fscanf(f, "%d %d", &n, &b) != 2) die("bad header");
    if (n < 1 || n > MAXN) die("n out of range");
    if (b < 1 || b > MAXB) die("b out of range");
    for (int l = 0; l < b; l++) {
        int k;
        if (fscanf(f, "%d", &k) != 1) die("bad line length");
        if (k < 1 || k > 16) die("line too long");
        line_len[l] = k;
        u128 m = 0;
        for (int j = 0; j < k; j++) {
            int p;
            if (fscanf(f, "%d", &p) != 1) die("bad point");
            if (p < 0 || p >= n) die("point out of range");
            if (m & ((u128)1 << p)) die("repeated point in line");
            m |= (u128)1 << p;
            line_pts[l][j] = p;
            point_lines[p][point_deg[p]++] = l;
        }
        line_mask[l] = m;
    }
    fclose(f);
    full_mask = ((u128)1 << n) - 1;

    clock_t t0 = clock();
    dfs(0, 0, 0);
    clock_t t1 = clock();

    long long total = 0;
    for (int s = 0; s < MAXN; s++) {
        total += size_count[s];
        if (size_count[s]) max_size = s;
    }

    size_t hcap = next_pow2((size_t)(total * 3 / 2 + 16));
    ht_init(hcap);

    /* Phase 2 */
    for (int sz = max_size; sz >= 0; sz--) {
        for (long long idx = 0; idx < bucket_len[sz]; idx++) {
            u128 S = bucket[sz][idx];
            u128 U = 0;
            for (int l = 0; l < b; l++) {
                if (pop128(line_mask[l] & S) == 2) U |= line_mask[l];
            }
            u128 cand = full_mask & ~S & ~U;
            unsigned seen = 0;
            int win = 0;
            u128 c = cand;
            while (c) {
                int p = ctz128(c);
                u128 bit = (u128)1 << p;
                c &= c - 1;
                unsigned char v = ht_get(S | bit);
                seen |= 1u << (unsigned)(v & 0x0F);
                if (!(v & 0x80)) win = 1;
            }
            int g = 0;
            while (seen & (1u << g)) g++;
            if (cand == 0) { g = 0; win = 1; }  /* terminal: misere win */
            if (g >= 16) die("grundy value too large for encoding");
            ht_put(S, (unsigned char)(g | (win ? 0x80 : 0)));
        }
    }
    clock_t t2 = clock();

    /* Stats */
    long long gdist[16];
    memset(gdist, 0, sizeof(gdist));
    long long win_total = 0, loss_total = 0;
    long long parity_mismatch = 0;
    uint64_t chk[MAXN];
    memset(chk, 0, sizeof(chk));
    for (int s = 0; s <= max_size; s++) {
        for (long long idx = 0; idx < bucket_len[s]; idx++) {
            chk[s] += sm64((uint64_t)bucket[s][idx]);
        }
    }

    long long maxa_total = 0, maxb_total = 0;
    int maxa_eq_maxb = 1, has_odd_max = 0, has_even_max = 0;
    for (int s = 0; s <= max_size; s++) {
        maxa_total += maxA_count[s];
        maxb_total += maxB_count[s];
        if (maxA_count[s] != maxB_count[s]) maxa_eq_maxb = 0;
        if ((s & 1) && maxA_count[s]) has_odd_max = 1;
        if (!(s & 1) && maxA_count[s]) has_even_max = 1;
    }

    printf("BOARD %s\n", tag);
    printf("N %d\n", n);
    printf("B %d\n", b);
    printf("SAFE %lld\n", total);
    printf("MAXSIZE %d\n", max_size);
    printf("TOTAL_MAXA %lld\n", maxa_total);
    printf("TOTAL_MAXB %lld\n", maxb_total);
    printf("MAXA_EQ_MAXB %d\n", maxa_eq_maxb);
    for (int s = 0; s <= max_size; s++) {
        printf("CHK %d %llu\n", s, (unsigned long long)chk[s]);
        if (max_chk_A[s] || max_chk_B[s]) {
            printf("MCHK_A %d %llu\n", s, (unsigned long long)max_chk_A[s]);
            printf("MCHK_B %d %llu\n", s, (unsigned long long)max_chk_B[s]);
        }
    }
    for (int s = 0; s <= max_size; s++) {
        long long gd[16];
        memset(gd, 0, sizeof(gd));
        long long w = 0, ls = 0;
        for (long long idx = 0; idx < bucket_len[s]; idx++) {
            unsigned char v = ht_get(bucket[s][idx]);
            int g = v & 0x0F;
            gd[g]++;
            gdist[g]++;
            if (v & 0x80) w++; else ls++;
            if ((v & 0x0F) != (unsigned)(s & 1)) parity_mismatch++;
        }
        win_total += w;
        loss_total += ls;
        printf("SIZE %d %lld %lld %lld", s, bucket_len[s], maxA_count[s], maxB_count[s]);
        for (int g = 0; g < 16; g++) if (gd[g]) printf(" G%d %lld", g, gd[g]);
        printf(" WIN %lld LOSS %lld\n", w, ls);
    }
    for (int g = 0; g < 16; g++) if (gdist[g]) printf("GRUNDY %d %lld\n", g, gdist[g]);
    unsigned char root = ht_get(0);
    printf("ROOT_G %d\n", root & 0x0F);
    printf("ROOT_WIN %d\n", (root & 0x80) ? 1 : 0);
    printf("WIN_TOTAL %lld\n", win_total);
    printf("LOSS_TOTAL %lld\n", loss_total);
    printf("PARITY_MISMATCH %lld\n", parity_mismatch);
    printf("MAXA_TOTAL %lld\n", maxa_total);
    printf("MAXB_TOTAL %lld\n", maxb_total);
    printf("HAS_ODD_MAXIMAL %d\n", has_odd_max);
    printf("HAS_EVEN_MAXIMAL %d\n", has_even_max);
    /* Deterministic samples for independent per-position re-evaluation. */
    for (int s = 4; s <= max_size; s++) {
        long long L = bucket_len[s];
        for (int t = 0; t < 6 && t < L; t++) {
            long long idx;
            if (t == 0) idx = 0;
            else if (t == 1) idx = L / 2;
            else if (t == 2) idx = L - 1;
            else {
                uint64_t z = (uint64_t)t * 0x9E3779B97F4A7C15ULL + (uint64_t)s;
                idx = (long long)(sm64(z) % (uint64_t)L);
            }
            u128 S = bucket[s][idx];
            unsigned char v = ht_get(S);
            printf("SAMPLE %d %llu %d %d\n", s,
                   (unsigned long long)(uint64_t)S, (int)(v & 0x0F),
                   (v & 0x80) ? 1 : 0);
        }
    }
    printf("SAMPLE 0 0 %d %d\n", root & 0x0F, (root & 0x80) ? 1 : 0);
    printf("SECONDS_ENUM %.3f\n", (double)(t1 - t0) / CLOCKS_PER_SEC);
    printf("SECONDS_DP %.3f\n", (double)(t2 - t1) / CLOCKS_PER_SEC);
    fflush(stdout);
    return 0;
}
