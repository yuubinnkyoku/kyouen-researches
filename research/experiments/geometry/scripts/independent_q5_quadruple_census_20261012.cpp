// Independent q=5 overlap census: enumerate forbidden quadruples, group by exact integer support equations.
#include <array>
#include <algorithm>
#include <iostream>
#include <map>
#include <numeric>
#include <vector>
using namespace std;
using ll=long long;
using U=unsigned __int128;
struct P{ll x,y;};
using Key=array<ll,5>; // type 0=line, 1=circle, then 4 coefficients
ll cross(ll x,ll y,ll u,ll v){return x*v-y*u;}
Key normalize(Key k){ll g=0;for(int i=1;i<5;i++)g=gcd(g,abs(k[i]));for(int i=1;i<5;i++)k[i]/=g;for(int i=1;i<5;i++)if(k[i]){if(k[i]<0)for(int j=1;j<5;j++)k[j]=-k[j];break;}return k;}
Key support(P p,P q,P r){
 ll x=q.x-p.x,y=q.y-p.y,u=r.x-p.x,v=r.y-p.y;
 ll delta=cross(x,y,u,v);
 if(!delta)return normalize({0,y,-x,x*p.y-y*p.x,0});
 ll h=-(q.x*q.x+q.y*q.y-p.x*p.x-p.y*p.y);
 ll j=-(r.x*r.x+r.y*r.y-p.x*p.x-p.y*p.y);
 ll A=h*v-j*y,B=x*j-u*h,C=-delta*(p.x*p.x+p.y*p.y)-A*p.x-B*p.y;
 return normalize({1,delta,A,B,C});
}
ll choose(ll n,int k){if(n<k)return 0;ll r=1;for(int i=1;i<=k;i++)r=r*(n-i+1)/i;return r;}
int main(int argc,char**argv){
 int n=argc>1?stoi(argv[1]):11,N=n*n; if(N>128)return 2;
 vector<P> p;for(int y=0;y<n;y++)for(int x=0;x<n;x++)p.push_back({x,y});
 map<Key,U> curves;ll quad=0;
 for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++){
   Key key=support(p[a],p[b],p[c]);
   for(int d=c+1;d<N;d++){
    P z=p[d];bool on=key[0]==0 ? key[1]*z.x+key[2]*z.y+key[3]==0:
       key[1]*(z.x*z.x+z.y*z.y)+key[2]*z.x+key[3]*z.y+key[4]==0;
    if(!on)continue;
    quad++;curves[key]|=((U)1<<a)|((U)1<<b)|((U)1<<c)|((U)1<<d);
   }
 }
 vector<ll> d1(N),d2(N*N);array<ll,5> M{};ll F=0;ll kept=0;array<ll,14> Fq{};int max_k=0;ll c12=0;
 for(auto &[key,mask]:curves){
   vector<int> ids;for(int i=0;i<N;i++)if(mask>>i&1)ids.push_back(i);
   int k=ids.size();max_k=max(max_k,k);if(key[0]==1 && k==12)c12++;for(int q=4;q<=12;q++)Fq[q]+=choose(k,q);if(k<5)continue;kept++;F+=choose(k,5);
   for(int i:ids)d1[i]+=choose(k-1,4);
   for(int i:ids)for(int j:ids)if(i<j)d2[i*N+j]+=choose(k-2,3);
   M[3]+=choose(k,3)*choose(choose(k-3,2),2);
   M[4]+=choose(k,4)*choose(k-4,2);
 }
 M[0]=choose(F,2);for(ll d:d1)M[1]+=choose(d,2);for(ll d:d2)M[2]+=choose(d,2);
 array<ll,5> O{};
 O[4]=M[4];O[3]=M[3]-4*O[4];O[2]=M[2]-3*O[3]-6*O[4];
 O[1]=M[1]-2*O[2]-3*O[3]-4*O[4];O[0]=M[0]-O[1]-O[2]-O[3]-O[4];
 cout<<"n="<<n<<" quadruples="<<quad<<" q5_curves="<<kept<<" F5="<<F<<" M=";
 for(ll x:M)cout<<x<<",";cout<<" O=";for(ll x:O)cout<<x<<",";cout<<" max_k="<<max_k<<" C12="<<c12<<" Fq4..12=";for(int q=4;q<=12;q++)cout<<Fq[q]<<",";cout<<"\n";
}
