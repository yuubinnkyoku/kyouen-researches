/* Full DP verification of the size ladder of the W_24 s=7 game against the
 * dodecad / maximal-13-cap subset census.
 *
 * Part A (exhaustive): compute the exact Grundy value of EVERY cap of size
 *   9..13 (6,661,168 positions, memoized bottom-up via recursion from the
 *   9-caps) and cross-tabulate (size, dodecad-subset flags, 13-cap-subset
 *   flags, Grundy).  This verifies the correspondence table at k>=9 fully,
 *   including the corrected k=12 layer (dodecads are non-maximal, G=1).
 *
 * Part B (samples): random caps of sizes 1..8 (parity layers) and random
 *   elements of the structural classes at k=6,7,8 (octad-derived subsets,
 *   dodecad subsets, residual non-dodecad classes).
 *
 * Single-threaded (shared-machine load cap: max 4 workers).
 *
 * Build: gcc -O2 -o dpverify dpverify.c
 * Run:   ./dpverify <board_w24.txt> <seed>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n = 24, nb;
static uint32_t blocks[1024];
static int pcnt[32][1024], npc[32];
static uint32_t allmask;

#define HSIZE (1u << 23)
static uint32_t *keys;
static int8_t *vals;

static int8_t grundy(uint32_t mask);

static int memo_get(uint32_t mask, int8_t *out) {
    uint32_t h = (mask * 2654435761u) >> 9;
    for (int i = 0; i < 256; i++) {
        uint32_t idx = (h + i) & (HSIZE - 1);
        uint32_t k = keys[idx];
        if (k == mask + 1) { *out = vals[idx]; return 1; }
        if (k == 0) return 0;
    }
    return 0;
}
static void memo_put(uint32_t mask, int8_t v) {
    uint32_t h = (mask * 2654435761u) >> 9;
    for (int i = 0; i < 256; i++) {
        uint32_t idx = (h + i) & (HSIZE - 1);
        if (keys[idx] == 0 || keys[idx] == mask + 1) { keys[idx] = mask + 1; vals[idx] = v; return; }
    }
}
static int ok_add(uint32_t mask, int p) {
    for (int i = 0; i < npc[p]; i++) {
        int b = pcnt[p][i];
        if (__builtin_popcount(mask & blocks[b]) >= 7) return 0;
    }
    return 1;
}
static int8_t grundy(uint32_t mask) {
    int8_t v;
    if (memo_get(mask, &v)) return v;
    int seen[8]; memset(seen, 0, sizeof seen);
    for (int p = 0; p < n; p++) {
        if (mask & (1u << p)) continue;
        if (!ok_add(mask, p)) continue;
        int8_t g = grundy(mask | (1u << p));
        if (g < 8) seen[g] = 1;
    }
    int mex = 0;
    while (mex < 8 && seen[mex]) mex++;
    memo_put(mask, (int8_t)mex);
    return (int8_t)mex;
}
static int is_cap(uint32_t m) {
    for (int i = 0; i < nb; i++)
        if ((m & blocks[i]) == blocks[i]) return 0;
    return 1;
}

/* flags over all masks: bit0 d9, bit1 d10, bit2 d11, bit3 d12, bit4 d8;
 * tf: bit0 t9, bit1 t10, bit2 t11, bit3 t12, bit4 t13 */
static uint8_t *df, *tf;
static uint32_t caps_list[40000];

static uint32_t rnd(void);

static uint32_t rand_k_subset_of(uint32_t D, int k) {
    int pts[12], c = 0;
    for (int p = 0; p < n; p++) if (D & (1u << p)) pts[c++] = p;
    for (int i = 0; i < k; i++) {
        int j = i + (int)(rnd() % (uint32_t)(c - i));
        int t = pts[i]; pts[i] = pts[j]; pts[j] = t;
    }
    uint32_t m = 0;
    for (int i = 0; i < k; i++) m |= 1u << pts[i];
    return m;
}

static uint32_t rngstate, seed0;
static uint32_t rnd(void) {
    uint32_t x = rngstate;
    x ^= x << 13; x ^= x >> 17; x ^= x << 5;
    rngstate = x;
    return x;
}
static uint32_t rand_k_subset(int k) {
    int perm[24];
    for (int i = 0; i < n; i++) perm[i] = i;
    uint32_t m = 0;
    for (int i = 0; i < k; i++) {
        int j = i + (int)(rnd() % (uint32_t)(n - i));
        int t = perm[i]; perm[i] = perm[j]; perm[j] = t;
        m |= 1u << perm[i];
    }
    return m;
}

