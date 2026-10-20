#include <bits/stdc++.h>
using namespace std;
using ll=long long;
using V=vector<ll>;
using P=pair<ll,ll>;
V Bfam(int k,int p,int q){
 V d={q,p,q,k==0?q:(k==1?p:q+p)};
 V B={0};for(auto x:d)B.push_back(B.back()+x);return B;
}
map<ll,int> profile(const V &a){map<ll,int>r;for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)r[a[i]+a[j]]++;return r;}
int H(const V &a){int z=0;for(auto [s,n]:profile(a))z+=n*n;return z;}
int E2(const V &b,const V &c2){auto pb=profile(b),pc=profile(c2);int e=0;for(auto [s,n]:pb)e+=n*pc[2*s];return e;}
struct Circle{int bm,cm;};
int compatible_count(const V &b,const V &c2){
 vector<Circle>cs;
 for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)
  for(int k=0;k<5;k++)for(int l=k+1;l<5;l++)
   if(2*(b[i]+b[j])==c2[k]+c2[l])cs.push_back({(1<<i)|(1<<j),(1<<k)|(1<<l)});
 int n=cs.size(),z=0;
 for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++)for(int l=k+1;l<n;l++){
  int a[4]={i,j,k,l};bool good=true;
  for(int x=0;x<4;x++)for(int y=x+1;y<4;y++)
   if(__builtin_popcount(unsigned(cs[a[x]].bm&cs[a[y]].bm))+
      __builtin_popcount(unsigned(cs[a[x]].cm&cs[a[y]].cm))!=1)good=false;
  z+=good;
 }
 return z;
}

struct Lin {int a,b;};
bool operator<(const Lin &x,const Lin &y){return x.a<y.a||(x.a==y.a&&x.b<y.b);}
bool operator==(const Lin &x,const Lin &y){return x.a==y.a&&x.b==y.b;}
Lin operator+(Lin x,Lin y){return {x.a+y.a,x.b+y.b};}
Lin operator-(Lin x,Lin y){return {x.a-y.a,x.b-y.b};}
Lin twice(Lin x){return {2*x.a,2*x.b};}
using VL=vector<Lin>;
VL linear_family(int k){
  VL gaps;
  if(k==0)gaps={{1,0},{0,1},{1,0},{1,0}};
  if(k==1)gaps={{1,0},{0,1},{1,0},{0,1}};
  if(k==2)gaps={{1,0},{0,1},{1,0},{1,1}};
  VL B={{0,0}};
  for(auto x:gaps)B.push_back(B.back()+x);
  return B;
}
map<Lin,int> profile_linear(const VL &a){
  map<Lin,int>r;
  for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)r[a[i]+a[j]]++;
  return r;
}
int energy_linear(const VL &b,const VL &c){
  auto pb=profile_linear(b),pc=profile_linear(c);
  int E=0;for(auto [s,n]:pb)E+=n*pc[s];return E;
}
int h_linear(const VL &b){int z=0;for(auto [s,n]:profile_linear(b))z+=n*n;return z;}
void generic_audit(){
  for(int k=0;k<3;k++){
    VL B=linear_family(k),B2;
    for(auto x:B)B2.push_back(twice(x));
    auto pb=profile_linear(B);
    VL S;set<Lin>support;
    for(auto [s,n]:pb){S.push_back(s);support.insert(twice(s));}
    set<VL> seen;int hits=0;
    for(auto a:S)for(auto b:S)for(auto c:S){
      Lin x=a+b-c,y=a+c-b,z=b+c-a;
      if(x==y||x==z||y==z)continue;
      for(auto d:S){
        Lin w=twice(d)-x;
        if(w==x||w==y||w==z)continue;
        int good=0;for(auto t:VL{x,y,z})good+=support.count(w+t);
        if(good<2)continue;
        for(auto e:S){
          Lin v=twice(e)-x;
          if(v==x||v==y||v==z||v==w)continue;
          VL C={x,y,z,w,v};sort(C.begin(),C.end());
          if(!seen.insert(C).second)continue;
          int en=energy_linear(B2,C);
          if(en>=13){hits++;assert(en==14&&h_linear(C)==14&&C==B2);}
        }
      }
    }
    assert(seen.size()==544&&hits==1);
    cerr<<"generic family="<<k<<" candidates="<<seen.size()<<" high_energy="<<hits<<"\n";
  }
}
void ap_audit(){
  V C={0,2,4,6,8};int candidates=0,hits=0;
  vector<V> shapes;
  for(int parity=0;parity<2;parity++){
    V pool;
    for(int x=(parity==0?-10:-9);x<=(parity==0?18:17);x+=2)pool.push_back(x);
    int n=pool.size();
    for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)
      for(int d=c+1;d<n;d++)for(int e=d+1;e<n;e++){
        V B={pool[a],pool[b],pool[c],pool[d],pool[e]};candidates++;
        if(E2(C, V{2*B[0],2*B[1],2*B[2],2*B[3],2*B[4]})!=13)continue;
        assert(H(B)==14);
        hits++;shapes.push_back(B);
        assert(compatible_count(C,V{2*B[0],2*B[1],2*B[2],2*B[3],2*B[4]})==0);
      }
  }
  assert(candidates==5005&&hits==8);
  cerr<<"AP E13 candidates="<<candidates<<" hits="<<hits<<" compatible_four=0\n";
}

