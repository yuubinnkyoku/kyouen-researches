#include <algorithm>
#include <array>
#include <bitset>
#include <cassert>
#include <iostream>
#include <vector>
using namespace std;
struct P{int x,y; bool operator==(const P&b)const{return x==b.x&&y==b.y;}};
using B=bitset<169>;
long long cross(P a,P b,P c){return 1LL*(b.x-a.x)*(c.y-a.y)-1LL*(b.y-a.y)*(c.x-a.x);}
bool four(P a,P b,P c,P p){
 long long ux=b.x-a.x,uy=b.y-a.y,vx=c.x-a.x,vy=c.y-a.y;
 long long det=ux*vy-uy*vx;
 if(det==0)return cross(a,b,p)==0;
 long long U=ux*ux+uy*uy,V=vx*vx+vy*vy;
 long long X=U*vy-V*uy,Y=ux*V-vx*U;
 long long dx=p.x-a.x,dy=p.y-a.y;
 return (dx*dx+dy*dy)*2*det == 2*(dx*X+dy*Y);
}
const vector<P> W={{0,0},{0,4},{1,1},{1,3},{3,1},{3,2},{3,4},{4,1},{4,5},{5,0},{5,2}};
int main(){
 vector<int> edges;
 for(int a=0;a<11;a++)for(int b=a+1;b<11;b++)for(int c=b+1;c<11;c++)for(int d=c+1;d<11;d++)
  if(four(W[a],W[b],W[c],W[d]))edges.push_back((1<<a)|(1<<b)|(1<<c)|(1<<d));
 assert(edges.size()==4);
 vector<int> memo(1<<11,-1);
 auto grundy=[&](auto&& self,int s)->int{
  if(memo[s]!=-1)return memo[s];
  bool seen[12]={};
  for(int i=0;i<11;i++)if(!(s>>i&1)){
   int t=s|(1<<i);bool safe=true;
   for(int e:edges)if((t&e)==e)safe=false;
   if(safe)seen[self(self,t)]=true;
  }
  int v=0;while(seen[v])v++;return memo[s]=v;
 };
 assert(grundy(grundy,0)==5);
 int safe_states=0;
 for(int s=0;s<(1<<11);s++)if(all_of(edges.begin(),edges.end(),[&](int e){return (s&e)!=e;}))safe_states++;
 assert(safe_states==1635);
 cout<<"witness: forbidden="<<edges.size()<<" safe="<<safe_states<<" g="<<memo[0]<<"\n";
 for(int n=6;n<=13;n++){
  vector<P> O,C;
  for(int x=0;x<n;x++)for(int y=0;y<n;y++){
   P p{x,y};if(find(W.begin(),W.end(),p)!=W.end())continue;
   O.push_back(p);
   bool hit=false;
   for(int i=0;i<11;i++)for(int j=i+1;j<11;j++)for(int k=j+1;k<11;k++)if(four(W[i],W[j],W[k],p))hit=true;
   if(!hit)C.push_back(p);
  }
  int z=C.size();
  vector<vector<bool>> pairbad(z,vector<bool>(z));
  vector<char> triplebad(z*z*z);
  vector<B> covers(z*z*z);
  auto idx=[&](int i,int j,int k){return (i*z+j)*z+k;};
  int pc=0,tc=0;
  for(int i=0;i<z;i++)for(int j=i+1;j<z;j++){
   for(int a=0;a<11;a++)for(int b=a+1;b<11;b++)
    if(four(W[a],W[b],C[i],C[j]))pairbad[i][j]=pairbad[j][i]=true;
   if(pairbad[i][j])pc++;
   for(int k=j+1;k<z;k++){
    int t=idx(i,j,k);
    for(auto w:W)if(four(C[i],C[j],C[k],w))triplebad[t]=true;
    if(triplebad[t])tc++;
    for(int p=0;p<(int)O.size();p++)if(!(O[p]==C[i]||O[p]==C[j]||O[p]==C[k]) && four(C[i],C[j],C[k],O[p]))covers[t].set(p);
   }
  }
  unsigned long long states=0;int maxS=0,maxBlock=0;bool success=false;
  vector<int> chosen;
  auto dfs=[&](auto&& self,int start,B blocked,B occupied)->void{
   states++;maxS=max(maxS,(int)chosen.size());maxBlock=max(maxBlock,(int)blocked.count());
   if((blocked|occupied).count()==O.size())success=true;
   for(int i=start;i<z;i++){
    bool valid=true;
    for(int j:chosen)if(pairbad[i][j])valid=false;
    if(!valid)continue;
    B b2=blocked;
    for(int a=0;a<(int)chosen.size();a++)for(int b=a+1;b<(int)chosen.size();b++){
     int t=idx(chosen[a],chosen[b],i);
     if(triplebad[t])valid=false;
     b2|=covers[t];
    }
    if(!valid)continue;
    B occ2=occupied;
    for(int p=0;p<(int)O.size();p++)if(O[p]==C[i]){occ2.set(p);break;}
    chosen.push_back(i);self(self,i+1,b2,occ2);chosen.pop_back();
   }
  };
  dfs(dfs,0,B{},B{});
  cout<<n<<" C="<<z<<" pairs="<<pc<<" triples="<<tc<<" states="<<states<<" maxS="<<maxS<<" maxblocked="<<maxBlock<<" outside="<<O.size()<<" success="<<success<<"\n";
  assert(!success);
 }
}
