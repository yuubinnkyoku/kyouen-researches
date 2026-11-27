/* Full census of dodecad k-subsets and maximal-13-cap k-subsets of W_24,
 * plus the d11 -> 13-cap incidence index (full verification of the
 * uniformity claim of K1349).
 *
 * Board: board_w24.txt (n=24, 759 octads).  s=7 game: a position meets
 * every octad in at most 7 points; a kyouen is a full octad.
 *
 * Outputs (output/):
 *   dodecads.txt     2,576 Golay weight-12 masks
 *   max13caps.txt    30,912 maximal 13-cap masks (octad-free 13-subsets)
 *   census_raw.json  per-k distinct counts, multiplicities, incidence data
 *
 * Single-threaded by design (shared-machine load cap: max 4 workers).
 *
 * Build: gcc -O2 -o census census.c
 * Run:   ./census ../design-kyouen-witt-20261125/output/board_w24.txt
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n = 24, nb;
static uint32_t blocks[1024];
static int pcnt[32][1024], npc[32];
static uint32_t allmask;

/* multiplicity arrays over all 2^24 masks (uint16 saturates well below 65536) */
static uint16_t *dcnt, *tcnt, *dext;

static long long d_by_k[24], t_by_k[24], both_by_k[24];
static long long dsum_by_k[24], tsum_by_k[24];
static long long d_hist[24][3000 + 1];   /* dodecad multiplicity per k-subset (max 2576) */
static long long t_hist[24][30912 + 1];  /* 13-cap multiplicity per k-subset  (max 30912) */
/* dext histograms restricted to masks that are dodecad k-subsets */
static long long dext_hist[24][30912 + 1];
/* 13-cap -> number of its 11-subsets that are d11 */
static long long capd11_hist[80];
/* d11 -> number of containing 13-caps */
static long long d11cap_hist[30912 + 1];
static long long d11_total, d11_count, d12_count, d12cap_total;

static long long C[25][25];
static void binomials(void) {
    for (int i = 0; i <= 24; i++) { C[i][0] = 1; for (int j = 1; j <= i; j++) C[i][j] = C[i-1][j-1] + (j <= i-1 ? C[i-1][j] : 0); }
}

static int ok_add(uint32_t mask, int p) {
    for (int i = 0; i < npc[p]; i++) {
        int b = pcnt[p][i];
        if (__builtin_popcount(mask & blocks[b]) >= 7) return 0;
    }
    return 1;
}

static int is_cap(uint32_t m) {
    for (int i = 0; i < nb; i++)
        if ((m & blocks[i]) == blocks[i]) return 0;
    return 1;
}

