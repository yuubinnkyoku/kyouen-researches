// Standalone independent audit of the quarter-turn modulo-four theorem.
// Build: c++ -std=c++17 -O2 quarter_turn_mod4_verify.cpp -o /tmp/quarter_turn_mod4
// Run: /tmp/quarter_turn_mod4 > quarter_turn_mod4_20261011.json
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <random>
#include <set>
#include <utility>
#include <vector>
using namespace std;
using P = pair<int,int>;
using i64 = long long;

struct Counts {i64 circle=0, line=0;};
static i64 cross(P a, P b, P c) {
  return (i64)(b.first-a.first)*(c.second-a.second)
       -(i64)(b.second-a.second)*(c.first-a.first);
}
static bool cocircular_or_collinear(P a, P b, P c, P d) {
  auto sq=[](P p)->i64{return (i64)p.first*p.first+(i64)p.second*p.second;};
  i64 x1=b.first-a.first,y1=b.second-a.second,z1=sq(b)-sq(a);
  i64 x2=c.first-a.first,y2=c.second-a.second,z2=sq(c)-sq(a);
  i64 x3=d.first-a.first,y3=d.second-a.second,z3=sq(d)-sq(a);
  return x1*(y2*z3-z2*y3)-y1*(x2*z3-z2*x3)+z1*(x2*y3-y2*x3)==0;
}
static Counts brute(const vector<P>& points) {
  Counts c;
  int n=(int)points.size();
  for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)
  for(int d=b+1;d<n;d++)for(int e=d+1;e<n;e++) {
    P p=points[a],q=points[b],r=points[d],s=points[e];
    bool line=cross(p,q,r)==0 && cross(p,q,s)==0;
    if(line) c.line++;
    else if(cocircular_or_collinear(p,q,r,s)) c.circle++;
  }
  return c;
}
// Point coordinates are doubled about the rotation center (cx2,cy2).
static Counts predicted_mod4(const vector<P>& points, int cx2,int cy2) {
  set<P> S(points.begin(),points.end());
  map<i64,int> radii;
  map<P,int> directions;
  for(P p:points) {
    int x=2*p.first-cx2,y=2*p.second-cy2;
    if(x==0 && y==0) continue;
    // Keep one representative of each antipodal pair.
    if(x<0 || (x==0 && y<0)) continue;
    assert(S.count(P(cx2-p.first,cy2-p.second)));
    radii[(i64)x*x+(i64)y*y]++;
    int g=gcd(abs(x),abs(y));
    directions[{x/g,y/g}]++;
  }
  Counts c;
  for(auto [r,z]:radii)c.circle+=(i64)z*(z-1)/2;
  for(auto [dir,z]:directions)c.line+=(i64)z*(z-1)/2;
  return c;
}
static void verify(const vector<P>& points,int cx2,int cy2) {
  set<P> S(points.begin(),points.end());
  assert(S.size()==points.size());
  for(P p:points) {
    // Quarter-turn of p around (cx2/2,cy2/2).
    int X=2*p.first-cx2,Y=2*p.second-cy2;
    int rx2=cx2-Y,ry2=cy2+X;
    assert(rx2%2==0 && ry2%2==0);
    assert(S.count({rx2/2,ry2/2}));
  }
  Counts a=brute(points),b=predicted_mod4(points,cx2,cy2);
  assert(a.circle%4==b.circle%4);
  assert(a.line%4==b.line%4);
  int center=0;
  for(P p:points)if(2*p.first==cx2 && 2*p.second==cy2)center++;
  assert(a.line%2==0);
  assert(a.circle%2==((int(points.size())-center)/4)%2);
}
static vector<vector<P>> orbits(int k) {
  set<P> seen;
  vector<vector<P>> out;
  for(int x=-k;x<=k;x++)for(int y=-k;y<=k;y++) {
    if((x==0 && y==0) || seen.count({x,y}))continue;
    vector<P> o={{x,y},{-y,x},{-x,-y},{y,-x}};
    for(P p:o)seen.insert(p);
    out.push_back(o);
  }
  return out;
}
int main() {
  constexpr i64 known[]={0,1,14,194,826,2491,6364,14564,29152,54441,95670};
  cout<<"{\"theorem\":\"quarter-turn modulo four\",\"squares\":[";
  for(int n=1;n<=11;n++) {
    vector<P> pts;
    for(int x=0;x<n;x++)for(int y=0;y<n;y++)pts.push_back({x,y});
    verify(pts,n-1,n-1);
    Counts c=brute(pts),p=predicted_mod4(pts,n-1,n-1);
    assert(c.circle+c.line==known[n-1]);
    if(n>1)cout<<",";
    cout<<"{\"n\":"<<n<<",\"circle\":"<<c.circle<<",\"line\":"<<c.line
        <<",\"circle_mod4\":"<<p.circle%4<<",\"line_mod4\":"<<p.line%4<<"}";
  }
  auto small=orbits(2);
  assert(small.size()==6);
  int exhaustive=0;
  for(int mask=0;mask<(1<<7);mask++) {
    vector<P> pts;
    if(mask&64)pts.push_back({0,0});
    for(int j=0;j<6;j++)if(mask&(1<<j))pts.insert(pts.end(),small[j].begin(),small[j].end());
    verify(pts,0,0);exhaustive++;
  }
  auto big=orbits(3);
  assert(big.size()==12);
  mt19937 rng(20261011);
  int random_checks=0;
  for(int t=0;t<256;t++) {
    vector<P> pts;
    if(rng()%2)pts.push_back({0,0});
    for(auto& o:big)if(rng()%4==0)pts.insert(pts.end(),o.begin(),o.end());
    verify(pts,0,0);random_checks++;
  }
  cout<<"],\"exhaustive_quarter_turn_subsets\":"<<exhaustive
      <<",\"random_quarter_turn_subsets\":"<<random_checks
      <<",\"status\":\"all_checks_passed\"}\n";
}
