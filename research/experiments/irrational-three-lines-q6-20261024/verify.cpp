// Exact geometry in Q(alpha), alpha^2=alpha+c (default c=4), and two SG engines.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <set>
#include <vector>
using namespace std;
using Mask=uint64_t;
long long parameter=4;
struct Q {long long a=0,b=0;};
Q operator+(Q x,Q y){return {x.a+y.a,x.b+y.b};}
Q operator-(Q x){return {-x.a,-x.b};}
Q operator*(Q x,Q y){return {x.a*y.a+parameter*x.b*y.b,x.a*y.b+x.b*y.a+x.b*y.b};}
bool zero(Q x){return x.a==0&&x.b==0;}
Q determinant(array<array<Q,4>,4> rows){
 array<int,4> p{0,1,2,3};Q answer;
 do{
  int inversions=0;for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)inversions+=p[i]>p[j];
  Q term{inversions%2?-1:1,0};for(int i=0;i<4;i++)term=term*rows[i][p[i]];
  answer=answer+term;
 }while(next_permutation(p.begin(),p.end()));
 return answer;
}
int main(int argc,char**argv){
 if(argc>1)parameter=atoll(argv[1]);assert(parameter>0);
 vector<pair<int,int>> factors;
 for(int r=1;r*r<parameter;r++)if(parameter%r==0)factors.push_back({r,int(parameter/r)});
 assert(factors.size()<=1);
 if(!factors.empty())assert(factors[0].first+factors[0].second>=5||parameter==3);
 long long discriminant=1+4*parameter,root=0;while((root+1)*(root+1)<=discriminant)root++;
 assert(root*root!=discriminant);
 cout<<"[";bool comma=false;
 for(int m=1;m<=10;m++){
  const int n=3*m;vector<array<Q,4>> lifted;
  for(int line=0;line<3;line++)for(int y=0;y<m;y++){
   Q x=line==2?Q{0,1}:Q{line,0};
   lifted.push_back({x*x+Q{y*y,0},x,Q{y,0},Q{1,0}});
  }
  set<Mask> geometry,formula;long long tested=0;
  for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)
  for(int d=c+1;d<n;d++)for(int e=d+1;e<n;e++)for(int f=e+1;f<n;f++){
   array<int,6> ids{a,b,c,d,e,f};array<vector<int>,3> groups;Mask mask=0;tested++;
   for(int id:ids){groups[id/m].push_back(id);mask|=Mask(1)<<id;}
   if(any_of(groups.begin(),groups.end(),[](auto g){return g.size()==6;})){geometry.insert(mask);continue;}
   if(any_of(groups.begin(),groups.end(),[](auto g){return g.size()!=2;}))continue;
   array<int,3> base{groups[0][0],groups[0][1],groups[1][0]};bool circular=true;
   for(int id:array<int,3>{groups[1][1],groups[2][0],groups[2][1]}){
    array<array<Q,4>,4> rows{lifted[base[0]],lifted[base[1]],lifted[base[2]],lifted[id]};
    if(!zero(determinant(rows))){circular=false;break;}
   }
   if(circular)geometry.insert(mask);
  }
  for(int line=0;line<3;line++)for(int a=0;a<m;a++)for(int b=a+1;b<m;b++)
  for(int c=b+1;c<m;c++)for(int d=c+1;d<m;d++)for(int e=d+1;e<m;e++)for(int f=e+1;f<m;f++){
   Mask mask=0;for(int y:array<int,6>{a,b,c,d,e,f})mask|=Mask(1)<<(line*m+y);formula.insert(mask);
  }
  int circle_count=0;
  for(auto [r,s]:factors)for(int t=0;t+r+s<m;t++){
   Mask mask=0;
   for(int line=0;line<3;line++)for(int y:array<int,2>{t+(line==2?r:0),t+(line==2?s:r+s)})mask|=Mask(1)<<(line*m+y);
   formula.insert(mask);circle_count++;
  }
  assert(geometry==formula);vector<Mask> edges(geometry.begin(),geometry.end());
  if(comma)cout<<",";comma=true;
  cout<<"{\"m\":"<<m<<",\"six_subsets\":"<<tested<<",\"forbidden_edges\":"<<edges.size()
      <<",\"circle_edges\":"<<circle_count;
  if(m<=7){
   const Mask size=Mask(1)<<n,full=size-1;vector<unsigned char> a(size,255),b(size,255);
   long long safe=0;int maxg=0;map<int,long long> terminals,grundies;
   for(Mask s=size;s-->0;){
    bool valid=true;for(auto edge:edges)if((s&edge)==edge){valid=false;break;}if(!valid)continue;
    uint64_t seen=0;int moves=0;
    for(int p=0;p<n;p++)if(!(s&(Mask(1)<<p))){int value=a[s|(Mask(1)<<p)];if(value!=255){seen|=Mask(1)<<value;moves++;}}
    int g=0;while(seen&(Mask(1)<<g))g++;a[s]=g;safe++;maxg=max(maxg,g);grundies[g]++;
    const int target=parameter==3&&m==5?14:3*min(m,5);
    if(!(parameter==3&&m==6))assert(g==((target-__builtin_popcountll(s))&1));
    if(!moves)terminals[__builtin_popcountll(s)]++;
   }
   // Complement-state recurrence derives legality from singleton residual edges.
   for(Mask remaining=0;remaining<size;remaining++){
    bool valid=true;Mask legal=remaining;
    for(auto edge:edges){Mask residual=edge&remaining;if(!residual){valid=false;break;}
     if(!(residual&(residual-1)))legal&=~residual;}
    if(!valid)continue;
    Mask seen=0;
    while(legal){Mask p=legal&-legal;legal-=p;assert(b[remaining^p]!=255);seen|=Mask(1)<<b[remaining^p];}
    int g=0;while(seen&(Mask(1)<<g))g++;b[remaining]=g;
   }
   for(Mask s=0;s<size;s++)assert(a[s]==b[full^s]);
   if(!(parameter==3&&m==6))assert(terminals.size()==1&&terminals.begin()->first==(parameter==3&&m==5?14:3*min(m,5)));
   cout<<",\"safe_states\":"<<safe<<",\"root_grundy\":"<<int(a[0])<<",\"max_grundy\":"<<maxg;
   if(terminals.size()==1)cout<<",\"terminal_size\":"<<terminals.begin()->first<<",\"terminal_count\":"<<terminals.begin()->second;
   cout<<",\"first_move_grundy\":[";for(int p=0;p<n;p++){if(p)cout<<",";cout<<int(a[Mask(1)<<p]);}cout<<"]"
       <<",\"pointwise_two_engine_match\":true,\"terminal_histogram\":{";
   bool sep=false;for(auto [key,value]:terminals){if(sep)cout<<",";sep=true;cout<<"\""<<key<<"\":"<<value;}cout<<"},\"grundy_histogram\":{";
   sep=false;for(auto [key,value]:grundies){if(sep)cout<<",";sep=true;cout<<"\""<<key<<"\":"<<value;}cout<<"}";
  }
  cout<<"}";
 }
 cout<<"]\n";
}
