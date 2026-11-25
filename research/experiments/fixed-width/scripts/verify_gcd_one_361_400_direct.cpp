// Sequential endpoint sieve for gcd-one theorem, widths 362..384.
// Depends on established 360-row theorem and 361-row endpoint verification.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <unordered_set>
#include <vector>
using namespace std;
struct Mask {
 array<uint64_t,4> a{};
 bool operator==(const Mask& x) const {return a==x.a;}
 int count()const{return __builtin_popcountll(a[0])+__builtin_popcountll(a[1])+__builtin_popcountll(a[2])+__builtin_popcountll(a[3]);}
 void set(int i){a[i/64]|=1ULL<<(i%64);}
 bool get(int i)const{return a[i/64]>>(i%64)&1;}
 Mask operator&(const Mask& x)const{return {{a[0]&x.a[0],a[1]&x.a[1],a[2]&x.a[2],a[3]&x.a[3]}};}
};
struct Hash{size_t operator()(const Mask&m)const{size_t h=0x9e3779b97f4a7c15ULL;for(auto x:m.a)h^=x+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);return h;}};
using Set=unordered_set<Mask,Hash>;
Set local(int width,int modulus){
 vector<char> sq(modulus);
 for(int x=0;x<modulus;x++)sq[x*x%modulus]=1;
 Set out;
 for(int c=0;c<modulus;c++)for(int n=0;n<modulus;n++){
  Mask mask;
  for(int k=0;k<width;k++){
   int t=(2*k+c)%modulus;
   if(sq[(n-t*t%modulus+modulus)%modulus])mask.set(k);
  }
  if(mask.count()>=25&&mask.get(0)&&mask.get(width-1))out.insert(mask);
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
 if(width>256)throw runtime_error("width too large");
 Mask full;for(int k=0;k<width;k++)full.set(k);
 Set states;states.insert(full);
 for(int mod:mods(g)){
  if(gcd(g,mod)!=1)continue;
  Set loc=local(width,mod),next;
  for(const Mask&a:states)for(const Mask&b:loc){Mask v=a&b;if(v.count()>=25)next.insert(v);}
  states.swap(next);
  cout<<"w="<<w<<" g="<<g<<" mod="<<mod<<" local="<<loc.size()<<" states="<<states.size()<<'\n';
  if(states.empty())return;
 }
 throw runtime_error("survivor w="+to_string(w)+" g="+to_string(g));
}
int main(){
 for(int w=361;w<=400;w++){
  for(int g=2;g<=((w-1)/24);g++)if((w-1)%g==0)check(w,g);
  cout<<"PASS w="<<w<<'\n';
 }
}
