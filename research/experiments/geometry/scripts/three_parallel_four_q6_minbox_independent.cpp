// Independent auditor: enumerate every 2+2+2 tuple on the *whole rectangle*,
// use integer 4-point circle determinants, then count contained circles for each board.
// Does not use pair sums, products or interpolation.
#include <array>
#include <iostream>
#include <vector>
using namespace std;
struct P{int x,y;};
long long det(P a,P b,P c,P d){
    auto row=[&](P q){return array<long long,3>{q.x-a.x,q.y-a.y,q.x*q.x+q.y*q.y-a.x*a.x-a.y*a.y};};
    auto u=row(b),v=row(c),w=row(d);
    return u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0]);
}
struct Circle{int m0,m1,m2;};
vector<int> fours(int W){vector<int> v;for(int a=0;a<W;a++)for(int b=a+1;b<W;b++)for(int c=b+1;c<W;c++)for(int d=c+1;d<W;d++)v.push_back((1<<a)|(1<<b)|(1<<c)|(1<<d));return v;}
vector<Circle> all_circles(int W,int y0,int y1,int y2){
    vector<Circle> v;
    for(int a=0;a<W;a++)for(int b=a+1;b<W;b++)
    for(int c=0;c<W;c++)for(int d=c+1;d<W;d++)
    for(int e=0;e<W;e++)for(int f=e+1;f<W;f++){
        P p0{a,y0},p1{b,y0},p2{c,y1};
        if(det(p0,p1,p2,{d,y1})||det(p0,p1,p2,{e,y2})||det(p0,p1,p2,{f,y2}))continue;
        v.push_back({(1<<a)|(1<<b),(1<<c)|(1<<d),(1<<e)|(1<<f)});
    }
    return v;
}
void run(int W,int H){
    auto v=fours(W);long long hist[4]={},total=0;
    for(int y0=0;y0<H;y0++)for(int y1=y0+1;y1<H;y1++)for(int y2=y1+1;y2<H;y2++){
      auto cs=all_circles(W,y0,y1,y2);
      for(int A:v)for(int B:v)for(int C:v){
        int cnt=0;
        for(auto z:cs)if((A&z.m0)==z.m0&&(B&z.m1)==z.m1&&(C&z.m2)==z.m2)cnt++;
        if(cnt>3){cerr<<"BAD "<<cnt<<"\n";exit(2);}
        ++hist[cnt];++total;
        if(cnt==3){
            cout<<"WITNESS "<<W<<' '<<H<<" y="<<y0<<','<<y1<<','<<y2<<" x=";
            for(int mask:{A,B,C}){cout<<'[';for(int x=0;x<W;x++)if(mask>>x&1)cout<<x<<',';cout<<']';}cout<<'\n';
        }
      }
    }
    cout<<"RESULT "<<W<<' '<<H<<" total="<<total<<" c0="<<hist[0]<<" c1="<<hist[1]<<" c2="<<hist[2]<<" c3="<<hist[3]<<'\n';
}
int main(){for(auto [W,H]:{pair<int,int>{9,3},{6,4},{5,5},{4,7},{7,4}})run(W,H);}
