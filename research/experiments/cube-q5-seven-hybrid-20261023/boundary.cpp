// Inspect exact candidate coverage of immediate children, without a new search.
#define main historical_hybrid_main
#include "../cube-q5-seven-frontier-20261022/solver.cpp"
#undef main
#include "layers.hpp"
int main(int argc,char**argv) {
    if(argc!=5 && argc!=6)return 2;
    Solver s(std::stoi(argv[1]),0,1000000);DiskStack base(argv[2],argv[3]);
    std::unique_ptr<Mapping> active;std::array<uint64_t,9> header{};
    if(argc==6) {
        active=std::make_unique<Mapping>(argv[5]);
        if(active->size<88 || std::memcmp(active->data,"Q5HYB2\n\0",8))throw std::runtime_error("bad active header");
        std::memcpy(header.data(),active->data+8,72);
        if(header[0]!=uint64_t(s.side) || header[1]!=base.fingerprint || header[2]!=base.rows || header[3]!=base.nodes || active->size!=88+104*header[7]+136*header[8])throw std::runtime_error("active dependency mismatch");
    }
    std::ifstream roots(argv[4]);std::string line;
    while(std::getline(roots,line)) {
        if(line.empty())continue;
        Mask root;std::istringstream input(line);int p;while(input>>p)root.set(p);
        root=s.canonical(root);std::map<Mask,int> children;
        for(int q:s.legal(root)){Mask child=root;child.set(q);children.emplace(s.canonical(child),q);}
        std::map<Mask,bool> delta;
        if(active)for(uint64_t i=0;i<header[7];i++) {
            const auto* row=active->data+80+104*i;Mask key;std::memcpy(key.w.data(),row,48);
            if(key.count()!=root.count()+1 || !children.count(key))continue;
            uint64_t label;std::memcpy(&label,row+48,8);if(label>1)throw std::runtime_error("bad active label");
            delta.emplace(key,bool(label));
        }
        uint64_t known_n=0,known_p=0;
        std::cout<<"{\"root\":[";bool comma=false;for(int q:root.ids()){if(comma)std::cout<<",";comma=true;std::cout<<q;}
        std::cout<<"],\"children\":[";comma=false;
        for(const auto& [child,q]:children) {
            auto e=base.get(child);auto extra=delta.find(child);
            if(extra!=delta.end())e=Entry{extra->second,{}};
            if(e){if(e->win)++known_n;else ++known_p;}
            if(comma)std::cout<<",";
            comma=true;
            std::cout<<"{\"point\":"<<q<<",\"label\":\""<<(e?(e->win?"N":"P"):"UNKNOWN")<<"\",\"root\":[";
            bool sep=false;for(int k:child.ids()){if(sep)std::cout<<",";sep=true;std::cout<<k;}std::cout<<"]}";
        }
        std::cout<<"],\"child_orbits\":"<<children.size()<<",\"candidate_n\":"<<known_n<<",\"candidate_p\":"<<known_p<<",\"independently_verified\":false}\n";
    }
}
