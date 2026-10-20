// Independent integer-only symbolic concurrency audit for q=6 on 3 lines.
// Compile: c++ -std=c++17 -O2 audit_independent.cpp -o audit && ./audit
#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <map>
#include <numeric>
#include <vector>
using namespace std;
using I = long long;
struct Circle { I s,delta,p; };
using Row = array<I,3>;
Row canonical(Row a){
 I g=gcd(gcd(abs(a[0]),abs(a[1])),abs(a[2]));
 if(!g)return {0,0,0};
 for(auto &x:a)x/=g;
 for(I x:a)if(x){if(x<0)for(auto &v:a)v=-v;break;}
 return a;
}
int main(){
 vector<array<int,2>> pairs;
 for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)pairs.push_back({i,j});
 vector<Circle> cs;
 for(auto b:pairs)for(auto c:pairs){
  if(b[0]+b[1]!=c[0]+c[1])continue;
  cs.push_back({b[0]+b[1],c[0]*c[1]-b[0]*b[1],b[0]*b[1]});
 }
 sort(cs.begin(),cs.end(),[](Circle x,Circle y){
  return tie(x.s,x.delta,x.p)<tie(y.s,y.delta,y.p);
 });
 assert(cs.size()==16);
 map<string,int> cnt;
 for(int i=0;i<16;i++)for(int j=i+1;j<16;j++)
 for(int k=j+1;k<16;k++)for(int l=k+1;l<16;l++){
  array<int,4> ids{i,j,k,l};
  Circle base=cs[i];
  array<Row,3> rows;
  for(int n=0;n<3;n++){
   Circle z=cs[ids[n+1]];
   rows[n]={base.s-z.s,z.delta-base.delta,z.p-base.p};
  }
  vector<Row> unique;
  for(Row r:rows){Row z=canonical(r);if(z!=Row{0,0,0} &&
      find(unique.begin(),unique.end(),z)==unique.end())unique.push_back(z);}
  assert(!unique.empty());
  if(unique.size()==1){
   Row r=unique[0];assert(r[0]==1 && r[1]==0 && r[2]<=0 && r[2]>=-4);
   I a=-r[2];
   for(int id:ids){auto z=cs[id];assert(z.delta==0 && z.p==a*(z.s-a));}
   cnt["rank_one_only_u_zero_or_one"]++;continue;
  }
  bool found=false;
  for(int m=0;m<3&&!found;m++)for(int n=m+1;n<3&&!found;n++){
   auto [A,B,C]=rows[m];auto [D,E,F]=rows[n];
   I det=A*E-B*D;
   if(!det)continue;
   found=true;
   I anum=-C*E+B*F, unum=-A*F+C*D;
   bool consistent=true;
   for(auto [X,Y,Z]:rows)if(X*anum+Y*unum+Z*det!=0)consistent=false;
   if(!consistent){cnt["inconsistent"]++;continue;}
   if(unum==0||unum==det){cnt["rank_two_u_zero_or_one"]++;continue;}
   I V=anum*anum-base.s*anum*det+base.delta*unum*det+base.p*det*det;
   I den=unum*(unum-det);
   assert(-V*den<=0);
   cnt[V==0?"rank_two_d_squared_zero":"rank_two_d_squared_negative"]++;
  }
  if(!found)cnt["inconsistent_parallel"]++;
 }
 const map<string,int> expected={
  {"inconsistent",1318},{"inconsistent_parallel",210},
  {"rank_one_only_u_zero_or_one",5},
  {"rank_two_d_squared_negative",37},
  {"rank_two_d_squared_zero",24},
  {"rank_two_u_zero_or_one",226}
 };
 assert(cnt==expected);
 int total=0;
 for(auto [name,count]:cnt){cout<<name<<" "<<count<<"\n";total+=count;}
 assert(total==1820);
 cout<<"all 1820 four-circle subsets excluded: PASS\n";
}
