#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>

// Individual labeled vertices, independent of membership-cell counts.
int main(int argc,char** argv) {
    if(argc!=3)return 2;
    std::ifstream input(argv[1]);std::ofstream output(argv[2],std::ios::binary);
    unsigned cases;input>>cases;
    std::uint64_t safe=0;
    for(unsigned test=0;test<cases;++test) {
        unsigned n,h;input>>n>>h;
        std::vector<unsigned> edges(h);for(auto& edge:edges)input>>edge;
        unsigned total=1u<<n;std::vector<std::uint8_t> values(total,255);
        for(int s=int(total)-1;s>=0;--s) {
            bool forbidden=false;
            for(auto edge:edges)if((unsigned(s)&edge)==edge){forbidden=true;break;}
            if(forbidden)continue;
            unsigned options=0;
            for(unsigned v=0;v<n;++v)if(!(s&(1u<<v))) {
                auto child=values[s|(1u<<v)];if(child!=255)options|=1u<<child;
            }
            unsigned g=0;while(options&(1u<<g))++g;
            values[s]=g;++safe;
        }
        output.put(char(values[0]));
    }
    if(!input||!output)return 3;
    std::cout<<"{\"cases\":"<<cases<<",\"safe_states\":"<<safe<<"}\n";
}
