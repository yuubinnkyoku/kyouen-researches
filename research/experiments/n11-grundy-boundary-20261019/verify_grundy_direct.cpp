// Independent C++ Grundy verifier: uses board geometry on every recursive move,
// not the Python forbidden-hyperedge reduction or saved WIN/LOSS verdicts.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
using U128=unsigned __int128;

long long det4(int a,int b,int c,int d){
    auto v=[&](int p){long long x=p%11-d%11,y=p/11-d/11;
        return array<long long,3>{x,y,x*x+y*y};};
    auto A=v(a),B=v(b),C=v(c);
    return A[0]*(B[1]*C[2]-B[2]*C[1])-A[1]*(B[0]*C[2]-B[2]*C[0])+A[2]*(B[0]*C[1]-B[1]*C[0]);
}
U128 parse(const string&s){
    if(s.size()!=32)throw runtime_error("bad board hex width");
    U128 x=0;
    for(char c:s){x<<=4;if(c>='0'&&c<='9')x|=c-'0';
        else if(c>='a'&&c<='f')x|=c-'a'+10;
        else throw runtime_error("bad hex digit");}
    if(x>>121)throw runtime_error("out-of-board bit");
    return x;
}
bool append_safe(const vector<int>&points,int p){
    for(size_t i=0;i<points.size();++i)
        for(size_t j=i+1;j<points.size();++j)
            for(size_t k=j+1;k<points.size();++k)
                if(det4(points[i],points[j],points[k],p)==0)return false;
    return true;
}
struct Result{int nimber;size_t states;int initial_moves;};
Result solve(U128 board){
    vector<int>base;
    for(int i=0;i<121;++i)if((board>>i)&1)base.push_back(i);
    if(base.size()!=10)throw runtime_error("not a ten-stone board");
    for(int i=0;i<10;++i){vector<int>other;
        for(int j=0;j<10;++j)if(i!=j)other.push_back(base[j]);
        if(!append_safe(other,base[i]))throw runtime_error("unsafe board");}
    vector<int>moves;
    for(int p=0;p<121;++p)if(!((board>>p)&1)&&append_safe(base,p))moves.push_back(p);
    if(moves.size()>63)throw runtime_error("too many moves");
    unordered_map<uint64_t,uint8_t> memo;
    memo.reserve(512);
    vector<int>current=base;
    auto dfs=[&](auto&&self,uint64_t state)->int{
        auto it=memo.find(state);if(it!=memo.end())return it->second;
        uint64_t child_values=0;
        for(size_t i=0;i<moves.size();++i){
            uint64_t bit=uint64_t(1)<<i;
            if(state&bit||!append_safe(current,moves[i]))continue;
            current.push_back(moves[i]);
            int g=self(self,state|bit);
            current.pop_back();
            if(g>=63)throw runtime_error("nimber too large");
            child_values|=uint64_t(1)<<g;
        }
        int mex=0;
        while((child_values>>mex)&1)++mex;
        memo[state]=(uint8_t)mex;
        return mex;
    };
    int nimber=dfs(dfs,0);
    return {nimber,memo.size(),(int)moves.size()};
}
int main(int argc,char**argv){
    if(argc!=3){cerr<<"usage: verify_grundy_direct INPUT OUTPUT\n";return 2;}
    ifstream in(argv[1]);ofstream out(argv[2]);
    if(!in||!out)throw runtime_error("cannot open input/output");
    string s;size_t count=0,total=0;array<int,16>hist{};
    while(in>>s){auto r=solve(parse(s));out<<s<<'\t'<<r.nimber<<'\t'<<r.states<<'\t'<<r.initial_moves<<'\n';
        if(r.nimber>=16)throw runtime_error("nimber exceeds histogram");
        ++hist[r.nimber];total+=r.states;++count;}
    cerr<<"roots="<<count<<" states="<<total<<" nimbers:";
    for(int i=0;i<16;++i)if(hist[i])cerr<<' '<<i<<'='<<hist[i];
    cerr<<'\n';
}
