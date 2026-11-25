// Exact classification of rank-two residual forbidden-edge games with <= 12 edges.
// C++17, no dependencies. Every graph has no isolated vertices; extra free vertices xor 1.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
struct Graph {
    int n=0;
    vector<uint32_t> adj;
    Graph()=default;
    Graph(int N):n(N),adj(N,0){}
    bool has(int u,int v) const {return (adj[u]>>v)&1;}
    void add(int u,int v){adj[u]|=1u<<v;adj[v]|=1u<<u;}
    int degree(int u)const{return __builtin_popcount(adj[u]);}
    vector<pair<int,int>> edges()const{
        vector<pair<int,int>> out;
        for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(has(i,j))out.emplace_back(i,j);
        return out;
    }
};
// A necessary invariant; collisions are always resolved by exact isomorphism.
string invariant(const Graph&g){
    // Exact isomorphism resolves all collisions of this necessary invariant.
    vector<string> signatures;
    int triangles=0;
    for(int i=0;i<g.n;i++){
        vector<int> nd;
        for(int j=0;j<g.n;j++)if(g.has(i,j))nd.push_back(g.degree(j));
        sort(nd.begin(),nd.end());
        int tri=0;
        for(int j=0;j<g.n;j++)if(g.has(i,j))
            for(int k=j+1;k<g.n;k++)if(g.has(i,k)&&g.has(j,k))tri++;
        triangles+=tri;
        string s=to_string(g.degree(i))+":"+to_string(tri)+":";
        for(int d:nd)s+=to_string(d)+",";
        signatures.push_back(s);
    }
    sort(signatures.begin(),signatures.end());
    string s=to_string(g.n)+":"+to_string(triangles/3)+":";
    for(const string&sig:signatures){s+=sig;s+=';';}
    return s;
}
bool isomorphic(const Graph&a,const Graph&b){
    if(a.n!=b.n)return false;
    int n=a.n;
    vector<int>order(n),used(n,0),mapping(n,-1);
    iota(order.begin(),order.end(),0);
    sort(order.begin(),order.end(),[&](int u,int v){
        if(a.degree(u)!=a.degree(v))return a.degree(u)>a.degree(v);
        int su=0,sv=0;
        for(int w=0;w<n;w++){if(a.has(u,w))su+=a.degree(w);if(a.has(v,w))sv+=a.degree(w);}
        return su>sv;
    });
    auto recurse=[&](auto&&self,int depth)->bool{
        if(depth==n)return true;
        int u=order[depth];
        for(int v=0;v<n;v++)if(!used[v]&&a.degree(u)==b.degree(v)){
            bool okay=true;
            for(int j=0;j<depth;j++)if(a.has(u,order[j])!=b.has(v,mapping[order[j]])){okay=false;break;}
            if(!okay)continue;
            mapping[u]=v;used[v]=1;
            if(self(self,depth+1))return true;
            mapping[u]=-1;used[v]=0;
        }
        return false;
    };
    return recurse(recurse,0);
}
int grundy(const Graph&g){
    int size=1<<g.n;
    vector<int8_t>memo(size,-1);
    auto recurse=[&](auto&&self,int avail)->int{
        if(!avail)return 0;
        int8_t& val=memo[avail];if(val>=0)return val;
        uint32_t seen=0;
        for(int x=avail;x;x&=x-1){
            int v=__builtin_ctz(x);
            int child=avail & ~(int(g.adj[v])|(1<<v));
            int z=self(self,child);assert(z<31);seen|=1u<<z;
        }
        int mex=0;while((seen>>mex)&1u)mex++;
        val=mex;return mex;
    };
    return recurse(recurse,size-1);
}
int grundy_occupied(const Graph&g){
    const int size=1<<g.n;
    vector<int8_t> memo(size,-1);
    auto dfs=[&](auto&&self,int chosen)->int{
        int8_t& val=memo[chosen];
        if(val>=0)return val;
        uint32_t seen=0;
        for(int v=0;v<g.n;v++){
            if((chosen>>v)&1)continue;
            if(g.adj[v]&chosen)continue;
            int z=self(self,chosen|(1<<v));
            assert(z<31);seen|=1u<<z;
        }
        int mex=0;while((seen>>mex)&1u)mex++;
        val=mex;return mex;
    };
    return dfs(dfs,0);
}
int main(){
    // Connected classes are complete: delete a non-bridge cycle edge, or a leaf edge.
    vector<Graph> prev{Graph(2)};prev[0].add(0,1);
    long long dp[13][32] = {};dp[0][0]=1;
    const long long expected_counts[13]={1,1,2,5,11,26,68,177,497,1476,4613,15216,52944};
    const vector<vector<long long>> expected_hist={
        {1},{0,1},{1,0,1},{1,3,0,1},{5,1,3,2},{5,10,4,7},
        {22,15,18,13},{43,55,33,43,3},{136,121,118,105,14,3},
        {366,405,309,309,56,28,3},{1173,1138,963,925,235,161,15,3},
        {3712,3722,2929,3014,920,809,75,35},
        {12522,12305,10047,9943,3818,3643,434,232}
    };
    for(int e=1;e<=12;e++){
        vector<Graph>next;
        if(e==1)next=prev;
        else{
            unordered_map<string,vector<int>>buckets;
            for(const Graph&g:prev){
                auto add_candidate=[&](int u,int v){
                    Graph h(max(g.n,max(u,v)+1));
                    for(int i=0;i<g.n;i++)h.adj[i]=g.adj[i];
                    h.add(u,v);
                    string key=invariant(h);
                    auto& bucket=buckets[key];
                    for(int id:bucket)if(isomorphic(h,next[id]))return;
                    bucket.push_back((int)next.size());next.push_back(move(h));
                };
                for(int i=0;i<g.n;i++)
                    for(int j=i+1;j<g.n;j++)if(!g.has(i,j))add_candidate(i,j);
                for(int i=0;i<g.n;i++)add_candidate(i,g.n);
            }
        }
        vector<int> chist(32,0);
        Graph witness;bool witness_found=false;
        for(const Graph&g:next){
            int z=grundy(g);
            int independent=grundy_occupied(g);
            if(z!=independent){
                cerr<<"MISMATCH at e="<<e<<endl;return 2;
            }
            if(e==12 && z==7 && !witness_found){
                witness=g;witness_found=true;
            }
            chist[z]++;
            // Unbounded knapsack over individual connected isomorphism types.
            for(int t=e;t<=12;t++)
                for(int x=0;x<32;x++)dp[t][x]+=dp[t-e][x^z];
        }
        long long cnt=0;int maxg=-1;
        for(int x=0;x<32;x++)if(dp[e][x]){cnt+=dp[e][x];maxg=x;}
        cout<<"edges="<<e<<" connected_classes="<<next.size()<<" connected_hist=";
        for(int i=0;i<32;i++)if(chist[i])cout<<i<<":"<<chist[i]<<",";
        cout<<" all_classes="<<cnt<<" all_hist=";
        for(int i=0;i<=maxg;i++)cout<<(i?",":"")<<dp[e][i];
        cout<<" max="<<maxg<<endl;
        assert(cnt==expected_counts[e]);
        for(int x=0;x<32;x++)
            assert(dp[e][x]==(x<(int)expected_hist[e].size()?expected_hist[e][x]:0));
        if(e==12){
            cout<<"connected_g7_witness_n="<<witness.n<<" edges=";
            for(auto [u,v]:witness.edges())cout<<"("<<u<<","<<v<<")";
            cout<<endl;
        }
        prev=move(next);
    }
}
