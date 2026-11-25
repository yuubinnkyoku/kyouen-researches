// Independent exact integer-circle census; no chord-length identity used.
#include <array>
#include <cassert>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <set>
using namespace std;
using ll=long long;
using Circle=array<ll,4>;
ll sq(ll x){return x*x;}
ll root(ll x){
 if(x<0)return -1;
 ll t=(ll)sqrtl((long double)x);
 while(sq(t)>x)--t;
 while(sq(t+1)<=x)++t;
 return sq(t)==x?t:-1;
}
Circle from_triple(ll x0,ll x1,ll x2,ll h){
 ll f2=sq(x1)+sq(h)-sq(x0),f3=sq(x2)+4*sq(h)-sq(x0);
 ll a=h*(2*x1-x2-x0);
 if(!a)return {0,0,0,0};
 ll b=h*(f3-2*f2);
 ll c=(x2-x0)*f2-(x1-x0)*f3;
 ll d=-a*sq(x0)-b*x0;
 ll g=gcd(gcd(abs(a),abs(b)),gcd(abs(c),abs(d)));
 a/=g;b/=g;c/=g;d/=g;
 if(a<0){a=-a;b=-b;c=-c;d=-d;}
 return {a,b,c,d};
}
bool two_roots(Circle z,ll y,ll m){
 auto [a,b,c,d]=z;
 ll disc=b*b-4*a*(a*y*y+c*y+d),t=root(disc);
 if(t<=0)return false;
 ll den=2*a,l=-b-t,r=-b+t;
 if(l%den||r%den)return false;
 return l/den>=0&&l/den<r/den&&r/den<m;
}
size_t circles(int h,int m){
 set<Circle> found;
 for(int x=0;x<m;++x)for(int y=0;y<m;++y)for(int z=0;z<m;++z){
  auto c=from_triple(x,y,z,h);
  if(c[0]&&two_roots(c,0,m)&&two_roots(c,h,m)&&two_roots(c,2*h,m))
   found.insert(c);
 }
 return found.size();
}
int r2_over4(int h){
 ll n=4LL*h+1;
 int r2=0;
 for(ll a=0;a*a<=n;++a){
  ll b=root(n-a*a);
  if(b<0)continue;
  r2+=(a==0||b==0)?2:4;
 }
 assert(r2%4==0);
 return r2/4;
}
int main(int argc,char**argv){
 int limit=argc>1?atoi(argv[1]):60;
 if(limit<1||limit>60)return 2;
 cout<<"h,width_below,below_count,threshold_width,threshold_count,r2_over_4\n";
 for(int h=1;h<=limit;++h){
  int m=2*h+1;
  size_t below=circles(h,m),at=circles(h,m+1);
  int expected=r2_over4(h);
  cout<<h<<","<<m<<","<<below<<","<<m+1<<","<<at<<","<<expected<<"\n";
  if(below!=0||at!=(size_t)expected)return 1;
 }
}
