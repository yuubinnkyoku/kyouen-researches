#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
using U=__uint128_t;
constexpr int N=11;
struct Hash{size_t operator()(U a)const noexcept{uint64_t lo=(uint64_t)a,hi=(uint64_t)(a>>64);return (lo*0x9e3779b97f4a7c15ULL)^(hi*0xbf58476d1ce4e5b9ULL);}};
array<int,121> X,Y,Z;
array<array<U,121>,8> d4;
unordered_map<int,U> circle_cache;
U ALL=((U(1)<<121)-1);
U bit(int p){return U(1)<<p;}
vector<int> points(U b){vector<int> a;for(int p=0;p<121;p++)if(b&bit(p))a.push_back(p);return a;}
string hex(U a){string s(32,'0');for(int i=31;i>=0;i--){int d=int(a&15);s[i]="0123456789abcdef"[d];a>>=4;}return s;}
U parse(string s){U x=0;for(char c:s){x=(x<<4)+(c>='0'&&c<='9'?c-'0':c-'a'+10);}return x;}
void init(){for(int p=0;p<121;p++){X[p]=p%11;Y[p]=p/11;Z[p]=X[p]*X[p]+Y[p]*Y[p];int x=X[p],y=Y[p];array<pair<int,int>,8> t={{{x,y},{10-y,x},{10-x,10-y},{y,10-x},{10-x,y},{10-y,10-x},{x,10-y},{y,x}}};for(int k=0;k<8;k++)d4[k][p]=bit(11*t[k].second+t[k].first);}}
U canonical(U b){vector<int> p=points(b);U best=ALL;for(auto &trans:d4){U r=0;for(int i:p)r|=trans[i];if(r<best)best=r;}return best;}
long long det4(int a,int b,int c,int d){int p[4]={a,b,c,d};long long M[4][4];for(int i=0;i<4;i++){M[i][0]=X[p[i]];M[i][1]=Y[p[i]];M[i][2]=Z[p[i]];M[i][3]=1;}int perm[4]={0,1,2,3};long long sum=0;do{int inv=0;for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)inv+=perm[i]>perm[j];long long prod=1;for(int i=0;i<4;i++)prod*=M[i][perm[i]];sum+=(inv&1)?-prod:prod;}while(next_permutation(perm,perm+4));return sum;}
U circle(int a,int b,int c){int key=(a<<14)|(b<<7)|c;auto it=circle_cache.find(key);if(it!=circle_cache.end())return it->second;U m=0;for(int p=0;p<121;p++)if(det4(a,b,c,p)==0)m|=bit(p);circle_cache[key]=m;return m;}
U legal(U b){vector<int> p=points(b);U block=b;for(int i=0;i<(int)p.size();i++)for(int j=i+1;j<(int)p.size();j++)for(int k=j+1;k<(int)p.size();k++)block|=circle(p[i],p[j],p[k]);return ALL^block;}
vector<U> children(U b){U m=legal(b);vector<U> a;for(int p=0;p<121;p++)if(m&bit(p))a.push_back(canonical(b|bit(p)));sort(a.begin(),a.end());a.erase(unique(a.begin(),a.end()),a.end());return a;}
unordered_map<U,uint8_t,Hash> memo;
bool solve(U b){auto it=memo.find(b);if(it!=memo.end())return it->second;bool ans=(points(b).size()%2)!=0;for(U ch:children(b)){bool val=solve(ch);if(ans&&!val){ans=false;break;}if(!ans&&val){ans=true;break;}}memo[b]=ans;return ans;}

int main(int argc,char**argv){init();if(argc!=2){cerr<<"usage: proof_cpp <s10 keys>\n";return 1;}ifstream in(argv[1]);string line;size_t n=0,sum=0;while(in>>line){U leaf=parse(line);if(points(leaf).size()!=10||canonical(leaf)!=leaf){cerr<<"invalid leaf";return 2;}memo.clear();bool val=solve(leaf);U moves=legal(leaf);int count=__builtin_popcountll((uint64_t)moves)+__builtin_popcountll((uint64_t)(moves>>64));cout<<hex(leaf)<<" "<<(val?"WIN":"LOSS")<<" "<<memo.size()<<" "<<count<<"\n";n++;sum+=memo.size();}cerr<<"PASS "<<n<<" S10 terminal leaves, states "<<sum<<"\n";}
