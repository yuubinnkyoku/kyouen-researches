#include <bits/stdc++.h>
using namespace std;
struct Pt{int x,y;};
struct Curve{long long a,b,c,d;int type;uint64_t mask;int cnt;};
long long ab(long long x){return x<0?-x:x;}
long long g4(long long a,long long b,long long c,long long d){return gcd(gcd(ab(a),ab(b)),gcd(ab(c),ab(d)));}
string key(const Curve&c){return to_string(c.type)+":"+to_string(c.a)+","+to_string(c.b)+","+to_string(c.c)+","+to_string(c.d);}
Curve makeC(Pt p,Pt q,Pt r){
 long long A=q.x-p.x,B=q.y-p.y,C=r.x-p.x,D=r.y-p.y,det=A*D-C*B;
 if(!det){long long a=q.y-p.y,b=p.x-q.x,c=-a*p.x-b*p.y,g=gcd(gcd(ab(a),ab(b)),ab(c));if(!g)g=1;a/=g;b/=g;c/=g;if(a<0||(a==0&&b<0))a=-a,b=-b,c=-c;return {a,b,c,0,0,0,0};}
 long long R1=q.x*q.x+q.y*q.y-p.x*p.x-p.y*p.y,R2=r.x*r.x+r.y*r.y-p.x*p.x-p.y*p.y;
 long long d1=-R1*D+R2*B,d2=-A*R2+C*R1,d3=-det*(p.x*p.x+p.y*p.y)-d1*p.x-d2*p.y;
 long long g=g4(det,d1,d2,d3);if(!g)g=1;det/=g;d1/=g;d2/=g;d3/=g;
 if(det<0)det=-det,d1=-d1,d2=-d2,d3=-d3;
 return {det,d1,d2,d3,1,0,0};
}
bool on(const Curve&c,Pt p){return c.type==0?c.a*p.x+c.b*p.y+c.c==0:c.a*(p.x*p.x+p.y*p.y)+c.b*p.x+c.c*p.y+c.d==0;}
int main(){
 vector<Pt>S={{9,0},{14,0},{19,0},{20,0},{21,0},{2,1},{8,1},{10,1},{13,1},{22,1},{7,2},{10,2},{13,2},{19,2},{22,2},{3,3},{8,3},{11,3},{27,3},{1,4},{5,4},{7,4},{8,4},{14,4},{4,5},{6,5},{19,5},{20,5},{25,5},{7,6},{8,6},{11,6},{17,6},{22,6}};
 const int N=S.size(),W=30,H=7;vector<Pt>cells;for(int y=0;y<H;y++)for(int x=0;x<W;x++)cells.push_back({x,y});
 int stoneAt[210];fill(stoneAt,stoneAt+210,-1);for(int i=0;i<N;i++)stoneAt[S[i].y*W+S[i].x]=i;
 unordered_map<string,int>ids;vector<Curve>cs;
 for(int i=0;i<N;i++)for(int j=i+1;j<N;j++)for(int k=j+1;k<N;k++){Curve c=makeC(S[i],S[j],S[k]);string z=key(c);auto it=ids.find(z);int id;if(it==ids.end()){id=cs.size();ids[z]=id;cs.push_back(c);}else id=it->second;cs[id].mask|=(1ULL<<i)|(1ULL<<j)|(1ULL<<k);}
 for(auto&c:cs){for(int i=0;i<N;i++)if(on(c,S[i]))c.mask|=1ULL<<i;c.cnt=__builtin_popcountll(c.mask);}
 vector<int>crit;vector<vector<int>>through(210),blockers(210);
 for(int i=0;i<(int)cs.size();i++){if(cs[i].cnt>=4)crit.push_back(i);if(cs[i].cnt>=3)for(int p=0;p<210;p++)if(on(cs[i],cells[p])){through[p].push_back(i);if(cs[i].cnt>=5)blockers[p].push_back(i);}}
 vector<Pt>lineAdd,offAdd,lineStones,offStones;
 for(Pt p:cells)if(stoneAt[p.y*W+p.x]<0){if(p.y==3&&p.x!=29)lineAdd.push_back(p);if(p.y!=3)offAdd.push_back(p);}
 for(Pt p:S)(p.y==3?lineStones:offStones).push_back(p);
 long long candA=0,safeA=0,maxA=0,candB=0,safeB=0,maxB=0;
 auto test=[&](Pt a,Pt b,int r1,int r2,long long&safe,long long&maximal){
  uint64_t rm=(1ULL<<r1)|(1ULL<<r2);
  for(int id:crit){const auto&c=cs[id];int n=c.cnt-__builtin_popcountll(c.mask&rm)+(on(c,a)?1:0)+(on(c,b)?1:0);if(n>5)return;}
  safe++;
  for(int p=0;p<210;p++){Pt z=cells[p];int si=stoneAt[p];bool added=(z.x==a.x&&z.y==a.y)||(z.x==b.x&&z.y==b.y);bool retained=si>=0&&!(rm>>si&1ULL);if(added||retained)continue;
   bool covered=false;
   for(int id:blockers[p]){const auto&c=cs[id];int n=5-__builtin_popcountll(c.mask&rm)+(on(c,a)?1:0)+(on(c,b)?1:0);if(n>=5){covered=true;break;}}
   if(!covered)for(int id:through[p]){const auto&c=cs[id];int n=c.cnt-__builtin_popcountll(c.mask&rm)+(on(c,a)?1:0)+(on(c,b)?1:0);if(n>=5){covered=true;break;}}
   if(!covered)return;
  }
  maximal++;
 };
 for(int i=0;i<(int)offStones.size();i++)for(int j=i+1;j<(int)offStones.size();j++){
  int r1=find_if(S.begin(),S.end(),[&](Pt p){return p.x==offStones[i].x&&p.y==offStones[i].y;})-S.begin();
  int r2=find_if(S.begin(),S.end(),[&](Pt p){return p.x==offStones[j].x&&p.y==offStones[j].y;})-S.begin();
  for(Pt a:lineAdd)for(Pt b:offAdd){candA++;test(a,b,r1,r2,safeA,maxA);}
 }
 for(Pt rl:lineStones)for(Pt ro:offStones){
  int r1=find_if(S.begin(),S.end(),[&](Pt p){return p.x==rl.x&&p.y==rl.y;})-S.begin();
  int r2=find_if(S.begin(),S.end(),[&](Pt p){return p.x==ro.x&&p.y==ro.y;})-S.begin();
  for(int i=0;i<(int)lineAdd.size();i++)for(int j=i+1;j<(int)lineAdd.size();j++){candB++;test(lineAdd[i],lineAdd[j],r1,r2,safeB,maxB);}
 }
 cout<<"{\"curves\":"<<cs.size()<<",\"critical\":"<<crit.size()
     <<",\"gapA\":{\"candidates\":"<<candA<<",\"safe\":"<<safeA<<",\"maximal\":"<<maxA<<"}"
     <<",\"gapB\":{\"candidates\":"<<candB<<",\"safe\":"<<safeB<<",\"maximal\":"<<maxB<<"}"
     <<",\"candidateTotal\":"<<candA+candB<<",\"safeTotal\":"<<safeA+safeB
     <<",\"maximalTotal\":"<<maxA+maxB<<",\"found\":[]}\n";
}
