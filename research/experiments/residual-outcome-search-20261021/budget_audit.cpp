// Budget coverage and resumable-memo audit against independent root outcomes.
#include "kyouen_residual_micro.hpp"
#include <iostream>
using namespace kyouen_residual;
int main(){
    const std::uint64_t caps[]={0,1,2,8,32,128,512,2048,100000};
    std::uint64_t known[9]{},calls[9]{},resumed=0,roots=0;
    int id,n,m,expected;
    while(std::cin>>id>>n>>m>>expected){
        if(n<0 || n>18 || m<0 || m>10000 || expected<0 || expected>1) return 2;
        State s{n?((Mask{1}<<n)-1):0,{}};
        for(int i=0;i<m;++i){Mask edge;if(!(std::cin>>edge))return 2;s.edges.push_back(edge);}
        s=normalize(std::move(s));
        std::map<Key,int> partial;
        int last=-1;
        for(int i=0;i<9;++i){
            Stats st;std::uint64_t left=caps[i];std::map<Key,int> memo;
            int value=outcome(s,memo,left,&st);
            if(left>caps[i] || st.calls!=caps[i]-left || (value>=0 && value!=expected))return 1;
            if(value>=0) ++known[i];calls[i]+=st.calls;
            left=caps[i];Stats reused;
            last=outcome(s,partial,left,&reused);
            if(left>caps[i] || reused.calls!=caps[i]-left || (last>=0 && last!=expected))return 1;
        }
        if(last!=expected) return 1;
        ++resumed;++roots;
    }
    if(roots!=826 || known[8]!=826 || known[0]!=0) return 1;
    std::cout<<"{\"roots\":"<<roots<<",\"resumed_correct\":"<<resumed<<",\"caps\":[";
    for(int i=0;i<9;++i){
        if(i)std::cout<<',';
        std::cout<<"{\"budget\":"<<caps[i]<<",\"known\":"<<known[i]<<",\"unknown\":"<<roots-known[i]<<",\"calls\":"<<calls[i]<<'}';
    }
    std::cout<<"]}\n";
}
