#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>

struct Values{uint8_t g,h,t;};
constexpr int N=14;
std::array<uint32_t,N> adjacency;
std::array<uint32_t,1<<N> stamp{};
std::array<Values,1<<N> memo{};
uint32_t generation=0;
uint64_t visited=0;
int mex(uint64_t options){return __builtin_ctzll(~options);}
Values game(uint32_t remaining){
    if(stamp[remaining]==generation)return memo[remaining];
    stamp[remaining]=generation;++visited;
    uint64_t gs=0,hs=0,ts=0;
    for(uint32_t bits=remaining;bits;bits&=bits-1){
        int v=__builtin_ctz(bits);auto child=game(remaining&~adjacency[v]);
        gs|=1ULL<<child.g;hs|=1ULL<<child.h;
        if(child.h<2)ts|=1ULL<<child.t;
    }
    int h=remaining?mex(hs):1;
    return memo[remaining]=Values{uint8_t(mex(gs)),uint8_t(h),uint8_t(h<2?mex(ts):255)};
}
Values evaluate(){++generation;return game((1<<N)-1);}
void toggle(int u,int v){adjacency[u]^=1U<<v;adjacency[v]^=1U<<u;}
int main(int argc,char**argv){
    uint64_t attempts=argc>1?std::strtoull(argv[1],nullptr,10):100000;
    std::mt19937_64 rng(20261108);
    for(int v=0;v<N;++v)adjacency[v]=1U<<v;
    for(int v=0;v<6;++v)toggle(v,(v+1)%6);
    for(int v=0;v<8;++v)toggle(8,v);
    auto initial=evaluate();if(initial.h!=1||initial.t!=3)return 2;
    auto best_graph=adjacency;auto best=initial;auto current=initial;
    uint64_t evaluated=1;
    for(uint64_t i=0;i<attempts;++i){
        if(i%1000==0){adjacency=best_graph;current=evaluate();++evaluated;}
        auto previous=adjacency;int flips=1+rng()%3;
        for(int j=0;j<flips;++j){int u=rng()%N,v=rng()%(N-1);if(v>=u)++v;toggle(u,v);}
        auto candidate=evaluate();++evaluated;
        int score=candidate.h<2?candidate.t:-1;
        int old=current.h<2?current.t:-1;
        if(score>=old||rng()%500==0)current=candidate;else adjacency=previous;
        if(score>best.t){best=candidate;best_graph=adjacency;}
        if(best.t>=4)break;
    }
    std::cout<<"{\"scope\":\"bounded local edge mutations on fourteen-vertex graphs\",\"seed\":20261108,"
             <<"\"evaluated\":"<<evaluated<<",\"recursive_states\":"<<visited
             <<",\"normal\":"<<int(best.g)<<",\"misere_aux\":"<<int(best.h)
             <<",\"restricted\":"<<int(best.t)<<",\"edges\":[";
    bool first=true;
    for(int u=0;u<N;++u)for(int v=u+1;v<N;++v)if(best_graph[u]>>v&1){
        std::cout<<(first?"":",")<<(1U<<u|1U<<v);first=false;
    }
    std::cout<<"]}\n";
}
