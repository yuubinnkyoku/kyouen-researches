// Independent count-state mex verification of the two-edge formula.
// Compile: c++ -O2 -std=c++17 verify_two_edges.cpp -o verify_two_edges
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <unordered_map>
using namespace std;

unordered_map<uint64_t,int> memo;
uint64_t key(int a,int b,int c,int f) {
    return uint64_t(a) | (uint64_t(b)<<12) | (uint64_t(c)<<24) | (uint64_t(f)<<36);
}
int grundy(int a,int b,int c,int f) {
    assert(a+c>=1 && b+c>=1);
    uint64_t k=key(a,b,c,f);
    if(auto it=memo.find(k);it!=memo.end()) return it->second;
    array<bool,8> seen{};
    if(a && a+c>1) seen[grundy(a-1,b,c,f)]=true;
    if(b && b+c>1) seen[grundy(a,b-1,c,f)]=true;
    if(c && a+c>1 && b+c>1) seen[grundy(a,b,c-1,f)]=true;
    if(f) seen[grundy(a,b,c,f-1)]=true;
    int v=0;
    while(v<(int)seen.size() && seen[v])++v;
    assert(v<(int)seen.size());
    memo.emplace(k,v);
    return v;
}
int formula(int a,int b,int c,int f) {
    int n=a+b+c+f;
    if(c>0 && c==min(a,b))return 2+((max(a,b)-c+f)&1);
    if(c>min(a,b))return (n-1)&1;
    return (n-2)&1;
}
int main(){
    long long checked=0;
    array<long long,4> distribution{};
    constexpr int limit=60;
    for(int a=1;a<=limit;++a)
      for(int b=1;a+b<=limit;++b)
        for(int c=0;a+b+c<=limit;++c)
          for(int f=0;f<=3;++f){
            int actual=grundy(a,b,c,f),expected=formula(a,b,c,f);
            if(actual!=expected){
              cerr<<"Mismatch "<<a<<' '<<b<<' '<<c<<' '<<f<<' '<<actual<<' '<<expected<<'\n';
              return 1;
            }
            ++checked;
            ++distribution[actual];
          }
    cout<<"{\"max_edge_vertices\":"<<limit<<",\"free_vertices\":\"0..3\",\"cases\":"<<checked
        <<",\"counts\":["<<distribution[0]<<','<<distribution[1]<<','<<distribution[2]<<','<<distribution[3]
        <<"],\"memo_states\":"<<memo.size()<<"}\n";
}
