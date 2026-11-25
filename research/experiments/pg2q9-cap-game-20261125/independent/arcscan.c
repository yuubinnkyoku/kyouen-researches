/* arcscan.c -- independent count of 4-caps and 5-caps via frames.
 *
 * Different route from the DFS census:
 *   - enumerate ORDERED frames (A,B,C,D) with no three collinear
 *     (91 * 90 * 81 * 64 frames), so the number of 4-caps is frames/4! and
 *     every 4-cap is met exactly 24 times;
 *   - for every frame compute the number of addable points
 *     (91 - |union of the 6 secant lines|) and histogram it;
 *   - identity: #5-caps = (#4-caps * addable) / 5  (each 5-cap has 5 4-subsets).
 *
 * usage: arcscan board
 */

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

typedef unsigned __int128 u128;
#define MAXN 128

static int N, NL, K;
static int lid[MAXN][MAXN];
static u128 lmask[MAXN];
static u128 allmask;

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: %s board\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { fprintf(stderr, "cannot open board\n"); return 2; }
    if (fscanf(f, "%d %d", &N, &NL) != 2) return 2;
    for (int li = 0; li < NL; li++) {
        int k;
        if (fscanf(f, "%d", &k) != 1) return 2;
        u128 m = 0;
        for (int t = 0; t < k; t++) { int p; if (fscanf(f, "%d", &p) != 1) return 2; m |= (u128)1 << p; }
        lmask[li] = m;
    }
    fclose(f);
    for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) lid[a][b] = -1;
    for (int li = 0; li < NL; li++)
        for (int a = 0; a < N; a++) if ((lmask[li] >> a) & 1)
            for (int b = a + 1; b < N; b++) if ((lmask[li] >> b) & 1) {
                lid[a][b] = li; lid[b][a] = li;
            }
    allmask = ((u128)1 << N) - 1;

    long long frames = 0;
    long long hist[MAXN];
    memset(hist, 0, sizeof hist);
    long long sum_add = 0;
    for (int a = 0; a < N; a++) {
        for (int b = 0; b < N; b++) {
            if (b == a) continue;
            int lab = lid[a][b];
            for (int c = 0; c < N; c++) {
                if (c == a || c == b) continue;
                if ((lmask[lab] >> c) & 1) continue;
                int lac = lid[a][c], lbc = lid[b][c];
                for (int d = 0; d < N; d++) {
                    if (d == a || d == b || d == c) continue;
                    if ((lmask[lab] >> d) & 1) continue;
                    if ((lmask[lac] >> d) & 1) continue;
                    if ((lmask[lbc] >> d) & 1) continue;
                    u128 bl = lmask[lab] | lmask[lac] | lmask[lbc];
                    bl |= lmask[lid[a][d]] | lmask[lid[b][d]] | lmask[lid[c][d]];
                    int add = N - __builtin_popcountll((uint64_t)bl)
                                  - __builtin_popcountll((uint64_t)(bl >> 64));
                    hist[add]++;
                    sum_add += add;
                    frames++;
                }
            }
        }
    }
    printf("frames %lld\n", frames);
    printf("frames_over_24 %lld\n", frames / 24);
    printf("sum_addable_over_24 %lld\n", sum_add / 24);
    for (int i = 0; i < N; i++)
        if (hist[i]) printf("addable_hist %d %lld\n", i, hist[i]);
    if (frames % 24 == 0 && frames > 0) {
        long long caps4 = frames / 24;
        printf("caps4 %lld\n", caps4);
        printf("caps5 %lld\n", (caps4 * (sum_add / frames)) / 5);
        printf("mean_addable %lld\n", sum_add / frames);
    }
    return 0;
}
