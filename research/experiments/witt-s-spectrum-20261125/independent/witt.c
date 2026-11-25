/* Independent verification engine for the W_24 (Witt S(5,8,24)) s-game.
 *
 * Written from scratch for this verification; deliberately different from the
 * original experiment's engine:
 *   - safe positions are enumerated in increasing point order, so the DFS tree
 *     has exactly one node per safe set (no memoisation / dedup needed);
 *   - the incremental state is cnt[B] = |S cap B| and bad[p] = number of
 *     saturated octads through p;
 *   - Grundy / misere tables are plain byte arrays indexed by the 24-bit mask.
 *
 * Modes:
 *   witt full <s>            enumerate + full Grundy/misere DP, print report
 *   witt full <s> dump       same, also write out/grundy_s<s>.bin and
 *                            out/misere_s<s>.bin (value + 1, 0 = unsafe)
 *   witt brute <s> <k>       enumerate all k-subsets, count safe/maximal sets
 *   witt dodecads            generate dodecads from octad pairs, verify them
 *   witt code                build Golay code from octads, verify weights
 *
 * Board path is fixed relative to the working directory (independent/).
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define N 24
#define M 759
#define TABSZ (1u << 24)

static uint32_t oct[M];
static int oct_pts[M][8];
static int thru[N][320];
static int thru_n[N];

static int s_param;
static int cnt[M];
static int bad[N];
static uint32_t S;

static uint32_t *masks[25];
static long cap[25], len[25];
static long maxcnt[25];

static uint8_t *gtab;

static long binom(int n, int k) {
    if (k < 0 || k > n) return 0;
    long r = 1;
    for (int i = 0; i < k; i++) r = r * (n - i) / (i + 1);
    return r;
}

static void load_board(const char *path) {
    FILE *f = fopen(path, "r");
    if (!f) { perror(path); exit(1); }
    int n, b;
    if (fscanf(f, "%d %d", &n, &b) != 2 || n != N || b != M) {
        fprintf(stderr, "bad header\n"); exit(1);
    }
    for (int i = 0; i < M; i++) {
        int k;
        if (fscanf(f, "%d", &k) != 1 || k != 8) { fprintf(stderr, "bad line\n"); exit(1); }
        uint32_t m = 0;
        for (int j = 0; j < 8; j++) {
            int p;
            if (fscanf(f, "%d", &p) != 1 || p < 0 || p >= N) { fprintf(stderr, "bad point\n"); exit(1); }
            if (m & (1u << p)) { fprintf(stderr, "duplicate point\n"); exit(1); }
            m |= 1u << p;
            oct_pts[i][j] = p;
        }
        oct[i] = m;
    }
    fclose(f);
    for (int p = 0; p < N; p++) thru_n[p] = 0;
    for (int i = 0; i < M; i++)
        for (int j = 0; j < 8; j++)
            thru[oct_pts[i][j]][thru_n[oct_pts[i][j]]++] = i;
    for (int p = 0; p < N; p++)
        if (thru_n[p] != 253) { fprintf(stderr, "thru[%d]=%d\n", p, thru_n[p]); exit(1); }
}

static void alloc_masks(void) {
    for (int k = 0; k <= N; k++) {
        cap[k] = binom(N, k);
        masks[k] = (uint32_t *)malloc(sizeof(uint32_t) * (size_t)cap[k]);
        if (!masks[k]) { fprintf(stderr, "oom\n"); exit(1); }
        len[k] = 0;
        maxcnt[k] = 0;
    }
    gtab = (uint8_t *)malloc(TABSZ);
    if (!gtab) { fprintf(stderr, "oom gtab\n"); exit(1); }
}

static void dfs(int last) {
    int sz = __builtin_popcount(S);
    if (len[sz] >= cap[sz]) { fprintf(stderr, "overflow size %d\n", sz); exit(1); }
    masks[sz][len[sz]++] = S;
    int maximal = 1;
    for (int p = 0; p < N; p++)
        if (!((S >> p) & 1) && bad[p] == 0) { maximal = 0; break; }
    if (maximal) maxcnt[sz]++;
    for (int p = last + 1; p < N; p++) {
        if (bad[p]) continue;
        S |= 1u << p;
        int changed[320];
        int nch = 0;
        int tn = thru_n[p];
        const int *tp = thru[p];
        for (int i = 0; i < tn; i++) {
            int b = tp[i];
            if (++cnt[b] == s_param) {
                changed[nch++] = b;
                const int *pp = oct_pts[b];
                bad[pp[0]]++; bad[pp[1]]++; bad[pp[2]]++; bad[pp[3]]++;
                bad[pp[4]]++; bad[pp[5]]++; bad[pp[6]]++; bad[pp[7]]++;
            }
        }
        dfs(p);
        S ^= 1u << p;
        for (int i = 0; i < nch; i++) {
            const int *pp = oct_pts[changed[i]];
            bad[pp[0]]--; bad[pp[1]]--; bad[pp[2]]--; bad[pp[3]]--;
            bad[pp[4]]--; bad[pp[5]]--; bad[pp[6]]--; bad[pp[7]]--;
        }
        for (int i = 0; i < tn; i++) cnt[tp[i]]--;
    }
}

static int max_size;

static void dp_grundy(long gdist[25][25]) {
    memset(gtab, 0, TABSZ);
    for (int k = 0; k <= max_size; k++)
        for (long i = 0; i < len[k]; i++) gtab[masks[k][i]] = 1;
    for (int k = max_size; k >= 0; k--) {
        for (long i = 0; i < len[k]; i++) {
            uint32_t m = masks[k][i];
            uint32_t seen = 0;
            for (int p = 0; p < N; p++) {
                if (m & (1u << p)) continue;
                uint8_t v = gtab[m | (1u << p)];
                if (v) seen |= 1u << (v - 1);
            }
            int g = __builtin_ctz(~seen);
            gtab[m] = (uint8_t)(g + 1);
            gdist[k][g]++;
        }
    }
}

static void dp_misere(long mdist[25][2]) {
    memset(gtab, 0, TABSZ);
    for (int k = 0; k <= max_size; k++)
        for (long i = 0; i < len[k]; i++) gtab[masks[k][i]] = 1;
    for (int k = max_size; k >= 0; k--) {
        for (long i = 0; i < len[k]; i++) {
            uint32_t m = masks[k][i];
            int has_child = 0, has0 = 0;
            for (int p = 0; p < N; p++) {
                if (m & (1u << p)) continue;
                uint8_t v = gtab[m | (1u << p)];
                if (v) { has_child = 1; if (v == 1) has0 = 1; }
            }
            int val = (!has_child) ? 1 : (has0 ? 1 : 0);
            gtab[m] = (uint8_t)(val + 1);
            mdist[k][val]++;
        }
    }
}

static void report(int dump) {
    static long gdist[25][25];
    static long mdist[25][2];
    memset(gdist, 0, sizeof(gdist));
    memset(mdist, 0, sizeof(mdist));
    long total = 0, maxtotal = 0;
    for (int k = 0; k <= N; k++) {
        if (len[k]) { total += len[k]; max_size = k; }
        maxtotal += maxcnt[k];
        if (len[k] || maxcnt[k])
            printf("SIZE %d %ld %ld\n", k, len[k], maxcnt[k]);
    }
    printf("SAFE %ld\n", total);
    printf("MAXIMAL %ld\n", maxtotal);
    dp_grundy(gdist);
    long gtot[25] = {0};
    long gtotal = 0;
    for (int k = 0; k <= max_size; k++)
        for (int g = 0; g <= 24; g++) {
            if (!gdist[k][g]) continue;
            gtot[g] += gdist[k][g];
            gtotal += gdist[k][g];
        }
    for (int g = 0; g <= 24; g++)
        if (gtot[g]) printf("GRUNDY %d %ld\n", g, gtot[g]);
    printf("GRUNDY_TOTAL %ld\n", gtotal);
    int root_g = gtab[0] - 1;
    if (dump) {
        char fn[128];
        snprintf(fn, sizeof fn, "out/grundy_s%d.bin", s_param);
        FILE *f = fopen(fn, "wb");
        if (!f) { perror(fn); exit(1); }
        fwrite(gtab, 1, TABSZ, f);
        fclose(f);
    }
    dp_misere(mdist);
    long mtot[2] = {0, 0};
    for (int k = 0; k <= max_size; k++)
        for (int v = 0; v < 2; v++) mtot[v] += mdist[k][v];
    printf("MISERE 0 %ld\n", mtot[0]);
    printf("MISERE 1 %ld\n", mtot[1]);
    int root_m = gtab[0] - 1;
    if (dump) {
        char fn[128];
        snprintf(fn, sizeof fn, "out/misere_s%d.bin", s_param);
        FILE *f = fopen(fn, "wb");
        if (!f) { perror(fn); exit(1); }
        fwrite(gtab, 1, TABSZ, f);
        fclose(f);
    }
    printf("ROOT_GRUNDY %d\n", root_g);
    printf("ROOT_MISERE %d\n", root_m);
    printf("DONE\n");
}

static void mode_full(int dump) {
    S = 0;
    for (int i = 0; i < M; i++) cnt[i] = 0;
    for (int p = 0; p < N; p++) bad[p] = 0;
    for (int k = 0; k <= N; k++) { len[k] = 0; maxcnt[k] = 0; }
    max_size = 0;
    dfs(-1);
    report(dump);
}

/* Second, independent enumeration: scan every k-subset with Gosper's hack and
 * test safety by a direct octad-intersection scan (no incremental state).
 * Safe-set sizes above s+7 are impossible here because a safe set of size
 * s+8 would have a safe (s+7)-subset; the loop verifies that no safe
 * (s+7)-set exists (and no safe larger set can then exist). */
