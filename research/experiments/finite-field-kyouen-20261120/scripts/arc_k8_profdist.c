
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 512
#define MAXB 8192
#define MAXS 64
#define MAXPROF 8192

static int n, b;
static int circ_len[MAXB];
static int circ_pts[MAXB][MAXS];
static int base_circle = 0;

static uint64_t pk[MAXPROF], pc[MAXPROF];
static int pn = 0;

static uint64_t pack3(int a, int c, int d) {
    return ((uint64_t)a << 40) | ((uint64_t)c << 20) | (uint64_t)d;
}

static void addp(int a, int c, int d) {
    uint64_t key = pack3(a, c, d);
    for (int i = 0; i < pn; i++) if (pk[i] == key) { pc[i]++; return; }
    pk[pn] = key; pc[pn] = 1; pn++;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s circles.txt\n", argv[0]); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    if (fscanf(f, "%d %d", &n, &b) != 2) { fprintf(stderr, "bad header\n"); return 1; }
    for (int i = 0; i < b; i++) {
        int k;
        if (fscanf(f, "%d", &k) != 1) { fprintf(stderr, "bad line\n"); return 1; }
        circ_len[i] = k;
        for (int j = 0; j < k; j++) {
            if (fscanf(f, "%d", &circ_pts[i][j]) != 1) { fprintf(stderr, "bad pt\n"); return 1; }
        }
    }
    fclose(f);

    int s = circ_len[base_circle];
    static char inbase[MAXN];
    for (int j = 0; j < s; j++) inbase[circ_pts[base_circle][j]] = 1;
    int outside[MAXN], nout = 0;
    for (int p = 0; p < n; p++) if (!inbase[p]) outside[nout++] = p;

    int B[MAXS];
    for (int j = 0; j < s; j++) B[j] = circ_pts[base_circle][j];

    // tuples(P) from the tuple loop
    for (int t0 = 0; t0 < s; t0++)
    for (int t1 = t0+1; t1 < s; t1++)
    for (int t2 = t1+1; t2 < s; t2++)
    for (int t3 = t2+1; t3 < s; t3++) {
        int T[4] = {B[t0], B[t1], B[t2], B[t3]};
        for (int x0 = 0; x0 < nout; x0++)
        for (int x1 = x0+1; x1 < nout; x1++)
        for (int x2 = x1+1; x2 < nout; x2++)
        for (int x3 = x2+1; x3 < nout; x3++) {
            int X[4] = {outside[x0], outside[x1], outside[x2], outside[x3]};
            int v2=0,v3=0,v4=0,u3=0,u4=0,z4=0;
            for (int c = 0; c < b; c++) {
                if (c == base_circle) continue;
                int ct = 0, cx = 0;
                for (int j = 0; j < circ_len[c]; j++) {
                    int p = circ_pts[c][j];
                    for (int q = 0; q < 4; q++) if (T[q] == p) { ct++; break; }
                    for (int q = 0; q < 4; q++) if (X[q] == p) { cx++; break; }
                }
                if (ct == 2) {
                    if (cx == 2) v2++;
                    else if (cx == 3) v3++;
                    else if (cx == 4) v4++;
                } else if (ct == 1) {
                    if (cx == 3) u3++;
                    else if (cx == 4) u4++;
                } else if (ct == 0) {
                    if (cx == 4) z4++;
                }
            }
            addp(1 + v2 + u3 + z4, v3 + u4, v4);
        }
    }

    printf("tuples(P) from the tuple loop (%d profiles):\n", pn);
    for (int i = 0; i < pn; i++) {
        int a = (int)(pk[i] >> 40);
        int c = (int)((pk[i] >> 20) & 0xFFFFF);
        int d = (int)(pk[i] & 0xFFFFF);
        printf("  (%d,%d,%d): %llu\n", a, c, d, pc[i]);
    }
    return 0;
}