static long long gk[14][8];            /* exhaustive (k, G) tally, k = 9..13 */
static long long xtab[14][8][8];       /* exhaustive (k, class, G): class 0=D, 1=T\D, 2=neither */
static long long parity_hist[9][8];    /* sampled parity layers */
static long long class_hist[8][8];     /* sampled structural classes k<=8 */
static long long gtotal[14];

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
    rngstate = argc > 2 ? (uint32_t)strtoul(argv[2], NULL, 10) : 20261128u;
    if (!rngstate) rngstate = 20261128u;
    seed0 = rngstate;

    /* Golay span -> dodecads */
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
    static uint32_t dodec[4096]; int ndodec = 0;
    for (int i = 0; i < nspan; i++) if (__builtin_popcount(span[i]) == 12) dodec[ndodec++] = span[i];
    if (ndodec != 2576) { fprintf(stderr, "FATAL dodecads\n"); return 3; }

    df = calloc(1u << 24, 1);
    tf = calloc(1u << 24, 1);
    keys = calloc(HSIZE, sizeof(uint32_t));
    vals = malloc(HSIZE);
    if (!df || !tf || !keys || !vals) { fprintf(stderr, "OOM\n"); return 2; }

    for (int i = 0; i < ndodec; i++) {
        uint32_t D = dodec[i];
        df[D] |= 8;                       /* d12 */
        for (uint32_t s = D; s; s = (s - 1) & D) {
            int pcs = __builtin_popcount(s);
            if (pcs == 8) df[s] |= 16;
            else if (pcs == 9) df[s] |= 1;
            else if (pcs == 10) df[s] |= 2;
            else if (pcs == 11) df[s] |= 4;
        }
    }
    /* 13-caps: enumerate + flag their 9..13-subsets */
    int ncaps = 0;
    for (uint32_t m = 0; m <= allmask; m++) {
        if (__builtin_popcount(m) != 13) continue;
        int cap = 1;
        for (int i = 0; i < nb; i++) if ((m & blocks[i]) == blocks[i]) { cap = 0; break; }
        if (cap) {
            caps_list[ncaps++] = m;
            tf[m] |= 16;
            for (uint32_t s = m; s; s = (s - 1) & m) {
                int pcs = __builtin_popcount(s);
                if (pcs == 9) tf[s] |= 1;
                else if (pcs == 10) tf[s] |= 2;
                else if (pcs == 11) tf[s] |= 4;
                else if (pcs == 12) tf[s] |= 8;
            }
        }
    }
    if (ncaps != 30912) { fprintf(stderr, "FATAL 13caps %d\n", ncaps); return 3; }
    fprintf(stderr, "flags marked (dodecads %d, 13caps %d)\n", ndodec, ncaps);

    /* Part A: exhaustive Grundy of every cap of size 9..13.
     * First pass: size 9 (recursion computes the whole subtree). */
    for (uint32_t m = 0; m <= allmask; m++) {
        if (__builtin_popcount(m) != 9) continue;
        if (!is_cap(m)) continue;
        int8_t g = grundy(m);
        gk[9][g]++; gtotal[9]++;
        int cls = (df[m] & 1) ? 0 : ((tf[m] & 1) ? 1 : 2);
        xtab[9][cls][g]++;
    }
    fprintf(stderr, "size 9 done\n");
    for (int k = 10; k <= 13; k++) {
        for (uint32_t m = 0; m <= allmask; m++) {
            if (__builtin_popcount(m) != k) continue;
            if (!is_cap(m)) continue;
            int8_t g = grundy(m);
            gk[k][g]++; gtotal[k]++;
            int cls;
            if (k <= 12) cls = ((df[m] >> (k - 9)) & 1) ? 0 : ((tf[m] & (k == 12 ? 8 : (1 << (k - 9)))) ? 1 : 2);
            else cls = (tf[m] & 16) ? 1 : 2;
            xtab[k][cls][g]++;
        }
        fprintf(stderr, "size %d done\n", k);
    }

    /* Part B: parity samples k=1..8 */
    for (int k = 1; k <= 8; k++) {
        int done = 0;
        while (done < 100) {
            uint32_t m = rand_k_subset(k);
            if (!is_cap(m)) continue;
            int8_t g = grundy(m);
            parity_hist[k][g]++;
            done++;
        }
    }
    /* structural classes at k = 6, 7, 8 */
    int done6a = 0, done6b = 0, done7 = 0, done8d = 0, done8r = 0;
    while (done6a < 50 || done6b < 50 || done7 < 50 || done8d < 50 || done8r < 50) {
        int which = (int)(rnd() % 5);
        uint32_t m; int slot;
        if (which == 0 && done6a < 50) {          /* 6-subset inside an octad */
            uint32_t o = blocks[rnd() % nb];
            m = o; /* drop 2 points */
            int pts[8], c = 0;
            for (int p = 0; p < n; p++) if (o & (1u << p)) pts[c++] = p;
            for (int t = 0; t < 2; t++) {
                int j = (int)(rnd() % (uint32_t)(c - t));
                int tmp = pts[t]; pts[t] = pts[t + j]; pts[t + j] = tmp;
            }
            m = 0; for (int t = 2; t < 8; t++) m |= 1u << pts[t];
            slot = 0; done6a++;
        } else if (which == 1 && done6b < 50) {   /* 6-subset in no octad */
            do { m = rand_k_subset(6); } while (0);
            int inoct = 0;
            for (int i = 0; i < nb; i++) if ((__builtin_popcount(m & blocks[i]) == 6)) { inoct = 1; break; }
            if (inoct) continue;
            slot = 1; done6b++;
        } else if (which == 2 && done7 < 50) {    /* 7 points of an octad */
            uint32_t o = blocks[rnd() % nb];
            int pts[8], c = 0;
            for (int p = 0; p < n; p++) if (o & (1u << p)) pts[c++] = p;
            int j = (int)(rnd() % 8);
            m = o & ~(1u << pts[j]);
            slot = 2; done7++;
        } else if (which == 3 && done8d < 50) {   /* dodecad 8-subset */
            uint32_t D = dodec[rnd() % ndodec];
            m = rand_k_subset_of(D, 8);
            slot = 3; done8d++;
        } else if (which == 4 && done8r < 50) {   /* 8-cap with 7 points of an octad, in no dodecad */
            uint32_t o = blocks[rnd() % nb];
            int pts[8], c = 0;
            for (int p = 0; p < n; p++) if (o & (1u << p)) pts[c++] = p;
            int j = (int)(rnd() % 8);
            int drop = pts[j];
            int q;
            do { q = (int)(rnd() % n); } while (o & (1u << q));
            m = (o & ~(1u << drop)) | (1u << q);
            if (!is_cap(m)) continue;
            if (df[m] & 16) continue;             /* must be a non-dodecad 8-cap */
            slot = 4; done8r++;
        } else continue;
        int8_t g = grundy(m);
        class_hist[slot][g]++;
    }

    /* output */
    FILE *fo = fopen("output/dpverify_raw.json", "w");
    fprintf(fo, "{\n");
    fprintf(fo, "  \"board\": \"%s\", \"seed\": %u,\n", argv[1], seed0);
    fprintf(fo, "  \"exhaustive\": {\n");
    fprintf(fo, "    \"note\": \"exact Grundy of every cap of size 9-13 (6661168 positions), classes: D=dodecad k-subset, Tonly=13cap k-subset not dodecad, neither\",\n");
    fprintf(fo, "    \"per_k\": [\n");
    for (int k = 9; k <= 13; k++) {
        fprintf(fo, "      {\"k\": %d, \"caps\": %lld, \"g_hist\": {", k, gtotal[k]);
        int first = 1;
        for (int g = 0; g < 8; g++) if (gk[k][g]) { fprintf(fo, "%s\"%d\": %lld", first ? "" : ", ", g, gk[k][g]); first = 0; }
        fprintf(fo, "}, \"classes\": [");
        const char *cn[3] = {"D", "Tonly", "neither"};
        for (int c = 0; c < 3; c++) {
            fprintf(fo, "%s{\"class\": \"%s\", \"n\": ", c ? ", " : "", cn[c]);
            long long tot = 0; for (int g = 0; g < 8; g++) tot += xtab[k][c][g];
            fprintf(fo, "%lld, \"g_hist\": {", tot);
            first = 1;
            for (int g = 0; g < 8; g++) if (xtab[k][c][g]) { fprintf(fo, "%s\"%d\": %lld", first ? "" : ", ", g, xtab[k][c][g]); first = 0; }
            fprintf(fo, "}}");
        }
        fprintf(fo, "]}%s\n", k < 13 ? "," : "");
    }
    fprintf(fo, "    ]\n  },\n");
    fprintf(fo, "  \"parity_samples\": [");
    for (int k = 1; k <= 8; k++) {
        fprintf(fo, "%s{\"k\": %d, \"n\": 100, \"g_hist\": {", k > 1 ? ", " : "", k);
        int first = 1;
        for (int g = 0; g < 8; g++) if (parity_hist[k][g]) { fprintf(fo, "%s\"%d\": %lld", first ? "" : ", ", g, parity_hist[k][g]); first = 0; }
        fprintf(fo, "}}");
    }
    fprintf(fo, "],\n");
    fprintf(fo, "  \"class_samples\": [");
    {
        const char *names[5] = {"k6_in_octad", "k6_no_octad", "k7_seven_of_octad", "k8_dodecad_subset", "k8_seven_of_octad_plus_one"};
        int ns[5] = {50, 50, 50, 50, 50};
        for (int i = 0; i < 5; i++) {
            fprintf(fo, "%s{\"class\": \"%s\", \"n\": %d, \"g_hist\": {", i ? ", " : "", names[i], ns[i]);
            int first = 1;
            for (int g = 0; g < 8; g++) if (class_hist[i][g]) { fprintf(fo, "%s\"%d\": %lld", first ? "" : ", ", g, class_hist[i][g]); first = 0; }
            fprintf(fo, "}}");
        }
    }
    fprintf(fo, "]\n}\n");
    fclose(fo);
    fprintf(stderr, "dpverify written\n");
    return 0;
}
