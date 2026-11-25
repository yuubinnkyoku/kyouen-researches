// Direct finite modular verifier for the 360-row gcd-one certificate.
// Direct enumeration of quadratic residues and intersections, no pruning by dominance.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <unordered_set>
#include <vector>
using namespace std;
struct Mask {
    array<uint64_t,3> a{};
    bool operator==(const Mask& x) const { return a==x.a; }
    int count() const {return __builtin_popcountll(a[0])+__builtin_popcountll(a[1])+__builtin_popcountll(a[2]);}
    void set(int i){a[i/64]|=1ULL<<(i%64);}
    Mask operator&(const Mask&x)const{return {{a[0]&x.a[0],a[1]&x.a[1],a[2]&x.a[2]}};}
};
struct Hash {size_t operator()(const Mask& m)const {size_t h=0x9e3779b97f4a7c15ULL;for(auto x:m.a)h^=x+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);return h;}};
using Set=unordered_set<Mask,Hash>;
Set local(int width,int modulus){
    vector<char> square(modulus);
    for(int x=0;x<modulus;x++)square[x*x%modulus]=1;
    Set out;
    for(int c=0;c<modulus;c++)for(int n=0;n<modulus;n++){
        Mask mask;
        for(int k=0;k<width;k++){
            int t=(2*k+c)%modulus;
            int d=(n-t*t%modulus+modulus)%modulus;
            if(square[d])mask.set(k);
        }
        if(mask.count()>=25)out.insert(mask);
    }
    return out;
}
void check(int g,vector<int> moduli){
    int width=(360+g-1)/g;
    Mask full;for(int k=0;k<width;k++)full.set(k);
    Set states;states.insert(full);
    cout<<"g="<<g<<" width="<<width<<"\n";
    for(int mod:moduli){
        if(gcd(g,mod)!=1)throw runtime_error("noninvertible modulus");
        Set loc=local(width,mod), next;
        for(const Mask& a:states)for(const Mask& b:loc){
            Mask v=a&b;
            if(v.count()>=25)next.insert(v);
        }
        states.swap(next);
        cout<<"  mod="<<mod<<" local="<<loc.size()<<" survivors="<<states.size()<<"\n";
        if(states.empty())break;
    }
    if(!states.empty())throw runtime_error("unexcluded gcd "+to_string(g));
}
int main(){
    check(2,{9,7,49,11,19,23,31,37,41,43,47,53,59});
    check(3,{11,19,23,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97});
    check(4,{11,19,23,31});
    check(5,{11,19,23,31});
    check(6,{19,23,31});
    for(int g=7;g<=14;g++)check(g,{19,23,31});
    cout<<"PASS: 360-row gcd-one certificate (direct)\n";
}
