#include <bits/stdc++.h>
using namespace std;
using Pt=pair<int,int>;
using Shape=vector<Pt>;
int overlap(const Shape &a,const Shape &b,int shift){
 int z=0;
 for(auto [x,y]:a)for(auto [u,v]:b)if(y==v && x==u+shift)++z;
 return z;
}
vector<int> possible_shifts(const Shape &a,const Shape &b){
 set<int> t;
 for(auto [x,y]:a)for(auto [u,v]:b)if(y==v)t.insert(x-u);
 return vector<int>(t.begin(),t.end());
}
int main(int argc,char**argv){
 if(argc!=2)return 2;
 vector<array<int,4>> chords{{1,3,3,1}};
 ifstream f(argv[1]);string line;
 while(getline(f,line)){
  replace(line.begin(),line.end(),',',' ');
  istringstream s(line);array<int,4> a;
  if(!(s>>a[0]>>a[1]>>a[2]>>a[3]))return 3;
  chords.push_back(a);reverse(a.begin(),a.end());chords.push_back(a);
 }
 vector<Shape> p;
 for(auto a:chords){
  Shape pts;int D=*max_element(a.begin(),a.end());
  for(int y=0;y<4;y++){
   if((D-a[y])%2)return 4;
   pts.push_back({(D-a[y])/2,y});pts.push_back({(D+a[y])/2,y});
  }
  p.push_back(pts);
 }
 int n=p.size();long long cases=0;int minunion=24;
 for(int i=0;i<n;i++)for(int j=0;j<n;j++){
  for(int t:possible_shifts(p[i],p[j])){
   int nij=overlap(p[i],p[j],t);
   if(nij>2 && !(i==j && t==0))return 5;
   if(nij!=2 || (i==j && t==0))continue;
   for(int k=0;k<n;k++)for(int u:possible_shifts(p[i],p[k])){
    if((i==k&&u==0)||(j==k&&t==u))continue;
    int nik=overlap(p[i],p[k],u),njk=overlap(p[j],p[k],u-t);
    if(nik==0||njk==0)continue;
    int triple=0;
    for(auto [x,y]:p[i]){
     bool inb=false,inc=false;
     for(auto [xx,yy]:p[j])if(xx+t==x&&yy==y)inb=true;
     for(auto [xx,yy]:p[k])if(xx+u==x&&yy==y)inc=true;
     if(inb&&inc)triple++;
    }
    int un=24-nij-nik-njk+triple;
    minunion=min(minunion,un);cases++;
    if(un<20){cerr<<"counterexample "<<i<<" "<<j<<" "<<k<<" "<<t<<" "<<u<<" union="<<un<<"\n";return 1;}
   }
  }
 }
 cout<<"shapes="<<n<<" checked="<<cases<<" minimum="<<minunion<<" no_union_le_19=true\n";
}
