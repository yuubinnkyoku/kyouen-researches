#include <array>
#include <cassert>
#include <cstdio>
#include <map>
#include <utility>
#include <vector>
using namespace std;
struct GH { int g,h; };

GH values(int n,const vector<pair<int,int>>& edges) {
    array<int,8> adj{};
    for(int i=0;i<n;++i) adj[i]=1<<i;
    for(auto [a,b]:edges){adj[a]|=1<<b;adj[b]|=1<<a;}
    array<GH,256> memo{};
    array<unsigned char,256> seen{};
    auto rec=[&](auto&& self,int mask)->GH {
        if(seen[mask])return memo[mask];
        seen[mask]=1;
        if(!mask)return memo[mask]={0,1};
        unsigned gset=0,hset=0;
        for(int v=0;v<n;++v)if(mask>>v&1){
            GH child=self(self,mask&~adj[v]);
            gset|=1u<<child.g;
            hset|=1u<<child.h;
        }
        int g=0,h=0;
        while(gset>>g&1)++g;
        while(hset>>h&1)++h;
        return memo[mask]={g,h};
    };
    return rec(rec,(1<<n)-1);
}
bool connected(int n,const vector<pair<int,int>>& edges){
    int seen=1;
    for(int i=0;i<n;++i)for(auto [a,b]:edges){
        if(seen>>a&1)seen|=1<<b;
        if(seen>>b&1)seen|=1<<a;
    }
    return seen==(1<<n)-1;
}
int main(){
    const int expected[6][4]={
        {1,1,0,0},{2,1,0,0},{8,4,0,0},
        {64,38,0,0},{1024,728,0,0},{32768,26704,150,60}
    };
    for(int n=1;n<=6;++n){
        vector<pair<int,int>> pairs;
        for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)pairs.emplace_back(a,b);
        int total=0,con=0,bad=0,badcon=0;
        for(int mask=0;mask<(1<<pairs.size());++mask){
            vector<pair<int,int>> edges;
            for(int j=0;j<(int)pairs.size();++j)
                if(mask>>j&1)edges.push_back(pairs[j]);
            GH p=values(n,edges);
            bool iscon=connected(n,edges);
            ++total;con+=iscon;
            if(p.h!=(p.g<=1?(p.g^1):p.g)){
                ++bad;badcon+=iscon;
                assert(n==6 && p.g==0 && p.h==0);
                if(iscon){
                    assert(edges.size()==6);
                    array<int,6> degree{};
                    for(auto [a,b]:edges){++degree[a];++degree[b];}
                    for(int d:degree)assert(d==2);
                }
            }
        }
        assert(total==expected[n-1][0] && con==expected[n-1][1]
            && bad==expected[n-1][2] && badcon==expected[n-1][3]);
        printf("graphs n=%d total=%d connected=%d bad=%d bad_connected=%d\n",
               n,total,con,bad,badcon);
    }
    const long long expected_bad[8]={0,0,0,0,0,0,0,45360};
    for(int n=1;n<=8;++n){
        long long lim=1;
        for(int i=0;i<n-2;++i)lim*=n;
        long long bad=0;
        map<pair<int,int>,long long> pairs;
        for(long long sequence=0;sequence<lim;++sequence){
            vector<int> code(n>=2?n-2:0);
            long long z=sequence;
            for(int &v:code){v=z%n;z/=n;}
            vector<int> degree(n,1);
            for(int v:code)++degree[v];
            vector<pair<int,int>> edges;
            for(int v:code){
                int leaf=0;
                while(degree[leaf]!=1)++leaf;
                edges.emplace_back(leaf,v);
                --degree[leaf];--degree[v];
            }
            if(n>=2){
                int a=-1,b=-1;
                for(int i=0;i<n;++i)if(degree[i]==1){
                    if(a<0)a=i;else b=i;
                }
                edges.emplace_back(a,b);
            }
            GH p=values(n,edges);
            if(p.h!=(p.g<=1?(p.g^1):p.g)){
                ++bad;++pairs[{p.g,p.h}];
            }
        }
        assert(bad==expected_bad[n-1]);
        if(n==8){
            assert((pairs[{1,4}]==25200));
            assert((pairs[{4,1}]==20160));
        }
        printf("trees n=%d labeled=%lld bad=%lld\n",n,lim,bad);
    }
}
