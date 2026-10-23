// Check every candidate row against a preserved immutable base, including witness.
#define main historical_main
#include "../cube-q5-seven-frontier-20261022/solver.cpp"
#undef main
#include "disk.hpp"
int main(int argc,char**argv) {
    if(argc!=4)return 2;
    DiskBase base(argv[1],argv[2]);Mapping candidate(argv[3]);
    uint64_t header[3];if(candidate.size<32 || std::memcmp(candidate.data,"Q5MEMO2\n",8))return 3;
    std::memcpy(header,candidate.data+8,24);
    if(header[0]!=uint64_t(base.side) || candidate.size!=32+104*header[2])return 4;
    for(uint64_t i=0;i<header[2];i++) {
        const auto* row=candidate.data+32+104*i;Mask key,witness;uint64_t label;
        std::memcpy(key.w.data(),row,48);std::memcpy(&label,row+48,8);std::memcpy(witness.w.data(),row+56,48);
        auto found=base.get(key);
        if(!found || uint64_t(found->win)!=label || !(found->witness==witness))return 5;
    }
    std::cout<<"{\"all_rows_and_witnesses_preserved\":true,\"rows\":"<<header[2]<<"}\n";
}
