// Independent fixed-edge enumeration using four-cycle masks and Gosper subsets.
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;

int main(int argc, char **argv) {
    if (argc != 3) return 2;
    int n = atoi(argv[1]), wanted = atoi(argv[2]);
    if (n < 4 || n > 9 || wanted < 2 || wanted >= n*(n-1)/2) return 2;
    array<array<int,9>,9> index{};
    int m = 0;
    for (int u=0; u<n; ++u) for (int v=u+1; v<n; ++v)
        index[u][v] = index[v][u] = m++;
    auto edge = [&](int u, int v) { return uint64_t(1) << index[u][v]; };
    vector<uint64_t> cycles;
    for (int a=0; a<n; ++a) for (int b=a+1; b<n; ++b)
        for (int c=b+1; c<n; ++c) for (int d=c+1; d<n; ++d) {
            cycles.push_back(edge(a,b)|edge(b,c)|edge(c,d)|edge(d,a));
            cycles.push_back(edge(a,b)|edge(b,d)|edge(d,c)|edge(c,a));
            cycles.push_back(edge(a,c)|edge(c,b)|edge(b,d)|edge(d,a));
        }
    vector<uint64_t> incidents(n);
    for (int u=0; u<n; ++u) for (int v=0; v<n; ++v)
        if (u != v) incidents[u] |= edge(u,v);
    uint64_t free_count=0, saturated=0, checked=0;
    uint64_t all=(uint64_t(1)<<m)-1;
    uint64_t x=(uint64_t(1)<<(wanted-1))-1, limit=uint64_t(1)<<(m-1);
    while (x < limit) {
        uint64_t state=(x<<1)|1;
        ++checked;
        bool safe=true;
        for (uint64_t c: cycles) if ((state & c)==c) { safe=false; break; }
        if (safe) {
            ++free_count;
            bool isolated=false;
            for (auto incident: incidents) if (!(incident & state)) { isolated=true; break; }
            if (!isolated) {
                uint64_t missing=all & ~state, blocked=0;
                for (uint64_t c: cycles)
                    if (__builtin_popcountll(c & state)==3) blocked |= c & ~state;
                if ((blocked & missing)==missing) ++saturated;
            }
        }
        uint64_t low=x & -x, next=x+low;
        x=next | (((next ^ x) >> 2) / low);
    }
    cout << "n=" << n << " edges=" << wanted << " fixed_edge=0-1"
         << " checked=" << checked << " c4_free=" << free_count
         << " saturated=" << saturated << '\n';
}
