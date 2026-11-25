/* Independent branch-and-bound for the q=7, s=4 case of the inversive-spectrum
 * experiment.  Reads a simple board data file (generated from the JSON by
 * verify_all.py), fixes the points given on the command line (WLOG by a
 * computationally verified 3-transitive Mobius symmetry), and searches for a
 * TARGET-set S with |S cap B| <= S for every circle B.
 *
 * No third-party code; standard C + gcc only.
 *
 * Usage: q7_bb <board.dat> <s> <target> [p1 p2 ...]
 * Board data format:
 *   v b k
 *   k integers per line, b lines
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXV 64
#define MAXB 512

static int V, B, S, TARGET;
static uint64_t blockmask[MAXB];
static int pb_off[MAXV + 1];
static int *pb_list = NULL;
static uint8_t counts[MAXB];
static uint64_t solution = 0;
static long long nodes = 0;
static int found = 0;

static inline int pc64(uint64_t x) { return __builtin_popcountll(x); }

static int dfs(uint64_t A, uint64_t U, int sel) {
    nodes++;
    if (sel == TARGET) {
        solution = A;
        found = 1;
        return 1;
    }
    int pc = pc64(U);
    if (sel + pc < TARGET) return 0;

    /* Moment upper bound: for any remaining set X of size m,
       sum_B C(|X cap B|,2) = 8 C(m,2) and sum_B C(|X cap B|,3) = C(m,3);
       with |X cap B| <= S-counts[B] this bounds m. */
    long long S2 = 0, S3 = 0;
    for (int bi = 0; bi < B; bi++) {
        int r = S - (int)counts[bi];
        if (r >= 2) S2 += (long long)r * (r - 1) / 2;
        if (r >= 3) S3 += (long long)r * (r - 1) * (r - 2) / 6;
    }
    int m = 0;
    for (int mm = 1; mm <= pc; mm++) {
        long long c2 = (long long)mm * (mm - 1) / 2;
        long long c3 = (long long)mm * (mm - 1) * (mm - 2) / 6;
        if (8 * c2 <= S2 && c3 <= S3)
            m = mm;
        else
            break;
    }
    if (sel + m < TARGET) return 0;

    /* choose the candidate with the largest sum of squared block loads */
    int best = -1, bestscore = -1;
    uint64_t u = U;
    while (u) {
        int p = __builtin_ctzll(u);
        u &= u - 1;
        int sc = 0;
        for (int idx = pb_off[p]; idx < pb_off[p + 1]; idx++) {
            int c = counts[pb_list[idx]];
            sc += c * c;
            if (c == S - 1) sc += 8;
        }
        if (sc > bestscore) {
            bestscore = sc;
            best = p;
        }
    }
    if (best < 0) return 0;

    uint64_t bit = 1ULL << best;
    for (int idx = pb_off[best]; idx < pb_off[best + 1]; idx++)
        counts[pb_list[idx]]++;
    uint64_t U2 = U & ~bit;
    for (int idx = pb_off[best]; idx < pb_off[best + 1]; idx++) {
        int bi = pb_list[idx];
        if (counts[bi] == S) U2 &= ~blockmask[bi];
    }
    if (dfs(A | bit, U2, sel + 1)) return 1; /* leave counts dirty on success */
    for (int idx = pb_off[best]; idx < pb_off[best + 1]; idx++)
        counts[pb_list[idx]]--;

    if (dfs(A, U & ~bit, sel)) return 1;
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 4) {
        fprintf(stderr, "usage: %s board.dat s target [p1 p2 ...]\n", argv[0]);
        return 2;
    }
    const char *path = argv[1];
    S = atoi(argv[2]);
    TARGET = atoi(argv[3]);
    FILE *f = fopen(path, "r");
    if (!f) {
        perror(path);
        return 2;
    }
    int k;
    if (fscanf(f, "%d %d %d", &V, &B, &k) != 3) return 2;
    if (V > MAXV || B > MAXB) {
        fprintf(stderr, "board too large\n");
        return 2;
    }
    memset(blockmask, 0, sizeof(blockmask));
    memset(pb_off, 0, sizeof(pb_off));
    int *deg = calloc((size_t)V, sizeof(int));
    int(*blocks)[16] = calloc((size_t)B, sizeof(*blocks));
    for (int bi = 0; bi < B; bi++) {
        for (int j = 0; j < k; j++) {
            int p;
            if (fscanf(f, "%d", &p) != 1) return 2;
            blocks[bi][j] = p;
            blockmask[bi] |= 1ULL << p;
            deg[p]++;
        }
    }
    fclose(f);
    pb_off[0] = 0;
    for (int p = 0; p < V; p++) pb_off[p + 1] = pb_off[p] + deg[p];
    pb_list = malloc((size_t)pb_off[V] * sizeof(int));
    int *fill = calloc((size_t)V, sizeof(int));
    for (int bi = 0; bi < B; bi++)
        for (int j = 0; j < k; j++) {
            int p = blocks[bi][j];
            pb_list[pb_off[p] + fill[p]++] = bi;
        }
    free(fill);
    free(deg);
    free(blocks);

    uint64_t A = 0;
    memset(counts, 0, sizeof(counts));
    for (int i = 4; i < argc; i++) {
        int p = atoi(argv[i]);
        if (p < 0 || p >= V || ((A >> p) & 1)) {
            fprintf(stderr, "bad fixed point %d\n", p);
            return 2;
        }
        A |= 1ULL << p;
        for (int idx = pb_off[p]; idx < pb_off[p + 1]; idx++)
            counts[pb_list[idx]]++;
    }
    uint64_t U = (((uint64_t)1 << V) - 1) & ~A;
    for (int bi = 0; bi < B; bi++)
        if (counts[bi] >= S) U &= ~blockmask[bi];

    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    int bits = pc64(A);
    dfs(A, U, bits);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double sec = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
    printf("fixed=");
    for (int i = 4; i < argc; i++) printf("%s%s", i > 4 ? "," : "", argv[i]);
    printf(" result=%s nodes=%lld seconds=%.6f", found ? "SAT" : "UNSAT", nodes, sec);
    if (found) {
        printf(" witness=");
        int first = 1;
        for (int p = 0; p < V; p++)
            if ((solution >> p) & 1) {
                printf("%s%d", first ? "" : ",", p);
                first = 0;
            }
    }
    printf("\n");
    return found ? 10 : 0;
}
