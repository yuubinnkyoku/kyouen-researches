// Exhaustive parity/positivity quotient for k=6, exactly four absent pair types.
// 9 isomorphism classes, 2^11 positive pair parities, 3^6 leaf states.
// No assumption about the k=5 formula is made in this enumeration.
#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <numeric>
#include <set>
#include <utility>
#include <vector>
using namespace std;
using ull = unsigned long long;

int main() {
    constexpr int K = 6;
    vector<pair<int,int>> edges;
    for (int i=0;i<K;i++) for (int j=i+1;j<K;j++) edges.push_back({i,j});
    vector<array<int,4>> reps;
    set<array<int,4>> covered;
    array<int,K> perm;
    iota(perm.begin(),perm.end(),0);
    for (int a=0;a<15;a++) for (int b=a+1;b<15;b++)
    for (int c=b+1;c<15;c++) for (int d=c+1;d<15;d++) {
        array<int,4> ids={a,b,c,d};
        if (covered.count(ids)) continue;
        reps.push_back(ids);
        do {
            array<int,4> mapped;
            for (int j=0;j<4;j++) {
                auto [x,y]=edges[ids[j]];
                x=perm[x]; y=perm[y];
                if (x>y) swap(x,y);
                mapped[j]=int(find(edges.begin(),edges.end(),pair<int,int>{x,y})-edges.begin());
            }
            sort(mapped.begin(),mapped.end());
            covered.insert(mapped);
        } while (next_permutation(perm.begin(),perm.end()));
    }
    assert(reps.size()==9 && covered.size()==1365);
    long long total=0, mismatches=0;
    for (int shape=0;shape<int(reps.size());shape++) {
        bool absent[15]={};
        for (int j:reps[shape]) absent[j]=true;
        int sig[17], n=0;
        for (int j=0;j<15;j++) if (!absent[j])
            sig[n++]=(1<<edges[j].first)|(1<<edges[j].second);
        assert(n==11);
        for (int i=0;i<K;i++) sig[n++]=1<<i;
        ull incidence[17]={};
        for (int j=0;j<17;j++)
            for (int mask=1;mask<64;mask++)
                if (sig[j]&mask) incidence[j]|=1ULL<<mask;
        ull pair_activity[2048]={}, leaf_activity[64]={};
        unsigned char pair_z[2048]={};
        for (int p=1;p<2048;p++) {
            int j=__builtin_ctz(unsigned(p)),prev=p&(p-1);
            pair_activity[p]=pair_activity[prev]^incidence[j];
            pair_z[p]=pair_z[prev]^sig[j];
        }
        for (int p=1;p<64;p++) {
            int j=__builtin_ctz(unsigned(p)),prev=p&(p-1);
            leaf_activity[p]=leaf_activity[prev]^incidence[11+j];
        }
        unsigned char leaf_odd[729],leaf_present[729];
        for (int t=0;t<729;t++) {
            int v=t,odd=0,present=0;
            for (int i=0;i<K;i++) {
                int digit=v%3;v/=3;
                if (digit&1) odd|=1<<i;
                if (digit) present|=1<<i;
            }
            leaf_odd[t]=odd;leaf_present[t]=present;
        }
        unsigned char next[64][17];
        for (int mask=0;mask<64;mask++)
            for (int j=0;j<17;j++) next[mask][j]=mask&~sig[j];
        long long bad=0;
        long long distribution[8]={};
        for (int p=0;p<2048;p++) for (int t=0;t<729;t++) {
            ull active_bits=pair_activity[p]^leaf_activity[leaf_odd[t]];
            int z=pair_z[p]^leaf_odd[t];
            unsigned char active[64],dp[64]={};
            for (int mask=0;mask<64;mask++) active[mask]=(active_bits>>mask)&1;
            for (int mask=1;mask<64;mask++) {
                unsigned options=0;
                int z_ones=z&mask;
                if (z_ones && z_ones!=mask) options=3;
                else options=1u<<(active[mask]^(z_ones!=0));
                for (int j=0;j<11;j++) if (sig[j]&mask) {
                    int child=next[mask][j];
                    options|=1u<<(dp[child]^active[mask]^active[child]^1);
                }
                int present=leaf_present[t]&mask;
                while (present) {
                    int i=__builtin_ctz(unsigned(present));
                    present&=present-1;
                    int child=next[mask][11+i];
                    options|=1u<<(dp[child]^active[mask]^active[child]^1);
                }
                dp[mask]=__builtin_ctz(~options);
            }
            int u=active[63];
            int predicted=(z==0||z==63)?(1^u^(z!=0)):2+u;
            int actual=dp[63];
            assert(actual>=0 && actual<8);
            distribution[actual]++;
            if (actual!=predicted) {
                bad++;
                if (bad<=3)
                    cerr<<"counterexample shape="<<shape<<" pair="<<p
                        <<" leaves="<<t<<" actual="<<actual<<" predicted="<<predicted<<"\n";
            }
        }
        cout<<"shape="<<shape+1<<" missing=";
        for (int j:reps[shape])
            cout<<edges[j].first<<edges[j].second<<",";
        cout<<" cases="<<2048*729<<" bad="<<bad<<" g=";
        for (int i=0;i<8;i++) cout<<distribution[i]<<(i==7?"":",");
        cout<<"\n";
        assert(bad==0);
        assert(distribution[0]==23360 && distribution[1]==23360);
        assert(distribution[2]==723136 && distribution[3]==723136);
        for (int i=4;i<8;i++) assert(distribution[i]==0);
        total+=2048LL*729;
        mismatches+=bad;
    }
    assert(total==13436928 && mismatches==0);
    cout<<"PASS k=6 four missing types: 9 orbits, 13,436,928 representatives\n";
}
