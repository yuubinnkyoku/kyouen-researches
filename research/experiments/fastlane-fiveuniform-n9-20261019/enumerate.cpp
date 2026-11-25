#include <bits/stdc++.h>
using namespace std;
// Enumerate all simple 4-uniform hypergraphs with exactly five edges, on n vertices.
// By relabelling one edge can be fixed to {0,1,2,3}; this is a complete coverage, not an isomorphism quotient.
int main(int argc,char**argv){
 int n=argc>1?atoi(argv[1]):8;
 if(n<4||n>12) return 2;
 vector<int> edges; for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)for(int d=c+1;d<n;d++)edges.push_back((1<<a)|(1<<b)|(1<<c)|(1<<d));
 int first=15; assert(edges[0]==first); int M=edges.size();
 int E[5], all=(1<<n)-1; E[0]=first;
 vector<unsigned char> g(1<<n); array<unsigned long long,16> hist{};
 unsigned long long total=0,cover=0,linear=0;
 int maxg=-1,maxlinear=-1; array<int,5> witness{},linearWitness{}; array<int,16> linearHist{};
 auto evaluate=[&](){
  total++; int uni=0;for(int x:E)uni|=x;
  if(uni!=all)return;
  cover++;
  bool lin=true; for(int i=0;i<5;i++)for(int j=0;j<i;j++)if(__builtin_popcount((unsigned)(E[i]&E[j]))>=3)lin=false;
  if(lin)linear++;
  // bottom-up over occupied subsets; 255 marks forbidden.
  for(int s=all;s>=0;s--){
   bool bad=false;for(int x:E)if((s&x)==x){bad=true;break;}
   if(bad){g[s]=255;continue;}
   unsigned int options=0;
   for(int rest=(all^s);rest;rest&=rest-1){int t=rest&-rest;int v=g[s|t];if(v!=255)options|=1u<<v;}
   g[s]=__builtin_ctz(~options);
  }
  int x=g[0];hist[x]++;if(lin){linearHist[x]++;if(x>maxlinear){maxlinear=x;copy(E,E+5,linearWitness.begin());}}if(x>maxg){maxg=x;copy(E,E+5,witness.begin());}
 };
 for(int a=1;a<M-3;a++)for(int b=a+1;b<M-2;b++)for(int c=b+1;c<M-1;c++)for(int d=c+1;d<M;d++){
  E[1]=edges[a];E[2]=edges[b];E[3]=edges[c];E[4]=edges[d];evaluate();
 }
 cout<<"n="<<n<<" all="<<total<<" cover="<<cover<<" linear-cover="<<linear<<" max="<<maxg<<"\n";
 for(int i=0;i<16;i++)if(hist[i])cout<<"g="<<i<<" count="<<hist[i]<<"\n";
 cout<<"witness=";for(int x:witness)cout<<x<<",";cout<<"\n";
 cout<<"linear-max="<<maxlinear<<"\n";for(int i=0;i<16;i++)if(linearHist[i])cout<<"linear-g="<<i<<" count="<<linearHist[i]<<"\n";
 cout<<"linear-witness=";for(int x:linearWitness)cout<<x<<",";cout<<"\n";
}
