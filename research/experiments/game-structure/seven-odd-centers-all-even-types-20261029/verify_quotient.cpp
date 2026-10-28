// Seven odd centers: exhaustive verification for one even-type count d.
// Compile: g++ -O3 -std=c++17 verify_quotient.cpp -o /tmp/seven-quotient-all
// Run separately for d=7,...,21 to keep the memo table bounded.
#include <bits/stdc++.h>
using namespace std;
static constexpr int K=7, M=21, N=1<<M;
static constexpr long long expected[22]={
 1044,10962,56318,187891,457353,866643,1333604,
 1717692,1893854,1816347,1530018,1135359,739558,418986,
 203596,83337,28088,7567,1563,232,22,1
};
vector<pair<int,int>> edges;
int idx[7][7], swmap[6][21];
uint32_t swap_adjacent(uint32_t x,int t){
 uint32_t y=0;
 while(x){int b=__builtin_ctz(x);x&=x-1;y|=1u<<swmap[t][b];}
 return y;
}
unordered_map<string,uint8_t> memo;
int sg(int k,vector<uint8_t> a){
 int iso=a[0]&1; a[0]=0;
 string key;key.reserve(a.size()+1);key.push_back(char(k));
 for(auto x:a)key.push_back(char(x));
 auto it=memo.find(key);
 if(it!=memo.end())return it->second^iso;
 uint64_t opts=0;int n=1<<k;
 // A center move deletes every center and every incident independent vertex.
 for(int i=0;i<k;i++){
  int p=0;
  for(int s=1;s<n;s++)if(!(s>>i&1))p^=a[s]&1;
  opts|=1ULL<<p;
 }
 // Move on one independent vertex of support s.
 for(int s=1;s<n;s++)if(a[s]){
  int rem[7],kk=0;
  for(int i=0;i<k;i++)if(!(s>>i&1))rem[kk++]=i;
  vector<uint8_t>b(1<<kk,0);
  for(int t=1;t<n;t++)if(a[t]){
   int support=0;
   for(int j=0;j<kk;j++)if(t>>rem[j]&1)support|=1<<j;
   b[support]+=a[t];
  }
  b[0]--;b[0]&=1;
  for(int j=1;j<(1<<kk);j++)if(b[j]>2)b[j]=(b[j]&1)?1:2;
  opts|=1ULL<<sg(kk,b);
 }
 int g=__builtin_ctzll(~opts);
 memo.emplace(move(key),(uint8_t)g);
 return g^iso;
}
int main(int argc,char**argv){
 if(argc!=2){cerr<<"usage: verify_quotient d (7..21)\n";return 2;}
 int d=atoi(argv[1]);
 if(d<7||d>21)return 2;
 for(int i=0;i<7;i++)for(int j=i+1;j<7;j++){
  idx[i][j]=idx[j][i]=edges.size();edges.emplace_back(i,j);
 }
 for(int t=0;t<6;t++)for(int e=0;e<21;e++){
  auto [i,j]=edges[e];
  if(i==t)i=t+1;else if(i==t+1)i=t;
  if(j==t)j=t+1;else if(j==t+1)j=t;
  swmap[t][e]=idx[i][j];
 }
 vector<uint8_t>seen(N);
 vector<uint32_t>orbit,reps;orbit.reserve(5040);reps.reserve(1044);
 for(uint32_t mask=0;mask<N;mask++){
  if(seen[mask])continue;
  orbit.clear();orbit.push_back(mask);seen[mask]=1;
  for(size_t i=0;i<orbit.size();i++)for(int t=0;t<6;t++){
   uint32_t x=swap_adjacent(orbit[i],t);
   if(!seen[x]){seen[x]=1;orbit.push_back(x);}
  }
  reps.push_back(mask);
 }
 if(reps.size()!=1044){cerr<<"wrong orbit count\n";return 1;}
 long long checked=0,errors=0;int nrep=0;
 for(uint32_t mask:reps){
  vector<uint8_t>a(128,0);
  for(int i=0;i<7;i++)a[1<<i]=1;
  vector<int>absent;
  for(int e=0;e<21;e++){
   auto [i,j]=edges[e];int s=(1<<i)|(1<<j);
   if(mask>>e&1)a[s]=1;else absent.push_back(s);
  }
  int base=sg(7,a);
  function<void(int,int)>visit=[&](int start,int left){
   if(!left){
    checked++;int g=sg(7,a);
    if(g!=base){errors++;cerr<<"FAIL mask="<<mask<<" d="<<d<<" base="<<base<<" got="<<g<<"\n";exit(1);}
    return;
   }
   for(int x=start;x<=(int)absent.size()-left;x++){
    a[absent[x]]=2;visit(x+1,left-1);a[absent[x]]=0;
   }
  };
  if((int)absent.size()>=d)visit(0,d);
  if(++nrep%10==0){memo.clear();memo.rehash(0);}
 }
 cout<<"d="<<d<<" orbit_reps="<<reps.size()<<" checked="<<checked
     <<" expected="<<expected[d]<<" mismatches="<<errors<<"\n";
 return checked!=expected[d]||errors?1:0;
}
