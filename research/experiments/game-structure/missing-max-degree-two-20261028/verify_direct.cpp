#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;

// Independent implementation: apply closed-neighbourhood deletion to each
// type of independent vertex, then quotient equal residual neighbourhoods.
// Counts 0/1/2 encode absent/positive odd/positive even twins.
struct State { int k; vector<int> leaf, pair; };
static unordered_map<string,uint8_t> memo;
static int norm(int x) { return x==0?0:(x&1?1:2); }
static int edge_index(int k,int a,int b) {
  if(a>b)swap(a,b);
  return a*(2*k-a-1)/2+b-a-1;
}
static string key(const State &s) {
  string out;out.push_back(char(s.k));
  for(int x:s.leaf)out.push_back(char(x));
  for(int x:s.pair)out.push_back(char(x));
  return out;
}
static int grundy(const State &s) {
  if(s.k==0)return 0;
  string id=key(s);auto it=memo.find(id);
  if(it!=memo.end())return it->second;
  int k=s.k;unsigned seen=0;
  // Clique vertex: all clique vertices disappear, leaving independent
  // vertices not incident to the chosen vertex, now isolated.
  for(int i=0;i<k;++i){
    int p=0;
    for(int j=0;j<k;++j)if(i!=j)p^=(s.leaf[j]&1);
    for(int a=0;a<k;++a)for(int b=a+1;b<k;++b)
      if(a!=i&&b!=i)p^=(s.pair[edge_index(k,a,b)]&1);
    seen|=1u<<p;
  }
  // A chosen independent vertex has one or two clique neighbours.
  vector<pair<int,int>> types;
  for(int i=0;i<k;++i)if(s.leaf[i])types.emplace_back(i,-1);
  for(int a=0;a<k;++a)for(int b=a+1;b<k;++b)
    if(s.pair[edge_index(k,a,b)])types.emplace_back(a,b);
  for(auto [a,b]:types){
    vector<int> remain,renumber(k,-1);
    for(int i=0;i<k;++i)if(i!=a&&i!=b){renumber[i]=(int)remain.size();remain.push_back(i);}
    State next{(int)remain.size(),vector<int>(remain.size(),0),vector<int>(remain.size()*(remain.size()-1)/2,0)};
    int isolated=0;
    // Process every old independent-vertex type, including the selected
    // type with its count decreased by one.
    auto distribute=[&](int x,int y,int count){
      if((x==a&&y==b) || (x==b&&y==a))--count;
      if(!count)return;
      int rx=(x>=0?renumber[x]:-1), ry=(y>=0?renumber[y]:-1);
      if(rx<0&&ry<0)isolated+=count;
      else if(rx<0)next.leaf[ry]+=count;
      else if(ry<0)next.leaf[rx]+=count;
      else next.pair[edge_index(next.k,rx,ry)]+=count;
    };
    for(int i=0;i<k;++i)distribute(i,-1,s.leaf[i]);
    for(int i=0;i<k;++i)for(int j=i+1;j<k;++j)
      distribute(i,j,s.pair[edge_index(k,i,j)]);
    for(int &x:next.leaf)x=norm(x);
    for(int &x:next.pair)x=norm(x);
    int child=grundy(next)^(isolated&1);
    assert(child<31);seen|=1u<<child;
  }
  int g=0;while(seen&(1u<<g))++g;
  memo.emplace(move(id),uint8_t(g));return g;
}
static int predicted(const State &s){
  int u=0;for(int x:s.leaf)u^=(x&1);
  for(int x:s.pair)u^=(x&1);
  vector<int> z=s.leaf;
  for(int i=0;i<s.k;++i)z[i]&=1;
  for(int i=0;i<s.k;++i)for(int j=i+1;j<s.k;++j){
    int v=s.pair[edge_index(s.k,i,j)]&1;z[i]^=v;z[j]^=v;
  }
  return all_of(z.begin(),z.end(),[&](int x){return x==z[0];})?(1^u^z[0]):(2+u);
}
static long long count_checked=0,failures=0;
static void test_mask(int k,int missing){
  vector<int> present;
  for(int i=0;i<k*(k-1)/2;++i)if(!(missing>>i&1))present.push_back(i);
  int choices=1<<present.size();int leaves=1;
  for(int i=0;i<k;++i)leaves*=3;
  for(int tcode=0;tcode<leaves;++tcode){
    State s{k,vector<int>(k),vector<int>(k*(k-1)/2,0)};
    int x=tcode;for(int &v:s.leaf){v=x%3;x/=3;}
    for(int bits=0;bits<choices;++bits){
      for(int i=0;i<(int)present.size();++i)s.pair[present[i]]=1+(bits>>i&1);
      int g=grundy(s),want=predicted(s);++count_checked;
      if(g!=want){
        ++failures;
        if(k>=5 || failures<=4){
          cerr<<"failure k="<<k<<" mask="<<missing<<" leaves="<<tcode<<" pairbits="<<bits<<" g="<<g<<" want="<<want<<"\n";
        }
        if(k>=5)exit(1);
      }
    }
  }
}
static int transform_mask(int k,int mask,const vector<int> &perm){
  int result=0;
  for(int a=0;a<k;++a)for(int b=a+1;b<k;++b)
    if(mask>>edge_index(k,a,b)&1)result|=1<<edge_index(k,perm[a],perm[b]);
  return result;
}
int main(){
  // k=4: exhaustive labelled missing graphs, max missing degree 2.
  for(int mask=0;mask<(1<<6);++mask){
    bool good=true;
    for(int i=0;i<4;++i){int deg=0;
      for(int j=0;j<4;++j)if(i!=j)deg+=(mask>>edge_index(4,i,j)&1);
      if(deg>2)good=false;
    }
    if(good)test_mask(4,mask);
  }
  cout<<"k4 checked="<<count_checked<<" failures="<<failures<<"\n";
  assert(count_checked==51516 && failures==4);
  // k=5: enumerate all 11 unlabelled missing graphs of maximum degree 2.
  set<int> representatives;vector<int> perm={0,1,2,3,4};
  vector<vector<int>> perms;
  do{perms.push_back(perm);}while(next_permutation(perm.begin(),perm.end()));
  for(int mask=0;mask<(1<<10);++mask){
    bool good=true;
    for(int i=0;i<5;++i){int deg=0;
      for(int j=0;j<5;++j)if(i!=j)deg+=(mask>>edge_index(5,i,j)&1);
      if(deg>2)good=false;
    }
    if(!good)continue;
    int rep=mask;
    for(auto &p:perms)rep=min(rep,transform_mask(5,mask,p));
    representatives.insert(rep);
  }
  assert(representatives.size()==11);
  auto before=count_checked;
  for(int mask:representatives)test_mask(5,mask);
  cout<<"k5 representatives="<<representatives.size()<<" checked="<<count_checked-before<<" failures="<<failures<<"\n";
  assert(count_checked-before==645408 && failures==4);
  // k=6 with six missing pairs and maximum degree two: only C6 and 2K3.
  auto mask_of=[&](const vector<pair<int,int>>&edges){
    int mask=0;for(auto [a,b]:edges)mask|=1<<edge_index(6,a,b);return mask;
  };
  before=count_checked;
  test_mask(6,mask_of({{0,1},{1,2},{2,3},{3,4},{4,5},{0,5}}));
  test_mask(6,mask_of({{0,1},{0,2},{1,2},{3,4},{3,5},{4,5}}));
  cout<<"k6 degree-two 6-edge cases checked="<<count_checked-before<<" failures="<<failures-4<<"\n";
  assert(count_checked-before==746496 && failures==4);
  cout<<"TOTAL checked="<<count_checked<<" memo="<<memo.size()<<"\n";
}
