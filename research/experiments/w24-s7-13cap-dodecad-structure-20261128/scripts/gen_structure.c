/*
 * gen_structure.c — W_24 s=7 stage 1 (enumeration & incidence, no Grundy)
 *
 * 1. Rebuild the binary Golay code from the 759 octads of board_w24.txt
 *    (F2 span), print the weight distribution, collect the 2,576 dodecads
 *    (weight-12 words).
 * 2. Build the d11 set: all 11-subsets of dodecads (expected 30,912,
 *    pairwise distinct).
 * 3. Enumerate ALL safe 13-subsets of the 24 points (no octad contained;
 *    this is exactly "safe position of size 13" in the s=7 game).
 *    Expected count 30,912. Also verify every one of them is terminal
 *    (no point can be added without creating an octad with 8 points).
 * 4. For every 13-cap, count the dodecads it contains (expect exactly 1),
 *    and for every dodecad count the 13-caps containing it (expect 12).
 *    Total incidences expected 30,912 = 2,576 x 12.
 * 5. For every 13-cap, split its C(13,11)=78 11-subsets into d11 members
 *    (expect exactly 12, all subsets of the unique contained dodecad) and
 *    non-d11 (expect exactly 66). Collect all non-d11 11-subsets
 *    (expect 30,912 x 66 = 2,040,192, pairwise distinct).
 *
 * Usage:
 *   gen_structure board golay_out caps_out d11_out nond11_bin summary_json
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXBLOCKS 1024

static int n = 24, nb;
static uint32_t blocks[MAXBLOCKS];
static int pc[32][MAXBLOCKS], npc[32];

static int cmp_u32(const void *a, const void *b) {
    uint32_t x = *(const uint32_t *)a, y = *(const uint32_t *)b;
    return (x > y) - (x < y);
}

static int bsearch_u32(const uint32_t *arr, int N, uint32_t v) {
    int lo = 0, hi = N - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] == v) return 1;
        if (arr[mid] < v) lo = mid + 1; else hi = mid - 1;
    }
    return 0;
}

static double now_sec(void) { return (double)clock() / CLOCKS_PER_SEC; }

int main(int argc, char **argv) {
    if (argc != 7) {
        fprintf(stderr, "usage: %s board golay_out caps_out d11_out nond11_bin summary_json\n", argv[0]);
        return 2;
    }
    double t0 = now_sec();

    /* ---- board ---- */
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("board"); return 2; }
    if (fscanf(f, "%d %d", &n, &nb) != 2) return 2;
    for (int i = 0; i < nb; i++) {
        int k, p; uint32_t m = 0;
        if (fscanf(f, "%d", &k) != 1) return 2;
        for (int j = 0; j < k; j++) { if (fscanf(f, "%d", &p) != 1) return 2; m |= 1u << p; }
        blocks[i] = m;
    }
    fclose(f);
    memset(npc, 0, sizeof npc);
    for (int i = 0; i < nb; i++)
        for (int p = 0; p < n; p++)
            if (blocks[i] & (1u << p)) pc[p][npc[p]++] = i;
    fprintf(stderr, "board n=%d nb=%d\n", n, nb);

    /* ---- Golay span from octads ---- */
    uint32_t piv[32]; memset(piv, 0, sizeof piv);
    for (int i = 0; i < nb; i++) {
        uint32_t x = blocks[i];
        while (x) { int hb = 31 - __builtin_clz(x); if (piv[hb]) x ^= piv[hb]; else { piv[hb] = x; break; } }
    }
    uint32_t basis[32]; int nbasis = 0;
    for (int i = 0; i < 32; i++) if (piv[i]) basis[nbasis++] = piv[i];
    uint32_t span[4096]; int nspan = 1; span[0] = 0;
    for (int i = 0; i < nbasis; i++) {
        int cur = nspan;
        for (int j = 0; j < cur; j++) span[nspan++] = span[j] ^ basis[i];
    }
    fprintf(stderr, "basis=%d span=%d\n", nbasis, nspan);

    int wh[25]; memset(wh, 0, sizeof wh);
    uint32_t *dod = malloc(4096 * sizeof(uint32_t)); int ndod = 0;
    for (int i = 0; i < nspan; i++) {
        int w = __builtin_popcount(span[i]);
        wh[w]++;
        if (w == 12) dod[ndod++] = span[i];
    }

    /* ---- d11 set ---- */
    uint32_t *d11 = malloc((size_t)ndod * 12 * sizeof(uint32_t)); int nd11 = 0;
    for (int i = 0; i < ndod; i++)
        for (int p = 0; p < n; p++)
            if (dod[i] & (1u << p)) d11[nd11++] = dod[i] ^ (1u << p);
    qsort(d11, nd11, sizeof(uint32_t), cmp_u32);
    long d11_dup = 0; uint32_t d11_dupfirst = 0;
    for (int i = 1; i < nd11; i++)
        if (d11[i] == d11[i - 1]) { if (!d11_dup) d11_dupfirst = d11[i]; d11_dup++; }

    /* ---- enumerate all safe 13-subsets ---- */
    double tc = now_sec();
    int capcap = 1 << 16; uint32_t *caps = malloc(capcap * sizeof(uint32_t)); int ncaps = 0;
    for (uint32_t m = 0; m < (1u << n); m++) {
        if (__builtin_popcount(m) != 13) continue;
        int safe = 1;
        for (int i = 0; i < nb; i++)
            if ((m & blocks[i]) == blocks[i]) { safe = 0; break; }
        if (safe) {
            if (ncaps == capcap) { capcap *= 2; caps = realloc(caps, capcap * sizeof(uint32_t)); }
            caps[ncaps++] = m;
        }
    }
    double tcap = now_sec() - tc;

    /* ---- maximality (terminality) of every 13-cap ---- */
    long caps_nonmax = 0; uint32_t caps_nonmax_first = 0;
    for (int i = 0; i < ncaps; i++) {
        uint32_t c = caps[i]; int ext = 0;
        for (int p = 0; p < n && !ext; p++) {
            if (c & (1u << p)) continue;
            int blocked = 0;
            for (int j = 0; j < npc[p]; j++)
                if (__builtin_popcount(c & blocks[pc[p][j]]) >= 7) { blocked = 1; break; }
            if (!blocked) ext = 1; /* p can legally be added -> not maximal */
        }
        if (ext) { if (!caps_nonmax) caps_nonmax_first = c; caps_nonmax++; }
    }

    /* ---- incidence: dodecads inside caps ---- */
    double ti = now_sec();
    int *percap = calloc(ncaps, sizeof(int));
    int *perdod = calloc(ndod, sizeof(int));
    uint32_t *capdod = malloc(ncaps * sizeof(uint32_t));
    long total_inc = 0;
    int percap_hist[64]; memset(percap_hist, 0, sizeof percap_hist);
    int perdod_min = 1 << 30, perdod_max = 0;
    for (int i = 0; i < ncaps; i++) {
        int cnt = 0;
        for (int j = 0; j < ndod; j++)
            if ((caps[i] & dod[j]) == dod[j]) { cnt++; perdod[j]++; capdod[i] = dod[j]; }
        percap[i] = cnt; percap_hist[cnt ? (cnt < 63 ? cnt : 63) : 0]++; total_inc += cnt;
    }
    for (int j = 0; j < ndod; j++) {
        if (perdod[j] < perdod_min) perdod_min = perdod[j];
        if (perdod[j] > perdod_max) perdod_max = perdod[j];
    }
    double tinc = now_sec() - ti;

    /* ---- 66/12 split of 11-subsets ---- */
    double ts = now_sec();
    uint32_t *nond11 = malloc((size_t)ncaps * 66 * sizeof(uint32_t)); long nnond = 0;
    int dhist[128]; memset(dhist, 0, sizeof dhist);
    long d11_outside_dod = 0;
    for (int i = 0; i < ncaps; i++) {
        uint32_t c = caps[i]; int pts[13], m = 0;
        for (int p = 0; p < n; p++) if (c & (1u << p)) pts[m++] = p;
        int din = 0;
        for (int a = 0; a < 13; a++) for (int b = a + 1; b < 13; b++) {
            uint32_t sub = c & ~((1u << pts[a]) | (1u << pts[b]));
            if (bsearch_u32(d11, nd11, sub)) {
                din++;
                if ((sub & capdod[i]) != sub) d11_outside_dod++;
            } else {
                nond11[nnond++] = sub;
            }
        }
        dhist[din < 127 ? din : 127]++;
    }
    qsort(nond11, nnond, sizeof(uint32_t), cmp_u32);
    long nond_dup = 0; uint32_t nond_dupfirst = 0;
    for (long i = 1; i < nnond; i++)
        if (nond11[i] == nond11[i - 1]) { if (!nond_dup) nond_dupfirst = nond11[i]; nond_dup++; }
    double tsplit = now_sec() - ts;
    double tall = now_sec() - t0;

    /* ---- outputs ---- */
    FILE *g = fopen(argv[2], "w");
    for (int w = 0; w <= 24; w++) if (wh[w]) fprintf(g, "weight %d count %d\n", w, wh[w]);
    fclose(g);
    FILE *cf = fopen(argv[3], "w");
    for (int i = 0; i < ncaps; i++) fprintf(cf, "%u\n", caps[i]);
    fclose(cf);
    FILE *df = fopen(argv[4], "w");
    for (int i = 0; i < nd11; i++) fprintf(df, "%u\n", d11[i]);
    fclose(df);
    FILE *nf = fopen(argv[5], "wb");
    fwrite(nond11, sizeof(uint32_t), nnond, nf);
    fclose(nf);

    /* pass flags */
    int pass_weights = wh[0] == 1 && wh[8] == 759 && wh[12] == 2576 && wh[16] == 759 && wh[24] == 1 && nspan == 4096;
    int pass_dod = ndod == 2576;
    int pass_d11 = nd11 == 30912 && d11_dup == 0;
    int pass_caps = ncaps == 30912 && caps_nonmax == 0;
    int pass_inc = total_inc == 30912 && percap_hist[1] == ncaps && perdod_min == 12 && perdod_max == 12;
    int pass_split = dhist[12] == ncaps && d11_outside_dod == 0 && nnond == 2040192L && nond_dup == 0;
    int pass_all = pass_weights && pass_dod && pass_d11 && pass_caps && pass_inc && pass_split;

    FILE *sf = fopen(argv[6], "w");
    fprintf(sf, "{\n");
    fprintf(sf, "  \"stage\": 1,\n");
    fprintf(sf, "  \"board\": \"%s\",\n", argv[1]);
    fprintf(sf, "  \"nbasis\": %d, \"span_size\": %d,\n", nbasis, nspan);
    fprintf(sf, "  \"weight_hist\": [%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d],\n",
            wh[0], wh[1], wh[2], wh[3], wh[4], wh[5], wh[6], wh[7], wh[8], wh[9], wh[10], wh[11],
            wh[12], wh[13], wh[14], wh[15], wh[16], wh[17], wh[18], wh[19], wh[20], wh[21], wh[22], wh[23], wh[24]);
    fprintf(sf, "  \"dodecads\": %d,\n", ndod);
    fprintf(sf, "  \"d11_count\": %d, \"d11_duplicates\": %ld, \"d11_dup_first\": %u,\n", nd11, d11_dup, d11_dupfirst);
    fprintf(sf, "  \"caps13_count\": %d, \"caps13_nonmaximal\": %ld, \"caps13_nonmax_first\": %u,\n", ncaps, caps_nonmax, caps_nonmax_first);
    fprintf(sf, "  \"per_cap_dodecad_hist\": {\"1\": %d},\n", percap_hist[1]);
    fprintf(sf, "  \"per_dodecad_caps_min\": %d, \"per_dodecad_caps_max\": %d,\n", perdod_min, perdod_max);
    fprintf(sf, "  \"total_incidences\": %ld,\n", total_inc);
    fprintf(sf, "  \"d11_per_cap_hist\": {\"12\": %d},\n", dhist[12]);
    fprintf(sf, "  \"d11_outside_contained_dodecad\": %ld,\n", d11_outside_dod);
    fprintf(sf, "  \"nond11_count\": %ld, \"nond11_duplicates\": %ld, \"nond11_dup_first\": %u,\n", nnond, nond_dup, nond_dupfirst);
    fprintf(sf, "  \"pass\": {\"weights\": %s, \"dodecads\": %s, \"d11\": %s, \"caps\": %s, \"incidence\": %s, \"split\": %s, \"all\": %s},\n",
            pass_weights ? "true" : "false", pass_dod ? "true" : "false", pass_d11 ? "true" : "false",
            pass_caps ? "true" : "false", pass_inc ? "true" : "false", pass_split ? "true" : "false",
            pass_all ? "true" : "false");
    fprintf(sf, "  \"seconds\": {\"caps_scan\": %.3f, \"incidence\": %.3f, \"split\": %.3f, \"total\": %.3f}\n",
            tcap, tinc, tsplit, tall);
    fprintf(sf, "}\n");
    fclose(sf);

    printf("stage1: span=%d weights_pass=%d dodecads=%d d11=%d(dup %ld) caps=%d(nonmax %ld) "
           "inc=%ld(caphist1 %d, dod %d..%d) split d11/cap=%d(nonmember %ld) nond11=%ld(dup %ld) PASS=%d  [%.1fs]\n",
           nspan, pass_weights, ndod, nd11, d11_dup, ncaps, caps_nonmax,
           total_inc, percap_hist[1], perdod_min, perdod_max,
           dhist[12], d11_outside_dod, nnond, nond_dup, pass_all, tall);
    free(dod); free(d11); free(caps); free(percap); free(perdod); free(capdod); free(nond11);
    return pass_all ? 0 : 1;
}
