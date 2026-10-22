// Exhaustive audit of every safe x-reflection-invariant state, <=64 points.
// Geometry: cofactor normal of the three lifted difference rows for each 4-set.
// Deliberately separate from the older solver's 5x5 Bareiss implementation.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <vector>
using U = uint64_t;
using Row = std::array<int64_t, 4>;

int64_t det3(const std::array<std::array<int64_t, 3>, 3>& a) {
    return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
         - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
         + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]);
}

int main(int argc, char** argv) {
    if (argc != 4) throw std::runtime_error("usage: audit X Y Z (X even, XYZ<=64)");
    int X=std::stoi(argv[1]), Y=std::stoi(argv[2]), Z=std::stoi(argv[3]);
    if (X<2 || X%2 || Y<1 || Z<1 || int64_t(X)*Y*Z>64)
        throw std::runtime_error("requires even X and 1<=XYZ<=64");
    std::vector<Row> pts;
    for(int x=0;x<X;x++) for(int y=0;y<Y;y++) for(int z=0;z<Z;z++)
        pts.push_back({x*x+y*y+z*z,x,y,z});
    int n=pts.size();
    U all=n==64 ? ~U(0) : (U(1)<<n)-1;
    uint64_t choose[65][6]{};
    for(int i=0;i<=n;i++) {
        choose[i][0]=1;
        for(int j=1;j<=5;j++) if(i) choose[i][j]=choose[i-1][j-1]+choose[i-1][j];
    }
    auto index=[&](int a,int b,int c,int d){
        return choose[a][1]+choose[b][2]+choose[c][3]+choose[d][4];
    };
    std::vector<U> completion(choose[n][4]);
    uint64_t incidences=0;
    for(int a=0;a<n;a++) for(int b=a+1;b<n;b++)
    for(int c=b+1;c<n;c++) for(int d=c+1;d<n;d++) {
        std::array<Row,3> rows;
        int ids[3]{b,c,d};
        for(int i=0;i<3;i++) for(int j=0;j<4;j++) rows[i][j]=pts[ids[i]][j]-pts[a][j];
        Row normal{};
        for(int j=0;j<4;j++) {
            std::array<std::array<int64_t,3>,3> minor{};
            for(int i=0;i<3;i++) for(int k=0,t=0;k<4;k++)
                if(k!=j) minor[i][t++]=rows[i][k];
            normal[j]=(j%2 ? -1 : 1)*det3(minor);
        }
        U blocked=0;
        for(int e=0;e<n;e++) if(e!=a && e!=b && e!=c && e!=d) {
            int64_t value=0;
            for(int j=0;j<4;j++) value+=normal[j]*(pts[e][j]-pts[a][j]);
            if(!value) blocked|=U(1)<<e;
        }
        completion[index(a,b,c,d)]=blocked;
        incidences+=__builtin_popcountll(blocked);
    }
    if(incidences%5) throw std::runtime_error("inconsistent incidence count");
    auto legal=[&](U mask) {
        std::vector<int> ids;
        for(U b=mask;b;b&=b-1) ids.push_back(__builtin_ctzll(b));
        U blocked=mask;
        int k=ids.size();
        for(int a=0;a<k;a++) for(int b=a+1;b<k;b++)
        for(int c=b+1;c<k;c++) for(int d=c+1;d<k;d++)
            blocked|=completion[index(ids[a],ids[b],ids[c],ids[d])];
        return all&~blocked;
    };
    std::vector<int> mirror(n), reps;
    for(int x=0;x<X;x++) for(int y=0;y<Y;y++) for(int z=0;z<Z;z++) {
        int i=(x*Y+y)*Z+z;
        mirror[i]=((X-1-x)*Y+y)*Z+z;
        if(i<mirror[i]) reps.push_back(i);
    }
    uint64_t states=0, replies=0, terminals=0;
    std::map<int,uint64_t> by_stones, terminal_by_stones;
    auto visit=[&](auto&& self,U mask,int next)->void {
        ++states;
        int k=__builtin_popcountll(mask);
        ++by_stones[k];
        U moves=legal(mask);
        if(!moves) {++terminals; ++terminal_by_stones[k];}
        for(U b=moves;b;b&=b-1) {
            int p=__builtin_ctzll(b), q=mirror[p];
            if(!(moves&(U(1)<<q)) || !(legal(mask|(U(1)<<p))&(U(1)<<q)))
                throw std::runtime_error("illegal reflection reply");
            ++replies;
        }
        for(int j=next;j<int(reps.size());j++) {
            int p=reps[j],q=mirror[p];
            if(moves&(U(1)<<p)) self(self,mask|(U(1)<<p)|(U(1)<<q),j+1);
        }
    };
    visit(visit,0,0);
    auto print_map=[](const std::map<int,uint64_t>& values) {
        std::cout<<"{";
        bool first=true;
        for(auto [k,v]:values) {if(!first)std::cout<<",";first=false;std::cout<<'"'<<k<<"\":"<<v;}
        std::cout<<"}";
    };
    std::cout<<"{\"shape\":["<<X<<","<<Y<<","<<Z<<"],\"forbidden_five_sets\":"<<incidences/5
             <<",\"symmetric_safe_states\":"<<states<<",\"legal_reply_checks\":"<<replies
             <<",\"symmetric_terminal_states\":"<<terminals<<",\"states_by_stones\":";
    print_map(by_stones);
    std::cout<<",\"terminal_by_stones\":";
    print_map(terminal_by_stones);
    std::cout<<",\"all_replies_legal\":true}\n";
}
