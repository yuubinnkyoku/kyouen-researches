// Independent terminal-four survey: Bareiss determinants, independent symmetries.
// No search-solver geometry or canonicalization is called.
#define main historical_verifier_main
#include "../cube-q5-seven-balanced-20261023/verify_incremental.cpp"
#undef main
#include <set>

int main(int argc,char**argv) {
    try {
        if(argc!=2)throw std::runtime_error("usage: verify_pairs side");
        int side=std::stoi(argv[1]),n=side*side*side;
        if(side<3 || side>7)throw std::runtime_error("unsupported side");
        std::vector<std::array<int64_t,5>> lift(n);
        for(int i=0;i<n;i++) {
            int x=i/(side*side),y=i/side%side,z=i%side;
            lift[i]={x*x+y*y+z*z,x,y,z,1};
        }
        std::array<int,5> frame={0,1,2,side,side*side};
        Matrix basis;for(int i=0;i<5;i++)basis[i]=lift[frame[i]];
        if(!determinant(basis))throw std::runtime_error("singular frame");
        std::vector<std::vector<int>> symmetries;
        std::array<int,3> perm={0,1,2};
        do {
            for(int flip=0;flip<8;flip++) {
                std::vector<int> map(n);
                for(int i=0;i<n;i++) {
                    std::array<int,3> p={i/(side*side),i/side%side,i%side},q{};
                    for(int j=0;j<3;j++)q[j]=(flip&(1<<j))?side-1-p[perm[j]]:p[perm[j]];
                    map[i]=(q[0]*side+q[1])*side+q[2];
                }
                symmetries.push_back(map);
            }
        } while(std::next_permutation(perm.begin(),perm.end()));
        auto canon=[&](const std::vector<int>& points) {
            U best=~U();
            for(const auto& map:symmetries) {
                U mask;for(int p:points)mask|=U(1)<<map[p];
                if(mask<best)best=mask;
            }
            return best;
        };
        std::set<U> pairs;
        for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)pairs.insert(canon({a,b}));
        uint64_t checks=0;
        for(const auto& pair:pairs) {
            auto p=elements(pair);int a=p[0],b=p[1];
            std::vector<int> bad;std::set<U> orbits;
            // The terminal-four relation is symmetric in the third and fourth point.
            std::vector<bool> covered(n,false);
            for(int c=0;c<n;c++)if(c!=a && c!=b && !covered[c]) {
                bool found=false;
                for(int d=0;d<n;d++)if(d!=a && d!=b && d!=c) {
                    Matrix m;m[0]=lift[a];m[1]=lift[b];m[2]=lift[c];m[3]=lift[d];
                    bool terminal=true;
                    for(int f:frame) {
                        m[4]=lift[f];++checks;
                        if(determinant(m)){terminal=false;break;}
                    }
                    if(terminal){found=true;covered[c]=covered[d]=true;break;}
                }
                if(!found){bad.push_back(c);orbits.insert(canon({a,b,c}));}
            }
            std::cout<<"{\"pair\":["<<a<<","<<b<<"],\"uncovered\":"<<bad.size()<<",\"residual_triple_orbits\":"<<orbits.size()<<",\"thirds\":[";
            for(size_t i=0;i<bad.size();i++){if(i)std::cout<<",";std::cout<<bad[i];}
            std::cout<<"],\"representatives\":[";bool first=true;
            for(const auto& orbit:orbits){if(!first)std::cout<<",";first=false;auto v=elements(orbit);std::cout<<"["<<v[0]<<","<<v[1]<<","<<v[2]<<"]";}
            std::cout<<"]}"<<std::endl;
        }
        std::cerr<<"{\"pairs\":"<<pairs.size()<<",\"determinants\":"<<checks<<",\"frame_determinant\":"<<determinant(basis)<<"}\n";
        return 0;
    } catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 1;}
}
