// Exact-span modular exclusion for 33 double-hit rows with row-difference gcd >= 2.
// A minimal-width witness of width W must contain both endpoint rows; thus g divides W-1.
// This run verifies W=595..616, with the mathematical reduction valid for W<=768.
// Build twice: normal and -DDIRECT_RESIDUES. Exact integer arithmetic only.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <unordered_set>
#include <vector>
using namespace std;
int W=561, K=33;
struct Bits {
  array<uint64_t,6> a{}; // g>=2 and W<=768 implies <=384 compressed rows
  void set(int i) { a[i/64] |= uint64_t(1)<<(i%64); }
  bool test(int i) const { return (a[i/64]>>(i%64))&1; }
  int count() const { int s=0; for(auto v:a) s+=popcount(v); return s; }
  bool operator==(Bits const& b) const { return a==b.a; }
  Bits operator&(Bits const& b) const {
    Bits c; for(int i=0;i<6;i++) c.a[i]=a[i]&b.a[i]; return c;
  }
};
struct Hash {
  size_t operator()(Bits const& b) const {
    return (b.a[0]*0x9e3779b97f4a7c15ULL)^
           (b.a[1]*0xc2b2ae3d27d4eb4fULL)^
           (b.a[2]*0x165667b19e3779f9ULL)^
           (b.a[3]*0x94d049bb133111ebULL)^
           (b.a[4]*0x2545f4914f6cdd1dULL)^
           (b.a[5]*0x9ddfea08eb382d69ULL);
  }
};
vector<Bits> allowed(int p,int g,int h) {
  vector<unsigned char> qr(p);
  for(int z=0;z<p;z++) qr[(z*z)%p]=1;
  unordered_set<Bits,Hash> unique;
#ifdef DIRECT_RESIDUES
  for(int c=0;c<p;c++) for(int n=0;n<p;n++) {
    Bits b;
    for(int i=0;i<h;i++) {
      int a=int((2LL*g*i+c)%p);
      if(qr[(n-a*a%p+p)%p]) b.set(i);
    }
    if(b.test(0) && b.test(h-1) && b.count()>=K) unique.insert(b);
  }
#else
  for(int c=0;c<p;c++) {
    vector<Bits> by_n(p);
    for(int i=0;i<h;i++) {
      int a=int((2LL*g*i+c)%p), sq=a*a%p;
      for(int n=0;n<p;n++)
        if(qr[(n-sq+p)%p]) by_n[n].set(i);
    }
    for(auto const& b:by_n)
      if(b.test(0) && b.test(h-1) && b.count()>=K) unique.insert(b);
  }
#endif
  return {unique.begin(),unique.end()};
}
int main(int argc, char** argv) {
  if(argc != 3) { cerr << "usage: verify_nonprimitive_rows WIDTH K\n"; return 2; }
  W=atoi(argv[1]); K=atoi(argv[2]);
  if(W<2 || K<2 || W>768) {
    cerr << "out of audited range\n"; return 2;
  }
  const vector<int> moduli={9,11,7,49,19,31,23,43,47,37,41,53,59};
  int cases=0;
  for(int g=2;g<=(W-1)/(K-1);g++) {
    if ((W-1)%g) continue;
    int h=(W-1)/g+1;
    Bits full; for(int i=0;i<h;i++) full.set(i);
    vector<Bits> states{full};
    for(int p:moduli) {
      if(gcd(g,p)!=1) continue;
      auto masks=allowed(p,g,h);
      unordered_set<Bits,Hash> next;
      for(auto const& a:states) for(auto const& b:masks) {
        Bits c=a&b;
        if(c.count()>=K && c.test(0) && c.test(h-1)) next.insert(c);
      }
      states.assign(next.begin(),next.end());
      int max_size=0;
      for(auto const& s:states) max_size=max(max_size,s.count());
      cout << "CASE "<<g<<' '<<p<<' '<<states.size()<<' '<<max_size<<'\n';
      ++cases;
      if(states.empty()) break;
    }
    if(!states.empty()) {
      cerr << "INCONCLUSIVE gcd="<<g<<'\n';
      return 1;
    }
  }
  cout << "PASS W="<<W<<" K="<<K<<" gcd>=2 cases="<<cases<<'\n';
}
