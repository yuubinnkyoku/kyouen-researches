// c++ -std=c++17 -O3 -Wall -Wextra -pedantic verify.cpp -o /tmp/v && /tmp/v
// Two independent exact Node Kayles recurrences, all 3^11 four-center bases.
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;
using U = uint64_t;
int digit(U x,int s){return (x>>(2*(s-1)))&3;}
U add(U x,int s,int n){return x|(U(n)<<(2*(s-1)));}
array<unordered_map<U,uint8_t>,5> memo;
int quotient(int k,U x){
 if(!k)return 0;
 auto &m=memo[k];auto it=m.find(x);if(it!=m.end())return it->second;
 int opts=0;
 for(int c=0;c<k;c++){
  int p=0;for(int s=1;s<(1<<k);s++)if(!(s&(1<<c)))p^=digit(x,s)&1;
  opts|=1<<p;
 }
 for(int s=1;s<(1<<k);s++)if(digit(x,s)){
  int k2=k-__builtin_popcount((unsigned)s),cnt[16]={};
  for(int t=1;t<(1<<k);t++){
   int n=digit(x,t)-(s==t);if(!n)continue;
   int v=0,b=0;for(int c=0;c<k;c++)if(!(s&(1<<c))){if(t&(1<<c))v|=1<<b;b++;}
   cnt[v]+=n;
  }
  U y=0;for(int t=1;t<(1<<k2);t++)if(cnt[t])y=add(y,t,(cnt[t]&1)?1:2);
  opts|=1<<((cnt[0]&1)^quotient(k2,y));
 }
 int g=0;while(opts&(1<<g))g++;m[x]=g;return g;
}
struct Graph{
 array<uint32_t,32> adj{};unordered_map<uint32_t,uint8_t> cache;
 int n=4;
 void edge(int a,int b){adj[a]|=uint32_t(1)<<b;adj[b]|=uint32_t(1)<<a;}
 int g(uint32_t mask){
  int parity=0;uint32_t core=mask;
  for(uint32_t p=mask;p;p&=p-1){int i=__builtin_ctz(p);if(!(adj[i]&mask)){parity^=1;core&=~(uint32_t(1)<<i);}}
  if(!core)return parity;
  auto it=cache.find(core);if(it!=cache.end())return parity^it->second;
  int opts=0;
  for(uint32_t p=core;p;p&=p-1){int i=__builtin_ctz(p);opts|=1<<g(core&~(adj[i]|(uint32_t(1)<<i)));}
  int ans=0;while(opts&(1<<ans))ans++;cache[core]=ans;return parity^ans;
 }
};
int named(const array<int,16>&cnt,U&states){
 Graph g;
 for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)g.edge(i,j);
 for(int s=1;s<16;s++)for(int z=0;z<cnt[s];z++){
  int v=g.n++;assert(v<32);for(int c=0;c<4;c++)if(s&(1<<c))g.edge(v,c);
 }
 int ans=g.g((uint32_t(1)<<g.n)-1);states+=g.cache.size();return ans;
}
int main(){
 vector<int>types;for(int s=1;s<16;s++)if(__builtin_popcount((unsigned)s)>=2)types.push_back(s);
 assert(types.size()==11&&types.back()==15);
 array<int,11>power{};power[0]=1;for(int i=1;i<11;i++)power[i]=3*power[i-1];
 constexpr int N=177147;vector<uint8_t>vals(N);array<U,8>dist{};U states=0;
 for(int x=0;x<N;x++){
  array<int,16>cnt{};U key=0;
  for(int c=0;c<4;c++){cnt[1<<c]=1;key=add(key,1<<c,1);}
  for(int j=0;j<11;j++){int n=(x/power[j])%3;cnt[types[j]]=n;if(n)key=add(key,types[j],n);}
  int a=quotient(4,key),b=named(cnt,states);assert(a==b&&a<8);vals[x]=a;dist[a]++;
 }
 array<U,5>checked{},changed{};U to3=0,to2=0;
 for(int x=0;x<N;x++)for(int j=0;j<11;j++)if((x/power[j])%3==0){
  int s=types[j],rank=__builtin_popcount((unsigned)s),a=vals[x],b=vals[x+2*power[j]];
  checked[rank]++;if(a!=b)changed[rank]++;
  if(rank<=3)assert(a==b);
  else{
   bool criterion=true;int t=0;
   for(int c=0;c<4;c++){
    int parity=0;for(int h=0;h<10;h++)if(types[h]&(1<<c))parity^=((x/power[h])%3==1);
    if(!parity)criterion=false;
   }
   for(int h=0;h<10;h++)t+=((x/power[h])%3==1);
   assert((a!=b)==criterion);
   if(criterion){assert(a==((1+t)&1)&&b==3-a);if(a==0)to3++;else to2++;}
  }
 }
 assert(checked[2]==354294&&checked[3]==236196&&checked[4]==59049);
 assert(changed[2]==0&&changed[3]==0&&changed[4]==3564);
 assert(to3==1744&&to2==1820);
 cout<<"bases="<<N<<" independent_matches="<<N<<" named_core_states="<<states<<'\n';
 for(int r=2;r<=4;r++)cout<<"rank"<<r<<"_checks="<<checked[r]<<" changes="<<changed[r]<<'\n';
 cout<<"rank4_transitions_0_to_3="<<to3<<" rank4_transitions_1_to_2="<<to2<<'\n';
 cout<<"grundy_distribution=";for(int i=0;i<8;i++)cout<<(i?",":"")<<dist[i];cout<<'\n';
}
