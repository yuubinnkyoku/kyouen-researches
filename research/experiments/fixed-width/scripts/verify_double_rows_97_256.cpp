// Independent integer enumeration in the X-coordinate, CSV comparison and direct substitution.
// Usage: ./verify_double_rows_97_256 path/to/double_rows_97_256.csv
#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
using ll=long long;
ll root(ll n) {ll x=sqrtl((long double)n);while((x+1)*(x+1)<=n)++x;while(x*x>n)--x;return x;}
vector<ll> rowlist(ll n){
 vector<ll> ys;
 for(ll x=1;x*x<n;x+=2){ll z=n-x*x,y=root(z);if(y*y==z&&(y&1)){ys.push_back(y);ys.push_back(-y);}}
 sort(ys.begin(),ys.end());ys.erase(unique(ys.begin(),ys.end()),ys.end());return ys;
}
int main(int argc,char**argv){
 if(argc!=2)return 1;
 map<ll,vector<ll>> cache;
 const map<ll,int> counts={{59283250,128},{296416250,160},{770682250,192},{2430613250LL,256}};
 for(auto [n,count]:counts){auto v=rowlist(n);if((int)v.size()!=count){cerr<<"bad count "<<n<<"\n";return 2;}cache[n]=move(v);}
 ifstream f(argv[1]);if(!f)return 3;
 string line;getline(f,line);if(!line.empty()&&line.back()=='\r')line.pop_back();if(line!="k,w,N,Ylo,Yhi,C,D")return 4;
 int lines=0;
 while(getline(f,line)){
  if(line.empty())continue;
  replace(line.begin(),line.end(),',',' ');
  istringstream ss(line);ll k,w,n,lo,hi,c,d;
  if(!(ss>>k>>w>>n>>lo>>hi>>c>>d))return 5;
  if(k!=97+lines || !counts.count(n))return 6;
  auto& v=cache.at(n);int nwin=0;ll best=INT64_MAX;
  for(int i=0;i+(int)k<=(int)v.size();i++){
   ll width=(v[i+(int)k-1]-v[i])/2+1;
   best=min(best,width);
   if(v[i]==lo && v[i+(int)k-1]==hi && width==w)nwin++;
  }
  if(nwin==0||best!=w||lo!=-c||4*d!=1+c*c-n)return 7;
  // Compare against all four candidates; tie-breaking is Python's lexicographic (w,lo,hi,n).
  ll bw=INT64_MAX,blo=0,bhi=0,bn=0;
  for(auto &[nn, vv]:cache)if((int)vv.size()>=k){
   for(int i=0;i+(int)k<=(int)vv.size();i++){
    ll ww=(vv[i+(int)k-1]-vv[i])/2+1;
    auto cand=make_tuple(ww,vv[i],vv[i+(int)k-1],nn);
    if(bw==INT64_MAX||cand<make_tuple(bw,blo,bhi,bn))tie(bw,blo,bhi,bn)=cand;
   }
  }
  if(tie(w,lo,hi,n)!=tie(bw,blo,bhi,bn))return 8;
  int hit=0;
  for(ll Y: v)if(lo<=Y&&Y<=hi){
   ll X=root(n-Y*Y);if(X<=0||X*X+Y*Y!=n)return 9;
   for(ll XX:{X,-X}){ll x=(XX-1)/2,y=(Y-lo)/2;
    if(x*x+y*y+x-c*y+d!=0 || y<0||y>=w)return 10;}
   hit++;
  }
  if(hit!=k)return 11;
  lines++;
 }
 if(lines!=160)return 12;
 cout<<"PASS 160 windows, 4 norm scans, 320 endpoint and witness checks, independent X enumeration\n";
}
