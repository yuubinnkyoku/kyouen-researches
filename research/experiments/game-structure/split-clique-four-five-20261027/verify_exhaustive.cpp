// Exact enumeration of split Node Kayles graphs with a clique of size <= 4,
// and of five-clique graphs with at most seven non-isolated independent vertices.
// Compile: c++ -std=c++17 -O3 -Wall -Wextra -pedantic verify_exhaustive.cpp -o /tmp/split_verify
#include <bits/stdc++.h>
using namespace std;

int pow3[17];
vector<int8_t> memo[5];

// Each independent-vertex neighborhood signature has count 0, 1, or 2.
// The positive parity reduction is justified by the independent-twin theorem K0336.
int encode(const int* counts, int n) {
    int key = 0;
    for (int i = 0; i < n; ++i) key += counts[i] * pow3[i];
    return key;
}

int grundy(int k, int key) {
    auto& cache = memo[k];
    if (cache[key] >= 0) return cache[key];
    int n = 1 << k, counts[16] = {}, tmp = key;
    for (int i = 0; i < n; ++i) {
        counts[i] = tmp % 3;
        tmp /= 3;
    }
    if (k == 0) return cache[key] = counts[0] % 2;
    int values = 0;
    // Choosing a clique vertex leaves an independent set.
    for (int v = 0; v < k; ++v) {
        int parity = 0;
        for (int s = 0; s < n; ++s)
            if (!(s & (1 << v))) parity ^= counts[s] & 1;
        values |= 1 << parity;
    }
    // Choosing an independent vertex removes its clique neighbors.
    for (int s = 0; s < n; ++s) if (counts[s]) {
        int remaining = (n - 1) & ~s;
        int subk = __builtin_popcount((unsigned)remaining);
        int projected[16] = {};
        for (int t = 0; t < n; ++t) {
            int p = 0, j = 0;
            for (int v = 0; v < k; ++v) if (remaining & (1 << v)) {
                if (t & (1 << v)) p |= 1 << j;
                ++j;
            }
            projected[p] += counts[t] - (s == t);
        }
        for (int i = 0; i < (1 << subk); ++i)
            if (projected[i]) projected[i] = (projected[i] & 1) ? 1 : 2;
        values |= 1 << grundy(subk, encode(projected, 1 << subk));
    }
    int g = 0;
    while (values & (1 << g)) ++g;
    return cache[key] = g;
}

int grundy_five(const int* counts) {
    int values = 0;
    for (int v = 0; v < 5; ++v) {
        int parity = 0;
        for (int s = 0; s < 32; ++s)
            if (!(s & (1 << v))) parity ^= counts[s] & 1;
        values |= 1 << parity;
    }
    for (int s = 1; s < 32; ++s) if (counts[s]) {
        int remaining = 31 & ~s;
        int subk = __builtin_popcount((unsigned)remaining);
        int projected[16] = {};
        for (int t = 1; t < 32; ++t) {
            int p = 0, j = 0;
            for (int v = 0; v < 5; ++v) if (remaining & (1 << v)) {
                if (t & (1 << v)) p |= 1 << j;
                ++j;
            }
            projected[p] += counts[t] - (s == t);
        }
        for (int i = 0; i < (1 << subk); ++i)
            if (projected[i]) projected[i] = (projected[i] & 1) ? 1 : 2;
        values |= 1 << grundy(subk, encode(projected, 1 << subk));
    }
    int g = 0;
    while (values & (1 << g)) ++g;
    return g;
}

int main() {
    pow3[0] = 1;
    for (int i = 1; i <= 16; ++i) pow3[i] = 3 * pow3[i - 1];
    for (int k = 0; k <= 4; ++k) memo[k].assign(pow3[1 << k], -1);

    long long hist4[5] = {};
    for (int x = 0; x < pow3[15]; ++x) {
        // Signature zero (isolated vertices) is absent; all other 15
        // signatures independently have counts 0, 1, or 2.
        int g = grundy(4, 3 * x);
        if (g > 3) return cerr << "counterexample c4: " << x << "\n", 1;
        ++hist4[g];
    }
    cout << "c4: " << pow3[15] << " signatures; g0..3 =";
    for (int i = 0; i < 4; ++i) cout << " " << hist4[i];
    cout << "\n";

    long long checked = 0;
    for (int n = 0; n <= 7; ++n) {
        int sorted[8] = {};
        for (int i = 0; i < n; ++i) sorted[i] = 1;
        long long hist[5] = {};
        while (true) {
            int counts[32] = {};
            for (int i = 0; i < n; ++i) ++counts[sorted[i]];
            for (int s = 1; s < 32; ++s)
                if (counts[s] > 2) counts[s] = (counts[s] & 1) ? 1 : 2;
            int g = grundy_five(counts);
            if (g > 3) return cerr << "counterexample c5, n=" << n << "\n", 1;
            ++hist[g];
            ++checked;
            int i = n - 1;
            while (i >= 0 && sorted[i] == 31) --i;
            if (i < 0) break;
            int next = sorted[i] + 1;
            for (int j = i; j < n; ++j) sorted[j] = next;
        }
        cout << "c5 independent=" << n << " g0..3 =";
        for (int i = 0; i < 4; ++i) cout << " " << hist[i];
        cout << "\n";
    }
    if (checked != 12620256LL) return cerr << "count mismatch\n", 1;

    int witness[32] = {};
    for (int s : {2, 8, 11, 11, 12, 14, 24, 26}) ++witness[s];
    if (grundy_five(witness) != 4) return cerr << "witness mismatch\n", 1;
    cout << "c5 <=7 independent: " << checked
         << " multisets, g<=3; c5 with 8 independent: g=4\n";
}
