// A proved P child proves every one-point-deleted parent N.
#define main historical_main
#include "../cube-q5-seven-frontier-20261022/solver.cpp"
#undef main
#include <set>
int main(int argc,char**argv) {
    if(argc!=3)return 2;
    std::ifstream in(argv[1]);std::string magic;int side,words;Mask child;
    in>>magic>>side>>words;if(magic!="Q5CUBE2" || side!=7 || words!=6)return 3;
    for(auto& word:child.w)in>>word;
    std::string ignored;std::getline(in,ignored);
    std::string body((std::istreambuf_iterator<char>(in)),{});
    Solver s(side,0,100000);std::set<Mask> parents;
    for(int p:child.ids()){Mask parent=child;parent.w[p/64]&=~(uint64_t(1)<<(p%64));parents.insert(s.canonical(parent));}
    for(const auto& parent:parents) {
        std::string suffix;for(int p:parent.ids())suffix+="-"+std::to_string(p);
        std::ofstream out(std::string(argv[2])+suffix+".cert");
        out<<"Q5CUBE2 7 6";for(auto word:parent.w)out<<" "<<word;out<<"\n";
        for(auto word:parent.w)out<<word<<" ";
        out<<"1";
        for(auto word:child.w)out<<" "<<word;
        out<<"\n"<<body;
        std::cout<<"[";bool first=true;for(int p:parent.ids()){if(!first)std::cout<<",";first=false;std::cout<<p;}std::cout<<"]\n";
    }
}
