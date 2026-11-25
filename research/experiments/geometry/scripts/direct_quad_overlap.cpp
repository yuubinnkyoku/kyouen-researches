// Independent exact four-point determinant enumeration. No curve grouping.
#include <iostream>
#include <vector>
#include <array>
#include <cstdint>
#include <cstdlib>
using namespace std;
using ll=long long;
ll choose2(ll x){return x*(x-1)/2;}
struct Point {ll x,y,z;};
int main(int argc,char**argv){
 int w=argc>1?atoi(argv[1]):11;
 int h=argc>2?atoi(argv[2]):w;
 int m=w*h;
 vector<Point> p;
 for(int y=0;y<h;y++)for(int x=0;x<w;x++)p.push_back({x,y,x*x+y*y});
 vector<ll> deg1(m),deg2(m*m),deg3(m*m*m),line2(m*m),circle2(m*m);
 ll Fline=0,Fcircle=0;
 ll F=0;
 for(int a=0;a<m;a++)for(int b=a+1;b<m;b++)for(int c=b+1;c<m;c++)for(int d=c+1;d<m;d++){
  ll x1=p[b].x-p[a].x,y1=p[b].y-p[a].y,z1=p[b].z-p[a].z;
  ll x2=p[c].x-p[a].x,y2=p[c].y-p[a].y,z2=p[c].z-p[a].z;
  ll x3=p[d].x-p[a].x,y3=p[d].y-p[a].y,z3=p[d].z-p[a].z;
  ll det=x1*(y2*z3-z2*y3)-y1*(x2*z3-z2*x3)+z1*(x2*y3-y2*x3);
  if(det)continue;
  bool isline=((p[b].x-p[a].x)*(p[c].y-p[a].y)==(p[b].y-p[a].y)*(p[c].x-p[a].x)) && ((p[b].x-p[a].x)*(p[d].y-p[a].y)==(p[b].y-p[a].y)*(p[d].x-p[a].x));
  (isline?Fline:Fcircle)++;
  F++;
  deg1[a]++;deg1[b]++;deg1[c]++;deg1[d]++;
  deg2[a*m+b]++;deg2[a*m+c]++;deg2[a*m+d]++;
  deg2[b*m+c]++;deg2[b*m+d]++;deg2[c*m+d]++;
  auto &typed=(isline?line2:circle2);
  typed[a*m+b]++;typed[a*m+c]++;typed[a*m+d]++;
  typed[b*m+c]++;typed[b*m+d]++;typed[c*m+d]++;
  deg3[(a*m+b)*m+c]++;deg3[(a*m+b)*m+d]++;
  deg3[(a*m+c)*m+d]++;deg3[(b*m+c)*m+d]++;
 }
 ll o3=0,o2sum=0,o1sum=0;
 for(ll v:deg3)o3+=choose2(v);
 for(ll v:deg2)o2sum+=choose2(v);
 for(ll v:deg1)o1sum+=choose2(v);
 ll o2=o2sum-3*o3,o1=o1sum-2*o2-3*o3,o0=choose2(F)-o1-o2-o3;
 ll mixed=0;for(int i=0;i<m*m;i++)mixed+=line2[i]*circle2[i];
 cout<<"{\"w\":"<<w<<",\"h\":"<<h<<",\"F\":"<<F<<",\"overlap\":["<<o0<<","<<o1<<","<<o2<<","<<o3<<"],\"line\":"<<Fline<<",\"circle\":"<<Fcircle<<",\"mixed2\":"<<mixed<<"}"<<endl;
}
