// Exhaustive three-row q=6 search, C++17, exact integer arithmetic.
// Usage: g++ -O3 -std=c++17 scan.cpp -o scan && ./scan 16 6
// For every 1<=a<=b<=max_gap and each row's five distinct integer x in [0,W),
// finds the maximum number of six-point circles, with no assumption that
// the three rows have equal x-coordinate sets.
#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <map>
#include <numeric>
#include <vector>
using namespace std;
struct Edge {int x,z,sum,product;};
struct Witness {int low=0,mid=0,high=0;};
int main(int argc,char**argv){
    int W=argc>1?stoi(argv[1]):16, max_gap=argc>2?stoi(argv[2]):6;
    if(W<5 || W>18 || max_gap<1 || max_gap>30){cerr<<"bounds: 5<=W<=18, 1<=max_gap<=30\n";return 2;}
    vector<Edge> edges;
    for(int x=0;x<W;x++)for(int z=x+1;z<W;z++)edges.push_back({x,z,x+z,x*z});
    int E=edges.size();
    vector<int> subsets;
    vector<array<int,10>> subset_edges;
    vector<array<array<short,2>,36>> by_sum;
    for(int mask=0;mask<(1<<W);mask++)if(__builtin_popcount((unsigned)mask)==5){
        subsets.push_back(mask);
        array<int,10> es{};int k=0;
        for(int t=0;t<E;t++)if((mask>>edges[t].x&1)&&(mask>>edges[t].z&1))es[k++]=t;
        assert(k==10);subset_edges.push_back(es);
        array<array<short,2>,36> table;for(auto &row:table)row={-1,-1};
        for(int t:es){int sm=edges[t].sum;int slot=(table[sm][0]==-1)?0:1;assert(table[sm][slot]==-1);table[sm][slot]=(short)t;}
        by_sum.push_back(table);
    }
    cout<<"# width="<<W<<" subsets_per_row="<<subsets.size()<<"\n";
    for(int a=1;a<=max_gap;a++)for(int b=a;b<=max_gap;b++){
        vector<vector<int>> middle_index(2*W,vector<int>(W*W,-1));
        for(int t=0;t<E;t++)middle_index[edges[t].sum][edges[t].product]=t;
        int best=0;Witness witness;
        long long outer_pairs=0,outer_with_at_least_five_potential=0,inner_scans=0;
        for(size_t i=0;i<subsets.size();i++)for(size_t j=0;j<subsets.size();j++){
            ++outer_pairs;
            unsigned char weights[160]={};
            int possible=0;
            for(int p:subset_edges[i])for(int slot=0;slot<2;slot++){
                int q=by_sum[j][edges[p].sum][slot];
                if(q<0)continue;
                int key=b*edges[p].product+a*edges[q].product-a*b*(a+b);
                if(key>=0 && key%(a+b)==0){
                    int product=key/(a+b);
                    if(product<W*W){int e=middle_index[edges[p].sum][product];
                        if(e>=0){++weights[e];++possible;}
                    }
                }
            }
            if(possible>=5)++outer_with_at_least_five_potential;
            // Every six-point circle contributes to exactly one middle-row edge.
            // 'possible' counts all circles if the middle row were unrestricted.
            if(possible<=best)continue;
            ++inner_scans;
            for(size_t k=0;k<subsets.size();k++){
                int count=0;
                for(int e:subset_edges[k])count+=weights[e];
                if(count>best){best=count;witness={subsets[i],subsets[k],subsets[j]};}
            }
        }
        auto emit=[&](int mask){cout<<'[';bool first=true;for(int x=0;x<W;x++)if(mask>>x&1){if(!first)cout<<',';cout<<x;first=false;}cout<<']';};
        cout<<"a="<<a<<" b="<<b<<" max="<<best<<" outer_pairs="<<outer_pairs
            <<" potential_ge5="<<outer_with_at_least_five_potential
            <<" inner_scans="<<inner_scans<<" y0=";
        emit(witness.low);cout<<" y"<<a<<'=';emit(witness.mid);
        cout<<" y"<<(a+b)<<'=';emit(witness.high);cout<<'\n';
    }
}
