// Exact 4-row 8-point circle chord census by Gaussian integer factorization.
// Independent of (d0,d1) or (d1,d2) lattice scans.
// g++ -O3 -std=c++17 q48_gauss.cpp -o q48_gauss && ./q48_gauss 10000000
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <stdexcept>
#include <vector>
using namespace std;
using ll=long long;
using Z=pair<ll,ll>;
static Z mul(Z a,Z b){return {a.first*b.first-a.second*b.second,a.first*b.second+a.second*b.first};}
static ll power(ll a,ll e,ll p){ll r=1;while(e){if(e&1)r=r*a%p;a=a*a%p;e>>=1;}return r;}
static ll isqrtll(ll x){ll r=sqrtl((long double)x);while((r+1)*(r+1)<=x)++r;while(r*r>x)--r;return r;}
static Z prime_sum_two_squares(int p){
 int g=2;while(power(g,(p-1)/2,p)!=p-1)++g;
 ll root=power(g,(p-1)/4,p);
 for(ll v:{root,(ll)p-root}){
  ll a=p,b=v;
  while(b*b>p){ll t=a%b;a=b;b=t;}
  ll c=isqrtll((ll)p-b*b);
  if(b*b+c*c==p)return {b,c};
 }
 throw runtime_error("Cornacchia failed for p="+to_string(p));
}
static vector<pair<int,int>> factor(int n,const vector<int>&spf){
 vector<pair<int,int>> f;
 while(n>1){int p=spf[n],e=0;do{n/=p;++e;}while(n%p==0);f.emplace_back(p,e);}
 return f;
}
int main(int argc,char**argv){
 int B=argc>1?atoi(argv[1]):1000000;
 if(B<3||B>100000000){cerr<<"3<=B<=100000000 required\n";return 2;}
 vector<int> spf(B+3);
 for(int i=2;i<(int)spf.size();++i)if(!spf[i]){
  spf[i]=i;
  if((ll)i*i<(int)spf.size())for(ll j=(ll)i*i;j<(int)spf.size();j+=i)if(!spf[j])spf[j]=i;
 }
 map<int,Z> repr;
 set<array<ll,4>> hits;
 ll candidate_b=0,valid_b=0,generated=0;
 for(int b=3;b<=B;b+=2){
  ++candidate_b;
  auto f1=factor(b-2,spf),f2=factor(b+2,spf);
  f1.insert(f1.end(),f2.begin(),f2.end());
  bool bad=false;
  for(auto [p,e]:f1)if(p%4==3 && (e&1)){bad=true;break;}
  if(bad)continue;
  ++valid_b;
  vector<Z> z={{1,1}}; // norm 2, since 2(b^2-4)
  for(auto [p,e]:f1){
   if(p%4==3){ll scale=1;for(int i=0;i<e/2;++i)scale*=p;for(auto &v:z){v.first*=scale;v.second*=scale;}continue;}
   if(p%4!=1)throw runtime_error("unexpected factor");
   auto it=repr.find(p);
   if(it==repr.end())it=repr.emplace(p,prime_sum_two_squares(p)).first;
   Z pi=it->second,conj={pi.first,-pi.second};
   vector<Z> powers(e+1,{1,0}),conjs(e+1,{1,0});
   for(int i=1;i<=e;++i){powers[i]=mul(powers[i-1],pi);conjs[i]=mul(conjs[i-1],conj);}
   vector<Z> next;next.reserve(z.size()*(e+1));
   for(auto v:z)for(int k=0;k<=e;++k)next.push_back(mul(v,mul(powers[k],conjs[e-k])));
   z.swap(next);
  }
  for(auto [x,y]:z){
   ll u=llabs(x),v=llabs(y);
   for(auto [a,c]:{Z{u,v},Z{v,u}}){
    ++generated;
    if(a==0||c==0||a>B||c>B)continue;
    ll d2=3LL*b*b-2*a*a-24;
    if(d2<=0||d2>1LL*B*B)continue;
    ll d=isqrtll(d2);
    if(d*d!=d2||d==0||d>B)continue;
    if((a&1)==0||(b&1)==0||(c&1)==0||(d&1)==0)continue;
    if(a*a-2LL*b*b+c*c!=-8||b*b-2LL*c*c+d*d!=-8)throw runtime_error("inconsistent");
    hits.insert({a,b,c,d});
   }
  }
 }
 cerr<<"B="<<B<<" odd-b="<<candidate_b<<" admissible-b="<<valid_b<<" Gaussian-candidates="<<generated<<" patterns="<<hits.size()<<"\n";
 for(auto v:hits)cout<<v[0]<<","<<v[1]<<","<<v[2]<<","<<v[3]<<"\n";
}
