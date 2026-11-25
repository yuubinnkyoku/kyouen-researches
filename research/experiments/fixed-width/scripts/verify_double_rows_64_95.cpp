// Independent transposed-residue verifier; C++17, unsigned __int128.
// T(63)=16 from K0369 is the only inductive external input.
#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std; using U=__uint128_t;
int bits(U a){return __builtin_popcountll((uint64_t)a)+__builtin_popcountll((uint64_t)(a>>64));}
vector<U> maximal(vector<U> v){
 sort(v.begin(),v.end());v.erase(unique(v.begin(),v.end()),v.end());
 sort(v.begin(),v.end(),[](U a,U b){return bits(a)!=bits(b)?bits(a)>bits(b):a<b;});
 vector<U> out;
 for(U a:v){bool dominated=false;for(U b:out)if((a&b)==a){dominated=true;break;}if(!dominated)out.push_back(a);}
 return out;
}
vector<U> local(int len,int p,int K){
 vector<U> all;
 for(int c=0;c<p;c++){
  vector<uint64_t> allowed(len,0);
  for(int y=0;y<len;y++){
   int z=(2*y+c)%p;z=z*z%p;
   for(int x=0;x<p;x++)allowed[y]|=uint64_t(1)<<((z+x*x)%p);
  }
  for(int n=0;n<p;n++){
   U m=0;for(int y=0;y<len;y++)if((allowed[y]>>n)&1)m|=U(1)<<y;
   if(bits(m)>=K && (m&1) && ((m>>(len-1))&1))all.push_back(m);
  }
 }
 return maximal(move(all));
}
int witness(int w,int c,int d){int count=0;for(int y=0;y<w;y++){
 int disc=1-4*(y*y+c*y+d);if(disc<=0)continue;
 int s=sqrt(disc);while(s*s<disc)s++;while(s*s>disc)s--;
 if(s*s==disc && (s&1)){
  int x1=(-1-s)/2,x2=(-1+s)/2;
  assert(x1!=x2 && x1*x1+y*y+x1+c*y+d==0 && x2*x2+y*y+x2+c*y+d==0);
  count++;
 }
}return count;}
int main(){const vector<int> mods={9,11,7,49,19,23,31,37,41,43,47,53};
 assert(witness(63,-47,0)==16);int prev=16;
 for(int w=64;w<=95;w++){
  int count=w<=82?witness(w,-47,0):witness(w,-105,-6);
  assert(count>=prev && count<=prev+1);
  if(count==prev+1){prev=count;cout<<"WIDTH "<<w<<" EXACT "<<prev<<" WITNESS_STEP\n";continue;}
  int K=prev+1;
  for(int g=1;g*(K-1)<=w-1;g++)if((w-1)%g==0){
   int len=(w-1)/g+1;vector<U> states={((U(1)<<len)-1)};bool excluded=false;
   for(int p:mods){if(gcd(g,p)!=1)continue;
    auto loc=local(len,p,K);vector<U> next;
    for(U a:states)for(U b:loc){U v=a&b;if(bits(v)>=K)next.push_back(v);}
    states=maximal(move(next));
    cout<<"CASE "<<w<<" "<<K<<" "<<g<<" "<<p<<" "<<loc.size()<<" "<<states.size()<<"\n";
    if(states.empty()){excluded=true;break;}
   }
   assert(excluded);
  }
  cout<<"WIDTH "<<w<<" EXACT "<<prev<<" EXCLUDED\n";
 }
 cout<<"PASS T(64..95)\n";
}
