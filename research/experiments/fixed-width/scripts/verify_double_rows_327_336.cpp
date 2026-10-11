// Certificate checker for conditional exact T(w)=32 on 327..336.
// The mathematical reduction is documented in the accompanying report.
// DIRECT_RESIDUES is a separately structured mask construction.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <cmath>
#include <unordered_set>
#include <vector>
using namespace std;
struct Bits {
 array<uint64_t,6> a{};
 bool operator==(Bits const& o) const {return a==o.a;}
 void set(int k){a[k/64]|=uint64_t(1)<<(k%64);}
 bool test(int k)const{return (a[k/64]>>(k%64))&1;}
 int count()const{return popcount(a[0])+popcount(a[1])+popcount(a[2])+popcount(a[3])+popcount(a[4])+popcount(a[5]);}
 Bits operator&(Bits const& o)const{return {{a[0]&o.a[0],a[1]&o.a[1],a[2]&o.a[2],a[3]&o.a[3],a[4]&o.a[4],a[5]&o.a[5]}};}
};
struct Hash{size_t operator()(Bits const& b)const{return (b.a[0]*0x9e3779b97f4a7c15ull)^(b.a[1]*0xc2b2ae3d27d4eb4full)^(b.a[2]*0x165667b19e3779f9ull)^(b.a[3]*0x94d049bb133111ebull)^(b.a[4]*0xd6e8feb86659fd93ull)^(b.a[5]*0x369dea0f31a53f85ull);}};
#ifdef DIRECT_RESIDUES
vector<Bits> masks(int p,int g,int w,int k){
 vector<unsigned char> qr(p,0);
 for(int z=0;z<p;z++)qr[z*z%p]=1;
 unordered_set<Bits,Hash> unique;
 for(int c=0;c<p;c++)for(int n=0;n<p;n++){
  Bits mask;
  for(int row=0;row<w;row++){
   int a=(2LL*g*row+c)%p;
   if(qr[(n-a*a%p+p)%p])mask.set(row);
  }
  if(mask.test(0)&&mask.test(w-1)&&mask.count()>=k)unique.insert(mask);
 }
 return {unique.begin(),unique.end()};
}
#else
vector<Bits> masks(int p,int g,int w,int k){
 vector<bool> qr(p);
 for(int z=0;z<p;z++)qr[(z*z)%p]=true;
 unordered_set<Bits,Hash> unique;
 for(int c=0;c<p;c++){
  vector<Bits> byN(p);
  for(int row=0;row<w;row++){
   int a=(2LL*g*row+c)%p;
   int sq=a*a%p;
   for(int n=0;n<p;n++)if(qr[(n-sq+p)%p])byN[n].set(row);
  }
  for(auto const& b:byN)if(b.test(0)&&b.test(w-1)&&b.count()>=k)unique.insert(b);
 }
 return {unique.begin(),unique.end()};
}
#endif
int witness(int w,int c,int d){
 int count=0;
 for(int y=0;y<w;y++){
  int disc=1-4*(y*y+c*y+d);
  if(disc<=0)continue;
  int root=(int)sqrt((double)disc);
  while((root+1)*(root+1)<=disc)++root;
  while(root*root>disc)--root;
  if(root*root==disc && (root&1)){
   int x1=(-1-root)/2,x2=(-1+root)/2;
   if(x1==x2 || x1*x1+y*y+x1+c*y+d!=0 || x2*x2+y*y+x2+c*y+d!=0)abort();
   ++count;
  }
 }
 return count;
}
int main(int argc,char**argv){
 int start=argc>1?atoi(argv[1]):327;
 int end=argc>2?atoi(argv[2]):336;
 if(start<327 || end>336 || start>end){cerr<<"range must be within 327..336\n";return 2;}
 const vector<int> modsSmall={9,11,7,49,19,23,31,37,41,43,47,53};
 const vector<int> modsMid={9,11,7,19,23,49,31,37,41,43,47,53};
 const vector<int> modsLarge={9,11,7,49,19,23,31,43,47,37,41,53,59};
 int prev=max({witness(start-1,-47,0),witness(start-1,-105,-6),witness(start-1,-95,-506),witness(start-1,-235,-6)});
 for(int W=start;W<=end;W++){
  int lower=max({witness(W,-47,0),witness(W,-105,-6),witness(W,-95,-506),witness(W,-235,-6)});
  if(lower<prev || lower>prev+1){cerr<<"unexpected witness count "<<W<<" "<<lower<<" "<<prev<<"\n";return 2;}
  if(lower==prev+1){prev=lower;cout<<"STEP "<<W<<" "<<prev<<"\n";continue;}
  int K=prev+1;
  const auto& mods=(W<=95?modsSmall:W<=128?modsMid:modsLarge);
  for(int g=1;g<=(W-1)/(K-1);g++){
   if((W-1)%g)continue;
   int w=(W-1)/g+1;
   Bits full;for(int i=0;i<w;i++)full.set(i);
   vector<Bits> states{full};
   // W=334 needs p=31 before p=23 to keep the intermediate set small.
   vector<int> selected=mods; if(W>=334)selected={9,11,7,49,19,31,23,43,47,37,41,53,59};
   for(int p:selected){
    if(gcd(g,p)!=1)continue;
    auto opts=masks(p,g,w,K);
    unordered_set<Bits,Hash> nxt;
    for(auto const& a:states)for(auto const& b:opts){
      Bits c=a&b;
      if(c.count()>=K)nxt.insert(c);
    }
    states.assign(nxt.begin(),nxt.end());
    int maxCount=0;for(auto const& s:states)maxCount=max(maxCount,s.count());
    cout<<"CASE "<<W<<' '<<K<<' '<<g<<' '<<p<<' '<<states.size()<<' '<<maxCount<<'\n';
    if(states.empty())break;
   }
   if(!states.empty()){cerr<<"UNEXCLUDED "<<W<<" "<<g<<'\n';return 1;}
  }
  cout<<"EXACT "<<W<<' '<<prev<<'\n';
 }
 cout<<"PASS "<<start<<".."<<end<<"\n";
}
