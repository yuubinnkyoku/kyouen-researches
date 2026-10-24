// All safe positions for n*n<=25. Independent integer determinant construction
// and incremental triple-completion recursion; writes compact JSON to stdout.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using Mask = uint32_t;
using I = int64_t;

I det3(const std::array<std::array<I,3>,3>& r) {
    return r[0][0]*(r[1][1]*r[2][2]-r[1][2]*r[2][1])
         - r[0][1]*(r[1][0]*r[2][2]-r[1][2]*r[2][0])
         + r[0][2]*(r[1][0]*r[2][1]-r[1][1]*r[2][0]);
}

struct Census {
    int n, count;
    bool generic;
    I numerator, denominator;
    std::vector<Mask> edges, completion;
    std::vector<uint8_t> grundy;
    std::array<uint64_t,26> layers{}, terminal{}, hist{};
    uint64_t states = 0, calls = 0;
    Census(int side, bool gen, I p, I q):n(side),count(side*side),generic(gen),
        numerator(p),denominator(q),completion(count*count*count,0),
        grundy(size_t(1)<<count,255) {}
    size_t index(int a,int b,int c) const {
        std::array<int,3> t{a,b,c}; std::sort(t.begin(),t.end());
        return (t[0]*count+t[1])*count+t[2];
    }
    I coefficient(const std::array<int,4>& ids, bool y_squared) const {
        std::array<std::array<I,3>,3> r{};
        I x0=ids[3]%n,y0=ids[3]/n;
        I z0=y_squared?y0*y0:x0*x0;
        for(int i=0;i<3;++i){
            I x=ids[i]%n,y=ids[i]/n,z=y_squared?y*y:x*x;
            r[i]={z-z0,x-x0,y-y0};
        }
        return det3(r);
    }
    void build() {
        for(int a=0;a<count;++a)for(int b=a+1;b<count;++b)
        for(int c=b+1;c<count;++c)for(int d=c+1;d<count;++d){
            std::array<int,4> t{a,b,c,d};
            I ca=coefficient(t,true),cb=coefficient(t,false);
            if(generic ? (ca!=0||cb!=0) : (numerator*ca+denominator*cb!=0))continue;
            Mask e=(Mask(1)<<a)|(Mask(1)<<b)|(Mask(1)<<c)|(Mask(1)<<d);
            edges.push_back(e);
            for(int omit=0;omit<4;++omit){
                std::array<int,3> tri{}; int j=0;
                for(int i=0;i<4;++i)if(i!=omit)tri[j++]=t[i];
                completion[index(tri[0],tri[1],tri[2])]|=Mask(1)<<t[omit];
            }
        }
    }
    uint8_t solve(Mask occupied, Mask legal) {
        ++calls;
        if(grundy[occupied]!=255)return grundy[occupied];
        ++states;
        int stones=__builtin_popcount(occupied); ++layers[stones];
        if(!legal)++terminal[stones];
        uint64_t options=0;
        Mask choices=legal;
        while(choices){
            int p=__builtin_ctz(choices); Mask bit=Mask(1)<<p; choices^=bit;
            Mask child=occupied|bit;
            uint8_t value=grundy[child];
            if(value==255){
                Mask next=legal^bit, as=occupied;
                while(as){
                    int a=__builtin_ctz(as);as&=as-1;
                    Mask bs=as;
                    while(bs){
                        int b=__builtin_ctz(bs);bs&=bs-1;
                        next&=~completion[index(p,a,b)];
                    }
                }
                value=solve(child,next);
            }
            options|=uint64_t(1)<<value;
        }
        uint8_t value=0;while(options&(uint64_t(1)<<value))++value;
        grundy[occupied]=value; ++hist[value];return value;
    }
    template<class T> void array_json(const T& a){
        std::cout<<'[';bool first=true;for(auto x:a){if(!first)std::cout<<',';first=false;std::cout<<uint64_t(x);}std::cout<<']';
    }
    void output() {
        std::cout<<"{\"side\":"<<n<<",\"lambda\":\"";
        if(generic)std::cout<<"generic";else std::cout<<numerator<<'/'<<denominator;
        std::cout<<"\",\"edge_count\":"<<edges.size()<<",\"empty_grundy\":"<<unsigned(grundy[0])
                 <<",\"safe_count\":"<<states<<",\"calls\":"<<calls<<",\"safe_layers\":";
        array_json(layers); std::cout<<",\"terminal_sizes\":";array_json(terminal);
        std::cout<<",\"grundy_histogram\":";array_json(hist);
        std::vector<int> first;for(int i=0;i<count;++i)first.push_back(grundy[Mask(1)<<i]);
        std::cout<<",\"first_move_grundy\":";array_json(first);
        std::cout<<",\"edges\":";array_json(edges);std::cout<<"}\n";
    }
};

int main(int argc,char**argv){
    if(argc!=3&&argc!=4){std::cerr<<"usage: census SIDE generic | census SIDE NUMERATOR DENOMINATOR\n";return 2;}
    int n=std::atoi(argv[1]);bool generic=std::string(argv[2])=="generic";
    if(n<2||n>5||(!generic&&argc!=4)){std::cerr<<"require 2<=SIDE<=5 and parameter\n";return 2;}
    I p=generic?0:std::stoll(argv[2]),q=generic?1:std::stoll(argv[3]);
    if(q<=0||std::abs(p)>1000000||q>1000000)return 2;
    Census job(n,generic,p,q);job.build();job.solve(0,(Mask(1)<<(n*n))-1);
    if(const char* path=std::getenv("KYOUEN_GRUNDY_DUMP")){
        std::ofstream out(path,std::ios::binary);out.write(reinterpret_cast<const char*>(job.grundy.data()),job.grundy.size());
        if(!out)return 3;
    }
    job.output();
}
