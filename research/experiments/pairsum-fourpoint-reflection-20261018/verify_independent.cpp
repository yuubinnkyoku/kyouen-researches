// Independent audit: group every four-element integer multiset by its six sums.
// Does not use the three-parameter reconstruction formula.
#include <array>
#include <algorithm>
#include <cassert>
#include <iostream>
#include <map>
#include <set>
#include <vector>
using A = std::array<int, 4>;
using P = std::array<int, 6>;
P sums(const A &a) {
    P p{}; int k=0;
    for (int i=0;i<4;++i) for (int j=i+1;j<4;++j) p[k++]=a[i]+a[j];
    std::sort(p.begin(),p.end()); return p;
}
A reflect(const A &a) {
    const int t=a[0]+a[1]+a[2]+a[3];
    // Twice the reflected entries; integer reflection requires even t.
    assert(t%2==0);
    A b{}; for(int i=0;i<4;++i) b[i]=t/2-a[i];
    std::sort(b.begin(),b.end()); return b;
}
void audit(bool repeats) {
    std::map<P,std::vector<A>> classes;
    const int lo=repeats?-5:-8, hi=repeats?7:8;
    for(int a=lo;a<=hi;++a) for(int b=repeats?a:a+1;b<=hi;++b)
      for(int c=repeats?b:b+1;c<=hi;++c)
        for(int d=repeats?c:c+1;d<=hi;++d) {
          A x{a,b,c,d}; classes[sums(x)].push_back(x);
        }
    long long tested=0,collisions=0,odd=0;
    for(const auto &[p, xs]: classes) {
        (void)p;
        assert(xs.size()<=2);
        for(const auto &x:xs) {
            ++tested;
            int t=x[0]+x[1]+x[2]+x[3];
            if(t%2) {assert(xs.size()==1); ++odd;}
            for(const auto &y:xs) {
                if(x==y) continue;
                assert(t%2==0);
                assert(y==reflect(x));
            }
        }
        if(xs.size()==2) ++collisions;
    }
    std::cout<<(repeats?"multisets":"distinct")<<" tested="<<tested
             <<" classes="<<classes.size()<<" collisions="<<collisions
             <<" odd_total="<<odd<<"\n";
}
int main() {audit(false); audit(true);}
