// Exact structural features for n=11 canonical s5 verdict caches.
//
// Reuses the audited kc_core121 geometry and residual() implementation from
// the n11 residual-twins experiment.  No game solving is performed here.
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wreturn-type"
#define main residual_twins_reference_main
#include "../../n11-residual-twins/scripts/sample_residual_twins.cpp"
#undef main
#pragma GCC diagnostic pop

#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>

static std::vector<std::string> split_csv(const std::string& s){
    std::vector<std::string> out; std::string cur;
    for(char c:s){
        if(c==','){ out.push_back(cur); cur.clear(); }
        else cur.push_back(c);
    }
    out.push_back(cur); return out;
}

static unsigned component_stats(kc::Bits legal,const std::vector<kc::Bits>& edges,
                                unsigned& isolated,unsigned& max_component){
    auto verts=points(legal);
    std::map<int,std::vector<int>> adj;
    for(int v:verts) adj[v]={};
    for(auto e:edges){
        auto p=points(e);
        for(std::size_t i=0;i<p.size();++i)for(std::size_t j=i+1;j<p.size();++j){
            adj[p[i]].push_back(p[j]); adj[p[j]].push_back(p[i]);
        }
    }
    std::set<int> seen; unsigned comps=0; isolated=0; max_component=0;
    for(int s:verts) if(!seen.count(s)){
        ++comps; std::vector<int> stack{s}; seen.insert(s); unsigned n=0;
        while(!stack.empty()){
            int u=stack.back(); stack.pop_back(); ++n;
            for(int v:adj[u]) if(!seen.count(v)){seen.insert(v);stack.push_back(v);}
        }
        if(n==1 && adj[s].empty()) ++isolated;
        max_component=std::max(max_component,n);
    }
    return comps;
}

int main(int argc,char** argv){
    if(argc!=2) throw std::invalid_argument("usage: extract_s5_features CACHE");
    std::ifstream in(argv[1]);
    if(!in) throw std::runtime_error("cannot open cache");
    kc::Board board; kc::build_square(board,11);

    std::cout
      <<"lo,hi,verdict,legal,e2,e3,e4,components,isolated,max_component,"
      <<"max_degree,max_d2,max_d3,max_d4,sum_degree,pair_max_degree,"
      <<"occ_sum_d2,occ_min_d2,occ_max_d2,occ_radius2_sum\n";

    std::string line;
    while(std::getline(in,line)){
        if(line.empty() || line[0]=='#') continue;
        auto r=split_csv(line);
        if(r.size()<5 || r[0]!="s5verdict") continue;
        std::uint64_t lo=std::stoull(r[1]), hi=std::stoull(r[2]);
        int verdict=std::stoi(r[4]);
        if(verdict!=1 && verdict!=2) continue;
        kc::Bits occ{lo,hi};
        if(occ.count()!=5) throw std::runtime_error("cache row is not s5");
        auto legal=kc::legal_mask(board,occ);
        auto edges=residual(board,occ,legal);

        unsigned e2=0,e3=0,e4=0;
        std::map<int,unsigned> deg,d2,d3,d4,pairdeg;
        for(int v:points(legal)) deg[v]=d2[v]=d3[v]=d4[v]=pairdeg[v]=0;
        unsigned sumdeg=0;
        for(auto e:edges){
            unsigned k=e.count(); sumdeg+=k;
            if(k==2)++e2; else if(k==3)++e3; else if(k==4)++e4;
            for(int v:points(e)){
                ++deg[v];
                if(k==2){++d2[v];++pairdeg[v];}
                else if(k==3)++d3[v]; else if(k==4)++d4[v];
            }
        }
        auto maxval=[](const auto& m){
            unsigned z=0; for(auto [k,v]:m) z=std::max(z,v); return z;
        };
        unsigned isolated=0,maxcomp=0;
        unsigned comps=component_stats(legal,edges,isolated,maxcomp);

        auto op=points(occ);
        long long sumd2=0,mind2=1LL<<60,maxd2geom=0,radius2=0;
        for(std::size_t i=0;i<op.size();++i){
            int xi=op[i]%11, yi=op[i]/11;
            long long dx=xi-5,dy=yi-5; radius2+=dx*dx+dy*dy;
            for(std::size_t j=i+1;j<op.size();++j){
                int xj=op[j]%11,yj=op[j]/11;
                long long a=xi-xj,b=yi-yj,q=a*a+b*b;
                sumd2+=q; mind2=std::min(mind2,q); maxd2geom=std::max(maxd2geom,q);
            }
        }

        std::cout<<lo<<','<<hi<<','<<verdict<<','<<legal.count()<<','
                 <<e2<<','<<e3<<','<<e4<<','<<comps<<','<<isolated<<','<<maxcomp<<','
                 <<maxval(deg)<<','<<maxval(d2)<<','<<maxval(d3)<<','<<maxval(d4)<<','
                 <<sumdeg<<','<<maxval(pairdeg)<<','
                 <<sumd2<<','<<mind2<<','<<maxd2geom<<','<<radius2<<'\n';
    }
}
