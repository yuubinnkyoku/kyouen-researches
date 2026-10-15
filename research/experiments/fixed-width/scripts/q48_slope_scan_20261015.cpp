#include <bits/stdc++.h>
using namespace std;
using ll=long long;
int main(){
 vector<tuple<ll,ll,ll,ll,ll,ll,ll,ll>> out;
 for(ll B=1;B<=30;B++)for(ll A=3*B+1;A<=180;A++){
  if(gcd(A,B)!=1 || A*A*A*A-18*A*A*B*B+9*B*B*B*B <= 0)continue;
  ll g=gcd(A,3LL), P=A*A-B*B,Q=(A*A-9*B*B)/(g*g);
  for(ll L=1;L<=20000;L++){
   ll n=P*L*L+8;
   if(n%Q)continue;
   ll v=n/Q;
   ll M=sqrtl(v);while(M*M<v)M++;while(M*M>v)M--;
   if(M*M!=v)continue;
   ll a=A*L-3*B/g*M,b=A/g*M-B*L,c=A/g*M+B*L,d=A*L+3*B/g*M;
   if(a>0 && a<b && b<c && c<d && a%2 && b%2 && c%2 && d%2){
    out.push_back({d,A,B,L,M,a,b,c});
    break;
   }
  }
 }
 sort(out.begin(),out.end());
 cerr<<"slope solutions "<<out.size()<<"\n";
 for(auto [d,A,B,L,M,a,b,c]:out) cout<<"span="<<d<<" slope="<<A<<"/"<<B<<" L="<<L<<" M="<<M<<" chords="<<a<<","<<b<<","<<c<<","<<d<<"\n";
}
