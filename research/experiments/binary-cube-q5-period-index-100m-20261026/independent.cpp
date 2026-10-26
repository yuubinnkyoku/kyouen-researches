// Independent audit: odd-only sieve, four separate multiplicative orders,
// then lcm (rather than directly reducing the common period).
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <string>
#include <vector>
using u64=uint64_t;
static u64 powmod(u64 x,u64 k,u64 p){
    u64 y=1;
    while(k){if(k%2)y=(__uint128_t)y*x%p;x=(__uint128_t)x*x%p;k/=2;}
    return y;
}
int main(int argc,char**argv){
    int limit=argc>1?std::stoi(argv[1]):100000000;
    int start=argc>2?std::stoi(argv[2]):37;
    // Only odd n=2*i+1 are represented; 1 is marked composite.
    std::vector<unsigned char> composite((limit+1)/2,0);
    composite[0]=1;
    for(int i=3;(int64_t)i*i<limit;i+=2)if(!composite[i/2])
        for(int64_t j=(int64_t)i*i;j<limit;j+=2*i)composite[j/2]=1;
    // Independently precompute smallest odd prime factors in a 16-bit table.
    std::vector<uint16_t> smallest((limit+1)/2,0);
    for(int i=3;(int64_t)i*i<limit;i+=2)if(!composite[i/2])
        for(int64_t j=(int64_t)i*i;j<limit;j+=2*i)
            if(!smallest[j/2])smallest[j/2]=(uint16_t)i;
    u64 count=0,short_count=0,max_index=0,first_max=0;
    std::map<u64,u64> histogram;
    std::vector<int> wieferich;
    for(int p=start|1;p<limit;p+=2){
        if(composite[p/2])continue;
        ++count;
        u64 rem=p-1;
        std::vector<u64> qs;
        while(rem>1){
            u64 q=rem%2==0?2:(smallest[rem/2]?smallest[rem/2]:rem);
            qs.push_back(q);
            do{rem/=q;}while(rem%q==0);
        }
        u64 period=1;
        for(u64 a:{2ULL,3ULL,5ULL,7ULL}){
            u64 ord=p-1;
            for(u64 q:qs)while(ord%q==0 && powmod(a,ord/q,p)==1)ord/=q;
            assert(powmod(a,ord,p)==1);
            period=std::lcm(period,ord);
        }
        u64 index=(p-1)/period;
        ++histogram[index];
        if(index>1)++short_count;
        if(index>max_index){max_index=index;first_max=p;}
        if(powmod(2,p-1,(u64)p*p)==1){
            wieferich.push_back(p);
            // A single non-Wieferich base certifies h_p=1.
            bool all=true;
            for(u64 a:{3ULL,5ULL,7ULL})if(powmod(a,p-1,(u64)p*p)!=1){all=false;break;}
            assert(!all);
        }
    }
    std::cout<<"N "<<limit<<"\nprimes "<<count<<"\nshort "<<short_count
             <<"\nmax_index "<<max_index<<"\nmax_index_first_prime "<<first_max
             <<"\nwieferich_base2";
    for(int p:wieferich)std::cout<<" "<<p;
    std::cout<<"\nindex_hist";
    for(auto [idx,c]:histogram)std::cout<<" "<<idx<<":"<<c;
    std::cout<<"\n";
}
