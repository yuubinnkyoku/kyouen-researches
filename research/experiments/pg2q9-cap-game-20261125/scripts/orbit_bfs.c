// Orbit size of a point set under a permutation group on n <= 128 points.
//
// Input:
//   argv[1] = gens file: one permutation per line, n integers (n read from the
//             first line's token count)
//   argv[2] = starts file: lines "<k> <hi> <lo>" where (hi,lo) is a 128-bit mask
//   argv[3] = capacity exponent for the hash set (e.g. 24 -> 2^24 slots)
//
// Output: one line per start "<k> <orbit_size>".
//
// Build: gcc -O2 -o orbit_bfs orbit_bfs.c

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef struct { uint64_t hi, lo; } Mask;

static int n;
static int *gens[64];
static int ngens;

static Mask *set_keys;
static size_t set_cap, set_mask, set_used;
static Mask *queue;

static inline size_t hash128(uint64_t hi, uint64_t lo) {
    uint64_t x = hi * 0x9e3779b97f4a7c15ULL ^ (lo + 0x9e3779b97f4a7c15ULL);
    x ^= x >> 30; x *= 0xbf58476d1ce4e5b9ULL;
    x ^= x >> 27; x *= 0x94d049bb133111ebULL;
    x ^= x >> 31;
    return (size_t)x;
}

static int set_add(Mask m) {  // returns 1 if newly added
    size_t h = hash128(m.hi, m.lo) & set_mask;
    while (set_keys[h].hi != 0 || set_keys[h].lo != 0) {
        if (set_keys[h].hi == m.hi && set_keys[h].lo == m.lo) return 0;
        h = (h + 1) & set_mask;
    }
    set_keys[h] = m;
    set_used++;
    return 1;
}

static Mask apply_gen(Mask m, const int *perm) {
    Mask r = {0, 0};
    uint64_t w = m.lo;
    while (w) {
        int p = __builtin_ctzll(w);
        w &= w - 1;
        int q = perm[p];
        if (q < 64) r.lo |= 1ULL << q; else r.hi |= 1ULL << (q - 64);
    }
    w = m.hi;
    while (w) {
        int p = __builtin_ctzll(w);
        w &= w - 1;
        int q = perm[p + 64];
        if (q < 64) r.lo |= 1ULL << q; else r.hi |= 1ULL << (q - 64);
    }
    return r;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s gens.txt starts.txt cap_exp\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("gens"); return 1; }
    char line[65536];
    ngens = 0;
    while (fgets(line, sizeof line, f)) {
        int vals[256], cnt = 0;
        char *tok = strtok(line, " \t\n");
        while (tok && cnt < 256) { vals[cnt++] = atoi(tok); tok = strtok(NULL, " \t\n"); }
        if (cnt == 0) continue;
        if (n == 0) n = cnt;
        if (cnt != n) { fprintf(stderr, "bad gen length\n"); return 1; }
        gens[ngens] = malloc(n * sizeof(int));
        memcpy(gens[ngens], vals, n * sizeof(int));
        ngens++;
    }
    fclose(f);
    int cap_exp = atoi(argv[3]);
    set_cap = (size_t)1 << cap_exp;
    set_mask = set_cap - 1;
    set_keys = calloc(set_cap, sizeof(Mask));
    queue = malloc(set_cap * sizeof(Mask) / 2);  // enough for the orbit
    if (!set_keys || !queue) { fprintf(stderr, "alloc failed\n"); return 1; }

    f = fopen(argv[2], "r");
    if (!f) { perror("starts"); return 1; }
    int k;
    unsigned long long hi, lo;
    while (fscanf(f, "%d %llu %llu", &k, &hi, &lo) == 3) {
        memset(set_keys, 0, set_cap * sizeof(Mask));
        set_used = 0;
        Mask start = {(uint64_t)hi, (uint64_t)lo};
        set_add(start);
        queue[0] = start;
        size_t head = 0, tail = 1;
        while (head < tail) {
            Mask m = queue[head++];
            for (int gi = 0; gi < ngens; gi++) {
                Mask r = apply_gen(m, gens[gi]);
                if (set_add(r)) queue[tail++] = r;
            }
        }
        printf("%d %zu\n", k, set_used);
    }
    fclose(f);
    return 0;
}
