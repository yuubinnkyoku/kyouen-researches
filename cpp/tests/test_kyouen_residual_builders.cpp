// Compare labelled residual clutters, independent of their Grundy values.
#define KYOUEN_DFPN_NO_MAIN
#include "../solvers/kyouen_dfpn_root.cpp"
#include <cassert>
int main(int argc,char** argv){
    DfPn<4> small(10);
    std::uint64_t safe=0;
    for(std::uint64_t occupied=0;occupied<(1ULL<<16);++occupied)
        if(small.audit_residual_builders(Bits{occupied,0},true)) ++safe;
    DfPn<8> boundary(10);
    assert(boundary.audit_residual_builders(Bits{},false)); // all 64 bits live
    assert(boundary.audit_residual_builders(Bits{1,0},true));
    std::uint64_t saved=0;
    if(argc==2){
        DfPn<11> large(10);
        std::ifstream input(argv[1]);
        if(!input) throw std::runtime_error("cannot open audit fixture");
        std::string line;
        while(std::getline(input,line)){
            if(line.empty()) continue;
            std::istringstream row(line);
            std::string lo,hi;
            if(!std::getline(row,lo,',') || !std::getline(row,hi) || hi.empty())
                throw std::runtime_error("invalid audit fixture");
            if(!large.audit_residual_builders(Bits{std::stoull(lo),std::stoull(hi)},true))
                throw std::runtime_error("unsafe saved root");
            ++saved;
        }
        if(saved!=826) throw std::runtime_error("expected all 826 saved roots");
    }
    std::cout<<"VERIFIED safe_n4="<<safe<<" boundary_n8=2 saved_n11="<<saved<<"\n";
}
