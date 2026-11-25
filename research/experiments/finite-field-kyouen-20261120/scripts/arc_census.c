// Exact arc census by depth-first enumeration of arcs (not of subsets).
//
// The board is read from circles.txt as usual.  The DFS visits every safe
// position (arc) exactly once, in increasing point order, keeping the
// incremental blocking counters, so the legal moves at a node are exactly the
// points on the "allowed" list.  From those counts we get exact arc numbers:
//
//     #arcs(k)  = number of nodes at depth k
//     #arcs(k+1) = ( sum over k-arcs of #legal extensions ) / (k+1)
//
// which turns the expensive subset enumeration into a walk over the arcs
// themselves.  For q=9 this reproduces the known 1,062,720 eight-arcs and
// 29,520 nine-arcs; for q=11 it settles whether a 10-arc exists, i.e. whether
// K(11) is 9 or more.
//
// Build: gcc -O2 -o arc_census arc_census.c
// Run:   ./arc_census ../output/circles_q11.txt [maxdepth]

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n, b;
static int *clen;
static int **cpts;
static int *adj_off, *adj;

static int *cnt;
static int *blk;
static char *inarc;
static int *allowed, *pos, nallowed;

static long long nodes[64];
static long long ext_sum[64];      // sum of |allowed| over arcs of each depth
static int max_depth = 12;

static inline void allow_remove(int p) {
    int i = pos[p];
    int last = allowed[--nallowed];
    allowed[i] = last;
    pos[last] = i;
}
static inline void allow_add(int p) {
    pos[p] = nallowed;
    allowed[nallowed++] = p;
}
static inline void add_point(int p) {
    inarc[p] = 1;
    allow_remove(p);
    for (int t = adj_off[p]; t < adj_off[p + 1]; t++) {
        int c = adj[t];
        if (++cnt[c] == 3) {
            const int *cp = cpts[c];
            int len = clen[c];
            for (int u = 0; u < len; u++) {
                int v = cp[u];
                if (!inarc[v] && blk[v]++ == 0) allow_remove(v);
            }
        }
    }
}
static inline void remove_point(int p) {
    for (int t = adj_off[p]; t < adj_off[p + 1]; t++) {
        int c = adj[t];
        if (cnt[c] == 3) {
            const int *cp = cpts[c];
            int len = clen[c];
            for (int u = 0; u < len; u++) {
                int v = cp[u];
                if (!inarc[v] && --blk[v] == 0) allow_add(v);
            }
        }
        cnt[c]--;
    }
    inarc[p] = 0;
    if (blk[p] == 0) allow_add(p);
}

static void dfs(int depth, int last) {
    nodes[depth]++;
    ext_sum[depth] += nallowed;
    if (depth >= max_depth) return;
    int cand[256];
    int nc = nallowed;
    memcpy(cand, allowed, (size_t)nc * sizeof(int));
    for (int j = 0; j < nc; j++) {
        int p = cand[j];
        if (p <= last) continue;
        if (inarc[p] || blk[p] > 0) continue;
        add_point(p);
        dfs(depth + 1, p);
        remove_point(p);
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s circles.txt [maxdepth]\n", argv[0]); return 2; }
    if (argc > 2) max_depth = atoi(argv[2]);
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    if (fscanf(f, "%d %d", &n, &b) != 2) { fprintf(stderr, "bad header\n"); return 1; }
    if (n > 256) { fprintf(stderr, "n=%d exceeds the 256 candidate buffer\n", n); return 1; }
    clen = (int *)malloc((size_t)b * sizeof(int));
    cpts = (int **)malloc((size_t)b * sizeof(int *));
    int *deg = (int *)calloc((size_t)n, sizeof(int));
    for (int c = 0; c < b; c++) {
        int len;
        if (fscanf(f, "%d", &len) != 1) { fprintf(stderr, "truncated\n"); return 1; }
        clen[c] = len;
        cpts[c] = (int *)malloc((size_t)len * sizeof(int));
        for (int j = 0; j < len; j++) {
            if (fscanf(f, "%d", &cpts[c][j]) != 1) { fprintf(stderr, "truncated\n"); return 1; }
            deg[cpts[c][j]]++;
        }
    }
    fclose(f);

    adj_off = (int *)malloc((size_t)(n + 1) * sizeof(int));
    adj_off[0] = 0;
    for (int p = 0; p < n; p++) adj_off[p + 1] = adj_off[p] + deg[p];
    adj = (int *)malloc((size_t)adj_off[n] * sizeof(int));
    int *fillv = (int *)calloc((size_t)n, sizeof(int));
    for (int c = 0; c < b; c++)
        for (int j = 0; j < clen[c]; j++) {
            int p = cpts[c][j];
            adj[adj_off[p] + fillv[p]++] = c;
        }
    free(fillv); free(deg);

    cnt = (int *)calloc((size_t)b, sizeof(int));
    blk = (int *)calloc((size_t)n, sizeof(int));
    inarc = (char *)calloc((size_t)n, sizeof(char));
    allowed = (int *)malloc((size_t)n * sizeof(int));
    pos = (int *)malloc((size_t)n * sizeof(int));
    nallowed = n;
    for (int i = 0; i < n; i++) { allowed[i] = i; pos[i] = i; }

    dfs(0, -1);

    printf("POINTS %d\nCIRCLES %d\nmaxdepth %d\n", n, b, max_depth);
    long long total = 0;
    for (int d = 0; d <= max_depth; d++) {
        total += nodes[d];
        printf("NODES %d %lld\n", d, nodes[d]);
    }
    printf("TOTAL %lld\n", total);
    for (int d = 0; d <= max_depth; d++) {
        if (nodes[d] == 0) continue;
        printf("EXT %d %lld  (=> #arcs(%d) = %lld / %d = %lld)\n",
               d, ext_sum[d], d + 1, ext_sum[d], d + 1, ext_sum[d] / (d + 1));
    }
    printf("DERIVED #arcs(%d) = %lld\n", max_depth,
           nodes[max_depth] ? nodes[max_depth] : -1);
    return 0;
}
