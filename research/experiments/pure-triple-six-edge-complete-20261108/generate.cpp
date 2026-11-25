#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <string>
#include <unordered_set>
#include <vector>

#ifndef EDGE_COUNT
#define EDGE_COUNT 6
#endif
constexpr int H=EDGE_COUNT,CELLS=1<<H,OLD_CELLS=CELLS>>1;
static_assert(H>=2&&H<=8);
constexpr unsigned factorial(){unsigned result=1;for(int i=2;i<=H;++i)result*=i;return result;}
constexpr unsigned FACTORIAL=factorial();
struct Canonical{std::string signature;unsigned automorphisms;};
Canonical canonical(const std::array<int,CELLS>&counts){
    std::vector<int> members;std::array<std::vector<int>,H> degrees;
    for(int mask=1;mask<CELLS;++mask)for(int j=0;j<counts[mask];++j){
        members.push_back(mask);int d=__builtin_popcount((unsigned)mask);
        for(int e=0;e<H;++e)if(mask>>e&1)degrees[e].push_back(d);
    }
    std::array<int,H> profile,order;for(int e=0;e<H;++e){
        assert(degrees[e].size()==3);std::sort(degrees[e].begin(),degrees[e].end());
        profile[e]=(H+1)*(H+1)*degrees[e][0]+(H+1)*degrees[e][1]+degrees[e][2];order[e]=e;
    }
    std::sort(order.begin(),order.end(),[&](int a,int b){return profile[a]!=profile[b]?profile[a]<profile[b]:a<b;});
    std::vector<std::vector<int>> groups;
    for(int e:order){if(groups.empty()||profile[groups.back()[0]]!=profile[e])groups.push_back({});groups.back().push_back(e);}
    std::array<int,H> mapping;std::string best;unsigned aut=0;
    std::function<void(int,int)> visit=[&](int group,int start){
        if(group==(int)groups.size()){
            std::string image(CELLS-1,'\0');for(int member:members){int target=0;
                for(int bits=member;bits;bits&=bits-1)target|=1<<mapping[__builtin_ctz((unsigned)bits)];
                ++image[target-1];}
            if(best.empty()||image<best){best=image;aut=1;}else if(image==best)++aut;
            return;
        }
        auto permutation=groups[group];do{
            for(unsigned j=0;j<permutation.size();++j)mapping[permutation[j]]=start+j;
            visit(group+1,start+permutation.size());
        }while(std::next_permutation(permutation.begin(),permutation.end()));
    };
    visit(0,0);assert(aut&&FACTORIAL%aut==0);return {best,aut};
}

int main(int argc,char**argv){
    if(argc!=3)return 2;std::ifstream input(argv[1]);std::ofstream output(argv[2]);
    int previous;input>>previous;std::unordered_set<std::string> found;uint64_t choices=0,valid=0;
    for(int row=0;row<previous;++row){
        std::vector<std::pair<int,int>> cells;for(int mask=1;mask<OLD_CELLS;++mask){int count;input>>count;if(count)cells.push_back({mask,count});}
        std::array<int,CELLS> counts{};
        std::function<void(int,int)> choose=[&](int index,int left){
            if(index<(int)cells.size()){
                auto [mask,count]=cells[index];for(int amount=0;amount<=std::min(left,count);++amount){
                    counts[mask]+=count-amount;counts[mask|OLD_CELLS]+=amount;
                    choose(index+1,left-amount);
                    counts[mask]-=count-amount;counts[mask|OLD_CELLS]-=amount;
                }return;
            }
            ++choices;counts[OLD_CELLS]+=left;
            std::array<uint32_t,H> edges{};unsigned v=0;
            for(int mask=1;mask<CELLS;++mask)for(int j=0;j<counts[mask];++j,++v)
                for(int e=0;e<H;++e)if(mask>>e&1)edges[e]|=1U<<v;
            auto sorted=edges;std::sort(sorted.begin(),sorted.end());
            if(std::adjacent_find(sorted.begin(),sorted.end())==sorted.end()){
                ++valid;found.insert(canonical(counts).signature);
            }
            counts[OLD_CELLS]-=left;
        };
        choose(0,3);
    }
    std::vector<std::string> signatures(found.begin(),found.end());std::sort(signatures.begin(),signatures.end());
    output<<signatures.size()<<'\n';uint64_t labeled=0;
    for(auto&signature:signatures){std::array<int,CELLS> counts{};
        for(int i=0;i<CELLS-1;++i)counts[i+1]=(unsigned char)signature[i];
        auto again=canonical(counts);assert(again.signature==signature);labeled+=FACTORIAL/again.automorphisms;
        output<<again.automorphisms;for(int i=1;i<CELLS;++i)output<<' '<<counts[i];output<<'\n';}
    if(!input||!output)return 3;
    std::cout<<"{\"previous_types\":"<<previous<<",\"extension_choices\":"<<choices
             <<",\"valid_extensions\":"<<valid<<",\"unlabeled_types\":"<<signatures.size()
             <<",\"labeled_signatures\":"<<labeled<<"}\n";
}
