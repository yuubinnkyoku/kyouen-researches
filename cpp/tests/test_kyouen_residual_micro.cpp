#include "kyouen_residual_micro.hpp"
#include <cassert>
#include <iostream>
using namespace kyouen_residual;

static int plain(State s,std::map<Key,int>& memo){
    s.edges=minimal(std::move(s.edges));
    Key k{s.vertices,s.edges}; auto it=memo.find(k); if(it!=memo.end())return it->second;
    std::vector<int> a; Mask x=s.vertices;
    while(x){int v=__builtin_ctzll(x);x&=x-1;a.push_back(plain(play(s,v),memo));}
    std::sort(a.begin(),a.end());a.erase(std::unique(a.begin(),a.end()),a.end());
    int g=0;for(int q:a){if(q==g)++g;else if(q>g)break;}memo.emplace(k,g);return g;
}
int main(){
    // Target the transition bug first: choosing one endpoint of a forbidden
    // pair must ban the other endpoint immediately.
    {
        State s{0b11,{0b11}};
        auto t=play(s,0);
        assert(t.vertices==0);
    }
    // Exhaust every clutter on <=4 vertices (all nonempty candidate edges of
    // size >=2). Compare the optimized kernel with direct mex recursion.
    std::uint64_t checked=0;
    for(int n=0;n<=4;++n){
        std::vector<Mask> cand;
        for(Mask e=1;e<(Mask{1}<<n);++e)if(pc(e)>=2)cand.push_back(e);
        std::uint64_t fams=Mask{1}<<cand.size();
        for(std::uint64_t f=0;f<fams;++f){
            State s; s.vertices=(n?((Mask{1}<<n)-1):0);
            for(std::size_t i=0;i<cand.size();++i)if((f>>i)&1)s.edges.push_back(cand[i]);
            s.edges=minimal(std::move(s.edges));
            std::map<Key,int> a,b;
            int ref=plain(s,a),got=grundy(s,b);
            assert(ref==got);
            // Parity conversion: terminal/P positions flip the fixed first
            // player proposition with side to move; N positions do the reverse.
            int even=first_player_verdict_from_grundy(got,0);
            int odd =first_player_verdict_from_grundy(got,1);
            assert(even!=odd);
            ++checked;
        }
    }
    std::cout<<"VERIFIED clutters="<<checked<<"\n";
}
