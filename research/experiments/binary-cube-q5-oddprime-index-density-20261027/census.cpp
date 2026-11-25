// Exact finite census for odd-prime divisors of the q=5 period index.
// g++ -O3 -std=c++17 census.cpp -o census && ./census 100000000
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using u64=std::uint64_t;
static u64 modpow(u64 a,u64 e,u64 p){
    u64 r=1;
    while(e){if(e&1)r=r*a%p; a=a*a%p;e>>=1;}
    return r;
}
int main(int argc,char**argv){
    u64 limit=argc>1?std::strtoull(argv[1],nullptr,10):1000000;
    if(limit<37 || limit>100000000){std::cerr<<"limit must be 37..100000000\n";return 2;}
    std::vector<bool> prime(limit,true);
    prime[0]=prime[1]=false;
    for(u64 i=2;i*i<limit;i++)if(prime[i])for(u64 j=i*i;j<limit;j+=i)prime[j]=false;
    constexpr std::array<unsigned,7> ell={3,5,7,11,13,17,19};
    constexpr std::array<u64,4> bases={2,3,5,7};
    std::array<std::array<u64,3>,7> counts{};
    std::array<std::array<u64,3>,7> first{};
    u64 total=0;
    for(u64 p=37;p<limit;p+=2){
        if(!prime[p])continue;
        ++total;
        for(unsigned j=0;j<ell.size();++j){
            u64 q=ell[j];
            for(unsigned r=0;r<3;++r){
                if((p-1)%q)break;
                u64 exp=(p-1)/q;
                bool ok=true;
                for(u64 a:bases)if(modpow(a,exp,p)!=1){ok=false;break;}
                if(ok){++counts[j][r];if(!first[j][r])first[j][r]=p;}
                q*=ell[j];
            }
        }
    }
    std::cout<<"limit="<<limit<<" primes="<<total<<"\n";
    for(unsigned j=0;j<ell.size();++j)
        for(unsigned r=0;r<3;++r)
            std::cout<<"ell="<<ell[j]<<" r="<<r+1<<" count="<<counts[j][r]<<" first="<<first[j][r]<<"\n";
}
