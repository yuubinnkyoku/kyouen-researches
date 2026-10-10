#define main kyouen_solver_main
#include "../../../../cpp/solvers/kyouen_dfpn_root.cpp"
#undef main
#include <filesystem>

int main(int argc,char** argv){
    if(argc!=2) return 1;
    DfPn<11> solver(12);
    std::string path=argv[1];
    auto write=[&](std::string rows){
        std::ofstream f(path);
        f<<"# s5 verdict cache: n=11 schema=1\n"<<rows;
    };
    write("s5verdict,1152925911243358208,536870912,5,1,0\n"
          "s5verdict,10448351135499552768,128,5,1,0\n");
    solver.oracle_load(path);
    if(solver.oracle_cache_size()!=0) return 2;
    std::vector<std::string> invalid={
        "s5verdict,1,0,5,1,0\n", // wrong rank
        "s5verdict,15,1,5,1,0\n", // collinear four
        "s5verdict,15,144115188075855872,5,1,0\n", // out of board
        "s5verdict,1,0,5abc,1,0\n", // truncated numeric parsing
        "s5verdict,1,0,5,0,0\n", // UNKNOWN
        "s5verdict,1,0,5,1\n"}; // malformed
    for(const auto& row:invalid){
        write(row);
        bool rejected=false;
        try { solver.oracle_load(path); } catch(const std::exception&) { rejected=true; }
        if(!rejected) return 3;
    }
    // Geometry-valid canonical position with a solver-trusted verdict.
    write("s5verdict,144115191431364608,0,5,2,0\n");
    solver.oracle_load(path);
    if(solver.oracle_cache_size()!=1) return 4;
    write("s5verdict,144115191431364608,0,5,1,0\n");
    bool conflict=false;
    try{ solver.oracle_load(path); }catch(const std::exception&){ conflict=true; }
    if(!conflict) return 5;
    for(const Bits m:std::vector<Bits>{{15,0},{0,1ULL<<57}}){
        std::uint64_t nodes=0;
        bool invalid=false;
        try{ solver.exact_replay(m,popcount(m),10,nodes); }catch(const std::exception&){invalid=true;}
        if(!invalid) return 6;
    }
    std::filesystem::remove(path);
    std::ostringstream cover;
    run_cover<11>(60,27,
        "research/experiments/n11-independent-exact-audit-20261010/output/canonical-current-s5.cache",cover);
    auto report=cover.str();
    if(report.find("classes_loss=31 classes_win=268 classes_unknown=3085")==std::string::npos ||
       report.find("# COVER covered=117/119")==std::string::npos ||
       report.find("# uncovered vertices: 100 108")==std::string::npos) return 7;
    std::cout<<"CPP_CACHE_POLICY_OK\n";
}
