#include <bits/stdc++.h>
using namespace std;
using ll=long long;
ll mpow(ll a,ll e,ll mod){ll r=1;for(;e;e>>=1,a=a*a%mod)if(e&1)r=r*a%mod;return r;}
int main(int argc,char**argv){
 int N=argc>1?atoi(argv[1]):100000;
 vector<bool> prime(N,true);prime[0]=prime[1]=false;
 for(int x=2;x*x<N;x++)if(prime[x])for(int y=x*x;y<N;y+=x)prime[y]=false;
 const int base[12]={2,4,6,8,10,12,14,16,18,20,24,32};
 const int coef[12]={-49,255,-495,250,780,-1977,2205,-1215,135,140,-30,1};
 for(int p=37;p<N;p++)if(prime[p]){
  int r[12];for(int i=0;i<12;i++)r[i]=1;
  for(int j=0;j<p-1;j++){
   ll val=0;for(int i=0;i<12;i++)val+=(ll)coef[i]*r[i];
   if((val%p+p)%p==0){
    ll mod=(ll)p*p;ll lo=0,hi=0;
    for(int i=0;i<12;i++){
     lo+=coef[i]*mpow(base[i],j,mod);
     hi+=coef[i]*mpow(base[i],j+p-1,mod);
    }
    if(((hi-lo)%mod+mod)%mod==0)cout<<p<<","<<j<<"\n";
   }
   for(int i=0;i<12;i++)r[i]=(ll)r[i]*base[i]%p;
  }
 }
}
