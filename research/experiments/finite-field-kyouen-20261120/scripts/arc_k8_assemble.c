// k=8 profile assembly in C: validates the profile formula + multiplicity
// theorem against the exhaustive count at q=9.
//
// For each 4-subset T of the base circle C and each 4-subset X of the
// points outside C, compute the 6 class counts (v2,v3,v4,u3,u4,z4) and
// hence the profile.  Accumulate tuples per profile.  Then
//
//   #8-sets with profile P = tuples(P) / (#4-circles in P) * b
//
// and #8-arcs = C(n,8) - sum - (7,) - (8,).
//
// The exhaustive count at q=9 is 1,062,720 (from arc_k8.exe), so this
// gives an independent check of the whole profile machinery.
//
// Build: gcc -O2 -o arc_k8_assemble arc_k8_assemble.c
// Run:   ./arc_k8_assemble circles_q9.txt

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 512
#define MAXB 8192
#define MAXS 64
#define MAXPROF 4096

static int n, b;
static int circ_len[MAXB];
static int circ_pts[MAXB][MAXS];
static int base_circle = -1;

// profile -> tuple count
static uint64_t prof_key[MAXPROF];
static uint64_t prof_cnt[MAXPROF];
static int prof_n = 0;

static uint64_t pack_prof(int n4, int n5, int n6) {
    return ((uint64_t)n4 << 32) | ((uint64_t)n5 << 16) | (uint64_t)n6;
}

static void add_prof(int n4, int n5, int n6) {
    uint64_t key = pack_prof(n4, n5, n6);
    for (int i = 0; i < prof_n; i++) {
        if (prof_key[i] == key) { prof_cnt[i]++; return; }
    }
    if (prof_n >= MAXPROF) { fprintf(stderr, "profile table full\n"); exit(1); }
    prof_key[prof_n] = key;
    prof_cnt[prof_n] = 1;
    prof_n++;
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

    // find the base circle: the one containing points 0..s-1 (the P^1(F_q))
    // we detect it as the circle whose length is s = q+1 and which is the
    // first one listed with that length (export_circles puts it first)
    int s = 0;
    for (int i = 0; i < b; i++) if (circ_len[i] > s) s = circ_len[i];
    // the base circle is the first with length s
    for (int i = 0; i < b; i++) if (circ_len[i] == s) { base_circle = i; break; }
    fprintf(stderr, "n=%d b=%d s=%d base=%d\n", n, b, s, base_circle);

    // membership: inbase[p]
    static char inbase[MAXN];
    for (int j = 0; j < circ_len[base_circle]; j++) inbase[circ_pts[base_circle][j]] = 1;

    // outside points
    int outside[MAXN], nout = 0;
    for (int p = 0; p < n; p++) if (!inbase[p]) outside[nout++] = p;
    fprintf(stderr, "outside=%d\n", nout);

    // enumerate T (4-subsets of base) and X (4-subsets of outside)
    int B[MAXS], nb = circ_len[base_circle];
    for (int j = 0; j < nb; j++) B[j] = circ_pts[base_circle][j];

    long long tuples = 0;
    for (int t0 = 0; t0 < nb; t0++)
    for (int t1 = t0+1; t1 < nb; t1++)
    for (int t2 = t1+1; t2 < nb; t2++)
    for (int t3 = t2+1; t3 < nb; t3++) {
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
            int n4 = 1 + v2 + u3 + z4;
            int n5 = v3 + u4;
            int n6 = v4;
            add_prof(n4, n5, n6);
            tuples++;
        }
    }
    fprintf(stderr, "tuples=%lld profiles=%d\n", tuples, prof_n);

    // assemble with EXACT integer arithmetic.
    // #8-sets with profile P = tuples(P) * b / n4.
    // NOTE: tuples(P)/n4 need NOT be an integer (e.g. 525/10), but
    // tuples(P)*b/n4 always is.  So multiply by b FIRST.
    unsigned long long bad = 0;
    int nonint = 0;
    for (int i = 0; i < prof_n; i++) {
        int n4 = (int)(prof_key[i] >> 32);
        unsigned long long num = prof_cnt[i] * (unsigned long long)b;
        if (num % (unsigned long long)n4 != 0) nonint++;
        bad += num / (unsigned long long)n4;
    }
    // (7,) = b*C(s,7)*(n-s), (8,) = b*C(s,8)
    unsigned long long seven = 0, eight = 0;
    if (s >= 7) {
        unsigned long long c = 1;
        for (int i = 0; i < 7; i++) c = c * (unsigned long long)(s - i) / (unsigned long long)(i + 1);
        seven = (unsigned long long)b * c * (unsigned long long)(n - s);
    }
    if (s >= 8) {
        unsigned long long c = 1;
        for (int i = 0; i < 8; i++) c = c * (unsigned long long)(s - i) / (unsigned long long)(i + 1);
        eight = (unsigned long long)b * c;
    }
    bad += seven + eight;

    unsigned long long total = 1;
    for (int i = 0; i < 8; i++) total = total * (unsigned long long)(n - i) / (unsigned long long)(i + 1);
    unsigned long long arcs = total - bad;

    printf("n=%d b=%d s=%d\n", n, b, s);
    printf("tuples=%lld profiles=%d nonint=%d\n", tuples, prof_n, nonint);
    printf("(7,)=%llu (8,)=%llu\n", seven, eight);
    printf("bad=%llu total=%llu arcs=%llu\n", bad, total, arcs);
    for (int i = 0; i < prof_n; i++) {
        int n4 = (int)(prof_key[i] >> 32);
        int n5 = (int)((prof_key[i] >> 16) & 0xFFFF);
        int n6 = (int)(prof_key[i] & 0xFFFF);
        printf("  prof (%d,%d,%d) tuples=%llu div=%d rem=%llu\n",
               n4, n5, n6, prof_cnt[i], n4,
               prof_cnt[i] % (unsigned long long)n4);
    }
    return 0;
}
