// Independent six-subset determinant enumeration and full bitmask game.
#include <array>
#include <algorithm>
#include <iostream>
#include <vector>
#include <map>
using namespace std;
struct Point { long long x,y; };
const array<Point,12> p{{{-2,0},{0,0},{1,0},{3,0},{-2,1},{-1,1},{2,1},{3,1},{-3,3},{0,3},{1,3},{4,3}}};
long long det3(long long a,long long b,long long c,long long d,long long e,long long f,long long g,long long h,long long i) {
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g);
}
long long cross(int a,int b,int c) {
    return (p[b].x-p[a].x)*(p[c].y-p[a].y)-(p[b].y-p[a].y)*(p[c].x-p[a].x);
}
long long incircle(int a,int b,int c,int d) {
    auto sq=[](Point q){return q.x*q.x+q.y*q.y;};
    auto A=p[a],B=p[b],C=p[c],D=p[d];
    return det3(B.x-A.x,B.y-A.y,sq(B)-sq(A),
                C.x-A.x,C.y-A.y,sq(C)-sq(A),
                D.x-A.x,D.y-A.y,sq(D)-sq(A));
}
bool forbidden_six(int mask) {
    int ids[6], k=0;
    for(int i=0;i<12;i++) if(mask>>i&1) ids[k++]=i;
    if(k!=6) return false;
    for(int i=0;i<6;i++)for(int j=i+1;j<6;j++)for(int l=j+1;l<6;l++){
        if(!cross(ids[i],ids[j],ids[l])) continue;
        for(int t=0;t<6;t++) if(incircle(ids[i],ids[j],ids[l],ids[t])) goto next_triple;
        return true;
        next_triple:;
    }
    return false;
}
int main() {
    vector<int> f;
    for(int mask=0;mask<(1<<12);mask++) if(__builtin_popcount((unsigned)mask)==6 && forbidden_six(mask))f.push_back(mask);
    if(f.size()!=3) return 2;
    vector<char> safe(1<<12,1);
    for(int mask=0;mask<(1<<12);mask++)for(int rule:f) if((mask&rule)==rule)safe[mask]=0;
    vector<int> g(1<<12,-1);map<int,int> hist, maximal;
    int safe_count=0, winning=0;
    for(int mask=(1<<12)-1;mask>=0;mask--) if(safe[mask]) {
        safe_count++;
        bool seen[13]={};int moves=0;
        for(int i=0;i<12;i++)if(!(mask>>i&1) && safe[mask|(1<<i)]){
            moves++;seen[g[mask|(1<<i)]]=true;
        }
        if(!moves)maximal[__builtin_popcount((unsigned)mask)]++;
        int t=0;while(seen[t])t++;g[mask]=t;hist[t]++;
    }
    for(int i=0;i<12;i++)winning+=(g[1<<i]==0);
    cout<<"six_point_forbidden="<<f.size()<<"\n";
    cout<<"masks=";for(auto x:f)cout<<x<<",";cout<<"\n";
    cout<<"safe_positions="<<safe_count<<"\nempty_grundy="<<g[0]<<"\nwinning_first_moves="<<winning<<"\n";
    cout<<"grundy_histogram=";for(auto [k,v]:hist)cout<<k<<":"<<v<<",";cout<<"\n";
    cout<<"maximal_sizes=";for(auto [k,v]:maximal)cout<<k<<":"<<v<<",";cout<<"\n";
    if(safe_count!=3915 || g[0]!=0 || winning!=0 || maximal[9]!=8 || maximal[10]!=24) return 3;
}
