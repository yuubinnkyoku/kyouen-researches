#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>

// No residual cleanup, small-core table, canonicalization, or Python recurrence.
// The raw independent-set placement game is evaluated for every family and subset.
int main(int argc, char** argv) {
    if (argc != 2) return 2;
    std::vector<unsigned> triples;
    for (unsigned a=0;a<6;++a)
        for (unsigned b=a+1;b<6;++b)
            for (unsigned c=b+1;c<6;++c)
                triples.push_back((1u<<a)|(1u<<b)|(1u<<c));
    std::array<unsigned,64> inside{};
    for (unsigned s=0;s<64;++s)
        for (unsigned j=0;j<20;++j)
            if ((s & triples[j])==triples[j]) inside[s] |= 1u<<j;
    std::array<std::uint64_t,7> histogram{};
    std::vector<std::uint8_t> roots(1u<<20);
    std::uint64_t safe_states=0;
    for (unsigned family=0;family<(1u<<20);++family) {
        std::array<std::uint8_t,64> value;
        value.fill(255);
        for (int s=63;s>=0;--s) {
            if (inside[s] & family) continue;
            unsigned options=0;
            for (unsigned v=0;v<6;++v) {
                if (s & (1u<<v)) continue;
                auto child=value[s | (1u<<v)];
                if (child!=255) options |= 1u<<child;
            }
            unsigned g=0;
            while (options & (1u<<g)) ++g;
            value[s]=g;
            ++safe_states;
        }
        roots[family]=value[0];
        ++histogram[value[0]];
    }
    std::ofstream out(argv[1],std::ios::binary);
    out.write(reinterpret_cast<const char*>(roots.data()),roots.size());
    if (!out) return 3;
    std::cout << "{\"families\":" << roots.size() << ",\"safe_states\":" << safe_states << ",\"histogram\":[";
    for (unsigned i=0;i<7;++i) std::cout << (i ? ",":"") << histogram[i];
    std::cout << "]}\n";
}