static void mode_fullbrute(int dump) {
    int kmax = s_param + 7;
    if (kmax > N) kmax = N;
    for (int k = 0; k <= N; k++) { len[k] = 0; maxcnt[k] = 0; }
    max_size = 0;
    for (int k = 0; k <= kmax; k++) {
        long safe = 0, maximal = 0;
        uint32_t lim = 1u << N;
        uint32_t x = (k == 0) ? 0u : ((1u << k) - 1u);
        while (1) {
            int ok = 1;
            uint32_t cover = 0;
            for (int b = 0; b < M; b++) {
                int c = __builtin_popcount(x & oct[b]);
                if (c > s_param) { ok = 0; break; }
                if (c == s_param) cover |= oct[b];
            }
            if (ok) {
                safe++;
                if (len[k] >= cap[k]) { fprintf(stderr, "overflow size %d\n", k); exit(1); }
                masks[k][len[k]++] = x;
                uint32_t outside = (~x) & 0xFFFFFFu;
                if ((outside & ~cover) == 0) maximal++;
            }
            if (k == 0) break;
            uint32_t u = x & (~x + 1u);
            if (!u) break;
            uint32_t v = x + u;
            x = v + (((v ^ x) / u) >> 2);
            if (x >= lim) break;
        }
        maxcnt[k] = maximal;
    }
    report(dump);
}

