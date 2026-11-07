#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>

#ifndef MAX_LEGAL_POINTS
#define MAX_LEGAL_POINTS 21
#endif
static_assert(MAX_LEGAL_POINTS<=24);

int main(int argc,char**argv){
    if(argc!=4)return 2;
    std::ifstream input(argv[1]);std::ofstream output(argv[2],std::ios::binary);
    uint64_t count;input>>count;uint64_t safe_count=0;
    for(uint64_t row=0;row<count;++row){
        int n,h;input>>n>>h;if(n>MAX_LEGAL_POINTS||n<0)return 3;
        std::vector<int> edges(h);for(auto&edge:edges)input>>edge;
        std::vector<uint8_t> safe(1<<n),g(1<<n),misere(1<<n);
        for(int s=(1<<n)-1;s>=0;--s){
            bool valid=true;for(int edge:edges)if((s&edge)==edge){valid=false;break;}
            if(!valid)continue;
            safe[s]=1;++safe_count;unsigned normal_options=0,misere_options=0;int moves=0;
            for(int v=0;v<n;++v)if(!(s>>v&1)&&safe[s|(1<<v)]){
                ++moves;normal_options|=1U<<g[s|(1<<v)];
                misere_options|=1U<<misere[s|(1<<v)];
            }
            g[s]=__builtin_ctz(~normal_options);
            misere[s]=moves?__builtin_ctz(~misere_options):1;
        }
        output.put(g[0]);output.put(misere[0]);
    }
    output.close();std::ofstream metadata(argv[3]);
    metadata<<"{\"cases\":"<<count<<",\"safe_states\":"<<safe_count<<"}\n";
    return input&&output?0:4;
}
