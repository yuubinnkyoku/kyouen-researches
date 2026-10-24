// Independent full-subset safety DP and reverse Grundy DP. Input: N E masks...
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <vector>
using Mask=uint32_t;
int main(){
    int n,e;if(!(std::cin>>n>>e)||n<1||n>25||e<0)return 2;
    std::vector<std::vector<Mask>> incident(n);
    for(int j=0;j<e;++j){
        Mask edge;std::cin>>edge;
        if(__builtin_popcount(edge)!=4||(edge>>n))return 2;
        for(int i=0;i<n;++i)if(edge&(Mask(1)<<i))incident[i].push_back(edge);
    }
    const Mask size=Mask(1)<<n,full=size-1;
    std::vector<uint8_t> safe(size,0),g(size,255);safe[0]=1;
    for(Mask s=1;s<size;++s){
        Mask bit=s&-s;if(!safe[s^bit])continue;
        int p=__builtin_ctz(bit);bool ok=true;
        for(Mask edge:incident[p])if((s&edge)==edge){ok=false;break;}
        safe[s]=ok;
    }
    std::array<uint64_t,26> layers{},hist{},terminal{};uint64_t states=0;
    for(Mask top=size;top;){
        Mask s=--top;if(!safe[s])continue;
        ++states;int k=__builtin_popcount(s);++layers[k];
        uint64_t options=0;Mask choices=full^s;bool has_move=false;
        while(choices){
            Mask bit=choices&-choices;choices^=bit;
            if(safe[s|bit]){has_move=true;options|=uint64_t(1)<<g[s|bit];}
        }
        unsigned value=0;while(options&(uint64_t(1)<<value))++value;
        g[s]=value;++hist[value];if(!has_move)++terminal[k];
    }
    if(const char* path=std::getenv("KYOUEN_GRUNDY_DUMP")){
        std::ofstream out(path,std::ios::binary);out.write(reinterpret_cast<const char*>(g.data()),g.size());if(!out)return 3;
    }
    auto output_array=[](const auto&a){std::cout<<'[';bool first=true;for(auto x:a){if(!first)std::cout<<',';first=false;std::cout<<uint64_t(x);}std::cout<<']';};
    std::cout<<"{\"empty_grundy\":"<<unsigned(g[0])<<",\"safe_count\":"<<states<<",\"safe_layers\":";
    output_array(layers);std::cout<<",\"terminal_sizes\":";output_array(terminal);
    std::cout<<",\"grundy_histogram\":";output_array(hist);
    std::vector<unsigned> first;for(int i=0;i<n;++i)first.push_back(g[Mask(1)<<i]);
    std::cout<<",\"first_move_grundy\":";output_array(first);std::cout<<"}\n";
}
