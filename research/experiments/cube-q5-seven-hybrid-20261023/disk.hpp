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
    static uint64_t word(const unsigned char* p){uint64_t value;std::memcpy(&value,p,8);return value;}
public:
    uint64_t rows=0,nodes=0,slots=0,fingerprint=0;
    int side=0;
    explicit DiskBase(const std::string& path,const std::string& index_path) {
        static_assert(__BYTE_ORDER__==__ORDER_LITTLE_ENDIAN__,"little endian required");
        data=std::make_unique<Mapping>(path);
        if(data->size<32 || std::memcmp(data->data,"Q5MEMO2\n",8))throw std::runtime_error("bad base magic");
        side=word(data->data+8);nodes=word(data->data+16);rows=word(data->data+24);
        if(side<3 || side>7 || rows>=UINT32_MAX || data->size!=32+104*rows)throw std::runtime_error("bad base header");
        std::ifstream existing(index_path,std::ios::binary);
        if(!existing) {
            slots=1;while(slots<rows+rows/2+1)slots*=2;
            std::vector<uint64_t> offsets(slots);
            fingerprint=0xcbf29ce484222325ULL;
            for(uint64_t i=0;i<rows;i++) {
                const auto* row=data->data+32+104*i;Mask key;std::memcpy(key.w.data(),row,48);
                uint64_t label=word(row+48);
                if(label>1)throw std::runtime_error("bad base label");
                for(int p:key.ids())if(p>=side*side*side)throw std::runtime_error("base key outside board");
                uint64_t hash=Hash{}(key),tag=hash&0xffffffff00000000ULL;
                size_t bucket=hash&(slots-1);
                while(offsets[bucket]) {
                    if((offsets[bucket]&0xffffffff00000000ULL)==tag) {
                        Mask previous;std::memcpy(previous.w.data(),data->data+32+104*(uint64_t(uint32_t(offsets[bucket]))-1),48);
                        if(previous==key)throw std::runtime_error("duplicate base row");
                    }
                    bucket=(bucket+1)&(slots-1);
                }
                offsets[bucket]=tag|(i+1);
                for(int j=0;j<13;j++)fingerprint=(fingerprint^word(row+8*j))*0x100000001b3ULL;
            }
            header={uint64_t(side),nodes,rows,slots,data->size,fingerprint,0};
            std::ofstream out(index_path+".new",std::ios::binary);out.write("Q5IDX2\n\0",8);
            out.write(reinterpret_cast<const char*>(header.data()),56);
            out.write(reinterpret_cast<const char*>(offsets.data()),offsets.size()*8);out.close();
            if(!out || std::rename((index_path+".new").c_str(),index_path.c_str()))throw std::runtime_error("index write failed");
        }
        index=std::make_unique<Mapping>(index_path);
        if(index->size<64 || std::memcmp(index->data,"Q5IDX2\n\0",8))throw std::runtime_error("bad index magic");
        std::memcpy(header.data(),index->data+8,56);
        slots=header[3];fingerprint=header[5];
        if(header[0]!=uint64_t(side) || header[1]!=nodes || header[2]!=rows || header[4]!=data->size || !slots || (slots&(slots-1)) || index->size!=64+slots*8)throw std::runtime_error("index/base mismatch");
    }
    std::optional<Entry> get(const Mask& key)const {
        uint64_t hash=Hash{}(key),tag=hash&0xffffffff00000000ULL;
        size_t bucket=hash&(slots-1);
        for(uint64_t probes=0;probes<slots;probes++) {
            uint64_t cell;std::memcpy(&cell,index->data+64+bucket*8,8);uint32_t offset=cell;
            if(!offset)return {};
            if(offset>rows)throw std::runtime_error("index offset outside base");
            if((cell&0xffffffff00000000ULL)!=tag){bucket=(bucket+1)&(slots-1);continue;}
            const auto* row=data->data+32+104*(uint64_t(offset)-1);Mask candidate;
            std::memcpy(candidate.w.data(),row,48);
            if(candidate==key){Entry entry{};entry.win=word(row+48);std::memcpy(entry.witness.w.data(),row+56,48);return entry;}
            bucket=(bucket+1)&(slots-1);
        }
        throw std::runtime_error("full/corrupt index");
    }
    template<class F> void each(F callback)const {
        for(uint64_t i=0;i<rows;i++) {
            const auto* row=data->data+32+104*i;Mask key;Entry entry{};
            std::memcpy(key.w.data(),row,48);entry.win=word(row+48);std::memcpy(entry.witness.w.data(),row+56,48);
            callback(key,entry);
        }
    }
};
