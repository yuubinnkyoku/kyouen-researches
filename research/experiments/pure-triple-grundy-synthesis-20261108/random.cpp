#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>

// Bounded witness search. Every candidate is evaluated on the full Boolean
// lattice; a failure to find a witness has no nonexistence implication.
int main(int argc,char**argv){
    uint64_t count=argc>1?std::strtoull(argv[1],nullptr,10):1000000;
    std::mt19937_64 rng(20261108);
    std::vector<int> triples;
    for(int s=1;s<256;++s)if(__builtin_popcount((unsigned)s)==3)triples.push_back(s);
    std::array<uint64_t,256> contained{};
    for(int s=0;s<256;++s)for(int i=0;i<56;++i)
        if((s&triples[i])==triples[i])contained[s]|=1ULL<<i;
    std::array<uint64_t,9> histogram{};
    uint64_t witness=0;int best=0;uint64_t evaluated=0;
    for(uint64_t iteration=0;iteration<count;++iteration){
        // Fixed edge counts 6..35, sampled uniformly at each count.
        int h=6+iteration%30;
        uint64_t family=0;
        while(__builtin_popcountll(family)<h)family|=1ULL<<(rng()%56);
        std::array<uint8_t,256> value{};
        for(int s=255;s>=0;--s){
            if(contained[s]&family)continue;
            unsigned options=0;
            for(int v=0;v<8;++v)if(!(s>>v&1)){
                int child=s|(1<<v);
                if(!(contained[child]&family))options|=1U<<value[child];
            }
            value[s]=__builtin_ctz(~options);
        }
        ++histogram[value[0]];++evaluated;
        if(value[0]>best){best=value[0];witness=family;}
        if(value[0]>=6)break;
    }
    std::cout<<"{\"vertices\":8,\"seed\":20261108,\"evaluated\":"<<evaluated
             <<",\"maximum_found\":"<<best<<",\"histogram\":[";
    for(int g=0;g<9;++g)std::cout<<(g?",":"")<<histogram[g];
    std::cout<<"],\"witness_edges\":[";bool first=true;
    for(int i=0;i<56;++i)if(witness>>i&1){std::cout<<(first?"":",")<<triples[i];first=false;}
    std::cout<<"]}\n";
}