/* ------------------------------- brute force over all k-subsets ---------- */
static uint8_t *build_dodecads(long *count) {
    uint8_t *dod = (uint8_t *)calloc(TABSZ, 1);
    if (!dod) { fprintf(stderr, "oom dod\n"); exit(1); }
    long c = 0;
    for (int i = 0; i < M; i++)
        for (int j = i + 1; j < M; j++) {
            uint32_t a = oct[i] & oct[j];
            if (__builtin_popcount(a) == 2) {
                uint32_t d = oct[i] ^ oct[j];
                if (!dod[d]) { dod[d] = 1; c++; }
            }
        }
    *count = c;
    return dod;
}

static void mode_brute(int k) {
    long safe = 0, maximal = 0;
    long dod_hits = 0, safe_not_dod = 0;
    uint8_t *dod = NULL;
    if (s_param == 6 && k == 12) {
        long dc;
        dod = build_dodecads(&dc);
        printf("DODECADS %ld\n", dc);
    }
    uint32_t lim = 1u << N;
    uint32_t x = (1u << k) - 1;
    while (x < lim) {
        int ok = 1;
        uint32_t cover = 0;
        for (int b = 0; b < M; b++) {
            int c = __builtin_popcount(x & oct[b]);
            if (c > s_param) { ok = 0; break; }
            if (c == s_param) cover |= oct[b];
        }
        if (ok) {
            safe++;
            if (dod && dod[x]) dod_hits++;
            if (dod && !dod[x]) safe_not_dod++;
            uint32_t outside = (~x) & 0xFFFFFFu;
            if ((outside & ~cover) == 0) maximal++;
        }
        uint32_t u = x & (~x + 1u);
        if (!u) break;
        uint32_t v = x + u;
        x = v + (((v ^ x) / u) >> 2);
    }
    printf("BRUTE s=%d k=%d TOTAL %ld SAFE %ld MAXIMAL %ld\n",
           s_param, k, binom(N, k), safe, maximal);
    if (dod) {
        printf("DODECAD_HITS %ld SAFE_NOT_DODECAD %ld\n", dod_hits, safe_not_dod);
        free(dod);
    }
    printf("DONE\n");
}

