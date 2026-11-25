// Exact forbidden-four overlap histogram by incidence moments.
// g++ -O3 -std=c++17 forbidden_overlap_moments.cpp -o forbidden_overlap_moments
// ./forbidden_overlap_moments 11
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;
using ll=long long;
struct P{ll x,y;};
ll c2(ll a){return a*(a-1)/2;}
ll det(const P &p,const P &q,const P &r,const P &s){
    ll x1=q.x-p.x,y1=q.y-p.y,z1=x1*x1+y1*y1;
    ll x2=r.x-p.x,y2=r.y-p.y,z2=x2*x2+y2*y2;
    ll x3=s.x-p.x,y3=s.y-p.y,z3=x3*x3+y3*y3;
    return z1*(x2*y3-y2*x3)+z2*(x3*y1-y3*x1)+z3*(x1*y2-y1*x2);
}
int main(int argc,char **argv){
    int n=argc>1?atoi(argv[1]):11;
    if(n<2 || n>25){cerr<<"n must be 2..25\n";return 2;}
    int N=n*n;
    vector<P> p; for(int y=0;y<n;y++)for(int x=0;x<n;x++)p.push_back({x,y});
    vector<ll> one(N),two((size_t)N*N),three((size_t)N*N*N);
    auto ti=[N](int a,int b,int c)->size_t{return ((size_t)a*N+b)*N+c;};
    ll F=0, lines=0,circles=0;
    for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int d=c+1;d<N;d++){
        if(det(p[a],p[b],p[c],p[d]))continue;
        F++;
        bool line=(p[b].x-p[a].x)*(p[c].y-p[a].y)==(p[b].y-p[a].y)*(p[c].x-p[a].x);
        if(line)lines++;else circles++;
        int v[4]={a,b,c,d};
        for(int i=0;i<4;i++)one[v[i]]++;
        for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)two[(size_t)v[i]*N+v[j]]++;
        for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)for(int k=j+1;k<4;k++)three[ti(v[i],v[j],v[k])]++;
    }
    ll M0=c2(F),M1=0,M2=0,M3=0;
    for(ll x:one)M1+=c2(x);
    for(ll x:two)M2+=c2(x);
    for(ll x:three)M3+=c2(x);
    ll O3=M3,O2=M2-3*M3,O1=M1-2*M2+3*M3,O0=M0-M1+M2-M3;
    cout<<"{\"n\":"<<n<<",\"forbidden\":"<<F<<",\"collinear\":"<<lines<<",\"cocircular\":"<<circles
        <<",\"moments\":["<<M0<<","<<M1<<","<<M2<<","<<M3<<"],\"intersection_histogram\":["
        <<O0<<","<<O1<<","<<O2<<","<<O3<<"]}\n";
    if(O0<0||O1<0||O2<0||O3<0||O0+O1+O2+O3!=M0){return 3;}
}
