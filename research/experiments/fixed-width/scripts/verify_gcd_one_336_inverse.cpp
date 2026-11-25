// Independent 336-row congruence certificate, inverse row-to-n construction.
// Uses std::bitset<192> rather than the three-word direct (c,n)-enumeration.
#include <bitset>
#include <array>
#include <vector>
#include <unordered_set>
#include <iostream>
#include <numeric>
#include <stdexcept>
using namespace std;
using Bits=bitset<192>;
struct Hash {
 size_t operator()(const Bits& b)const{
  const Bits low((1ULL<<63)-1ULL); // chunks of 63 bits
  auto a=(b&low).to_ullong();auto c=((b>>63)&low).to_ullong();auto d=((b>>126)&low).to_ullong();
  size_t h=a*0x9e3779b97f4a7c15ULL;h^=c+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);h^=d+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);return h;
 }
};
using Set=unordered_set<Bits,Hash>;
Set allowed(int w,int p){
 vector<int> squares;vector<bool> is_square(p);
 for(int a=0;a<p;a++){int v=a*a%p;if(!is_square[v]){is_square[v]=true;squares.push_back(v);}}
 Set all;
 for(int c=0;c<p;c++){
  vector<Bits> by_n(p);
  for(int y=0;y<w;y++){
   int a=(2*y+c)%p,z=a*a%p;
   for(int s:squares)by_n[(z+s)%p].set(y);
  }
  for(const auto &v:by_n)if(v.count()>=25)all.insert(v);
 }
 return all;
}
void check(int g,vector<int> mods){
 int w=(336+g-1)/g;
 Bits full;for(int y=0;y<w;y++)full.set(y);
 Set states{full};
 cout<<"g="<<g<<" width="<<w<<'\n';
 for(int p:mods){
  if(gcd(g,p)!=1)throw runtime_error("noncoprime modulus");
  Set loc=allowed(w,p),next;
  for(const auto &a:states)for(const auto &b:loc){auto c=a&b;if(c.count()>=25)next.insert(c);}
  states.swap(next);
  cout<<"  mod="<<p<<" local="<<loc.size()<<" survivors="<<states.size()<<'\n';
  if(states.empty())break;
 }
 if(!states.empty())throw runtime_error("not excluded: g="+to_string(g));
}
int main(){
 check(2,{9,7,49,11,19,23,31,37,41,43,47,53,59});
 check(3,{11,19,23,31,37,41,43});
 check(4,{11,19,23,31});
 check(5,{11,19,23});
 check(6,{19,23,31});
 check(7,{19,23});
 check(8,{19,23});
 for(int g=9;g<=13;g++)check(g,{19});
 cout<<"PASS: 336 consecutive rows with >=25 double-hit rows force gcd=1\n";
}
