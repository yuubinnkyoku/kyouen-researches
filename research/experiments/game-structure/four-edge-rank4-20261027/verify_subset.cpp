// Independent direct labeled-subset mex checker for four minimal forbidden edges.
// Build: c++ -O3 -std=c++17 verify_subset.cpp -o /tmp/verify_subset
// Run: /tmp/verify_subset
#include <array>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;

struct Audit {
    int rank;
    array<int,15> c{};
    array<int,4> remaining{};
    array<long long,8> hist{};
    long long cases=0;
    int max_g=-1, min_n=100;
    array<int,15> witness{};
    explicit Audit(int r):rank(r){remaining.fill(r);}

    int direct_grundy(){
        array<uint32_t,4> edges{};
        int n=0;
        for(int p=1;p<16;p++)for(int k=0;k<c[p-1];k++){
            for(int i=0;i<4;i++)if(p&(1<<i))edges[i] |= 1u<<n;
            n++;
        }
        vector<int8_t> memo(size_t(1)<<n,-1);
        auto dfs=[&](auto&& self,uint32_t taken)->int{
            int8_t &cached=memo[taken];
            if(cached>=0)return cached;
            unsigned seen=0;
            for(int v=0;v<n;v++)if(!(taken&(1u<<v))){
                uint32_t next=taken|(1u<<v);
                bool legal=true;
                for(auto e:edges)if((next&e)==e){legal=false;break;}
                if(legal)seen |= 1u<<self(self,next);
            }
            int g=0;while(seen&(1u<<g))g++;
            cached=g;return g;
        };
        return dfs(dfs,0);
    }
    void enumerate(int p){
        if(p==16){
            for(int i=0;i<4;i++)if(rank-remaining[i]<2)return;
            for(int i=0;i<4;i++)for(int j=0;j<4;j++)if(i!=j){
                bool strict=false;
                for(int q=1;q<16;q++)if(c[q-1] && (q&(1<<i)) && !(q&(1<<j))){strict=true;break;}
                if(!strict)return;
            }
            int g=direct_grundy();
            cases++;hist[g]++;
            int n=0;for(int x:c)n+=x;
            if(g>max_g || (g==max_g && n<min_n)){
                max_g=g;min_n=n;witness=c;
            }
            return;
        }
        int cap=rank;
        for(int i=0;i<4;i++)if(p&(1<<i))cap=min(cap,remaining[i]);
        for(int value=0;value<=cap;value++){
            c[p-1]=value;
            for(int i=0;i<4;i++)if(p&(1<<i))remaining[i]-=value;
            enumerate(p+1);
            for(int i=0;i<4;i++)if(p&(1<<i))remaining[i]+=value;
        }
        c[p-1]=0;
    }
};

int main(){
    const array<long long,8> h2={15,12,19,24,0,0,0,0};
    const array<long long,8> h3={953,923,434,438,12,0,0,0};
    const array<long long,8> h4={13508,13427,5111,5270,240,36,0,0};
    for(int r=2;r<=4;r++){
        Audit a(r);a.enumerate(1);
        cout<<"rank="<<r<<" cases="<<a.cases<<" max="<<a.max_g
            <<" min_witness_vertices="<<a.min_n<<" histogram=";
        for(int i=0;i<8;i++)cout<<(i?",":"")<<a.hist[i];
        cout<<" witness=";
        for(int i=0;i<15;i++)cout<<(i?",":"")<<a.witness[i];
        cout<<"\n";
        const auto &expect=r==2?h2:(r==3?h3:h4);
        if(a.hist!=expect || a.cases!=(r==2?70:(r==3?2760:37592)) ||
           a.max_g!=(r==2?3:(r==3?4:5)) || a.min_n!=(r==2?5:(r==3?8:9)))return 1;
    }
}
