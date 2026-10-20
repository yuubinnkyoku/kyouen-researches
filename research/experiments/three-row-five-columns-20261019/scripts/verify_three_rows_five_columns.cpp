// Independent integer-circle audit. Compile: g++ -O2 -std=c++17 ...
#include <array>
#include <algorithm>
#include <cassert>
#include <iostream>
#include <map>
#include <vector>
using namespace std;

int count_circles(const array<int,5>& x, int a, int b) {
    int ys[3] = {0, a, a+b};
    int count = 0;
    // Every 6-point circle contains exactly two points in each of three rows.
    for(int i=0;i<5;i++) for(int j=i+1;j<5;j++) {
      const long long s = x[i]+x[j], c = 1LL*x[i]*x[j];
      for(int k=0;k<5;k++) for(int l=k+1;l<5;l++) {
        // The circle equation is a*(x^2+y^2-s*x+c)+n*y=0.
        const long long n = s*x[k]-1LL*x[k]*x[k]-1LL*a*a-c;
        auto on = [&](int xx, int yy) -> bool {
            return 1LL*a*(1LL*xx*xx+1LL*yy*yy-s*xx+c)+n*yy == 0;
        };
        if(!on(x[l],ys[1])) continue;
        for(int p=0;p<5;p++) for(int q=p+1;q<5;q++) {
            if(on(x[p],ys[2]) && on(x[q],ys[2])) ++count;
        }
      }
    }
    return count;
}
int main(){
    map<int,long long> hist;
    long long total=0, fours=0, threes=0;
    for(int x0=0;x0<11;x0++) for(int x1=x0+1;x1<11;x1++)
    for(int x2=x1+1;x2<11;x2++) for(int x3=x2+1;x3<11;x3++)
    for(int x4=x3+1;x4<11;x4++) {
      array<int,5> xs{x0,x1,x2,x3,x4};
      bool ap=(x1-x0==x2-x1 && x2-x1==x3-x2 && x3-x2==x4-x3);
      for(int a=1;a<=7;a++) for(int b=1;b<=7;b++) {
        int cnt=count_circles(xs,a,b);
        assert(cnt<=4);
        if(cnt==4){assert(ap && a==b && a==x1-x0); ++fours;}
        if(cnt==3)++threes;
        ++hist[cnt];++total;
      }
    }
    cout << "total " << total << " four " << fours << " three " << threes << " histogram";
    for(auto [k,v]:hist) cout << " " << k << ":" << v;
    cout << '\n';
    assert(total==22638 && fours==10 && threes==20);
}
