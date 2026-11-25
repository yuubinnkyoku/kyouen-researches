// Independent exact lifted-determinant audit: 3x5 symmetric columns, q=6.
// g++ -O2 -std=c++17 -Wall -Wextra symmetric_five_columns_q6_independent.cpp -o /tmp/sym5audit
#include <algorithm>
#include <array>
#include <cassert>
#include <climits>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;
using ll = long long;
using i128 = __int128_t;
using Row = array<ll, 4>;

static bool det_zero(array<Row, 4> m) {
    array<array<i128, 4>, 4> a{};
    for (int i=0;i<4;i++) for (int j=0;j<4;j++) a[i][j]=m[i][j];
    i128 prev=1;
    for (int k=0;k<3;k++) {
        int p=k;
        while (p<4 && a[p][k]==0) ++p;
        if (p==4) return true;
        if (p!=k) swap(a[p],a[k]);
        i128 v=a[k][k];
        for (int i=k+1;i<4;i++) for (int j=k+1;j<4;j++) {
            i128 num=a[i][j]*v-a[i][k]*a[k][j];
            assert(num%prev==0);
            a[i][j]=num/prev;
        }
        for (int i=k+1;i<4;i++) a[i][k]=0;
        prev=v;
    }
    return a[3][3]==0;
}

struct Result {int circles, safe, root, maxg; map<int,int> maximal;};
static Result solve(int u,int v,int a,int b) {
    const int xs[5]={-u,-v,0,v,u};
    const int ys[3]={0,a,a+b};
    array<Row,15> rows{};
    for (int j=0;j<3;j++) for (int i=0;i<5;i++) {
        int x=xs[i],y=ys[j];
        rows[j*5+i]={x*x+y*y,x,y,1};
    }
    vector<int> forbidden;
    for (int mask=0;mask<(1<<15);mask++) {
        if (__builtin_popcount((unsigned)mask)!=6) continue;
        int pts[6],idx=0;
        for (int i=0;i<15;i++) if ((mask>>i)&1) pts[idx++]=i;
        bool on_circle=true;
        for (int i=0;i<6 && on_circle;i++) for (int j=i+1;j<6 && on_circle;j++)
        for (int k=j+1;k<6 && on_circle;k++) for (int l=k+1;l<6;l++) {
            if (!det_zero({rows[pts[i]],rows[pts[j]],rows[pts[k]],rows[pts[l]]})) {
                on_circle=false;
                break;
            }
        }
        if (on_circle) forbidden.push_back(mask);
    }
    vector<unsigned char> safe(1<<15,1),grundy(1<<15,0);
    for (int mask=0;mask<(1<<15);mask++)
        for (int e:forbidden) if ((mask&e)==e) {safe[mask]=0;break;}
    int maxg=0; map<int,int> maximal;
    for (int mask=(1<<15)-1;mask>=0;mask--) {
        if (!safe[mask]) continue;
        unsigned seen=0;int legal=0;
        for (int i=0;i<15;i++) if (!(mask>>i&1) && safe[mask|(1<<i)]) {
            seen|=1u<<grundy[mask|(1<<i)];++legal;
        }
        if (!legal) ++maximal[__builtin_popcount((unsigned)mask)];
        while (seen>>grundy[mask]&1u) ++grundy[mask];
        maxg=max(maxg,(int)grundy[mask]);
    }
    return {(int)forbidden.size(),(int)count(safe.begin(),safe.end(),1),grundy[0],maxg,maximal};
}
int main() {
    struct Case {string name;int u,v,a,b,circles,safe,root,maxg;map<int,int> maximal;};
    vector<Case> cases={
        {"generic_off",3,1,1,1,0,32768,1,1,{{15,1}}},
        {"generic_one",3,1,1,7,1,32256,0,1,{{14,6}}},
        {"generic_two",3,1,2,2,2,31776,1,3,{{13,16},{14,2}}},
        {"exceptional_four",2,1,1,1,4,30866,1,5,{{11,1},{12,58},{13,9}}},
        {"generic_ratio_3_2",3,2,1,4,1,32256,0,1,{{14,6}}}
    };
    for (const auto& c:cases) {
        auto r=solve(c.u,c.v,c.a,c.b);
        if (r.circles!=c.circles || r.safe!=c.safe || r.root!=c.root || r.maxg!=c.maxg || r.maximal!=c.maximal) {
            cerr<<"FAIL "<<c.name<<" got "<<r.circles<<","<<r.safe<<","<<r.root<<","<<r.maxg<<"\n";
            return 1;
        }
        cout<<"PASS "<<c.name<<" circles="<<r.circles<<" safe="<<r.safe<<" root="<<r.root<<" maxg="<<r.maxg<<"\n";
    }
    cout<<"PASS all 5 independent determinant/game cases\n";
}
