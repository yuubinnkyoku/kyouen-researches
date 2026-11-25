// Exact quotient mex for k=6 with exactly five missing pair signatures.
// Each present pair has 1 or 2 twins, each leaf signature has 0, 1 or 2.
// The k=5 and k=6 exceptions are NOT replaced by the claimed formula.
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
    constexpr int K=6, MAX_T=729;
    vector<pair<int,int>> edges;
    for(int i=0;i<K;i++) for(int j=i+1;j<K;j++) edges.push_back({i,j});
    vector<array<int,5>> reps;
    set<array<int,5>> covered;
    array<int,K> perm;
    iota(perm.begin(),perm.end(),0);
    for(int a=0;a<15;a++) for(int b=a+1;b<15;b++)
    for(int c=b+1;c<15;c++) for(int d=c+1;d<15;d++)
    for(int e=d+1;e<15;e++) {
        array<int,5> ids={a,b,c,d,e};
        if(covered.count(ids)) continue;
        reps.push_back(ids);
        do {
            array<int,5> mapped;
            for(int j=0;j<5;j++) {
                auto [x,y]=edges[ids[j]];
                x=perm[x]; y=perm[y];
                if(x>y) swap(x,y);
                mapped[j]=int(find(edges.begin(),edges.end(),pair<int,int>{x,y})-edges.begin());
            }
            sort(mapped.begin(),mapped.end());
            covered.insert(mapped);
        } while(next_permutation(perm.begin(),perm.end()));
    }
    assert(reps.size()==15 && covered.size()==3003);
    long long total=0;
    for(int shape=0;shape<int(reps.size());shape++) {
        bool absent[15]={};
        for(int j:reps[shape]) absent[j]=true;
        int sig[16],n=0;
        for(int j=0;j<15;j++) if(!absent[j])
            sig[n++]=(1<<edges[j].first)|(1<<edges[j].second);
        for(int i=0;i<K;i++) sig[n++]=1<<i;
        assert(n==16);
        ull incidence[16]={};
        for(int j=0;j<16;j++) for(int mask=1;mask<64;mask++)
            if(sig[j]&mask) incidence[j]|=1ULL<<mask;
        ull pair_activity[1024]={},leaf_activity[64]={};
        unsigned char pair_z[1024]={};
        for(int p=1;p<1024;p++) {
            int j=__builtin_ctz(unsigned(p)),prev=p&(p-1);
            pair_activity[p]=pair_activity[prev]^incidence[j];
            pair_z[p]=pair_z[prev]^sig[j];
        }
        for(int p=1;p<64;p++) {
            int j=__builtin_ctz(unsigned(p)),prev=p&(p-1);
            leaf_activity[p]=leaf_activity[prev]^incidence[10+j];
        }
        unsigned char leaf_odd[729],leaf_present[729];
        for(int t=0;t<729;t++) {
            int v=t,odd=0,present=0;
            for(int i=0;i<K;i++) {
                int digit=v%3;v/=3;
                if(digit&1) odd|=1<<i;
                if(digit) present|=1<<i;
            }
            leaf_odd[t]=odd;leaf_present[t]=present;
        }
        unsigned char next[64][16];
        for(int mask=0;mask<64;mask++) for(int j=0;j<16;j++)
            next[mask][j]=mask&~sig[j];
        long long bad=0,bad_center_positive=0,bad_center_zero=0;
        long long distribution[8]={};
        int firstP=-1,firstT=-1,firstA=-1,firstF=-1;
        for(int p=0;p<1024;p++) for(int t=0;t<MAX_T;t++) {
            ull active_bits=pair_activity[p]^leaf_activity[leaf_odd[t]];
            int z=pair_z[p]^leaf_odd[t];
            unsigned char active[64],dp[64]={};
            for(int mask=0;mask<64;mask++) active[mask]=(active_bits>>mask)&1;
            for(int mask=1;mask<64;mask++) {
                unsigned options=0;
                int z_ones=z&mask;
                if(z_ones && z_ones!=mask) options=3;
                else options=1u<<(active[mask]^(z_ones!=0));
                for(int j=0;j<10;j++) if(sig[j]&mask) {
                    int child=next[mask][j];
                    options|=1u<<(dp[child]^active[mask]^active[child]^1);
                }
                int present=leaf_present[t]&mask;
                while(present) {
                    int i=__builtin_ctz(unsigned(present));
                    present&=present-1;
                    int child=next[mask][10+i];
                    options|=1u<<(dp[child]^active[mask]^active[child]^1);
                }
                dp[mask]=__builtin_ctz(~options);
            }
            int u=active[63];
            int predicted=(z==0||z==63)?(1^u^(z!=0)):2+u;
            int actual=dp[63];
            assert(actual>=0 && actual<8);
            distribution[actual]++;
            if(actual!=predicted) {
                bad++;
                if(t%3) bad_center_positive++;
                else bad_center_zero++;
                if(firstP<0) {firstP=p;firstT=t;firstA=actual;firstF=predicted;}
            }
        }
        cout<<"shape="<<shape+1<<" missing=";
        for(int j:reps[shape]) cout<<edges[j].first<<edges[j].second<<",";
        cout<<" bad="<<bad<<" center_positive_bad="<<bad_center_positive
            <<" center_zero_bad="<<bad_center_zero<<" total="<<1024*MAX_T
            <<" first="<<firstP<<","<<firstT<<","<<firstA<<","<<firstF<<" dist=";
        for(int i=0;i<8;i++) cout<<distribution[i]<<",";
        cout<<"\n";
        assert(bad_center_positive==0);
        assert(bad==(shape==0?241024:0));
        assert(distribution[0]==11680 && distribution[1]==11680);
        assert(distribution[2]==361568 && distribution[3]==361568);
        for(int i=4;i<8;i++) assert(distribution[i]==0);
        total+=1024LL*MAX_T;
    }
    assert(total==11197440);
    cout<<"PASS: 15 missing-five orbits, 11197440 representatives; only five-star with zero center leaves can violate formula\n";
}
