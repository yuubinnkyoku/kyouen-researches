// Exact enumeration of deficient maximal configurations for the generic
// three-row quadratic-pencil game. No floating point.
// g++ -std=c++17 -O3 exhaustive_maximal.cpp -o /tmp/exhaustive_maximal
// /tmp/exhaustive_maximal
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
struct Row {uint32_t occupied=0, sums=0;vector<int> xs;};
vector<Row> rows(int m,int k){
 vector<Row> out;
 for(uint32_t b=0;b<(1u<<m);++b){
  if(__builtin_popcount(b)!=k)continue;
  Row t;t.occupied=b;
  for(int x=0;x<m;++x)if((b>>x)&1u)t.xs.push_back(x);
  for(int i=0;i<k;++i)for(int j=i+1;j<k;++j)
   t.sums|=1u<<(t.xs[i]+t.xs[j]);
  out.push_back(t);
 }
 return out;
}
bool saturated(const Row& a,uint32_t forbidden_sums,int m){
 if(a.xs.size()==3)return true;
 for(int x=0;x<m;++x){
  if((a.occupied>>x)&1u)continue;
  bool blocked=false;
  for(int old:a.xs)if((forbidden_sums>>(x+old))&1u){
   blocked=true;break;
  }
  if(!blocked)return false;
 }
 return true;
}
string show(const Row& r){
 string s="{";
 for(int x:r.xs){if(s.size()>1)s+=",";s+=to_string(x);}
 return s+"}";
}
int main(){
 for(int m: {14,15}){
  auto two=rows(m,2),three=rows(m,3);
  uint64_t safe=0,deficient=0;string first;
  for(int pattern=0;pattern<3;++pattern){
   // Counts (2,2,2), (2,3,2), (2,3,3), up to row permutation.
   const auto &a=two,&b=pattern==0?two:three,&c=pattern==2?three:two;
   for(const Row& A:a)for(const Row& B:b){
    if(A.sums&B.sums)continue;
    for(const Row& C:c){
     if((A.sums&C.sums)||(B.sums&C.sums))continue;
     ++safe;
     if(!saturated(A,B.sums|C.sums,m))continue;
     if(!saturated(B,A.sums|C.sums,m))continue;
     if(!saturated(C,A.sums|B.sums,m))continue;
     ++deficient;
     if(first.empty())first=show(A)+" "+show(B)+" "+show(C);
    }
   }
  }
  cout<<"m="<<m<<" safe_deficient_candidates="<<safe
      <<" deficient_maximal="<<deficient
      <<" witness="<<(first.empty()?"none":first)<<"\n";
  if((m==14 && deficient==0)||(m==15 && deficient!=0))return 1;
 }
}
