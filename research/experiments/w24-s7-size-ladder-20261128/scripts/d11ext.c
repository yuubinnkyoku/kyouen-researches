/* Exhaustive audit of the maximal extensions of every dodecad 11-subset
 * (d11) of W_24 at s=7.
 *
 * K1349 claims (from samples) that every d11 has maximal-extension profile
 * {13:12}: exactly 12 maximal 13-cap extensions and NO maximal 12-cap
 * extension.  The 13-cap side is fully verified by census.c (uniform 12).
 * Here we verify the "no maximal 12-cap extension" side for all 30,912
 * d11s: every 12-cap extension S+{x} of a d11 is still contained in some
 * maximal 13-cap (i.e. non-maximal).
 *
 * Build: gcc -O2 -o d11ext d11ext.c
 * Run:   ./d11ext <board_w24.txt>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n = 24, nb;
static uint32_t blocks[1024];
static int pcnt[32][1024], npc[32];
static uint32_t allmask;
static uint8_t *tf12;   /* bit set iff mask is a 12-subset of some maximal 13-cap */

static int ok_add(uint32_t mask, int p) {
    for (int i = 0; i < npc[p]; i++) {
        int b = pcnt[p][i];
        if (__builtin_popcount(mask & blocks[b]) >= 7) return 0;
    }
    return 1;
}

static long long ext12_hist[32], max12_hist[32];
static long long nd11, total_ext, total_max12;

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

    tf12 = calloc(1u << 24, 1);
    if (!tf12) { fprintf(stderr, "OOM\n"); return 2; }
    int ncaps = 0;
    for (uint32_t m = 0; m <= allmask; m++) {
        if (__builtin_popcount(m) != 13) continue;
        int cap = 1;
        for (int i = 0; i < nb; i++) if ((m & blocks[i]) == blocks[i]) { cap = 0; break; }
        if (!cap) continue;
        ncaps++;
        for (uint32_t s = m; s; s = (s - 1) & m)
            if (__builtin_popcount(s) == 12) tf12[s] = 1;
    }
    if (ncaps != 30912) { fprintf(stderr, "FATAL 13caps\n"); return 3; }

    for (int i = 0; i < ndodec; i++) {
        uint32_t D = dodec[i];
        for (int drop = 0; drop < 12; drop++) {
            /* one 11-subset per dropped point; dedup via scan is unnecessary:
             * distinct dodecads share <= 8 points so 11-subsets are unique */
            int pts[12], c = 0;
            for (int p = 0; p < n; p++) if (D & (1u << p)) pts[c++] = p;
            uint32_t S = 0;
            for (int j = 0; j < 12; j++) if (j != drop) S |= 1u << pts[j];
            int ext12 = 0, max12 = 0;
            for (int p = 0; p < n; p++) {
                if (S & (1u << p)) continue;
                if (!ok_add(S, p)) continue;
                uint32_t M = S | (1u << p);
                ext12++;
                if (!tf12[M]) max12++;
            }
            ext12_hist[ext12]++;
            max12_hist[max12]++;
            nd11++;
            total_ext += ext12;
            total_max12 += max12;
        }
    }
    if (nd11 != 30912) { fprintf(stderr, "FATAL d11 count %lld\n", nd11); return 3; }

    FILE *fo = fopen("output/d11ext.json", "w");
    fprintf(fo, "{\n");
    fprintf(fo, "  \"board\": \"%s\",\n", argv[1]);
    fprintf(fo, "  \"d11_count\": %lld,\n", nd11);
    fprintf(fo, "  \"cap12_extensions_per_d11_hist\": {");
    int first = 1;
    for (int v = 0; v < 32; v++) if (ext12_hist[v]) { fprintf(fo, "%s\"%d\": %lld", first ? "" : ", ", v, ext12_hist[v]); first = 0; }
    fprintf(fo, "},\n");
    fprintf(fo, "  \"maximal12_extensions_per_d11_hist\": {");
    first = 1;
    for (int v = 0; v < 32; v++) if (max12_hist[v]) { fprintf(fo, "%s\"%d\": %lld", first ? "" : ", ", v, max12_hist[v]); first = 0; }
    fprintf(fo, "},\n");
    fprintf(fo, "  \"total_cap12_extensions\": %lld,\n", total_ext);
    fprintf(fo, "  \"total_maximal12_extensions\": %lld,\n", total_max12);
    fprintf(fo, "  \"all_extensions_nonmaximal\": %s\n", total_max12 == 0 ? "true" : "false");
    fprintf(fo, "}\n");
    fclose(fo);
    fprintf(stderr, "d11ext written (nd11=%lld total_ext=%lld total_max12=%lld)\n", nd11, total_ext, total_max12);
    return 0;
}
