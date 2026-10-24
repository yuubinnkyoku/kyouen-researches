// Independent column-pattern enumeration and bottom-up safe-state membership DP.
// Input format is identical to audit.cpp; no triple-completion propagation.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using Mask=uint64_t;
struct ColumnAudit{
    int w,n;std::vector<std::vector<int>> columns;std::vector<Mask> column_masks;
    std::unordered_set<Mask> forbidden;std::unordered_map<Mask,uint8_t> values;
    std::vector<std::vector<Mask>> layers;
    std::array<uint64_t,64> layer_counts{},hist{},terminals{};uint64_t mismatch=0;
    Mask g3_witness=0;int g3_stones=-1;
    ColumnAudit(int width,int count):w(width),n(count),columns(w),column_masks(w),layers(64){values.reserve(1000000);}
    void leaf(Mask mask,const std::vector<int>& chosen){
        int k=chosen.size();
        for(int a=0;a<k;++a)for(int b=a+1;b<k;++b)for(int c=b+1;c<k;++c)for(int d=c+1;d<k;++d){
            Mask q=(Mask(1)<<chosen[a])|(Mask(1)<<chosen[b])|(Mask(1)<<chosen[c])|(Mask(1)<<chosen[d]);
            if(forbidden.count(q))return;
        }
        if(values.emplace(mask,255).second)layers[k].push_back(mask);
    }
    void enumerate(int column,int doubled,Mask mask,std::vector<int>& chosen){
        if(column==w){leaf(mask,chosen);return;}
        if(column==doubled){enumerate(column+1,doubled,mask,chosen);return;}
        enumerate(column+1,doubled,mask,chosen);
        for(int p:columns[column]){chosen.push_back(p);enumerate(column+1,doubled,mask|(Mask(1)<<p),chosen);chosen.pop_back();}
    }
    void run(){
        std::vector<int> chosen;enumerate(0,-1,0,chosen);
        for(int col=0;col<w;++col){const auto&v=columns[col];
            for(size_t a=0;a<v.size();++a)for(size_t b=a+1;b<v.size();++b){
                chosen={v[a],v[b]};enumerate(0,col,(Mask(1)<<v[a])|(Mask(1)<<v[b]),chosen);
            }
            for(size_t a=0;a<v.size();++a)for(size_t b=a+1;b<v.size();++b)for(size_t c=b+1;c<v.size();++c){
                chosen={v[a],v[b],v[c]};leaf((Mask(1)<<v[a])|(Mask(1)<<v[b])|(Mask(1)<<v[c]),chosen);
            }
        }
        const Mask full=(Mask(1)<<n)-1;
        for(int k=63;k>=0;--k)for(Mask s:layers[k]){
            uint64_t options=0;bool has_move=false;Mask bits=full^s;
            while(bits){Mask bit=bits&-bits;bits^=bit;auto it=values.find(s|bit);
                if(it!=values.end()){has_move=true;options|=Mask(1)<<it->second;}}
            uint8_t g=0;while(options&(Mask(1)<<g))++g;values[s]=g;
            if(g==3&&(k>g3_stones||(k==g3_stones&&s<g3_witness))){g3_witness=s;g3_stones=k;}
            ++layer_counts[k];++hist[g];if(!has_move)++terminals[k];
            int active=0;for(Mask cm:column_masks)active+=bool(s&cm);
            int predicted;
            if(w%2==0)predicted=(k%2==0);
            else if(active==1&&k==2)predicted=2;
            else if(active==1&&k==3)predicted=0;
            else predicted=k%2;
            if(g!=predicted)++mismatch;
        }
    }
    void output(){
        if(const char* path=std::getenv("KYOUEN_ZERO_GRUNDY_DUMP")){
            std::vector<std::pair<Mask,uint8_t>> sorted(values.begin(),values.end());std::sort(sorted.begin(),sorted.end());
            std::ofstream out(path,std::ios::binary);
            for(auto [mask,value]:sorted){out.write(reinterpret_cast<const char*>(&mask),sizeof(mask));out.write(reinterpret_cast<const char*>(&value),sizeof(value));}
            if(!out)std::exit(3);
        }
        auto array=[](const auto&a){std::cout<<'[';bool first=true;for(auto x:a){if(!first)std::cout<<',';first=false;std::cout<<uint64_t(x);}std::cout<<']';};
        std::cout<<"{\"empty_grundy\":"<<unsigned(values[0])<<",\"safe_count\":"<<values.size()<<",\"formula_mismatches\":"<<mismatch
                 <<",\"grundy_three_witness\":"<<g3_witness<<",\"grundy_three_stones\":"<<g3_stones<<",\"safe_layers\":";
        array(layer_counts);std::cout<<",\"grundy_histogram\":";array(hist);std::cout<<",\"terminal_sizes\":";array(terminals);std::cout<<"}\n";
    }
};
int main(){
    int w,n,e;if(!(std::cin>>w>>n>>e)||w<2||n<1||n>63)return 2;
    ColumnAudit job(w,n);
    for(int i=0;i<n;++i){int col;std::cin>>col;if(col<0||col>=w)return 2;job.columns[col].push_back(i);job.column_masks[col]|=Mask(1)<<i;}
    for(int i=0;i<e;++i){Mask edge;std::cin>>edge;if(__builtin_popcountll(edge)!=4)return 2;job.forbidden.insert(edge);}
    job.run();job.output();
}
