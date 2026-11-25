// Exhaustive 5-subset census of {0,1}^6, no rank calculations.
// g++ -O3 -std=c++17 d6_support.cpp -o d6_support && ./d6_support
#include <cstdio>
int main(){
 long long candidates[7]={}, circuits[7]={};
 for(int a=0;a<60;a++)for(int b=a+1;b<61;b++)for(int c=b+1;c<62;c++)
 for(int d=c+1;d<63;d++)for(int e=d+1;e<64;e++){
  int v[5]={a,b,c,d,e}; int degree[5]={}; bool adj[5][5]={};
  int k=0,edges=0; bool singleton=false;
  for(int j=0;j<6;j++){
   int mask=0;
   for(int i=0;i<5;i++)if((v[i]>>j)&1)mask|=1<<i;
   int z=__builtin_popcount((unsigned)mask);
   if(z==0||z==5)continue;
   ++k;
   if(z==1||z==4){singleton=true;break;}
   if(z==3)mask^=31;
   int x=-1,y=-1;
   for(int i=0;i<5;i++)if(mask>>i&1){if(x<0)x=i;else y=i;}
   if(!adj[x][y]){adj[x][y]=true;++degree[x];++degree[y];++edges;}
  }
  if(singleton)continue;
  ++candidates[k];
  int maximum=0,isolated=0;
  for(int x:degree){if(x>maximum)maximum=x;if(x==0)++isolated;}
  if(edges==3&&maximum==3&&isolated==1)++circuits[k];
 }
 long long total=0;
 for(int k=0;k<=6;k++){
  printf("k=%d singleton-free=%lld circuits=%lld\\n",k,candidates[k],circuits[k]);
  total+=circuits[k];
 }
 printf("total=%lld\\n",total);
 return total==22400?0:1;
}
