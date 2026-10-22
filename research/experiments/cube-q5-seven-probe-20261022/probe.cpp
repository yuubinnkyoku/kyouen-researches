// Bounded exact P/N search with lazy geometry for cubes through side 7.
// UNKNOWN is never cached as an exact result. No claim follows from UNKNOWN.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <unordered_map>
#include <unordered_set>
#include <vector>
struct Mask {
    std::array<uint64_t,6> w{};
    void set(int p){w[p/64]|=uint64_t(1)<<(p%64);}
    bool has(int p)const{return (w[p/64]>>(p%64))&1;}
    bool operator==(const Mask& b)const{return w==b.w;}
    bool operator<(const Mask& b)const {
        for(int i=5;i>=0;i--)if(w[i]!=b.w[i])return w[i]<b.w[i];
        return false;
    }
    std::vector<int> ids()const {
        std::vector<int> r;
        for(int i=0;i<6;i++)for(uint64_t b=w[i];b;b&=b-1)r.push_back(i*64+__builtin_ctzll(b));
        return r;
    }
    int count()const{int n=0;for(auto v:w)n+=__builtin_popcountll(v);return n;}
};
struct Hash {
    size_t operator()(const Mask& m)const {
        uint64_t h=0x9e3779b97f4a7c15ULL;
        for(uint64_t x:m.w){x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;x*=0x94d049bb133111ebULL;h^=(x^(x>>31))+(h<<6)+(h>>2);}
        return h;
    }
};
struct Entry {bool win;Mask witness;};
struct Limit {const char* reason;};
using Row=std::array<int64_t,4>;
class Solver {
public:
    int side,n;
    uint64_t budget,nodes=0,geometry_limit,geometry_evaluations=0;
    std::vector<Row> points;
    std::vector<std::vector<int>> sym;
    std::unordered_map<uint64_t,Mask> completions;
    std::unordered_map<Mask,Entry,Hash> memo;
    Solver(int s,uint64_t b,uint64_t g):side(s),budget(b),geometry_limit(g) {
        if(side<3 || side>7)throw std::runtime_error("side must be between 3 and 7");
        n=side*side*side;
        for(int x=0;x<side;x++)for(int y=0;y<side;y++)for(int z=0;z<side;z++)points.push_back({x*x+y*y+z*z,x,y,z});
        std::array<int,3> axes{0,1,2};
        do {for(int flips=0;flips<8;flips++) {
            std::vector<int> mapping;
            for(auto p:points) {
                int q[3];for(int j=0;j<3;j++)q[j]=(flips>>j&1)?side-1-int(p[axes[j]+1]):int(p[axes[j]+1]);
                mapping.push_back((q[0]*side+q[1])*side+q[2]);
            }
            sym.push_back(std::move(mapping));
        }}while(std::next_permutation(axes.begin(),axes.end()));
    }
    Mask canonical(const Mask& mask)const {
        auto bits=mask.ids();Mask best=mask;
        for(const auto& m:sym){Mask v;for(int p:bits)v.set(m[p]);if(v<best)best=v;}
        return best;
    }
    Mask completion(int a,int b,int c,int d) {
        uint64_t key=uint64_t(a)|(uint64_t(b)<<9)|(uint64_t(c)<<18)|(uint64_t(d)<<27);
        auto found=completions.find(key);if(found!=completions.end())return found->second;
        if(completions.size()>=geometry_limit)throw Limit{"geometry-limit"};
        ++geometry_evaluations;
        Row v{},w{},t{},normal{};
        for(int j=0;j<4;j++){v[j]=points[b][j]-points[a][j];w[j]=points[c][j]-points[a][j];t[j]=points[d][j]-points[a][j];}
        for(int j=0;j<4;j++) {
            int k[3],at=0;for(int l=0;l<4;l++)if(l!=j)k[at++]=l;
            int i=k[0],h=k[1],l=k[2];
            normal[j]=(j%2?-1:1)*(v[i]*(w[h]*t[l]-w[l]*t[h])-v[h]*(w[i]*t[l]-w[l]*t[i])+v[l]*(w[i]*t[h]-w[h]*t[i]));
        }
        Mask blocked;
        for(int e=0;e<n;e++) {
            int64_t value=0;for(int j=0;j<4;j++)value+=normal[j]*(points[e][j]-points[a][j]);
            if(!value)blocked.set(e);
        }
        completions.emplace(key,blocked);return blocked;
    }
    std::vector<int> legal(const Mask& mask) {
        auto p=mask.ids();int k=p.size();Mask blocked=mask;
        for(int a=0;a<k;a++)for(int b=a+1;b<k;b++)for(int c=b+1;c<k;c++)for(int d=c+1;d<k;d++) {
            auto q=completion(p[a],p[b],p[c],p[d]);
            for(int j=0;j<6;j++)blocked.w[j]|=q.w[j];
        }
        std::vector<int> moves;
        for(int i=0;i<n;i++)if(!blocked.has(i))moves.push_back(i);
        return moves;
    }
    bool solve(const Mask& input) {
        Mask mask=canonical(input);
        auto found=memo.find(mask);if(found!=memo.end())return found->second.win;
        if(nodes>=budget)throw Limit{"node-limit"};
        ++nodes;
        if(nodes%100000==0)std::cerr<<"nodes="<<nodes<<" memo="<<memo.size()<<" quadruples="<<completions.size()<<" depth="<<mask.count()<<"\n";
        auto moves=legal(mask);
        if(moves.empty()){memo.emplace(mask,Entry{false,{}});return false;}
        std::vector<std::pair<int,Mask>> children;
        for(int p:moves) {
            Mask child=mask;child.set(p);child=canonical(child);
            auto it=memo.find(child);
            if(it!=memo.end() && !it->second.win){memo.emplace(mask,Entry{true,child});return true;}
            int mobility=legal(child).size();
            if(!mobility){memo.emplace(child,Entry{false,{}});memo.emplace(mask,Entry{true,child});return true;}
            children.emplace_back(mobility,child);
        }
        std::sort(children.begin(),children.end());children.erase(std::unique(children.begin(),children.end()),children.end());
        for(const auto& item:children)if(!solve(item.second)){memo.emplace(mask,Entry{true,item.second});return true;}
        memo.emplace(mask,Entry{false,{}});return false;
    }
    void certificate(Mask root,const std::string& path) {
        std::unordered_set<Mask,Hash> seen;
        auto visit=[&](auto&& self,const Mask& input)->void {
            Mask mask=canonical(input);if(!seen.insert(mask).second)return;
            const Entry e=memo.at(mask);
            if(e.win)self(self,e.witness);
            else for(int p:legal(mask)){Mask child=mask;child.set(p);self(self,child);}
        };
        visit(visit,root);
        std::vector<Mask> sorted(seen.begin(),seen.end());std::sort(sorted.begin(),sorted.end());
        std::ofstream out(path);if(!out)throw std::runtime_error("cannot write certificate");
        root=canonical(root);
        if(side<=5) {
            out<<"Q5CUBE1 "<<side<<" "<<root.w[0]<<" "<<root.w[1]<<"\n";
            for(const auto& m:sorted){auto e=memo.at(m);out<<m.w[0]<<" "<<m.w[1]<<" "<<e.win<<" "<<e.witness.w[0]<<" "<<e.witness.w[1]<<"\n";}
        }else {
            out<<"Q5CUBE2 "<<side<<" 6";for(auto x:root.w)out<<" "<<x;out<<"\n";
            for(const auto& m:sorted){auto e=memo.at(m);for(auto x:m.w)out<<x<<" ";out<<e.win;for(auto x:e.witness.w)out<<" "<<x;out<<"\n";}
        }
        if(!out)throw std::runtime_error("cannot write certificate");
        std::cerr<<"certificate states="<<sorted.size()<<"\n";
    }
};
int main(int argc,char**argv) {
    if(argc<7){std::cerr<<"usage: probe side nodes quadruples certificate points...\n";return 2;}
    Solver s(std::stoi(argv[1]),std::stoull(argv[2]),std::stoull(argv[3]));Mask root;
    for(int i=5;i<argc;i++){int p=std::stoi(argv[i]);if(p<0 || p>=s.n || root.has(p))throw std::runtime_error("invalid point");root.set(p);}
    if(std::string(argv[4])=="--legal") {
        if(root.count()!=4)throw std::runtime_error("geometry check requires exactly four occupied points");
        auto moves=s.legal(root);std::cout<<"{\"side\":"<<s.side<<",\"legal_indices\":[";
        bool first=true;for(int p:moves){if(!first)std::cout<<",";first=false;std::cout<<p;}
        std::cout<<"]}\n";return 0;
    }
    const char* outcome="UNKNOWN";const char* reason="";
    try {
        Mask partial;
        for(int p:root.ids()) {
            auto moves=s.legal(partial);if(std::find(moves.begin(),moves.end(),p)==moves.end())throw std::runtime_error("unsafe root");
            partial.set(p);
        }
        bool win=s.solve(root);
        // Certificate traversal may need an uncached quad. A complete exact
        // result is retained, but no partial certificate is emitted on failure.
        s.geometry_limit=uint64_t(-1);
        s.certificate(root,argv[4]);outcome=win?"N":"P";
    }catch(Limit limit){reason=limit.reason;}
    std::cout<<"{\"side\":"<<s.side<<",\"outcome\":\""<<outcome<<"\",\"reason\":\""<<reason
             <<"\",\"nodes\":"<<s.nodes<<",\"memo\":"<<s.memo.size()<<",\"quadruples\":"<<s.completions.size()<<"}\n";
}
