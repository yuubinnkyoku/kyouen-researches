#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>

struct Values{uint8_t g,h,t;};
int n;std::vector<uint32_t> adjacency,stamp;std::vector<Values> memo;
uint32_t generation=0;uint64_t visited=0;
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
Values evaluate(){++generation;return game((1<<n)-1);}
void toggle(int u,int v){adjacency[u]^=1U<<v;adjacency[v]^=1U<<u;}
int main(int argc,char**argv){
    if(argc!=5)return 2;
    n=std::atoi(argv[1]);uint64_t attempts=std::strtoull(argv[2],nullptr,10);int target=std::atoi(argv[3]);
    if(n<3||n>20||target<1)return 2;
    std::ifstream input(argv[4]);unsigned base,edges;input>>base>>edges;if(base>unsigned(n))return 3;
    adjacency.resize(n);stamp.assign(1<<n,0);memo.resize(1<<n);
    for(int v=0;v<n;++v)adjacency[v]=1U<<v;
    for(unsigned i=0;i<edges;++i){uint32_t edge;input>>edge;if(__builtin_popcount(edge)!=2||edge>=(1U<<n))return 3;
        int u=__builtin_ctz(edge);edge&=edge-1;int v=__builtin_ctz(edge);toggle(u,v);}
    if(!input)return 3;
    std::mt19937_64 rng(20261108);auto initial=evaluate();if(initial.h>=2)return 4;
    auto best_graph=adjacency;auto best=initial;auto current=initial;uint64_t evaluated=1;
    for(uint64_t i=0;i<attempts&&best.t<target;++i){
        if(i%1000==0){adjacency=best_graph;current=evaluate();++evaluated;}
        auto previous=adjacency;int flips=1+rng()%3;
        for(int j=0;j<flips;++j){int u=rng()%n,v=rng()%(n-1);if(v>=u)++v;toggle(u,v);}
        auto candidate=evaluate();++evaluated;int score=candidate.h<2?candidate.t:-1;
        int old=current.h<2?current.t:-1;
        if(score>=old||rng()%500==0)current=candidate;else adjacency=previous;
        if(score>best.t){best=candidate;best_graph=adjacency;}
    }
    std::cout<<"{\"scope\":\"bounded local edge mutations\",\"vertices\":"<<n<<",\"seed\":20261108,"
             <<"\"attempt_limit\":"<<attempts<<",\"target\":"<<target<<",\"evaluated\":"<<evaluated
             <<",\"recursive_states\":"<<visited<<",\"normal\":"<<int(best.g)<<",\"misere_aux\":"<<int(best.h)
             <<",\"restricted\":"<<int(best.t)<<",\"edges\":[";
    bool first=true;
    for(int u=0;u<n;++u)for(int v=u+1;v<n;++v)if(best_graph[u]>>v&1){
        std::cout<<(first?"":",")<<(1U<<u|1U<<v);first=false;}
    std::cout<<"]}\n";
}
