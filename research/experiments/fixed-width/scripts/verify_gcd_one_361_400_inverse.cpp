// Independent inverse-square-residue construction for sequential endpoint theorem.
#include <bitset>
#include <vector>
#include <unordered_set>
#include <iostream>
#include <numeric>
#include <stdexcept>
using namespace std;
using Bits=bitset<256>;
struct Hash{size_t operator()(const Bits&b)const{const Bits low((1ULL<<63)-1ULL);auto a=(b&low).to_ullong(),c=((b>>63)&low).to_ullong(),d=((b>>126)&low).to_ullong();size_t h=a*0x9e3779b97f4a7c15ULL;h^=c+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);h^=d+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);return h;}};
using Set=unordered_set<Bits,Hash>;
Set allowed(int width,int p){
 vector<int> squares;vector<bool> seen(p);
 for(int x=0;x<p;x++){int s=x*x%p;if(!seen[s]){seen[s]=true;squares.push_back(s);}}
 Set out;
 for(int c=0;c<p;c++){
  vector<Bits> by_n(p);
  for(int k=0;k<width;k++){
   int a=(2*k+c)%p,z=a*a%p;
   for(int s:squares)by_n[(z+s)%p].set(k);
  }
  for(const auto& v:by_n)if(v.count()>=25&&v.test(0)&&v.test(width-1))out.insert(v);
 }
 return out;
}
vector<int> mods(int g){
 if(g==2)return {9,7,49,11,19,23,31,37,41,43,47,53,59,61,67};
 if(g==3)return {11,19,23,31,37,41,43,47,53,59,61,67};
 if(g==4||g==5)return {11,19,23,31,37,41,43,47};
 return {19,23,31,37,41,43,47,53,59,61,67};
}
void check(int w,int g){
 int width=(w-1)/g+1;
 if(width>256)throw runtime_error("too large");
 Bits full;for(int k=0;k<width;k++)full.set(k);
 Set states{full};
 for(int p:mods(g)){
  if(gcd(g,p)!=1)continue;
  Set loc=allowed(width,p),next;
  for(const auto&a:states)for(const auto&b:loc){auto c=a&b;if(c.count()>=25)next.insert(c);}
  states.swap(next);
  cout<<"w="<<w<<" g="<<g<<" mod="<<p<<" local="<<loc.size()<<" states="<<states.size()<<'\n';
  if(states.empty())return;
 }
 throw runtime_error("not excluded");
}
int main(){
 for(int w=361;w<=400;w++){
  for(int g=2;g<=(w-1)/24;g++)if((w-1)%g==0)check(w,g);
  cout<<"PASS w="<<w<<'\n';
 }
}
