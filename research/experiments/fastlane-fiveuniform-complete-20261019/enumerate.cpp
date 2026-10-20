#include <bits/stdc++.h>
using namespace std;
// Enumerate every multiset of nonempty membership patterns in five labelled 4-edges.
// An integer count[t] means that many vertices occur in precisely the edges indexed by set bits of t.
constexpr int H=5;
int cnt[32],remaining[5]={4,4,4,4,4},nverts=0;
long long patterns[21]={}, valid[21]={};
long long hist[21][21]={};
int maxg[21];
array<int,5> best_edges[21];
long long components[6]={};
int target_n=-1;
ofstream g6dump;
int grundy(vector<int> edges,int n){
 int sz=1<<n,full=sz-1;
 vector<unsigned char> g(sz);
 for(int s=full;s>=0;s--){
  bool bad=false;
  for(int e:edges)if((s&e)==e){bad=true;break;}
  if(bad){g[s]=255;continue;}
  unsigned seen=0;
  for(int b=full^s;b;b&=b-1){int t=s|(b&-b),v=g[t];if(v!=255)seen|=1u<<v;}
  g[s]=__builtin_ctz(~seen);
 }
 return g[0];
}
int evaluate(array<int,5>& E,int n){
 int parent[5]={0,1,2,3,4};
 auto root=[&](int a){while(parent[a]!=a)a=parent[a]=parent[parent[a]];return a;};
 for(int i=0;i<5;i++)for(int j=0;j<i;j++)if(E[i]&E[j]){int a=root(i),b=root(j);parent[a]=b;}
 int g=0, comps=0;
 for(int i=0;i<5;i++)if(root(i)==i){
  comps++;
  int U=0;vector<int> ed;
  for(int j=0;j<5;j++)if(root(j)==i){ed.push_back(E[j]);U|=E[j];}
  int m=__builtin_popcount((unsigned)U);
  vector<int> ee;for(int x:ed){int z=0,k=0;for(int b=U;b;b&=b-1,k++)if(x&(b&-b))z|=1<<k;ee.push_back(z);}
  g^=grundy(ee,m);
 }
 components[comps]++;
 return g;
}
void emit(){
 int n=nverts;
 if(target_n!=-1&&n!=target_n)return;
 patterns[n]++;
 array<int,5> E{};
 int k=0;
 for(int t=1;t<32;t++)for(int j=0;j<cnt[t];j++,k++)for(int i=0;i<5;i++)if(t>>i&1)E[i]|=1<<k;
 assert(k==n);
 for(int i=0;i<5;i++)for(int j=0;j<i;j++)if(E[i]==E[j])return;
 valid[n]++;
 int g=evaluate(E,n);
 hist[n][g]++;
 if(n==12&&g==6&&g6dump.is_open()){for(int t=1;t<32;t++)g6dump<<cnt[t];g6dump<<"\n";}
 if(g>maxg[n]){maxg[n]=g;best_edges[n]=E;}
}
void rec(int t){
 if(t==32){if(remaining[0]||remaining[1]||remaining[2]||remaining[3]||remaining[4])return;emit();return;}
 int kmax=20-nverts;
 for(int i=0;i<5;i++)if(t>>i&1)kmax=min(kmax,remaining[i]);
 for(int k=0;k<=kmax;k++){
  cnt[t]=k;nverts+=k;
  for(int i=0;i<5;i++)if(t>>i&1)remaining[i]-=k;
  rec(t+1);
  for(int i=0;i<5;i++)if(t>>i&1)remaining[i]+=k;
  nverts-=k;
 }
 cnt[t]=0;
}
int main(int argc,char**argv){
 fill(maxg,maxg+21,-1);
 if(argc>1)target_n=atoi(argv[1]);
 if(argc>2)g6dump.open(argv[2]);
 rec(1);
 for(int n=4;n<=20;n++)if(patterns[n]){
  cout<<"n="<<n<<" patterns="<<patterns[n]<<" distinct="<<valid[n]<<" max="<<maxg[n]<<" hist=";
  for(int i=0;i<16;i++)if(hist[n][i])cout<<i<<":"<<hist[n][i]<<",";
  cout<<" witness=";for(int e:best_edges[n])cout<<e<<",";cout<<"\n";
 }
 cerr<<"components:";for(int i=1;i<=5;i++)cerr<<" "<<i<<":"<<components[i];cerr<<"\n";
}
