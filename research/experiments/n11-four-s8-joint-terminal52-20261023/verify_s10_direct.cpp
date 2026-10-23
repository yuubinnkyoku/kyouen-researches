#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
using U=unsigned __int128;
void need(bool b,const string&s){if(!b)throw runtime_error(s);}
U parse(const string&s){need(s.size()==32,"hex size");U b=0;for(char c:s){b<<=4; if(c>='0'&&c<='9')b+=c-'0';else if(c>='a'&&c<='f')b+=c-'a'+10;else throw runtime_error("hex char");}need((b>>121)==0,"bounds");return b;}
string hx(U b){string s(32,'0');for(int i=31;i>=0;i--){s[i]="0123456789abcdef"[int(b&15)];b>>=4;}return s;}
vector<int> points(U b){vector<int>p;for(int i=0;i<121;i++)if((b>>i)&1)p.push_back(i);return p;}
// Independent 4x4 determinant, expansion along final column.
long long det3(const array<array<long long,3>,3>&a){return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]);}
bool bad(int a,int b,int c,int d){int p[4]={a,b,c,d};array<array<long long,3>,4>m;for(int i=0;i<4;i++){long long x=p[i]%11,y=p[i]/11;m[i]={x,y,x*x+y*y};}long long sum=0;for(int omit=0;omit<4;omit++){array<array<long long,3>,3>sub;int k=0;for(int j=0;j<4;j++)if(j!=omit)sub[k++]=m[j];sum+=(omit%2?-1:1)*det3(sub);}return sum==0;}
bool safe_add(const vector<int>&p,int x){for(int i=0;i<(int)p.size();i++)for(int j=i+1;j<(int)p.size();j++)for(int k=j+1;k<(int)p.size();k++)if(bad(p[i],p[j],p[k],x))return false;return true;}
bool safe(U b){vector<int>p=points(b);for(int i=0;i<(int)p.size();i++){vector<int>q=p;q.erase(q.begin()+i);if(!safe_add(q,p[i]))return false;}return true;}
U canon(U b){auto p=points(b);U best=~U(0);for(int t=0;t<8;t++){U v=0;for(int z:p){int x=z%11,y=z/11;int X=x,Y=y;switch(t){case 0:break;case 1:X=10-y;Y=x;break;case 2:X=10-x;Y=10-y;break;case 3:X=y;Y=10-x;break;case 4:X=10-x;break;case 5:X=10-y;Y=10-x;break;case 6:Y=10-y;break;case 7:X=y;Y=x;break;}v|=U(1)<<(11*Y+X);}best=min(best,v);}return best;}
vector<int> legal(U b){auto p=points(b);vector<int>r;for(int x=0;x<121;x++)if(!((b>>x)&1)&&safe_add(p,x))r.push_back(x);return r;}
set<U> children(U b){set<U>r;for(int p:legal(b))r.insert(canon(b|(U(1)<<p)));return r;}
struct Result{bool win;size_t states;int legal;};
Result terminal(U b){auto base=points(b);need(base.size()==10 && safe(b),"bad terminal root");auto moves=legal(b);int n=moves.size();need(n<=63,"terminal move width");vector<vector<uint64_t>> blockers(n);
  auto add_block=[&](uint64_t mask){for(int i=0;i<n;i++)if(mask&(1ULL<<i))blockers[i].push_back(mask^(1ULL<<i));};
  for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){
    bool forbidden=false;for(int a=0;a<(int)base.size()&&!forbidden;a++)for(int c=a+1;c<(int)base.size();c++)if(bad(base[a],base[c],moves[i],moves[j])){forbidden=true;break;}
    if(forbidden)add_block((1ULL<<i)|(1ULL<<j));
  }
  for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++){
    uint64_t mask=(1ULL<<i)|(1ULL<<j)|(1ULL<<k);bool already=false;
    for(int a:{i,j,k})for(uint64_t block:blockers[a])if(((mask^(1ULL<<a))&block)==block){already=true;break;}
    if(already)continue;
    bool forbidden=false;for(int p:base)if(bad(p,moves[i],moves[j],moves[k])){forbidden=true;break;}
    if(forbidden)add_block(mask);
  }
  for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++)for(int l=k+1;l<n;l++){
    uint64_t mask=(1ULL<<i)|(1ULL<<j)|(1ULL<<k)|(1ULL<<l);bool already=false;
    for(int a:{i,j,k,l})for(uint64_t block:blockers[a])if(((mask^(1ULL<<a))&block)==block){already=true;break;}
    if(already)continue;
    if(bad(moves[i],moves[j],moves[k],moves[l]))add_block(mask);
  }
  unordered_map<uint64_t,bool>memo;memo.reserve(1024);
  auto dfs=[&](auto&&self,uint64_t mask)->bool{
    auto it=memo.find(mask);if(it!=memo.end())return it->second;
    for(int i=0;i<n;i++)if(!(mask&(1ULL<<i))){bool okay=true;for(uint64_t block:blockers[i])if((mask&block)==block){okay=false;break;}if(okay&&!self(self,mask|(1ULL<<i)))return memo[mask]=true;}
    return memo[mask]=false;
  };
  bool win=dfs(dfs,0);return {win,memo.size(),n};
}
int main(int argc,char**argv){try{need(argc==3,"usage input keys output TSV");ifstream f(argv[1]);ofstream o(argv[2]);string h;size_t n=0,sum=0,w=0,l=0;while(f>>h){auto r=terminal(parse(h));o<<h<<" "<<(r.win?"WIN":"LOSS")<<" "<<r.states<<" "<<r.legal<<"\n";n++;sum+=r.states;if(r.win)w++;else l++;if(n%25==0)cerr<<"progress "<<n<<" states "<<sum<<"\n";}cerr<<"PASS n="<<n<<" WIN="<<w<<" LOSS="<<l<<" states="<<sum<<"\n";return 0;}catch(const exception&e){cerr<<"ERROR "<<e.what()<<"\n";return 1;}}
