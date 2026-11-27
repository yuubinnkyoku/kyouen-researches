// Independent verification of the PG(2,5), s=3 kyouen-game Grundy table.
//
// This program shares no code with the published grundy_s_stats.c.  It uses:
//   * a separate board parser (fgets + strtol),
//   * depth-first enumeration in increasing point order,
//   * the game rule applied point-by-point: p is a legal addition to S iff
//     every line through p contains at most 2 points of S (so S+p has at most
//     3 on every line; lines not through p are unchanged),
//   * per-size arrays of 64-bit masks, sorted, with binary search for children,
//     instead of an open-addressing hash map.
//
// It computes the normal-play Grundy value and the misere win flag for every
// safe position, plus per-size maximal-position counts.
//
// Usage: indep_verify board.txt [probe.txt]
// probe.txt: first token count m, then m decimal 64-bit masks (one per token);
// for each, prints "PROBE4 <mask> <grundy>" (or -1 if not a safe position).

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 64
#define MAXB 256

static int n, b;
static uint64_t lmask[MAXB];
static int llen[MAXB];
static int ptlines[MAXN][MAXB];
static int ptlcount[MAXN];

static uint64_t *bucket[MAXN];
static long long bcnt[MAXN], bcap[MAXN];

static void die(const char *msg) {
    fprintf(stderr, "FATAL: %s\n", msg);
    exit(1);
}

static void push(int s, uint64_t m) {
    if (bcnt[s] == bcap[s]) {
        bcap[s] = bcap[s] ? bcap[s] * 2 : 4096;
        bucket[s] = (uint64_t *)realloc(bucket[s],
                                        (size_t)bcap[s] * sizeof(uint64_t));
        if (!bucket[s]) die("out of memory in push");
    }
    bucket[s][bcnt[s]++] = m;
}

/* p may be added to set iff no line through p already holds 3 of set's points */
static int legal_add(uint64_t set, int p) {
    int np = ptlcount[p];
    for (int t = 0; t < np; t++) {
        int c = ptlines[p][t];
        if (__builtin_popcountll(set & lmask[c]) >= 3) return 0;
    }
    return 1;
}

static void dfs(int s, uint64_t set, int last) {
    push(s, set);
    for (int p = last + 1; p < n; p++) {
        if ((set >> p) & 1ULL) continue;
        if (!legal_add(set, p)) continue;
        dfs(s + 1, set | (1ULL << p), p);
    }
}

static int cmpu64(const void *a, const void *b) {
    uint64_t x = *(const uint64_t *)a, y = *(const uint64_t *)b;
    return (x > y) - (x < y);
}

