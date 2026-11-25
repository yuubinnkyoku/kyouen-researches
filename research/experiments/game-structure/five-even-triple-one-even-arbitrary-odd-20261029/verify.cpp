// Five-center split Node Kayles: a triple type may gain two vertices
// when every other non-private type is odd/absent, except for ONE even type.
// Exhaustive enumeration under the S3 x S2 symmetry preserving target {0,1,2}.
// Build: c++ -std=c++17 -O3 -Wall -Wextra -pedantic verify.cpp -o verify
// Run: ./verify
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>
using namespace std;
constexpr int N=5, FULL=31, TARGET=7;
vector<int> types;
vector<array<int,25>> perms;
uint32_t intersect[32]={}, cover[32][32]={};
int onebits[32]={};

// Exact quotient recurrence. p[r] is the parity of non-isolated
// independent vertices while the surviving clique is r.
// An even type changes legal options but not any parity.
int evaluate(uint32_t odd, int even, int &with_two) {
    int p[32],g0[32]={},g2[32]={};
    for(int r=0;r<=FULL;r++)
        p[r]=(__builtin_popcount((unsigned)r)&1)
            ^(__builtin_popcount(odd&intersect[r])&1);
    for(int r=1;r<=FULL;r++){
        unsigned a=0,b=0;
        int pr=p[r];
        for(int c=0;c<N;c++)
            if(r&(1<<c))a|=1u<<(pr^p[1<<c]);
        b=a;
        int te=TARGET&r,ee=even&r;
        for(int t=r;t;t=(t-1)&r){
            bool present=(odd&cover[r][t]) || (onebits[t]==1) || (ee==t);
            bool target=(te==t);
            if(!present&&!target)continue;
            int child=r^t, isolated=pr^p[child]^1;
            if(present)a|=1u<<(g0[child]^isolated);
            if(present||target)b|=1u<<(g2[child]^isolated);
        }
        g0[r]=__builtin_ctz(~a);
        g2[r]=__builtin_ctz(~b);
    }
    with_two=g2[FULL];return g0[FULL];
}
uint32_t image(uint32_t mask,const array<int,25>& perm){
    uint32_t out=0;
    while(mask){
        int j=__builtin_ctz(mask);mask&=mask-1;
        out|=1u<<perm[j];
    }
    return out;
}
uint32_t orbit(uint32_t mask,const vector<int>& group){
    uint32_t arr[12];int n=0;
    for(int k:group){
        uint32_t m=image(mask,perms[k]);
        bool seen=false;
        for(int i=0;i<n;i++)if(arr[i]==m)seen=true;
        if(!seen)arr[n++]=m;
    }
    return n;
}
int main(){
    for(int s=1;s<=FULL;s++){
        onebits[s]=__builtin_popcount((unsigned)s);
        if(onebits[s]>=2&&s!=TARGET)types.push_back(s);
    }
    assert(types.size()==25);
    for(int r=1;r<=FULL;r++)for(int j=0;j<25;j++){
        int s=types[j],t=s&r;
        if(t){intersect[r]|=1u<<j;cover[r][t]|=1u<<j;}
    }
    vector<int> p={0,1,2},q={3,4};
    do{do{
        int f[5]={p[0],p[1],p[2],q[0],q[1]};
        array<int,25> perm{};
        for(int j=0;j<25;j++){
            int s=types[j],t=0;
            for(int c=0;c<5;c++)if(s&(1<<c))t|=1<<f[c];
            auto it=find(types.begin(),types.end(),t);
            assert(it!=types.end());
            perm[j]=it-types.begin();
        }
        perms.push_back(perm);
    }while(next_permutation(q.begin(),q.end()));}while(next_permutation(p.begin(),p.end()));
    assert(perms.size()==12);
    uint64_t total=0,weighted=0;
    int even_orbits=0;
    for(int e=0;e<25;e++){
        bool isrep=true;
        for(auto &perm:perms)if(perm[e]<e)isrep=false;
        if(!isrep)continue;
        even_orbits++;
        vector<int> group;
        for(int k=0;k<12;k++)if(perms[k][e]==e)group.push_back(k);
        int orbitE=12/group.size();
        int other[24],n=0;
        for(int j=0;j<25;j++)if(j!=e)other[n++]=j;
        uint64_t cases=0,w=0;
        for(uint32_t x=0;x<(1u<<24);x++){
            uint32_t odd=0;
            uint32_t y=x;
            while(y){
                int bit=__builtin_ctz(y);y&=y-1;
                odd|=1u<<other[bit];
            }
            bool canonical=true;
            for(int k:group)
                if(image(odd,perms[k])<odd){canonical=false;break;}
            if(!canonical)continue;
            int g2,g0=evaluate(odd,types[e],g2);
            if(g0!=g2){
                printf("FAIL even=%d oddbits=%u g0=%d g2=%d\n",
                       types[e],odd,g0,g2);
                return 2;
            }
            cases++;
            w+=orbit(odd,group);
        }
        if(w!=(1u<<24))return 3;
        total+=cases;weighted+=w*orbitE;
        printf("even=%d orbitE=%d stabilizer=%zu representatives=%llu weighted=%llu\n",
            types[e],orbitE,group.size(),(unsigned long long)cases,
            (unsigned long long)(w*orbitE));
    }
    if(weighted!=25ull*(1u<<24))return 4;
    if(even_orbits!=8||total!=35454336ull)return 5;
    printf("PASS even_orbits=%d representatives=%llu weighted=%llu\n",
        even_orbits,(unsigned long long)total,(unsigned long long)weighted);
}
