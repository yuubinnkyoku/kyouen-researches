// Exact q5 period census: g++ -O3 -std=c++17 census.cpp -o census
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <numeric>
#include <vector>
using U=uint64_t;
U power(U a,U n,U m){U r=1;while(n){if(n&1)r=(__uint128_t)r*a%m;a=(__uint128_t)a*a%m;n>>=1;}return r;}
U joint(int p,const std::vector<int>&f,const std::vector<int>&a){U n=p-1;for(int q:f)while(n%q==0){bool ok=true;for(int x:a)if(power(x,n/q,p)!=1){ok=false;break;}if(!ok)break;n/=q;}return n;}
int main(int argc,char**argv){
 int N=argc>1?atoi(argv[1]):10000000;assert(N>37&&N<=20000000);
 std::vector<int> sp(N);for(int i=2;i<N;i++)if(!sp[i]){sp[i]=i;if((U)i*i<N)for(int j=i*i;j<N;j+=i)if(!sp[j])sp[j]=i;}
 const std::vector<int> a={2,3,5,7},b={2,4,6,8,10,12,14,16,18,20,24,32};
 std::map<U,U> hist;U count=0,shortened=0;std::vector<int> exceptional,max_primes;U maxindex=0;int first=0;
 for(int p=37;p<N;p++)if(sp[p]==p){
  ++count;int v=p-1;std::vector<int> f;while(v>1){int q=sp[v];f.push_back(q);while(v%q==0)v/=q;}
  U L=joint(p,f,a);assert(L==joint(p,f,b));U independently=1;
  for(int x:a)independently=std::lcm(independently,joint(p,f,{x}));assert(L==independently);
  U idx=(p-1)/L;hist[idx]++;if(idx>1){++shortened;if(!first)first=p;}
  if(idx>maxindex){maxindex=idx;max_primes.clear();}if(idx==maxindex)max_primes.push_back(p);
  U pp=(U)p*p;bool all=true;for(int x:a)if(power(x,L,pp)!=1){all=false;break;}if(all)exceptional.push_back(p);
 }
 std::cout<<"exclusive_bound="<<N<<" primes="<<count<<" shortened="<<shortened<<" first="<<first<<"\n";
 for(auto [i,n]:hist)std::cout<<i<<":"<<n<<" ";std::cout<<"\nmax_index="<<maxindex<<" primes=";
 for(int p:max_primes)std::cout<<p<<",";std::cout<<"\np2_exception_count="<<exceptional.size()<<" primes=";
 for(int p:exceptional)std::cout<<p<<",";std::cout<<"\n";
}
