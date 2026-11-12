// Enumerate connected min-degree-two n-vertex (n+3)-edge graphs by canonical cores.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <string>
#include <utility>
#include <vector>
using namespace std;
int n,b,cm,typesN; vector<pair<int,int>> types,cedges; vector<int> lens; array<int,6> deg{}; array<array<int,6>,6> mat{}; set<string> seen; uint64_t labeled=0,uniqueC=0,assignments=0,freeC=0,sat=0; ofstream candidates;
string key(const vector<int>& p){string s;for(int i=0;i<b;i++)for(int j=i;j<b;j++)s+=char('A'+mat[p[i]][p[j]]);return s;}
string canonical(){vector<int> p(b);iota(p.begin(),p.end(),0);string best=key(p);while(next_permutation(p.begin(),p.end()))best=min(best,key(p));return best;}
bool connected(){int seenMask=1,old=0;while(seenMask!=old){old=seenMask;for(int u=0;u<b;u++)if(seenMask>>u&1)for(int v=0;v<b;v++)if(mat[u][v])seenMask|=1<<v;}return seenMask==(1<<b)-1;}
bool witness(unsigned adj[13]){for(int u=0;u<n;u++)for(int v=u+1;v<n;v++)if(__builtin_popcount(adj[u]&adj[v])>=2)return false;freeC++;for(int u=0;u<n;u++)for(int v=u+1;v<n;v++)if(!(adj[u]>>v&1)){unsigned tmp=adj[u];bool ok=false;while(tmp){int x=__builtin_ctz(tmp);tmp&=tmp-1;if(adj[x]&adj[v]){ok=true;break;}}if(!ok)return false;}return true;}
void test(){unsigned adj[13]={};int nxt=b;for(size_t i=0;i<cedges.size();i++){auto [u,v]=cedges[i];int last=u;for(int j=1;j<lens[i];j++){adj[last]|=1u<<nxt;adj[nxt]|=1u<<last;last=nxt++;}adj[last]|=1u<<v;adj[v]|=1u<<last;}if(nxt!=n){cerr<<"invalid vertices\n";exit(3);}assignments++; candidates<<b; for(size_t i=0;i<cedges.size();i++) candidates<<" "<<cedges[i].first<<","<<cedges[i].second<<","<<lens[i]; candidates<<"\n"; if(witness(adj)) sat++;}
void assign(int i,int left){if(i==cm){if(!left)test();return;}auto [u,v]=cedges[i];int minlen=u==v?3:1;if(i&&cedges[i]==cedges[i-1]){minlen=max(minlen,lens[i-1]);if(u!=v&&minlen==1)minlen=2;}int tail=0;for(int j=i+1;j<cm;j++)tail+=cedges[j].first==cedges[j].second?3:1;for(int x=minlen;x<=left-tail;x++){lens.push_back(x);assign(i+1,left-x);lens.pop_back();}}
void evaluate(){if(*min_element(deg.begin(),deg.begin()+b)<3||!connected())return;labeled++;string k=canonical();if(!seen.insert(k).second)return;uniqueC++;cedges.clear();for(auto [u,v]:types)for(int z=0;z<mat[u][v];z++)cedges.emplace_back(u,v);assign(0,n+3);}
void gen(int i,int left){if(i==typesN){if(!left)evaluate();return;}auto [u,v]=types[i];for(int k=0;k<=left;k++){mat[u][v]=mat[v][u]=k;deg[u]+=k;deg[v]+=k;gen(i+1,left-k);deg[u]-=k;deg[v]-=k;}mat[u][v]=mat[v][u]=0;}
int main(int argc,char**argv){if(argc!=3)return 2;n=atoi(argv[1]);if(n<6||n>13)return 2;candidates.open(argv[2]);if(!candidates)return 2;for(b=1;b<=min(n,6);b++){cm=b+3;types.clear();mat={};deg.fill(0);seen.clear();labeled=uniqueC=assignments=freeC=sat=0;for(int i=0;i<b;i++)for(int j=i;j<b;j++)types.emplace_back(i,j);typesN=types.size();gen(0,cm);cout<<"branches="<<b<<" labelled_cores="<<labeled<<" core_types="<<uniqueC<<" assignments="<<assignments<<" c4_free="<<freeC<<" saturated="<<sat<<endl;}}
