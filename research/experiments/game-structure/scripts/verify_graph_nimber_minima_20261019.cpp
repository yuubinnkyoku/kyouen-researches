// Independent occupied-set recurrence for the Node Kayles graph witnesses.
// g(occupied)=mex{g(occupied | (1<<v)) : v not occupied and no occupied neighbor}.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>
using namespace std;
using Edge = pair<int,int>;
const vector<Edge> G3 = {{0,1},{0,2}};
const vector<Edge> G7 = {{0,1},{0,2},{0,5},{1,4},{2,3},{3,5},{3,6}};
const vector<Edge> G13 = {{0,1},{0,2},{0,4},{0,5},{1,2},{1,3},{1,6},{3,6},{5,6},{8,10},{9,10},{11,12},{2,11},{7,11},{8,11}};
struct Graph {int n;vector<Edge> edges;};
Graph join(initializer_list<Graph> parts){Graph g{0,{}};for(const auto &p:parts){for(auto [u,v]:p.edges)g.edges.push_back({u+g.n,v+g.n});g.n+=p.n;}return g;}
struct Solver{
 int n; vector<uint32_t> adj; vector<int8_t> memo;
 Solver(const Graph&g):n(g.n),adj(n),memo(1u<<n,-1){for(auto [u,v]:g.edges){assert(u>=0&&u<v&&v<n);adj[u]|=1u<<v;adj[v]|=1u<<u;}}
 int solve(uint32_t occupied){auto &ans=memo[occupied];if(ans!=-1)return ans;uint32_t seen=0;for(int v=0;v<n;v++)if(!(occupied>>v&1)&&!(adj[v]&occupied)){int child=solve(occupied|(1u<<v));seen|=1u<<child;}ans=__builtin_ctz(~seen);return ans;}
};
int main(){
 vector<Graph> gs={ {0,{}},{1,{}},{3,G3},join({{3,G3},{1,{}}}),{7,G7},join({{7,G7},{1,{}}}),join({{7,G7},{3,G3}}),join({{7,G7},{3,G3},{1,{}}}),{13,G13},join({{13,G13},{1,{}}}),join({{13,G13},{3,G3}}),join({{13,G13},{3,G3},{1,{}}})};
 const vector<int> sizes={0,1,3,4,7,8,10,11,13,14,16,17};
 for(int k=0;k<(int)gs.size();k++){assert(gs[k].n==sizes[k]);Solver s(gs[k]);int g=s.solve(0);assert(g==k);cout<<"witness g="<<k<<" n="<<gs[k].n<<" edges="<<gs[k].edges.size()<<"\n";}
 for(int n=0;n<=6;n++){vector<Edge> pairs;for(int u=0;u<n;u++)for(int v=u+1;v<n;v++)pairs.push_back({u,v});array<int,5> hist={};for(uint32_t bits=0;bits<(1u<<pairs.size());bits++){Graph gr{n,{}};for(int i=0;i<(int)pairs.size();i++)if(bits>>i&1)gr.edges.push_back(pairs[i]);Solver s(gr);int g=s.solve(0);assert(g>=0&&g<=4);hist[g]++;}cout<<"n="<<n<<" histogram=";for(int k=0;k<5;k++)cout<<(k?",":"")<<hist[k];cout<<"\n";}
}
