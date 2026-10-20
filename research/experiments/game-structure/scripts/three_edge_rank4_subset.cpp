// Independent subset-based verifier of the three-edge, rank<=4 Venn census.
// Uses explicit labelled vertices and occupied-set mex, NOT the class-count DP.
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;

int main(int argc, char** argv) {
    bool cases=(argc>1 && std::string(argv[1])=="--cases");
    array<long long, 8> histogram{};
    array<long long, 13*8> by_size{};
    long long configurations = 0;
    int max_grundy = 0;
    array<int,7> witness{};
    int best_size = 99;
    for (int code=0; code<78125; ++code) {
        int digits[7], t=code;
        for(int i=0;i<7;++i) { digits[i]=t%5; t/=5; }
        uint16_t edges[3]={};
        int n=0;
        for(int p=1;p<=7;++p) {
            for(int j=0;j<digits[p-1];++j) {
                uint16_t bit=uint16_t(1u<<n++);
                for(int k=0;k<3;++k) if(p&(1<<k)) edges[k]|=bit;
            }
        }
        bool valid=true;
        for(int k=0;k<3;++k) {
            int z=__builtin_popcount((unsigned)edges[k]);
            if(z<2 || z>4) valid=false;
            for(int j=0;j<3;++j)
                if(k!=j && (edges[k]&edges[j])==edges[k]) valid=false;
        }
        if(!valid) continue;
        assert(n<=12);
        ++configurations;
        vector<int8_t> memo(1u<<n,-1);
        auto solve=[&](auto&& self,uint16_t occupied)->int {
            int8_t &cached=memo[occupied];
            if(cached!=-1)return cached;
            uint16_t legal_mask=uint16_t(((1u<<n)-1u)&~occupied);
            unsigned seen=0;
            while(legal_mask) {
                uint16_t bit=uint16_t(legal_mask & -legal_mask);
                legal_mask^=bit;
                uint16_t next=occupied|bit;
                if((next&edges[0])==edges[0] ||
                   (next&edges[1])==edges[1] ||
                   (next&edges[2])==edges[2]) continue;
                seen |= 1u<<self(self,next);
            }
            int g=0;
            while(seen & (1u<<g)) ++g;
            cached=int8_t(g);
            return g;
        };
        int g=solve(solve,0);
        assert(g<8);
        if(cases) cout<<code<<","<<g<<"\n";
        ++histogram[g];
        ++by_size[n*8+g];
        if(g>max_grundy || (g==max_grundy && n<best_size)) {
            max_grundy=g;
            best_size=n;
            for(int i=0;i<7;++i)witness[i]=digits[i];
        }
    }
    if(!cases) cout<<"configs="<<configurations<<" max="<<max_grundy<<" histogram=";
    if(!cases) for(int i=0;i<8;++i)cout<<(i?",":"")<<histogram[i];
    if(!cases) cout<<"\nmin_witness_size="<<best_size<<" counts=";
    if(!cases) {for(int i=0;i<7;++i)cout<<(i?",":"")<<witness[i];
    cout<<"\n";}
    assert(configurations==562);
    assert(histogram[0]==228 && histogram[1]==231 && histogram[2]==49 && histogram[3]==54);
    for(int i=4;i<8;++i)assert(histogram[i]==0);
}
