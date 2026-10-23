// Immutable Q5MEMO2 base and a compact open-addressed row-offset index.
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <cstring>
#include <memory>
#include <optional>
class Mapping {
    int fd=-1;
public:
    size_t size=0;const unsigned char* data=nullptr;
    explicit Mapping(const std::string& path) {
        fd=open(path.c_str(),O_RDONLY);struct stat st{};
        if(fd<0 || fstat(fd,&st) || st.st_size<=0)throw std::runtime_error("cannot map "+path);
        size=st.st_size;auto address=mmap(nullptr,size,PROT_READ,MAP_SHARED,fd,0);
        if(address==MAP_FAILED)throw std::runtime_error("mmap failed");
        data=static_cast<const unsigned char*>(address);
    }
    ~Mapping(){if(data)munmap(const_cast<unsigned char*>(data),size);if(fd>=0)close(fd);}
    Mapping(const Mapping&)=delete;
};
class DiskBase {
    std::unique_ptr<Mapping> data,index;
    std::array<uint64_t,7> header{};
    uint64_t row_offset=32,bloom_bits=0;
    static uint64_t word(const unsigned char* p){uint64_t value;std::memcpy(&value,p,8);return value;}
public:
    uint64_t rows=0,nodes=0,slots=0,fingerprint=0;
    int side=0;
    bool overlay=false;
    uint64_t parent_fingerprint=0,parent_rows=0,parent_nodes=0;
    explicit DiskBase(const std::string& path,const std::string& index_path) {
        static_assert(__BYTE_ORDER__==__ORDER_LITTLE_ENDIAN__,"little endian required");
        data=std::make_unique<Mapping>(path);
        if(data->size<32)throw std::runtime_error("bad base magic");
        if(!std::memcmp(data->data,"Q5MEMO2\n",8)) {
            side=word(data->data+8);nodes=word(data->data+16);rows=word(data->data+24);
            if(data->size!=32+104*rows)throw std::runtime_error("bad base length");
        }else if(data->size>=88 && (!std::memcmp(data->data,"Q5HYB1\n\0",8) || !std::memcmp(data->data,"Q5HYB2\n\0",8))) {
            overlay=true;row_offset=80;side=word(data->data+8);nodes=word(data->data+56);rows=word(data->data+64);
            parent_fingerprint=word(data->data+16);parent_rows=word(data->data+24);parent_nodes=word(data->data+32);
            if(data->size<88+104*rows || std::memcmp(data->data+data->size-8,"Q5END1\n\0",8))throw std::runtime_error("incomplete overlay");
        }else throw std::runtime_error("bad base magic");
        if(side<3 || side>7 || rows>=UINT32_MAX)throw std::runtime_error("bad base header");
        std::ifstream existing(index_path,std::ios::binary);
        if(!existing) {
            slots=1;while(slots<rows+rows/2+1)slots*=2;
            std::vector<uint64_t> offsets(slots);
            bloom_bits=64;while(bloom_bits<rows*8)bloom_bits*=2;
            std::vector<uint64_t> bloom(bloom_bits/64);
            fingerprint=0xcbf29ce484222325ULL;
            for(uint64_t i=0;i<rows;i++) {
                const auto* row=data->data+row_offset+104*i;Mask key;std::memcpy(key.w.data(),row,48);
                uint64_t label=word(row+48);
                if(label>1)throw std::runtime_error("bad base label");
                for(int p:key.ids())if(p>=side*side*side)throw std::runtime_error("base key outside board");
                uint64_t hash=Hash{}(key),tag=hash&0xffffffff00000000ULL;
                uint64_t first=uint32_t(hash),step=(hash>>32)|1;
                for(int k=0;k<4;k++){uint64_t bit=(first+k*step)&(bloom_bits-1);bloom[bit/64]|=uint64_t(1)<<(bit%64);}
                size_t bucket=hash&(slots-1);
                while(offsets[bucket]) {
                    if((offsets[bucket]&0xffffffff00000000ULL)==tag) {
                        Mask previous;std::memcpy(previous.w.data(),data->data+row_offset+104*(uint64_t(uint32_t(offsets[bucket]))-1),48);
                        if(previous==key)throw std::runtime_error("duplicate base row");
                    }
                    bucket=(bucket+1)&(slots-1);
                }
                offsets[bucket]=tag|(i+1);
                for(int j=0;j<13;j++)fingerprint=(fingerprint^word(row+8*j))*0x100000001b3ULL;
            }
            header={uint64_t(side),nodes,rows,slots,data->size,fingerprint,bloom_bits};
            std::ofstream out(index_path+".new",std::ios::binary);out.write("Q5IDX3\n\0",8);
            out.write(reinterpret_cast<const char*>(header.data()),56);
            out.write(reinterpret_cast<const char*>(offsets.data()),offsets.size()*8);
            out.write(reinterpret_cast<const char*>(bloom.data()),bloom.size()*8);out.close();
            if(!out || std::rename((index_path+".new").c_str(),index_path.c_str()))throw std::runtime_error("index write failed");
        }
        index=std::make_unique<Mapping>(index_path);
        if(index->size<64 || (std::memcmp(index->data,"Q5IDX2\n\0",8) && std::memcmp(index->data,"Q5IDX3\n\0",8)))throw std::runtime_error("bad index magic");
        std::memcpy(header.data(),index->data+8,56);
        slots=header[3];fingerprint=header[5];bloom_bits=header[6];
        if(header[0]!=uint64_t(side) || header[1]!=nodes || header[2]!=rows || header[4]!=data->size || !slots || (slots&(slots-1)) || (bloom_bits && ((bloom_bits&(bloom_bits-1)) || bloom_bits<64)) || index->size!=64+slots*8+bloom_bits/8)throw std::runtime_error("index/base mismatch");
    }
    std::optional<Entry> get(const Mask& key)const {
        uint64_t hash=Hash{}(key),tag=hash&0xffffffff00000000ULL;
        if(bloom_bits) {
            uint64_t first=uint32_t(hash),step=(hash>>32)|1;
            for(int k=0;k<4;k++) {
                uint64_t bit=(first+k*step)&(bloom_bits-1),bits=word(index->data+64+slots*8+(bit/64)*8);
                if(!(bits>>(bit%64)&1))return {};
            }
        }
        size_t bucket=hash&(slots-1);
        for(uint64_t probes=0;probes<slots;probes++) {
            uint64_t cell;std::memcpy(&cell,index->data+64+bucket*8,8);uint32_t offset=cell;
            if(!offset)return {};
            if(offset>rows)throw std::runtime_error("index offset outside base");
            if((cell&0xffffffff00000000ULL)!=tag){bucket=(bucket+1)&(slots-1);continue;}
            const auto* row=data->data+row_offset+104*(uint64_t(offset)-1);Mask candidate;
            std::memcpy(candidate.w.data(),row,48);
            if(candidate==key){Entry entry{};entry.win=word(row+48);std::memcpy(entry.witness.w.data(),row+56,48);return entry;}
            bucket=(bucket+1)&(slots-1);
        }
        throw std::runtime_error("full/corrupt index");
    }
    template<class F> void each(F callback)const {
        for(uint64_t i=0;i<rows;i++) {
            const auto* row=data->data+row_offset+104*i;Mask key;Entry entry{};
            std::memcpy(key.w.data(),row,48);entry.win=word(row+48);std::memcpy(entry.witness.w.data(),row+56,48);
            callback(key,entry);
        }
    }
};
class DiskStack {
    std::vector<std::unique_ptr<DiskBase>> layers;
    static std::vector<std::string> split(const std::string& text) {
        std::vector<std::string> result;std::istringstream in(text);std::string part;
        while(std::getline(in,part,','))result.push_back(part);
        return result;
    }
public:
    uint64_t rows=0,nodes=0,fingerprint=0,previous_rows=0,previous_nodes=0,previous_fingerprint=0;
    int side=0;std::string last_path;
    DiskStack(const std::string& paths,const std::string& indices) {
        auto files=split(paths),indexes=split(indices);if(files.empty() || files.size()!=indexes.size())throw std::runtime_error("bad layer paths");
        for(size_t i=0;i<files.size();i++) {
            auto layer=std::make_unique<DiskBase>(files[i],indexes[i]);
            if(!i) {
                if(layer->overlay)throw std::runtime_error("first layer must be Q5MEMO2");
                side=layer->side;rows=layer->rows;nodes=layer->nodes;fingerprint=layer->fingerprint;
            }else {
                if(!layer->overlay || layer->side!=side || layer->parent_fingerprint!=fingerprint || layer->parent_rows!=rows || layer->parent_nodes!=nodes)throw std::runtime_error("overlay dependency mismatch");
                previous_rows=rows;previous_nodes=nodes;previous_fingerprint=fingerprint;
                rows+=layer->rows;nodes=layer->nodes;fingerprint=(fingerprint^layer->fingerprint)*0x100000001b3ULL;
            }
            last_path=files[i];layers.push_back(std::move(layer));
        }
    }
    bool has_overlay()const{return layers.size()>1;}
    std::optional<Entry> get(const Mask& key)const {
        for(auto it=layers.rbegin();it!=layers.rend();it++){auto value=(*it)->get(key);if(value)return value;}
        return {};
    }
    template<class F> void each(F callback)const{for(const auto& layer:layers)layer->each(callback);}
};
