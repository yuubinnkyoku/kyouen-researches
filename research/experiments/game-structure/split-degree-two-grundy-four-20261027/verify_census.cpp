// Independent exhaustive census of 5-clique / 8 independent vertices,
// where each independent vertex has one or two neighbors in the clique.
// Uses direct 13-vertex closed-neighborhood recursion, not signature projection.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <set>
#include <vector>
using namespace std;

constexpr int K=5, I=8, N=K+I, FULL=(1<<N)-1;
array<int,N> closed{};
array<int,1<<N> visited{},memo{};
int epoch=0;
array<long long,8> histogram{};
long long total=0, g4_count=0;
int min_cross=100;
vector<int> types;
vector<int> chosen(I);
set<vector<int>> expected_orbit, observed;

int grundy(int mask){
 if(mask==0)return 0;
 if(visited[mask]==epoch)return memo[mask];
 int seen=0,remain=mask;
 while(remain){
  int v=__builtin_ctz((unsigned)remain);
  remain&=remain-1;
  seen|=1<<grundy(mask&~closed[v]);
 }
 int g=0;while(seen&(1<<g))g++;
 visited[mask]=epoch;memo[mask]=g;
 return g;
}

void inspect(){
 for(int j=0;j<K;j++)closed[j]=(1<<K)-1;
 int cross=0;
 for(int j=0;j<I;j++){
  int s=types[chosen[j]];
  int v=K+j;
  closed[v]=(1<<v)|s;
  cross+=__builtin_popcount((unsigned)s);
  for(int c=0;c<K;c++)if(s&(1<<c))closed[c]|=1<<v;
 }
 ++epoch;
 int g=grundy(FULL);
 if(g>=8){cerr<<"unexpected grundy="<<g<<"\n";exit(1);}
 histogram[g]++;total++;
 if(g==4){
  g4_count++;
  min_cross=min(min_cross,cross);
  vector<int> v;
  for(int j=0;j<I;j++)v.push_back(types[chosen[j]]);
  observed.insert(v);
  if(!expected_orbit.count(v)){
   cerr<<"unexpected g4 witness";for(int s:v)cerr<<" "<<s;cerr<<"\n";exit(2);
  }
 }
}

void enumerate(int pos,int from){
 if(pos==I){inspect();return;}
 for(int j=from;j<(int)types.size();j++){
  chosen[pos]=j;
  enumerate(pos+1,j);
 }
}

int main(){
 for(int s=1;s<(1<<K);s++)if(__builtin_popcount((unsigned)s)<=2)types.push_back(s);
 vector<int> p={0,1,2,3,4};
 do{
  vector<int> witness={1,3,3,5,5,9,9,16};
  for(int &s:witness){
   int t=0;for(int j=0;j<K;j++)if(s&(1<<j))t|=1<<p[j];
   s=t;
  }
  sort(witness.begin(),witness.end());
  expected_orbit.insert(witness);
 }while(next_permutation(p.begin(),p.end()));
 enumerate(0,0);
 cout<<"all_multisets="<<total<<"\n";
 cout<<"grundy_histogram=";
 for(int i=0;i<8;i++)cout<<(i?",":"")<<histogram[i];
 cout<<"\n";
 cout<<"g4_multisets="<<g4_count<<" orbit_size="<<expected_orbit.size()
     <<" distinct_witnesses="<<observed.size()<<" min_cross_edges="<<min_cross<<"\n";
 if(total!=319770||g4_count!=20||expected_orbit!=observed||min_cross!=14)return 3;
 cout<<"all checks passed\n";
}
