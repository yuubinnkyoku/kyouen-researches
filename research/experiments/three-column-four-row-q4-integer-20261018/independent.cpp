// Independent 4x4 determinant and subset-DP audit, no use of coefficient classes.
#include <array>
#include <cassert>
#include <iostream>
#include <vector>
#include <cstdint>
using namespace std;
struct P { long long x,y; };
long long determinant(const array<P,12>& p,int a,int b,int c,int d){
    const auto &p0=p[a];
    long long v[3][3];
    int ids[]={b,c,d};
    for(int i=0;i<3;i++){
        const auto &q=p[ids[i]];
        v[i][0]=q.x-p0.x;
        v[i][1]=q.y-p0.y;
        v[i][2]=q.x*q.x+q.y*q.y-p0.x*p0.x-p0.y*p0.y;
    }
    return v[0][0]*(v[1][1]*v[2][2]-v[1][2]*v[2][1])
          -v[0][1]*(v[1][0]*v[2][2]-v[1][2]*v[2][0])
          +v[0][2]*(v[1][0]*v[2][1]-v[1][1]*v[2][0]);
}
pair<int,int> solve(int a,int b,int d){
    array<P,12> p;
    long long xs[]={0,a,a+b};
    for(int i=0;i<3;i++)for(int j=0;j<4;j++)p[4*i+j]={xs[i],j*d};
    vector<int> forbidden;
    for(int i=0;i<12;i++)for(int j=i+1;j<12;j++)
    for(int k=j+1;k<12;k++)for(int l=k+1;l<12;l++)
        if(determinant(p,i,j,k,l)==0)forbidden.push_back((1<<i)|(1<<j)|(1<<k)|(1<<l));
    array<vector<int>,12> bypoint;
    for(int f:forbidden)for(int i=0;i<12;i++)if(f>>i&1)bypoint[i].push_back(f);
    array<unsigned char,4096> safe{};
    safe[0]=1;
    for(int s=1;s<4096;s++){
        int bit=s&-s,idx=__builtin_ctz((unsigned)bit);
        if(!safe[s^bit])continue;
        safe[s]=1;
        for(int f:bypoint[idx])if((s&f)==f){safe[s]=0;break;}
    }
    array<int,4096> grundy{};
    grundy.fill(-1);
    for(int s=4095;s>=0;s--){
        if(!safe[s])continue;
        unsigned options=0;
        for(int i=0;i<12;i++)if(!(s>>i&1)&&safe[s|(1<<i)])options|=1u<<grundy[s|(1<<i)];
        int g=0;
        while(options>>g&1u)g++;
        grundy[s]=g;
    }
    int firstwin=0;
    for(int i=0;i<12;i++)firstwin+=(grundy[1<<i]==0);
    return {grundy[0],firstwin};
}
int main(){
    int checked=0,positive=0;
    for(int a=1;a<=16;a++)for(int b=1;b<=16;b++)for(int d=1;d<=16;d++){
        auto [g,win]=solve(a,b,d);
        bool expected=(a==d&&b==d)||(a==d&&b==2*d)||(a==2*d&&b==d);
        if(g!=(expected?2:0)||win!=(expected?((a==b)?6:4):0)){
            cerr<<"FAIL "<<a<<" "<<b<<" "<<d<<" g="<<g<<" wins="<<win<<"\n";
            return 1;
        }
        checked++;positive+=expected;
    }
    cout<<"PASS exhaustive 1<=a,b,d<=16: "<<checked<<" boards, "<<positive<<" first-player-win boards\n";
    return 0;
}
