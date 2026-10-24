// Input: W N E; N column labels; E forbidden quadruple masks.
// Exact memoized mex, compared at every safe state with the proposed formula.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <vector>
using Mask=uint64_t;
struct Audit {
    int w,n;std::vector<int> col;std::vector<Mask> cmask,completion;
    std::unordered_map<Mask,uint8_t> memo;
    std::array<uint64_t,64> layers{},hist{},terminals{};
    uint64_t mismatch=0,terminal_outside=0;Mask witness=0;
    int witness_size=100,witness_actual=-1,witness_expected=-1;
    Audit(int width,int points):w(width),n(points),col(n),cmask(w),completion(n*n*n) {memo.reserve(1000000);}
    size_t index(int a,int b,int c)const{
        std::array<int,3> v{a,b,c};std::sort(v.begin(),v.end());return (v[0]*n+v[1])*n+v[2];
    }
    void edge(Mask e){
        std::array<int,4> points{};Mask bits=e;int k=0;
        while(bits){int p=__builtin_ctzll(bits);bits&=bits-1;if(k<4)points[k]=p;++k;}
        if(k!=4){std::cerr<<"bad edge\n";std::exit(2);}
        for(int i=0;i<4;++i){std::array<int,3> t{};int j=0;for(int a=0;a<4;++a)if(a!=i)t[j++]=points[a];
            completion[index(t[0],t[1],t[2])]|=Mask(1)<<points[i];}
    }
    uint8_t solve(Mask s,Mask legal){
        auto it=memo.find(s);if(it!=memo.end())return it->second;
        int k=__builtin_popcountll(s),active=0;for(Mask mask:cmask)active+=bool(s&mask);
        ++layers[k];if(!legal){++terminals[k];if(k!=w+1&&!(k==3&&active==1))++terminal_outside;}
        uint64_t options=0;Mask bits=legal;
        while(bits){int p=__builtin_ctzll(bits);Mask bit=Mask(1)<<p;bits^=bit;Mask child=s|bit;
            auto jt=memo.find(child);uint8_t value;
            if(jt!=memo.end())value=jt->second;
            else{Mask next=legal^bit,as=s;while(as){int a=__builtin_ctzll(as);as&=as-1;Mask bs=as;
                while(bs){int b=__builtin_ctzll(bs);bs&=bs-1;next&=~completion[index(p,a,b)];}}
                value=solve(child,next);}
            options|=Mask(1)<<value;
        }
        uint8_t g=0;while(options&(Mask(1)<<g))++g;++hist[g];
        int predicted=w%2==0 ? 1-(k%2) : (active==1&&k==2 ? 2 : active==1&&k==3 ? 0 : k%2);
        if(g!=predicted){++mismatch;if(k<witness_size){witness=s;witness_size=k;witness_actual=g;witness_expected=predicted;}}
        memo.emplace(s,g);return g;
    }
    void output(unsigned root){
        auto array=[](const auto&a){std::cout<<'[';bool first=true;for(auto x:a){if(!first)std::cout<<',';first=false;std::cout<<uint64_t(x);}std::cout<<']';};
        std::cout<<"{\"empty_grundy\":"<<root<<",\"safe_count\":"<<memo.size()<<",\"formula_mismatches\":"<<mismatch
          <<",\"terminal_outside\":"<<terminal_outside<<",\"witness\":"<<witness<<",\"witness_actual\":"<<witness_actual
          <<",\"witness_expected\":"<<witness_expected<<",\"safe_layers\":";array(layers);
        std::cout<<",\"grundy_histogram\":";array(hist);std::cout<<",\"terminal_sizes\":";array(terminals);std::cout<<"}\n";
    }
};
int main(){
    int w,n,e;if(!(std::cin>>w>>n>>e)||w<2||n<1||n>63)return 2;
    Audit a(w,n);for(int i=0;i<n;++i){std::cin>>a.col[i];if(a.col[i]<0||a.col[i]>=w)return 2;a.cmask[a.col[i]]|=Mask(1)<<i;}
    for(int i=0;i<e;++i){Mask mask;std::cin>>mask;a.edge(mask);}
    unsigned root=a.solve(0,(Mask(1)<<n)-1);a.output(root);
}
