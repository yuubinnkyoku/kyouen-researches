// Independent determinant and dense DP audit of the 11-point witness;
// exhaustive enumeration of all C(25,11) subsets for the 5x5 lower bound.
// Build: g++ -O3 -std=c++17 verify_independent.cpp -o /tmp/verify && /tmp/verify
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
struct Point { int x,y; };
using Mask=uint32_t;
long long norm(Point p){return p.x*p.x+p.y*p.y;}
bool bad(Point a,Point b,Point c,Point d){
    long long X1=b.x-a.x,Y1=b.y-a.y,Z1=norm(b)-norm(a);
    long long X2=c.x-a.x,Y2=c.y-a.y,Z2=norm(c)-norm(a);
    long long X3=d.x-a.x,Y3=d.y-a.y,Z3=norm(d)-norm(a);
    return Z1*(X2*Y3-X3*Y2)-X1*(Z2*Y3-Z3*Y2)
        +Y1*(Z2*X3-X2*Z3)==0;
}
vector<Mask> edges(const vector<Point>& p){
    vector<Mask> e;
    for(int a=0;a<(int)p.size();a++)for(int b=a+1;b<(int)p.size();b++)
    for(int c=b+1;c<(int)p.size();c++)for(int d=c+1;d<(int)p.size();d++)
        if(bad(p[a],p[b],p[c],p[d]))
            e.push_back((1u<<a)|(1u<<b)|(1u<<c)|(1u<<d));
    return e;
}
int main(){
    vector<Point> w={{0,0},{0,4},{1,1},{1,3},{3,1},{3,2},
                     {3,4},{4,1},{4,5},{5,0},{5,2}};
    auto e=edges(w);
    if(e.size()!=4){cerr<<"witness edge count wrong\n";return 1;}
    array<int,6> hist{};
    array<int,2048> g{};
    int safe=0;
    for(int s=2047;s>=0;s--){
        bool invalid=false;
        for(auto x:e)if(((Mask)s&x)==x){invalid=true;break;}
        if(invalid){g[s]=-1;continue;}
        safe++;
        unsigned options=0;
        for(int i=0;i<11;i++)if(!(s&(1<<i)) && g[s|(1<<i)]>=0)
            options|=1u<<g[s|(1<<i)];
        int val=0;while(options&(1u<<val))val++;
        if(val>5){cerr<<"nimber >5\n";return 1;}
        g[s]=val;hist[val]++;
    }
    if(g[0]!=5 || safe!=1635 || hist!=array<int,6>{{585,586,224,230,9,1}}){
        cerr<<"witness DP mismatch\n";return 1;
    }
    vector<Point> p;
    for(int x=0;x<5;x++)for(int y=0;y<5;y++)p.push_back({x,y});
    auto all=edges(p);
    if(all.size()!=826){cerr<<"5x5 geometry mismatch\n";return 1;}
    long long total=0, min_count=10000, min_witnesses=0, at_most_four=0;
    Mask s=(1u<<11)-1;
    while(s<(1u<<25)){
        total++;
        int count=0;
        for(auto x:all)if((s&x)==x)count++;
        if(count<min_count){min_count=count;min_witnesses=0;}
        if(count==min_count)min_witnesses++;
        if(count<=4)at_most_four++;
        Mask c=s&-s,r=s+c;
        if(!r)break;
        s=(((r^s)>>2)/c)|r;
    }
    if(total!=4457400 || min_count!=5 || min_witnesses!=8 || at_most_four!=0){
        cerr<<"5x5 enumeration mismatch\n";return 1;
    }
    cout<<"6x6 witness: n=11, edges="<<e.size()<<", safe="<<safe
        <<", g(empty)="<<g[0]<<", hist=";
    for(int v:hist)cout<<v<<" ";
    cout<<"\n5x5: C(25,11)="<<total<<", min forbidden="<<min_count
        <<", minimizers="<<min_witnesses<<", at most four="<<at_most_four<<"\n";
}
