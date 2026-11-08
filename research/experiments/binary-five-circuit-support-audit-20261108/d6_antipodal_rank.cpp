// Independent affine-rank census of 5-point circuits in {0,1}^6.
// Compile: c++ -O3 -std=c++17 d6_antipodal_rank.cpp -o audit && ./audit
#include <array>
#include <iostream>
using namespace std;
template<int N> int rank_rows(int a[N][7]) {
  int r=0;
  for(int c=0;c<7 && r<N;c++) {
    int z=r; while(z<N && !a[z][c]) ++z;
    if(z==N) continue;
    for(int k=c;k<7;k++) swap(a[z][k],a[r][k]);
    int inv=1; while(inv*a[r][c]%101!=1) ++inv;
    for(int i=r+1;i<N;i++) if(a[i][c]) {
      int f=a[i][c]*inv%101;
      for(int k=c;k<7;k++) a[i][k]=(a[i][k]-f*a[r][k]%101+101)%101;
    }
    ++r;
  }
  return r;
}
template<int N> int affine_rank(const array<int,N>& p) {
  int a[N][7];
  for(int i=0;i<N;i++) {
    a[i][0]=1;
    for(int j=0;j<6;j++) a[i][j+1]=(p[i]>>j)&1;
  }
  return rank_rows<N>(a);
}
int main() {
  long long total=0,cir=0,unique=0,bad=0,fixed=0,support[7]={};
  array<int,5> p;
  for(p[0]=0;p[0]<60;p[0]++)
  for(p[1]=p[0]+1;p[1]<61;p[1]++)
  for(p[2]=p[1]+1;p[2]<62;p[2]++)
  for(p[3]=p[2]+1;p[3]<63;p[3]++)
  for(p[4]=p[3]+1;p[4]<64;p[4]++) {
    ++total;
    if(affine_rank(p)!=4) continue;
    bool minimal=true;
    for(int skip=0;skip<5;skip++) {
      array<int,4> q; int t=0;
      for(int i=0;i<5;i++) if(i!=skip) q[t++]=p[i];
      if(affine_rank(q)!=4) {minimal=false;break;}
    }
    if(!minimal) continue;
    ++cir;
    int ones=63,zeros=63;
    for(int x:p) {ones&=x;zeros&=(~x)&63;}
    int mask=63^(ones|zeros);
    ++support[__builtin_popcount((unsigned)mask)];
    int n=0;
    for(int i=0;i<5;i++) for(int j=i+1;j<5;j++)
      if(((p[i]^p[j])&mask)==mask) ++n;
    if(n==1) ++unique; else ++bad;
    bool has0=false,has63=false;
    for(int x:p) {has0|=x==0;has63|=x==63;}
    if(has0&&has63) ++fixed;
  }
  cout<<total<<" "<<cir<<" "<<unique<<" "<<bad<<" "<<fixed<<"\n";
  for(long long x:support) cout<<x<<" ";
  cout<<"\n";
}
// All relevant minors are 0/1 determinants of order <=5.
// Hadamard bound: |det| <= 5^(5/2) < 101, so rank mod 101 equals rank over Q.
