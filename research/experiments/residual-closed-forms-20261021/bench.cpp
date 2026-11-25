// Cold-cache A/B on saved residual states. No board search or shared cache writes.
#include "kyouen_residual_micro.hpp"
#include <chrono>
#include <iomanip>
#include <iostream>
#include <string>
using namespace kyouen_residual;
struct Result { int g; Stats stats; std::size_t memo; double us; };
static Result run(const State& s,bool fast){
    std::map<Key,int> memo; Stats st;
    auto start=std::chrono::steady_clock::now();
    int g=grundy(s,memo,&st,fast);
    double us=std::chrono::duration<double,std::micro>(std::chrono::steady_clock::now()-start).count();
    return {g,st,memo.size(),us};
}
int main(int argc,char** argv){
    int repeats=argc>1?std::stoi(argv[1]):7;
    if(repeats<1 || repeats>100) return 2;
    std::cout<<"id,n,edges,g,baseline_calls,fast_calls,baseline_memo,fast_memo,free_hits,two_hits,sunflower_hits,path_hits,baseline_us,fast_us\n";
    int id,n,m;
    while(std::cin>>id>>n>>m){
        if(n<0 || n>18 || m<0) return 2;
        State s{n?((Mask{1}<<n)-1):0,{}};
        for(int i=0;i<m;++i){ Mask e; if(!(std::cin>>e)) return 2; s.edges.push_back(e); }
        s=normalize(std::move(s));
        std::vector<double> bt,ft; Result b{},f{};
        for(int i=0;i<repeats;++i){
            if(i%2){ f=run(s,true); b=run(s,false); }
            else { b=run(s,false); f=run(s,true); }
            if(b.g!=f.g){std::cerr<<"MISMATCH "<<id<<"\n";return 1;}
            bt.push_back(b.us); ft.push_back(f.us);
        }
        std::sort(bt.begin(),bt.end());std::sort(ft.begin(),ft.end());
        std::cout<<id<<','<<n<<','<<m<<','<<f.g<<','<<b.stats.calls<<','<<f.stats.calls<<','
                 <<b.memo<<','<<f.memo<<','<<f.stats.closed_free<<','<<f.stats.closed_two_edges<<','
                 <<f.stats.closed_sunflower<<','<<f.stats.closed_paths<<','
                 <<std::fixed<<std::setprecision(3)<<bt[bt.size()/2]<<','<<ft[ft.size()/2]<<'\n';
    }
}
