// Independent full occupancy-subset dynamic program (not the Python count-state recursion).
// g(mask) = mex(g(mask | (1<<v)) for legal additions v), all four edges rank 2..4.
#include <array>
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <vector>
#include <cstdlib>
#include <set>
using namespace std;
array<int, 16> mult{};
array<int, 4> sizes{};
array<long long, 16> hist{}, uniform_hist{};
long long enumerated=0, minimal=0;
int max_g=-1;
array<long long,17> g5_by_vertices{};
set<array<int,16>> g5_orbits;
array<int,16> witness{};

int full_subset_sg(const array<uint32_t,4>& edges, int n) {
    int count = 1 << n;
    vector<uint8_t> dp(count, 255);
    for (int mask = count - 1; mask >= 0; --mask) {
        bool safe = true;
        for (uint32_t e : edges) if ((uint32_t(mask) & e) == e) {safe = false;break;}
        if (!safe) continue;
        uint32_t children = 0;
        for (int v=0;v<n;++v) if (!(mask & (1<<v))) {
            int next=mask|(1<<v);
            if (dp[next]!=255) children |= 1u << dp[next];
        }
        uint8_t mex=0;
        while (children & (1u << mex)) ++mex;
        dp[mask]=mex;
    }
    return dp[0];
}

void walk(int t) {
    if (t==16) {
        ++enumerated;
        for (int s:sizes) if (s<2 || s>4) return;
        array<uint32_t,4> edges{};
        int n=0;
        for (int mask=1;mask<16;++mask) for(int j=0;j<mult[mask];++j) {
            for (int i=0;i<4;++i) if(mask&(1<<i)) edges[i] |= (1u<<n);
            ++n;
        }
        for (int i=0;i<4;++i) for(int j=0;j<4;++j) if(i!=j)
            if ((edges[i] & edges[j])==edges[i]) return; // not an antichain
        ++minimal;
        int g=full_subset_sg(edges,n);
        if (g>15) {fprintf(stderr,"out of range\n");exit(1);}
        ++hist[g];
        if (g == 5) {
            ++g5_by_vertices[n];
            array<int,4> perm={0,1,2,3};
            array<int,16> best{};
            bool first=true;
            do {
                array<int,16> transformed{};
                for(int old=1;old<16;++old) {
                    int mapped=0;
                    for(int i=0;i<4;++i) if(old&(1<<i)) mapped|=1<<perm[i];
                    transformed[mapped]=mult[old];
                }
                if(first || transformed<best) {best=transformed;first=false;}
            } while(next_permutation(perm.begin(),perm.end()));
            g5_orbits.insert(best);
        }
        if (all_of(sizes.begin(),sizes.end(),[](int x){return x==4;})) ++uniform_hist[g];
        if (g>max_g) {max_g=g;witness=mult;}
        return;
    }
    int limit=4;
    for(int i=0;i<4;++i) if(t & (1<<i)) limit=min(limit,4-sizes[i]);
    for(int x=0;x<=limit;++x) {
        mult[t]=x;
        for(int i=0;i<4;++i) if(t&(1<<i)) sizes[i]+=x;
        walk(t+1);
        for(int i=0;i<4;++i) if(t&(1<<i)) sizes[i]-=x;
    }
    mult[t]=0;
}
int main() {
    walk(1);
    printf("all_vectors=%lld minimal_2to4=%lld max_g=%d\n",enumerated,minimal,max_g);
    printf("hist:");for(int i=0;i<=max_g;++i) printf(" %d:%lld",i,hist[i]);puts("");
    printf("uniform4:");for(int i=0;i<=max_g;++i) printf(" %d:%lld",i,uniform_hist[i]);puts("");
    printf("g5_sizes: 9:%lld 11:%lld; orbits=%zu\n",g5_by_vertices[9],g5_by_vertices[11],g5_orbits.size());
    printf("first_max_witness:");for(int i=1;i<16;++i) if(witness[i]) printf(" %d:%d",i,witness[i]);puts("");
    if(enumerated!=92550 || minimal!=37592 || max_g!=5 || g5_by_vertices[9]!=24 || g5_by_vertices[11]!=12 || g5_orbits.size()!=2) return 2;
    array<long long,6> expect={13508,13427,5111,5270,240,36};
    array<long long,6> uexpect={1269,1294,429,602,36,12};
    for(int i=0;i<6;++i) if(hist[i]!=expect[i] || uniform_hist[i]!=uexpect[i]) return 3;
}
