// Exhaustive six-point affine circuits in {0,1}^d, d=4 or 5.
// g++ -O3 -std=c++17 six_circuit_support.cpp -o six && ./six 4 && ./six 5
#include <array>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;
int affine_rank(const vector<int>& a,int d) {
  int b[6][6]={}, n=(int)a.size();
  for(int i=0;i<n;i++) {
    b[i][0]=1;
    for(int j=0;j<d;j++) b[i][j+1]=(a[i]>>j)&1;
  }
  int r=0;
  for(int c=0;c<=d;c++) {
    int k=r;
    while(k<n && b[k][c]==0) ++k;
    if(k==n) continue;
    for(int j=c;j<=d;j++) swap(b[k][j],b[r][j]);
    int inv=1;
    while(inv*b[r][c]%101!=1) ++inv;
    for(int j=c;j<=d;j++) b[r][j]=b[r][j]*inv%101;
    for(int i=r+1;i<n;i++) {
      int z=b[i][c];
      for(int j=c;j<=d;j++) b[i][j]=(b[i][j]-z*b[r][j]%101+101)%101;
    }
    ++r;
    if(r==n) break;
  }
  return r;
}
int main(int argc,char**argv) {
  if(argc!=2) return 2;
  int d=atoi(argv[1]);
  if(d!=4 && d!=5) return 2;
  int N=1<<d;
  long long total=0, hist[6]={};
  for(int i=0;i<N;i++) for(int j=i+1;j<N;j++)
  for(int k=j+1;k<N;k++) for(int l=k+1;l<N;l++)
  for(int m=l+1;m<N;m++) for(int n=m+1;n<N;n++) {
    vector<int>a={i,j,k,l,m,n};
    if(affine_rank(a,d)==6) continue;
    bool minimal=true;
    for(int z=0;z<6;z++) {
      vector<int>b;
      for(int t=0;t<6;t++) if(t!=z) b.push_back(a[t]);
      if(affine_rank(b,d)!=5) {minimal=false;break;}
    }
    if(!minimal) continue;
    ++total;
    int mask=0;
    for(int v:a) mask|=v^i;
    ++hist[__builtin_popcount((unsigned)mask)];
  }
  cout<<"d="<<d<<" circuits="<<total;
  for(int s=0;s<=d;s++) cout<<" support_"<<s<<"="<<hist[s];
  cout<<"\n";
}
