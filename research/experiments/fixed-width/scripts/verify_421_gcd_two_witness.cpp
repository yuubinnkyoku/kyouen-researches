// Independent integer-root enumeration for the 421-row gcd-two witness.
#include <cassert>
#include <cmath>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
int main(){
 vector<int> a,b;
 int g=0;
 for(int y=0;y<421;y++){
  long long r=25LL+470LL*y-1LL*y*y;
  if(r<=0)continue;
  long long x=llround(sqrt((long double)r));
  while(x*x<r)++x;
  while(x*x>r)--x;
  if(x*x!=r)continue;
  assert(x>0 && x*x+1LL*y*y-470LL*y-25==0);
  b.push_back(y);
  g=gcd(g,y);
 }
 for(int y=0;y<211;y++){
  long long d2=25LL+940LL*y-4LL*y*y;
  if(d2<=0)continue;
  long long d=llround(sqrt((long double)d2));
  while(d*d<d2)++d;
  while(d*d>d2)--d;
  if(d*d!=d2 || d%2==0)continue;
  long long x=(-1+d)/2;
  assert(x*x+x+1LL*y*y-235LL*y-6==0);
  a.push_back(y);
 }
 assert(a.size()==25 && b.size()==25 && g==2);
 for(int i=0;i<25;i++)assert(b[i]==2*a[i]);
 assert(b.front()==0 && b.back()==420 && b[1]==2);
 cout<<"PASS independent C++ witness: 25 rows in 211; 25 even rows in 421; gcd=2\n";
}
