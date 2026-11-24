/* setcmp.c -- compare two binary sets of 128-bit point masks.
 *
 * File format: uint64 count, then count * 16-byte little-endian u128.
 * Reports: element counts, distinct-element counts, and whether the two sets
 * (after deduplication) are equal.  Exit code 0 iff equal.
 *
 * usage: setcmp A.bin B.bin [--list-diff N]
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef unsigned __int128 u128;

typedef struct {
    u128 *a;
    size_t n;
} Set;

static Set load(const char *path)
{
    Set s = {NULL, 0};
    FILE *f = fopen(path, "rb");
    if (!f) { fprintf(stderr, "cannot open %s\n", path); exit(2); }
    uint64_t n = 0;
    if (fread(&n, 8, 1, f) != 1) { fprintf(stderr, "bad header %s\n", path); exit(2); }
    s.a = (u128 *)malloc((size_t)n * sizeof(u128));
    if (!s.a && n) { fprintf(stderr, "OOM\n"); exit(2); }
    if (n && fread(s.a, sizeof(u128), (size_t)n, f) != (size_t)n) {
        fprintf(stderr, "short read %s\n", path); exit(2);
    }
    fclose(f);
    s.n = (size_t)n;
    return s;
}

static int cmp128(const void *x, const void *y)
{
    u128 a = *(const u128 *)x, b = *(const u128 *)y;
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
}

static size_t dedupe(Set *s)
{
    if (!s->n) return 0;
    qsort(s->a, s->n, sizeof(u128), cmp128);
    size_t w = 1;
    for (size_t i = 1; i < s->n; i++)
        if (s->a[i] != s->a[w - 1]) s->a[w++] = s->a[i];
    s->n = w;
    return w;
}

int main(int argc, char **argv)
{
    if (argc < 3) {
        fprintf(stderr, "usage: %s A.bin B.bin\n", argv[0]);
        return 2;
    }
    Set a = load(argv[1]), b = load(argv[2]);
    size_t rawn = a.n, rawb = b.n;
    size_t na = dedupe(&a), nb = dedupe(&b);
    size_t i = 0, j = 0, onlya = 0, onlyb = 0, first = 0;
    while (i < na && j < nb) {
        if (a.a[i] == b.a[j]) { i++; j++; }
        else if (a.a[i] < b.a[j]) {
            if (first < 5) {
                unsigned long long lo = (unsigned long long)a.a[i];
                unsigned long long hi = (unsigned long long)(a.a[i] >> 64);
                fprintf(stderr, "  only-A %016llx%016llx\n", hi, lo);
                first++;
            }
            onlya++; i++;
        } else {
            if (first < 5) {
                unsigned long long lo = (unsigned long long)b.a[j];
                unsigned long long hi = (unsigned long long)(b.a[j] >> 64);
                fprintf(stderr, "  only-B %016llx%016llx\n", hi, lo);
                first++;
            }
            onlyb++; j++;
        }
    }
    onlya += na - i;
    onlyb += nb - j;
    printf("rawA %zu distinctA %zu\n", rawn, na);
    printf("rawB %zu distinctB %zu\n", rawb, nb);
    printf("onlyA %zu onlyB %zu\n", onlya, onlyb);
    printf("equal_sets %s\n", (onlya == 0 && onlyb == 0) ? "YES" : "NO");
    return (onlya == 0 && onlyb == 0) ? 0 : 1;
}
