// Census of maximal caps (s=2) in a projective plane board.
//
// Reads a board "n b" + b lines; enumerates all caps (sets with <=2 points on
// every line) with incremental counters, and counts, per size, the caps that
// are maximal (no addable point).  No position masks are needed, so this works
// for n > 64 (e.g. PG(2,8), n = 73).
//
// Build: gcc -O2 -o cap_census cap_census.c
// Run:   ./cap_census board_pg2q8.txt

#include <stdio.h>
#include <stdlib.h>

static int n, b;
static int *clen, **cpts;
static int *adj_off, *adj;
static int *cnt, *blk;
static char *inarc;
static int *allowed, *pos, nallowed;
static long long size_count[128], max_count[128];

static inline void allow_remove(int p) {
    int i = pos[p];
    int last = allowed[--nallowed];
    allowed[i] = last; pos[last] = i;
}
static inline void allow_add(int p) {
    pos[p] = nallowed; allowed[nallowed++] = p;
}
static void add_point(int p) {
    inarc[p] = 1; allow_remove(p);
    for (int t = adj_off[p]; t < adj_off[p + 1]; t++) {
        int c = adj[t];
        if (++cnt[c] == 2) {
            const int *cp = cpts[c];
            for (int u = 0; u < clen[c]; u++) {
                int v = cp[u];
                if (!inarc[v] && blk[v]++ == 0) allow_remove(v);
            }
        }
    }
}
static void remove_point(int p) {
    for (int t = adj_off[p]; t < adj_off[p + 1]; t++) {
        int c = adj[t];
        if (cnt[c] == 2) {
            const int *cp = cpts[c];
            for (int u = 0; u < clen[c]; u++) {
                int v = cp[u];
                if (!inarc[v] && --blk[v] == 0) allow_add(v);
            }
        }
        cnt[c]--;
    }
    inarc[p] = 0;
    if (blk[p] == 0) allow_add(p);
}
static void enumerate(int size, int last) {
    size_count[size]++;
    if (nallowed == 0) max_count[size]++;
    int cand[256];
    int nc = nallowed;
    for (int j = 0; j < nc; j++) cand[j] = allowed[j];
    for (int j = 0; j < nc; j++) {
        int p = cand[j];
        if (p <= last) continue;
        if (inarc[p] || blk[p] > 0) continue;
        add_point(p);
        enumerate(size + 1, p);
        remove_point(p);
    }
}
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s board.txt\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    if (fscanf(f, "%d %d", &n, &b) != 2) { fprintf(stderr, "bad header\n"); return 1; }
    clen = malloc(b * sizeof(int)); cpts = malloc(b * sizeof(int *));
    int *deg = calloc(n, sizeof(int));
    for (int c = 0; c < b; c++) {
        if (fscanf(f, "%d", &clen[c]) != 1) return 1;
        cpts[c] = malloc(clen[c] * sizeof(int));
        for (int j = 0; j < clen[c]; j++) {
            if (fscanf(f, "%d", &cpts[c][j]) != 1) return 1;
            deg[cpts[c][j]]++;
        }
    }
    fclose(f);
    adj_off = malloc((n + 1) * sizeof(int)); adj_off[0] = 0;
    for (int p = 0; p < n; p++) adj_off[p + 1] = adj_off[p] + deg[p];
    adj = malloc(adj_off[n] * sizeof(int));
    int *fill = calloc(n, sizeof(int));
    for (int c = 0; c < b; c++)
        for (int j = 0; j < clen[c]; j++) {
            int p = cpts[c][j];
            adj[adj_off[p] + fill[p]++] = c;
        }
    free(fill); free(deg);
    cnt = calloc(b, sizeof(int)); blk = calloc(n, sizeof(int));
    inarc = calloc(n, 1);
    allowed = malloc(n * sizeof(int)); pos = malloc(n * sizeof(int));
    nallowed = n;
    for (int i = 0; i < n; i++) { allowed[i] = i; pos[i] = i; }
    enumerate(0, -1);
    long long total = 0;
    for (int k = 0; k < 128; k++) total += size_count[k];
    printf("N %d B %d SAFE %lld\n", n, b, total);
    for (int k = 0; k < 128; k++)
        if (size_count[k]) printf("SIZE %d %lld %lld\n", k, size_count[k], max_count[k]);
    return 0;
}
