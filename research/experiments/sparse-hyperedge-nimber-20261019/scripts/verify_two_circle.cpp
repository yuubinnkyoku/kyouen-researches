// Independent exact 4x4 determinant and subset-mex check.
// Build: c++ -std=c++17 -O2 -Wall -Wextra -pedantic verify_two_circle.cpp -o verify_two_circle
#include <array>
#include <algorithm>
#include <cassert>
#include <iostream>
#include <map>
#include <vector>
using namespace std;
using P = pair<long long,long long>;
const array<P,7> pts = {{{3,4},{-5,0},{-4,-3},{-4,3},{1,0},{2,-3},{6,-5}}};
long long det3(array<array<long long,3>,3> a) {
    return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
          -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
          +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]);
}
long long det4(array<int,4> indices) {
    array<array<long long,4>,4> m{};
    for(int i=0;i<4;++i) {
        auto [x,y]=pts[indices[i]];
        m[i]={x*x+y*y,x,y,1};
    }
    long long answer=0;
    for(int j=0;j<4;++j) {
        array<array<long long,3>,3> sub{};
        for(int i=1;i<4;++i) for(int k=0,t=0;k<4;++k) if(k!=j) sub[i-1][t++]=m[i][k];
        answer+=(j%2?-1:1)*m[0][j]*det3(sub);
    }
    return answer;
}
int main() {
    vector<int> edges;
    for(int a=0;a<7;++a) for(int b=a+1;b<7;++b)
    for(int c=b+1;c<7;++c) for(int d=c+1;d<7;++d)
        if(det4({a,b,c,d})==0) edges.push_back((1<<a)|(1<<b)|(1<<c)|(1<<d));
    sort(edges.begin(),edges.end());
    assert((edges==vector<int>{15,113}));
    array<int,128> grundy{}; grundy.fill(-1);
    map<int,int> hist;
    for(int s=127;s>=0;--s) {
        bool valid=true;
        for(int e:edges) if((s&e)==e) valid=false;
        if(!valid)continue;
        array<bool,8> seen{};
        for(int i=0;i<7;++i) {
            if(s&(1<<i))continue;
            int t=s|(1<<i);
            bool legal=true;
            for(int e:edges) if((t&e)==e) legal=false;
            if(legal) {assert(grundy[t]>=0);seen[grundy[t]]=true;}
        }
        int g=0;
        while(seen[g])++g;
        assert(g<=3);
        grundy[s]=g;
        hist[g]++;
    }
    assert(grundy[0]==1 && grundy[50]==3);
    assert(hist[0]==38 && hist[1]==42 && hist[2]==15 && hist[3]==18);
    cout<<"forbidden masks:";for(int e:edges)cout<<" "<<e;
    cout<<"\nsafe states: "<<hist[0]+hist[1]+hist[2]+hist[3]<<"\n";
    cout<<"root nimber: "<<grundy[0]<<"; witness nimber: "<<grundy[50]<<"\n";
    for(auto [g,count]:hist)cout<<"g="<<g<<": "<<count<<"\n";
}
