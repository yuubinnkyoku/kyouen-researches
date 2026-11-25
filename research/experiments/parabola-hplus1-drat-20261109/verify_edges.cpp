// Check every supplied edge by generic integer geometry, without the generator.
#define main unused_subset_main
#include "../parabola-local-repair-20261109/verify_subset.cpp"
#undef main
#include <fstream>
#include <string>
int main(int argc,char**argv){
    if(argc!=2)return 2;
    std::ifstream input(argv[1]);
    int p,n;
    if(!(input>>p>>n) || !prime(p) || p>100000 || n<1)return 2;
    for(int i=0;i<n;++i){
        std::array<int,4> q;
        for(int& t:q)if(!(input>>t))return 2;
        if(q[0]<0 || q[3]>=p || !(q[0]<q[1] && q[1]<q[2] && q[2]<q[3]))return 3;
        if(determinant(q,p)!=0){std::cerr<<"NONEDGE "<<i<<'\n';return 4;}
    }
    std::string extra;if(input>>extra)return 2;
    std::cout<<"VERIFIED_EDGES "<<p<<' '<<n<<'\n';
    return 0;
}
