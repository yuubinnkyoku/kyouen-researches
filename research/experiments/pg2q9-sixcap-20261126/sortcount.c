
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int cmp(const void *a, const void *b) {
    u128 x = *(const u128*)a, y = *(const u128*)b;
    uint64_t xl=(uint64_t)x, xh=(uint64_t)(x>>64), yl=(uint64_t)y, yh=(uint64_t)(y>>64);
    if (xh != yh) return xh < yh ? -1 : 1;
    if (xl != yl) return xl < yl ? -1 : 1;
    return 0;
}
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s file\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "rb");
    if (!f) { perror("open"); return 2; }
    uint64_t n;
    if (fread(&n, 8, 1, f) != 1) { fprintf(stderr, "bad file\n"); return 2; }
    u128 *a = (u128*)malloc((size_t)n * sizeof(u128));
    if (!a) { fprintf(stderr, "OOM\n"); return 2; }
    if (n && fread(a, sizeof(u128), (size_t)n, f) != n) { fprintf(stderr, "short read\n"); return 2; }
    fclose(f);
    qsort(a, (size_t)n, sizeof(u128), cmp);
    uint64_t distinct = n ? 1 : 0;
    for (uint64_t i = 1; i < n; i++) if (cmp(&a[i-1], &a[i]) != 0) distinct++;
    printf("n %llu distinct %llu duplicates %llu\n", (unsigned long long)n, (unsigned long long)distinct, (unsigned long long)(n - distinct));
    return 0;
}
