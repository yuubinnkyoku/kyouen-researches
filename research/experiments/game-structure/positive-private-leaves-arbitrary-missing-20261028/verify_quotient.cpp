// Exact parity-quotient enumeration of split-graph Node Kayles bases.
// Independent vertices have 1- or 2-vertex clique neighborhoods.
// Run: c++ -std=c++17 -O3 -Wall -Wextra -pedantic verify_quotient.cpp -o /tmp/positive_leaves
//      /tmp/positive_leaves
// No proposed formula is used inside the Grundy recurrence.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>
using namespace std;

struct Result { long long total=0, bad=0; int maxg=0; };

static Result verify(int k) {
    vector<pair<int,int>> pairs;
    for(int i=0;i<k;i++)for(int j=i+1;j<k;j++)pairs.emplace_back(i,j);
    int m=(int)pairs.size();
    long long pairmax=1;
    for(int j=0;j<m;j++)pairmax*=3;
    Result out;
    for(int L=0;L<(1<<k);L++)for(long long P=0;P<pairmax;P++) {
        vector<int> leaves(k);
        for(int i=0;i<k;i++)leaves[i]=1+((L>>i)&1);
        vector<int> r(m);
        long long x=P;
        for(int j=0;j<m;j++){r[j]=(int)(x%3);x/=3;}
        vector<int> types,counts;
        for(int i=0;i<k;i++){types.push_back(1<<i);counts.push_back(leaves[i]);}
        for(int j=0;j<m;j++)if(r[j]){
            types.push_back((1<<pairs[j].first)|(1<<pairs[j].second));
            counts.push_back(r[j]);
        }
        const int states=1<<k;
        vector<int> active(states),incident(k),grundy(states);
        for(int S=0;S<states;S++)for(size_t j=0;j<types.size();j++)
            if(types[j]&S)active[S]^=counts[j]&1;
        for(size_t j=0;j<types.size();j++)for(int i=0;i<k;i++)
            if(types[j]&(1<<i))incident[i]^=counts[j]&1;
        for(int S=1;S<states;S++){
            unsigned int seen=0;
            // Playing clique vertex i deletes all clique vertices, and
            // every independent vertex adjacent to i.
            for(int i=0;i<k;i++)if(S&(1<<i))
                seen|=1u<<(active[S]^incident[i]);
            // Playing one independent vertex of neighborhood B removes B.
            // All other vertices whose last neighbor disappears become isolated.
            for(size_t j=0;j<types.size();j++)if(types[j]&S){
                int T=S&~types[j];
                int child=grundy[T]^(active[S]^active[T]^1);
                assert(child<31);
                seen|=1u<<child;
            }
            while(seen&(1u<<grundy[S]))grundy[S]++;
        }
        int u=active[states-1];
        bool uniform=all_of(incident.begin(),incident.end(),
                            [&](int v){return v==incident[0];});
        int predicted=uniform?(1^u^incident[0]):2+u;
        out.total++;
        out.maxg=max(out.maxg,grundy[states-1]);
        if(grundy[states-1]!=predicted){
            out.bad++;
            if(out.bad<=3)
                cerr<<"counterexample k="<<k<<" leavesMask="<<L
                    <<" pairTernary="<<P<<" actual="<<grundy[states-1]
                    <<" predicted="<<predicted<<"\n";
        }
    }
    return out;
}

int main(){
    const array<long long,4> totals={2,12,216,11664};
    const array<long long,4> bads={1,2,0,0};
    for(int k=1;k<=4;k++){
        Result r=verify(k);
        cout<<"k="<<k<<" total="<<r.total<<" bad="<<r.bad
            <<" maxGrundy="<<r.maxg<<"\n";
        assert(r.total==totals[k-1] && r.bad==bads[k-1]);
        if(k>=3)assert(r.maxg==3);
    }
    cout<<"PASS exhaustive bases k=3,4; sharpness k=1,2\n";
}
