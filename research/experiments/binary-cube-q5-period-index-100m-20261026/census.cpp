// Exact finite census for the q=5 binary-cube section periods, 32<p<1e8.
// Requires the previously proved four-generator minimal-period theorem (K0567).
// C++17, no third-party dependencies.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using u64=uint64_t;
static u64 power(u64 a,u64 e,u64 m){
    u64 r=1;
    while(e){if(e&1)r=(u64)((__uint128_t)r*a%m);a=(u64)((__uint128_t)a*a%m);e>>=1;}
    return r;
}
static bool all_one(u64 e,u64 p){
    for(u64 a: {2ULL,3ULL,5ULL,7ULL})if(power(a,e,p)!=1)return false;
    return true;
}
int main(int argc,char**argv){
    const int N=argc>1?std::stoi(argv[1]):100000000;
    std::vector<bool> prime(N,true);
    prime[0]=prime[1]=false;
    for(int i=2;(int64_t)i*i<N;++i)if(prime[i])
        for(int j=i*i;j<N;j+=i)prime[j]=false;
    std::vector<int> small;
    for(int i=2;(int64_t)i*i<N;++i)if(prime[i])small.push_back(i);
    u64 count=0,short_count=0,nonlift_count=0;
    u64 max_index=0,max_index_p=0;
    std::map<u64,u64> index_hist;
    std::vector<u64> wieferich2,exception;
    std::vector<std::pair<u64,u64>> high_indices;
    for(int p=37;p<N;++p){
        if(!prime[p])continue;
        ++count;
        u64 n=p-1,rem=n;
        std::vector<u64> factors;
        for(int q:small){
            if((u64)q*q>rem)break;
            if(rem%q==0){factors.push_back(q);do{rem/=q;}while(rem%q==0);}
        }
        if(rem>1)factors.push_back(rem);
        u64 L=n;
        for(u64 q:factors)while(L%q==0 && all_one(L/q,p))L/=q;
        assert(all_one(L,p));
        u64 idx=n/L;
        ++index_hist[idx];
        if(idx>1)++short_count;
        if(idx>=25)high_indices.emplace_back(p,idx);
        if(idx>max_index){max_index=idx;max_index_p=p;}
        u64 pp=(u64)p*p;
        bool w2=power(2,n,pp)==1;
        if(w2)wieferich2.push_back(p);
        bool all_w=true;
        for(u64 a:{2ULL,3ULL,5ULL,7ULL})if(power(a,n,pp)!=1){all_w=false;break;}
        bool nonlift=all_one(L,pp);
        assert(nonlift==all_w); // p does not divide (p-1)/L
        if(nonlift){++nonlift_count;exception.push_back(p);}
    }
    std::cout<<"N "<<N<<"\nprimes "<<count<<"\nshort "<<short_count
             <<"\nmax_index "<<max_index<<"\nmax_index_first_prime "<<max_index_p
             <<"\nnonlift "<<nonlift_count<<"\nwieferich_base2";
    for(u64 p:wieferich2)std::cout<<" "<<p;
    std::cout<<"\nnonlift_primes";
    for(u64 p:exception)std::cout<<" "<<p;
    std::cout<<"\nindex_hist";
    for(auto [idx,c]:index_hist)std::cout<<" "<<idx<<":"<<c;
    std::cout<<"\nhigh_indices";
    for(auto [p,idx]:high_indices)std::cout<<" "<<p<<":"<<idx;
    std::cout<<"\n";
}
