// Exact modular necessary-condition verifier for a circle having >=25 double-hit rows.
// Fixed 256-bit masks, supports widths 129..256. Independent transposed residues.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <unordered_set>
#include <vector>
using namespace std;
struct M { array<uint64_t,4> a{}; bool operator==(const M&b)const{return a==b.a;} bool operator<(const M&b)const{return a<b.a;} int cnt()const{return __builtin_popcountll(a[0])+__builtin_popcountll(a[1])+__builtin_popcountll(a[2])+__builtin_popcountll(a[3]);} bool contains(const M&b)const {for(int i=0;i<4;i++)if((a[i]&b.a[i])!=b.a[i])return false;return true;} M operator&(const M&b)const {M c;for(int i=0;i<4;i++)c.a[i]=a[i]&b.a[i];return c;} void set(int y){a[y/64]|=1ull<<(y%64);} };
vector<M> maximal(vector<M> v){
 sort(v.begin(),v.end());v.erase(unique(v.begin(),v.end()),v.end());
 sort(v.begin(),v.end(),[](const M&a,const M&b){int ca=a.cnt(),cb=b.cnt();return ca!=cb?ca>cb:a<b;});
 vector<M> out;out.reserve(v.size());
 for(auto &a:v){bool dominated=false;int ca=a.cnt();for(auto &b:out){if(b.cnt()==ca)continue;if(b.contains(a)){dominated=true;break;}}if(!dominated)out.push_back(a);}
 return out;
}
vector<M> local(int len,int p,int K){
 vector<M> all;
 for(int c=0;c<p;c++){
  vector<char> square(p,0);for(int x=0;x<p;x++)square[x*x%p]=1;
  for(int n=0;n<p;n++){
   M m;for(int y=0;y<len;y++){int z=(2*y+c)%p;int delta=(n-z*z%p+p)%p;if(square[delta])m.set(y);}
   if(m.cnt()>=K && (m.a[0]&1) && ((m.a[(len-1)/64]>>((len-1)%64))&1))all.push_back(m);
  }
 }
 return maximal(move(all));
}
int main(int argc,char**argv){
 int start=129,end=147; if(argc>1)start=atoi(argv[1]);if(argc>2)end=atoi(argv[2]);
 const vector<int> original={9,11,7,19,23,49,31,37,41,43,47,53};
 const vector<int> alternative={9,11,23,7,19,49,31,37,41,43,47,53};
 for(int w=start;w<=end;w++){
  const auto& mods=(w==134?alternative:original);
  assert(w<=256);
  for(int g=1;g*24<=w-1;g++)if((w-1)%g==0){
   int len=(w-1)/g+1;
   M full;for(int y=0;y<len;y++)full.set(y);
   vector<M> states{full};bool excluded=false;
   for(int p:mods){if(gcd(g,p)!=1)continue;
    auto loc=local(len,p,25);vector<M> next;
    for(const M&a:states)for(const M&b:loc){M v=a&b;if(v.cnt()>=25)next.push_back(v);}
    states=maximal(move(next));
    cout<<"CASE "<<w<<" 25 "<<g<<" "<<p<<" "<<loc.size()<<" "<<states.size()<<"\n";
    if(states.empty()){excluded=true;break;}
   }
   if(!excluded){cerr<<"NOT EXCLUDED "<<w<<" "<<g<<"\n";return 2;}
  }
  cout<<"WIDTH "<<w<<" EXCLUDED_25\n";
 }
 cout<<"PASS\n";
}
