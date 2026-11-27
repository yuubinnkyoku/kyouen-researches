
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n = 24, nb;
static uint32_t blocks[1024];
static int pc[32][1024], npc[32];
static uint32_t allmask;
static int g_count[64];

/* memo hash: key uint32 (0 = empty), value int8 */
#define HSIZE (1u<<23)
static uint32_t *keys;
static int8_t *vals;

static int8_t grundy(uint32_t mask, int depth);

static int memo_get(uint32_t mask, int8_t *out) {
    uint32_t h = (mask * 2654435761u) >> 9; /* HSIZE=2^23 -> shift 9 */
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
    uint32_t bit = 1u << p;
    for (int i = 0; i < npc[p]; i++) {
        int b = pc[p][i];
        if (__builtin_popcount(mask & blocks[b]) >= 7) return 0;
    }
    return 1;
}
static int8_t grundy(uint32_t mask, int depth) {
    int8_t v;
    if (memo_get(mask, &v)) return v;
    int seen[32]; memset(seen, 0, sizeof seen);
    for (int p = 0; p < n; p++) {
        if (mask & (1u << p)) continue;
        if (!ok_add(mask, p)) continue;
        int8_t g = grundy(mask | (1u << p), depth + 1);
        seen[g] = 1;
    }
    int mex = 0;
    while (mex < 31 && seen[mex]) mex++;
    memo_put(mask, (int8_t)mex);
    return (int8_t)mex;
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
            if (blocks[i] & (1u << p)) pc[p][npc[p]++] = i;
    allmask = (1u << n) - 1;
    keys = calloc(HSIZE, sizeof(uint32_t));
    vals = malloc(HSIZE);
    if (!keys || !vals) { fprintf(stderr, "OOM\n"); return 2; }

    /* build Golay span from octads */
    uint32_t piv[32]; memset(piv, 0, sizeof piv);
    for (int i = 0; i < nb; i++) {
        uint32_t x = blocks[i];
        while (x) { int hb = 31 - __builtin_clz(x); if (piv[hb]) x ^= piv[hb]; else { piv[hb] = x; break; } }
    }
    uint32_t basis[32]; int nbasis = 0;
    for (int i = 0; i < 32; i++) if (piv[i]) basis[nbasis++] = piv[i];
    fprintf(stderr, "board n=%d nb=%d basis=%d\n", n, nb, nbasis);

    /* enumerate span by recursion */
    uint32_t *span = malloc(4096 * sizeof(uint32_t)); int nspan = 0;
    /* iterative doubling */
    span[0] = 0; nspan = 1;
    for (int i = 0; i < nbasis; i++) {
        int cur = nspan;
        for (int j = 0; j < cur; j++) span[nspan++] = span[j] ^ basis[i];
    }
    fprintf(stderr, "span %d\n", nspan);
    int dodecads = 0;
    /* for each weight-12 */
    for (int i = 0; i < nspan; i++) {
        uint32_t D = span[i];
        if (__builtin_popcount(D) != 12) continue;
        dodecads++;
        int pts[12], m = 0;
        for (int p = 0; p < n; p++) if (D & (1u << p)) pts[m++] = p;
        /* 10-subsets */
        for (int a = 0; a < 12; a++) for (int b = a+1; b < 12; b++) for (int c = b+1; c < 12; c++)
        for (int d = c+1; d < 12; d++) for (int e = d+1; e < 12; e++) for (int f = e+1; f < 12; f++)
        for (int g = f+1; g < 12; g++) for (int h = g+1; h < 12; h++) for (int k = h+1; k < 12; k++)
        for (int l = k+1; l < 12; l++) {
            uint32_t Z = (1u<<pts[a])|(1u<<pts[b])|(1u<<pts[c])|(1u<<pts[d])|(1u<<pts[e])|(1u<<pts[f])|(1u<<pts[g])|(1u<<pts[h])|(1u<<pts[k])|(1u<<pts[l]);
            int8_t gv = grundy(Z, 0);
            g_count[32 + gv]++;  /* offset 32 for 10-subsets */
        }
        if (dodecads % 256 == 0) fprintf(stderr, "dodecads %d\n", dodecads);
    }
    printf("dodecads %d\n", dodecads);
    printf("10subsets: ");
    for (int g = 0; g < 10; g++) if (g_count[32+g]) printf("G%d=%d ", g, g_count[32+g]);
    printf("\n9subsets: ");
    for (int g = 0; g < 10; g++) if (g_count[g]) printf("G%d=%d ", g, g_count[g]);
    printf("\n11subsets: ");
    for (int g = 0; g < 10; g++) if (g_count[16+g]) printf("G%d=%d ", g, g_count[16+g]);
    printf("\n");
    return 0;
}
