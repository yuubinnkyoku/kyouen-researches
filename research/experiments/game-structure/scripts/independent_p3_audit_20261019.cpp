// Independent integer determinant + recursive game audit for the P3 witness.
// g++ -std=c++17 -O2 independent_p3_audit.cpp -o /tmp/p3_audit && /tmp/p3_audit
#include <algorithm>
#include <cassert>
#include <iostream>
#include <vector>
using namespace std;
struct P {long long x,y;};
using i128=__int128_t;
static i128 det4(const P& a,const P& b,const P& c,const P& d){
  auto row=[&](P p){return vector<i128>{(i128)p.x-a.x,(i128)p.y-a.y,
      (i128)p.x*p.x+(i128)p.y*p.y-(i128)a.x*a.x-(i128)a.y*a.y};};
  auto u=row(b),v=row(c),w=row(d);
  return u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])
         +u[2]*(v[0]*w[1]-v[1]*w[0]);
}
int main(){
  vector<P> p={{17,17},{34,68},{51,153},{34,51},{32,77},{17,51},{51,102}};
  vector<vector<int>> found;
  for(int a=0;a<7;a++)for(int b=a+1;b<7;b++)for(int c=b+1;c<7;c++)for(int d=c+1;d<7;d++)
    if(det4(p[a],p[b],p[c],p[d])==0)found.push_back({a,b,c,d});
  vector<vector<int>> expected={{0,1,3,4},{1,2,5,6}};
  assert(found==expected);
  vector<int> memo(1<<7,-1); int calls=0;
  auto grundy=[&](auto&& self,int mask)->int{
    int &r=memo[mask];if(r>=0)return r;
    calls++;bool seen[8]={};
    for(int v=0;v<3;v++)if(!(mask&(1<<v))){
      int child=mask|(1<<v);bool ok=true;
      for(auto q:found){int e=0;for(int x:q)e|=1<<x;if((child&e)==e)ok=false;}
      if(ok)seen[self(self,child)]=true;
    }
    r=0;while(seen[r])r++;return r;
  };
  int result=grundy(grundy, (1<<3)|(1<<4)|(1<<5)|(1<<6));
  assert(result==2);
  cout<<"P3: points=7 forbidden_quads="<<found.size()<<" grundy="<<result<<" states="<<calls<<"\n";
}
