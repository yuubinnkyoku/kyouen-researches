// Independent audit: direct 4x4 determinant (permutations), subset DP.
// g(terminal)=0; misere auxiliary h(terminal)=1.
#include <array>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <vector>
#include <string>
using namespace std;
using Point = array<int,3>;

long long det4(const array<Point,4>& q) {
    long long a[4][4];
    for (int i=0;i<4;i++) {
        a[i][0]=1;
        for(int j=0;j<3;j++) a[i][j+1]=q[i][j];
    }
    array<int,4> p{0,1,2,3};
    long long ans=0;
    do {
        long long term=1;
        int inversions=0;
        for (int i=0;i<4;i++) {
            term *= a[i][p[i]];
            for(int j=0;j<i;j++) inversions+=(p[j]>p[i]);
        }
        ans+=(inversions%2?-term:term);
    } while(next_permutation(p.begin(),p.end()));
    return ans;
}

void audit(int k,int m) {
    vector<Point> p;
    for(int x=0;x<2;x++) for(int y=0;y<k;y++) for(int z=0;z<m;z++) p.push_back({x,y,z});
    const int n=p.size(), N=1<<n;
    assert(n<=18);
    vector<vector<int>> bad_by_high(n);
    int bad=0;
    for(int a=0;a<n;a++) for(int b=a+1;b<n;b++)
    for(int c=b+1;c<n;c++) for(int d=c+1;d<n;d++) {
        if(det4({p[a],p[b],p[c],p[d]})==0) {
            bad_by_high[d].push_back((1<<a)|(1<<b)|(1<<c)|(1<<d));
            bad++;
        }
    }
    vector<uint8_t> safe(N),g(N),h(N);
    safe[0]=1;
    vector<vector<int>> layers(7);
    layers[0].push_back(0);
    for(int s=1;s<N;s++) {
        int top=31-__builtin_clz((unsigned)s);
        if(!safe[s^(1<<top)]) continue;
        bool ok=true;
        for(int b:bad_by_high[top]) if((s&b)==b) {ok=false;break;}
        if(ok) {
            safe[s]=1;
            int size=__builtin_popcount((unsigned)s);
            assert(size<=6);
            layers[size].push_back(s);
        }
    }
    map<int,int> terminal,first_g,first_h;
    for(int lev=6;lev>=0;lev--) for(int s:layers[lev]) {
        bool used_g[16]={},used_h[16]={};
        int children=0;
        for(int i=0;i<n;i++) if(!(s&(1<<i)) && safe[s|(1<<i)]) {
            int t=s|(1<<i);
            used_g[g[t]]=true;
            used_h[h[t]]=true;
            children++;
        }
        if(children==0) {
            terminal[lev]++;
            h[s]=1;
        } else {
            int a=0,b=0;
            while(used_g[a]) a++;
            while(used_h[b]) b++;
            g[s]=a;h[s]=b;
        }
    }
    int swap=0;
    for(int s=0;s<N;s++) if(safe[s]) {
        int expected=(g[s]<2)?1-g[s]:g[s];
        if(h[s]!=expected) swap++;
    }
    for(int i=0;i<n;i++) {first_g[g[1<<i]]++;first_h[h[1<<i]]++;}
    cout<<"board 2 "<<k<<" "<<m<<"\nforbidden "<<bad<<"\nsafe_layers";
    for(auto& layer:layers) cout<<" "<<layer.size();
    cout<<"\nterminal";
    for(auto [size,count]:terminal) cout<<" "<<size<<":"<<count;
    cout<<"\ng0 "<<(int)g[0]<<"\nh0 "<<(int)h[0]<<"\nfirst_g";
    for(auto [nim,count]:first_g) cout<<" "<<nim<<":"<<count;
    cout<<"\nfirst_h";
    for(auto [nim,count]:first_h) cout<<" "<<nim<<":"<<count;
    cout<<"\nswap_failures "<<swap<<"\nfirst_winning";
    for(int i=0;i<n;i++) if(g[1<<i]==0)
        cout<<" ("<<p[i][0]<<","<<p[i][1]<<","<<p[i][2]<<")";
    cout<<"\n";
}

struct P2 { int y, z; };
int cross2(P2 a, P2 b) { return a.y*b.z-a.z*b.y; }
P2 subtract2(P2 a, P2 b) { return {a.y-b.y,a.z-b.z}; }

// Enumerate all oriented 3+2 safe sets, and all terminal 5-stone sets.
// Fixing the 3-stone layer at x=0 avoids duplicate enumeration.
void audit_large_square_terminal5(int k) {
    const int n=k*k;
    vector<P2> p;
    for(int y=0;y<k;y++) for(int z=0;z<k;z++) p.push_back({y,z});
    long long safe=0,terminal=0;
    for(int a=0;a<n;a++) for(int b=a+1;b<n;b++)
    for(int c=b+1;c<n;c++) {
        P2 ab=subtract2(p[b],p[a]),ac=subtract2(p[c],p[a]);
        P2 bc=subtract2(p[c],p[b]);
        if(cross2(ab,ac)==0) continue;
        P2 directions[3]={ab,ac,bc};
        for(int d=0;d<n;d++) for(int e=d+1;e<n;e++) {
            P2 de=subtract2(p[e],p[d]);
            if(cross2(de,ab)==0||cross2(de,ac)==0||
               cross2(de,bc)==0) continue;
            safe++;
            bool extend=false;
            for(int f=0;f<n;f++) {
                if(f==d||f==e) continue;
                P2 df=subtract2(p[f],p[d]),ef=subtract2(p[f],p[e]);
                if(cross2(de,df)==0) continue;
                bool good=true;
                for(auto direction:directions)
                    if(cross2(direction,df)==0||
                       cross2(direction,ef)==0) {good=false;break;}
                if(good) {extend=true;break;}
            }
            if(!extend) terminal++;
        }
    }
    cout<<"large_square "<<k<<" safe_oriented_3plus2 "<<safe
        <<" terminal_oriented_3plus2 "<<terminal<<"\\n";
    const long long expected_safe[]={0,0,0,1332,40368,475400,3408680,17308328};
    const long long expected_terminal[]={0,0,0,532,304,0,0,0};
    assert(k>=3&&k<=7);
    assert(safe==expected_safe[k]&&terminal==expected_terminal[k]);
}

int main(int argc,char** argv) {
    if(argc>1 && string(argv[1])=="--large-square") {
        for(int k=3;k<=7;k++) audit_large_square_terminal5(k);
        return 0;
    }
    audit(2,2);
    audit(2,3);
    audit(3,2);
    audit(3,3);
}
