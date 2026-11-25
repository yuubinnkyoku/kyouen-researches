// Exact 5-circuit pair codegrees in the binary cube, anchored at zero.
// g++ -O3 -std=c++17 five_circuit_pair_codegrees.cpp -o /tmp/five-pair && /tmp/five-pair
#include <bits/stdc++.h>
using namespace std;
int rank101(const int* a,int n,int d){
 int m[4][6]={};
 for(int i=1;i<n;i++)for(int j=0;j<d;j++)
  m[i-1][j]=(((a[i]>>j)&1)-((a[0]>>j)&1)+101)%101;
 int r=0;
 for(int c=0;c<d&&r<n-1;c++){
  int p=r;while(p<n-1&&!m[p][c])++p;
  if(p==n-1)continue;
  for(int j=c;j<d;j++)swap(m[p][j],m[r][j]);
  int inv=1;while(inv*m[r][c]%101!=1)++inv;
  for(int j=c;j<d;j++)m[r][j]=m[r][j]*inv%101;
  for(int i=r+1;i<n-1;i++){
   int t=m[i][c];
   for(int j=c;j<d;j++)m[i][j]=(m[i][j]-t*m[r][j]%101+101)%101;
  }++r;
 }return r;
}
int choose(int n,int k){int x=1;for(int i=1;i<=k;i++)x=x*(n-i+1)/i;return x;}
int main(){
 const long long expected[4][7]={
  {0,6,12,2,0,0,0},{0,48,84,56,12,0,0},
  {0,250,400,400,200,50,0},{0,1080,1650,1960,1470,660,180}
 };
 const long long total_expected[]={5,50,325,1750};
 for(int d=3;d<=6;d++){
  int N=1<<d,a[5]={0};long long hist[7]={},total=0;
  for(a[1]=1;a[1]<N;a[1]++)
  for(a[2]=a[1]+1;a[2]<N;a[2]++)
  for(a[3]=a[2]+1;a[3]<N;a[3]++)
  for(a[4]=a[3]+1;a[4]<N;a[4]++){
   if(rank101(a,5,d)!=3)continue;
   bool minimal=true;
   for(int omit=0;omit<5;omit++){
    int b[4],k=0;
    for(int j=0;j<5;j++)if(j!=omit)b[k++]=a[j];
    if(rank101(b,4,d)!=3){minimal=false;break;}
   }
   if(!minimal)continue;
   total++;
   for(int j=1;j<5;j++)hist[__builtin_popcount((unsigned)a[j])]++;
  }
  assert(total==total_expected[d-3]);
  long long check=0;
  for(int h=1;h<=d;h++){
   assert(hist[h]==expected[d-3][h]);
   assert(hist[h]%choose(d,h)==0);
   check+=hist[h];
   cout<<"d="<<d<<" h="<<h<<" pair_codegree="<<hist[h]/choose(d,h)<<"\n";
  }
  assert(check==4*total);
 }
}
