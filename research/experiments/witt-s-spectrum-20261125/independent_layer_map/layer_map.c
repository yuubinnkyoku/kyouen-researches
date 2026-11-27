/* Independent layer-map verification for the W_24 (S(5,8,24)) s=7 kyouen game.
 *
 * Written from scratch for the K1349 audit.  It uses none of the original
 * engine's data structures: safety is decided by an explicit "contains an
 * octad" bitmap built as a union of block-supersets, the Grundy values are a
 * direct mex DP over a full 2^24 byte table, and every set-level statement
 * (dodecad layers, maximal layers, extension profiles) is tabulated exactly.
 *
 * Build: gcc -O2 -o layer_map.exe layer_map.c
 * Run  : ./layer_map.exe ../../design-kyouen-witt-20261125/output/board_w24.txt [outfile]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define N 24
#define MAXB 1024
#define NMASK (1u << N)

static int n = N, nb;
static uint32_t blocks[MAXB];
static int blen[MAXB];
static int bpts[MAXB][8];

static uint8_t *gval;      /* Grundy value, 0xFF = not a safe position */
static uint8_t *unsafe_;   /* 1 = mask contains a whole block */
static uint8_t *isdd;      /* 1 = mask is a subset of a dodecad (sizes 9..12) */
static uint16_t *cnt12;    /* number of maximal 12-caps containing mask */
static uint16_t *cnt13;    /* number of maximal 13-caps containing mask */

static uint32_t *lst[16];  /* safe positions by size */
static long long lcnt[16];
static long long gsize[16][16];
static long long maximal[16];
static long long ddc[2][16][16];   /* [is-dodecad-subset][size][grundy] */

static uint32_t *max12, *max13;
static long long nmax12, nmax13;

static uint32_t dodecads[4096];
static int ndd;

static inline uint32_t next_comb(uint32_t v) {
    uint32_t c = v & (0u - v);
    uint32_t r = v + c;
    return (((r ^ v) >> 2) / c) | r;
}

static int popc(uint32_t x) { return __builtin_popcount(x); }

static int cmpu32(const void *a, const void *b) {
    uint32_t x = *(const uint32_t *)a, y = *(const uint32_t *)b;
    return (x > y) - (x < y);
}

/* -------- recursive subset walk over a small point list -------- */
static int mode;   /* 0: mark isdd, 1: bump cnt12, 2: bump cnt13 */
static void walk(uint32_t base, const int *pts, int m, int start, int left) {
    if (left == 0) {
        switch (mode) {
        case 0: isdd[base] = 1; break;
        case 1: cnt12[base]++; break;
        default: cnt13[base]++; break;
        }
        return;
    }
    for (int i = start; i <= m - left; i++)
        walk(base | (1u << pts[i]), pts, m, i + 1, left - 1);
}

