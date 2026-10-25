#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <vector>

// Independent verifier: enumerate actual q-subsets of {0,1}^d.
// Integer fraction-free elimination, without finite fields or pattern
// support grouping. Intended for d<=6, q<=6.
struct LatticeBasis {
    int d, rank=0;
    std::array<std::array<int64_t,6>,6> b{};
    std::array<bool,6> used{};
    explicit LatticeBasis(int dim):d(dim){}
    void reduce(std::array<int64_t,6>& v) const {
        for(int j=0;j<d;++j)if(used[j] && v[j]) {
            int64_t a=b[j][j], c=v[j];
            // Scale ALL columns, including earlier non-pivot columns.
            for(int k=0;k<d;++k)v[k]=a*v[k]-c*b[j][k];
            int64_t g=0;
            for(int k=0;k<d;++k)g=std::gcd(g,std::llabs(v[k]));
            if(g>1)for(int k=0;k<d;++k)v[k]/=g;
        }
    }
    void add(std::array<int64_t,6> v) {
        reduce(v);
        for(int j=0;j<d;++j)if(v[j]) {
            int64_t g=0;
            for(int k=j;k<d;++k)g=std::gcd(g,std::llabs(v[k]));
            if(g>1)for(int k=j;k<d;++k)v[k]/=g;
            if(v[j]<0)for(int k=j;k<d;++k)v[k]=-v[k];
            b[j]=v;used[j]=true;++rank;
            return;
        }
    }
    bool contains(std::array<int64_t,6> v) const {
        reduce(v);
        for(int j=0;j<d;++j)if(v[j])return false;
        return true;
    }
};

int main(int argc,char**argv) {
    if(argc!=3)return 2;
    int d=std::atoi(argv[1]), q=std::atoi(argv[2]);
    if(d<1||d>6||q<1||q>6||q>(1<<d))return 2;
    int n=1<<d;
    std::vector<int> pick(q);
    std::vector<uint64_t> by_rank(d+1,0);
    uint64_t checked=0;
    auto run=[&]() {
        ++checked;
        LatticeBasis basis(d);
        for(int j=1;j<q;++j) {
            std::array<int64_t,6> v{};
            for(int c=0;c<d;++c)
                v[c]=((pick[j]>>c)&1)-((pick[0]>>c)&1);
            basis.add(v);
        }
        if(basis.rank==d)return;
        int count=0;
        for(int x=0;x<n;++x) {
            std::array<int64_t,6> v{};
            for(int c=0;c<d;++c)
                v[c]=((x>>c)&1)-((pick[0]>>c)&1);
            count+=basis.contains(v);
            if(count>q)break;
        }
        if(count==q)++by_rank[basis.rank];
    };
    auto recur=[&](auto&&self,int depth,int start)->void {
        if(depth==q){run();return;}
        for(int i=start;i<=n-(q-depth);++i) {
            pick[depth]=i;
            self(self,depth+1,i+1);
        }
    };
    recur(recur,0,0);
    std::cout<<"d="<<d<<" q="<<q<<" checked="<<checked;
    uint64_t total=0;
    for(int i=0;i<=d;++i)if(by_rank[i]) {
        std::cout<<" rank"<<i<<"="<<by_rank[i];
        total+=by_rank[i];
    }
    std::cout<<" total="<<total<<"\n";
    return 0;
}
