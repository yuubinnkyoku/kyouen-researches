// Independent integer-affine-rank verification of d=5, q=16.
// Enumerate all affine hyperplanes through 5 affinely independent cube
// vertices, retain those containing exactly 16 of the 32 vertices.
// No coordinate/diagonal face classification is assumed.
// g++ -std=c++17 -O3 -Wall -Wextra -Werror verify_d5_dense_swap_rank.cpp -o /tmp/d5rank && /tmp/d5rank
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <set>
#include <unordered_map>
#include <vector>
using namespace std;
int det4(array<array<int,4>,4> a){
    array<int,4> p{0,1,2,3};int ans=0;
    do{
        int prod=1,inv=0;
        for(int i=0;i<4;i++){
            prod*=a[i][p[i]];
            for(int j=i+1;j<4;j++)inv+=(p[i]>p[j]);
        }
        ans+=(inv%2?-prod:prod);
    }while(next_permutation(p.begin(),p.end()));
    return ans;
}
array<int,5> normal(const array<int,5>& pts){
    array<int,5> n{};
    for(int skip=0;skip<5;skip++){
        array<array<int,4>,4> m{};
        for(int i=0;i<4;i++){
            int col=0;
            for(int j=0;j<5;j++)if(j!=skip)
                m[i][col++]=((pts[i+1]>>j)&1)-((pts[0]>>j)&1);
        }
        n[skip]=(skip%2?-1:1)*det4(m);
    }
    return n;
}
int dot(array<int,5> n,int x){
    int v=0;for(int j=0;j<5;j++)v+=n[j]*((x>>j)&1);return v;
}
template<class F> void each_comb(int n,int k,F &&func){
    uint64_t m=(uint64_t(1)<<k)-1,lim=uint64_t(1)<<n;
    while(m<lim){func(uint32_t(m));uint64_t a=m&-m,b=m+a;m=(((m^b)>>2)/a)|b;}
}
int main(){
    set<uint32_t> hyperplanes;
    long long bases=0;
    for(int a=0;a<32;a++)for(int b=a+1;b<32;b++)
    for(int c=b+1;c<32;c++)for(int d=c+1;d<32;d++)
    for(int e=d+1;e<32;e++){
        auto n=normal({a,b,c,d,e});
        if(all_of(n.begin(),n.end(),[](int z){return z==0;}))continue;
        bases++;
        int v=dot(n,a);uint32_t mask=0;
        for(int x=0;x<32;x++)if(dot(n,x)==v)mask|=uint32_t(1)<<x;
        if(__builtin_popcount(mask)==16)hyperplanes.insert(mask);
    }
    cout<<"affinely independent bases="<<bases
        <<" distinct 16-point hyperplanes="<<hyperplanes.size()<<'\n';
    assert(bases==179136&&hyperplanes.size()==30);
    auto safe=[&](uint32_t m){
        for(uint32_t f:hyperplanes)if(!(m&f))return false;
        return true;
    };
    // All 7-point complement masks, with complete descendant recursion
    // down to the minimal hitting size 4.
    unordered_map<uint32_t,int> prev,curr;
    uint64_t counts[8]={},bad=0;
    for(int t=4;t<=7;t++){
        curr.clear();
        if(t<7)curr.reserve(t==4?4000:(t==5?100000:750000));
        each_comb(32,t,[&](uint32_t m){
            if(!safe(m))return;
            counts[t]++;
            int gs=0,hs=0;bool has=false;
            for(uint32_t z=m;z;z&=z-1){
                auto it=prev.find(m^(z&-z));
                if(it==prev.end())continue;
                has=true;int val=it->second;
                gs|=1<<(val/8);hs|=1<<(val%8);
            }
            int g=0,h=1;
            if(has){
                h=0;while(gs&(1<<g))++g;while(hs&(1<<h))++h;
            }
            if(t<7)curr.emplace(m,8*g+h);
            else if(h!=(g<2?1-g:g)){assert(g==0&&h==0);bad++;}
        });
        cout<<"t="<<t<<" safe="<<counts[t]<<'\n';
        prev.swap(curr);
    }
    cout<<"t=7 exchange failures="<<bad<<'\n';
    assert(counts[4]==3360&&counts[5]==89376&&counts[6]==675472&&counts[7]==3025376);
    assert(bad==34560);
    // Directly verify one simple 7-point witness and its six legal children.
    const vector<int> T{0,1,2,7,13,24,28};
    array<int,128> g{},h{};g.fill(-1);h.fill(-1);
    array<bool,128> ok{};
    for(int m=0;m<128;m++){
        uint32_t mask=0;
        for(int i=0;i<7;i++)if(m&(1<<i))mask|=uint32_t(1)<<T[i];
        ok[m]=safe(mask);
    }
    for(int m=1;m<128;m++){
        if(!ok[m])continue;
        int gs=0,hs=0;bool has=false;
        for(int i=0;i<7;i++)if(m&(1<<i)){
            int sub=m^(1<<i);
            if(!ok[sub])continue;
            has=true;gs|=1<<g[sub];hs|=1<<h[sub];
        }
        if(!has){g[m]=0;h[m]=1;}
        else{
            g[m]=0;h[m]=0;
            while(gs&(1<<g[m]))++g[m];
            while(hs&(1<<h[m]))++h[m];
        }
    }
    assert(g[127]==0&&h[127]==0);
    int legal=0;
    for(int i=0;i<7;i++){
        int sub=127^(1<<i);
        if(!ok[sub]){assert(T[i]==13);continue;}
        legal++;
        assert(g[sub]==2&&h[sub]==2);
    }
    assert(legal==6);
    cout<<"witness T={0,1,2,7,13,24,28}, (g,h)=(0,0), legal moves=6\n";
}
