// Independent AND/OR certificate checker. Does not invoke the search solver.
// Geometry uses fraction-free 5x5 Bareiss determinants, not cofactor normals.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using U=__uint128_t;
struct Hash {
    size_t operator()(U v)const {
        uint64_t x=uint64_t(v)^(uint64_t(v>>64)*0x9e3779b97f4a7c15ULL);
        x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;x*=0x94d049bb133111ebULL;
        return x^(x>>31);
    }
};
int count(U a){return __builtin_popcountll(uint64_t(a))+__builtin_popcountll(uint64_t(a>>64));}
std::vector<int> elements(U v) {
    std::vector<int> r;
    while(v) {
        int p=uint64_t(v)?__builtin_ctzll(uint64_t(v)):64+__builtin_ctzll(uint64_t(v>>64));
        r.push_back(p);v&=v-1;
    }
    return r;
}
using Matrix=std::array<std::array<int64_t,5>,5>;
int64_t determinant(Matrix a) {
    int sign=1;int64_t previous=1;
    for(int i=0;i<4;i++) {
        int pivot=i;while(pivot<5 && !a[pivot][i])++pivot;
        if(pivot==5)return 0;
        if(pivot!=i){std::swap(a[pivot],a[i]);sign=-sign;}
        int64_t value=a[i][i];
        for(int j=i+1;j<5;j++)for(int k=i+1;k<5;k++) {
            __int128 numerator=__int128(a[j][k])*value-__int128(a[j][i])*a[i][k];
            if(numerator%previous)throw std::runtime_error("nonexact Bareiss division");
            a[j][k]=int64_t(numerator/previous);
        }
        for(int j=i+1;j<5;j++)a[j][i]=0;
        previous=value;
    }
    return sign*a[4][4];
}
struct Entry {int label;U witness;};
int main(int argc,char**argv) {
    try {
        if(argc!=2)throw std::runtime_error("usage: verify_certificate file.cert");
        std::ifstream input(argv[1]);
        std::string magic;int side;uint64_t lo,hi;
        if(!(input>>magic>>side>>lo>>hi) || magic!="Q5CUBE1" || side<3 || side>5)
            throw std::runtime_error("bad header");
        int n=side*side*side;U all=(U(1)<<n)-1,root=U(lo)|(U(hi)<<64);
        if(root&~all)throw std::runtime_error("root outside board");
        std::unordered_map<U,Entry,Hash> rows;
        while(input>>lo) {
            int label;uint64_t wlo,whi;
            if(!(input>>hi>>label>>wlo>>whi))throw std::runtime_error("truncated row");
            U mask=U(lo)|(U(hi)<<64),witness=U(wlo)|(U(whi)<<64);
            if((mask&~all) || label<0 || label>1 || (!label && witness))throw std::runtime_error("invalid row");
            if(!rows.emplace(mask,Entry{label,witness}).second)throw std::runtime_error("duplicate row");
        }
        if(!input.eof())throw std::runtime_error("invalid trailing data");
        std::vector<std::array<int64_t,5>> lifts;
        for(int x=0;x<side;x++)for(int y=0;y<side;y++)for(int z=0;z<side;z++)
            lifts.push_back({x*x+y*y+z*z,x,y,z,1});
        std::vector<std::vector<int>> transforms;
        std::array<int,3> axes{0,1,2};
        do {for(int flips=0;flips<8;flips++) {
            std::vector<int> mapping;
            for(int p=0;p<n;p++) {
                std::array<int,3> coord{p/(side*side),(p/side)%side,p%side},image{};
                for(int j=0;j<3;j++)image[j]=((flips>>j)&1)?side-1-coord[axes[j]]:coord[axes[j]];
                mapping.push_back((image[0]*side+image[1])*side+image[2]);
            }
            transforms.push_back(mapping);
        }}while(std::next_permutation(axes.begin(),axes.end()));
        auto canonical=[&](U mask) {
            U result=mask;auto points=elements(mask);
            for(const auto& mapping:transforms) {
                U image=0;for(int p:points)image|=U(1)<<mapping[p];
                result=std::min(result,image);
            }
            return result;
        };
        for(const auto& [mask,e]:rows) {
            (void)e;
            if(canonical(mask)!=mask)throw std::runtime_error("noncanonical row");
        }
        std::unordered_map<U,U,Hash> blocked_cache;
        uint64_t determinant_checks=0;
        auto completion=[&](std::array<int,4> points) {
            U key=0;Matrix matrix{};
            for(int j=0;j<4;j++){key|=U(1)<<points[j];matrix[j]=lifts[points[j]];}
            auto it=blocked_cache.find(key);if(it!=blocked_cache.end())return it->second;
            U blocked=key;
            for(int p=0;p<n;p++)if(!(key&(U(1)<<p))) {
                matrix[4]=lifts[p];++determinant_checks;
                if(!determinant(matrix))blocked|=U(1)<<p;
            }
            blocked_cache.emplace(key,blocked);return blocked;
        };
        auto legal=[&](U mask) {
            auto p=elements(mask);int k=p.size();U blocked=mask;
            for(int a=0;a<k;a++)for(int b=a+1;b<k;b++)for(int c=b+1;c<k;c++)for(int d=c+1;d<k;d++)
                blocked|=completion({p[a],p[b],p[c],p[d]});
            return all&~blocked;
        };
        // Establish root safety, then check every edge; reachability proves safety
        // of every certificate row without assuming the labels are correct.
        U partial=0;
        for(int p:elements(root)) {
            if(!(legal(partial)&(U(1)<<p)))throw std::runtime_error("unsafe root");
            partial|=U(1)<<p;
        }
        if(canonical(root)!=root)throw std::runtime_error("noncanonical root");
        uint64_t edges=0,terminals=0;
        std::unordered_set<U,Hash> visited;
        std::map<int,uint64_t> layers;
        std::function<void(U)> check=[&](U mask) {
            if(!visited.insert(mask).second)return;
            auto it=rows.find(mask);if(it==rows.end())throw std::runtime_error("missing child");
            ++layers[count(mask)];
            U moves=legal(mask);
            const auto entry=it->second;
            if(!moves)++terminals;
            if(entry.label) {
                bool found=false;
                for(int p:elements(moves))if(canonical(mask|(U(1)<<p))==entry.witness){found=true;break;}
                auto child=rows.find(entry.witness);
                if(!found || child==rows.end() || child->second.label!=0)
                    throw std::runtime_error("bad winning witness");
                ++edges;check(entry.witness);
            }else {
                for(int p:elements(moves)) {
                    U child=canonical(mask|(U(1)<<p));
                    auto jt=rows.find(child);
                    if(jt==rows.end() || jt->second.label!=1)throw std::runtime_error("incomplete losing boundary");
                    ++edges;check(child);
                }
            }
        };
        check(root);
        if(visited.size()!=rows.size())throw std::runtime_error("unreachable extra rows");
        std::cout<<"{\"verified\":true,\"side\":"<<side<<",\"root_lo\":"<<uint64_t(root)<<",\"root_hi\":"<<uint64_t(root>>64)
                 <<",\"outcome\":\""<<(rows.at(root).label?"N":"P")<<"\",\"states\":"<<rows.size()
                 <<",\"edges\":"<<edges<<",\"terminals\":"<<terminals<<",\"determinant_checks\":"<<determinant_checks<<",\"layers\":{";
        bool first=true;for(auto [k,v]:layers){if(!first)std::cout<<",";first=false;std::cout<<'"'<<k<<"\":"<<v;}
        std::cout<<"}}\n";
    }catch(const std::exception& e) {std::cerr<<e.what()<<"\n";return 1;}
}
