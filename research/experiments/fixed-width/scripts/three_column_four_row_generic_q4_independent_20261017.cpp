#include <array>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;

static constexpr int N=12;
static constexpr int LIMIT=1<<N;

long long det4(const array<array<long long,4>,4>& a){
    array<int,4> p={0,1,2,3};
    long long ans=0;
    do {
        int inversions=0;
        for(int i=0;i<4;i++) for(int j=i+1;j<4;j++) inversions+=(p[i]>p[j]);
        long long term=1;
        for(int i=0;i<4;i++) term*=a[i][p[i]];
        ans+=(inversions%2?-term:term);
    }while(next_permutation(p.begin(),p.end()));
    return ans;
}
vector<int> forbidden(int a,int b,int d){
    vector<array<long long,4>> rows;
    for(int x:{0,a,a+b}) for(int y=0;y<4;y++) {
        long long Y=1LL*d*y;
        rows.push_back({1LL*x*x+Y*Y,x,Y,1});
    }
    vector<int> edges;
    for(int i=0;i<N;i++)for(int j=i+1;j<N;j++)
    for(int k=j+1;k<N;k++)for(int l=k+1;l<N;l++) {
        array<array<long long,4>,4> mat={rows[i],rows[j],rows[k],rows[l]};
        if(det4(mat)==0)edges.push_back((1<<i)|(1<<j)|(1<<k)|(1<<l));
    }
    return edges;
}
int main(){
    auto edges=forbidden(1,1,2);
    assert(edges.size()==27);
    assert(forbidden(2,3,1).size()==35);
    vector<bool> safe(LIMIT,true);
    for(int s=0;s<LIMIT;s++) for(int e:edges) if((s&e)==e){safe[s]=false;break;}
    vector<int> memo(LIMIT,-1);
    auto rec=[&](auto&& self,int s)->int {
        if(memo[s]!=-1)return memo[s];
        unsigned options=0;
        for(int i=0;i<N;i++)if(!(s&(1<<i))&&safe[s|(1<<i)]){
            int g=self(self,s|(1<<i));
            options|=1u<<g;
        }
        int nim=0;
        while(options&(1u<<nim))nim++;
        return memo[s]=nim;
    };
    array<int,13> hist{},maximal{};
    int count=0;
    for(int s=0;s<LIMIT;s++)if(safe[s]){
        count++;
        hist[rec(rec,s)]++;
        bool terminal=true;
        for(int i=0;i<N;i++)if(!(s&(1<<i))&&safe[s|(1<<i)])terminal=false;
        if(terminal)maximal[__builtin_popcount((unsigned)s)]++;
    }
    assert(count==1655 && memo[0]==0);
    for(int i=0;i<N;i++)assert(memo[1<<i]==4);
    assert(hist[0]==397&&hist[1]==514&&hist[2]==384&&hist[3]==324&&hist[4]==36);
    assert(maximal[5]==12&&maximal[6]==144&&maximal[7]==24);
    cout<<"PASS independent C++ 4x4 determinant and recursive Grundy: "<<count
        <<" safe, root "<<memo[0]<<", all 12 first nimbers 4\n";
    for(int i=0;i<5;i++)cout<<"g="<<i<<" count="<<hist[i]<<"\n";
    for(int i=5;i<=7;i++)cout<<"maximal size="<<i<<" count="<<maximal[i]<<"\n";
}
