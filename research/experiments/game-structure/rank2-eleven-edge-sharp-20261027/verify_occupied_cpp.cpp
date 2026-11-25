// Exact classification of rank-two residual forbidden-edge games with <= 11 edges.
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
    vector<int>d;for(int i=0;i<g.n;i++)d.push_back(g.degree(i));sort(d.begin(),d.end());
    string s=to_string(g.n)+":";
    for(int x:d)s+=to_string(x)+",";
    vector<int>component(g.n,-1),comp_v,comp_e;
    for(int i=0;i<g.n;i++)if(component[i]<0){
        int k=comp_v.size(), nv=0, degsum=0;
        vector<int>stack{i};component[i]=k;
        while(!stack.empty()){
            int v=stack.back();stack.pop_back();nv++;degsum+=g.degree(v);
            for(int w=0;w<g.n;w++)if(g.has(v,w)&&component[w]<0){component[w]=k;stack.push_back(w);}
        }
        comp_v.push_back(nv);comp_e.push_back(degsum/2);
    }
    vector<pair<int,int>> comps;
    for(int i=0;i<(int)comp_v.size();i++)comps.emplace_back(comp_v[i],comp_e[i]);
    sort(comps.begin(),comps.end());s+=':';
    for(auto [v,e]:comps)s+=to_string(v)+"-"+to_string(e)+",";
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
    vector<int8_t> memo(size,-1);
    auto recurse=[&](auto&& self,int chosen)->int {
        int8_t &val=memo[chosen];
        if(val>=0)return val;
        uint32_t seen=0;
        for(int v=0;v<g.n;v++){
            if((chosen>>v)&1)continue;
            if(g.adj[v] & chosen)continue;
            int z=self(self,chosen | (1<<v));
            assert(z<31);seen|=1u<<z;
        }
        int mex=0;while((seen>>mex)&1u)mex++;
        val=mex;return mex;
    };
    return recurse(recurse,0);
}

int main(){
    // Explicit sharpness witness: nine rank-two edges and one isolated/free vertex.
    Graph sharp(11);
    for(auto [u,v]:vector<pair<int,int>>{{0,1},{0,2},{0,3},{1,4},{2,4},
                                        {3,5},{4,6},{7,8},{7,9}})sharp.add(u,v);
    assert(grundy(sharp)==7);
    Graph core(10);
    for(int i=0;i<10;i++)core.adj[i]=sharp.adj[i];
    assert(grundy(core)==6);
    Graph ten(12), eleven(12);
    for(auto [u,v]:vector<pair<int,int>>{{0,1},{0,2},{0,3},{1,4},{2,4},{3,5},{4,6},{7,8},{7,9},{10,11}})ten.add(u,v);
    for(auto [u,v]:vector<pair<int,int>>{{0,1},{0,2},{0,3},{0,4},{1,2},{1,3},{2,5},{5,6},{7,8},{7,9},{10,11}})eleven.add(u,v);
    assert(grundy(ten)==7 && grundy(eleven)==7);
    vector<Graph>prev{Graph(0)};
    const vector<int> expected_n{0,1,2,5,11,26,68,177,497,1476,4613,15216};
    const vector<vector<int>> expected_hist{
        {},{0,1},{1,0,1},{1,3,0,1},{5,1,3,2},
        {5,10,4,7},{22,15,18,13},{43,55,33,43,3},
        {136,121,118,105,14,3},{366,405,309,309,56,28,3},
        {1173,1138,963,925,235,161,15,3},
        {3712,3722,2929,3014,920,809,75,35}
    };
    for(int e=1;e<=11;e++){
        vector<Graph>next;
        unordered_map<string,vector<int>>buckets;
        for(const Graph&g:prev){
            auto add_candidate=[&](int u,int v){
                Graph h(max(g.n,max(u,v)+1));
                for(int i=0;i<g.n;i++)h.adj[i]=g.adj[i];
                h.add(u,v);
                string key=invariant(h);
                for(int id:buckets[key])if(isomorphic(h,next[id]))return;
                buckets[key].push_back((int)next.size());next.push_back(move(h));
            };
            for(int i=0;i<g.n;i++)for(int j=i+1;j<g.n;j++)if(!g.has(i,j))add_candidate(i,j);
            for(int i=0;i<g.n;i++)add_candidate(i,g.n);
            add_candidate(g.n,g.n+1);
        }
        vector<int>hist(20,0);int maxg=-1;Graph witness;
        for(const Graph&g:next){int z=grundy(g);hist[z]++;if(z>maxg){maxg=z;witness=g;}}
        assert((int)next.size()==expected_n[e]);
        for(int i=0;i<20;i++)assert(hist[i]==(i<(int)expected_hist[e].size()?expected_hist[e][i]:0));
        cout<<"edges="<<e<<" unlabeled_graphs="<<next.size()<<" histogram=";
        for(int i=0;i<=maxg;i++)cout<<(i?",":"")<<hist[i];
        int free_max=0;for(int i=0;i<20;i++)if(hist[i])free_max=max(free_max,max(i,i^1));
        cout<<" max="<<maxg<<" max_with_free="<<free_max<<" witness_n="<<witness.n<<" witness_edges=";
        for(auto [u,v]:witness.edges())cout<<"("<<u<<","<<v<<")";
        cout<<"\n";
        prev=move(next);
    }
}
