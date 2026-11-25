// Exact all-real lambda classification for 3x6, with independent checks.
// C++17: g++ -O2 -std=c++17 quadratic_3x6.cpp -o quadratic_3x6
#include <bits/stdc++.h>
using namespace std;
using ll=long long;
struct Point { ll x,y; };
struct Rational {
 ll p,q;
 Rational(ll a=0,ll b=1) {
  if(b<0) a=-a,b=-b;
  ll g=std::gcd(abs(a),b); p=a/g;q=b/g;
 }
 bool operator<(const Rational& t) const {return (__int128)p*t.q<(__int128)t.p*q;}
 string str() const {return to_string(p)+(q==1?"":"/"+to_string(q));}
};
ll det3(const array<array<ll,3>,3>& a){
 return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]);
}
ll det4(array<array<ll,4>,4> a){
 // Independent Leibniz determinant (no shared det3 subroutine).
 array<int,4> p={0,1,2,3};ll s=0;
 do {int inv=0;ll v=1;for(int i=0;i<4;i++){v*=a[i][p[i]];for(int j=i+1;j<4;j++)inv+=p[i]>p[j];}s+=(inv&1)?-v:v;}while(next_permutation(p.begin(),p.end()));
 return s;
}
struct Quad {int mask;ll a,b;array<int,4> ids;};
struct Result {int grundy; int safe; int forb; vector<int> wins; array<int,19> sizes{}, terminals{}, gsizes{};};
Result bottom_up(int n, const vector<int>& fs) {
 const int N=1<<n;vector<unsigned char> bad(N,0),g(N,255);
 for(int m:fs)bad[m]=1;
 for(int m=1;m<N;m++)if(!bad[m]){
  int bits=m;
  while(bits){int b=bits&-bits;bits-=b;if(bad[m^b]){bad[m]=1;break;}}
 }
 Result r{};r.forb=fs.size();
 for(int m=N-1;m>=0;m--){
  if(bad[m])continue;
  r.safe++;int sz=__builtin_popcount((unsigned)m);r.sizes[sz]++;
  unsigned int present=0;bool terminal=true;
  int bits=(N-1)^m;
  while(bits){int b=bits&-bits;bits-=b;int t=m|b;if(bad[t])continue;terminal=false;present|=1u<<g[t];}
  if(terminal)r.terminals[sz]++;
  g[m]=__builtin_ctz(~present);r.gsizes[g[m]]++;
 }
 r.grundy=g[0];for(int i=0;i<n;i++)if(g[1<<i]==0)r.wins.push_back(i);
 return r;
}
Result top_down(int n,const vector<Quad>& quads,Rational lambda){
 vector<vector<int>> by_new(n);int forbidden=0;
 for(auto &z:quads){
  array<array<ll,4>,4> a{};
  for(int k=0;k<4;k++){
   auto id=z.ids[k];ll x=id/3,y=id%3;
   a[k]={lambda.q*x*x+lambda.p*y*y,lambda.q*x,lambda.q*y,lambda.q};
  }
  if(det4(a)!=0)continue;
  forbidden++;
  for(int i:z.ids)by_new[i].push_back(z.mask^(1<<i));
 }
 const int N=1<<n;vector<signed char> memo(N,-1);Result r{};r.forb=forbidden;
 auto rec=[&](auto&& self,int mask)->int{
  if(memo[mask]!=-1)return memo[mask];
  r.safe++;int sz=__builtin_popcount((unsigned)mask);r.sizes[sz]++;
  unsigned present=0;bool terminal=true;
  for(int i=0;i<n;i++)if(!(mask>>i&1)){
   bool legal=true;for(int tri:by_new[i])if((mask&tri)==tri){legal=false;break;}
   if(!legal)continue;
   terminal=false;present|=1u<<self(self,mask|(1<<i));
  }
  if(terminal)r.terminals[sz]++;
  int g=__builtin_ctz(~present);r.gsizes[g]++;memo[mask]=g;return g;
 };
 r.grundy=rec(rec,0);
 for(int i=0;i<n;i++)if(memo[1<<i]==0)r.wins.push_back(i);
 return r;
}
int main(int argc,char**argv){
 int width=argc>1?atoi(argv[1]):6;const int n=3*width;
 if(width<2||n>21){cerr<<"width must be 2..7\n";return 2;}
 vector<Point> points;for(int x=0;x<width;x++)for(int y=0;y<3;y++)points.push_back({x,y});
 vector<Quad> quads;set<Rational> ex;
 for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++)for(int l=k+1;l<n;l++){
  array<int,4> ids={i,j,k,l};array<array<ll,3>,3> A{},B{};
  for(int h=1;h<4;h++){
   Point p=points[ids[h]],q=points[i];
   A[h-1]={p.x*p.x-q.x*q.x,p.x-q.x,p.y-q.y};
   B[h-1]={p.y*p.y-q.y*q.y,p.x-q.x,p.y-q.y};
  }
  ll a=det3(A),b=det3(B);
  if(b)ex.insert(Rational(-a,b));
  quads.push_back({(1<<i)|(1<<j)|(1<<k)|(1<<l),a,b,ids});
 }
 Rational generic(1000003);
 if(ex.count(generic)){cerr<<"generic collision\n";return 2;}
 vector<pair<string,Rational>> cases={{"generic",generic}};
 for(auto v:ex)cases.push_back({v.str(),v});
 cout<<"# width="<<width<<" height=3 exceptions="<<ex.size()<<" quadruples="<<quads.size()<<" cases="<<cases.size()<<"\n";
 cout<<"lambda\tgrundy\tsafe\tforbidden\twins\tmaximal\tsafe_by_size\n";
 for(auto &[label,lam]:cases){
  vector<int> fs;for(auto &q:quads)if(q.a*lam.q+q.b*lam.p==0)fs.push_back(q.mask);
  Result a=bottom_up(n,fs),b=top_down(n,quads,lam);
  if(a.grundy!=b.grundy||a.safe!=b.safe||a.forb!=b.forb||a.wins!=b.wins||a.sizes!=b.sizes||a.terminals!=b.terminals||a.gsizes!=b.gsizes){cerr<<"MISMATCH at "<<label<<"\n";return 1;}
  auto vec=[&](const vector<int>& v){string s;for(int x:v){if(!s.empty())s+=",";s+=to_string(x);}return s.empty()?"-":s;};
  auto hist=[&](const array<int,19>& v){string s;for(int i=0;i<=n;i++)if(v[i]){if(!s.empty())s+=",";s+=to_string(i)+":"+to_string(v[i]);}return s;};
  cout<<label<<"\t"<<a.grundy<<"\t"<<a.safe<<"\t"<<a.forb<<"\t"<<vec(a.wins)<<"\t"<<hist(a.terminals)<<"\t"<<hist(a.sizes)<<"\n";
 }
 cerr<<"Independent 3x3 bottom-up and 4x4 top-down checks PASS: "<<cases.size()<<" cases.\n";
}
