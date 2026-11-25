// Five-dimensional Boolean cube: exact integer Bareiss determinant and
// increasing-subset enumeration of every safe position.
#include <bits/stdc++.h>
using namespace std;
using U = uint32_t;

static int det5(U mask) {
    int p[6], c = 0;
    for (int i = 0; i < 32; ++i) if ((mask >> i) & 1) p[c++] = i;
    assert(c == 6);
    long long a[5][5];
    for (int i = 0; i < 5; ++i)
        for (int j = 0; j < 5; ++j)
            a[i][j] = ((p[i + 1] >> j) & 1) - ((p[0] >> j) & 1);
    long long denom = 1, sign = 1;
    for (int k = 0; k < 4; ++k) {
        if (!a[k][k]) {
            int i = k + 1;
            while (i < 5 && !a[i][k]) ++i;
            if (i == 5) return 0;
            for (int j = 0; j < 5; ++j) swap(a[k][j], a[i][j]);
            sign = -sign;
        }
        long long pivot = a[k][k];
        for (int i = k + 1; i < 5; ++i)
            for (int j = k + 1; j < 5; ++j) {
                long long v = a[i][j] * pivot - a[i][k] * a[k][j];
                assert(v % denom == 0);
                a[i][j] = v / denom;
            }
        for (int i = k + 1; i < 5; ++i) a[i][k] = 0;
        denom = pivot;
    }
    return int(sign * a[4][4]);
}

static unordered_set<U> bad;
static vector<U> safe[33];

static bool extend(U mask, int x, int n) {
    if (n < 5) return true;
    int a[32], c = 0;
    for (int i = 0; i < 32; ++i) if ((mask >> i) & 1) a[c++] = i;
    assert(c == n);
    // Any newly forbidden six-set must contain the added vertex x.
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j)
            for (int k = j + 1; k < n; ++k)
                for (int l = k + 1; l < n; ++l)
                    for (int m = l + 1; m < n; ++m) {
                        U six = (1u << x) | (1u << a[i]) | (1u << a[j])
                              | (1u << a[k]) | (1u << a[l]) | (1u << a[m]);
                        if (bad.count(six)) return false;
                    }
    return true;
}

static void visit(U mask, int next, int n) {
    safe[n].push_back(mask);
    for (int x = next; x < 32; ++x)
        if (extend(mask, x, n)) visit(mask | (1u << x), x + 1, n + 1);
}

static int mex(uint64_t bits) {
    for (int i = 0; i < 63; ++i) if (!((bits >> i) & 1)) return i;
    abort();
}

int main() {
    unsigned long long n6 = 0;
    int max_abs_det = 0;
    for (int a = 0; a < 32; ++a)
        for (int b = a + 1; b < 32; ++b)
            for (int c = b + 1; c < 32; ++c)
                for (int d = c + 1; d < 32; ++d)
                    for (int e = d + 1; e < 32; ++e)
                        for (int f = e + 1; f < 32; ++f) {
                            U mask = (1u << a) | (1u << b) | (1u << c)
                                   | (1u << d) | (1u << e) | (1u << f);
                            int det = det5(mask);
                            max_abs_det = max(max_abs_det, abs(det));
                            if (!det) bad.insert(mask);
                            ++n6;
                        }
    visit(0, 0, 0);
    size_t all = 0;
    for (auto &v : safe) all += v.size();

    unordered_map<U, uint16_t> value;
    value.reserve(all * 2);
    unsigned long long dist[33][64]{}, terminal[33]{}, swap_bad = 0;
    unsigned long long first_g[64]{}, first_h[64]{};
    for (int n = 32; n >= 0; --n)
        for (U mask : safe[n]) {
            uint64_t gm = 0, hm = 0;
            int moves = 0;
            for (int x = 0; x < 32; ++x) if (!((mask >> x) & 1)) {
                auto it = value.find(mask | (1u << x));
                if (it == value.end()) continue;
                ++moves;
                int g = it->second & 255, h = it->second >> 8;
                gm |= 1ull << g;
                hm |= 1ull << h;
            }
            int g = mex(gm), h = moves ? mex(hm) : 1;
            value[mask] = uint16_t(g | (h << 8));
            if (!moves) ++terminal[n];
            ++dist[n][g];
            if ((g == 0 && h != 1) || (g == 1 && h != 0)
                || (g >= 2 && h != g)) ++swap_bad;
            if (n == 1) { ++first_g[g]; ++first_h[h]; }
        }

    assert(n6 == 906192 && bad.size() == 350000 && max_abs_det == 5);
    assert(all == 1108073 && safe[7].size() == 309056 && safe[8].empty());
    assert(terminal[5] == 22240 && terminal[6] == 46080 && terminal[7] == 309056);
    assert((value[0] & 255) == 1 && (value[0] >> 8) == 0 && swap_bad == 0);
    cout << "forbidden6=" << bad.size() << " all_safe=" << all << "\n";
    for (int n = 0; n <= 32; ++n) if (!safe[n].empty()) {
        cout << n << " safe=" << safe[n].size() << " terminal=" << terminal[n] << " g=";
        for (int g = 0; g < 64; ++g) if (dist[n][g]) cout << g << ":" << dist[n][g] << ",";
        cout << "\n";
    }
    cout << "root=" << (value[0] & 255) << "," << (value[0] >> 8)
         << " swap_bad=" << swap_bad << "\n";
    cout << "first_g=";
    for (int i = 0; i < 64; ++i) if (first_g[i]) cout << i << ":" << first_g[i] << ",";
    cout << " first_h=";
    for (int i = 0; i < 64; ++i) if (first_h[i]) cout << i << ":" << first_h[i] << ",";
    cout << "\n";
}
