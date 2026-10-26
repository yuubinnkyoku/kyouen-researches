// Independent census: factor p-1, strip the common multiplicative order.
// Usage: g++ -O3 -std=c++17 independent.cpp -o independent && ./independent 100000000
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
#include <array>
using namespace std;
using u64=uint64_t;
u64 modpow(u64 a,u64 e,u64 p){
    u64 z=1;
    for(;e;e>>=1,a=a*a%p) if(e&1) z=z*a%p;
    return z;
}
int main(int argc,char**argv){
    int N=argc>1?atoi(argv[1]):10000000;
    if(N<37||N>100000000){cerr<<"require 37<=N<=100000000\n";return 2;}
    vector<int> least(N,0),primes;
    for(int i=2;i<N;++i){
        if(!least[i]){least[i]=i;primes.push_back(i);}
        for(int q:primes){
            int64_t x=1LL*i*q;
            if(x>=N||q>least[i]) break;
            least[x]=q;
        }
    }
    const array<int,10> ns={3,5,7,9,15,21,35,45,63,105};
    array<int,10> count={},first={};
    int checked=0;
    for(int p:primes){
        if(p<=32) continue;
        int k=p-1;
        if(k%3 && k%5 && k%7) continue;
        ++checked;
        vector<int> factors;
        int t=k;
        while(t>1){
            int q=least[t];
            factors.push_back(q);
            do{t/=q;}while(t%q==0);
        }
        int L=k;
        for(int q:factors){
            while(L%q==0){
                int candidate=L/q;
                bool good=true;
                for(int a:{2,3,5,7})
                    if(modpow(a,candidate,p)!=1){good=false;break;}
                if(!good) break;
                L=candidate;
            }
        }
        int index=k/L;
        for(size_t i=0;i<ns.size();++i){
            if(index%ns[i]) continue;
            ++count[i];
            if(!first[i]) first[i]=p;
        }
    }
    cout<<"limit "<<N<<" checked "<<checked<<"\n";
    for(size_t i=0;i<ns.size();++i)
        cout<<ns[i]<<" "<<count[i]<<" "<<first[i]<<"\n";
}
