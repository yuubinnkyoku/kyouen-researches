// Independent C++ exhaustive clique-mask mex for k=5 and four missing pair types.
#include <array>
#include <algorithm>
#include <cassert>
#include <iostream>
#include <set>
#include <utility>
#include <vector>
using namespace std;
using Edge=pair<int,int>;
int main() {
    const vector<vector<Edge>> patterns={
        {{0,1},{0,2},{0,3},{0,4}},
        {{0,1},{0,2},{0,3},{1,2}},
        {{0,1},{0,2},{0,3},{1,4}},
        {{0,1},{0,2},{1,2},{3,4}},
        {{0,1},{0,2},{1,3},{2,3}},
        {{0,1},{0,2},{1,3},{2,4}}
    };
    int grand=0;
    for (size_t shape=0;shape<patterns.size();++shape) {
        vector<int> sig;
        for(int i=0;i<5;++i)for(int j=i+1;j<5;++j)
            if(!count(patterns[shape].begin(),patterns[shape].end(),Edge{i,j}))
                sig.push_back((1<<i)|(1<<j));
        assert(sig.size()==6);
        for(int i=0;i<5;++i)sig.push_back(1<<i);
        array<int,4> distribution{};
        int mismatches=0;
        for(int parity=0;parity<64;++parity) {
            for(int leaves=0;leaves<243;++leaves) {
                array<int,11> multiplicity{};
                for(int i=0;i<6;++i)multiplicity[i]=1+((parity>>i)&1);
                int rem=leaves;
                for(int i=6;i<11;++i){multiplicity[i]=rem%3;rem/=3;}
                array<int,32> active{},dp{};
                array<int,5> z{};
                for(int i=0;i<11;++i)if(multiplicity[i]&1) {
                    for(int mask=1;mask<32;++mask)if(mask&sig[i])active[mask]^=1;
                    for(int c=0;c<5;++c)if(sig[i]&(1<<c))z[c]^=1;
                }
                for(int mask=1;mask<32;++mask) {
                    unsigned seen=0;
                    for(int c=0;c<5;++c)if(mask&(1<<c))
                        seen|=1u<<(active[mask]^z[c]);
                    for(int i=0;i<11;++i)if(multiplicity[i] && (mask&sig[i])) {
                        int next=mask&~sig[i];
                        int child=dp[next]^active[mask]^active[next]^1;
                        seen|=1u<<child;
                    }
                    int g=0;
                    while(seen&(1u<<g))++g;
                    dp[mask]=g;
                }
                int u=active[31];
                bool uniform=true;
                for(int c=1;c<5;++c)if(z[c]!=z[0])uniform=false;
                int predicted=uniform?(1^u^z[0]):2+u;
                assert(dp[31]>=0 && dp[31]<=3);
                distribution[dp[31]]++;
                mismatches+=(dp[31]!=predicted);
            }
        }
        assert(mismatches==(shape==0?4856:0));
        int total=0;
        for(int n:distribution)total+=n;
        assert(total==15552);
        grand+=total;
        cout<<"shape="<<shape+1<<" count="<<total<<" mismatch="<<mismatches
            <<" g0="<<distribution[0]<<" g1="<<distribution[1]
            <<" g2="<<distribution[2]<<" g3="<<distribution[3]<<"\n";
    }
    assert(grand==93312);
    cout<<"PASS 93312 C++ exhaustive representatives\n";
}
