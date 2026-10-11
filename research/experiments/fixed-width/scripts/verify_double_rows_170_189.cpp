// Conditional modular certificate for T(w)=24, 170<=w<=189, assuming T(169)=24.
// Two independent local-mask builders, dominance-preserving intersections,
// endpoint induction, and direct integer-circle witness checks.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>
using namespace std;
struct Mask {
    array<uint64_t,3> a{0,0,0};
    void set(int i) {a[i>>6] |= uint64_t(1)<<(i&63);}
    bool test(int i) const {return (a[i>>6]>>(i&63))&1;}
    int count() const {return __builtin_popcountll(a[0])+__builtin_popcountll(a[1])+__builtin_popcountll(a[2]);}
    Mask operator&(const Mask &b)const {return {{a[0]&b.a[0],a[1]&b.a[1],a[2]&b.a[2]}};}
    bool operator==(const Mask &b)const {return a==b.a;}
    bool operator<(const Mask &b)const {return a<b.a;}
    bool subset(const Mask &b)const {return ((a[0]&b.a[0])==a[0] && (a[1]&b.a[1])==a[1] && (a[2]&b.a[2])==a[2]);}
};
struct Hash {
    size_t operator()(const Mask &m)const {
        uint64_t x=0x9e3779b97f4a7c15ULL;
        for(uint64_t y:m.a){x^=y+0x9e3779b97f4a7c15ULL+(x<<6)+(x>>2);}
        return (size_t)x;
    }
};
static vector<Mask> maximal(vector<Mask> v){
    sort(v.begin(),v.end());v.erase(unique(v.begin(),v.end()),v.end());
    sort(v.begin(),v.end(),[](const Mask &a,const Mask &b){int x=a.count(),y=b.count();return x!=y?x>y:a<b;});
    vector<Mask> keep;
    for(const auto &a:v){bool dominated=false;for(const auto &b:keep)if(a.subset(b)){dominated=true;break;}if(!dominated)keep.push_back(a);}
    return keep;
}
static vector<Mask> local_masks(int w,int p,int k,Mask allowed,Mask required){
    vector<bool> square(p,false);
    for(int t=0;t<p;t++)square[(t*t)%p]=true;
    vector<Mask> v;
    for(int c=0;c<p;c++){
        vector<int> z(w);
        vector<vector<bool>> inverse(w,vector<bool>(p,false));
        for(int y=0;y<w;y++){
            int a=(2*y+c)%p;z[y]=(a*a)%p;
            for(int t=0;t<p;t++)inverse[y][(z[y]+t*t)%p]=true;
        }
        for(int n=0;n<p;n++){
            Mask direct,transposed;
            for(int y=0;y<w;y++){
                if(square[(n-z[y]+p)%p])direct.set(y);
                if(inverse[y][n])transposed.set(y);
            }
            if(!(direct==transposed))throw runtime_error("independent mask mismatch");
            direct=direct&allowed;
            if(direct.count()<k || !required.subset(direct))continue;
            v.push_back(direct);
        }
    }
    return maximal(move(v));
}
static vector<Mask> intersection(vector<Mask> states,const vector<Mask> &local,int k){
    vector<Mask> cand;
    cand.reserve(states.size()*min(size_t(20),local.size()));
    for(const auto &a:states)for(const auto &b:local){Mask m=a&b;if(m.count()>=k)cand.push_back(m);}
    return maximal(move(cand));
}
static int exclude(int w,int k,bool endpoints,bool g3){
    Mask allowed,required;
    for(int y=0;y<w;y++)if(!g3 || y%3==0)allowed.set(y);
    if(endpoints){required.set(0);required.set(w-1);}
    vector<Mask> states{allowed};
    vector<int> mods=g3?vector<int>{11,19,23,31,43,47,59,67,71,79,83}:endpoints?vector<int>{9,7,49,11,19,23,31,43}:vector<int>{9,11,19,23,7,49};
    int last=0;
    for(int p:mods){
        auto local=local_masks(w,p,k,allowed,required);
        states=intersection(move(states),local,k);
        last=p;
        if(states.empty())break;
    }
    if(!states.empty())throw runtime_error("unexcluded width="+to_string(w)+" k="+to_string(k)+" g3="+to_string(g3));
    return last;
}
static bool is_square(int64_t x){
    if(x<0)return false;
    int64_t a=0,b=1;while(b*b<=x)b*=2;
    while(a+1<b){auto m=(a+b)/2;if(m*m<=x)a=m;else b=m;}
    return a*a==x;
}
static vector<int> circle_rows(int w,int C,int D){
    vector<int> ys;
    for(int y=0;y<w;y++){
        int64_t delta=1-4LL*(1LL*y*y+1LL*C*y+D);
        if(delta<=0||!is_square(delta))continue;
        int64_t z=0;while((z+1)*(z+1)<=delta)z++; // small integers, independent check
        if(z%2!=1)continue;
        int64_t x1=(-1-z)/2,x2=(-1+z)/2;
        if(x1==x2 || x1*x1+1LL*y*y+x1+1LL*C*y+D!=0 || x2*x2+1LL*y*y+x2+1LL*C*y+D!=0)
            throw runtime_error("bad circle witness");
        ys.push_back(y);
    }
    return ys;
}
int main(int argc,char**argv){
    try{
        int lo=170,hi=189;
        if(argc==3){lo=stoi(argv[1]);hi=stoi(argv[2]);}
        else if(argc!=1)throw runtime_error("usage: verifier [first last]");
        if(lo<170||hi>189||lo>hi)throw runtime_error("range outside 170..189");
        // One circle of norm N=11050 has 24 distinct double-hit rows in 0..105.
        const vector<int> Y{0,1,5,6,9,12,19,23,28,30,42,50,55,63,75,77,82,86,93,96,99,100,104,105};
        if(circle_rows(106,-105,-6)!=Y)throw runtime_error("24-row witness invalid");
        int previous=24;
        for(int w=lo;w<=hi;w++){
            int best=0,shift=0;
            for(int s=-w;s<=106;s++){
                int hits=0;for(int y:Y)hits+=(s<=y && y<s+w);
                if(hits>best){best=hits;shift=s;}
            }
            int expected=max(16,best);
            if(w<=82 && circle_rows(w,-47,0).size()!=16)throw runtime_error("16-row witness invalid");
            if(w>=83){
                // Vertical translation y'=y-shift transforms C to C+2*shift,
                // and D to D+C*shift+shift^2, preserving integral coefficients.
                int C=-105+2*shift,D=-6-105*shift+shift*shift;
                if(circle_rows(w,C,D).size()!=size_t(best))throw runtime_error("translated witness invalid");
            }
            if(w==64){
                if(expected!=16)throw runtime_error("unexpected base lower bound");
                int m=exclude(w,17,false,false);
                // For g=3, 17 hits among at most 22 rows congruent mod3 imply
                // at least 14 distinct mod19 residues, while a circle has <=11.
                if(17-(22-19)<=11)throw runtime_error("g3 counting failed");
                cout<<"BASE w=64 T=16 last_mod="<<m<<'\n';
            }else if(expected==previous+1){
                // T(w)<=T(w-1)+1: a new row contains at most one double-hit row.
                cout<<"JUMP w="<<w<<" T="<<expected<<" witness_shift="<<shift<<'\n';
            }else if(expected==previous){
                int k=expected+1;
                if((w-1)/expected>7)throw runtime_error("g bound exceeded");
                // At w=169, g=7 would force exactly y=0,7,...,168.
                // These contain all 19 residues modulo 19; at most 11 are admissible.
                if((w-1)%7==0){
                    // For w=176,183, a g=7 candidate lies in <=27 multiples of 7.
                    // Each residue modulo 19 occurs at most twice, hence 25 hits
                    // would require >=13 residues; only <=11 are admissible.
                    int len=(w-1)/7+1;
                    if(len>38 || (k+1)/2<=11)throw runtime_error("g7 counting failed");
                }
                int m=exclude(w,k,true,false);
                int m3=0;
                if((w-1)%3==0)m3=exclude(w,k,true,true);
                cout<<"PLATEAU w="<<w<<" T="<<expected<<" excluded_k="<<k<<" last_mod="<<m<<" g3_mod="<<m3<<'\n';
            }else throw runtime_error("unexpected jump in lower bound");
            previous=expected;
        }
        cout<<"PASS conditional checks "<<lo<<".."<<hi<<" (given T(169)=24)"<<endl;
    }catch(const exception &e){cerr<<"FAIL: "<<e.what()<<endl;return 1;}
}
