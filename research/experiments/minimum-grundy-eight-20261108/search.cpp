#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>

int main(int argc,char**argv){
    if(argc!=7)return 2;
    int n=std::atoi(argv[1]),low=std::atoi(argv[2]),high=std::atoi(argv[3]),cover=std::atoi(argv[4]);
    uint64_t limit=std::strtoull(argv[5],nullptr,10);int target=std::atoi(argv[6]);
    if(n<3||n>16||low<2||high<low||cover<1||cover>n)return 2;
    int full=(1<<n)-1;std::mt19937_64 rng(20261108);std::vector<int> candidates;
    for(int s=1;s<=full;++s){int rank=__builtin_popcount((unsigned)s);
        if((s&((1<<cover)-1))&&rank>=low&&rank<=high)candidates.push_back(s);}
    if(candidates.empty())return 2;
    std::vector<uint8_t> unsafe(1<<n),value(1<<n);std::vector<uint64_t> histogram(n+1);
    std::vector<int> best_edges;uint64_t evaluated=0,safe_states=0;int best=-1;
    for(uint64_t iteration=0;iteration<limit;++iteration){
        int h=std::min<int>(candidates.size(),1+iteration%40);std::vector<int> edges;
        while((int)edges.size()<h){int edge=candidates[rng()%candidates.size()];
            if(std::find(edges.begin(),edges.end(),edge)==edges.end())edges.push_back(edge);}
        std::fill(unsafe.begin(),unsafe.end(),0);
        for(int edge:edges){int remaining=full^edge;
            for(int part=remaining;;part=(part-1)&remaining){unsafe[edge|part]=1;if(!part)break;}}
        for(int s=full;s>=0;--s){
            if(unsafe[s])continue;++safe_states;unsigned options=0;
            for(int remaining=full^s;remaining;remaining&=remaining-1){int child=s|(remaining&-remaining);
                if(!unsafe[child])options|=1U<<value[child];}
            value[s]=__builtin_ctz(~options);
        }
        ++histogram[value[0]];++evaluated;if(value[0]>best){best=value[0];best_edges=edges;}
        if(best>=target)break;
    }
    std::cout<<"{\"scope\":\"bounded families hitting a fixed cover\",\"vertices\":"<<n
             <<",\"rank_min\":"<<low<<",\"rank_max\":"<<high<<",\"cover_size\":"<<cover
             <<",\"seed\":20261108,\"evaluated\":"<<evaluated<<",\"safe_states\":"<<safe_states
             <<",\"maximum_found\":"<<best<<",\"histogram\":[";
    for(int g=0;g<=n;++g)std::cout<<(g?",":"")<<histogram[g];
    std::cout<<"],\"witness_edges\":[";
    for(unsigned i=0;i<best_edges.size();++i)std::cout<<(i?",":"")<<best_edges[i];
    std::cout<<"]}\n";
}
