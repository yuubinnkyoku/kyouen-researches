// Complete congruence census for odd composite period indices.
// Usage: g++ -O3 -std=c++17 direct.cpp -o direct && ./direct 100000000
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
#include <array>
using namespace std;
using u64=uint64_t;
u64 modpow(u64 a,u64 e,u64 p){
    u64 z=1;
    while(e){if(e&1) z=z*a%p; a=a*a%p; e>>=1;}
    return z;
}
int main(int argc,char**argv){
    int N=argc>1?atoi(argv[1]):100000000;
    if(N<37||N>100000000){cerr<<"require 37<=N<=100000000\n";return 2;}
    vector<uint8_t> composite(N,0);
    for(int i=2;1LL*i*i<N;++i)
        if(!composite[i])
            for(int64_t j=1LL*i*i;j<N;j+=i) composite[j]=1;
    const array<int,10> ns={3,5,7,9,15,21,35,45,63,105};
    array<int,10> count={},first={};
    int primes=0;
    for(int p=37;p<N;p+=2){
        if(composite[p]) continue;
        ++primes;
        for(size_t i=0;i<ns.size();++i){
            int n=ns[i];
            if((p-1)%n) continue;
            u64 e=(p-1)/n;
            if(modpow(2,e,p)!=1||modpow(3,e,p)!=1||
               modpow(5,e,p)!=1||modpow(7,e,p)!=1) continue;
            ++count[i];
            if(!first[i]) first[i]=p;
        }
    }
    cout<<"limit "<<N<<" primes "<<primes<<"\n";
    for(size_t i=0;i<ns.size();++i)
        cout<<ns[i]<<" "<<count[i]<<" "<<first[i]<<"\n";
}
