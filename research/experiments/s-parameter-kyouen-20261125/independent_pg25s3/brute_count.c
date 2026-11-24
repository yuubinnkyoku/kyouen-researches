/* brute_count.c -- completely different independent enumeration:
 * for each size k = 0..12, iterate over *all* C(n,k) subsets (Gosper's hack)
 * and test safety directly by popcounting S against all b line masks.
 * Counts safe sets and maximal safe sets per size.  No DFS, no pruning.
 *
 * A safe set is maximal iff S | (union of all tight lines) == full, where a
 * line is tight when |S cap L| == 3 (then none of its 6 points can be added,
 * because all 3 outside points of L would give 4).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define MAXV 64
#define MAXB 256

static int n, nb;
static uint32_t linemask[MAXB];
static uint32_t full;

static uint64_t comb(int nn, int kk) {
    if (kk < 0 || kk > nn) return 0;
    uint64_t r = 1;
    for (int i = 1; i <= kk; i++) r = r * (uint64_t)(nn - kk + i) / (uint64_t)i;
    return r;
}

int main(int argc, char **argv) {
    const char *board = argc > 1 ? argv[1] : "board.txt";
    int maxk = argc > 2 ? atoi(argv[2]) : 12;

    FILE *f = fopen(board, "r");
    if (!f) { perror(board); return 2; }
    if (fscanf(f, "%d %d", &n, &nb) != 2) return 2;
    if (n > MAXV || nb > MAXB) return 2;
    for (int i = 0; i < nb; i++) {
        int k;
        if (fscanf(f, "%d", &k) != 1) return 2;
        uint32_t m = 0;
        for (int j = 0; j < k; j++) {
            int p;
            if (fscanf(f, "%d", &p) != 1) return 2;
            m |= (1u << p);
        }
        linemask[i] = m;
    }
    fclose(f);
    full = (n >= 32) ? 0xFFFFFFFFu : ((1u << n) - 1);

    uint64_t *safe = (uint64_t *)calloc((size_t)maxk + 2, sizeof(uint64_t));
    uint64_t *maxi = (uint64_t *)calloc((size_t)maxk + 2, sizeof(uint64_t));
    if (!safe || !maxi) return 2;

    unsigned long long tested = 0;
    for (int k = 0; k <= maxk && k <= n; k++) {
        uint64_t tot = comb(n, k);
        uint32_t x = (k == 0) ? 0u : (uint32_t)((1ull << k) - 1ull);
        for (uint64_t i = 0; i < tot; i++) {
            uint32_t tight = 0;
            int ok = 1;
            for (int L = 0; L < nb; L++) {
                int c = __builtin_popcount(x & linemask[L]);
                if (c > 3) { ok = 0; break; }
                if (c == 3) tight |= linemask[L];
            }
            if (ok) {
                safe[k]++;
                if ((x | tight) == full) maxi[k]++;
            }
            if (i + 1 < tot) {
                uint32_t c = x & (0u - x);
                uint32_t r = x + c;
                x = (((r ^ x) >> 2) / c) | r;
            }
            tested++;
        }
    }

    printf("BRUTE_BOARD n=%d b=%d maxk=%d tested=%llu\n", n, nb, maxk, tested);
    uint64_t ts = 0, tm = 0;
    for (int k = 0; k <= maxk; k++) {
        printf("SIZE %d %llu %llu\n", k, (unsigned long long)safe[k],
               (unsigned long long)maxi[k]);
        ts += safe[k];
        tm += maxi[k];
    }
    printf("SAFE %llu MAXIMAL %llu\n", (unsigned long long)ts, (unsigned long long)tm);
    return 0;
}
