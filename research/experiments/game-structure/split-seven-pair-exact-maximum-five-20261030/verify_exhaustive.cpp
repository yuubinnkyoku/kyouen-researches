// Seven-center degree-two split graph: exhaustive Node Kayles audit.
// Multiplicity 0/1/2 suffices by independent-twin parity compression.
// The 2^21 doubled-edge supports are partitioned into S7 orbits.
#include <bits/stdc++.h>
using namespace std;
constexpr int K=7,N=128,M=21;
int sig[M],inter[N];
int eval(unsigned odd,unsigned even){
 uint8_t p[N]={},g[N]={};
 for(int x=1;x<N;x++)p[x]=__builtin_parity(odd&inter[x]);
 unsigned odddeg=0;for(int i=0;i<K;i++)if(p[1<<i])odddeg|=1u<<i;
 unsigned present=odd|even;
 for(int x=1;x<N;x++){
  unsigned opts=0;
  if(x&odddeg)opts|=1u<<(p[x]^1);
  if(x&(~odddeg))opts|=1u<<p[x];
  for(unsigned z=present;z;z&=z-1){
   int j=__builtin_ctz(z);
   if(sig[j]&x){int y=x&~sig[j];opts|=1u<<(g[y]^p[x]^p[y]^1);}
  }
  g[x]=__builtin_ctz(~opts);
 }
 return g[N-1];
}
int main(int argc,char**argv){
 int j=0;
 for(int a=0;a<K;a++)for(int b=a+1;b<K;b++)sig[j++]=(1<<a)|(1<<b);
 for(int x=0;x<N;x++)for(int i=0;i<M;i++)if(sig[i]&x)inter[x]|=1<<i;
 int edge[7][7]={},ei=0;
 for(int a=0;a<7;a++)for(int b=a+1;b<7;b++)edge[a][b]=edge[b][a]=ei++;
 vector<int16_t> owner(1<<M,-1);
 vector<unsigned> reps;
 vector<int> weights;
 long long orbit_coverage=0;
 for(unsigned mask=0;mask<(1u<<M);mask++){
  if(owner[mask]!=-1)continue;
  int id=(int)reps.size(),perm[7]={0,1,2,3,4,5,6},size=0;
  do{
   unsigned transformed=0;int bit=0;
   for(int a=0;a<7;a++)for(int b=a+1;b<7;b++,bit++)
    if(mask>>bit&1)transformed|=1u<<edge[perm[a]][perm[b]];
   if(owner[transformed]==-1){owner[transformed]=id;size++;}
   else if(owner[transformed]!=id){cerr<<"orbit collision\n";return 2;}
  }while(next_permutation(perm,perm+7));
  reps.push_back(mask);weights.push_back(size);orbit_coverage+=size;
 }
 assert(reps.size()==1044 && orbit_coverage==(1<<M));
 for(auto id:owner)assert(id>=0);
 cerr<<"Verified 1044 disjoint orbits covering all 2^21 doubled supports.\n";
 unsigned long long global[10]={},byd[22][10]={};
 unsigned long long totalrepresentatives=0,global_weight=0;
 int bestcost[10];unsigned bestodd[10]={},besteven[10]={};
 fill(bestcost,bestcost+10,10000);
 size_t begin=argc>1?stoul(argv[1]):0,end=argc>2?stoul(argv[2]):reps.size();
 assert(begin<=end && end<=reps.size());
 for(size_t i=begin;i<end;i++){
  unsigned even=reps[i];int d=__builtin_popcount(even),n=M-d;
  int other[M],j=0;
  for(int e=0;e<M;e++)if(!(even>>e&1))other[j++]=e;
  assert(j==n);
  unsigned odd=0,prevgray=0;
  for(unsigned code=0;code<(1u<<n);code++){
   unsigned gray=code^(code>>1);
   if(code){int bit=__builtin_ctz(gray^prevgray);odd^=1u<<other[bit];}
   prevgray=gray;
   int g=eval(odd,even);
   if(g>=10){cerr<<"INVALID g="<<g<<"\n";return 2;}
   global[g]+=weights[i];byd[d][g]+=weights[i];
   int cost=__builtin_popcount(odd)+2*d;
   if(cost<bestcost[g]){bestcost[g]=cost;bestodd[g]=odd;besteven[g]=even;}
  }
  totalrepresentatives+=1u<<n;
  global_weight+=(unsigned long long)weights[i]*(1u<<n);
 }
 cerr<<"TOTAL representatives="<<totalrepresentatives<<" weighted="<<global_weight<<"\n";
 cout<<"HIST";
 for(int g=0;g<10;g++)cout<<" g"<<g<<"="<<global[g];
 cout<<"\n";
 for(int d=0;d<=21;d++){
  cout<<"D="<<d;
  for(int g=0;g<10;g++)cout<<" "<<byd[d][g];
  cout<<"\n";
 }
 for(int g=0;g<10;g++)if(bestcost[g]!=10000){
  cout<<"MIN g="<<g<<" independent="<<bestcost[g]
      <<" oddmask="<<bestodd[g]<<" evenmask="<<besteven[g]<<" sigs=";
  for(int j=0;j<M;j++){
   if(besteven[g]>>j&1)cout<<sig[j]<<","<<sig[j]<<",";
   else if(bestodd[g]>>j&1)cout<<sig[j]<<",";
  }
  cout<<"\n";
 }
 if(argc<2){
  assert(totalrepresentatives==12490035ULL && global_weight==10460353203ULL);
  assert(global[0]==82385617ULL && global[1]==82695704ULL);
  assert(global[2]==5147523591ULL && global[3]==5147720151ULL);
  assert(global[4]==18480ULL && global[5]==9660ULL);
  for(int g=6;g<10;g++)assert(global[g]==0);
  assert(bestcost[4]==10 && bestcost[5]==9);
 }
}
