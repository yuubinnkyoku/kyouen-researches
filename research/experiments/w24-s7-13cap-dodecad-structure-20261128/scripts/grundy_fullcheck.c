/*
 * grundy_fullcheck.c — W_24 s=7 stage 2 (Grundy + extension profiles of
 * the 11-subset layers)
 *
 * Semantics (s=7 game): a position is safe iff every octad meets it in
 * <= 7 points.  A safe 13-subset is terminal (all safe 13-subsets are the
 * 30,912 maximal caps; verified in stage 1).  Therefore for any safe
 * 12-mask M: G(M) = 0 if M has no safe child, else 1 (children of M are
 * safe 13-masks with G = 0).  For an 11-mask S, the children S+{p} are
 * safe 12-masks with G in {0,1}, so G(S) = mex{0,1} subset = 0/1/2, and
 * G(S) = 2 iff S has both a terminal (maximal) and a non-terminal child.
 *
 * Program verifies, over a slice of the 2,040,192 non-d11 11-subsets:
 *   - Grundy value (expect 2 for every one)
 *   - number of maximal 12-caps S+{p} (maximal 12-extensions; expect 6)
 *   - number of 13-caps containing S (maximal 13-extensions; expect 1)
 * Part 0 additionally verifies the d11 side (expect G=0, no maximal
 * 12-extension, exactly 12 13-caps for every d11) and the dodecads
 * themselves (12 addable points, all children terminal => G=1; contained
 * in exactly 12 13-caps).
 *
 * Usage:
 *   grundy_fullcheck board caps_file d11_file nond11_bin part nparts limit stride out_json
 * limit > 0: probe mode, process at most `limit` masks (extras skipped).
 * stride > 1: process masks whose global index i satisfies i % stride == part.
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
static uint8_t *capbit, *d11bit;

static inline int bittest(const uint8_t *b, uint32_t m) { return (b[m >> 3] >> (m & 7)) & 1; }
static inline void bitsetit(uint8_t *b, uint32_t m) { b[m >> 3] |= (uint8_t)(1u << (m & 7)); }

static inline int ok_add(uint32_t mask, int p) {
    for (int i = 0; i < npc[p]; i++)
        if (__builtin_popcount(mask & blocks[pc[p][i]]) >= 7) return 0;
    return 1;
}

/* Grundy of a safe 11-mask S by one-level expansion, plus the number of
 * terminal (= maximal 12-cap) children. */
static void analyze11(uint32_t S, int *gout, int *max12out) {
    int seen0 = 0, seen1 = 0, max12 = 0;
    for (int p = 0; p < n; p++) {
        if (S & (1u << p)) continue;
        if (!ok_add(S, p)) continue;
        uint32_t C = S | (1u << p);
        int childmove = 0;
        for (int q = 0; q < n; q++) {
            if (C & (1u << q)) continue;
            if (ok_add(C, q)) { childmove = 1; break; }
        }
        if (childmove) seen1 = 1; else { seen0 = 1; max12++; }
    }
    *gout = seen0 ? (seen1 ? 2 : 1) : 0;
    *max12out = max12;
}

/* number of safe 13-masks containing S (pairs over the complement) */
static int count13(uint32_t S) {
    int comp[24], nc = 0;
    for (int p = 0; p < n; p++) if (!(S & (1u << p))) comp[nc++] = p;
    int cnt = 0;
    for (int i = 0; i < nc; i++) for (int j = i + 1; j < nc; j++)
        if (bittest(capbit, S | (1u << comp[i]) | (1u << comp[j]))) cnt++;
    return cnt;
}

static double now_sec(void) { return (double)clock() / CLOCKS_PER_SEC; }

