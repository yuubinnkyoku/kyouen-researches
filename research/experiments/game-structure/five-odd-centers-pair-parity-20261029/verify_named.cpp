// Independent exact verification: named-vertex closed-neighborhood Node Kayles.
// Enumerates all 792 S5-orbits of 3^10 pair-multiplicity configurations.
// Build: g++ -O3 -std=c++17 verify_named.cpp -o verify_named
#include <bits/stdc++.h>
using namespace std;
using U = uint32_t;
static const int K=5, E=10;
vector<pair<int,int>> edges;
vector<array<int,E>> permaps;
vector<U> closed_, adj_;
unordered_map<U,unsigned char> memo;
size_t maxstates=0;

unsigned char rec(U mask) {
    if (!mask) return 0;
    auto it=memo.find(mask);
    if (it!=memo.end()) return it->second;
    U iso=0, tmp=mask;
    while (tmp) {
        U b=tmp&-tmp; tmp-=b;
        int i=__builtin_ctz(b);
        if (!(adj_[i]&mask)) iso|=b;
    }
    // An isolated component contributes its parity by xor.
    if (iso) {
        auto x=rec(mask&~iso)^(__builtin_popcount(iso)&1);
        memo.emplace(mask,x);
        return x;
    }
    bool seen[40]={};
    tmp=mask;
    while (tmp) {
        U b=tmp&-tmp; tmp-=b;
        int i=__builtin_ctz(b);
        seen[rec(mask&~closed_[i])]=true;
    }
    unsigned char ans=0;
    while (seen[ans]) ++ans;
    memo.emplace(mask,ans);
    return ans;
}
void add(vector<int> ns) {
    int v=adj_.size();
    adj_.push_back(0);
    closed_.push_back(0);
    for (int i:ns) {
        adj_[i]|=U(1)<<v;
        adj_[v]|=U(1)<<i;
    }
}
unsigned char named(const array<int,E>& c) {
    adj_.assign(K,0);
    closed_.assign(K,0);
    for (int i=0;i<K;i++) adj_[i]=((U(1)<<K)-1)^(U(1)<<i);
    for (int i=0;i<K;i++) add({i});
    for (int e=0;e<E;e++)
        for (int j=0;j<c[e];j++)
            add({edges[e].first,edges[e].second});
    for (int i=0;i<(int)adj_.size();i++)
        closed_[i]=adj_[i]|(U(1)<<i);
    memo.clear();
    unsigned char ans=rec((U(1)<<adj_.size())-1);
    maxstates=max(maxstates,memo.size());
    return ans;
}
array<int,E> decode(int n) {
    array<int,E> c{};
    for (int i=E-1;i>=0;i--) {
        c[i]=n%3; n/=3;
    }
    return c;
}
int main() {
    for (int i=0;i<K;i++)
        for (int j=i+1;j<K;j++) edges.push_back({i,j});
    array<int,K> p{};
    iota(p.begin(),p.end(),0);
    do {
        array<int,E> v{};
        for (int i=0;i<E;i++) {
            auto [a,b]=edges[i];
            if (p[a]>p[b]) swap(a,b);
            a=p[a]; b=p[b];
            v[i]=find(edges.begin(),edges.end(),make_pair(a,b))-edges.begin();
        }
        permaps.push_back(v);
    } while (next_permutation(p.begin(),p.end()));
    const int N=59049;
    vector<unsigned char> visited(N);
    int orbits=0;
    long long checked=0;
    int hist[4]={};
    auto encode=[](const array<int,E>&c) {
        int x=0;
        for (int v:c) x=3*x+v;
        return x;
    };
    for (int z=0;z<N;z++) {
        if (visited[z]) continue;
        auto c=decode(z);
        int sz=0;
        for (auto& p:permaps) {
            array<int,E> d{};
            for (int i=0;i<E;i++) d[p[i]]=c[i];
            int id=encode(d);
            if (!visited[id]) { visited[id]=1; sz++; }
        }
        auto a=named(c);
        auto parity=c;
        for (auto &v:parity) v&=1;
        auto b=named(parity);
        if (a!=b) {
            cerr<<"FAIL orbit "<<orbits<<" id "<<z
                <<" values "<<(int)a<<" "<<(int)b<<"\n";
            return 1;
        }
        if (a>3) { cerr<<"FAIL unexpected nimber "<<(int)a<<"\n"; return 1; }
        hist[a]+=sz;
        checked+=sz;
        orbits++;
    }
    if (orbits!=792 || checked!=N ||
        hist[0]!=1744 || hist[1]!=2225 ||
        hist[2]!=27780 || hist[3]!=27300) {
        cerr<<"FAIL orbit coverage or histogram\n";
        return 1;
    }
    cout<<"PASS 792/792 ternary isomorphism classes, "
        <<checked<<"/"<<N<<" labelled configurations\n";
    cout<<"Grundy histogram: "<<hist[0]<<","<<hist[1]
        <<","<<hist[2]<<","<<hist[3]<<"\n";
    cout<<"Maximum named memo states: "<<maxstates<<"\n";
}
