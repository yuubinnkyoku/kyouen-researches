// Restrict an exact candidate cache to descendants of each selected root.
// Every child preserves containment of some cube image of the root.
#define main historical_solver_main
#include "../cube-q5-seven-frontier-20261022/solver.cpp"
#undef main
#include "../cube-q5-seven-hybrid-20261023/layers.hpp"
#include <set>
struct Output {
    Mask root;
    std::vector<Mask> images;
    std::unordered_map<Mask,Entry,Hash> rows;
    uint64_t duplicates=0;
    bool contains(const Mask& key)const {
        for(const auto& image:images) {
            bool subset=true;
            for(int j=0;j<6;j++)if((key.w[j]&image.w[j])!=image.w[j]){subset=false;break;}
            if(subset)return true;
        }
        return false;
    }
};
uint64_t read_word(const unsigned char* bytes){uint64_t value;std::memcpy(&value,bytes,8);return value;}
int main(int argc,char**argv) {
    try {
        if(argc<5)throw std::runtime_error("usage: filter side roots output-prefix inputs...");
        int side=std::stoi(argv[1]);Solver solver(side,0,1000000);
        std::ifstream roots(argv[2]);if(!roots)throw std::runtime_error("missing roots");
        std::string line;std::vector<Output> outputs;
        while(std::getline(roots,line)) {
            if(line.empty())continue;
            Output output;std::istringstream row(line);int p;
            while(row>>p){if(p<0 || p>=solver.n || output.root.has(p))throw std::runtime_error("bad root");output.root.set(p);}
            if(!output.root.count())throw std::runtime_error("empty root");
            output.root=solver.canonical(output.root);std::set<Mask> images;
            for(const auto& symmetry:solver.sym){Mask image;for(int q:output.root.ids())image.set(symmetry[q]);images.insert(image);}
            output.images.assign(images.begin(),images.end());outputs.push_back(std::move(output));
        }
        if(outputs.empty())throw std::runtime_error("no roots");
        uint64_t counter_seed=0,scanned=0;
        for(int argument=4;argument<argc;argument++) {
            Mapping input(argv[argument]);uint64_t offset=0,rows=0,nodes=0;
            if(input.size>=32 && !std::memcmp(input.data,"Q5MEMO2\n",8)) {
                if(read_word(input.data+8)!=uint64_t(side))throw std::runtime_error("side mismatch");
                offset=32;nodes=read_word(input.data+16);rows=read_word(input.data+24);
                if(input.size!=32+104*rows)throw std::runtime_error("bad memo length");
            }else if(input.size>=88 && (!std::memcmp(input.data,"Q5HYB1\n\0",8) || !std::memcmp(input.data,"Q5HYB2\n\0",8))) {
                if(read_word(input.data+8)!=uint64_t(side))throw std::runtime_error("side mismatch");
                offset=80;nodes=read_word(input.data+56);rows=read_word(input.data+64);
                if(input.size<88+104*rows || std::memcmp(input.data+input.size-8,"Q5END1\n\0",8))throw std::runtime_error("incomplete hybrid");
            }else throw std::runtime_error("unrecognized input");
            counter_seed=std::max(counter_seed,nodes);scanned+=rows;
            madvise(const_cast<unsigned char*>(input.data),input.size,MADV_SEQUENTIAL);
            for(uint64_t i=0;i<rows;i++) {
                const auto* row=input.data+offset+104*i;Mask key;std::memcpy(key.w.data(),row,48);
                for(auto& output:outputs)if(output.contains(key)) {
                    Entry entry;uint64_t label=read_word(row+48);std::memcpy(entry.witness.w.data(),row+56,48);
                    if(label>1)throw std::runtime_error("bad label");
                    entry.win=label;
                    for(int p:key.ids())if(p>=solver.n)throw std::runtime_error("key outside board");
                    if(!entry.win && entry.witness.count())throw std::runtime_error("nonzero P witness");
                    auto [it,added]=output.rows.emplace(key,entry);
                    if(!added){++output.duplicates;if(it->second.win!=entry.win)throw std::runtime_error("conflicting exact labels");}
                }
            }
            std::cerr<<"scanned "<<argv[argument]<<" rows="<<rows<<"\n";
        }
        for(size_t i=0;i<outputs.size();i++) {
            auto& output=outputs[i];uint64_t checked_n=0;
            for(const auto& [key,entry]:output.rows)if(entry.win) {
                (void)key;auto witness=output.rows.find(entry.witness);
                if(witness==output.rows.end() || witness->second.win)throw std::runtime_error("missing P witness after restriction");
                ++checked_n;
            }
            std::string path=std::string(argv[3])+"-"+std::to_string(i)+".memo";
            if(std::ifstream(path).good())throw std::runtime_error("refusing to overwrite output");
            std::ofstream out(path+".new",std::ios::binary);out.write("Q5MEMO2\n",8);
            std::array<uint64_t,3> header{uint64_t(side),counter_seed,output.rows.size()};out.write(reinterpret_cast<const char*>(header.data()),24);
            for(const auto& [key,entry]:output.rows) {
                out.write(reinterpret_cast<const char*>(key.w.data()),48);uint64_t label=entry.win;out.write(reinterpret_cast<const char*>(&label),8);out.write(reinterpret_cast<const char*>(entry.witness.w.data()),48);
            }
            out.close();if(!out || std::rename((path+".new").c_str(),path.c_str()))throw std::runtime_error("write failed");
            std::cout<<"{\"output\":\""<<path<<"\",\"root\":[";bool comma=false;for(int p:output.root.ids()){if(comma)std::cout<<",";comma=true;std::cout<<p;}
            std::cout<<"],\"source_rows_scanned\":"<<scanned<<",\"rows\":"<<output.rows.size()<<",\"root_images\":"<<output.images.size()<<",\"duplicates\":"<<output.duplicates<<",\"n_witnesses_retained\":"<<checked_n<<",\"counter_seed\":"<<counter_seed<<",\"labels_are_candidates\":true}\n";
        }
        return 0;
    }catch(const std::exception& error){std::cerr<<error.what()<<"\n";return 1;}
}
