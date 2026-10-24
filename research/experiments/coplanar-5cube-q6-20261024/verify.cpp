// Primary exhaustive verifier: exact integer Bareiss determinant + bottom-up mex.
// Build: g++ -O3 -std=c++17 verify.cpp -o verify
#include <algorithm>
#include <array>
#include <cstdlib>
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;
using Mask=uint64_t;
static constexpr int N=32;
static unordered_set<Mask> forbidden;
static vector<Mask> layer[9];
static unordered_map<Mask,uint16_t> gh;
static uint64_t terminals[9]={}, edges[9]={}, histogram[9][4][4]={};

static long long determinant(const array<int,6>& p){
 long long a[5][5];
 for(int i=0;i<5;i++)for(int j=0;j<5;j++)
  a[i][j]=((p[i+1]>>j)&1)-((p[0]>>j)&1);
 long long prev=1,sign=1;
 for(int k=0;k<4;k++){
  int pivot=k;while(pivot<5 && a[pivot][k]==0)pivot++;
  if(pivot==5)return 0;
  if(pivot!=k){for(int j=k;j<5;j++)swap(a[pivot][j],a[k][j]);sign=-sign;}
  long long q=a[k][k];
  for(int i=k+1;i<5;i++)for(int j=k+1;j<5;j++){
   long long v=a[i][j]*q-a[i][k]*a[k][j];
   if(v%prev){cerr<<"nonintegral Bareiss quotient\n";abort();}
   a[i][j]=v/prev;
  }
  for(int i=k+1;i<5;i++)a[i][k]=0;
  prev=q;
 }
 return sign*a[4][4];
}
static void build_forbidden(){
 array<int,6> p;
 for(p[0]=0;p[0]<27;p[0]++)for(p[1]=p[0]+1;p[1]<28;p[1]++)
 for(p[2]=p[1]+1;p[2]<29;p[2]++)for(p[3]=p[2]+1;p[3]<30;p[3]++)
 for(p[4]=p[3]+1;p[4]<31;p[4]++)for(p[5]=p[4]+1;p[5]<32;p[5]++){
  if(determinant(p)==0){Mask s=0;for(int x:p)s|=Mask(1)<<x;forbidden.insert(s);}
 }
}
static bool legal(Mask s,int x){
 if(__builtin_popcountll(s)<5)return true;
 Mask b=Mask(1)<<x;
 for(Mask sub=s;sub;sub=(sub-1)&s)
  if(__builtin_popcountll(sub)==5 && forbidden.count(sub|b))return false;
 return true;
}
static void build_layers(){
 layer[0].push_back(0);
 for(int k=0;k<7;k++){
  for(Mask s:layer[k]){
   int last=s?(63-__builtin_clzll(s)):-1;
   for(int x=last+1;x<N;x++)if(legal(s,x))layer[k+1].push_back(s|(Mask(1)<<x));
  }
 }
 // Verify that no safe eight-point set exists, not merely that the
 // seven-point layer has been enumerated.
 for(Mask s:layer[7])for(int x=0;x<N;x++)if(!(s&(Mask(1)<<x)) && legal(s,x)){
  cerr<<"unexpected eight-point safe set\n";abort();
 }
}
static void compute_grundy(){
 gh.reserve(1200000);
 for(int k=7;k>=0;k--){
  for(Mask s:layer[k]){
   unsigned gm=0,hm=0;int n=0;
   for(int x=0;x<N;x++)if(!(s&(Mask(1)<<x)) && legal(s,x)){
    auto it=gh.find(s|(Mask(1)<<x));
    if(it==gh.end()){cerr<<"missing child\n";abort();}
    int g=it->second&255,h=it->second>>8;
    gm|=1u<<g;hm|=1u<<h;n++;
   }
   int g=0,h=0;
   while(gm&(1u<<g))g++;
   if(n==0)h=1;else while(hm&(1u<<h))h++;
   if(g>=4||h>=4){cerr<<"unexpected mex\n";abort();}
   gh[s]=(h<<8)|g;
   terminals[k]+=(n==0);edges[k]+=n;histogram[k][g][h]++;
  }
 }
}
int main(){
 build_forbidden();build_layers();compute_grundy();
 cout<<"forbidden6 "<<forbidden.size()<<"\n";
 cout<<"root "<<(gh.at(0)&255)<<" "<<(gh.at(0)>>8)<<"\n";
 uint64_t total=0;
 for(int k=0;k<=7;k++){
  total+=layer[k].size();
  cout<<"layer "<<k<<" "<<layer[k].size()<<" terminal "<<terminals[k]<<" edges "<<edges[k]<<" gh";
  for(int g=0;g<4;g++)for(int h=0;h<4;h++)if(histogram[k][g][h])
   cout<<" ("<<g<<","<<h<<")="<<histogram[k][g][h];
  cout<<"\n";
 }
 cout<<"total "<<total<<"\n";
 for(int x=0;x<N;x++)if(gh.at(Mask(1)<<x)!=((1<<8)|0)){
  cerr<<"nonuniform opening "<<x<<"\n";return 1;
 }
 return 0;
}