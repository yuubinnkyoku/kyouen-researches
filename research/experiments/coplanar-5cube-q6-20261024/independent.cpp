// Independent audit: modular rank of the augmented 6x6 binary matrix,
// direct enumeration of every k-subset (k <= 8), and a separate mex pass.
// Hadamard: |det| <= (sqrt(6))^6 = 216 < 1009, so mod 1009 is exact.
#include <bits/stdc++.h>
using namespace std;
using U = uint32_t;
constexpr int MOD = 1009;
static int inverse[MOD];

static bool singular6(U mask) {
    int a[6][6]{}, r = 0;
    for (int v = 0; v < 32; ++v) if ((mask >> v) & 1) {
        a[r][0] = 1;
        for (int j = 0; j < 5; ++j) a[r][j + 1] = (v >> j) & 1;
        ++r;
    }
    assert(r == 6);
    for (int j = 0; j < 6; ++j) {
        int p = j;
        while (p < 6 && !a[p][j]) ++p;
        if (p == 6) return true;
        if (p != j)
            for (int k = 0; k < 6; ++k) swap(a[p][k], a[j][k]);
        int z = inverse[a[j][j]];
        for (int i = j + 1; i < 6; ++i) if (a[i][j]) {
            int c = a[i][j] * z % MOD;
            for (int k = j; k < 6; ++k)
                a[i][k] = (a[i][k] - c * a[j][k] % MOD + MOD) % MOD;
        }
    }
    return false;
}

static uint64_t next_combination(uint64_t x) {
    uint64_t u = x & -x, v = x + u;
    return v + (((v ^ x) / u) >> 2);
}

static unordered_set<U> bad6, safe7;
static vector<U> level[9];

static int mex(uint64_t bits) {
    int i = 0;
    while ((bits >> i) & 1) ++i;
    return i;
}

int main() {
    inverse[1] = 1;
    for (int i = 2; i < MOD; ++i)
        inverse[i] = MOD - (MOD / i) * inverse[MOD % i] % MOD;
    constexpr uint64_t END = 1ull << 32;
    level[0].push_back(0);
    for (int k = 1; k <= 8; ++k) {
        for (uint64_t x = (1ull << k) - 1; x < END; x = next_combination(x)) {
            U mask = U(x);
            bool ok = true;
            if (k == 6) {
                ok = !singular6(mask);
                if (!ok) bad6.insert(mask);
            } else if (k == 7) {
                for (int i = 0; i < 32; ++i) if ((mask >> i) & 1)
                    if (bad6.count(mask ^ (1u << i))) { ok = false; break; }
            } else if (k == 8) {
                // An eight-set is safe iff all its seven-subsets are safe.
                for (int i = 0; i < 32; ++i) if ((mask >> i) & 1)
                    if (!safe7.count(mask ^ (1u << i))) { ok = false; break; }
            }
            if (ok) {
                level[k].push_back(mask);
                if (k == 7) safe7.insert(mask);
            }
        }
    }
    size_t nstates = 0;
    for (auto &v : level) nstates += v.size();
    unordered_map<U, uint16_t> values;
    values.reserve(nstates * 2);
    uint64_t terminal[9]{}, dist[9][16]{}, swap_bad = 0;
    uint64_t dual6 = 0, nonterminal5 = 0;
    for (int k = 8; k >= 0; --k) for (U mask : level[k]) {
        uint64_t gb = 0, hb = 0;
        int children = 0;
        bool has_terminal6 = false, has_nonterminal6 = false;
        for (int p = 0; p < 32; ++p) if (!((mask >> p) & 1)) {
            auto it = values.find(mask | (1u << p));
            if (it == values.end()) continue;
            ++children;
            int g = it->second & 255, h = it->second >> 8;
            gb |= 1ull << g;
            hb |= 1ull << h;
            if (k == 5) {
                if (g == 0) has_terminal6 = true;
                if (g == 1) has_nonterminal6 = true;
            }
        }
        int g = mex(gb), h = children ? mex(hb) : 1;
        values.emplace(mask, uint16_t(g | (h << 8)));
        if (!children) ++terminal[k];
        ++dist[k][g];
        if ((g == 0 && h != 1) || (g == 1 && h != 0)
            || (g >= 2 && h != g)) ++swap_bad;
        if (k == 5 && children) {
            ++nonterminal5;
            if (has_terminal6 && has_nonterminal6) ++dual6;
        }
    }

    assert(bad6.size() == 350000 && nstates == 1108073 && level[8].empty());
    assert(terminal[5] == 22240 && terminal[6] == 46080 && terminal[7] == 309056);
    assert((values.at(0) & 255) == 1 && (values.at(0) >> 8) == 0);
    assert(swap_bad == 0 && dual6 == 107040);
    cout << "forbidden6=" << bad6.size() << " all_safe=" << nstates
         << " root=" << (values.at(0) & 255) << "," << (values.at(0) >> 8)
         << " swap_bad=" << swap_bad << "\n";
    for (int k = 0; k <= 8; ++k) {
        cout << k << " safe=" << level[k].size() << " terminal=" << terminal[k] << " g=";
        for (int i = 0; i < 16; ++i) if (dist[k][i]) cout << i << ":" << dist[k][i] << ",";
        cout << "\n";
    }
    cout << "nonterminal5=" << nonterminal5 << " dual6=" << dual6 << "\n";
}
