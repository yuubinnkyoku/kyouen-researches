// Complete sorted-state bottom-up mex DP for odd residual column count n=w-h.
// Example: g++ -std=c++17 -O3 check_global_bound.cpp -o check_global_bound
//          ./check_global_bound 11 11
// Includes ALL 1<=r<h*m, 2<=h<w with odd n, all safe sorted states.
// This is finite evidence, NOT an unbounded proof of Grundy <= 3.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
struct State {
    uint64_t key;
    uint16_t total;
    array<uint8_t, 12> x;
};
int main(int argc, char** argv) {
    const int w = argc > 1 ? stoi(argv[1]) : 11;
    const int m = argc > 2 ? stoi(argv[2]) : 11;
    if (w < 3 || w > 12 || m < 1 || m > 16) return 2;
    array<uint64_t, 12> pw{};
    pw[0] = 1;
    for (int i = 1; i < w; i++) pw[i] = pw[i-1] * (m + 1);
    vector<State> states;
    array<uint8_t, 12> x{};
    function<void(int,int,int,uint64_t)> enumerate =
        [&](int i, int max_next, int total, uint64_t key) {
            if (i == w) { states.push_back({key, (uint16_t)total, x}); return; }
            for (int v = max_next; v >= 0; --v) {
                x[i] = (uint8_t)v;
                enumerate(i + 1, v, total + v, key + (uint64_t)v * pw[i]);
            }
        };
    enumerate(0, m, 0, 0);
    sort(states.begin(), states.end(),
         [](const State& a, const State& b) { return a.total > b.total; });
    unordered_map<uint64_t, size_t> index;
    index.reserve(states.size() * 14 / 10);
    for (size_t i = 0; i < states.size(); i++) index[states[i].key] = i;
    vector<uint8_t> g(states.size());
    uint64_t tested = 0, even_slack_nonbinary = 0;
    array<uint64_t, 5> distribution{};
    int maximum = 0;
    for (int h = 2; h < w; h++) {
        if ((w - h) % 2 == 0) continue; // even n already binary by K0352
        for (int r = 1; r < h * m; r++) {
            for (size_t j = 0; j < states.size(); j++) {
                const State& s = states[j];
                int top = 0;
                for (int i = 0; i < h; i++) top += s.x[i];
                if (top > r) continue;
                uint32_t seen = 0;
                for (int i = 0; i < w; i++) {
                    if (s.x[i] == m || (i && s.x[i] == s.x[i-1])) continue;
                    // Increment the first member of an equal-height group.
                    // The sorted order remains valid; only this digit changes.
                    auto it = index.find(s.key + pw[i]);
                    if (it == index.end()) return 3;
                    const auto& child = states[it->second];
                    int child_top = 0;
                    for (int z = 0; z < h; z++) child_top += child.x[z];
                    if (child_top > r) continue;
                    if (it->second >= j) return 4; // not already evaluated
                    if (g[it->second] >= 31) return 5;
                    seen |= 1u << g[it->second];
                }
                int value = 0;
                while (value < 31 && (seen & (1u << value))) value++;
                if (value >= 5) return 6; // would exceed the histogram
                g[j] = (uint8_t)value;
                distribution[value]++;
                tested++;
                maximum = max(maximum, value);
                if ((r - top) % 2 == 0 && value >= 2) {
                    even_slack_nonbinary++;
                    cerr << "EVEN_SLACK_COUNTEREXAMPLE w=" << w << " h=" << h
                         << " m=" << m << " r=" << r << " g=" << value << " x=";
                    for (int i=0;i<w;i++) cerr << (int)s.x[i] << ',';
                    cerr << "\n";
                    return 7;
                }
                if (value >= 4) {
                    cerr << "G4_COUNTEREXAMPLE w=" << w << " h=" << h
                         << " m=" << m << " r=" << r << " g=" << value << " x=";
                    for (int i=0;i<w;i++) cerr << (int)s.x[i] << ',';
                    cerr << "\n";
                    return 8;
                }
            }
        }
    }
    cout << "PASS w=" << w << " m=" << m << " states=" << tested
         << " maxg=" << maximum << " even_slack_nonbinary=" << even_slack_nonbinary
         << " g0=" << distribution[0] << " g1=" << distribution[1]
         << " g2=" << distribution[2] << " g3=" << distribution[3]
         << " g4=" << distribution[4] << "\n";
    return 0;
}
