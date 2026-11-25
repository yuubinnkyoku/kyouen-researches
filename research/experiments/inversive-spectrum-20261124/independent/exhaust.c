/* Independent exhaustive enumerator for small boards (q=4, q=5).
 * Counts all n-subsets S with |S cap B| <= s for every block B.
 * Standard C + gcc only.
 *
 * Usage: exhaust <board.dat> <s> <n>
 * Prints: count, first witness, nodes, seconds.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXV 64
#define MAXB 512

static int V, B, S, N;
static uint64_t blockmask[MAXB];
static int pb_off[MAXV + 1];
static int *pb_list = NULL;
static uint8_t counts[MAXB];
static long long nodes = 0, valid = 0;
static uint64_t first_witness = 0;
static int have_witness = 0;

static void dfs(int start, int need, uint64_t chosen) {
    nodes++;
    if (need == 0) {
        valid++;
        if (!have_witness) {
            first_witness = chosen;
            have_witness = 1;
        }
        return;
    }
    if (V - start < need) return;
    for (int p = start; p <= V - need; p++) {
        int ok = 1;
        for (int idx = pb_off[p]; idx < pb_off[p + 1]; idx++)
            if (counts[pb_list[idx]] >= S) {
                ok = 0;
                break;
            }
        if (!ok) continue;
        for (int idx = pb_off[p]; idx < pb_off[p + 1]; idx++)
            counts[pb_list[idx]]++;
        dfs(p + 1, need - 1, chosen | (1ULL << p));
        for (int idx = pb_off[p]; idx < pb_off[p + 1]; idx++)
            counts[pb_list[idx]]--;
    }
}

int main(int argc, char **argv) {
    if (argc != 4) {
        fprintf(stderr, "usage: %s board.dat s n\n", argv[0]);
        return 2;
    }
    const char *path = argv[1];
    S = atoi(argv[2]);
    N = atoi(argv[3]);
    FILE *f = fopen(path, "r");
    if (!f) {
        perror(path);
        return 2;
    }
    int k;
    if (fscanf(f, "%d %d %d", &V, &B, &k) != 3) return 2;
    if (V > MAXV || B > MAXB) return 2;
    int *deg = calloc((size_t)V, sizeof(int));
    int(*blocks)[16] = calloc((size_t)B, sizeof(*blocks));
    for (int bi = 0; bi < B; bi++) {
        blockmask[bi] = 0;
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
    memset(counts, 0, sizeof(counts));

    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    dfs(0, N, 0);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double sec = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
    printf("v=%d b=%d s=%d n=%d count=%lld nodes=%lld seconds=%.6f", V, B, S, N,
           valid, nodes, sec);
    if (have_witness) {
        printf(" witness=");
        int first = 1;
        for (int p = 0; p < V; p++)
            if ((first_witness >> p) & 1) {
                printf("%s%d", first ? "" : ",", p);
                first = 0;
            }
    }
    printf("\n");
    return 0;
}
