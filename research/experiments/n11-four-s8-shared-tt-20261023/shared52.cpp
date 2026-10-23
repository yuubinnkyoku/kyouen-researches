#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
using U=unsigned __int128;
struct Hash { size_t operator()(U x) const noexcept {uint64_t lo=(uint64_t)x,hi=(uint64_t)(x>>64);return std::hash<uint64_t>{}(lo^(hi*0x9e3779b97f4a7c15ULL));}};
void need(bool b,const string&s){if(!b)throw runtime_error(s);}
U parse(const string&s){need(s.size()==32,"hex size");U b=0;for(char c:s){b<<=4; if(c>='0'&&c<='9')b+=c-'0';else if(c>='a'&&c<='f')b+=c-'a'+10;else throw runtime_error("hex char");}need((b>>121)==0,"bounds");return b;}
string hx(U b){string s(32,'0');for(int i=31;i>=0;i--){s[i]="0123456789abcdef"[int(b&15)];b>>=4;}return s;}
vector<int> points(U b){vector<int>p;for(int i=0;i<121;i++)if((b>>i)&1)p.push_back(i);return p;}
long long det3(const array<array<long long,3>,3>&a){return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][1]*a[2][0])+a[0][2]*(a[0][1]*a[1][2]-a[0][2]*a[1][1]);}
bool bad(int a,int b,int c,int d){int p[4]={a,b,c,d};array<array<long long,3>,4>m;for(int i=0;i<4;i++){long long x=p[i]%11,y=p[i]/11;m[i]={x,y,x*x+y*y};}long long sum=0;for(int omit=0;omit<4;omit++){array<array<long long,3>,3>sub;int k=0;for(int j=0;j<4;j++)if(j!=omit)sub[k++]=m[j];sum+=(omit%2?-1:1)*det3(sub);}return sum==0;}
bool safe_add(const vector<int>&p,int x){for(int i=0;i<(int)p.size();i++)for(int j=i+1;j<(int)p.size();j++)for(int k=j+1;k<(int)p.size();k++)if(bad(p[i],p[j],p[k],x))return false;return true;}
bool safe(U b){vector<int>p=points(b);for(int i=0;i<(int)p.size();i++){vector<int>q=p;q.erase(q.begin()+i);if(!safe_add(q,p[i]))return false;}return true;}
int D4[8][121];
void init_d4(){for(int p=0;p<121;p++){int x=p%11,y=p/11;int X[8]={x,10-y,10-x,y,10-x,10-y,x,y};int Y[8]={y,x,10-y,10-x,y,10-x,10-y,x};for(int t=0;t<8;t++)D4[t][p]=11*Y[t]+X[t];}}
U canon(U b){auto p=points(b);U best=b;for(int t=1;t<8;t++){U v=0;for(int z:p)v|=U(1)<<D4[t][z];if(v<best)best=v;}return best;}
vector<int> legal(U b){auto p=points(b);vector<int>r;for(int x=0;x<121;x++)if(!((b>>x)&1)&&safe_add(p,x))r.push_back(x);return r;}
struct Root{U base;vector<int> moves;vector<vector<uint64_t>> blockers;vector<int> order;};
Root prepare(U b,int mode){need(points(b).size()==10&&safe(b),"bad root");Root r;r.base=b;r.moves=legal(b);int n=r.moves.size();need(n<=63,"too many moves");r.blockers.resize(n);
 auto add=[&](uint64_t mask){for(int i=0;i<n;i++)if(mask&(1ULL<<i))r.blockers[i].push_back(mask^(1ULL<<i));};
 auto prohibited=[&](uint64_t mask){for(int i=0;i<n;i++)if(mask&(1ULL<<i))for(auto sub:r.blockers[i])if((mask&~(1ULL<<i)&sub)==sub)return true;return false;};
 auto base=points(b);
 for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){
  bool forbidden=false;for(int a=0;a<(int)base.size()&&!forbidden;a++)for(int c=a+1;c<(int)base.size();c++)if(bad(base[a],base[c],r.moves[i],r.moves[j])){forbidden=true;break;}
  if(forbidden)add((1ULL<<i)|(1ULL<<j));
 }
 for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++){
  uint64_t mask=(1ULL<<i)|(1ULL<<j)|(1ULL<<k);if(prohibited(mask))continue;
  bool forbidden=false;for(int p:base)if(bad(p,r.moves[i],r.moves[j],r.moves[k])){forbidden=true;break;}
  if(forbidden)add(mask);
 }
 for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++)for(int l=k+1;l<n;l++){
  uint64_t mask=(1ULL<<i)|(1ULL<<j)|(1ULL<<k)|(1ULL<<l);if(prohibited(mask))continue;
  if(bad(r.moves[i],r.moves[j],r.moves[k],r.moves[l]))add(mask);
 }
 r.order.resize(n);iota(r.order.begin(),r.order.end(),0);
 if(mode>=2){
  vector<int> influence(n),all(n),triple(n),quad(n),dist(n);
  for(int i=0;i<n;i++){
    for(auto sub:r.blockers[i]){all[i]++;int k=__builtin_popcountll(sub);if(k==1)influence[i]++;if(k==2)triple[i]++;if(k==3)quad[i]++;}
    int x=r.moves[i]%11,y=r.moves[i]/11;dist[i]=abs(x-5)+abs(y-5);
  }
  stable_sort(r.order.begin(),r.order.end(),[&](int a,int c){
    auto score=[&](int i)->long long{
      switch(mode){
      case 2:return 100000LL*influence[i];
      case 3:return 100000LL*all[i];
      case 4:return -100000LL*dist[i];
      case 5:return -100000LL*influence[i];
      case 6:return 100000LL*influence[i]+1000LL*triple[i]+quad[i];
      case 7:return 100000LL*influence[i]+1000LL*triple[i]-dist[i];
      case 8:return 100000LL*all[i]-100LL*dist[i];
      case 9:return 100000LL*triple[i]+1000LL*quad[i];
      }return 0LL;
    };
    if(score(a)!=score(c))return score(a)>score(c);
    return r.moves[a]<r.moves[c];
  });
 }
 return r;
}
struct Solver{
 unordered_map<U,uint8_t,Hash> memo;
 uint64_t lookups=0,hits=0,entries=0,children=0;
 int mode;
 bool dfs(const Root&r,uint64_t mask,U board){
  U key=mode==0?board:canon(board);
  lookups++;
  auto it=memo.find(key);if(it!=memo.end()){hits++;return it->second;}
  bool result=false;
  for(int i:r.order)if(!(mask&(1ULL<<i))){bool okay=true;for(auto sub:r.blockers[i])if((mask&sub)==sub){okay=false;break;}if(!okay)continue;
    children++;
    if(!dfs(r,mask|(1ULL<<i),board|(U(1)<<r.moves[i]))){result=true;break;}
  }
  memo.emplace(key,result);entries++;
  return result;
 }
};
int main(int argc,char**argv){try{
 need(argc>=3,"usage: shared52 selected52.keys MODE(0=plain 1=D4 2..9=D4+heuristics) [reverse] [separate]");init_d4();int mode=stoi(argv[2]);need(mode>=0&&mode<=9,"bad mode");vector<U> roots;ifstream f(argv[1]);string s;while(f>>s){U b=parse(s);need(canon(b)==b,"noncanonical root");roots.push_back(b);}need(roots.size()==52,"52 roots expected");need(set<U>(roots.begin(),roots.end()).size()==52,"duplicate roots");bool reverse_order=false,separate=false;for(int i=3;i<argc;i++){if(string(argv[i])=="reverse")reverse_order=true;else if(string(argv[i])=="separate")separate=true;else throw runtime_error("unknown option");}if(reverse_order)reverse(roots.begin(),roots.end());
 Solver sol;sol.mode=mode;sol.memo.reserve(25000);size_t root_n=0,sum_separate=0;
 auto start=chrono::steady_clock::now();for(U b:roots){Root r=prepare(b,mode);bool w=sol.dfs(r,0,b);need(!w,"selected leaf is not LOSS "+hx(b));root_n++;if(separate){sum_separate+=sol.memo.size();sol.memo.clear();}}
 auto elapsed=chrono::duration<double>(chrono::steady_clock::now()-start).count();cout<<"PASS roots="<<root_n<<" states="<<(separate?sum_separate:sol.memo.size())<<" lookups="<<sol.lookups<<" hits="<<sol.hits<<" hit_rate="<<double(sol.hits)/sol.lookups<<" children="<<sol.children<<" seconds="<<elapsed<<" mode="<<mode<<"\n";
 return 0;
 }catch(exception&e){cerr<<"ERROR "<<e.what()<<"\n";return 1;}}
