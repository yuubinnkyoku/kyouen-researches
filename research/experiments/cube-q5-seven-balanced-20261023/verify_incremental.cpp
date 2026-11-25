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
struct U {
    std::array<uint64_t,6> words{};
    U(uint64_t low=0){words[0]=low;}
    explicit operator bool()const{for(auto x:words)if(x)return true;return false;}
    explicit operator uint64_t()const{return words[0];}
    bool operator==(const U& b)const{return words==b.words;}
    bool operator!=(const U& b)const{return !(*this==b);}
    bool operator<(const U& b)const{for(int j=5;j>=0;j--)if(words[j]!=b.words[j])return words[j]<b.words[j];return false;}
    U operator|(const U& b)const{U r;for(int j=0;j<6;j++)r.words[j]=words[j]|b.words[j];return r;}
    U operator&(const U& b)const{U r;for(int j=0;j<6;j++)r.words[j]=words[j]&b.words[j];return r;}
    U operator~()const{U r;for(int j=0;j<6;j++)r.words[j]=~words[j];return r;}
    U& operator|=(const U& b){return *this=*this|b;}
    U& operator&=(const U& b){return *this=*this&b;}
    U operator-(uint64_t amount)const{U r=*this;for(int j=0;j<6 && amount;j++){auto old=r.words[j];r.words[j]-=amount;amount=old<amount;}return r;}
    U operator<<(unsigned amount)const {
        U r;if(amount>=384)return r;
        for(unsigned j=0;j<6;j++) {
            unsigned to=j+amount/64;
            if(to<6)r.words[to]|=words[j]<<(amount%64);
            if(amount%64 && to+1<6)r.words[to+1]|=words[j]>>(64-amount%64);
        }
        return r;
    }
    U operator>>(unsigned amount)const {
        U r;if(amount>=384)return r;
        for(unsigned j=amount/64;j<6;j++) {
            r.words[j-amount/64]|=words[j]>>(amount%64);
            if(amount%64 && j>amount/64)r.words[j-amount/64-1]|=words[j]<<(64-amount%64);
        }
        return r;
    }
};
struct Hash {
    size_t operator()(U v)const {
        uint64_t h=0xcbf29ce484222325ULL;
        for(auto x:v.words){h^=x;h*=0x100000001b3ULL;h^=h>>29;}
        return h;
    }
};
int count(U a){int n=0;for(auto x:a.words)n+=__builtin_popcountll(x);return n;}
std::vector<int> elements(U v) {
    std::vector<int> r;
    for(int j=0;j<6;j++)for(uint64_t x=v.words[j];x;x&=x-1)r.push_back(j*64+__builtin_ctzll(x));
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
        std::string magic;int side;uint64_t lo;
        if(!(input>>magic>>side) || (magic!="Q5CUBE1" && magic!="Q5CUBE2") || side<3 || side>7)
            throw std::runtime_error("bad header");
        int width=2;
        if(magic=="Q5CUBE2"){if(!(input>>width) || width!=6)throw std::runtime_error("bad mask width");}
        if(width==2 && side>5)throw std::runtime_error("legacy board too large");
        int n=side*side*side;U all=(U(1)<<n)-1,root;
        for(int j=0;j<width;j++)if(!(input>>root.words[j]))throw std::runtime_error("truncated root");
        if(root&~all)throw std::runtime_error("root outside board");
        std::unordered_map<U,Entry,Hash> rows;
        while(input>>lo) {
            int label;U mask(lo),witness;
            for(int j=1;j<width;j++)if(!(input>>mask.words[j]))throw std::runtime_error("truncated mask");
            if(!(input>>label))throw std::runtime_error("truncated label");
            for(int j=0;j<width;j++)if(!(input>>witness.words[j]))throw std::runtime_error("truncated witness");
            if((mask&~all) || (witness&~all) || label<0 || label>1 || (!label && witness))throw std::runtime_error("invalid row");
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
        auto transport=[&](U mask,U live) {
            U best=mask,best_live=live;auto points=elements(mask);
            for(const auto& mapping:transforms) {
                U image=0;for(int p:points)image|=U(1)<<mapping[p];
                if(image<best) {
                    best=image;best_live=0;
                    for(int p:elements(live))best_live|=U(1)<<mapping[p];
                }
            }
            return std::pair<U,U>{best,best_live};
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
            if(blocked_cache.size()>=2000000)blocked_cache.clear();
            blocked_cache.emplace(key,blocked);return blocked;
        };
        auto legal=[&](U mask) {
            auto p=elements(mask);int k=p.size();U blocked=mask;
            for(int a=0;a<k;a++)for(int b=a+1;b<k;b++)for(int c=b+1;c<k;c++)for(int d=c+1;d<k;d++)
                blocked|=completion({p[a],p[b],p[c],p[d]});
            return all&~blocked;
        };
        // Independent 5x5 Bareiss geometry. Existing illegal candidates stay
        // illegal; only new quads containing the played point need testing.
        auto advance=[&](U mask,U live,int move) {
            U result=live&~(U(1)<<move);auto points=elements(mask);int k=points.size();
            for(int a=0;a<k && result;a++)for(int b=a+1;b<k && result;b++)
            for(int c=b+1;c<k && result;c++) {
                Matrix matrix{};matrix[0]=lifts[points[a]];matrix[1]=lifts[points[b]];
                matrix[2]=lifts[points[c]];matrix[3]=lifts[move];
                for(int p:elements(result)) {
                    matrix[4]=lifts[p];++determinant_checks;
                    if(!determinant(matrix))result=result&~(U(1)<<p);
                }
            }
            return result;
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
        std::function<void(U,U)> check=[&](U mask,U moves) {
            if(!visited.insert(mask).second)return;
            auto it=rows.find(mask);if(it==rows.end())throw std::runtime_error("missing child");
            ++layers[count(mask)];
            const auto entry=it->second;
            if(!moves)++terminals;
            if(entry.label) {
                int selected=-1;
                for(int p:elements(moves))if(canonical(mask|(U(1)<<p))==entry.witness){selected=p;break;}
                auto child=rows.find(entry.witness);
                if(selected<0 || child==rows.end() || child->second.label!=0)
                    throw std::runtime_error("bad winning witness");
                ++edges;
                if(!visited.count(entry.witness)) {
                    auto [key,live]=transport(mask|(U(1)<<selected),advance(mask,moves,selected));
                    if(!(key==entry.witness))throw std::runtime_error("transport mismatch");
                    check(key,live);
                }
            }else {
                for(int p:elements(moves)) {
                    U child=canonical(mask|(U(1)<<p));
                    auto jt=rows.find(child);
                    if(jt==rows.end() || jt->second.label!=1)throw std::runtime_error("incomplete losing boundary");
                    ++edges;
                    if(!visited.count(child)) {
                        auto [key,live]=transport(mask|(U(1)<<p),advance(mask,moves,p));
                        if(!(key==child))throw std::runtime_error("transport mismatch");
                        check(key,live);
                    }
                }
            }
        };
        check(root,legal(root));
        if(visited.size()!=rows.size())throw std::runtime_error("unreachable extra rows");
        std::cout<<"{\"verified\":true,\"side\":"<<side<<",\"root_words\":[";
        for(int j=0;j<6;j++){if(j)std::cout<<",";std::cout<<root.words[j];}
        std::cout<<"],\"outcome\":\""<<(rows.at(root).label?"N":"P")<<"\",\"states\":"<<rows.size()
                 <<",\"edges\":"<<edges<<",\"terminals\":"<<terminals<<",\"determinant_checks\":"<<determinant_checks<<",\"layers\":{";
        bool first=true;for(auto [k,v]:layers){if(!first)std::cout<<",";first=false;std::cout<<'"'<<k<<"\":"<<v;}
        std::cout<<"}}\n";
        return 0;
    }catch(const std::exception& e) {std::cerr<<e.what()<<"\n";return 1;}
}
