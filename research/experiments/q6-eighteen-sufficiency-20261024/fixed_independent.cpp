// Independent integer-only audit. Compile without NDEBUG.
#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <map>
#include <string>
#include <tuple>
#include <vector>
using namespace std;
using I=long long;
using Wide=__int128_t;
using Points=array<int,5>;
struct Circle { I s,delta,p; };
using Row=array<I,3>;
map<int,int> sums(Points a){
 map<int,int> r;for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)r[a[i]+a[j]]++;return r;
}
int main(){
 Points ap{0,2,4,6,8};auto target=sums(ap);vector<Points> near;int tested=0;
 for(int a=-5;a<=9;a++)for(int b=a+1;b<=10;b++)for(int c=b+1;c<=11;c++)
 for(int d=c+1;d<=12;d++)for(int e=d+1;e<=13;e++){
  Points p{a,b,c,d,e};auto r=sums(p);int h=0,energy=0;tested++;
  for(auto [s,n]:r){h+=n*n;energy+=n*target[s];}
  if(h==14&&energy==14)near.push_back(p);
 }
 assert(tested==11628);
 assert((near==vector<Points>{{-2,2,4,6,8},{0,2,4,6,10}}));
 vector<pair<string,Points>> cases{{"equal-ap-regression",ap},{"half-step-ap",{1,3,5,7,9}},
  {"near-ap-left",near[0]},{"near-ap-right",near[1]}};
 int grand=0;cout<<"near-ap "<<tested<<" "<<near.size()<<"\n";
 for(auto [name,c]:cases){
  vector<Circle> cs;
  for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)
  for(int k=0;k<5;k++)for(int l=k+1;l<5;l++)
   if(ap[i]+ap[j]==c[k]+c[l])cs.push_back({ap[i]+ap[j],c[k]*c[l]-ap[i]*ap[j],ap[i]*ap[j]});
  sort(cs.begin(),cs.end(),[](auto a,auto b){return tie(a.s,a.delta,a.p)<tie(b.s,b.delta,b.p);});
  int n=cs.size();assert(n==(name=="equal-ap-regression"?16:14));
  map<string,int> count;
  for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++)for(int l=k+1;l<n;l++){
   array<int,3> ids{j,k,l};auto base=cs[i];array<Row,3> rows;
   for(int q=0;q<3;q++){auto z=cs[ids[q]];rows[q]={base.s-z.s,z.delta-base.delta,z.p-base.p};}
   bool rank2=false;
   for(int q=0;q<3&&!rank2;q++)for(int v=q+1;v<3&&!rank2;v++){
    auto [A,B,C]=rows[q];auto [D,E,F]=rows[v];I det=A*E-B*D;if(!det)continue;rank2=true;
    I yn=-C*E+B*F,un=-A*F+C*D;bool consistent=true;
    for(auto [X,Y,Z]:rows)if(X*yn+Y*un+Z*det)consistent=false;
    if(!consistent){count["inconsistent"]++;continue;}
    if(un==0||un==det){count["rank-two-boundary"]++;continue;}
    Wide residual=Wide(yn)*yn-Wide(base.s)*yn*det+Wide(base.delta)*un*det+Wide(base.p)*det*det;
    Wide denominator=Wide(un)*(un-det);
    assert(-residual*denominator<=0);
    count[residual==0?"rank-two-zero":"rank-two-negative"]++;
   }
   if(rank2)continue;
   Row pivot{0,0,0};for(auto r:rows)if(r[0]||r[1]){pivot=r;break;}
   auto [A,B,C]=pivot;assert(A||B);bool consistent=true;
   for(auto [X,Y,Z]:rows)if(A*Z!=C*X||B*Z!=C*Y)consistent=false;
   if(!consistent){count["inconsistent-parallel"]++;continue;}
   if(A){
    assert(C*C+base.s*C*A+base.p*A*A==0);
    assert((B+C)*(B+C)+base.s*(B+C)*A+(base.delta+base.p)*A*A==0);
    count["rank-one-nonpositive"]++;
   }else{
    if(C==0||C==-B){count["rank-one-boundary"]++;continue;}
    if(B<0){B=-B;C=-C;}
    assert(-C<0||-C>B);
    assert(4*(-base.delta*C+base.p*B)-base.s*base.s*B>=0);
    count["rank-one-nonpositive"]++;
   }
  }
  int total=0;for(auto [key,value]:count){cout<<name<<" "<<key<<" "<<value<<"\n";total+=value;}
  assert(total==n*(n-1)*(n-2)*(n-3)/24);grand+=total;
 }
 assert(grand==4823);cout<<"all "<<grand<<" four-circle subsets excluded: PASS\n";
}