static int nmoves(uint32_t m) {
    int c = 0;
    for (int p = 0; p < N; p++) {
        uint32_t bit = 1u << p;
        if (!(m & bit) && gval[m | bit] != 0xFF) c++;
    }
    return c;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s board.txt [outfile]\n", argv[0]); return 2; }
    if (argc > 2) {
        if (!freopen(argv[2], "w", stdout)) { perror("outfile"); return 2; }
    }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("board"); return 2; }
    if (fscanf(f, "%d %d", &n, &nb) != 2) { fprintf(stderr, "bad header\n"); return 2; }
    int fmt_ok = 1, size_ok = 1, distinct_ok = 1, range_ok = 1;
    for (int i = 0; i < nb; i++) {
        int k;
        if (fscanf(f, "%d", &k) != 1) { fprintf(stderr, "truncated\n"); return 2; }
        blen[i] = k;
        if (k != 8) size_ok = 0;
        uint32_t m = 0;
        for (int j = 0; j < k && j < 8; j++) {
            int p;
            if (fscanf(f, "%d", &p) != 1) { fprintf(stderr, "truncated\n"); return 2; }
            bpts[i][j] = p;
            if (p < 0 || p >= n) range_ok = 0;
            if (m & (1u << p)) distinct_ok = 0;
            m |= 1u << p;
        }
        blocks[i] = m;
    }
    fclose(f);
    if (nb != 759 || n != 24) fmt_ok = 0;
    /* distinct blocks */
    int dup = 0;
    for (int i = 0; i < nb; i++) {
        int sorted_ok = 1;
        for (int j = 1; j < blen[i]; j++) if (bpts[i][j] <= bpts[i][j - 1]) sorted_ok = 0;
        if (!sorted_ok) { /* not a format requirement, only note */ }
        for (int j = i + 1; j < nb; j++) if (blocks[i] == blocks[j]) dup = 1;
    }
    printf("BOARD n=%d blocks=%d fmt_ok=%d size_ok=%d distinct_ok=%d range_ok=%d dup_blocks=%d\n",
           n, nb, fmt_ok, size_ok, distinct_ok, range_ok, dup);

    /* ---- S(5,8,24): every 5-subset lies in exactly one block ---- */
    {
        static uint32_t fives[50000];
        long long nf = 0;
        for (int i = 0; i < nb; i++) {
            int p[8];
            for (int j = 0; j < 8; j++) p[j] = bpts[i][j];
            for (int a = 0; a < 4; a++) for (int b = a + 1; b < 5; b++)
            for (int c = b + 1; c < 6; c++) for (int d = c + 1; d < 7; d++)
            for (int e = d + 1; e < 8; e++)
                fives[nf++] = (1u << p[a]) | (1u << p[b]) | (1u << p[c]) |
                              (1u << p[d]) | (1u << p[e]);
        }
        qsort(fives, (size_t)nf, sizeof(uint32_t), cmpu32);
        long long distinct = 0, maxmult = 0, cur = 0;
        for (long long i = 0; i < nf; i++) {
            if (i == 0 || fives[i] != fives[i - 1]) { distinct++; cur = 1; }
            else cur++;
            if (cur > maxmult) maxmult = cur;
        }
        printf("FIVES incidences=%lld distinct=%lld C(24,5)=42504 max_multiplicity=%lld\n",
               nf, distinct, maxmult);
    }

    /* ---- Golay span ---- */
    {
        static uint32_t piv[32];
        memset(piv, 0, sizeof piv);
        for (int i = 0; i < nb; i++) {
            uint32_t x = blocks[i];
            while (x) {
                int hb = 31 - __builtin_clz(x);
                if (piv[hb]) x ^= piv[hb];
                else { piv[hb] = x; break; }
            }
        }
        uint32_t basis[32]; int nbas = 0;
        for (int i = 0; i < 32; i++) if (piv[i]) basis[nbas++] = piv[i];
        static uint32_t span[4096];
        int ns = 1; span[0] = 0;
        for (int i = 0; i < nbas; i++)
            for (int j = 0, cur = ns; j < cur; j++) span[ns++] = span[j] ^ basis[i];
        long long wh[25]; memset(wh, 0, sizeof wh);
        for (int i = 0; i < ns; i++) wh[popc(span[i])]++;
        int w8match = 1;
        for (int i = 0; i < ns; i++) {
            if (popc(span[i]) != 8) continue;
            int found = 0;
            for (int j = 0; j < nb; j++) if (blocks[j] == span[i]) { found = 1; break; }
            if (!found) w8match = 0;
        }
        ndd = 0;
        for (int i = 0; i < ns; i++) if (popc(span[i]) == 12) dodecads[ndd++] = span[i];
        printf("GOLAY rank=%d span=%d weights 0:%lld 4:%lld 8:%lld 12:%lld 16:%lld 20:%lld 24:%lld\n",
               nbas, ns, wh[0], wh[4], wh[8], wh[12], wh[16], wh[20], wh[24]);
        printf("GOLAY weight8_equals_blocks=%d DODECADS=%d\n", w8match, ndd);
    }

    /* ---- unsafe bitmap: all masks of size 8..14 that contain a block ---- */
    unsafe_ = (uint8_t *)calloc(NMASK, 1);
    if (!unsafe_) { fprintf(stderr, "OOM unsafe\n"); return 3; }
    {
        long long marks = 0;
        for (int i = 0; i < nb; i++) {
            uint32_t b = blocks[i];
            int comp[16], m = 0;
            for (int p = 0; p < N; p++) if (!(b & (1u << p))) comp[m++] = p;
            /* every X subset of comp with |X| <= 6 */
            for (int x = 0; x <= 6; x++) {
                mode = -1; /* unused */
                /* iterative over all x-subsets of comp[16] */
                if (x == 0) { unsafe_[b] = 1; marks++; continue; }
                int idx[6];
                for (int j = 0; j < x; j++) idx[j] = j;
                while (1) {
                    uint32_t mm = b;
                    for (int j = 0; j < x; j++) mm |= 1u << comp[idx[j]];
                    unsafe_[mm] = 1; marks++;
                    int j = x - 1;
                    while (j >= 0 && idx[j] == m - x + j) j--;
                    if (j < 0) break;
                    idx[j]++;
                    for (int t = j + 1; t < x; t++) idx[t] = idx[t - 1] + 1;
                }
            }
        }
        printf("UNSAFE_MARKS %lld\n", marks);
    }

    /* ---- safe positions by size, k = 0..14 ---- */
    for (int k = 0; k <= 14; k++) {
        long long c = 0;
        if (k == 0) c = 1;
        else {
            uint32_t v = (1u << k) - 1, lim = 1u << N;
            while (v < lim) { if (!unsafe_[v]) c++; v = next_comb(v); }
        }
        lcnt[k] = c;
        lst[k] = (uint32_t *)malloc((size_t)(c ? c : 1) * sizeof(uint32_t));
        if (!lst[k]) { fprintf(stderr, "OOM lst\n"); return 3; }
        if (k == 0) lst[0][0] = 0;
        else {
            long long w = 0;
            uint32_t v = (1u << k) - 1, lim = 1u << N;
            while (v < lim) { if (!unsafe_[v]) lst[k][w++] = v; v = next_comb(v); }
            if (w != c) { fprintf(stderr, "count/fill mismatch k=%d\n", k); return 3; }
        }
    }
    long long tot = 0;
    for (int k = 0; k <= 14; k++) tot += lcnt[k];
    printf("SAFE_TOTAL %lld\n", tot);
    for (int k = 0; k <= 14; k++) printf("SAFE %d %lld\n", k, lcnt[k]);

    /* ---- Grundy DP ---- */
    gval = (uint8_t *)malloc(NMASK);
    if (!gval) { fprintf(stderr, "OOM gval\n"); return 3; }
    memset(gval, 0xFF, NMASK);
    max12 = (uint32_t *)malloc((size_t)(lcnt[12] ? lcnt[12] : 1) * sizeof(uint32_t));
    max13 = (uint32_t *)malloc((size_t)(lcnt[13] ? lcnt[13] : 1) * sizeof(uint32_t));
    for (int k = 14; k >= 0; k--) {
        for (long long i = 0; i < lcnt[k]; i++) {
            uint32_t m = lst[k][i];
            unsigned seen = 0;
            int nm = 0;
            for (int p = 0; p < N; p++) {
                uint32_t bit = 1u << p;
                if (m & bit) continue;
                uint8_t v = gval[m | bit];
                if (v == 0xFF) continue;
                seen |= 1u << v;
                nm++;
            }
            int mex = 0;
            while (mex < 15 && (seen & (1u << mex))) mex++;
            gval[m] = (uint8_t)mex;
            gsize[k][mex]++;
            if (nm == 0) {
                maximal[k]++;
                if (k == 12) max12[nmax12++] = m;
                if (k == 13) max13[nmax13++] = m;
            }
        }
    }
    printf("MAXIMAL_TOTAL %lld\n", nmax12 + nmax13);
    printf("ROOT %d\n", gval[0]);
    for (int k = 0; k <= 14; k++) {
        printf("SIZE %d safe=%lld maximal=%lld\n", k, lcnt[k], maximal[k]);
        for (int g = 0; g < 16; g++)
            if (gsize[k][g]) printf("GSIZE %d %d %lld\n", k, g, gsize[k][g]);
    }
    printf("MAXLIST 12 %lld 13 %lld\n", nmax12, nmax13);

    /* ---- dodecad-subset flags (sizes 9..12) ---- */
    isdd = (uint8_t *)calloc(NMASK, 1);
    if (!isdd) { fprintf(stderr, "OOM isdd\n"); return 3; }
    for (int d = 0; d < ndd; d++) {
        int pts[12], np = 0;
        for (int p = 0; p < N; p++) if (dodecads[d] & (1u << p)) pts[np++] = p;
        for (int k = 9; k <= 12; k++) {
            mode = 0;
            walk(0, pts, np, 0, k);
        }
    }
    for (int k = 9; k <= 12; k++) {
        long long c1 = 0;
        for (long long i = 0; i < lcnt[k]; i++) if (isdd[lst[k][i]]) c1++;
        printf("DODECADSUBSETS %d %lld\n", k, c1);
    }

    /* ---- classify every 12-cap: maximal / dodecad / 11-subset of dodecad ---- */
    {
        long long nonmax = 0, nonmax_dd = 0, nonmax_nd = 0, nonmax_nd_with11 = 0;
        long long mx_with11 = 0;
        for (long long i = 0; i < lcnt[12]; i++) {
            uint32_t m = lst[12][i];
            int nm = nmoves(m);
            int has11 = 0;
            int pts[12], np = 0;
            for (int p = 0; p < N; p++) if (m & (1u << p)) pts[np++] = p;
            for (int a = 0; a < 12; a++) {
                uint32_t s = m & ~(1u << pts[a]);
                if (isdd[s]) { has11 = 1; break; }
            }
            if (nm == 0) { if (has11) mx_with11++; }
            else {
                nonmax++;
                if (isdd[m]) nonmax_dd++;
                else { nonmax_nd++; if (has11) nonmax_nd_with11++; }
            }
        }
        printf("SIZE12 nonmax=%lld nonmax_dodecad=%lld nonmax_nondodecad=%lld "
               "nonmax_nondodecad_with_dodecad11=%lld maximal_with_dodecad11=%lld\n",
               nonmax, nonmax_dd, nonmax_nd, nonmax_nd_with11, mx_with11);
    }

    /* ---- dodecad-subset flags and per-layer cross tab ---- */
    for (int k = 9; k <= 12; k++)
        for (long long i = 0; i < lcnt[k]; i++) {
            uint32_t m = lst[k][i];
            ddc[isdd[m] ? 1 : 0][k][gval[m]]++;
        }
    for (int k = 9; k <= 12; k++)
        for (int t = 0; t < 2; t++)
            for (int g = 0; g < 16; g++)
                if (ddc[t][k][g]) printf("CROSS k=%d type=%s G=%d count=%lld\n",
                                          k, t ? "dodecad" : "nondodecad", g, ddc[t][k][g]);

    /* ---- extension profiles: maximal caps containing each cap ---- */
    cnt12 = (uint16_t *)calloc(NMASK, sizeof(uint16_t));
    cnt13 = (uint16_t *)calloc(NMASK, sizeof(uint16_t));
    if (!cnt12 || !cnt13) { fprintf(stderr, "OOM cnt\n"); return 3; }
    for (long long i = 0; i < nmax12; i++) {
        uint32_t m = max12[i];
        int pts[12], np = 0;
        for (int p = 0; p < N; p++) if (m & (1u << p)) pts[np++] = p;
        for (int k = 9; k <= 12; k++) { mode = 1; walk(0, pts, np, 0, k); }
    }
    for (long long i = 0; i < nmax13; i++) {
        uint32_t m = max13[i];
        int pts[13], np = 0;
        for (int p = 0; p < N; p++) if (m & (1u << p)) pts[np++] = p;
        for (int k = 9; k <= 13; k++) { mode = 2; walk(0, pts, np, 0, k); }
    }
    /* histogram of profiles per layer type (full check, not a sample) */
    for (int k = 9; k <= 12; k++) {
        for (int t = 0; t < 2; t++) {
            /* collect profiles into a small dynamic list */
            typedef struct { int a, b; long long c; } Prof;
            static Prof prof[4096];
            int np = 0;
            for (long long i = 0; i < lcnt[k]; i++) {
                uint32_t m = lst[k][i];
                if ((isdd[m] ? 1 : 0) != t) continue;
                int a = cnt12[m], b = cnt13[m];
                int j;
                for (j = 0; j < np; j++) if (prof[j].a == a && prof[j].b == b) { prof[j].c++; break; }
                if (j == np) { if (np >= 4096) { fprintf(stderr, "too many profiles\n"); return 3; }
                               prof[np].a = a; prof[np].b = b; prof[np].c = 1; np++; }
            }
            for (int j = 0; j < np; j++)
                printf("PROFILE k=%d type=%s 12:%d 13:%d count=%lld\n",
                       k, t ? "dodecad" : "nondodecad", prof[j].a, prof[j].b, prof[j].c);
            printf("PROFILE_TYPES k=%d type=%s distinct=%d\n", k, t ? "dodecad" : "nondodecad", np);
        }
    }

    /* ---- explicit random samples (10 per layer type) ---- */
    {
        uint64_t rng = 0x243F6A8885A308D3ULL;
        for (int k = 9; k <= 11; k++) {
            for (int t = 0; t < 2; t++) {
                int got = 0;
                uint32_t chosen[10];
                while (got < 10) {
                    rng = rng * 6364136223846793005ULL + 1442695040888963407ULL;
                    long long i = (long long)((rng >> 17) % (uint64_t)lcnt[k]);
                    uint32_t m = lst[k][i];
                    if ((isdd[m] ? 1 : 0) != t) continue;
                    int dup = 0;
                    for (int j = 0; j < got; j++) if (chosen[j] == m) dup = 1;
                    if (dup) continue;
                    chosen[got++] = m;
                }
                for (int j = 0; j < 10; j++) {
                    uint32_t m = chosen[j];
                    printf("SAMPLE k=%d type=%s mask=%u G=%d 12:%d 13:%d points=",
                           k, t ? "dodecad" : "nondodecad", m, gval[m], cnt12[m], cnt13[m]);
                    for (int p = 0; p < N; p++) if (m & (1u << p)) printf("%d,", p);
                    printf("\n");
                }
            }
        }
        /* size 12 (maximal and non-maximal) and size 13 samples */
        {
            uint32_t chosen[10];
            int got_m = 0, got_n = 0, nt = 0;
            while ((got_m < 5 || got_n < 5) && nt < 1000000) {
                rng = rng * 6364136223846793005ULL + 1442695040888963407ULL;
                long long i = (long long)((rng >> 17) % (uint64_t)lcnt[12]);
                uint32_t m = lst[12][i];
                int dup = 0;
                for (int j = 0; j < got_m + got_n; j++) if (chosen[j] == m) dup = 1;
                if (dup) continue;
                int nm = nmoves(m);
                if (nm == 0 && got_m < 5) {
                    chosen[got_m + got_n] = m;
                    got_m++;
                    printf("SAMPLE k=12 type=maximal mask=%u G=%d 12:%d 13:%d points=",
                           m, gval[m], cnt12[m], cnt13[m]);
                    for (int p = 0; p < N; p++) if (m & (1u << p)) printf("%d,", p);
                    printf("\n");
                } else if (nm > 0 && got_n < 5) {
                    chosen[got_m + got_n] = m;
                    got_n++;
                    printf("SAMPLE k=12 type=nonmaximal mask=%u G=%d 12:%d 13:%d points=",
                           m, gval[m], cnt12[m], cnt13[m]);
                    for (int p = 0; p < N; p++) if (m & (1u << p)) printf("%d,", p);
                    printf("\n");
                }
                nt++;
            }
            int got13 = 0;
            uint32_t ch13[5];
            while (got13 < 5) {
                rng = rng * 6364136223846793005ULL + 1442695040888963407ULL;
                long long i = (long long)((rng >> 17) % (uint64_t)lcnt[13]);
                uint32_t m = lst[13][i];
                int dup = 0;
                for (int j = 0; j < got13; j++) if (ch13[j] == m) dup = 1;
                if (dup) continue;
                ch13[got13++] = m;
                printf("SAMPLE k=13 type=maximal mask=%u G=%d 12:%d 13:%d points=",
                       m, gval[m], cnt12[m], cnt13[m]);
                for (int p = 0; p < N; p++) if (m & (1u << p)) printf("%d,", p);
                printf("\n");
            }
        }
    }

    /* ---- structural: dodecads are non-maximal 12-caps with 12 moves, and the
     *      (11-subset of a dodecad, outside point) family is exactly the
     *      non-dodecad non-maximal 12-caps ---- */
    {
        long long bad = 0, moves_ok = 1;
        long long distinct_ext = 0;
        long long pairs = 0, pair_bad = 0;
        static uint8_t *seen = NULL;
        seen = (uint8_t *)calloc(NMASK, 1);
        if (!seen) { fprintf(stderr, "OOM seen\n"); return 3; }
        for (int d = 0; d < ndd; d++) {
            uint32_t D = dodecads[d];
            int nm = nmoves(D);
            if (nm != 12) moves_ok = 0;
            if (gval[D] != 1) bad++;
            int pts[12], np = 0;
            for (int p = 0; p < N; p++) if (D & (1u << p)) pts[np++] = p;
            for (int a = 0; a < 12; a++) {
                uint32_t S = D & ~(1u << pts[a]);
                for (int p = 0; p < N; p++) {
                    uint32_t bit = 1u << p;
                    if (D & bit) continue;              /* p outside the dodecad only */
                    uint32_t M = S | bit;
                    pairs++;
                    if (gval[M] == 0xFF) { pair_bad++; continue; }  /* must be safe */
                    if (nmoves(M) == 0) { pair_bad++; continue; }   /* must be non-maximal */
                    if (isdd[M]) { pair_bad++; continue; }          /* must not be a dodecad */
                    if (!seen[M]) { seen[M] = 1; distinct_ext++; }
                }
            }
        }
        printf("DODECAD_CHECK wrong_g=%lld moves_ok=%lld pairs=%lld pair_bad=%lld "
               "distinct_extensions=%lld (expect %d)\n",
               bad, moves_ok, pairs, pair_bad, distinct_ext, ndd * 12 * 12);        free(seen);
    }

    /* ---- total counts ---- */
    {
        long long s0 = 0, s1 = 0, s2 = 0;
        for (int k = 0; k <= 14; k++) { s0 += gsize[k][0]; s1 += gsize[k][1]; s2 += gsize[k][2]; }
        printf("TOTAL_G 0:%lld 1:%lld 2:%lld\n", s0, s1, s2);
    }
    return 0;
}
