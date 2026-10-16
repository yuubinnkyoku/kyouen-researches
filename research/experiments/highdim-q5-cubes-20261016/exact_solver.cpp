#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
struct Point { int x,y,z; };
using U = uint32_t;

long long det5(array<array<long long,5>,5> a) {
 long long sign=1,prev=1;
 for(int i=0;i<4;i++){
  int pivot=i; while(pivot<5 && a[pivot][i]==0)++pivot;
  if(pivot==5)return 0;
  if(pivot!=i){swap(a[i],a[pivot]);sign=-sign;}
  long long pv=a[i][i];
  for(int j=i+1;j<5;j++)for(int k=i+1;k<5;k++){
   __int128 v=(__int128)a[j][k]*pv-(__int128)a[j][i]*a[i][k];
   assert(v%prev==0);
   a[j][k]=(long long)(v/prev);
  }
  for(int j=i+1;j<5;j++)a[j][i]=0;
  prev=pv;
 }
 return sign*a[4][4];
}

int main(int argc,char**argv){
 if(argc!=4){cerr<<"usage: exact_solver nx ny nz\n";return 1;}
 int X=stoi(argv[1]),Y=stoi(argv[2]),Z=stoi(argv[3]);
 if(X<1 || Y<1 || Z<1 || (long long)X*Y*Z>27){cerr<<"invalid size\n";return 2;}
 vector<Point> p;
 for(int z=0;z<Z;z++)for(int y=0;y<Y;y++)for(int x=0;x<X;x++)p.push_back({x,y,z});
 int n=p.size();
 vector<U> edges;
 unordered_map<U,U> completion;
 for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)
 for(int c=b+1;c<n;c++)for(int d=c+1;d<n;d++)
 for(int e=d+1;e<n;e++){
  array<int,5> ids{a,b,c,d,e};
  array<array<long long,5>,5> mat;
  for(int j=0;j<5;j++){
   Point v=p[ids[j]];
   mat[j]={(long long)v.x*v.x+v.y*v.y+v.z*v.z,v.x,v.y,v.z,1};
  }
  if(det5(mat)==0){
   U mask=0;for(int i:ids)mask|=U(1)<<i;
   edges.push_back(mask);
   for(int i:ids)completion[mask^(U(1)<<i)]|=U(1)<<i;
  }
 }
 auto legal=[&](U mask){
  U blocked=0,bits=mask;
  int ids[27],k=0;
  while(bits){int j=__builtin_ctz(bits);bits&=bits-1;ids[k++]=j;}
  for(int i=0;i<k;i++)for(int j=i+1;j<k;j++)
  for(int a=j+1;a<k;a++)for(int b=a+1;b<k;b++){
   U sub=(U(1)<<ids[i])|(U(1)<<ids[j])|(U(1)<<ids[a])|(U(1)<<ids[b]);
   auto it=completion.find(sub);
   if(it!=completion.end())blocked|=it->second;
  }
  return (~(mask|blocked))&((U(1)<<n)-1);
 };
 vector<U> states;states.reserve(400000);
 auto enumerate=[&](auto&& self,U mask,int next)->void{
  states.push_back(mask);
  U moves=legal(mask);
  for(int j=next;j<n;j++)if((moves>>j)&1)self(self,mask|(U(1)<<j),j+1);
 };
 enumerate(enumerate,0,0);
 sort(states.begin(),states.end(),[](U a,U b){
  int ka=__builtin_popcount(a),kb=__builtin_popcount(b);
  return ka>kb||(ka==kb&&a<b);
 });
 unordered_map<U,uint8_t> g;g.reserve(states.size()*2);
 map<int,array<int,8>> hist;
 int terminal=0;
 for(U mask:states){
  U moves=legal(mask), options=0;
  if(!moves)++terminal;
  while(moves){
   int j=__builtin_ctz(moves);moves&=moves-1;
   auto it=g.find(mask|(U(1)<<j));
   assert(it!=g.end());
   options|=U(1)<<it->second;
  }
  int value=0;while((options>>value)&1)++value;
  assert(value<8);
  g.emplace(mask,value);
  ++hist[__builtin_popcount(mask)][value];
 }
 int two_loss=0,total_pairs=0;
 for(U mask:states)if(__builtin_popcount(mask)==2){
  ++total_pairs;two_loss+=g[mask]==0;
 }
 cout<<"shape="<<X<<"x"<<Y<<"x"<<Z
     <<" forbidden="<<edges.size()<<" safe="<<states.size()
     <<" terminals="<<terminal<<" root_g="<<int(g[0])
     <<" two_stone_g0="<<two_loss<<"/"<<total_pairs<<"\n";
 for(auto& kv:hist){
  cout<<kv.first;
  for(int v:kv.second)cout<<" "<<v;
  cout<<"\n";
 }
}
