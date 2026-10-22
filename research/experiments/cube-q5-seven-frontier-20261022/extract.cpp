// Extract closed AND/OR subproofs from a private checkpoint, without search.
#define main q5_dfs_main
#include "solver.cpp"
#undef main
int main(int argc,char**argv) {
    if(argc!=5){std::cerr<<"usage: extract side checkpoint roots prefix\n";return 2;}
    Solver s(std::stoi(argv[1]),0,1000000);s.restore(argv[2]);
    std::ifstream in(argv[3]);if(!in)throw std::runtime_error("missing roots");std::string line;
    while(std::getline(in,line)) {
        if(line.empty())continue;
        std::istringstream row(line);int p;Mask root;std::string suffix;
        while(row>>p){if(p<0 || p>=s.n || root.has(p))throw std::runtime_error("bad root");root.set(p);suffix+="-"+std::to_string(p);}
        s.certificate(root,std::string(argv[4])+suffix+".cert");
    }
}
