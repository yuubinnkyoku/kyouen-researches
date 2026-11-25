// Independent, named-vertex closed-neighbourhood recursion for all six-center ternary orbits.
#include <bits/stdc++.h>
using namespace std;
struct Named {
 vector<uint64_t> adj;
 unordered_map<uint64_t,unsigned char> cache;
 int sg(uint64_t mask){
  uint64_t isolated=0;
  for(uint64_t p=mask;p;p&=p-1){int v=__builtin_ctzll(p);if(!(adj[v]&mask))isolated|=1ULL<<v;}
  int iso=__builtin_popcountll(isolated)&1;
  mask &= ~isolated;
  if(!mask)return iso;
  auto it=cache.find(mask);if(it!=cache.end())return it->second^iso;
  uint64_t opts=0;
  for(uint64_t p=mask;p;p&=p-1){int v=__builtin_ctzll(p);
   int g=sg(mask&~(adj[v]|(1ULL<<v)));
   opts|=1ULL<<g;
  }
  int g=__builtin_ctzll(~opts);
  cache.emplace(mask,(unsigned char)g);
  return g^iso;
 }
 int value(int code,bool reduce){
  adj.clear();cache.clear();
  auto add=[&](){adj.push_back(0);return (int)adj.size()-1;};
  auto connect=[&](int a,int b){adj[a]|=1ULL<<b;adj[b]|=1ULL<<a;};
  for(int i=0;i<6;i++)add();
  for(int i=0;i<6;i++)for(int j=i+1;j<6;j++)connect(i,j);
  for(int i=0;i<6;i++){int v=add();connect(i,v);}
  for(int i=0;i<6;i++)for(int j=i+1;j<6;j++){
   int count=code%3;code/=3;if(reduce)count&=1;
   for(int r=0;r<count;r++){int v=add();connect(i,v);connect(j,v);}
  }
  if(adj.size()>63)abort();
  return sg((1ULL<<adj.size())-1);
 }
};
int main(int argc,char**argv){
 int step=argc>1?atoi(argv[1]):1;
 int pw[16];pw[0]=1;for(int i=1;i<=15;i++)pw[i]=pw[i-1]*3;
 int ix[6][6],e=0;vector<pair<int,int>> edges;
 for(int i=0;i<6;i++)for(int j=i+1;j<6;j++){ix[i][j]=ix[j][i]=e++;edges.emplace_back(i,j);}
 int maps[5][15];for(int t=0;t<5;t++){
  int p[6]={0,1,2,3,4,5};swap(p[t],p[t+1]);
  for(int j=0;j<15;j++)maps[t][j]=ix[p[edges[j].first]][p[edges[j].second]];
 }
 vector<unsigned char> seen(pw[15]);vector<int> q;q.reserve(720);
 Named a,b;long long orbits=0,checked=0,errors=0,max_cache=0; array<long long,16> histogram{}, simple_histogram{}; array<int,16> simple_class_histogram{}; long long checked_cases=0, simple_cases=0, simple_classes=0;
 auto t0=chrono::steady_clock::now();
 for(int code=0;code<pw[15];code++){
  if(seen[code])continue;
  q.clear();q.push_back(code);seen[code]=1;
  for(size_t h=0;h<q.size();h++){
   int x=q[h],d[15];for(int j=0;j<15;j++){d[j]=x%3;x/=3;}
   for(int t=0;t<5;t++){
    int y=0;for(int j=0;j<15;j++)y+=d[j]*pw[maps[t][j]];
    if(!seen[y]){seen[y]=1;q.push_back(y);}
   }
  }
  if(orbits%step==0 || code==pw[15]-1){
   int v=a.value(code,false),w=b.value(code,true);
   if(v!=w){cout<<"FAIL code="<<code<<" g="<<v<<" parity_g="<<w<<"\n";errors++;}
   max_cache=max({max_cache,(long long)a.cache.size(),(long long)b.cache.size()});
   histogram[v]+=q.size();checked_cases+=q.size();
   int tmp=code;bool binary=true;
   for(int j=0;j<15;j++){if(tmp%3==2)binary=false;tmp/=3;}
   if(binary){simple_histogram[v]+=q.size();simple_class_histogram[v]++;simple_cases+=q.size();simple_classes++;}
   checked++;
  }
  orbits++;
  if(checked%500==0 && orbits%step==1)cerr<<"checked "<<checked<<" orbits "<<orbits<<"\n";
 }
 cout<<"orbits="<<orbits<<" checked_named="<<checked<<" mismatches="<<errors<<" max_cache="<<max_cache<<" checked_cases="<<checked_cases<<"\n";
 cout<<"simple_cases="<<simple_cases<<" simple_classes="<<simple_classes<<"\n";
 for(int i=0;i<16;i++)if(histogram[i])cout<<"g="<<i<<" ternary="<<histogram[i]<<" simple="<<simple_histogram[i]<<" simple_classes="<<simple_class_histogram[i]<<"\n";
 cerr<<"seconds="<<chrono::duration<double>(chrono::steady_clock::now()-t0).count()<<"\n";
 if(step==1 && (errors || checked!=25506 || checked_cases!=pw[15] || simple_cases!=32768 || simple_classes!=156 || histogram[0]!=455625 || histogram[1]!=443232 || histogram[2]!=6721950 || histogram[3]!=6728100 || simple_histogram[0]!=1024 || simple_histogram[1]!=1024 || simple_histogram[2]!=15360 || simple_histogram[3]!=15360))return 1;
}
