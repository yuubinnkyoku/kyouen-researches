// Bounded ceiling experiment, adapted from the existing validated clutter
// generator game_structure_20261003_complexes.cpp. No square-board inference.
// Mode 0: all hereditary complexes on n legal vertices (singletons legal).
// Mode 1: all nonempty complexes D on n named vertices, including absent
// vertices, and K = simplex([n]) union ({b} * D). Thus all n+1 vertices of K
// are legal and its maximum-facet deficit is one, except for D=the simplex.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <vector>
using U = uint64_t;
int n, N, mode;
std::vector<int> edges;
std::vector<U> incompatible, supersets;
U count = 0;
std::map<int,U> histogram;
std::map<int,U> first_witness;
void visit(U rem, U unsafe) {
    if (rem) {
        int i = __builtin_ctzll(rem);
        visit(rem & ~(U(1)<<i), unsafe);
        visit(rem & ~incompatible[i], unsafe | supersets[i]);
        return;
    }
    ++count;
    U safe = ~unsafe;
    if (n<6) safe &= (U(1)<<N)-1;
    unsigned char g[64]{}, height[64]{}, wrapper[64]{};
    for (int s=N-1;s>=0;--s) if ((safe>>s)&1) {
        unsigned seen=0;int h=0;
        for (int p=0;p<n;++p) if (!(s>>p&1)) {
            int c=s|(1<<p);
            if ((safe>>c)&1) {
                seen|=1u<<g[c]; h=std::max(h,int(height[c])+1);
            }
        }
        g[s]=__builtin_ctz(~seen);height[s]=h;
    }
    int value=g[0], h=height[0];
    if (mode==1) {
        for(int s=N-1;s>=0;--s) {
            unsigned seen=0;
            for(int p=0;p<n;++p) if(!(s>>p&1)) seen|=1u<<wrapper[s|(1<<p)];
            if((safe>>s)&1) seen|=1u<<g[s];
            wrapper[s]=__builtin_ctz(~seen);
        }
        value=wrapper[0]; h=n+(((safe>>(N-1))&1)?1:0);
    }
    int key=16*value+h;
    ++histogram[key];
    if(!first_witness.count(key)) first_witness[key]=safe;
}
int main(int argc,char**argv) {
    if(argc!=3) return 1;
    n=std::atoi(argv[1]);mode=std::atoi(argv[2]);
    assert(n>=1&&n<=6&&(mode==0||mode==1));N=1<<n;
    for(int s=1;s<N;++s) if(__builtin_popcount(unsigned(s))>= (mode?1:2)) edges.push_back(s);
    int m=edges.size();
    assert(m<64);
    for(int s:edges) {
        U inc=0,sup=0;
        for(int j=0;j<m;++j) if((s&edges[j])==s || (s&edges[j])==edges[j]) inc|=U(1)<<j;
        for(int t=0;t<N;++t) if((s&t)==s) sup|=U(1)<<t;
        incompatible.push_back(inc);supersets.push_back(sup);
    }
    visit((U(1)<<m)-1,0);
    std::printf("{\"n\":%d,\"mode\":%d,\"families\":%llu,\"grundy_height_histogram\":[",n,mode,(unsigned long long)count);
    bool first=true;
    for(auto [key,c]:histogram) {
        std::printf("%s{\"grundy\":%d,\"height\":%d,\"count\":%llu,\"link_safe_mask\":\"%llu\"}",
            first?"":",",key/16,key%16,(unsigned long long)c,(unsigned long long)first_witness[key]);
        first=false;
    }
    std::printf("]}\n");
}
