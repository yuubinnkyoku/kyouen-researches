// Standalone exhaustive exact-cover impossibility checker.
// Input is a positive/zero obligation incidence matrix produced by an
// independently checked exact-geometry/dual enumerator.
// All selected columns must cover each positive row exactly once, and each
// zero row at least once. The search is exhaustive; no optimizer is trusted.
#include <algorithm>
#include <bit>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <vector>
#include <chrono>
#include <unordered_set>
#include <string>
using namespace std;
using U=uint64_t;
using Bits=vector<U>;
struct Column {vector<int> pos,zero;Bits conflicts;};
int P,Z,C,W;
vector<Column> cols;
vector<Bits> byp,byz;
uint64_t calls=0,branches=0;
uint64_t budget=0;
unordered_set<string> memo;
static inline string state_key(const Bits&a,const Bits&b,const Bits&c){
 string s; s.reserve((a.size()+b.size()+c.size())*sizeof(U));
 s.append((const char*)a.data(),a.size()*sizeof(U));
 s.append((const char*)b.data(),b.size()*sizeof(U));
 s.append((const char*)c.data(),c.size()*sizeof(U));
 return s;
}
static inline void bitset_set(Bits& b,int i){b[i>>6]|=U(1)<<(i&63);}
static inline bool bitset_get(const Bits& b,int i){return (b[i>>6]>>(i&63))&1;}
static inline bool any(const Bits& b){for(U v:b)if(v)return true;return false;}
static inline int and_count(const Bits& a,const Bits& b,int best){int n=0;for(int i=0;i<W;i++){n+=popcount(a[i]&b[i]);if(n>=best)break;}return n;}
static inline Bits bits_intersect(const Bits& a,const Bits& b){Bits x(W);for(int i=0;i<W;i++)x[i]=a[i]&b[i];return x;}
static inline void unset(Bits& a,int i){a[i>>6]&=~(U(1)<<(i&63));}
static inline int choose(const Bits& b){for(int i=0;i<(int)b.size();i++)if(b[i])return i*64+countr_zero(b[i]);return -1;}
static inline bool emptyrows(const Bits& b){for(U x:b)if(x)return false;return true;}
bool search(Bits avail,Bits needp,Bits needz){
 ++calls;
 if(budget && calls>budget)throw runtime_error("search budget exhausted");
 if(emptyrows(needp) && emptyrows(needz))return true;
 string key=state_key(avail,needp,needz);
 if(memo.find(key)!=memo.end())return false;
 int best=INT32_MAX;int row=-1;bool iszero=false;
 for(int i=0;i<P;i++)if(bitset_get(needp,i)){
  int n=and_count(avail,byp[i],best);
  if(n==0){memo.insert(move(key));return false;}
  if(n<best){best=n;row=i;iszero=false;}
  if(best==1)break;
 }
 if(best!=1){
  for(int i=0;i<Z;i++)if(bitset_get(needz,i)){
   int n=and_count(avail,byz[i],best);
   if(n==0){memo.insert(move(key));return false;}
   if(n<best){best=n;row=i;iszero=true;}
   if(best==1)break;
  }
 }
 Bits options=bits_intersect(avail,iszero?byz[row]:byp[row]);
 while(any(options)){
  int c=choose(options);unset(options,c);++branches;
  Bits av=avail,p=needp,z=needz;
  for(int j=0;j<W;j++)av[j]&=~cols[c].conflicts[j];
  for(int i:cols[c].pos)unset(p,i);
  for(int i:cols[c].zero)unset(z,i);
  if(search(move(av),move(p),move(z)))return true;
 }
 memo.insert(move(key));return false;
}
int main(int argc,char**argv){
 try{
 if(!(cin>>P>>Z>>C)||P<=0||Z<0||C<=0||C>10000)throw runtime_error("invalid dimensions");
 if(argc>1)budget=stoull(argv[1]);
 W=(C+63)/64;
 cols.resize(C);byp.assign(P,Bits(W));byz.assign(Z,Bits(W));
 for(int c=0;c<C;c++){
  int a,b;if(!(cin>>a>>b)||a<0||b<0||a>P||b>Z)throw runtime_error("bad column");
  for(int j=0;j<a;j++){int i;cin>>i;if(i<0||i>=P)throw runtime_error("bad pos index");cols[c].pos.push_back(i);bitset_set(byp[i],c);}
  for(int j=0;j<b;j++){int i;cin>>i;if(i<0||i>=Z)throw runtime_error("bad zero index");cols[c].zero.push_back(i);bitset_set(byz[i],c);}
 }
 for(int c=0;c<C;c++){
  cols[c].conflicts.assign(W,0);
  for(int i:cols[c].pos)for(int j=0;j<W;j++)cols[c].conflicts[j]|=byp[i][j];
 }
 Bits avail(W,~U(0));avail.back()&=(C%64==0?~U(0):((U(1)<<(C%64))-1));
 Bits needp((P+63)/64,~U(0)),needz((Z+63)/64,~U(0));
 if(P%64)needp.back()&=(U(1)<<(P%64))-1;
 if(Z%64)needz.back()&=(U(1)<<(Z%64))-1;
 auto start=chrono::steady_clock::now();bool sat=search(avail,needp,needz);
 cerr<<"P="<<P<<" Z="<<Z<<" C="<<C<<" calls="<<calls<<" branches="<<branches<<" memo="<<memo.size()<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"\n";
 if(sat){cout<<"SAT (gap not proved)\n";return 2;}
 cout<<"UNSAT (exhaustive independent gap proof)\n";return 0;
 }catch(const exception&e){cerr<<"ERROR: "<<e.what()<<" calls="<<calls<<"\n";return 3;}
}
