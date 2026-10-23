// Exhaust all cube-symmetry pair orbits, rank residual triple orbits after terminal-four replies.
#define main historical_main
#include "../cube-q5-seven-frontier-20261022/solver.cpp"
#undef main
#include <set>
bool terminal_reply(const Solver& s,int a,int b,int c) {
    Row u{},v{};for(int k=0;k<4;k++){u[k]=s.points[b][k]-s.points[a][k];v[k]=s.points[c][k]-s.points[a][k];}
    int i=-1,j=-1;int64_t det=0;
    for(int x=0;x<4 && !det;x++)for(int y=x+1;y<4;y++)if(u[x]*v[y]-u[y]*v[x]){i=x;j=y;det=u[x]*v[y]-u[y]*v[x];break;}
    if(!det)throw std::runtime_error("rank-two lift expected");
    int k[2],at=0;for(int x=0;x<4;x++)if(x!=i && x!=j)k[at++]=x;
    for(int d=0;d<s.n;d++)if(d!=a && d!=b && d!=c) {
        Row w{};for(int x=0;x<4;x++)w[x]=s.points[d][x]-s.points[a][x];
        int64_t left=w[i]*v[j]-w[j]*v[i],right=u[i]*w[j]-u[j]*w[i];
        if(det*w[k[0]]==left*u[k[0]]+right*v[k[0]] && det*w[k[1]]==left*u[k[1]]+right*v[k[1]])return true;
    }
    return false;
}
int main(int argc,char**argv) {
    if(argc!=2)return 2;
    Solver s(std::stoi(argv[1]),0,1);std::set<Mask> pairs;
    for(int a=0;a<s.n;a++)for(int b=a+1;b<s.n;b++){Mask key;key.set(a);key.set(b);pairs.insert(s.canonical(key));}
    for(const Mask& pair:pairs) {
        auto ids=pair.ids();int a=ids[0],b=ids[1];std::vector<int> bad;std::set<Mask> orbits;
        for(int c=0;c<s.n;c++)if(c!=a && c!=b && !terminal_reply(s,a,b,c)){bad.push_back(c);Mask key=pair;key.set(c);orbits.insert(s.canonical(key));}
        std::cout<<"{\"pair\":["<<a<<","<<b<<"],\"uncovered\":"<<bad.size()<<",\"residual_triple_orbits\":"<<orbits.size()<<",\"thirds\":[";
        bool first=true;for(int c:bad){if(!first)std::cout<<",";first=false;std::cout<<c;}
        std::cout<<"],\"representatives\":[";first=true;
        for(const Mask& key:orbits){if(!first)std::cout<<",";first=false;std::cout<<"[";bool comma=false;for(int p:key.ids()){if(comma)std::cout<<",";comma=true;std::cout<<p;}std::cout<<"]";}
        std::cout<<"]}"<<std::endl;
    }
}
