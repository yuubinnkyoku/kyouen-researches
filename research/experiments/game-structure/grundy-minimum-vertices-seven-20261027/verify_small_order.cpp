// Exhaustive labelled-cover / unlabelled-outside check of small-order bounds.
// Independent individual-vertex Node Kayles recursion, no twin compression.
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
using namespace std;

static array<int, 1024> memo;
static array<int, 10> closed_neigh;
static long long hist[16], cases;
static int cover, vertices, outside, signatures[10];

int grundy(int mask) {
    if (!mask) return 0;
    int &ans = memo[mask];
    if (ans >= 0) return ans;
    unsigned seen = 0;
    for (int todo = mask; todo; todo &= todo - 1) {
        const int v = __builtin_ctz((unsigned)todo);
        const int child = grundy(mask & ~closed_neigh[v]);
        if (child >= 31) abort();
        seen |= 1u << child;
    }
    ans = 0;
    while ((seen >> ans) & 1u) ++ans;
    return ans;
}

void inspect() {
    const int possible_cover_edges = cover * (cover - 1) / 2;
    for (int ed = 0; ed < (1 << possible_cover_edges); ++ed) {
        for (int v = 0; v < vertices; ++v) closed_neigh[v] = 1 << v;
        int b = 0;
        for (int i = 0; i < cover; ++i) {
            for (int j = i + 1; j < cover; ++j, ++b) {
                if ((ed >> b) & 1) {
                    closed_neigh[i] |= 1 << j;
                    closed_neigh[j] |= 1 << i;
                }
            }
        }
        for (int t = 0; t < outside; ++t) {
            for (int i = 0; i < cover; ++i) {
                if ((signatures[t] >> i) & 1) {
                    closed_neigh[cover + t] |= 1 << i;
                    closed_neigh[i] |= 1 << (cover + t);
                }
            }
        }
        memo.fill(-1);
        const int value = grundy((1 << vertices) - 1);
        if (value >= 16) abort();
        ++hist[value];
        ++cases;
    }
}

void generate(int pos, int first) {
    if (pos == outside) {
        inspect();
        return;
    }
    for (int sig = first; sig < (1 << cover); ++sig) {
        signatures[pos] = sig;
        generate(pos + 1, sig);
    }
}

void check(int n, int k, int bound, long long expected,
           const array<long long, 6> &expected_hist) {
    vertices = n;
    cover = k;
    outside = n - k;
    for (auto &h : hist) h = 0;
    cases = 0;
    generate(0, 0);
    int maximum = 0;
    for (int g = 0; g < 16; ++g)
        if (hist[g]) maximum = g;
    printf("n=%d cover=%d cases=%lld maximum=%d histogram=",
           n, k, cases, maximum);
    for (int g = 0; g <= maximum; ++g)
        printf("%s%lld", g ? "," : "", hist[g]);
    puts("");
    if (cases != expected || maximum > bound) exit(1);
    for (int g = 0; g < 6; ++g)
        if (hist[g] != expected_hist[g]) exit(2);
}

int main() {
    // C(20,5)*2^6 = 992,256; all 9-vertex graphs with a 4-cover.
    check(9, 4, 5, 992256, {109045, 262211, 103504,
                            318696, 111202, 87598});
    // C(14,7)*2^3 = 27,456; all 10-vertex graphs with a 3-cover.
    check(10, 3, 5, 27456, {2146, 8517, 1797,
                             12425, 1491, 1080});
}
