#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){int LIMIT=argc>1?atoi(argv[1]):3000000;const int K0=25,K1=110;vector<uint8_t> cnt(LIMIT+1,1);
vector<uint8_t> composite(LIMIT+1,0);for(int i=2;1LL*i*i<=LIMIT;i++)if(!composite[i])for(int j=i*i;j<=LIMIT;j+=i)composite[j]=1;
for(int p=5;p<=LIMIT;p+=4)if(!composite[p])for(long long j=p;j<=LIMIT;j+=p){int e=0;long long z=j;while(z%p==0){e++;z/=p;}cnt[j]=min(255,cnt[j]*(e+1));}
struct Rec{int w=INT_MAX,N=0,par=0,lo=0,hi=0;};array<Rec,K1+1> best;int candidates=0;
for(int N=2;N<=LIMIT;N++){if(cnt[N]<13)continue;candidates++;vector<int> ys[2];int x=1,y=(int)sqrt((double)N);while(1LL*y*y>N)y--;while(1LL*(y+1)*(y+1)<=N)y++;for(;x*x<=N;x++){while(y>=0&&x*x+y*y>N)y--;if(y<0)break;if(x*x+y*y==N){ys[y&1].push_back(-y);if(y)ys[y&1].push_back(y);}}
for(int p=0;p<2;p++){auto &v=ys[p];if(v.size()<K0)continue;sort(v.begin(),v.end());v.erase(unique(v.begin(),v.end()),v.end());for(int k=K0;k<=K1&&k<=(int)v.size();k++)for(int j=k-1;j<(int)v.size();j++){int w=(v[j]-v[j-k+1])/2+1;if(w<best[k].w){best[k]={w,N,p,v[j-k+1],v[j]};}}}}
cerr<<"LIMIT "<<LIMIT<<" candidates "<<candidates<<"\n";for(int k=K0;k<=K1;k++){auto &r=best[k];if(r.w!=INT_MAX)cout<<k<<" "<<r.w<<" "<<r.N<<" "<<r.par<<" "<<r.lo<<" "<<r.hi<<"\n";}
}