static void load_list(const char *path, uint32_t **arr, int *N, uint8_t *bits, int exp_pc) {
    FILE *f = fopen(path, "r");
    if (!f) { perror(path); exit(2); }
    int cap = 1 << 16, k = 0; uint32_t v;
    uint32_t *a = malloc(cap * sizeof(uint32_t));
    while (fscanf(f, "%u", &v) == 1) {
        if (k == cap) { cap *= 2; a = realloc(a, cap * sizeof(uint32_t)); }
        a[k++] = v;
        if (__builtin_popcount(v) != exp_pc) { fprintf(stderr, "bad popcount %u in %s\n", v, path); exit(2); }
        if (bits) bitsetit(bits, v);
    }
    fclose(f);
    *arr = a; *N = k;
}

int main(int argc, char **argv) {
    if (argc != 10) {
        fprintf(stderr, "usage: %s board caps d11 nond11 part nparts limit stride out_json\n", argv[0]);
        return 2;
    }
    int part = atoi(argv[5]), nparts = atoi(argv[6]);
    long limit = atol(argv[7]);
    int stride = atoi(argv[8]);
    double t0 = now_sec();

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

    capbit = calloc(1u << 21, 1);
    d11bit = calloc(1u << 21, 1);
    uint32_t *caps, *d11; int ncaps, nd11;
    load_list(argv[2], &caps, &ncaps, capbit, 13);
    load_list(argv[3], &d11, &nd11, d11bit, 11);

    /* nond11 binary */
    FILE *bf = fopen(argv[4], "rb");
    if (!bf) { perror(argv[4]); return 2; }
    fseek(bf, 0, SEEK_END); long fsz = ftell(bf); fseek(bf, 0, SEEK_SET);
    long Ntot = fsz / 4;
    uint32_t *masks = malloc(fsz);
    fread(masks, 4, Ntot, bf);
    fclose(bf);

    long processed = 0;
    int gh[8]; memset(gh, 0, sizeof gh);
    static int prof[2048]; memset(prof, 0, sizeof prof); /* key = max12*128 + sup13 */
    long sum_max12 = 0, sum_sup13 = 0;
    long fails_g = 0, fails_sup = 0, fails_order = 0, fails_sanity = 0;
    uint32_t fex_g[5] = {0, 0, 0, 0, 0}, fex_sup[5] = {0, 0, 0, 0, 0}; int nf_g = 0, nf_sup = 0;
    int min_max12 = 1 << 30, max_max12 = 0, min_sup = 1 << 30, max_sup = 0;
    long nond11_size_mismatch = (Ntot != 2040192L) || (fsz % 4 != 0);

    long i_start, i_end, i_step;
    if (stride > 1) { i_start = part; i_end = Ntot; i_step = stride; }
    else {
        long chunk = Ntot / nparts, rem = Ntot % nparts;
        i_start = (long)part * chunk + (part < rem ? part : rem);
        long len = chunk + (part < rem ? 1 : 0);
        i_end = i_start + len; i_step = 1;
    }
    for (long i = i_start; i < i_end; i += i_step) {
        if (limit > 0 && processed >= limit) break;
        uint32_t S = masks[i];
        if (__builtin_popcount(S) != 11 || bittest(d11bit, S)) {
            fails_sanity++; continue;
        }
        if (processed > 0 && stride <= 1 && S <= masks[i - i_step]) {
            if (fails_order == 0) fprintf(stderr, "part %d: order violation at %ld (%u <= %u)\n", part, i, S, masks[i - i_step]);
            fails_order++;
        }
        int g, max12;
        analyze11(S, &g, &max12);
        int sup13 = count13(S);
        gh[g]++; prof[max12 * 128 + sup13]++;
        sum_max12 += max12; sum_sup13 += sup13;
        if (max12 < min_max12) min_max12 = max12;
        if (max12 > max_max12) max_max12 = max12;
        if (sup13 < min_sup) min_sup = sup13;
        if (sup13 > max_sup) max_sup = sup13;
        if (g != 2 && nf_g < 5) fex_g[nf_g++] = S;
        if (g != 2) fails_g++;
        if (sup13 != 1 && nf_sup < 5) fex_sup[nf_sup++] = S;
        if (sup13 != 1) fails_sup++;
        processed++;
    }
    double tmain = now_sec() - t0;

    /* ---- part 0 extras: d11 layer and dodecads ---- */
    long d11_bad = 0; int d11_gh[8]; memset(d11_gh, 0, sizeof d11_gh);
    static int d11_prof[2048]; memset(d11_prof, 0, sizeof d11_prof);
    uint32_t d11_badfirst = 0;
    long dod_bad = 0; int dod_gh[8]; memset(dod_gh, 0, sizeof dod_gh);
    long dod_add_hist[32]; memset(dod_add_hist, 0, sizeof dod_add_hist);
    long dod_sup_hist[64]; memset(dod_sup_hist, 0, sizeof dod_sup_hist);
    long dod_childmove_viol = 0;
    double tex = 0;
    if (part == 0 && limit <= 0) {
        double tx = now_sec();
        for (int i = 0; i < nd11; i++) {
            uint32_t S = d11[i];
            int g, max12; analyze11(S, &g, &max12);
            int sup13 = count13(S);
            d11_gh[g]++; d11_prof[max12 * 128 + sup13]++;
            if (g != 0 || max12 != 0 || sup13 != 12) {
                if (!d11_bad) d11_badfirst = S;
                d11_bad++;
            }
        }
        /* dodecads: rebuild span from octads */
        uint32_t piv[32]; memset(piv, 0, sizeof piv);
        for (int i = 0; i < nb; i++) {
            uint32_t x = blocks[i];
            while (x) { int hb = 31 - __builtin_clz(x); if (piv[hb]) x ^= piv[hb]; else { piv[hb] = x; break; } }
        }
        uint32_t basis[32]; int nbasis = 0;
        for (int i = 0; i < 32; i++) if (piv[i]) basis[nbasis++] = piv[i];
        uint32_t span[4096]; int nspan = 1; span[0] = 0;
        for (int i = 0; i < nbasis; i++) { int cur = nspan; for (int j = 0; j < cur; j++) span[nspan++] = span[j] ^ basis[i]; }
        for (int i = 0; i < nspan; i++) {
            uint32_t D = span[i];
            if (__builtin_popcount(D) != 12) continue;
            int addable = 0, term_child = 0, nchild = 0;
            for (int p = 0; p < n; p++) {
                if (D & (1u << p)) continue;
                if (!ok_add(D, p)) continue;
                addable++; nchild++;
                uint32_t C = D | (1u << p);
                int move = 0;
                for (int q = 0; q < n; q++) {
                    if (C & (1u << q)) continue;
                    if (ok_add(C, q)) { move = 1; break; }
                }
                if (!move) term_child++;
            }
            int gD = 0;
            { int seen0 = term_child > 0, seen1 = (nchild - term_child) > 0;
              gD = seen0 ? (seen1 ? 2 : 1) : 0; }
            dod_gh[gD]++;
            if (gD != 1 || addable != 12 || nchild != 12 || term_child != nchild) dod_bad++;
            if (term_child != nchild) dod_childmove_viol++;
            dod_add_hist[addable < 31 ? addable : 31]++;
            /* 13-caps containing D are exactly the safe single additions
             * (every D+{p} is a safe 13-mask; every cap containing D is
             * D+{p} for one p). count13 (pair additions) would count
             * 14-masks and is meaningless here. */
            int sup13 = addable;
            dod_sup_hist[sup13 < 63 ? sup13 : 63]++;
            if (sup13 != 12) dod_bad++;
        }
        tex = now_sec() - tx;
    }
    double tall = now_sec() - t0;

    /* ---- JSON out ---- */
    FILE *o = fopen(argv[9], "w");
    fprintf(o, "{\n  \"stage\": 2, \"part\": %d, \"nparts\": %d, \"limit\": %ld, \"stride\": %d,\n", part, nparts, limit, stride);
    fprintf(o, "  \"nond11_total\": %ld, \"nond11_size_mismatch\": %ld, \"processed\": %ld,\n", Ntot, nond11_size_mismatch, processed);
    fprintf(o, "  \"grundy_hist\": {\"0\": %d, \"1\": %d, \"2\": %d, \"3\": %d},\n", gh[0], gh[1], gh[2], gh[3]);
    fprintf(o, "  \"max12_ext_min\": %d, \"max12_ext_max\": %d, \"sup13_min\": %d, \"sup13_max\": %d,\n", min_max12, max_max12, min_sup, max_sup);
    fprintf(o, "  \"sum_max12\": %ld, \"sum_sup13\": %ld,\n", sum_max12, sum_sup13);
    fprintf(o, "  \"profile_hist\": {");
    int first = 1;
    for (int k = 0; k < 2048; k++) if (prof[k]) {
        if (!first) fprintf(o, ", ");
        fprintf(o, "\"%d,%d\": %d", k / 128, k % 128, prof[k]);
        first = 0;
    }
    fprintf(o, "},\n");
    fprintf(o, "  \"fails\": {\"sanity\": %ld, \"order\": %ld, \"grundy_ne_2\": %ld, \"sup13_ne_1\": %ld},\n",
            fails_sanity, fails_order, fails_g, fails_sup);
    fprintf(o, "  \"fail_examples_grundy\": [%u, %u, %u, %u, %u],\n", fex_g[0], fex_g[1], fex_g[2], fex_g[3], fex_g[4]);
    fprintf(o, "  \"fail_examples_sup13\": [%u, %u, %u, %u, %u],\n", fex_sup[0], fex_sup[1], fex_sup[2], fex_sup[3], fex_sup[4]);
    if (part == 0 && limit <= 0) {
        fprintf(o, "  \"d11_checked\": %d, \"d11_grundy_hist\": {\"0\": %d, \"1\": %d, \"2\": %d}, \"d11_bad\": %ld, \"d11_bad_first\": %u,\n",
                nd11, d11_gh[0], d11_gh[1], d11_gh[2], d11_bad, d11_badfirst);
        fprintf(o, "  \"d11_profile_hist\": {");
        first = 1;
        for (int k = 0; k < 2048; k++) if (d11_prof[k]) {
            if (!first) fprintf(o, ", ");
            fprintf(o, "\"%d,%d\": %d", k / 128, k % 128, d11_prof[k]);
            first = 0;
        }
        fprintf(o, "},\n");
        fprintf(o, "  \"dodecads_grundy_hist\": {\"0\": %d, \"1\": %d, \"2\": %d}, \"dodecads_bad\": %ld,\n", dod_gh[0], dod_gh[1], dod_gh[2], dod_bad);
        fprintf(o, "  \"dodecad_addable_hist\": {\"12\": %ld}, \"dodecad_sup13_hist\": {\"12\": %ld}, \"dodecad_mixed_children\": %ld,\n",
                dod_add_hist[12], dod_sup_hist[12], dod_childmove_viol);
    }
    fprintf(o, "  \"seconds\": {\"main\": %.3f, \"extras\": %.3f, \"total\": %.3f}\n", tmain, tex, tall);
    fprintf(o, "}\n");
    fclose(o);

    printf("stage2 part %d/%d%s%s: processed %ld g2=%d g0=%d g1=%d fails(san %ld ord %ld g %ld sup %ld) "
           "max12 %d..%d sup13 %d..%d%s [%.1fs]\n",
           part, nparts, stride > 1 ? " stride" : "", limit > 0 ? " probe" : "",
           processed, gh[2], gh[0], gh[1], fails_sanity, fails_order, fails_g, fails_sup,
           min_max12, max_max12, min_sup, max_sup,
           (part == 0 && limit <= 0) ? " (extras done)" : "", tall);
    free(caps); free(d11); free(masks); free(capbit); free(d11bit);
    return 0;
}
