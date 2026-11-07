#include <cassert>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <vector>

int main(int argc,char**argv){
    if(argc!=3)return 2;std::ifstream input(argv[1]);std::ofstream output(argv[2],std::ios::binary);
    unsigned cases;input>>cases;uint64_t states=0;
    for(unsigned row=0;row<cases;++row){
        unsigned n,h;input>>n>>h;assert(h<=8&&n<=24);
        std::vector<uint32_t> edges(h);for(auto&e:edges){input>>e;assert(__builtin_popcount(e)==3);}
        std::vector<unsigned> counts(1U<<h);
        for(unsigned v=0;v<n;++v){unsigned mask=0;for(unsigned e=0;e<h;++e)if(edges[e]>>v&1)mask|=1U<<e;
            assert(mask);++counts[mask];}
        std::vector<unsigned> masks,capacity,stride;unsigned total=1;
        for(unsigned mask=1;mask<counts.size();++mask)if(counts[mask]){
            masks.push_back(mask);capacity.push_back(counts[mask]);stride.push_back(total);total*=counts[mask]+1;}
        std::vector<uint8_t> memo(total,255);std::vector<unsigned> chosen(masks.size()),usage(h);
        std::function<uint8_t(unsigned)> game=[&](unsigned code)->uint8_t{
            if(memo[code]!=255)return memo[code];++states;unsigned options=0;
            for(unsigned i=0;i<masks.size();++i){
                if(chosen[i]==capacity[i])continue;bool legal=true;
                for(unsigned bits=masks[i];bits;bits&=bits-1)if(usage[__builtin_ctz(bits)]==2){legal=false;break;}
                if(!legal)continue;++chosen[i];for(unsigned bits=masks[i];bits;bits&=bits-1)++usage[__builtin_ctz(bits)];
                options|=1U<<game(code+stride[i]);
                for(unsigned bits=masks[i];bits;bits&=bits-1)--usage[__builtin_ctz(bits)];--chosen[i];
            }
            return memo[code]=__builtin_ctz(~options);
        };
        output.put(game(0));
    }
    if(!input||!output)return 3;
    std::cout<<"{\"cases\":"<<cases<<",\"cell_states\":"<<states<<"}\n";
}
