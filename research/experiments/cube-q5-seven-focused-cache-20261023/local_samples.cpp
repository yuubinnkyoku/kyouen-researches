#define Q5_HYBRID_LIBRARY
#include "endgame.cpp"
#undef Q5_HYBRID_LIBRARY
#include <set>
int main() {
    Incremental s(7,0,1000000);s.direct=true;std::mt19937 random(20261024);
    std::set<Mask> seen;
    for(int trial=0;trial<100000 && seen.size()<16;trial++) {
        Mask occupied,live=s.full_live(occupied);
        while(live.count()>10) {
            auto options=live.ids();int p=options[random()%options.size()];
            live=s.advance(occupied,live,p);occupied.set(p);
        }
        if(live.count()<6)continue;
        auto options=live.ids();std::vector<uint16_t> adjacent;
        for(int p:options) {
            Mask next=s.advance(occupied,live,p);uint16_t bits=0;
            for(size_t j=0;j<options.size();j++)if(next.has(options[j]))bits|=uint16_t(1)<<j;
            adjacent.push_back(bits);
        }
        bool triangle=false;
        for(size_t i=0;i<options.size();i++)for(size_t j=i+1;j<options.size();j++)
            if((adjacent[i]>>j&1) && (adjacent[i]&adjacent[j]))triangle=true;
        if(!triangle)continue;
        Mask key=s.canonical(occupied);if(!seen.insert(key).second)continue;
        bool comma=false;for(int p:key.ids()){if(comma)std::cout<<" ";comma=true;std::cout<<p;}std::cout<<"\n";
    }
    return seen.size()==16?0:1;
}
