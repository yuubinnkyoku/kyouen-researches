// Exact support-count mex verifier: seven odd centers, up to six even pair types.
// Usage: g++ -O3 -std=c++17 verify_quotient.cpp -o /tmp/seven-quotient
//        /tmp/seven-quotient /tmp/seven-representatives.tsv
#include <bits/stdc++.h>
using namespace std;
unordered_map<string,uint8_t> memo;
int sg(int k,vector<uint8_t> a){
 int iso=a[0]&1;a[0]=0;
 string key;key.reserve(a.size()+1);key.push_back(char(k));
 for(uint8_t x:a)key.push_back(char(x));
 auto it=memo.find(key);if(it!=memo.end())return it->second^iso;
 uint64_t opts=0;int n=1<<k;
 for(int i=0;i<k;i++){
  int p=0;for(int s=1;s<n;s++)if(!(s>>i&1))p^=a[s]&1;
  opts|=1ULL<<p;
 }
 for(int s=1;s<n;s++)if(a[s]){
  int remaining[7],kk=0;
  for(int i=0;i<k;i++)if(!(s>>i&1))remaining[kk++]=i;
  vector<uint8_t>b(1<<kk,0);
  for(int t=1;t<n;t++)if(a[t]){
   int support=0;
   for(int j=0;j<kk;j++)if(t>>remaining[j]&1)support|=1<<j;
   b[support]+=a[t];
  }
  b[0]--;b[0]&=1;
  for(int j=1;j<(1<<kk);j++)if(b[j]>2)b[j]=(b[j]&1)?1:2;
  opts|=1ULL<<sg(kk,b);
 }
 int g=__builtin_ctzll(~opts);
 memo.emplace(std::move(key),(uint8_t)g);
 return g^iso;
}
int main(int argc,char**argv){
 if(argc!=2){cerr<<"usage: verify_quotient representatives.tsv\n";return 2;}
 ifstream f(argv[1]);if(!f)return 2;
 string line;getline(f,line);
 vector<pair<int,int>>edges;
 for(int i=0;i<7;i++)for(int j=i+1;j<7;j++)edges.emplace_back(i,j);
 long long checked=0,errors=0,per[7]={};
 int classes=0;
 while(getline(f,line)){
  if(line.empty())continue;
  istringstream ss(line);int mask,orbit,expected,missing;
  ss>>mask>>orbit>>expected>>missing;
  vector<int>absent;
  for(int e=0;e<21;e++)if(!(mask>>e&1))absent.push_back(e);
  vector<uint8_t>a(128,0);
  for(int i=0;i<7;i++)a[1<<i]=1;
  for(int e=0;e<21;e++)if(mask>>e&1){
   auto [i,j]=edges[e];a[(1<<i)|(1<<j)]=1;
  }
  int g=sg(7,a);
  if(g!=expected){cerr<<"BASE mismatch "<<mask<<"\n";return 1;}
  classes++;
  int d=0;
  function<void(int,int)>check=[&](int start,int left){
   if(!left){
    checked++;per[d]++;
    int v=sg(7,a);
    if(v!=g){errors++;cerr<<"FAIL "<<mask<<" g="<<g<<" v="<<v<<"\n";}
    return;
   }
   for(int x=start;x<=(int)absent.size()-left;x++){
    auto[i,j]=edges[absent[x]];int s=(1<<i)|(1<<j);
    a[s]=2;check(x+1,left-1);a[s]=0;
   }
  };
  for(d=4;d<=6;d++)if(missing>=d)check(0,d);
  if(classes%10==0){memo.clear();memo.rehash(0);}
 }
 cout<<"classes="<<classes<<" checked4="<<per[4]<<" checked5="<<per[5]
     <<" checked6="<<per[6]<<" mismatches="<<errors<<"\n";
 return (classes!=1044||per[4]!=457353||per[5]!=866643||
         per[6]!=1333604||errors)?1:0;
}
