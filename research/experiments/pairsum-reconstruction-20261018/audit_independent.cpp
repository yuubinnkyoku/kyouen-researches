// Independent C++17 implementation: construct and check all power-of-two examples.
#include <algorithm>
#include <cassert>
#include <iostream>
#include <map>
#include <vector>
using namespace std;
using VI=vector<long long>;
map<long long,int> histogram(const VI& a){
    map<long long,int> h;
    for(size_t i=0;i<a.size();++i)for(size_t j=i+1;j<a.size();++j)++h[a[i]+a[j]];
    return h;
}
void normalize(VI& a,VI& b){
    long long mn=min(*min_element(a.begin(),a.end()),*min_element(b.begin(),b.end()));
    for(auto& x:a)x-=mn;
    for(auto& x:b)x-=mn;
    sort(a.begin(),a.end());sort(b.begin(),b.end());
}
int main(){
    VI a={0,1,4,7};
    long long t=0;for(auto x:a)t+=x;
    VI b;for(auto x:a)b.push_back(t/2-x);
    normalize(a,b);
    for(int n=4;n<=32;n*=2){
        assert(a.size()==(size_t)n&&b.size()==(size_t)n&&a!=b);
        assert(adjacent_find(a.begin(),a.end())==a.end());
        assert(adjacent_find(b.begin(),b.end())==b.end());
        assert(histogram(a)==histogram(b));
        cout<<"n="<<n<<" distinct_pair_sums="<<histogram(a).size()<<" check=OK\n";
        long long m=max(a.back(),b.back())+11;
        VI aa=a,bb=b;
        for(auto x:b)aa.push_back(x+m);
        for(auto x:a)bb.push_back(x+m);
        a=aa;b=bb;normalize(a,b);
    }
}
