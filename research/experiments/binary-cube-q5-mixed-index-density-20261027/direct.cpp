#include <bits/stdc++.h>
using namespace std;
using ull = unsigned long long;

static ull modpow(ull a, ull e, ull p) {
    ull z = 1;
    while (e) {
        if (e & 1) z = z * a % p;
        a = a * a % p;
        e >>= 1;
    }
    return z;
}
static constexpr int BASES[] = {2, 3, 5, 7};
static constexpr int ODD[] = {3, 5, 7, 9, 15, 21, 35, 105};
static constexpr int MAX_R = 4;

int main(int argc, char **argv) {
    int limit = argc > 1 ? atoi(argv[1]) : 10000000;
    if (limit < 37 || limit > 100000000) return 2;
    vector<bool> composite(limit, false);
    for (int i = 2; 1LL * i * i < limit; ++i)
        if (!composite[i])
            for (int j = i * i; j < limit; j += i) composite[j] = true;

    long long count[MAX_R][8] = {}, first[MAX_R][8] = {};
    long long prime_count = 0;
    for (int p = 37; p < limit; p += 2) {
        if (composite[p]) continue;
        ++prime_count;
        int v2 = 0;
        for (int r = 1; r <= MAX_R && (p - 1) % (1 << r) == 0; ++r) {
            ull e = (p - 1) / (1 << r);
            bool ok = true;
            for (int a : BASES)
                if (modpow(a, e, p) != 1) { ok = false; break; }
            if (!ok) break;
            v2 = r;
        }
        for (int j = 0; j < 8; ++j) {
            int n = ODD[j];
            if ((p - 1) % n != 0) continue;
            ull e = (p - 1) / n;
            bool ok = true;
            for (int a : BASES)
                if (modpow(a, e, p) != 1) { ok = false; break; }
            if (!ok) continue;
            for (int r = 1; r <= v2; ++r) {
                ++count[r - 1][j];
                if (!first[r - 1][j]) first[r - 1][j] = p;
            }
        }
    }
    cout << "p<" << limit << " primes=" << prime_count << "\n";
    for (int r = 1; r <= MAX_R; ++r)
        for (int j = 0; j < 8; ++j)
            cout << "r=" << r << " n=" << ODD[j]
                 << " count=" << count[r - 1][j]
                 << " first=" << first[r - 1][j] << "\n";
}
