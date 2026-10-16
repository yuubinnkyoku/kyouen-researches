// Exhaustive exact search for a five-row circle with one lattice point on
// each row.  Run: g++ -O3 -std=c++17 this.cpp -o audit && ./audit 1200 4
// x coordinates on rows 0,1,2 are enumerated in [0,h*(m-1)].
// Rows 3 and 4 are checked on the ENTIRE infinite hZ lattice.
// No floating-point decision is used (sqrtl only seeds corrected isqrt).
#include <bits/stdc++.h>
using namespace std;
using i64=long long;
using i128=__int128_t;
i64 exact_sqrt(i128 n) {
    i64 x=(i64)sqrtl((long double)n);
    while ((i128)(x+1)*(x+1)<=n) ++x;
    while ((i128)x*x>n) --x;
    return x;
}
int main(int argc,char**argv) {
    int m=argc>1?stoi(argv[1]):1200, h=argc>2?stoi(argv[2]):4;
    if(m<1||h<1||m>1200||h>4) {cerr<<"Supported: 1<=m<=1200, 1<=h<=4\n";return 2;}
    long long triples=0, hit3=0;
    for(int a=0;a<m;++a) for(int b=0;b<m;++b) for(int c=0;c<m;++c) {
        i64 x0=(i64)h*a, x1=(i64)h*b, x2=(i64)h*c;
        i64 D=2*(2*x1-x2-x0);
        if(D==0) continue; // first three points are collinear
        i64 r0=x0*x0, r1=x1*x1+1, r2=x2*x2+4;
        i64 X=2*(r1-r0)-(r2-r0);
        i64 Y=(x1-x0)*(r2-r0)-(x2-x0)*(r1-r0);
        i128 R=(i128)(D*x0-X)*(D*x0-X)+(i128)Y*Y;
        auto meets=[&](int y,i64 &xout)->bool {
            i128 dy=(i128)D*y-Y, Q=R-dy*dy;
            if(Q<0) return false;
            i64 root=exact_sqrt(Q);
            if((i128)root*root!=Q) return false;
            for(i64 s:{root,-root}) {
                if((X+s)%D==0 && ((X+s)/D)%h==0) {
                    xout=(X+s)/D;
                    return true;
                }
            }
            return false;
        };
        ++triples;
        i64 x3=0,x4=0;
        if(!meets(3,x3)) continue;
        ++hit3;
        if(!meets(4,x4)) continue;
        cout<<"COUNTEREXAMPLE "<<x0<<" "<<x1<<" "<<x2<<" "<<x3<<" "<<x4<<"\n";
        return 1;
    }
    cout<<"PASS m="<<m<<" h="<<h<<" noncollinear_triples="<<triples
        <<" extend_to_row3="<<hit3<<" extend_to_row4=0\n";
}
