#include <bits/stdc++.h>
using namespace std;
using ll=long long;
static bool square(ll n,ll &x){if(n<0)return false;x=sqrtl((long double)n);while(x*x<n)++x;while(x*x>n)--x;return x*x==n;}
struct Answer{int width=INT_MAX;int type=0;int n=0;int parity=0;vector<int> ys;};
int main(int argc,char**argv){int limit=argc>1?atoi(argv[1]):30000000;int minK=34,maxK=96;vector<Answer> best(maxK+1);int R=sqrt(limit)+1;vector<uint16_t> ce(limit+1),co(limit+1);
for(int x=1;x<=R;x++)for(int y=0;1LL*x*x+1LL*y*y<=limit;y++){int n=x*x+y*y;(y%2?co[n]:ce[n])+=y?2:1;}
vector<uint16_t> he(4LL*limit+1),ho(4LL*limit+1);
for(int x=1;1LL*x*x<=4LL*limit;x+=2)for(int y=0;1LL*x*x+4LL*y*y<=4LL*limit;y++){int n=x*x+4*y*y;(y%2?ho[n]:he[n])+=y?2:1;}
ll candidates=0;
auto eval=[&](int n,int type,int parity,int count){if(count<minK)return; ++candidates;vector<int> ys;int ymax=type?sqrtl((long double)n/4):sqrtl((long double)n);for(int y=-ymax;y<=ymax;y++){if((y&1)!=parity)continue;ll x2=type?n-4LL*y*y:n-1LL*y*y,X;if(x2>0&&square(x2,X)&&(!type||(X&1)))ys.push_back(y);}
if((int)ys.size()!=count){cerr<<"count mismatch "<<n<<" "<<type<<" "<<parity<<" "<<ys.size()<<" "<<count<<"\n";exit(1);}
for(int k=minK;k<=maxK && k<=count;k++)for(int i=0;i+k<=count;i++){int w=ys[i+k-1]-ys[i]+1;if(w<best[k].width){best[k]={w,type,n,parity,vector<int>(ys.begin()+i,ys.begin()+i+k)};}}};
for(int n=1;n<=limit;n++){if(ce[n]>=minK)eval(n,0,0,ce[n]);if(co[n]>=minK)eval(n,0,1,co[n]);}
for(int n=1;n<=4LL*limit;n+=4){if(he[n]>=minK)eval(n,1,0,he[n]);if(ho[n]>=minK)eval(n,1,1,ho[n]);}
cout<<"# candidates="<<candidates<<" limit="<<limit<<"\n";
for(int k=minK;k<=maxK;k++){auto &b=best[k];if(b.width==INT_MAX){cout<<k<<"\tNA\n";continue;}cout<<k<<"\t"<<b.width<<"\t"<<b.type<<"\t"<<b.n<<"\t"<<b.ys.front()<<"\t"<<b.ys.back()<<"\t";for(int y:b.ys)cout<<y<<",";cout<<"\n";}
}