int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("board"); return 2; }
    if (fscanf(f, "%d %d", &n, &nb) != 2) return 2;
    for (int i = 0; i < nb; i++) {
        int k, p; if (fscanf(f, "%d", &k) != 1) return 2;
        uint32_t m = 0;
        for (int j = 0; j < k; j++) { fscanf(f, "%d", &p); m |= 1u << p; }
        blocks[i] = m;
    }
    fclose(f);
    memset(npc, 0, sizeof npc);
    for (int i = 0; i < nb; i++)
        for (int p = 0; p < n; p++)
            if (blocks[i] & (1u << p)) pcnt[p][npc[p]++] = i;
    allmask = (1u << n) - 1;
    binomials();

    /* Golay span from octads (same construction as fullcheck.c) */
    uint32_t piv[32]; memset(piv, 0, sizeof piv);
    for (int i = 0; i < nb; i++) {
        uint32_t x = blocks[i];
        while (x) { int hb = 31 - __builtin_clz(x); if (piv[hb]) x ^= piv[hb]; else { piv[hb] = x; break; } }
    }
    uint32_t basis[32]; int nbasis = 0;
    for (int i = 0; i < 32; i++) if (piv[i]) basis[nbasis++] = piv[i];
    static uint32_t span[4096]; int nspan = 0;
    span[nspan++] = 0;
    for (int i = 0; i < nbasis; i++) {
        int cur = nspan;
        for (int j = 0; j < cur; j++) span[nspan++] = span[j] ^ basis[i];
    }
    long long wdist[25] = {0};
    for (int i = 0; i < nspan; i++) wdist[__builtin_popcount(span[i])]++;
    static uint32_t dodec[4096]; int ndodec = 0;
    for (int i = 0; i < nspan; i++) if (__builtin_popcount(span[i]) == 12) dodec[ndodec++] = span[i];
    fprintf(stderr, "span %d, dodecads %d\n", nspan, ndodec);
    if (ndodec != 2576) { fprintf(stderr, "FATAL dodecad count\n"); return 3; }

    /* enumerate maximal 13-caps = octad-free 13-subsets */
    static uint32_t *caps; caps = malloc(40000 * sizeof(uint32_t)); int ncaps = 0;
    for (uint32_t m = 0; m <= allmask; m++) {
        if (__builtin_popcount(m) != 13) continue;
        int cap = 1;
        for (int i = 0; i < nb; i++) if ((m & blocks[i]) == blocks[i]) { cap = 0; break; }
        if (cap) caps[ncaps++] = m;
    }
    fprintf(stderr, "max13caps %d\n", ncaps);
    if (ncaps != 30912) { fprintf(stderr, "FATAL 13cap count\n"); return 3; }
    /* spot-check maximality of 5 caps */
    for (int t = 0; t < 5; t++) {
        uint32_t m = caps[(t * 7919) % ncaps];
        for (int p = 0; p < n; p++) {
            if (m & (1u << p)) continue;
            if (ok_add(m, p)) { fprintf(stderr, "FATAL 13cap %u extendable\n", m); return 3; }
        }
    }

    dcnt = calloc(1u << 24, sizeof(uint16_t));
    tcnt = calloc(1u << 24, sizeof(uint16_t));
    dext = calloc(1u << 24, sizeof(uint16_t));
    if (!dcnt || !tcnt || !dext) { fprintf(stderr, "OOM\n"); return 2; }

    /* mark dodecad subsets with multiplicities */
    for (int i = 0; i < ndodec; i++) {
        uint32_t D = dodec[i];
        for (uint32_t s = D; s; s = (s - 1) & D) dcnt[s]++;
        dcnt[0]++;
    }
    /* mark 13-cap subsets with multiplicities; index dodecad-subset incidences */
    for (int i = 0; i < ncaps; i++) {
        uint32_t Cm = caps[i];
        int d11_here = 0;
        for (uint32_t s = Cm; s; s = (s - 1) & Cm) {
            tcnt[s]++;
            if (dcnt[s]) {
                dext[s]++;
                int pcs = __builtin_popcount(s);
                if (pcs == 11) d11_here++;
                if (pcs == 12) d12cap_total++;
            }
        }
        tcnt[0]++;
        if (dcnt[0]) { /* empty set contained in every dodecad */
            dext[0]++;
        }
        capd11_hist[d11_here]++;
    }
    fprintf(stderr, "marking done\n");

    /* readout */
    for (uint32_t m = 0; m <= allmask; m++) {
        int pcs = __builtin_popcount(m);
        if (dcnt[m]) { d_by_k[pcs]++; dsum_by_k[pcs] += dcnt[m]; if (dcnt[m] <= 3000) d_hist[pcs][dcnt[m]]++; }
        if (tcnt[m]) { t_by_k[pcs]++; tsum_by_k[pcs] += tcnt[m]; if (tcnt[m] <= 30912) t_hist[pcs][tcnt[m]]++; }
        if (dcnt[m] && tcnt[m]) both_by_k[pcs]++;
        if (dcnt[m]) { dext_hist[pcs][dext[m]]++; if (pcs == 11) { d11_count++; d11_total += dext[m]; } if (pcs == 12) d12_count++; }
    }

    /* self-checks */
    int checks_ok = 1;
    for (int k = 0; k <= 13; k++) {
        long long expd = (long long)ndodec * C[12][k];
        long long expt = (long long)ncaps * C[13][k];
        if (dsum_by_k[k] != expd) { fprintf(stderr, "CHECK FAIL dsum k=%d %lld != %lld\n", k, dsum_by_k[k], expd); checks_ok = 0; }
        if (tsum_by_k[k] != expt) { fprintf(stderr, "CHECK FAIL tsum k=%d %lld != %lld\n", k, tsum_by_k[k], expt); checks_ok = 0; }
    }
    /* d11 multiplicities must all be 1 (two dodecads share <= 8 points) */
    if (d_by_k[11] != dsum_by_k[11] || d_by_k[11] != 30912) { fprintf(stderr, "CHECK FAIL d11 multiplicity\n"); checks_ok = 0; }
    fprintf(stderr, "self-checks %s\n", checks_ok ? "PASS" : "FAIL");

    /* aggregate dodecad x octad intersection profile */
    long long prof[9] = {0};
    for (int i = 0; i < ndodec; i++)
        for (int b = 0; b < nb; b++) { int c = __builtin_popcount(dodec[i] & blocks[b]); prof[c]++; }
    fprintf(stderr, "dodecad-octad intersection profile:");
    for (int c = 0; c <= 8; c++) if (prof[c]) fprintf(stderr, " %d:%lld", c, prof[c]);
    fprintf(stderr, "\n");

    FILE *fd = fopen("output/dodecads.txt", "w");
    fprintf(fd, "dodecads %d\n", ndodec);
    for (int i = 0; i < ndodec; i++) fprintf(fd, "%u\n", dodec[i]);
    fclose(fd);
    FILE *fc = fopen("output/max13caps.txt", "w");
    fprintf(fc, "max13caps %d\n", ncaps);
    for (int i = 0; i < ncaps; i++) fprintf(fc, "%u\n", caps[i]);
    fclose(fc);

    FILE *fo = fopen("output/census_raw.json", "w");
    fprintf(fo, "{\n");
    fprintf(fo, "  \"board\": \"%s\",\n", argv[1]);
    fprintf(fo, "  \"n\": %d, \"blocks\": %d, \"s\": 7,\n", n, nb);
    fprintf(fo, "  \"span\": %d, \"weight_distribution\": {", nspan);
    int first = 1;
    for (int w = 0; w <= 24; w++) if (wdist[w]) { fprintf(fo, "%s\"%d\": %lld", first ? "" : ", ", w, wdist[w]); first = 0; }
    fprintf(fo, "},\n");
    fprintf(fo, "  \"dodecads\": %d,\n", ndodec);
    fprintf(fo, "  \"max13caps\": %d,\n", ncaps);
    fprintf(fo, "  \"self_checks_pass\": %s,\n", checks_ok ? "true" : "false");
    fprintf(fo, "  \"dodecad_octad_profile\": {");
    first = 1;
    for (int c = 0; c <= 8; c++) if (prof[c]) { fprintf(fo, "%s\"%d\": %lld", first ? "" : ", ", c, prof[c]); first = 0; }
    fprintf(fo, "},\n");
    fprintf(fo, "  \"capd11_hist\": {");
    first = 1;
    for (int v = 0; v <= 78; v++) if (capd11_hist[v]) { fprintf(fo, "%s\"%d\": %lld", first ? "" : ", ", v, capd11_hist[v]); first = 0; }
    fprintf(fo, "},\n");
    fprintf(fo, "  \"d11_count\": %lld, \"d11cap_total\": %lld,\n", d11_count, d11_total);
    fprintf(fo, "  \"d12_count\": %lld, \"d12cap_total_rawcheck_note\": \"dodecad 13-cap containment from dext_hist[12]\",\n", d12_count);
    fprintf(fo, "  \"per_k\": [\n");
    for (int k = 0; k <= 13; k++) {
        fprintf(fo, "    {\"k\": %d, \"binom24\": %lld, \"dodecad_subsets\": %lld, \"cap13_subsets\": %lld, \"both\": %lld, \"d_raw\": %lld, \"t_raw\": %lld,\n",
                k, C[24][k], d_by_k[k], t_by_k[k], both_by_k[k], dsum_by_k[k], tsum_by_k[k]);
        fprintf(fo, "     \"d_mult_hist\": {");
        first = 1;
        for (int v = 0; v <= 3000; v++) if (d_hist[k][v]) { fprintf(fo, "%s\"%d\": %lld", first ? "" : ", ", v, d_hist[k][v]); first = 0; }
        fprintf(fo, "}, \"t_mult_hist\": {");
        first = 1;
        for (int v = 0; v <= 30912; v++) if (t_hist[k][v]) { fprintf(fo, "%s\"%d\": %lld", first ? "" : ", ", v, t_hist[k][v]); first = 0; }
        fprintf(fo, "}, \"dext_hist_in_dodecad_subsets\": {");
        first = 1;
        for (int v = 0; v <= 30912; v++) if (dext_hist[k][v]) { fprintf(fo, "%s\"%d\": %lld", first ? "" : ", ", v, dext_hist[k][v]); first = 0; }
        fprintf(fo, "}}%s\n", k < 13 ? "," : "");
    }
    fprintf(fo, "  ]\n}\n");
    fclose(fo);
    fprintf(stderr, "census written\n");
    return 0;
}
