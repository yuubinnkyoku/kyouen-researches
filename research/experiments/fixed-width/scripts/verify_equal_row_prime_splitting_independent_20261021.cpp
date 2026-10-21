// Independent audit: enumerate polynomial coefficients A,L directly.
#include <cassert>
#include <iostream>
#include <tuple>
#include <vector>
using namespace std;
bool prime(int p) {if(p<2)return false;for(int d=2;d*d<=p;++d)if(p%d==0)return false;return true;}
int count(int p,int n,int d,bool root=false){
 vector<bool> qr(p,false);
 for(int x=0;x<p;++x)qr[1LL*x*x%p]=true;
 int ans=0;
 for(int A=0;A<p;++A)for(int L=0;L<p;++L){
  bool ok=true;int zeros=0;
  for(int j=0;j<n;++j){
   int v=(A+1LL*L*j-4LL*d*d*j*j)%p;if(v<0)v+=p;
   if(!qr[v]){ok=false;break;}if(v==0)++zeros;
  }
  if(ok){++ans;if(root&&d%p&&p%4==1){
   assert(zeros==1);assert((1LL*L*L+16LL*d*d*A)%p==0);
  }}
 }
 return ans;
}
int main(){
 for(int p=5;p<=43;++p)if(prime(p)){
  int n=count(p,p,1,true);assert(n==(p%4==1?p:0));
  cout<<"p "<<p<<" full_period "<<n<<'\n';
 }
 for(auto [p,yes,no]:vector<tuple<int,int,int>>{{7,5,6},{11,6,7},{19,9,10},{23,8,9},{31,10,11}}){
  int a=count(p,yes,1),b=count(p,no,1);
  assert(a>0&&b==0);
  cout<<"p "<<p<<" allowed "<<yes<<" "<<a<<" forbidden "<<no<<" "<<b<<'\n';
 }
 for(int d=1;d<9;++d)if(d%3)assert(count(9,5,d)==0);
 cout<<"mod9 PASS\n";
}
