// Exhaustive 2-for-2 replacement audit for 7-row q=4 deficient-maximal witnesses.
// Exact integer geometry only. No SAT encoding or search heuristic is used.
#include <bits/stdc++.h>
using namespace std;
struct P { int x, y; };
static constexpr int H=7, N=20;
using Stones = vector<P>;
long long cross(P a,P b,P c){return 1LL*(b.x-a.x)*(c.y-a.y)-1LL*(b.y-a.y)*(c.x-a.x);}
bool forbidden4(P a,P b,P c,P d){
 if(cross(a,b,c)==0&&cross(a,b,d)==0)return true;
 long long ax=b.x-a.x,ay=b.y-a.y,az=1LL*b.x*b.x+1LL*b.y*b.y-1LL*a.x*a.x-1LL*a.y*a.y;
 long long bx=c.x-a.x,by=c.y-a.y,bz=1LL*c.x*c.x+1LL*c.y*c.y-1LL*a.x*a.x-1LL*a.y*a.y;
 long long cx=d.x-a.x,cy=d.y-a.y,cz=1LL*d.x*d.x+1LL*d.y*d.y-1LL*a.x*a.x-1LL*a.y*a.y;
 return ax*(by*cz-bz*cy)-ay*(bx*cz-bz*cx)+az*(bx*cy-by*cx)==0;
}
struct SingleMeta{int total=0,deg[N]={},deg2[N][N]={};};
struct PairMeta{int total=0,deg[N]={};unsigned char bad[N][N]={};};
struct Result{string name;int width=0,empty=0;long long row_capacity_candidates=0,safe_candidates=0,safe_maximal=0;vector<Stones>witnesses;};
Result run_case(const string&name,int width,const Stones&base){
 if((int)base.size()!=N)throw runtime_error("base size");
 bool occupied[H][100]={};int base_rows[H]={};
 for(auto p:base){if(p.x<0||p.x>=width||p.y<0||p.y>=H||occupied[p.y][p.x])throw runtime_error("invalid base");occupied[p.y][p.x]=true;base_rows[p.y]++;}
 for(int y=0;y<H;y++)if(base_rows[y]>3)throw runtime_error("row capacity");
 for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int d=c+1;d<N;d++)if(forbidden4(base[a],base[b],base[c],base[d]))throw runtime_error("unsafe base");
 vector<P>cells;for(int y=0;y<H;y++)for(int x=0;x<width;x++)if(!occupied[y][x])cells.push_back({x,y});
 int C=cells.size();vector<array<int,3>>triples;vector<array<int,2>>oldpairs;
 for(int i=0;i<N;i++)for(int j=i+1;j<N;j++){oldpairs.push_back({i,j});for(int k=j+1;k<N;k++)triples.push_back({i,j,k});}
 vector<SingleMeta>one(C);
 for(int pi=0;pi<C;pi++){auto&z=one[pi];for(auto t:triples)if(forbidden4(cells[pi],base[t[0]],base[t[1]],base[t[2]])){z.total++;for(int i:t)z.deg[i]++;z.deg2[t[0]][t[1]]++;z.deg2[t[0]][t[2]]++;z.deg2[t[1]][t[2]]++;}}
 vector<PairMeta>two((size_t)C*C);
 auto pm=[&](int p,int q)->PairMeta&{if(p>q)swap(p,q);return two[(size_t)p*C+q];};
 for(int pi=0;pi<C;pi++)for(int qi=pi+1;qi<C;qi++){auto&z=pm(pi,qi);for(auto ij:oldpairs)if(forbidden4(cells[pi],cells[qi],base[ij[0]],base[ij[1]])){z.total++;z.deg[ij[0]]++;z.deg[ij[1]]++;z.bad[ij[0]][ij[1]]=z.bad[ij[1]][ij[0]]=1;}}
 Result out;out.name=name;out.width=width;out.empty=C;
 for(int ri=0;ri<N;ri++)for(int rj=ri+1;rj<N;rj++){
  int rc[H];copy(base_rows,base_rows+H,rc);rc[base[ri].y]--;rc[base[rj].y]--;
  vector<int>avail;for(int pi=0;pi<C;pi++)if(rc[cells[pi].y]<3)avail.push_back(pi);
  for(size_t aa=0;aa<avail.size();aa++)for(size_t bb=aa+1;bb<avail.size();bb++){
   int pi=avail[aa],qi=avail[bb];P p=cells[pi],q=cells[qi];if(p.y==q.y&&rc[p.y]>1)continue;out.row_capacity_candidates++;
   auto single_ok=[&](int z){const auto&v=one[z];return v.total-v.deg[ri]-v.deg[rj]+v.deg2[ri][rj]==0;};
   if(!single_ok(pi)||!single_ok(qi))continue;
   const auto&v=pm(pi,qi);if(v.total-v.deg[ri]-v.deg[rj]+(v.bad[ri][rj]?1:0)!=0)continue;out.safe_candidates++;
   Stones cand;for(int k=0;k<N;k++)if(k!=ri&&k!=rj)cand.push_back(base[k]);cand.push_back(p);cand.push_back(q);
   int counts[H]={};for(auto z:cand)counts[z.y]++;int deficient=-1;bool shape=true;
   for(int y=0;y<H;y++){if(counts[y]>3)shape=false;if(counts[y]==2){if(deficient!=-1)shape=false;deficient=y;}else if(counts[y]!=3)shape=false;}
   if(!shape||deficient<0)throw runtime_error("capacity invariant");
   bool maximal=true;
   for(int x=0;x<width&&maximal;x++){P point{x,deficient};if(find_if(cand.begin(),cand.end(),[&](P z){return z.x==x&&z.y==deficient;})!=cand.end())continue;bool blocked=false;
    for(int a=0;a<N&&!blocked;a++)for(int b=a+1;b<N&&!blocked;b++)for(int c=b+1;c<N&&!blocked;c++)if(forbidden4(point,cand[a],cand[b],cand[c]))blocked=true;
    if(!blocked)maximal=false;
   }
   if(maximal){out.safe_maximal++;if(out.witnesses.size()<8)out.witnesses.push_back(cand);}
  }
 }
 return out;
}
void print_result(const Result&r){
 cout<<"{\"name\":\""<<r.name<<"\",\"width\":"<<r.width<<",\"empty_cells\":"<<r.empty<<",\"row_capacity_candidates\":"<<r.row_capacity_candidates<<",\"safe_candidates\":"<<r.safe_candidates<<",\"safe_maximal_row_deficient\":"<<r.safe_maximal<<",\"witnesses\":[";
 for(size_t i=0;i<r.witnesses.size();i++){if(i)cout<<",";cout<<"[";for(size_t j=0;j<r.witnesses[i].size();j++){if(j)cout<<",";cout<<"["<<r.witnesses[i][j].x<<","<<r.witnesses[i][j].y<<"]";}cout<<"]";}cout<<"]}";
}
int main(){
 Stones base53={{21,0},{23,0},{26,0},{18,1},{27,1},{39,1},{14,2},{28,2},{46,2},{25,3},{30,3},{39,3},{18,4},{36,4},{43,4},{13,5},{27,5},{35,5},{14,6},{42,6}};
 Stones foundB={{21,0},{23,0},{26,0},{18,1},{27,1},{39,1},{14,2},{46,2},{25,3},{30,3},{39,3},{18,4},{43,4},{13,5},{27,5},{35,5},{14,6},{42,6},{56,2},{7,4}};
 vector<Result>r={run_case("base53_on_7x57",57,base53),run_case("base53_on_7x60",60,base53),run_case("foundB_on_7x60",60,foundB)};
 cout<<"{\"scope\":\"complete 2-for-2 replacement neighborhoods of the stated base witnesses, with every final row capacity <=3\",\"results\":[";
 for(size_t i=0;i<r.size();i++){if(i)cout<<",";print_result(r[i]);}cout<<"]}\n";
}