/* enum_safe.c -- independent enumeration of all safe sets for the
 * "at most 3 points on every line" game on the board given in a file.
 *
 * Board format: first line "<n> <b>", then b lines "<k> p1 ... pk".
 *
 * Algorithm: DFS over safe sets in increasing point order.  `cnt[L]` is
 * |S cap L|, `tightpt[p]` is the number of tight lines (cnt==3) through p.
 * A point p is addable iff p not in S and tightpt[p]==0.  Every safe set is
 * visited exactly once (its points added in increasing order), and every
 * prefix of a safe set is safe, so the DFS is complete.
 *
 * For each size we record every safe mask and its full addable-point mask
 * (all legal moves, not only those >= start), plus counts of safe sets and
 * of maximal safe sets (addable mask == 0).
 *
 * Outputs a text summary on stdout and a binary dump "safesets.bin".
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAXV 64
#define MAXB 256
#define MAXS 40

static int n, nb, maxseen;
static uint32_t linemask[MAXV];
static int lpts[MAXB][MAXV];
static int nlpts[MAXB];
static int pl[MAXV][32];
static int npl[MAXV];
static int cnt[MAXB];
static int tightpt[MAXV];
static uint32_t full;

static uint64_t sizeCnt[MAXS], maxCnt[MAXS], total;

typedef struct { uint32_t *m; uint32_t *a; uint64_t k, cap; } Lev;
static Lev lev[MAXS];

static void die(const char *s) { fprintf(stderr, "FATAL: %s\n", s); exit(2); }

static void push(int s, uint32_t m, uint32_t a) {
    Lev *L = &lev[s];
    if (L->k == L->cap) {
        uint64_t nc = L->cap ? L->cap * 2 : 8192;
        uint32_t *nm = (uint32_t *)realloc(L->m, (size_t)nc * sizeof(uint32_t));
        uint32_t *na = (uint32_t *)realloc(L->a, (size_t)nc * sizeof(uint32_t));
        if (!nm || !na) die("oom");
        L->m = nm; L->a = na; L->cap = nc;
    }
    L->m[L->k] = m;
    L->a[L->k] = a;
    L->k++;
}

static void dfs(uint32_t S, int start, int size) {
    if (size >= MAXS) die("size overflow");
    uint32_t add = 0;
    uint32_t rest = full & ~S;
    while (rest) {
        int p = __builtin_ctz(rest);
        rest &= rest - 1;
        if (!tightpt[p]) add |= (1u << p);
    }
    push(size, S, add);
    sizeCnt[size]++;
    total++;
    if (size > maxseen) maxseen = size;
    if (!add) {                 /* no legal move: maximal */
        maxCnt[size]++;
        return;
    }
    uint32_t cand = add & (~0u << start);
    while (cand) {
        int p = __builtin_ctz(cand);
        cand &= cand - 1;
        for (int j = 0; j < npl[p]; j++) {
            int L = pl[p][j];
            if (++cnt[L] == 3)
                for (int k = 0; k < nlpts[L]; k++) tightpt[lpts[L][k]]++;
        }
        dfs(S | (1u << p), p + 1, size + 1);
        for (int j = 0; j < npl[p]; j++) {
            int L = pl[p][j];
            if (--cnt[L] == 2)
                for (int k = 0; k < nlpts[L]; k++) tightpt[lpts[L][k]]--;
        }
    }
}

int main(int argc, char **argv) {
    const char *board = argc > 1 ? argv[1] : "board.txt";
    const char *dump = argc > 2 ? argv[2] : "safesets.bin";

    FILE *f = fopen(board, "r");
    if (!f) { perror(board); return 2; }
    if (fscanf(f, "%d %d", &n, &nb) != 2) die("bad header");
    if (n < 0 || n > MAXV || nb < 0 || nb > MAXB) die("board too large");
    for (int i = 0; i < nb; i++) {
        int k;
        if (fscanf(f, "%d", &k) != 1) die("bad line header");
        if (k < 0 || k > MAXV) die("bad line size");
        nlpts[i] = k;
        for (int j = 0; j < k; j++) {
            int p;
            if (fscanf(f, "%d", &p) != 1) die("bad point");
            if (p < 0 || p >= n) die("point out of range");
            lpts[i][j] = p;
        }
    }
    fclose(f);

    /* build masks and point->line incidence */
    for (int i = 0; i < nb; i++) {
        linemask[i] = 0;
        for (int j = 0; j < nlpts[i]; j++) {
            int p = lpts[i][j];
            linemask[i] |= (1u << p);
            if (npl[p] >= 32) die("too many lines through a point");
            pl[p][npl[p]++] = i;
        }
    }
    full = (n >= 32) ? 0xFFFFFFFFu : ((1u << n) - 1);

    printf("BOARD %s\n", board);
    printf("N %d B %d FULL %08X\n", n, nb, full);
    for (int i = 0; i < nb; i++) printf("LINE %d SIZE %d MASK %08X\n", i, nlpts[i], linemask[i]);

    dfs(0, 0, 0);

    printf("SAFE %llu\n", (unsigned long long)total);
    printf("MAXSIZE %d\n", maxseen);
    for (int s = 0; s <= maxseen; s++)
        printf("SIZE %d %llu %llu\n", s,
               (unsigned long long)sizeCnt[s], (unsigned long long)maxCnt[s]);
    for (int s = 0; s <= maxseen; s++)
        if (lev[s].k != sizeCnt[s]) die("internal count mismatch");

    /* binary dump */
    FILE *g = fopen(dump, "wb");
    if (!g) { perror(dump); return 2; }
    fwrite("PG2Q5S3", 1, 8, g);
    uint32_t hdr[3] = {(uint32_t)n, (uint32_t)nb, (uint32_t)maxseen};
    fwrite(hdr, sizeof(uint32_t), 3, g);
    fwrite(sizeCnt, sizeof(uint64_t), (size_t)maxseen + 1, g);
    fwrite(maxCnt, sizeof(uint64_t), (size_t)maxseen + 1, g);
    for (int s = 0; s <= maxseen; s++) {
        fwrite(lev[s].m, sizeof(uint32_t), (size_t)lev[s].k, g);
        fwrite(lev[s].a, sizeof(uint32_t), (size_t)lev[s].k, g);
    }
    fclose(g);
    printf("DUMP %s\n", dump);
    return 0;
}
