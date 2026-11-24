/* grundy_rec.c -- second, structurally different full Grundy/misere
 * computation: recursive memoized mex directly from the board file, no
 * precomputed safe-set dump, no level ordering.  Maintains |S cap L| on the
 * recursion stack and memoizes (mask -> encoded value) in an open-addressing
 * table.  Also re-derives the safe-set and maximal-set counts independently.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAXV 64
#define MAXB 256
#define MAXS 40

static int n, nb;
static uint32_t linemask[MAXB];
static uint32_t full;
static int cnt[MAXB];
static int tightpt[MAXV];
static int lpts[MAXB][MAXV];
static int nlpts[MAXB];
static int pl[MAXV][32];
static int npl[MAXV];

static uint64_t sizeCnt[MAXS];
static long long gdist[MAXS][16], mdist[MAXS][2];
static long long gtot[16];
static uint64_t total, maxseen;

#define ENC(g, mv) ((uint8_t)((g) | ((mv) << 4)))
#define DEC_G(v) ((v) & 15)
#define DEC_M(v) (((v) >> 4) & 1)

static uint32_t *keys;
static uint8_t *vals;
static uint32_t hmask;
static uint32_t hused;

static void die(const char *s) { fprintf(stderr, "FATAL: %s\n", s); exit(2); }

static inline uint32_t hsh(uint32_t x) {
    x ^= x >> 16; x *= 0x7feb352du; x ^= x >> 15; x *= 0x846ca68bu; x ^= x >> 16;
    return x;
}
static inline int tget(uint32_t key) {
    uint32_t i = hsh(key) & hmask;
    while (keys[i]) {
        if (keys[i] == key) return vals[i];
        i = (i + 1) & hmask;
    }
    return -1;
}
static inline void tput(uint32_t key, uint8_t val) {
    uint32_t i = hsh(key) & hmask;
    while (keys[i]) {
        if (keys[i] == key) { vals[i] = val; return; }
        i = (i + 1) & hmask;
    }
    keys[i] = key;
    vals[i] = val;
    hused++;
}

static uint8_t grundy(uint32_t S, int size) {
    int cached = tget(S);
    if (cached >= 0) return (uint8_t)cached;

    unsigned mark = 0;
    int nch = 0, anyL = 0;
    uint32_t rest = full & ~S;
    while (rest) {
        int p = __builtin_ctz(rest);
        rest &= rest - 1;
        if (tightpt[p]) continue;
        /* add p */
        for (int j = 0; j < npl[p]; j++) {
            int L = pl[p][j];
            if (++cnt[L] == 3)
                for (int k = 0; k < nlpts[L]; k++) tightpt[lpts[L][k]]++;
        }
        uint8_t v = grundy(S | (1u << p), size + 1);
        /* remove p */
        for (int j = 0; j < npl[p]; j++) {
            int L = pl[p][j];
            if (--cnt[L] == 2)
                for (int k = 0; k < nlpts[L]; k++) tightpt[lpts[L][k]]--;
        }
        mark |= 1u << DEC_G(v);
        nch++;
        if (!DEC_M(v)) anyL = 1;
    }
    int g = 0;
    while (mark & (1u << g)) g++;
    if (g > 15) die("grundy too large");
    int mv = (nch == 0) ? 1 : anyL;
    uint8_t val = ENC(g, mv);

    /* bookkeeping exactly once per state */
    sizeCnt[size]++;
    total++;
    if ((uint64_t)size > maxseen) maxseen = (uint64_t)size;
    gdist[size][g]++;
    mdist[size][mv]++;
    gtot[g]++;
    if (hused * 10 >= (hmask + 1u) * 7u) die("hash table too full");
    tput(S, val);
    return val;
}

int main(int argc, char **argv) {
    const char *board = argc > 1 ? argv[1] : "board.txt";
    int log_slots = argc > 2 ? atoi(argv[2]) : 24;

    FILE *f = fopen(board, "r");
    if (!f) { perror(board); return 2; }
    if (fscanf(f, "%d %d", &n, &nb) != 2) die("bad header");
    if (n < 0 || n > MAXV || nb < 0 || nb > MAXB) die("board too large");
    for (int i = 0; i < nb; i++) {
        int k;
        if (fscanf(f, "%d", &k) != 1) die("bad line header");
        nlpts[i] = k;
        for (int j = 0; j < k; j++) {
            int p;
            if (fscanf(f, "%d", &p) != 1) die("bad point");
            lpts[i][j] = p;
        }
    }
    fclose(f);
    for (int i = 0; i < nb; i++) {
        linemask[i] = 0;
        for (int j = 0; j < nlpts[i]; j++) {
            int p = lpts[i][j];
            linemask[i] |= (1u << p);
            if (npl[p] >= 32) die("too many lines");
            pl[p][npl[p]++] = i;
        }
    }
    full = (n >= 32) ? 0xFFFFFFFFu : ((1u << n) - 1);

    uint64_t slots = 1ull << log_slots;
    keys = (uint32_t *)calloc((size_t)slots, sizeof(uint32_t));
    vals = (uint8_t *)calloc((size_t)slots, sizeof(uint8_t));
    if (!keys || !vals) die("oom");
    hmask = (uint32_t)(slots - 1);

    uint8_t root = grundy(0u, 0);

    printf("REC_SAFE %llu\n", (unsigned long long)total);
    printf("REC_MAXSIZE %llu\n", (unsigned long long)maxseen);
    for (int s = 0; s <= (int)maxseen && s < MAXS; s++)
        printf("REC_SIZE %d %llu\n", s, (unsigned long long)sizeCnt[s]);
    for (int g = 0; g < 16; g++)
        if (gtot[g]) printf("REC_GRUNDY %d %lld\n", g, gtot[g]);
    printf("REC_ROOTS %d %d\n", DEC_G(root), DEC_M(root));
    printf("REC_HASH_USED %u SLOTS %llu\n", hused, (unsigned long long)slots);
    for (int s = 0; s <= (int)maxseen && s < MAXS; s++) {
        printf("REC_SIZE_GRUNDY %d", s);
        for (int g = 0; g < 16; g++) printf(" %lld", gdist[s][g]);
        printf("\n");
        printf("REC_SIZE_MISERE %d %lld %lld\n", s, mdist[s][0], mdist[s][1]);
    }
    return 0;
}