int main(){
 generic_audit();
 ap_audit();
 long long total=0,hits=0,unique_hits=0,compat=0;
 set<string> uniq;vector<string> ex;
 for(int k=0;k<3;k++){
  long long local=0;
  for(int p=1;p<=36;p++)for(int q=1;q<=24;q++){
   if(gcd(p,q)!=1)continue;
   V b=Bfam(k,p,q);
   if(H(b)!=14)continue;
   auto pb=profile(b);
   V S;for(auto [s,n]:pb)S.push_back(s);
   set<ll> good;for(ll s:S)good.insert(2*s);
   int m=S.size();
   for(int a=0;a<m;a++)for(int bb=0;bb<m;bb++)for(int c=0;c<m;c++){
    ll x=S[a]+S[bb]-S[c],y=S[a]+S[c]-S[bb],z=S[bb]+S[c]-S[a];
    if(x==y||x==z||y==z)continue;
    for(int d=0;d<m;d++){
     ll w=2*S[d]-x;
     if(w==x||w==y||w==z)continue;
     int ok=0;
     ll first4[]={x,y,z,w};
     for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)ok+=good.count(first4[i]+first4[j]);
     if(ok<5)continue;
     for(int e=0;e<m;e++){
      ll v=2*S[e]-x;
      if(v==x||v==y||v==z||v==w)continue;
      V C={x,y,z,w,v};sort(C.begin(),C.end());
      total++;
      if(E2(b,C)!=13)continue;
      // H(C) is unaffected by multiplying all C coordinates by 2.
      if(H(C)!=14)continue;
      hits++;local++;
      string key=to_string(k)+"/"+to_string(p)+"/"+to_string(q)+":";
      for(auto t:C)key+=to_string(t)+",";
      if(!uniq.insert(key).second)continue;
      unique_hits++;
      int ct=compatible_count(b,C);compat+=ct;
      if(ct||ex.size()<15){string s="k="+to_string(k)+" t="+to_string(p)+"/"+to_string(q)+" B=";for(auto z:b)s+=to_string(z)+",";s+=" C2=";for(auto z:C)s+=to_string(z)+",";s+=" four="+to_string(ct);ex.push_back(s);}
     }
    }
   }
  }
  cerr<<"family="<<k<<" E13H14hits="<<local<<"\n";
 }
 cout<<"tested_candidates="<<total<<" hits="<<hits<<" unique="<<unique_hits<<" compatible_four="<<compat<<"\n";
 for(auto s:ex)cout<<s<<"\n";
}
