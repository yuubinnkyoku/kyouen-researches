// Independent full census: translated determinant geometry and direct D4 maps.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <unordered_map>
#include <vector>
using M = __uint128_t;
struct Hash { size_t operator()(M m) const { return uint64_t(m) ^ (uint64_t(m >> 64)*0x9e3779b97f4a7c15ULL); } };
const M full = (M(1)<<121)-1;
std::array<std::array<int,121>,8> maps;
std::unordered_map<int,M> completions;
std::vector<int> points(M m) {
    std::vector<int> r;
    for (int p=0;p<121;++p) if ((m>>p)&1) r.push_back(p);
    return r;
}
M transform(M m,int t) {
    M out=0;
    uint64_t lo=uint64_t(m), hi=uint64_t(m>>64);
    while(lo) { int p=std::countr_zero(lo); out|=M(1)<<maps[t][p]; lo&=lo-1; }
    while(hi) { int p=64+std::countr_zero(hi); out|=M(1)<<maps[t][p]; hi&=hi-1; }
    return out;
}
M canonical(M m) {
    M out=m;
    for(int t=1;t<8;++t) out=std::min(out,transform(m,t));
    return out;
}
std::array<int64_t,3> row(int p,int a) {
    int64_t x=p%11-a%11, y=p/11-a/11;
    return {x,y,x*x+y*y};
}
M completion(int a,int b,int c) {
    int key=(a*121+b)*121+c;
    auto it=completions.find(key);
    if(it!=completions.end()) return it->second;
    auto u=row(b,a), v=row(c,a);
    M out=0;
    for(int p=0;p<121;++p) {
        auto w=row(p,a);
        int64_t det=u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0]);
        if(!det) out|=M(1)<<p;
    }
    completions.emplace(key,out);
    return out;
}
int main() {
    try {
        for(int p=0;p<121;++p) {
            int x=p%11,y=p/11;
            for(int reflected=0;reflected<2;++reflected) {
                int a=reflected?10-x:x,b=y;
                for(int turn=0;turn<4;++turn) {
                    maps[4*reflected+turn][p]=11*b+a;
                    int old=a; a=10-b; b=old;
                }
            }
        }
        size_t count=0, edges=0, orbits=0, incidence=0, extra=0, extra_parents=0;
        std::unordered_map<M,int,Hash> union_counts;
        uint64_t index,lo,hi; int expected_legal,expected_stab,expected_orbits,expected_children;
        while(std::cin>>index>>lo>>hi>>expected_legal>>expected_stab>>expected_orbits>>expected_children) {
            M mask=M(lo)|(M(hi)<<64);
            auto pts=points(mask);
            if(mask & ~full || pts.size()!=5 || canonical(mask)!=mask) throw std::runtime_error("invalid parent");
            M blocked=mask;
            for(size_t i=0;i<5;++i) for(size_t j=i+1;j<5;++j) for(size_t k=j+1;k<5;++k) {
                M curve=completion(pts[i],pts[j],pts[k]);
                M triple=(M(1)<<pts[i])|(M(1)<<pts[j])|(M(1)<<pts[k]);
                if(curve & (mask ^ triple)) throw std::runtime_error("unsafe parent");
                blocked |=curve;
            }
            auto moves=points(full & ~blocked);
            int stab=0, fixed=0;
            for(int t=0;t<8;++t) if(transform(mask,t)==mask) {
                ++stab;
                for(int p:moves) fixed+=maps[t][p]==p;
            }
            if(fixed%stab) throw std::runtime_error("nonintegral Burnside");
            std::vector<M> children;
            for(int p:moves) children.push_back(canonical(mask|(M(1)<<p)));
            std::sort(children.begin(),children.end());
            children.erase(std::unique(children.begin(),children.end()),children.end());
            if(int(moves.size())!=expected_legal || stab!=expected_stab || fixed/stab!=expected_orbits || int(children.size())!=expected_children) {
                std::cerr<<"mismatch parent="<<index<<" actual="<<moves.size()<<","<<stab<<","<<fixed/stab<<","<<children.size()<<"\n";
                return 1;
            }
            ++count; edges+=moves.size(); orbits+=fixed/stab; incidence+=children.size();
            extra+=fixed/stab-children.size(); extra_parents+=int(children.size())<fixed/stab;
            for(M c:children) ++union_counts[c];
        }
        if(!std::cin.eof() || !count) throw std::runtime_error("invalid/empty input");
        size_t shared=0,duplicates=0; std::unordered_map<int,size_t> multiplicity;
        for(auto [child,n]:union_counts) { (void)child; shared+=n>1; duplicates+=n-1; ++multiplicity[n]; }
        std::cout<<"{\"passed\":true,\"parents\":"<<count<<",\"legal_edges\":"<<edges
                 <<",\"stabilizer_orbits\":"<<orbits<<",\"canonical_child_incidence\":"<<incidence
                 <<",\"distinct_children\":"<<union_counts.size()<<",\"shared_children\":"<<shared
                 <<",\"cross_parent_duplicate_incidence\":"<<duplicates
                 <<",\"extra_merges\":"<<extra<<",\"parent_extra_merge_count\":"<<extra_parents<<",\"child_parent_multiplicity\":{";
        std::vector<int> keys; for(auto [n,c]:multiplicity) { (void)c; keys.push_back(n); }
        std::sort(keys.begin(),keys.end());
        for(size_t i=0;i<keys.size();++i) { if(i) std::cout<<","; std::cout<<"\""<<keys[i]<<"\":"<<multiplicity[keys[i]]; }
        std::cout<<"}}\n";
    } catch(const std::exception& e) { std::cerr<<e.what()<<"\n"; return 1; }
}
