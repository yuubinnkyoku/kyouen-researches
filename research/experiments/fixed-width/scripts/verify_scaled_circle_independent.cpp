#include <algorithm>
#include <cassert>
#include <cmath>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
long long isqrtll(long long n) {
  long long lo=0, hi=1;
  while (hi*hi<=n) hi*=2;
  while (lo+1<hi) { long long m=(lo+hi)/2; if(m*m<=n)lo=m;else hi=m; }
  return lo;
}
vector<int> rows(int g,int h){
  vector<int> v;
  for(int y=0;y<h;y++) {
    long long D=55250LL*g*g-(2LL*y-235LL*g)*(2LL*y-235LL*g);
    if(D<=0)continue;
    long long s=isqrtll(D);
    if(s*s!=D || ((s-g)&1))continue;
    long long x=(-g+s)/2;
    assert(x*x+1LL*y*y+1LL*g*x-235LL*g*y-6LL*g*g==0);
    v.push_back(y);
  }
  return v;
}
int main(){
  auto b=rows(1,236);
  assert(b.size()==32);
  const int expected[8]={211,214,221,226,232,233,235,236};
  for(int k=25;k<=32;k++){
    int best=100000;
    for(int i=0;i+k<=(int)b.size();i++) best=min(best,b[i+k-1]-b[i]+1);
    assert(best==expected[k-25]);
    cout<<"k="<<k<<" min_window="<<best<<"\n";
  }
  for(int g: {1,2,3,4,7,8,11,16}){
    auto v=rows(g,210*g+1);
    assert(v.size()==25 && v.front()==0 && v.back()==210*g);
    int d=0;
    for(auto y:v) d=gcd(d,y);
    assert(d==g);
    cout<<"g="<<g<<" rows="<<v.size()<<" gcd="<<d<<"\n";
  }
  cout<<"PASS\n";
}
