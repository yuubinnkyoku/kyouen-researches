#define main historical_main
#include "../cube-q5-seven-frontier-20261022/solver.cpp"
#undef main
#include <random>
int main() {
    Solver s(7,0,1000000);std::mt19937_64 rng(20261023);
    for(int trial=0;trial<24;trial++) {
        Mask root;
        while(true) {
            auto moves=s.legal(root);
            if(root.count()>=5 && moves.size()<=8)break;
            if(moves.empty())return 2;
            root.set(moves[rng()%moves.size()]);
        }
        bool first=true;for(int p:root.ids()){if(!first)std::cout<<" ";first=false;std::cout<<p;}std::cout<<"\n";
    }
}