/* index of key in sorted arr[0..len-1], or -1 */
static long long bfind(const uint64_t *arr, long long len, uint64_t key) {
    long long lo = 0, hi = len - 1;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        if (arr[mid] == key) return mid;
        if (arr[mid] < key) lo = mid + 1; else hi = mid - 1;
    }
    return -1;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s board.txt [probe.txt]\n", argv[0]); return 2; }

    /* ---------- parse board (independent of the published engine) ---------- */
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("board"); return 1; }
    char buf[8192];
    if (!fgets(buf, sizeof buf, f)) die("empty board file");
    if (sscanf(buf, "%d %d", &n, &b) != 2) die("bad header");
    if (n < 0 || n > MAXN) die("n out of range");
    if (b < 0 || b > MAXB) die("b out of range");
    for (int c = 0; c < b; c++) {
        if (!fgets(buf, sizeof buf, f)) die("truncated board");
        char *p = buf;
        char *end;
        long len = strtol(p, &end, 10);
        if (end == p || len <= 0 || len > MAXN) die("bad line length");
        p = end;
        lmask[c] = 0;
        llen[c] = (int)len;
        for (int j = 0; j < len; j++) {
            long v = strtol(p, &end, 10);
            if (end == p || v < 0 || v >= n) die("bad point index");
            if ((lmask[c] >> v) & 1ULL) die("repeated point on a line");
            lmask[c] |= 1ULL << v;
            p = end;
        }
    }
    fclose(f);

    for (int c = 0; c < b; c++)
        for (int v = 0; v < n; v++)
            if ((lmask[c] >> v) & 1ULL) {
                if (ptlcount[v] >= MAXB) die("too many lines per point");
                ptlines[v][ptlcount[v]++] = c;
            }

    /* ---------- phase 1: enumerate every safe position exactly once ---------- */
    dfs(0, 0ULL, -1);

    int maxk = 0;
    long long total = 0;
    for (int s = 0; s < MAXN; s++) {
        if (bcnt[s]) maxk = s;
        total += bcnt[s];
    }
    printf("POINTS %d\nCIRCLES %d\nSAFE %lld\n", n, b, total);

    /* sort each bucket and check uniqueness (enumeration has no duplicates) */
    for (int s = 0; s <= maxk; s++) {
        qsort(bucket[s], (size_t)bcnt[s], sizeof(uint64_t), cmpu64);
        for (long long i = 1; i < bcnt[s]; i++)
            if (bucket[s][i] == bucket[s][i - 1])
                die("duplicate safe position in a size bucket");
    }

    /* ---------- phase 2: Grundy values, largest size first ---------- */
    unsigned char *val[MAXN];
    memset(val, 0, sizeof val);
    long long gsize[MAXN][64];
    long long ghist[64];
    long long maximal[MAXN];
    memset(gsize, 0, sizeof gsize);
    memset(ghist, 0, sizeof ghist);
    memset(maximal, 0, sizeof maximal);

    for (int s = maxk; s >= 0; s--) {
        long long cnt = bcnt[s];
        val[s] = (unsigned char *)malloc((size_t)(cnt ? cnt : 1));
        if (!val[s]) die("out of memory for values");
        for (long long i = 0; i < cnt; i++) {
            uint64_t m = bucket[s][i];
            uint64_t seen = 0;
            int nmoves = 0, win = 0;
            for (int p = 0; p < n; p++) {
                if ((m >> p) & 1ULL) continue;
                if (!legal_add(m, p)) continue;
                long long idx = bfind(bucket[s + 1], bcnt[s + 1],
                                      m | (1ULL << p));
                if (idx < 0) die("child not found: enumeration/rule mismatch");
                unsigned cv = val[s + 1][idx];
                unsigned g = cv & 63u;
                unsigned cwin = (cv >> 6) & 1u;
                if (g < 64) seen |= 1ULL << g;
                nmoves++;
                if (!cwin) win = 1;
            }
            unsigned g = 0;
            while (g < 64 && ((seen >> g) & 1ULL)) g++;
            if (nmoves == 0) { maximal[s]++; win = 1; }
            val[s][i] = (unsigned char)(g | ((unsigned)win << 6));
            gsize[s][g]++;
            ghist[g]++;
        }
    }

    /* root and misere root */
    {
        long long idx = bfind(bucket[0], bcnt[0], 0ULL);
        if (idx < 0) die("empty position missing");
        unsigned rv = val[0][idx];
        printf("ROOT %u %u\n", rv & 63u, (rv >> 6) & 1u);
    }

    for (int s = 0; s <= maxk; s++) {
        long long g0 = 0;
        for (int g = 0; g < 64; g++) if (g == 0) g0 = gsize[s][0];
        printf("SIZE %d %lld %lld %lld\n", s, bcnt[s], maximal[s], g0);
    }
    for (int g = 0; g < 64; g++)
        if (ghist[g]) printf("GRUNDY %d %lld\n", g, ghist[g]);
    for (int s = 0; s <= maxk; s++)
        for (int g = 0; g < 64; g++)
            if (gsize[s][g]) printf("GSIZE %d %d %lld\n", s, g, gsize[s][g]);

    /* ---------- optional probe values ---------- */
    if (argc >= 3) {
        FILE *pf = fopen(argv[2], "r");
        if (!pf) { perror("probe"); return 1; }
        long mcount;
        if (fscanf(pf, "%ld", &mcount) != 1 || mcount < 0)
            die("bad probe header");
        for (long z = 0; z < mcount; z++) {
            unsigned long long raw;
            if (fscanf(pf, "%llu", &raw) != 1) die("probe truncated");
            uint64_t m = (uint64_t)raw;
            int pc = __builtin_popcountll(m);
            int found = -1;
            if (pc <= maxk && bcnt[pc] > 0) {
                long long idx = bfind(bucket[pc], bcnt[pc], m);
                if (idx >= 0) found = val[pc][idx] & 63u;
            }
            printf("PROBE4 %llu %d\n", raw, found);
        }
        fclose(pf);
    }

    return 0;
}
