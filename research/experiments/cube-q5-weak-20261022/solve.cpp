// Exact win/loss solver for coplanar/cospherical q=5 cubes, n^3<=128.
// Limits produce UNKNOWN; only completed nodes enter the transposition table.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using U=__uint128_t;
using Row=std::array<int64_t,4>;
struct Hash {
    size_t operator()(U u)const {
        uint64_t a=uint64_t(u),b=uint64_t(u>>64);
        a^=b+0x9e3779b97f4a7c15ULL+(a<<6)+(a>>2);
        a^=a>>30;a*=0xbf58476d1ce4e5b9ULL;a^=a>>27;a*=0x94d049bb133111ebULL;
        return a^(a>>31);
    }
};
int pop(U a){return __builtin_popcountll(uint64_t(a))+__builtin_popcountll(uint64_t(a>>64));}
int first(U a){return uint64_t(a)?__builtin_ctzll(uint64_t(a)):64+__builtin_ctzll(uint64_t(a>>64));}
std::vector<int> ids(U a){std::vector<int> r;for(;a;a&=a-1)r.push_back(first(a));return r;}
struct Entry {bool win;U witness;};
struct Limit {};
class Solver {
public:
    int side,n;
    U all;
    uint64_t choose[129][5]{},nodes=0,budget;
    std::vector<Row> points;
    std::vector<std::vector<U>> sym;
    std::vector<U> completion;
    std::unordered_map<U,Entry,Hash> memo;
    Solver(int s,uint64_t b):side(s),n(s*s*s),budget(b) {
        if(s<3 || n>128)throw std::runtime_error("side must be 3,4,5");
        all=n==128?~U(0):(U(1)<<n)-1;
        for(int i=0;i<=n;i++) {
            choose[i][0]=1;
            for(int j=1;j<=4;j++)if(i)choose[i][j]=choose[i-1][j]+choose[i-1][j-1];
        }
        for(int x=0;x<side;x++)for(int y=0;y<side;y++)for(int z=0;z<side;z++)
            points.push_back({x*x+y*y+z*z,x,y,z});
        std::array<int,3> axes{0,1,2};
        do {for(int flips=0;flips<8;flips++) {
            std::vector<U> map;
            for(auto p:points) {
                int q[3];for(int j=0;j<3;j++)q[j]=(flips>>j&1)?side-1-int(p[axes[j]+1]):int(p[axes[j]+1]);
                map.push_back(U(1)<<((q[0]*side+q[1])*side+q[2]));
            }
            sym.push_back(std::move(map));
        }}while(std::next_permutation(axes.begin(),axes.end()));
        completion.resize(choose[n][4]);
        for(int a=0;a<n;a++)for(int b1=a+1;b1<n;b1++)for(int c=b1+1;c<n;c++)for(int d=c+1;d<n;d++) {
            Row v{},w{},t{},normal{};
            for(int j=0;j<4;j++){v[j]=points[b1][j]-points[a][j];w[j]=points[c][j]-points[a][j];t[j]=points[d][j]-points[a][j];}
            for(int j=0;j<4;j++) {
                int k[3],at=0;for(int l=0;l<4;l++)if(l!=j)k[at++]=l;
                int i=k[0],h=k[1],l=k[2];
                normal[j]=(j%2?-1:1)*(v[i]*(w[h]*t[l]-w[l]*t[h])-v[h]*(w[i]*t[l]-w[l]*t[i])+v[l]*(w[i]*t[h]-w[h]*t[i]));
            }
            U blocked=0;
            for(int e=0;e<n;e++) {
                int64_t value=0;for(int j=0;j<4;j++)value+=normal[j]*(points[e][j]-points[a][j]);
                if(!value)blocked|=U(1)<<e;
            }
            completion[index(a,b1,c,d)]=blocked;
        }
        std::cerr<<"geometry ready side="<<side<<" quadruples="<<completion.size()<<"\n";
    }
    uint64_t index(int a,int b,int c,int d)const{return choose[a][1]+choose[b][2]+choose[c][3]+choose[d][4];}
    U canonical(U mask)const {
        auto bits=ids(mask);U best=mask;
        for(const auto& m:sym){U v=0;for(int p:bits)v|=m[p];if(v<best)best=v;}
        return best;
    }
    U legal(U mask)const {
        auto v=ids(mask);int k=v.size();U blocked=mask;
        for(int a=0;a<k;a++)for(int b=a+1;b<k;b++)for(int c=b+1;c<k;c++)for(int d=c+1;d<k;d++)
            blocked|=completion[index(v[a],v[b],v[c],v[d])];
        return all&~blocked;
    }
    bool solve(U input) {
        U mask=canonical(input);
        auto found=memo.find(mask);if(found!=memo.end())return found->second.win;
        if(nodes>=budget)throw Limit{};
        ++nodes;
        if(nodes%1000000==0)std::cerr<<"nodes="<<nodes<<" memo="<<memo.size()<<" depth="<<pop(mask)<<"\n";
        U moves=legal(mask);
        if(!moves){memo.emplace(mask,Entry{false,0});return false;}
        std::vector<std::pair<int,U>> children;
        for(int p:ids(moves)) {
            U child=canonical(mask|(U(1)<<p));
            auto it=memo.find(child);
            if(it!=memo.end() && !it->second.win) {memo.emplace(mask,Entry{true,child});return true;}
            int mobility=pop(legal(child));
            if(!mobility) {
                memo.emplace(child,Entry{false,0});
                memo.emplace(mask,Entry{true,child});return true;
            }
            children.emplace_back(mobility,child);
        }
        std::sort(children.begin(),children.end());
        children.erase(std::unique(children.begin(),children.end()),children.end());
        for(auto [mobility,child]:children) {
            (void)mobility;
            if(!solve(child)){memo.emplace(mask,Entry{true,child});return true;}
        }
        memo.emplace(mask,Entry{false,0});return false;
    }
    void certificate(U root,const std::string& path)const {
        std::unordered_set<U,Hash> seen;
        auto visit=[&](auto&& self,U input)->void {
            U mask=canonical(input);
            if(!seen.insert(mask).second)return;
            const Entry& e=memo.at(mask);
            if(e.win)self(self,e.witness);
            else for(int p:ids(legal(mask)))self(self,mask|(U(1)<<p));
        };
        visit(visit,root);
        std::vector<U> sorted(seen.begin(),seen.end());std::sort(sorted.begin(),sorted.end());
        std::ofstream out(path);
        if(!out)throw std::runtime_error("cannot open certificate");
        out<<"Q5CUBE1 "<<side<<" "<<uint64_t(canonical(root))<<" "<<uint64_t(canonical(root)>>64)<<"\n";
        for(U mask:sorted) {
            const Entry& e=memo.at(mask);
            out<<uint64_t(mask)<<" "<<uint64_t(mask>>64)<<" "<<e.win<<" "<<uint64_t(e.witness)<<" "<<uint64_t(e.witness>>64)<<"\n";
        }
        if(!out)throw std::runtime_error("cannot write certificate");
        std::cerr<<"certificate="<<path<<" states="<<seen.size()<<"\n";
    }
};
int main(int argc,char**argv) {
    if(argc>=6 && std::string(argv[1])=="--merge") {
        Solver s(std::stoi(argv[2]),0);std::vector<U> losing_pairs;
        for(int i=4;i<argc;i++) {
            std::ifstream in(argv[i]);std::string magic;int side;uint64_t lo,hi;
            if(!(in>>magic>>side>>lo>>hi) || magic!="Q5CUBE1" || side!=s.side)throw std::runtime_error("bad merge header");
            U root=U(lo)|(U(hi)<<64);
            while(in>>lo) {
                uint64_t wlo,whi;int label;
                if(!(in>>hi>>label>>wlo>>whi) || label<0 || label>1)throw std::runtime_error("bad merge row");
                U mask=U(lo)|(U(hi)<<64),witness=U(wlo)|(U(whi)<<64);
                auto it=s.memo.find(mask);
                if(it!=s.memo.end() && it->second.win!=bool(label))throw std::runtime_error("conflicting labels");
                s.memo.emplace(mask,Entry{bool(label),witness});
            }
            if(!in.eof())throw std::runtime_error("bad trailing merge data");
            if(pop(root)!=2 || s.memo.at(root).win)throw std::runtime_error("merge needs P two-stone roots");
            losing_pairs.push_back(root);
        }
        std::unordered_set<U,Hash> singles;
        for(int p=0;p<s.n;p++)singles.insert(s.canonical(U(1)<<p));
        for(U single:singles) {
            bool found=false;
            for(U pair:losing_pairs)for(int p:ids(pair))if(s.canonical(U(1)<<p)==single) {
                s.memo.emplace(single,Entry{true,pair});found=true;break;
            }
            if(!found)throw std::runtime_error("missing first-move orbit");
        }
        s.memo.emplace(U(0),Entry{false,0});
        s.certificate(0,argv[3]);
        std::cout<<"{\"side\":"<<s.side<<",\"root_outcome\":\"P\",\"first_move_orbits\":"<<singles.size()
                 <<",\"pair_certificates\":"<<losing_pairs.size()<<"}\n";
        return 0;
    }
    if(argc==6 && std::string(argv[4])=="--batch") {
        int side=std::stoi(argv[1]);uint64_t budget=std::stoull(argv[2]);
        Solver s(side,budget);std::ifstream input(argv[5]);
        if(!input)throw std::runtime_error("cannot open batch");
        int a,b;
        while(input>>a>>b) {
            if(a<0 || b<0 || a>=s.n || b>=s.n || a==b)throw std::runtime_error("invalid pair");
            U root=(U(1)<<a)|(U(1)<<b);uint64_t before=s.nodes;
            s.budget=before+budget;
            std::cerr<<"pair="<<a<<","<<b<<"\n";
            try {
                bool win=s.solve(root);
                s.certificate(root,std::string(argv[3])+"-"+std::to_string(a)+"-"+std::to_string(b)+".cert");
                std::cout<<"{\"side\":"<<side<<",\"pair\":["<<a<<","<<b<<"],\"outcome\":\""<<(win?"N":"P")
                         <<"\",\"nodes\":"<<s.nodes-before<<",\"cumulative_nodes\":"<<s.nodes<<",\"memo\":"<<s.memo.size()<<"}"<<std::endl;
            }catch(Limit&) {
                std::cout<<"{\"side\":"<<side<<",\"pair\":["<<a<<","<<b<<"],\"outcome\":\"UNKNOWN\",\"nodes\":"<<s.nodes-before
                         <<",\"cumulative_nodes\":"<<s.nodes<<",\"memo\":"<<s.memo.size()<<"}"<<std::endl;
            }
        }
        return 0;
    }
    if(argc<6){std::cerr<<"usage: solve side budget certificate point ... (>=2 points)\n";return 2;}
    int side=std::stoi(argv[1]);uint64_t budget=std::stoull(argv[2]);
    Solver s(side,budget);U root=0;
    for(int i=4;i<argc;i++) {
        int p=std::stoi(argv[i]);if(p<0 || p>=s.n || (root&(U(1)<<p)))throw std::runtime_error("invalid point");
        if(!(s.legal(root)&(U(1)<<p)))throw std::runtime_error("unsafe input");
        root|=U(1)<<p;
    }
    try {
        bool win=s.solve(root);
        s.certificate(root,argv[3]);
        std::cout<<"{\"side\":"<<side<<",\"root_lo\":"<<uint64_t(s.canonical(root))<<",\"root_hi\":"<<uint64_t(s.canonical(root)>>64)
                 <<",\"outcome\":\""<<(win?"N":"P")<<"\",\"nodes\":"<<s.nodes<<",\"memo\":"<<s.memo.size()<<"}\n";
    }catch(Limit&) {
        std::cout<<"{\"side\":"<<side<<",\"outcome\":\"UNKNOWN\",\"nodes\":"<<s.nodes<<",\"memo\":"<<s.memo.size()<<"}\n";
    }
}
