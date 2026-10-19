// Independent C++ audit: labelled subset recurrence against profile recurrence.
#include <algorithm>
#include <cassert>
#include <functional>
#include <iostream>
#include <map>
#include <numeric>
#include <random>
#include <set>
#include <vector>
using namespace std;
using V=vector<int>;
static int mex(const set<int>& s){int v=0;while(s.count(v))++v;return v;}
static long long choose(int n,int k){long long v=1;for(int i=1;i<=k;i++)v=v*(n-i+1)/i;return v;}
void check(const V& sizes, const vector<V>& profiles){
    int n=accumulate(sizes.begin(),sizes.end(),0), d=(int)sizes.size();
    assert(n<=14);
    vector<int> which(n);int off=0;
    for(int i=0;i<d;i++)for(int j=0;j<sizes[i];j++)which[off++]=i;
    vector<int> forbidden;
    for(int mask=1;mask<(1<<n);mask++){
        V cnt(d);for(int v=0;v<n;v++)if(mask>>v&1)cnt[which[v]]++;
        for(const auto& p:profiles)if(cnt==p){forbidden.push_back(mask);break;}
    }
    auto safe_label=[&](int mask){for(int e:forbidden)if((mask&e)==e)return false;return true;};
    auto safe_count=[&](const V& a){for(const auto& p:profiles){bool contains=true;for(int i=0;i<d;i++)if(a[i]<p[i])contains=false;if(contains)return false;}return true;};
    map<int,int> lmemo;
    function<int(int)> lg=[&](int mask)->int{
        auto it=lmemo.find(mask);if(it!=lmemo.end())return it->second;
        set<int> s;for(int v=0;v<n;v++)if(!(mask>>v&1)&&safe_label(mask|(1<<v)))s.insert(lg(mask|(1<<v)));
        return lmemo[mask]=mex(s);
    };
    map<V,int> cmemo;
    function<int(V)> cg=[&](V a)->int{
        auto it=cmemo.find(a);if(it!=cmemo.end())return it->second;
        set<int> s;for(int i=0;i<d;i++)if(a[i]<sizes[i]){a[i]++;if(safe_count(a))s.insert(cg(a));a[i]--;}
        return cmemo[a]=mex(s);
    };
    map<int,long long> ls,cs;
    for(int mask=0;mask<(1<<n);mask++){
        V a(d);for(int v=0;v<n;v++)if(mask>>v&1)a[which[v]]++;
        assert(safe_label(mask)==safe_count(a));
        if(!safe_label(mask))continue;
        assert(lg(mask)==cg(a));
        bool terminal=true;
        for(int v=0;v<n;v++)if(!(mask>>v&1)&&safe_label(mask|(1<<v)))terminal=false;
        if(terminal)ls[__builtin_popcount((unsigned)mask)]++;
    }
    V a(d);
    function<void(int)> enumerate=[&](int i){
        if(i==d){
            if(!safe_count(a))return;
            bool terminal=true;
            for(int j=0;j<d;j++)if(a[j]<sizes[j]){a[j]++;if(safe_count(a))terminal=false;a[j]--;}
            if(terminal){long long weight=1;int total=0;for(int j=0;j<d;j++){weight*=choose(sizes[j],a[j]);total+=a[j];}cs[total]+=weight;}
            return;
        }
        for(a[i]=0;a[i]<=sizes[i];a[i]++)enumerate(i+1);
    };
    enumerate(0);
    assert(ls==cs);
}
int main(){
    mt19937 rng(20261020);int tests=0;
    for(const V& sizes: {V{2,3},V{3,3},V{2,3,2},V{3,2,3},V{2,2,2,2},V{3,3,2,2}}){
        V p(sizes.size());vector<V> options;
        function<void(int)> gen=[&](int i){if(i==(int)sizes.size()){
            int sum=accumulate(p.begin(),p.end(),0);if(sum>=2&&sum<=4)options.push_back(p);return;}
            for(p[i]=0;p[i]<=sizes[i];p[i]++)gen(i+1);
        };gen(0);
        for(int rep=0;rep<120;rep++){
            vector<V> chosen;for(auto q:options)if(rng()%7==0)chosen.push_back(q);
            check(sizes,chosen);tests++;
        }
    }
    cout<<"PASS C++ independent planted profiles="<<tests<<"\n";
}
