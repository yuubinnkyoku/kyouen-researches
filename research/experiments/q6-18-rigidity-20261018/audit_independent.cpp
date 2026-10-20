#include <array>
#include <iostream>
#include <map>
#include <vector>
#include <cassert>
using namespace std;
struct Item{array<int,5>a;map<int,int>p;int h=0;};
int main(){
 vector<Item>v;
 for(int a=0;a<10;a++)for(int b=a+1;b<10;b++)for(int c=b+1;c<10;c++)for(int d=c+1;d<10;d++)for(int e=d+1;e<10;e++){
  Item x; x.a={a,b,c,d,e};
  for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)x.p[x.a[i]+x.a[j]]++;
  for(auto kv:x.p)x.h+=kv.second*kv.second;
  v.push_back(x);
 }
 map<pair<int,int>,int>classes;int n15=0;
 for(auto &x:v)for(auto &y:v){
  int z=0;for(auto [s,n]:x.p){auto it=y.p.find(s);if(it!=y.p.end())z+=n*it->second;}
  assert(z<=16);
  if(z==15)n15++;
  if(z!=14)continue;
  classes[{x.h,y.h}]++;
  if(x.h==14&&y.h==14)assert(x.a==y.a);
  else if(x.h==16&&y.h==16){
   int dx=x.a[1]-x.a[0],dy=y.a[1]-y.a[0];
   assert(dx==dy&&2*abs(x.a[0]-y.a[0])==dx);
  }else{
   assert((x.h==14&&y.h==16)||(x.h==16&&y.h==14));
   int diff=0;
   for(auto [s,n]:x.p){auto it=y.p.find(s);diff+=abs(n-(it==y.p.end()?0:it->second));}
   for(auto [s,n]:y.p)if(!x.p.count(s))diff+=n;
   assert(diff==2);
  }
 }
 assert(n15==0);
 cout<<"sets="<<v.size()<<" pairs="<<v.size()*v.size()<<" E15="<<n15<<"\n";
 for(auto [k,n]:classes)cout<<"E14 H="<<k.first<<","<<k.second<<" count="<<n<<"\n";
 cout<<"PASS\n";
}
