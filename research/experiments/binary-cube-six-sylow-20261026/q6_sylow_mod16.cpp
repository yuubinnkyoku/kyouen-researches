// Exact q=6 rooted support coefficients modulo 16 via the 2-Sylow subgroup of S_6.
// Compile: g++ -O3 -std=c++17 -Wall -Wextra q6_sylow_mod16.cpp -o /tmp/q6_sylow
// Run: /tmp/q6_sylow
// The mod-1009 test is exact: all 5x5 0/1 minors have absolute value <56;
// Cramer's rule bounds a binary coordinate discrepancy by <336 <1009.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <map>
#include <numeric>
#include <vector>
using namespace std;
constexpr int PRIME=1009;
using Perm=array<int,32>;
int inverse_mod[PRIME];

Perm compose(const Perm&a,const Perm&b) {
    Perm c;
    for(int i=0;i<32;i++) c[i]=a[b[i]];
    return c;
}
Perm identity() {
    Perm a;
    for(int i=0;i<32;i++) a[i]=i;
    return a;
}
Perm row_perm(array<int,5> p) {
    Perm a;
    for(int x=0;x<32;x++) {
        int y=0;
        for(int i=0;i<5;i++) if(x>>i&1) y|=1<<p[i];
        a[x]=y;
    }
    return a;
}
Perm origin_swap() {
    Perm a;
    for(int x=0;x<32;x++) a[x]=(x&16)?(x^15):x;
    return a;
}
vector<Perm> sylow_group() {
    vector<Perm> generators={
        row_perm({1,2,3,0,4}), row_perm({3,2,1,0,4}), origin_swap()
    };
    vector<Perm> group={identity()};
    for(size_t i=0;i<group.size();i++)
        for(const auto&g:generators) {
            Perm x=compose(g,group[i]);
            if(find(group.begin(),group.end(),x)==group.end()) group.push_back(x);
        }
    assert(group.size()==16);
    return group;
}
vector<uint32_t> subgroups(const vector<Perm>&group) {
    int n=group.size(),mul[16][16]={};
    for(int i=0;i<n;i++) for(int j=0;j<n;j++) {
        Perm p=compose(group[i],group[j]);
        auto it=find(group.begin(),group.end(),p);
        assert(it!=group.end());
        mul[i][j]=it-group.begin();
    }
    auto closure=[&](uint32_t mask) {
        bool changed=true;
        while(changed) {
            changed=false;
            for(int i=0;i<n;i++) if(mask>>i&1)
                for(int j=0;j<n;j++) if(mask>>j&1) {
                    uint32_t bit=1u<<mul[i][j];
                    if(!(mask&bit)) {mask|=bit;changed=true;}
                }
        }
        return mask;
    };
    vector<uint32_t> result={1u};
    for(size_t z=0;z<result.size();z++) for(int g=0;g<n;g++) {
        uint32_t h=closure(result[z]|(1u<<g));
        if(find(result.begin(),result.end(),h)==result.end()) result.push_back(h);
    }
    assert(result.size()==35);
    sort(result.begin(),result.end(),[](uint32_t a,uint32_t b) {
        return __builtin_popcount(a)>__builtin_popcount(b);
    });
    return result;
}
vector<vector<int>> column_orbits(const vector<Perm>&group,uint32_t subgroup) {
    bool seen[32]={};
    vector<vector<int>> result;
    for(int x=0;x<32;x++) if(!seen[x]) {
        vector<int> orbit={x};
        seen[x]=true;
        for(size_t i=0;i<orbit.size();i++)
            for(int g=0;g<(int)group.size();g++) if(subgroup>>g&1) {
                int y=group[g][orbit[i]];
                if(!seen[y]) {seen[y]=true;orbit.push_back(y);}
            }
        sort(orbit.begin(),orbit.end());
        result.push_back(orbit);
    }
    return result;
}
// A 5 x k binary matrix represents the five nonzero rooted vertices.
// It is admissible iff the binary points in its real row span are exactly
// the zero row and those five distinct rows.
bool admissible(const vector<int>&columns) {
    int k=columns.size(), a[5][32]={}, row_bits[5]={};
    for(int i=0;i<5;i++) for(int j=0;j<k;j++) {
        a[i][j]=(columns[j]>>i)&1;
        row_bits[i]|=a[i][j]<<j;
    }
    for(int i=0;i<5;i++) {
        if(!row_bits[i]) return false;
        for(int j=0;j<i;j++) if(row_bits[i]==row_bits[j]) return false;
    }
    int rank=0;
    for(int j=0;j<k&&rank<5;j++) {
        int p=rank;
        while(p<5&&!a[p][j]) p++;
        if(p==5) continue;
        if(p!=rank) for(int l=0;l<k;l++) swap(a[p][l],a[rank][l]);
        int inv=inverse_mod[a[rank][j]];
        for(int l=0;l<k;l++) a[rank][l]=a[rank][l]*inv%PRIME;
        for(int i=0;i<5;i++) if(i!=rank&&a[i][j]) {
            int factor=a[i][j];
            for(int l=0;l<k;l++) {
                int v=a[i][l]-factor*a[rank][l]%PRIME;
                a[i][l]=v<0?v+PRIME:v;
            }
        }
        rank++;
    }
    int binary_points=0;
    for(int mask=0;mask<(1<<rank);mask++) {
        bool good=true;
        for(int j=0;j<k;j++) {
            int v=0;
            for(int i=0;i<rank;i++) if(mask>>i&1) v+=a[i][j];
            v%=PRIME;
            if(v!=0&&v!=1) {good=false;break;}
        }
        if(good&&++binary_points>6) return false;
    }
    return binary_points==6;
}
struct Count {uint64_t visited=0, valid=0;};
Count fixed_count(const vector<vector<int>>&orbits,int k) {
    Count result;
    vector<int> columns;
    function<void(int,int)> visit=[&](int i,int remaining) {
        if(i==(int)orbits.size()) {
            if(remaining==0) {
                result.visited++;
                if(admissible(columns)) result.valid++;
            }
            return;
        }
        visit(i+1,remaining);
        if((int)orbits[i].size()<=remaining) {
            for(int x:orbits[i]) columns.push_back(x);
            visit(i+1,remaining-(int)orbits[i].size());
            for(size_t j=0;j<orbits[i].size();j++) columns.pop_back();
        }
    };
    visit(0,k);
    return result;
}
int main() {
    inverse_mod[1]=1;
    for(int i=2;i<PRIME;i++)
        inverse_mod[i]=PRIME-(PRIME/i)*inverse_mod[PRIME%i]%PRIME;
    auto group=sylow_group();
    auto H=subgroups(group);
    for(int k:{10,11}) {
        vector<int64_t> fixed(H.size()),exact(H.size());
        map<vector<vector<int>>,Count> cache;
        uint64_t checked=0;
        for(size_t i=0;i<H.size();i++) {
            if(__builtin_popcount(H[i])==1) continue; // free orbits vanish mod 16
            auto orbits=column_orbits(group,H[i]);
            auto it=cache.find(orbits);
            Count c;
            if(it!=cache.end()) c=it->second;
            else {
                c=fixed_count(orbits,k);
                cache[orbits]=c;
                checked+=c.visited;
            }
            fixed[i]=c.valid;
            exact[i]=fixed[i];
            for(size_t j=0;j<i;j++)
                if((H[j]&H[i])==H[i]) exact[i]-=exact[j];
            assert(exact[i]>=0);
        }
        int64_t nonfree=accumulate(exact.begin(),exact.end(),int64_t{0});
        int residue=nonfree%16;
        assert(residue==(k==10?10:6));
        cout<<"k="<<k<<" h_mod16="<<residue
            <<" checked="<<checked<<" distinct_orbit_partitions="<<cache.size()
            <<" nontrivial_stabilizer_points="<<nonfree<<"\n";
    }
}
