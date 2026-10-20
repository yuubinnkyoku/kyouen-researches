// Direct full-board legal-move minimax, independent of forbidden-edge reduction.
// 11x11 q=4, normal play. No cache is read or trusted across S10 inputs.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
using U128 = unsigned __int128;

int coordx(int p){return p%11;}
int coordy(int p){return p/11;}
long long det4(int a,int b,int c,int d){
    auto diff=[&](int p){long long x=coordx(p),y=coordy(p),u=coordx(d),v=coordy(d);return array<long long,3>{x-u,y-v,x*x+y*y-u*u-v*v};};
    auto A=diff(a),B=diff(b),C=diff(c);
    return A[0]*(B[1]*C[2]-B[2]*C[1])-A[1]*(B[0]*C[2]-B[2]*C[0])+A[2]*(B[0]*C[1]-B[1]*C[0]);
}
U128 parse(const string&s){
    if(s.size()!=32)throw runtime_error("invalid hex length");
    U128 v=0;
    for(char c:s){v<<=4;if(c>='0'&&c<='9')v|=c-'0';else if(c>='a'&&c<='f')v|=c-'a'+10;else throw runtime_error("invalid hex character");}
    if(v>>121)throw runtime_error("out-of-board bits");
    return v;
}
vector<int> occupied(U128 b){vector<int>p;for(int i=0;i<121;i++)if((b>>i)&1)p.push_back(i);return p;}
bool safe_append(const vector<int>&points,int p){
    for(size_t i=0;i<points.size();i++)for(size_t j=i+1;j<points.size();j++)for(size_t k=j+1;k<points.size();k++)
        if(det4(points[i],points[j],points[k],p)==0)return false;
    return true;
}
struct Result {bool first_wins;size_t states;int initial_moves;int witness;};
Result solve(U128 root){
    auto base=occupied(root);
    if(base.size()!=11)throw runtime_error("not 11 stones");
    for(size_t i=0;i<base.size();i++){
        vector<int>other;
        for(size_t j=0;j<base.size();j++)if(i!=j)other.push_back(base[j]);
        if(!safe_append(other,base[i]))throw runtime_error("unsafe root");
    }
    vector<int>candidates;
    for(int p=0;p<121;p++)if(!((root>>p)&1)&&safe_append(base,p))candidates.push_back(p);
    if(candidates.size()>63)throw runtime_error("too many candidates");
    unordered_map<uint64_t,bool> memo;
    memo.reserve(4096);
    vector<int>state_points=base;
    int witness=-1;
    auto dfs=[&](auto&&self,uint64_t state)->bool{
        auto it=memo.find(state);if(it!=memo.end())return it->second;
        for(size_t i=0;i<candidates.size();i++){
            uint64_t bit=uint64_t(1)<<i;
            if(state&bit)continue;
            int p=candidates[i];
            if(!safe_append(state_points,p))continue;
            state_points.push_back(p);
            bool opponent_wins=self(self,state|bit);
            state_points.pop_back();
            if(!opponent_wins){if(state==0)witness=p;memo[state]=true;return true;}
        }
        memo[state]=false;
        return false;
    };
    bool w=dfs(dfs,0);
    return {w,memo.size(),(int)candidates.size(),witness};
}
int main(int argc,char**argv){
    if(argc!=3){cerr<<"usage: verify_s10_direct INPUT OUTPUT\n";return 2;}
    ifstream in(argv[1]);ofstream out(argv[2]);
    if(!in||!out)throw runtime_error("cannot open file");
    string s;size_t n=0,w=0,total=0;
    while(in>>s){auto result=solve(parse(s));out<<s<<'\t'<<(result.first_wins?"WIN":"LOSS")<<'\t'<<result.states<<'\t'<<result.initial_moves<<'\t'<<result.witness<<'\n';n++;w+=result.first_wins;total+=result.states;}
    cerr<<"roots="<<n<<" WIN="<<w<<" LOSS="<<(n-w)<<" states="<<total<<'\n';
}