static void mode_dodecads(void) {
    long dc;
    uint8_t *dod = build_dodecads(&dc);
    printf("DODECADS %ld\n", dc);
    long bad_inters = 0, not_max = 0;
    long profile[9] = {0};
    for (uint32_t d = 0; d < TABSZ; d++) {
        if (!dod[d]) continue;
        int counts[9] = {0};
        uint32_t cover = 0;
        int ok = 1;
        for (int b = 0; b < M; b++) {
            int c = __builtin_popcount(d & oct[b]);
            if (c & 1) ok = 0;
            if (c < 2 || c > 6) ok = 0;
            counts[c]++;
            if (c == 6) cover |= oct[b];
        }
        if (!ok) bad_inters++;
        if (((~d) & 0xFFFFFFu & ~cover) != 0) not_max++;
        for (int c = 0; c <= 8; c++) if (counts[c]) profile[c]++;
    }
    printf("BAD_INTERSECTION_PROFILE %ld\n", bad_inters);
    printf("NOT_MAXIMAL_S6 %ld\n", not_max);
    for (int c = 0; c <= 8; c++)
        if (profile[c]) printf("PROFILE %d %ld\n", c, profile[c]);
    free(dod);
    printf("DONE\n");
}

static void mode_code(void) {
    /* F2 span of the octads */
    uint32_t basis[24] = {0};
    int rank = 0;
    for (int i = 0; i < M; i++) {
        uint32_t x = oct[i];
        for (int b = 23; b >= 0; b--) {
            if (!((x >> b) & 1)) continue;
            if (basis[b]) { x ^= basis[b]; }
            else { basis[b] = x; rank++; break; }
        }
    }
    printf("RANK %d\n", rank);
    /* enumerate the span */
    uint32_t rows[24];
    int nr = 0;
    for (int b = 0; b < 24; b++) if (basis[b]) rows[nr++] = basis[b];
    long wd[25] = {0};
    uint8_t *w8 = (uint8_t *)calloc(TABSZ, 1);
    uint8_t *w12 = (uint8_t *)calloc(TABSZ, 1);
    uint8_t *w16 = (uint8_t *)calloc(TABSZ, 1);
    for (uint32_t m = 0; m < (1u << nr); m++) {
        uint32_t w = 0;
        for (int i = 0; i < nr; i++) if ((m >> i) & 1) w ^= rows[i];
        int wt = __builtin_popcount(w);
        wd[wt]++;
        if (wt == 8) w8[w] = 1;
        if (wt == 12) w12[w] = 1;
        if (wt == 16) w16[w] = 1;
    }
    for (int wt = 0; wt <= 24; wt++) if (wd[wt]) printf("WEIGHT %d %ld\n", wt, wd[wt]);
    long oct_hits = 0, dod_hits = 0, comp_hits = 0;
    for (int i = 0; i < M; i++) if (w8[oct[i]]) oct_hits++;
    long dc;
    uint8_t *dod = build_dodecads(&dc);
    for (uint32_t d = 0; d < TABSZ; d++) {
        if (!dod[d]) continue;
        dod_hits++;
        if (w12[d]) comp_hits++;
        if (!w16[d ^ 0xFFFFFFu]) { /* complement weight 12 of a dodecad */ }
    }
    printf("WEIGHT8_ARE_OCTADS %ld/%d\n", oct_hits, M);
    printf("DODECADS %ld WEIGHT12_FLAG %ld CODE_WEIGHT12_HITS %ld\n", dc, dod_hits, comp_hits);
    for (uint32_t d = 0; d < TABSZ; d++) {
        if (w12[d] && !dod[d]) printf("WEIGHT12_NOT_DODECAD %u\n", d);
    }
    free(w8); free(w12); free(w16); free(dod);
    printf("DONE\n");
}

int main(int argc, char **argv) {
    setvbuf(stdout, NULL, _IONBF, 0);
    load_board("../../design-kyouen-witt-20261125/output/board_w24.txt");
    if (argc < 2) { fprintf(stderr, "usage: witt full|brute|dodecads|code ...\n"); return 2; }
    if (!strcmp(argv[1], "full")) {
        if (argc < 3) { fprintf(stderr, "need s\n"); return 2; }
        s_param = atoi(argv[2]);
        alloc_masks();
        mode_full(argc >= 4 && !strcmp(argv[3], "dump"));
    } else if (!strcmp(argv[1], "fullbrute")) {
        if (argc < 3) { fprintf(stderr, "need s\n"); return 2; }
        s_param = atoi(argv[2]);
        alloc_masks();
        mode_fullbrute(argc >= 4 && !strcmp(argv[3], "dump"));
    } else if (!strcmp(argv[1], "brute")) {
        if (argc < 4) { fprintf(stderr, "need s k\n"); return 2; }
        s_param = atoi(argv[2]);
        int k = atoi(argv[3]);
        alloc_masks();
        mode_brute(k);
    } else if (!strcmp(argv[1], "dodecads")) {
        mode_dodecads();
    } else if (!strcmp(argv[1], "code")) {
        mode_code();
    } else {
        fprintf(stderr, "unknown mode\n");
        return 2;
    }
    return 0;
}
