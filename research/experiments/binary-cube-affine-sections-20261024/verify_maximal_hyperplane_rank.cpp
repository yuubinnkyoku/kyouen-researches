// Independent exhaustive affine-rank check of maximal hyperplane sections.
// For d=3,4, every q=2^(d-1) subset is tested, not only the listed flats.
// Over F_101 rank agrees with real rank: the integer 0/1 minors of order
// at most 5 have absolute value <= 5^(5/2) < 101 (Hadamard).
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <set>
#include <vector>
using namespace std;
constexpr int MOD = 101;
int inverse(int a) {
    for (int b = 1; b < MOD; ++b) if (a*b%MOD==1) return b;
    assert(false); return 0;
}
int affine_rank(const vector<int>& points, int d) {
    int a[16][6]{};
    for (int i=0; i<(int)points.size(); ++i) {
        a[i][0]=1;
        for (int j=0;j<d;++j) a[i][j+1]=(points[i]>>j)&1;
    }
    int rank=0;
    for (int c=0;c<=d;++c) {
        int p=rank;
        while (p<(int)points.size() && !a[p][c]) ++p;
        if (p==(int)points.size()) continue;
        for (int j=c;j<=d;++j) swap(a[p][j],a[rank][j]);
        int factor=inverse(a[rank][c]);
        for (int j=c;j<=d;++j) a[rank][j]=a[rank][j]*factor%MOD;
        for (int i=rank+1;i<(int)points.size();++i) if (a[i][c]) {
            factor=a[i][c];
            for (int j=c;j<=d;++j)
                a[i][j]=(a[i][j]-factor*a[rank][j]%MOD+MOD)%MOD;
        }
        ++rank;
        if (rank==(int)points.size()) break;
    }
    return rank;
}
void check(int d) {
    int n=1<<d, q=1<<(d-1);
    set<uint64_t> expected, actual;
    for (int i=0;i<d;++i) for (int b=0;b<2;++b) {
        uint64_t mask=0;
        for (int x=0;x<n;++x) if (((x>>i)&1)==b) mask|=1ULL<<x;
        expected.insert(mask);
    }
    for (int i=0;i<d;++i) for (int j=i+1;j<d;++j)
        for (int b=0;b<2;++b) {
            uint64_t mask=0;
            for (int x=0;x<n;++x)
                if ((((x>>i)^(x>>j))&1)==b) mask|=1ULL<<x;
            expected.insert(mask);
        }
    vector<int> chosen;
    long long subsets=0;
    auto dfs=[&](auto&& self,int first)->void {
        if ((int)chosen.size()==q) {
            ++subsets;
            if (affine_rank(chosen,d)<=d) {
                uint64_t mask=0;
                for (int x:chosen) mask|=1ULL<<x;
                actual.insert(mask);
            }
            return;
        }
        for (int x=first;x<=n-(q-(int)chosen.size());++x) {
            chosen.push_back(x);self(self,x+1);chosen.pop_back();
        }
    };
    dfs(dfs,0);
    assert(actual==expected);
    assert((int)actual.size()==d*(d+1));
    cout<<"d="<<d<<" q="<<q<<" subsets="<<subsets
        <<" coplanar="<<actual.size()<<" PASS\n";
}
int main() { check(3); check(4); }
