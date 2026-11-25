#include <bits/stdc++.h>
using namespace std;
unordered_map<string,unsigned char> memo;
long long calls=0;
int grundy(int k, vector<unsigned char> a) {
    int iso=a[0]&1; a[0]=0;
    string key; key.reserve(a.size()+1); key.push_back(char(k));
    for(auto x:a)key.push_back(char(x));
    auto it=memo.find(key); if(it!=memo.end())return (int)it->second ^ iso;
    calls++;
    unsigned options=0;
    int n=1<<k;
    for(int i=0;i<k;i++){
        int parity=0;
        for(int s=1;s<n;s++)if(!(s>>i&1))parity^=(a[s]&1);
        options|=1u<<parity;
    }
    for(int s=1;s<n;s++)if(a[s]){
        int map[6],kk=0; for(int i=0;i<k;i++)if(!(s>>i&1))map[kk++]=i;
        vector<unsigned char> b(1<<kk,0);
        for(int t=1;t<n;t++)if(a[t]){
            int v=0;for(int j=0;j<kk;j++)if(t>>map[j]&1)v|=1<<j;
            b[v]+=a[t];
        }
        b[0]--; // remove selected independent vertex (now isolated)
        b[0]&=1;
        for(int j=1;j<(1<<kk);j++)if(b[j]>2)b[j]=(b[j]&1)?1:2;
        int g=grundy(kk,b);options|=1u<<g;
    }
    int g=0;while(options>>g&1)g++;
    memo.emplace(std::move(key),(unsigned char)g);
    return g^iso;
}

int main(){
 const int k=6,E=15;vector<pair<int,int>> edges;
 for(int i=0;i<k;i++)for(int j=i+1;j<k;j++)edges.emplace_back(i,j);
 int pow3[16];pow3[0]=1;for(int i=1;i<=15;i++)pow3[i]=pow3[i-1]*3;
 int edge_index[6][6];for(int i=0;i<E;i++){auto [u,v]=edges[i];edge_index[u][v]=edge_index[v][u]=i;}
 int maps[5][15];for(int t=0;t<5;t++){
  int perm[6]={0,1,2,3,4,5};swap(perm[t],perm[t+1]);
  for(int e=0;e<E;e++){auto [u,v]=edges[e];maps[t][e]=edge_index[perm[u]][perm[v]];}
 }
 vector<unsigned char> visited(pow3[15],0);
 vector<unsigned char> simple(1<<15);
 auto make_counts=[&](int code,bool ternary){
  vector<unsigned char> a(1<<k,0);
  for(int i=0;i<k;i++)a[1<<i]=1;
  for(int e=0;e<E;e++){
   int d=ternary?(code%3):(code&1);code=ternary?(code/3):(code>>1);
   auto [u,v]=edges[e];a[(1<<u)|(1<<v)]=d;
  }
  return a;
 };
 for(int mask=0;mask<(1<<E);mask++)simple[mask]=grundy(k,make_counts(mask,false));
 cerr<<"simple complete: cache "<<memo.size()<<"\n";
 {
  vector<unsigned char> binary_seen(1<<E,0);vector<int> binary_q;
  array<int,16> class_hist{};
  int nclasses=0;
  for(int mask=0;mask<(1<<E);mask++){
   if(binary_seen[mask])continue;
   binary_q.clear();binary_q.push_back(mask);binary_seen[mask]=1;
   for(size_t h=0;h<binary_q.size();h++){
    int x=binary_q[h];
    for(int t=0;t<5;t++){
     int y=0;for(int e=0;e<E;e++)if(x>>e&1)y|=1<<maps[t][e];
     if(!binary_seen[y]){binary_seen[y]=1;binary_q.push_back(y);}
    }
   }
   nclasses++;class_hist[simple[mask]]++;
   if(simple[mask]<=1){
    cout<<"low_nimber_class mask="<<mask<<" g="<<(int)simple[mask]<<" orbit="<<binary_q.size()<<"\n";
   }
  }
  if(nclasses!=156 || class_hist[0]!=20 || class_hist[1]!=12 || class_hist[2]!=62 || class_hist[3]!=62)return 1;
  cout<<"simple_isomorphism_classes="<<nclasses<<"\n";
  for(int g=0;g<16;g++)if(class_hist[g])cout<<"g="<<g<<" class_count="<<class_hist[g]<<"\n";
 }

 long long n_orbits=0,n_cases=0,n_bad=0;array<long long,16> hist{};
 int maxg=0,max_orbit=0;
 vector<int> queue;queue.reserve(720);
 auto start=chrono::steady_clock::now();
 for(int code=0;code<pow3[E];code++){
  if(visited[code])continue;
  queue.clear();queue.push_back(code);visited[code]=1;
  for(size_t head=0;head<queue.size();head++){
   int x=queue[head];int digits[15];for(int e=0;e<E;e++){digits[e]=x%3;x/=3;}
   for(int t=0;t<5;t++){
    int y=0;for(int e=0;e<E;e++)y+=digits[e]*pow3[maps[t][e]];
    if(!visited[y]){visited[y]=1;queue.push_back(y);}
   }
  }
  int binary=0,copy=code;
  for(int e=0;e<E;e++){int d=copy%3;copy/=3;if(d==1)binary|=1<<e;}
  int g=grundy(k,make_counts(code,true));int expected=simple[binary];
  n_cases+=queue.size();n_orbits++;hist[g]+=queue.size();maxg=max(maxg,g);max_orbit=max(max_orbit,(int)queue.size());
  if(g!=expected){n_bad++;cout<<"COUNTEREXAMPLE ternary_code="<<code<<" binary_mask="<<binary<<" g="<<g<<" parity_g="<<expected<<" orbit="<<queue.size()<<"\n";}
  if(n_orbits%5000==0)cerr<<"orbits "<<n_orbits<<" cases "<<n_cases<<" memo "<<memo.size()<<"\n";
 }
 cout<<"total="<<n_cases<<" orbits="<<n_orbits<<" mismatch_orbits="<<n_bad<<" max_g="<<maxg<<" max_orbit="<<max_orbit<<" cache="<<memo.size()<<"\n";
 for(int i=0;i<16;i++)if(hist[i])cout<<"g="<<i<<" count="<<hist[i]<<"\n";
 cerr<<"seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"\n";
 if(n_bad || n_cases!=pow3[E] || n_orbits!=25506 || maxg!=3 || hist[0]!=455625 || hist[1]!=443232 || hist[2]!=6721950 || hist[3]!=6728100)return 1;
}
