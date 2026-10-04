// Generate all circles with >=7 points on 5xm by every pair of horizontal
// two-point chords with equal sum.  Rational coefficients and one in-board
// root are retained.  At least seven points in five rows force two chords.
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <set>
#include <vector>

int main(int argc,char**argv){
 int m=argc>1?std::atoi(argv[1]):200;
 std::vector<std::vector<int>> products(2*m-1);
 for(int a=0;a<m;++a)for(int b=a+1;b<m;++b)products[a+b].push_back(a*b);
 std::set<std::vector<int>> circles;
 unsigned long long candidates=0;
 for(int i=0;i<5;++i)for(int j=i+1;j<5;++j)for(int s=0;s<2*m-1;++s)
  for(int p:products[s])for(int q:products[s]){
   ++candidates;long long a=j-i,b=-s*a,c=q-p-a*(i+j),d=a*p-a*i*i-c*i;
   std::vector<int> points;
   for(int y=0;y<5;++y){
    long long disc=b*b-4*a*(a*y*y+c*y+d);
    if(disc<0)continue;
    long long root=(long long)std::sqrt((long double)disc);
    while((root+1)*(root+1)<=disc)++root;
    while(root*root>disc)--root;
    if(root*root!=disc)continue;
    for(int sign:{-1,1}){
     long long n=-b+sign*root;if(n%(2*a))continue;
     long long x=n/(2*a);if(x<0||x>=m)continue;
     int id=y*m+(int)x;
     if(points.empty()||points.back()!=id)points.push_back(id);
    }
   }
   if(points.size()>=7)circles.insert(points);
  }
 std::cerr<<"{\"m\":"<<m<<",\"pair_assignments\":"<<candidates
          <<",\"circles\":"<<circles.size()<<"}\n";
 for(const auto& ps:circles){bool first=true;for(int id:ps){if(!first)std::cout<<' ';std::cout<<id;first=false;}std::cout<<'\n';}
}
