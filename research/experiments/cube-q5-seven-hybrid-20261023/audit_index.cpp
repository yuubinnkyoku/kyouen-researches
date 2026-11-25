#define main historical_main
#include "../cube-q5-seven-frontier-20261022/solver.cpp"
#undef main
#include "layers.hpp"
int main(int argc,char**argv) {
    if(argc!=3)return 2;
    DiskBase base(argv[1],argv[2]);uint64_t checked=0;
    base.each([&](const Mask& key,Entry entry) {
        auto found=base.get(key);
        if(!found || found->win!=entry.win || !(found->witness==entry.witness))throw std::runtime_error("index mismatch");
        ++checked;
    });
    if(checked!=base.rows)return 3;
    std::cout<<"{\"every_row_and_witness_checked\":true,\"rows\":"<<checked<<"}\n";
}
