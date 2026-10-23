// Stream candidate labels for the two layers below a root; no label is trusted.
#define main historical_main
#include "../cube-q5-seven-frontier-20261022/solver.cpp"
#undef main
#include <set>
struct State {int label=-1;std::vector<Mask> children;};
int main(int argc,char** argv) {
    if(argc<5)return 2;
    Solver s(std::stoi(argv[1]),0,1000000);Mask root;
    for(int i=3;i<argc;i++)root.set(std::stoi(argv[i]));
    root=s.canonical(root);
    std::map<Mask,State> layer;
    std::unordered_map<Mask,int,Hash> leaves;
    for(int p:s.legal(root)){Mask child=root;child.set(p);layer.emplace(s.canonical(child),State{});}
    for(auto& [key,state]:layer) {
        for(int p:s.legal(key)){Mask child=key;child.set(p);child=s.canonical(child);state.children.push_back(child);leaves.emplace(child,-1);}
        std::sort(state.children.begin(),state.children.end());
        state.children.erase(std::unique(state.children.begin(),state.children.end()),state.children.end());
    }
    std::ifstream in(argv[2],std::ios::binary);char magic[8];uint64_t header[3];
    if(!in.read(magic,8) || std::string(magic,8)!="Q5MEMO2\n" || !in.read(reinterpret_cast<char*>(header),24))return 3;
    uint64_t histogram[8][2]{};std::vector<uint64_t> buffer(13*8192);uint64_t left=header[2];
    while(left) {
        size_t rows=std::min<uint64_t>(8192,left);
        if(!in.read(reinterpret_cast<char*>(buffer.data()),rows*104))return 4;
        for(size_t i=0;i<rows;i++) {
            const uint64_t* row=buffer.data()+i*13;Mask mask;
            std::copy(row,row+6,mask.w.begin());int k=mask.count();
            if(k<8 && row[6]<2)++histogram[k][row[6]];
            if(k==root.count()+1){auto found=layer.find(mask);if(found!=layer.end())found->second.label=row[6];}
            if(k==root.count()+2){auto found=leaves.find(mask);if(found!=leaves.end())found->second=row[6];}
        }
        left-=rows;
    }
    auto ids=[](const Mask& key){std::cout<<"[";bool first=true;for(int p:key.ids()){if(!first)std::cout<<",";first=false;std::cout<<p;}std::cout<<"]";};
    std::cout<<"{\"root\":";ids(root);std::cout<<",\"candidate_rows\":"<<header[2]<<",\"shallow_candidate_counts\":[";
    for(int k=0;k<8;k++){if(k)std::cout<<",";std::cout<<"["<<histogram[k][0]<<","<<histogram[k][1]<<"]";}
    std::cout<<"],\"children\":[";bool first=true;
    for(const auto& [key,state]:layer) {
        int counts[3]{};for(const Mask& child:state.children)++counts[leaves.at(child)+1];
        if(!first)std::cout<<",";
        first=false;std::cout<<"{\"root\":";ids(key);
        std::cout<<",\"candidate_label\":"<<state.label<<",\"child_unknown\":"<<counts[0]<<",\"child_P\":"<<counts[1]<<",\"child_N\":"<<counts[2]<<"}";
    }
    std::cout<<"]}\n";
}
