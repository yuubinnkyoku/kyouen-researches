// Exhaustive named-vertex closed-neighborhood recursion.
// Checks the length generating polynomial and sharp fixed-edge extrema.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <limits>
#include <numeric>
#include <vector>
using namespace std;
using U=unsigned long long;
U fac[12];
struct Poly {array<U,12> v{};};

Poly enumerate_plays(int mask,const vector<int>& closed,vector<Poly>& memo,vector<char>& seen){
 if(seen[mask])return memo[mask];
 seen[mask]=1;
 Poly p;
 if(!mask){p.v[0]=1;return memo[mask]=p;}
 for(int x=mask;x;x&=x-1){
  int i=__builtin_ctz((unsigned)x);
  Poly child=enumerate_plays(mask&~closed[i],closed,memo,seen);
  for(int t=0;t<11;t++)p.v[t+1]+=child.v[t];
 }
 return memo[mask]=p;
}
Poly direct(int k,int m,unsigned edges){
 int n=k+m;
 vector<int> closed(n);
 for(int i=0;i<n;i++)closed[i]=1<<i;
 for(int i=0;i<k;i++)for(int j=0;j<k;j++)closed[i]|=1<<j;
 for(int i=0;i<k;i++)for(int j=0;j<m;j++)if(edges>>(i*m+j)&1u){
  closed[i]|=1<<(k+j);closed[k+j]|=1<<i;
 }
 vector<Poly> memo(1<<n);vector<char> seen(1<<n);
 return enumerate_plays((1<<n)-1,closed,memo,seen);
}
Poly formula(int k,int m,unsigned edges){
 Poly p;
 if(k==0){p.v[m]=fac[m];return p;}
 bool all_positive=true;
 for(int i=0;i<k;i++){
  int d=0;
  for(int j=0;j<m;j++)d+=edges>>(i*m+j)&1u;
  all_positive&=d>0;
  p.v[m+1-d]+=fac[m+1-d];
 }
 if(all_positive)p.v[m]+=fac[m];
 return p;
}
vector<int> balanced(int n,int lo,int hi,int total){
 if(n==0)return total==0?vector<int>{}:vector<int>{-1};
 if(total<n*lo||total>n*hi)return {-1};
 int q=(total-n*lo)/n,r=(total-n*lo)%n;
 vector<int> a(n,lo+q);
 for(int i=0;i<r;i++)a[i]++;
 return a;
}
vector<int> extremes(int n,int lo,int hi,int total){
 if(n==0)return total==0?vector<int>{}:vector<int>{-1};
 if(total<n*lo||total>n*hi)return {-1};
 if(lo==hi)return vector<int>(n,lo);
 int q=(total-n*lo)/(hi-lo),r=(total-n*lo)%(hi-lo);
 vector<int> a(q,hi);
 if(r)a.push_back(lo+r);
 while((int)a.size()<n)a.push_back(lo);
 return a;
}
pair<U,U> sharp(int k,int m,int e){
 U mn=numeric_limits<U>::max(),mx=0;
 auto value=[&](const vector<int>& a,bool positive){
  U ans=positive?fac[m]:0;
  for(int d:a)ans+=fac[m+1-d];
  return ans;
 };
 if(e<=(k-1)*m){
  auto a=balanced(k-1,0,m,e);
  a.push_back(0);
  mn=min(mn,value(a,false));
  auto b=extremes(k,0,m,e);
  assert(find(b.begin(),b.end(),0)!=b.end());
  mx=max(mx,value(b,false));
 }
 if(e>=k){
  auto a=balanced(k,1,m,e),b=extremes(k,1,m,e);
  mn=min(mn,value(a,true));
  mx=max(mx,value(b,true));
 }
 return {mn,mx};
}
int main(){
 fac[0]=1;
 for(int i=1;i<12;i++)fac[i]=fac[i-1]*i;
 U graphs=0,plays=0;
 int comparisons=0;
 for(int k=0;k<=5;k++)for(int m=0;m<=5;m++){
  if(k*m>16||k+m>10)continue;
  int cases=1<<(k*m);
  vector<pair<U,U>> actual(k*m+1,{numeric_limits<U>::max(),0});
  for(int bits=0;bits<cases;bits++){
   auto p=direct(k,m,bits),q=formula(k,m,bits);
   assert(p.v==q.v);
   U cnt=accumulate(p.v.begin(),p.v.end(),0ULL);
   int e=__builtin_popcount((unsigned)bits);
   actual[e].first=min(actual[e].first,cnt);
   actual[e].second=max(actual[e].second,cnt);
   graphs++;
   plays+=cnt;
  }
  if(k>0)for(int e=0;e<=k*m;e++){
   assert(actual[e]==sharp(k,m,e));
   comparisons++;
  }
 }
 cout<<"PASS: graphs="<<graphs
     <<" extremal_edge_classes="<<comparisons
     <<" terminal_sequences_sum="<<plays
     <<"; direct closed-neighborhood DFS matches formula and both sharp extrema\n";
}
