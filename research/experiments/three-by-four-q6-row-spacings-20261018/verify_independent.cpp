// Independent exact integer determinant + iterative subset DP.
// g++ -std=c++17 -O2 verify_independent.cpp -o /tmp/q6_3x4 && /tmp/q6_3x4
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
using namespace std;
using P = array<long long,2>;

long long det(vector<vector<long long>> a) {
    int n = (int)a.size();
    if (n == 1) return a[0][0];
    long long ans = 0;
    for (int j=0;j<n;j++) {
        vector<vector<long long>> b;
        for (int i=1;i<n;i++) {
            vector<long long> row;
            for (int k=0;k<n;k++) if (k!=j) row.push_back(a[i][k]);
            b.push_back(row);
        }
        ans += (j%2 ? -1 : 1)*a[0][j]*det(b);
    }
    return ans;
}

bool forbidden(const array<P,12>& p, int mask) {
    vector<int> ids;
    for(int i=0;i<12;i++) if(mask>>i&1) ids.push_back(i);
    assert(ids.size()==6);
    int a=-1,b=-1,c=-1;
    for(int i=0;i<6 && a<0;i++)
      for(int j=i+1;j<6 && a<0;j++)
        for(int k=j+1;k<6 && a<0;k++) {
            auto A=p[ids[i]], B=p[ids[j]], C=p[ids[k]];
            if ((B[0]-A[0])*(C[1]-A[1])-(B[1]-A[1])*(C[0]-A[0])!=0)
                a=ids[i], b=ids[j], c=ids[k];
        }
    if(a<0) return true;
    for(int i:ids) {
        auto row=[](P v){return vector<long long>{v[0]*v[0]+v[1]*v[1],v[0],v[1],1};};
        if(det({row(p[a]),row(p[b]),row(p[c]),row(p[i])})!=0) return false;
    }
    return true;
}

void run(string name, int a2, int b2, int expected_edges, int expected_root) {
    array<P,12> p;
    int ys[3]={0,a2,a2+b2};
    for(int r=0;r<3;r++) for(int x=0;x<4;x++) p[4*r+x]={2*x,ys[r]};
    vector<int> edges;
    for(int m=0;m<(1<<12);m++) if(__builtin_popcount((unsigned)m)==6 && forbidden(p,m)) edges.push_back(m);
    assert((int)edges.size()==expected_edges);
    if(edges.size()==2) assert(__builtin_popcount((unsigned)(edges[0]&edges[1]))==2);
    vector<int> g(1<<12,-1);
    map<int,int> hist,term;
    int safe=0;
    for(int m=(1<<12)-1;m>=0;m--) {
        bool bad=false;
        for(int e:edges) if((m&e)==e) {bad=true;break;}
        if(bad) continue;
        ++safe;
        unsigned successor_bits=0;
        int options=0;
        for(int i=0;i<12;i++) if(!(m>>i&1) && g[m|(1<<i)]>=0) {
            successor_bits|=(1u<<g[m|(1<<i)]);
            ++options;
        }
        int k=0; while(successor_bits>>k&1) k++;
        g[m]=k;
        hist[k]++;
        if(!options) term[__builtin_popcount((unsigned)m)]++;
    }
    assert(g[0]==expected_root);
    for(int i=0;i<12;i++) assert(g[1<<i]==(expected_root==1 ? 0 : 1));
    if(name=="double") {
        assert(safe==3972 && term[10]==16 && term[11]==2);
        assert(hist[0]==1378 && hist[1]==1378 && hist[2]==608 && hist[3]==608);
    }
    cout << name << " edges=" << edges.size() << " safe=" << safe
         << " root=" << g[0] << " max_g=" << hist.rbegin()->first << " terminals=";
    for(auto [n,count]:term) cout << n << ":" << count << ",";
    cout << "\n";
}

int main() {
    run("none",2,6,0,0);
    run("ab",2,4,1,1);
    run("a_times_total",1,7,1,1);
    run("b_times_total",7,1,1,1);
    run("double",2,2,2,0);
}
