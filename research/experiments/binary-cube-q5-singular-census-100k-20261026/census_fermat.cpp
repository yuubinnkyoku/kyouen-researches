#include <bits/stdc++.h>
using namespace std;
using ll=long long;
ll modpow(ll a,ll n,ll m){ll r=1;for(;n;n>>=1,a=a*a%m)if(n&1)r=r*a%m;return r;}
int main(int argc,char**argv){
 int N=argc>1?atoi(argv[1]):100000;
 vector<bool> is(N,true);is[0]=is[1]=false;
 for(int i=2;i*i<N;i++)if(is[i])for(int j=i*i;j<N;j+=i)is[j]=false;
 const int A[]={32,24,20,18,16,14,12,10,8,6,4,2};
 const int C[]={1,-30,140,135,-1215,2205,-1977,780,250,-495,255,-49};
 int primes=0,singulars=0;map<int,int> hist;
 for(int p=37;p<N;p++)if(is[p]){
  primes++;ll powv[12],fq[12];
  for(int i=0;i<12;i++){powv[i]=1;fq[i]=(modpow(A[i],p-1,1LL*p*p)-1)/p;}
  int roots=0;
  for(int j=0;j<p-1;j++){
   ll s=0,t=0;
   for(int i=0;i<12;i++){s+=C[i]*powv[i];t+=C[i]*powv[i]*fq[i];}
   if((s%p+p)%p==0){
    roots++;
    if((t%p+p)%p==0){singulars++;cout<<p<<","<<j<<",0,0\n";}
   }
   for(int i=0;i<12;i++)powv[i]=powv[i]*A[i]%p;
  }
  hist[roots]++;
 }
 cerr<<"primes="<<primes<<" singular="<<singulars<<" histogram:";
 for(auto [a,b]:hist)cerr<<" "<<a<<":"<<b;
 cerr<<"\n";
}
