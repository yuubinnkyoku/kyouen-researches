// Exhaustive finite bases and deterministic larger-k tests for the missing-matching theorem.
// c++ -std=c++17 -O2 -Wall -Wextra -pedantic verify.cpp -o /tmp/verify_matching && /tmp/verify_matching
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>
using namespace std;

int sg(int k, const vector<int>& types, const vector<int>& cnt) {
    int n = 1<<k;
    vector<int> parity(n), dp(n);
    int z[16]={};
    for (size_t a=0;a<types.size();++a) {
        if (!(cnt[a]&1)) continue;
        for (int i=0;i<k;++i) if (types[a]&(1<<i)) z[i]^=1;
    }
    for (int mask=1;mask<n;++mask) {
        int v=0;
        for (size_t a=0;a<types.size();++a)
            if ((types[a]&mask)!=0) v^=cnt[a]&1;
        parity[mask]=v;
    }
    for (int mask=1;mask<n;++mask) {
        unsigned child=0;
        for (int i=0;i<k;++i)
            if (mask&(1<<i)) child|=1u<<(parity[mask]^z[i]);
        for (size_t a=0;a<types.size();++a) {
            if (!cnt[a] || !(types[a]&mask)) continue;
            int next=mask&~types[a];
            int value=dp[next]^parity[mask]^parity[next]^1;
            assert(value<32);
            child|=1u<<value;
        }
        int v=0;
        while (child&(1u<<v)) ++v;
        dp[mask]=v;
    }
    return dp[n-1];
}
int predicted(int k,const vector<int>& types,const vector<int>& cnt) {
    int u=0,z[16]={};
    for (size_t a=0;a<types.size();++a) {
        u^=cnt[a]&1;
        for(int i=0;i<k;++i) if(types[a]&(1<<i)) z[i]^=cnt[a]&1;
    }
    bool uniform=true;
    for(int i=1;i<k;++i) if(z[i]!=z[0]) uniform=false;
    return uniform ? (1^u^z[0]) : (2+u);
}
vector<int> types_for(int k,int missing) {
    vector<int> t;
    for(int i=0;i<k;++i) t.push_back(1<<i);
    for(int i=0;i<k;++i) for(int j=i+1;j<k;++j) {
        bool absent=false;
        for(int a=0;a<missing;++a) if(i==2*a && j==2*a+1) absent=true;
        if(!absent)t.push_back((1<<i)|(1<<j));
    }
    return t;
}
int main() {
    uint64_t total=0;
    for(int k=3;k<=5;++k) for(int missing=0;missing<=k/2;++missing) {
        vector<int> t=types_for(k,missing);
        int pair_count=int(t.size())-k;
        uint64_t cases=0;
        int leaf_total=1;
        for(int i=0;i<k;++i) leaf_total*=3;
        for(int leaf_code=0;leaf_code<leaf_total;++leaf_code) {
            vector<int> cnt(t.size(),1);
            int code=leaf_code;
            for(int i=0;i<k;++i) {cnt[i]=code%3;code/=3;}
            for(int bits=0;bits<(1<<pair_count);++bits) {
                for(int j=0;j<pair_count;++j)cnt[k+j]=1+((bits>>j)&1);
                int actual=sg(k,t,cnt),want=predicted(k,t,cnt);
                if(actual!=want) {
                    cerr<<"FAIL k="<<k<<" missing="<<missing<<" leaf="<<leaf_code<<" pairbits="<<bits<<" actual="<<actual<<" predicted="<<want<<"\n";
                    return 1;
                }
                ++cases;
            }
        }
        total+=cases;
        cout<<"EXHAUSTIVE k="<<k<<" missing="<<missing<<" cases="<<cases<<" PASS\n";
    }
    mt19937 rng(20261028);
    uint64_t sampled=0;
    for(int k=6;k<=12;++k) for(int missing=0;missing<=k/2;++missing) {
        auto t=types_for(k,missing);
        for(int rep=0;rep<200;++rep) {
            vector<int> cnt(t.size());
            for(int i=0;i<k;++i)cnt[i]=rng()%7;
            for(size_t j=k;j<t.size();++j)cnt[j]=1+rng()%7;
            int actual=sg(k,t,cnt),want=predicted(k,t,cnt);
            if(actual!=want) {cerr<<"RANDOM FAIL k="<<k<<" missing="<<missing<<"\n";return 2;}
            ++sampled;
        }
    }
    cout<<"PASS exhaustive="<<total<<" deterministic_samples="<<sampled<<"\n";
}
