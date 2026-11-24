/* grundy_level.c -- full Grundy / misere DP from the binary safe-set dump
 * produced by enum_safe.c.  Independent of the repo's C engine.
 *
 * Levels are processed by decreasing size.  For each safe set S of size k
 * the legal children are exactly {S | 1<<p : p in add(S)} and they all live
 * at level k+1, so a hash table of level k+1 (mask -> encoded value) is
 * enough.  Encoded byte: bits0-3 Grundy, bit4 misere win, bits5-6 parity set
 * f(S) (bit p set iff some maximal extension of S has size == p mod 2),
 * bit7 desc2 (some T >= S has Grundy >= 2).
 *
 * Checks K1298 on every position:
 *   f(S) uniform  =>  Grundy(S) == (p - |S|) mod 2
 *   desc2(S) <=> f(S) mixed                                  (violations counted)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAXS 40
#define MAXB 256

typedef struct {
    uint32_t *keys;
    uint8_t *vals;
    uint32_t mask;
    uint32_t used;
} Table;

static void die(const char *s) { fprintf(stderr, "FATAL: %s\n", s); exit(2); }

static inline uint32_t hsh(uint32_t x) {
    x ^= x >> 16; x *= 0x7feb352du; x ^= x >> 15; x *= 0x846ca68bu; x ^= x >> 16;
    return x;
}

static Table tnew(uint64_t cnt) {
    uint64_t slots = 1024;
    while (slots < cnt * 2 + 16) slots <<= 1;
    if (slots > (1ull << 32)) die("table too large");
    Table t;
    t.keys = (uint32_t *)calloc((size_t)slots, sizeof(uint32_t));
    t.vals = (uint8_t *)calloc((size_t)slots, sizeof(uint8_t));
    if (!t.keys || !t.vals) die("oom table");
    t.mask = (uint32_t)(slots - 1);
    t.used = 0;
    return t;
}

static inline void tfree(Table *t) { free(t->keys); free(t->vals); t->keys = NULL; t->vals = NULL; }

static inline void tput(Table *t, uint32_t key, uint8_t val) {
    uint32_t i = hsh(key) & t->mask;
    while (t->keys[i]) {
        if (t->keys[i] == key) { t->vals[i] = val; return; }
        i = (i + 1) & t->mask;
    }
    t->keys[i] = key;
    t->vals[i] = val;
    t->used++;
}

static inline int tget(const Table *t, uint32_t key) {
    uint32_t i = hsh(key) & t->mask;
    while (t->keys[i]) {
        if (t->keys[i] == key) return t->vals[i];
        i = (i + 1) & t->mask;
    }
    return -1;
}

#define ENC(g, mv, f, d2) ((uint8_t)((g) | ((mv) << 4) | ((f) << 5) | ((d2) << 7)))
#define DEC_G(v) ((v) & 15)
#define DEC_M(v) (((v) >> 4) & 1)
#define DEC_F(v) (((v) >> 5) & 3)
#define DEC_D(v) (((v) >> 7) & 1)

static int n, nb, maxsize;
static uint64_t lcnt[MAXS], lmax[MAXS];
static uint32_t *lmask[MAXS];
static uint32_t *ladd[MAXS];
static uint8_t *gval[MAXS];

static long long gdist[MAXS][16], mdist[MAXS][2];
static long long gtot[16], mtot[2];
static long long uniform_checked, uniform_viol;
static long long desc_checked, desc_viol;
static long long misere_checked, misere_viol;

int main(int argc, char **argv) {
    const char *dump = argc > 1 ? argv[1] : "safesets.bin";
    const char *vfile = argc > 2 ? argv[2] : "grundy_values.bin";
    FILE *f = fopen(dump, "rb");
    if (!f) { perror(dump); return 2; }
    char magic[8];
    if (fread(magic, 1, 8, f) != 8 || memcmp(magic, "PG2Q5S3", 8) != 0)
        die("bad dump magic");
    uint32_t hdr[3];
    if (fread(hdr, 4, 3, f) != 3) die("bad header");
    n = (int)hdr[0]; nb = (int)hdr[1]; maxsize = (int)hdr[2];
    if (maxsize >= MAXS) die("maxsize too large");
    if (fread(lcnt, 8, (size_t)maxsize + 1, f) != (size_t)maxsize + 1) die("bad counts");
    if (fread(lmax, 8, (size_t)maxsize + 1, f) != (size_t)maxsize + 1) die("bad maxcounts");
    uint64_t total = 0;
    for (int s = 0; s <= maxsize; s++) {
        lmask[s] = (uint32_t *)malloc((size_t)(lcnt[s] ? lcnt[s] : 1) * 4);
        ladd[s] = (uint32_t *)malloc((size_t)(lcnt[s] ? lcnt[s] : 1) * 4);
        gval[s] = (uint8_t *)malloc((size_t)(lcnt[s] ? lcnt[s] : 1));
        if (!lmask[s] || !ladd[s] || !gval[s]) die("oom dump");
        if (fread(lmask[s], 4, (size_t)lcnt[s], f) != (size_t)lcnt[s]) die("short masks");
        if (fread(ladd[s], 4, (size_t)lcnt[s], f) != (size_t)lcnt[s]) die("short adds");
        total += lcnt[s];
    }
    fclose(f);

    printf("LOADED n=%d b=%d maxsize=%d total=%llu\n", n, nb, maxsize,
           (unsigned long long)total);

    /* level maxsize: every safe set of maximum size is terminal */
    Table tab = tnew(lcnt[maxsize]);
    for (uint64_t i = 0; i < lcnt[maxsize]; i++) {
        if (ladd[maxsize][i] != 0) die("maximal-size set has a legal move");
        uint8_t v0 = ENC(0, 1, 1u << (maxsize & 1), 0);
        tput(&tab, lmask[maxsize][i], v0);
        gval[maxsize][i] = v0;
        gdist[maxsize][0]++;
        mdist[maxsize][1]++;
        gtot[0]++;
        mtot[1]++;
        uniform_checked++;   /* f uniform (only parity maxsize&1), g == (p-k)&1 */
        desc_checked++;
        misere_checked++;    /* g == 0 and mv == 1 here: K1298 misere rule holds */
        if (1 != 1) misere_viol++;
    }

    for (int k = maxsize - 1; k >= 0; k--) {
        Table cur = tnew(lcnt[k]);
        for (uint64_t i = 0; i < lcnt[k]; i++) {
            uint32_t m = lmask[k][i];
            uint32_t av = ladd[k][i];
            unsigned mark = 0;
            int nch = 0, anyL = 0, fs = 0, d2 = 0;
            while (av) {
                int p = __builtin_ctz(av);
                av &= av - 1;
                uint32_t ch = m | (1u << p);
                int v = tget(&tab, ch);
                if (v < 0) { fprintf(stderr, "missing child mask=%08X p=%d\n", m, p); die("child missing"); }
                mark |= 1u << DEC_G(v);
                nch++;
                if (!DEC_M(v)) anyL = 1;
                fs |= DEC_F(v);
                d2 |= DEC_D(v);
            }
            int g = 0;
            while (mark & (1u << g)) g++;
            if (g > 15) die("grundy too large");
            int mv, ff, dd;
            if (nch == 0) {
                mv = 1;                 /* no move: wins under misere */
                ff = 1 << (k & 1);      /* only maximal extension is S itself */
                dd = 0;
            } else {
                mv = anyL;              /* win iff some child loses */
                ff = fs;
                dd = d2 | (g >= 2);
            }
            /* K1298 checks */
            if (ff == 3) {
                desc_checked++;
                if (!dd) desc_viol++;
            } else {
                int p = (ff == 1) ? 0 : 1;
                uniform_checked++;
                if (g != ((p - k) & 1)) uniform_viol++;
                desc_checked++;
                if (dd) desc_viol++;
                misere_checked++;
                if (mv != (g == 0)) misere_viol++;
            }
            gdist[k][g]++;
            mdist[k][mv]++;
            gtot[g]++;
            mtot[mv]++;
            uint8_t val = ENC(g, mv, ff, dd);
            gval[k][i] = val;
            if (k > 0) tput(&cur, m, val);
        }
        tfree(&tab);
        tab = cur;
    }
    tfree(&tab);

    printf("SAFE %llu\n", (unsigned long long)total);
    printf("MAXSIZE %d\n", maxsize);
    for (int s = 0; s <= maxsize; s++)
        printf("SIZE %d %llu %llu\n", s, (unsigned long long)lcnt[s],
               (unsigned long long)lmax[s]);
    for (int g = 0; g < 16; g++)
        if (gtot[g]) printf("GRUNDY %d %lld\n", g, gtot[g]);
    printf("MISERE 0 %lld\n", mtot[0]);
    printf("MISERE 1 %lld\n", mtot[1]);
    printf("ROOT %lld %lld\n", gdist[0][1] ? 1LL : 0LL, (long long)mdist[0][1]);
    printf("K1298_UNIFORM_CHECKED %lld VIOLATIONS %lld\n", uniform_checked, uniform_viol);
    printf("K1298_DESC_CHECKED %lld VIOLATIONS %lld\n", desc_checked, desc_viol);
    printf("K1298_MISERE_CHECKED %lld VIOLATIONS %lld\n", misere_checked, misere_viol);
    for (int s = 0; s <= maxsize; s++) {
        printf("SIZE_GRUNDY %d", s);
        for (int g = 0; g < 16; g++) printf(" %lld", gdist[s][g]);
        printf("\n");
    }
    for (int s = 0; s <= maxsize; s++)
        printf("SIZE_MISERE %d %lld %lld\n", s, mdist[s][0], mdist[s][1]);

    /* dump per-state encoded values (level order, same as safesets.bin) */
    FILE *vf = fopen(vfile, "wb");
    if (!vf) { perror(vfile); return 2; }
    fwrite("PG2G5V1", 1, 8, vf);
    fwrite(hdr, sizeof(uint32_t), 3, vf);
    fwrite(lcnt, sizeof(uint64_t), (size_t)maxsize + 1, vf);
    for (int s = 0; s <= maxsize; s++)
        fwrite(gval[s], 1, (size_t)lcnt[s], vf);
    fclose(vf);
    printf("GVALUES %s\n", vfile);
    return 0;
}
