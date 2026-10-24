#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <unordered_map>
#include <vector>
using namespace std;
using U=uint64_t;
struct P {int x,y,z;};
int det3(array<int,3> a,array<int,3> b,array<int,3> c){
 return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0]);
}
bool coplanar(P a,P b,P c,P d){
 return det3({b.x-a.x,b.y-a.y,b.z-a.z},{c.x-a.x,c.y-a.y,c.z-a.z},{d.x-a.x,d.y-a.y,d.z-a.z})==0;
}
void run(int k,int m,const vector<long long>& want_safe,const vector<long long>& want_fail,int want_g,int want_h){
 int n=2*k*m; vector<P> p;
 for(int x=0;x<2;x++)for(int y=0;y<k;y++)for(int z=0;z<m;z++)p.push_back({x,y,z});
 vector<vector<U>> levels(7);levels[0].push_back(0);
 for(int t=0;t<6;t++)for(U s:levels[t]){
  int first=s?64-__builtin_clzll(s):0;
  for(int i=first;i<n;i++){
   bool ok=true;vector<int> ids;
   for(int j=0;j<n;j++)if(s>>j&1)ids.push_back(j);
   for(int a=0;a<(int)ids.size()&&ok;a++)for(int b=a+1;b<(int)ids.size()&&ok;b++)for(int c=b+1;c<(int)ids.size();c++)
    if(coplanar(p[ids[a]],p[ids[b]],p[ids[c]],p[i])){ok=false;break;}
   if(ok)levels[t+1].push_back(s|(U(1)<<i));
  }
 }
 vector<long long> fail(7),terminal(7);vector<U> witnesses(7);vector<int> wg(7),wh(7);
 unordered_map<U,unsigned char> next,now;
 for(int t=6;t>=0;t--){
  now.clear();now.reserve(levels[t].size()*2+1);
  for(U s:levels[t]){
   unsigned usedg=0,usedh=0;bool has=false;
   for(int i=0;i<n;i++)if(!(s>>i&1)){
    auto it=next.find(s|(U(1)<<i));
    if(it==next.end())continue;
    has=true;usedg|=1u<<(it->second&15);usedh|=1u<<(it->second>>4);
   }
   int g=0,h=has?0:1;
   while(usedg>>g&1)g++;
   while(usedh>>h&1)h++;
   now.emplace(s,(unsigned char)(g|(h<<4)));
   if(!has)terminal[t]++;
   if(h!=(g<2?1-g:g)){
    fail[t]++;if(fail[t]==1){witnesses[t]=s;wg[t]=g;wh[t]=h;}
   }
  }
  next.swap(now);
 }
 cout<<k<<"x"<<m<<" safe";
 for(int t=0;t<=6;t++)cout<<" "<<levels[t].size();
 cout<<" terminal";for(int t=0;t<=6;t++)cout<<" "<<terminal[t];
 cout<<" failures";for(int t=0;t<=6;t++)cout<<" "<<fail[t];
 auto root=next.at(0);cout<<" root="<<int(root&15)<<","<<int(root>>4)<<"\n";
 for(int t=0;t<=6;t++)if((long long)levels[t].size()!=want_safe[t] || fail[t]!=want_fail[t])throw runtime_error("census mismatch");
 if((root&15)!=want_g || (root>>4)!=want_h)throw runtime_error("root mismatch");
 for(int t=0;t<=6;t++)if(fail[t]){
  cout<<" witness t="<<t<<" g="<<wg[t]<<" h="<<wh[t]<<" points=";
  for(int i=0;i<n;i++)if(witnesses[t]>>i&1)cout<<"("<<p[i].x<<","<<p[i].y<<","<<p[i].z<<")";
  cout<<"\n";
 }
}
int main(){
 run(1,1,{1,2,1,0,0,0,0},{0,0,0,0,0,0,0},0,1);
 run(1,2,{1,4,6,4,0,0,0},{0,0,0,0,0,0,0},1,0);
 run(1,3,{1,6,15,20,0,0,0},{0,0,0,0,0,0,0},1,0);
 run(1,4,{1,8,28,56,0,0,0},{0,0,0,0,0,0,0},1,0);
 run(2,2,{1,8,28,56,58,8,0},{1,8,16,0,0,0,0},0,0);
 run(2,3,{1,12,66,220,386,172,0},{0,0,0,0,0,0,0},1,0);
 run(2,4,{1,16,120,560,1364,1008,0},{0,0,0,0,0,0,0},1,0);
 run(3,3,{1,18,153,816,2436,2664,368},{0,10,25,16,0,0,0},1,0);
 run(3,4,{1,24,276,2024,8500,15056,5648},{0,0,8,12,0,0,0},0,1);
 run(3,5,{1,30,435,4060,21840,52680,31800},{0,0,0,0,0,0,0},0,1);
 run(3,6,{1,36,630,7140,46854,143652,123200},{0,0,0,0,0,0,0},0,1);
 run(4,4,{1,32,496,4960,29172,80736,64696},{0,0,0,0,0,0,0},0,1);
 run(4,5,{1,40,780,9880,74496,278760,343080},{0,0,0,0,0,0,0},0,1);
}
