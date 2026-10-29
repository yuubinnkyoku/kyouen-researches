// Five-center split Node Kayles: deletion of an even triple-support type.
// Complete orbit enumeration under S3 x S2 preserving target {0,1,2}.
// Build: c++ -std=c++17 -O3 -Wall -Wextra -pedantic verify.cpp -o verify
// Run: ./verify odd && ./verify mixed8
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
using namespace std;
constexpr int K=5, TARGET=7, FULL=31, MAX_EXTRA=8;
int counts[32]={};
uint32_t intersect_bits[32]={};
vector<int> types;
vector<array<int,25>> perms;
uint64_t sets[9]={}, cases[9]={}, weighted[9]={};

// Surviving clique mask R. Adding two T-vertices does not alter any
// isolated-vertex parity; it adds only an independent move of type T.
// The recurrence is exact Node Kayles closed-neighborhood deletion.
int evaluate(int &with_two){
    int active[32],n=0;
    uint32_t parity=0;
    for(int s=1;s<=FULL;++s)if(counts[s]){
        active[n++]=s;
        if(counts[s]&1)parity^=intersect_bits[s];
    }
    int g0[32]={},g2[32]={};
    for(int R=1;R<=FULL;++R){
        int p=(parity>>R)&1;
        unsigned options0=0;
        for(int c=0;c<K;++c)if(R&(1<<c)){
            int child=p^((parity>>(1<<c))&1);
            options0|=1u<<child;
        }
        unsigned options2=options0;
        for(int j=0;j<n;++j){
            int s=active[j];
            if(!(s&R))continue;
            int next=R&~s;
            int isolated=p^((parity>>next)&1)^1;
            int child0=g0[next]^isolated;
            int child2=g2[next]^isolated;
            if(child0>=31||child2>=31)abort();
            options0|=1u<<child0;
            options2|=1u<<child2;
        }
        if(R&TARGET){
            int next=R&~TARGET;
            int isolated=p^((parity>>next)&1)^1;
            int child=g2[next]^isolated;
            if(child>=31)abort();
            options2|=1u<<child;
        }
        g0[R]=__builtin_ctz(~options0);
        g2[R]=__builtin_ctz(~options2);
    }
    with_two=g2[FULL];
    return g0[FULL];
}
uint32_t image(uint32_t mask,const array<int,25>&perm){
    uint32_t transformed=0;
    while(mask){
        int j=__builtin_ctz(mask);
        mask&=mask-1;
        transformed|=1u<<perm[j];
    }
    return transformed;
}
bool canonical(uint32_t mask){
    for(const auto &perm:perms)if(image(mask,perm)<mask)return false;
    return true;
}
int orbit_size(uint32_t mask){
    uint32_t seen[12];int n=0;
    for(const auto &perm:perms){
        uint32_t v=image(mask,perm);
        bool found=false;
        for(int j=0;j<n;++j)if(seen[j]==v){found=true;break;}
        if(!found)seen[n++]=v;
    }
    return n;
}
void check(uint32_t mask,int k){
    int g2,g0=evaluate(g2);
    if(g0!=g2){
        fprintf(stderr,"COUNTEREXAMPLE mask=%u k=%d g0=%d g2=%d\n",mask,k,g0,g2);
        for(int s:types)if(counts[s])fprintf(stderr," %d:%d",s,counts[s]);
        fputc('\n',stderr);
        exit(2);
    }
}
void assign(const vector<int>&chosen,int i,int k,uint32_t mask){
    if(i==k){++cases[k];check(mask,k);return;}
    int s=chosen[i];
    counts[s]=1;assign(chosen,i+1,k,mask);
    counts[s]=2;assign(chosen,i+1,k,mask);
    counts[s]=0;
}
void subsets(int start,int k,uint32_t mask,vector<int>&chosen){
    if((int)chosen.size()==k){
        if(!canonical(mask))return;
        ++sets[k];
        weighted[k]+=orbit_size(mask);
        assign(chosen,0,k,mask);
        return;
    }
    for(int j=start;j<=25-(k-(int)chosen.size());++j){
        chosen.push_back(types[j]);
        subsets(j+1,k,mask|(1u<<j),chosen);
        chosen.pop_back();
    }
}
void run_mixed8(){
    vector<int> chosen;
    uint64_t binom=1,total=0;
    for(int k=0;k<=MAX_EXTRA;++k){
        if(k)binom=binom*(26-k)/k;
        subsets(0,k,0,chosen);
        uint64_t expected=binom*(1ull<<k);
        total+=cases[k];
        printf("k=%d support_orbits=%llu cases=%llu weighted=%llu expected=%llu\n",k,
            (unsigned long long)sets[k],(unsigned long long)cases[k],
            (unsigned long long)(weighted[k]*(1ull<<k)),(unsigned long long)expected);
        if(weighted[k]!=binom||cases[k]!=sets[k]*(1ull<<k))exit(3);
    }
    printf("PASS mixed8 total_representatives=%llu\n",(unsigned long long)total);
}
void run_odd(){
    uint64_t reps=0,weighted_count=0;
    for(uint32_t mask=0;mask<(1u<<25);++mask){
        if(!canonical(mask))continue;
        ++reps;
        uint32_t bits=mask;
        while(bits){
            int j=__builtin_ctz(bits);
            bits&=bits-1;
            counts[types[j]]=1;
        }
        check(mask,__builtin_popcount(mask));
        bits=mask;
        while(bits){
            int j=__builtin_ctz(bits);
            bits&=bits-1;
            counts[types[j]]=0;
        }
        weighted_count+=orbit_size(mask);
    }
    printf("PASS all_odd representatives=%llu weighted=%llu expected=%u\n",
        (unsigned long long)reps,(unsigned long long)weighted_count,1u<<25);
    if(weighted_count!=(1u<<25))exit(4);
}
int main(int argc,char**argv){
    if(argc!=2||(strcmp(argv[1],"mixed8")&&strcmp(argv[1],"odd"))){
        fprintf(stderr,"usage: verify mixed8|odd\n");
        return 1;
    }
    for(int c=0;c<K;++c)counts[1<<c]=1;
    for(int s=1;s<=FULL;++s){
        for(int R=1;R<=FULL;++R)if(s&R)intersect_bits[s]|=1u<<R;
        if(__builtin_popcount((unsigned)s)>=2&&s!=TARGET)types.push_back(s);
    }
    vector<int> p={0,1,2},q={3,4};
    do{do{
        int f[5]={p[0],p[1],p[2],q[0],q[1]};
        array<int,25> perm{};
        for(int j=0;j<25;++j){
            int s=types[j],t=0;
            for(int c=0;c<K;++c)if(s&(1<<c))t|=1<<f[c];
            auto it=find(types.begin(),types.end(),t);
            if(it==types.end())abort();
            perm[j]=int(it-types.begin());
        }
        perms.push_back(perm);
    }while(next_permutation(q.begin(),q.end()));}while(next_permutation(p.begin(),p.end()));
    if(types.size()!=25||perms.size()!=12)abort();
    if(!strcmp(argv[1],"mixed8"))run_mixed8();
    else if(!strcmp(argv[1],"odd"))run_odd();
    else return 1;
}
