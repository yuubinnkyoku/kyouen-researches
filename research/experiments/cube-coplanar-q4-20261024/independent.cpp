// Independent direct 4x4 affine determinant and descending mask recursion.
#include <array>
#include <algorithm>
#include <cassert>
#include <iostream>
using namespace std;
using Point = array<int,3>;
static int det(Point a, Point b, Point c) {
    return a[0]*(b[1]*c[2]-b[2]*c[1])
         - a[1]*(b[0]*c[2]-b[2]*c[0])
         + a[2]*(b[0]*c[1]-b[1]*c[0]);
}
static int mex(int bits) { int k=0; while (bits & (1<<k)) ++k; return k; }
int main() {
    Point p[8];
    for(int i=0;i<8;i++) p[i]={i&1,(i>>1)&1,(i>>2)&1};
    bool bad4[256]={}, safe[256]={};
    int forbidden=0;
    for(int a=0;a<8;a++)for(int b=a+1;b<8;b++)
    for(int c=b+1;c<8;c++)for(int d=c+1;d<8;d++) {
        Point u,v,w;
        for(int j=0;j<3;j++) {
            u[j]=p[b][j]-p[a][j];
            v[j]=p[c][j]-p[a][j];
            w[j]=p[d][j]-p[a][j];
        }
        int mask=(1<<a)|(1<<b)|(1<<c)|(1<<d);
        if(det(u,v,w)==0) {bad4[mask]=true; ++forbidden;}
    }
    int g[256]={},h[256]={}, layer[6]={}, mx[6]={};
    int ng[6][4]={},nh[6][4]={};
    int safeCount=0, swapMismatch=0;
    for(int s=255;s>=0;s--) {
        bool valid=true;
        for(int f=0;f<256;f++) if(bad4[f] && (s&f)==f) valid=false;
        safe[s]=valid;
        if(!valid) continue;
        ++safeCount;
        int cg=0,ch=0,nchild=0;
        for(int i=0;i<8;i++) if(!(s&(1<<i)) && safe[s|(1<<i)]) {
            cg |= 1<<g[s|(1<<i)]; ch |= 1<<h[s|(1<<i)]; ++nchild;
        }
        g[s]=mex(cg); h[s]=nchild?mex(ch):1;
        int k=__builtin_popcount((unsigned)s);
        assert(k<=5);
        ++layer[k]; ++ng[k][g[s]]; ++nh[k][h[s]];
        if(!nchild) ++mx[k];
        if(h[s]!=(g[s]<2?1-g[s]:g[s])) ++swapMismatch;
    }
    assert(forbidden==12 && safeCount==159 && mx[4]==24 && mx[5]==8);
    assert(g[0]==0 && h[0]==0 && swapMismatch==25);
    for(int i=0;i<8;i++) assert(g[1<<i]==2);
    cout<<"forbidden="<<forbidden<<" safe="<<safeCount
        <<" normal_empty="<<g[0]<<" misere_empty="<<h[0]
        <<" swap_mismatches="<<swapMismatch<<"\n";
    for(int k=0;k<=5;k++) {
        cout<<"size="<<k<<" safe="<<layer[k]<<" maximal="<<mx[k]<<" g=";
        for(int j=0;j<4;j++) cout<<ng[k][j]<<(j==3?' ':',');
        cout<<"h=";
        for(int j=0;j<4;j++) cout<<nh[k][j]<<(j==3?'\n':',');
    }
}
