#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>
using namespace std;
int main(){
  for(long long n: {55250LL,143650LL,320450LL}){
    long long m=0;
    for(long long b=1;b*b<n;b+=2){
      long long a2=n-b*b;
      long long a=(long long)sqrtl(a2);
      while((a+1)*(a+1)<=a2)++a;
      while(a*a>a2)--a;
      if(a>0&&(a&1)&&a*a==a2)m=b;
    }
    long long d=(1+m*m-n)/4;
    vector<int> ys;
    for(long long y=0;y<=m;++y){
      int hits=0;
      for(long long x=-1000;x<=1000;++x)
        if(x*x+y*y+x-m*y+d==0)++hits;
      if(hits==2)ys.push_back((int)y);
      else if(hits!=0){cerr<<"Unexpected hit count "<<hits<<"\n";return 1;}
    }
    cout<<n<<" "<<m<<" "<<d<<" "<<ys.size()<<" ";
    for(int y:ys)cout<<y<<",";
    cout<<"\n";
  }
}
