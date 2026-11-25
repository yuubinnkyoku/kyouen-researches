#include "kyouen_residual_micro.hpp"
#include <chrono>
#include <iomanip>
#include <iostream>
using namespace kyouen_residual;
struct Result { int value; Stats stats; std::size_t memo; double us; };
Result evaluate(const State& s,bool pn){
    std::map<Key,int> memo; Stats st; std::uint64_t quota=100000;
    auto start=ProfileClock::now();
    int value=pn?outcome(s,memo,quota,&st):grundy(s,memo,&st);
    double us=std::chrono::duration<double,std::micro>(ProfileClock::now()-start).count();
    return {value,st,memo.size(),us};
}
int main(){
    std::cout<<"id,n,edges,g,pn,sg_calls,pn_calls,sg_memo,pn_memo,cutoffs,sg_us,pn_us\n";
    int id,n,m;
    while(std::cin>>id>>n>>m){
        if(n<0 || n>18 || m<0 || m>10000) return 2;
        State s{n?((Mask{1}<<n)-1):0,{}};
        for(int i=0;i<m;++i){ Mask edge; if(!(std::cin>>edge)) return 2; s.edges.push_back(edge); }
        s=normalize(std::move(s));
        std::vector<double> a,b; Result sg{},pn{};
        for(int repeat=0;repeat<7;++repeat){
            if(repeat%2){ pn=evaluate(s,true); sg=evaluate(s,false); }
            else { sg=evaluate(s,false); pn=evaluate(s,true); }
            if(pn.value<0 || pn.value!=(sg.value!=0)) return 1;
            a.push_back(sg.us); b.push_back(pn.us);
        }
        std::sort(a.begin(),a.end()); std::sort(b.begin(),b.end());
        std::cout<<id<<','<<n<<','<<m<<','<<sg.value<<','<<pn.value<<','<<sg.stats.calls<<','<<pn.stats.calls<<','
            <<sg.memo<<','<<pn.memo<<','<<pn.stats.outcome_cutoffs<<','<<std::fixed<<std::setprecision(3)<<a[3]<<','<<b[3]<<'\n';
    }
}
