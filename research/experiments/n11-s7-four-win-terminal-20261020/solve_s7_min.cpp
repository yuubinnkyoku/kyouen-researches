#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iomanip>
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
string hx(U v){string s(32,'0');for(int i=31;i>=0;i--){int x=v&15;s[i]="0123456789abcdef"[x];v>>=4;}return s;}
U parse(string s){if(s.size()!=32)throw runtime_error("invalid hex");U x=0;for(char c:s){x<<=4;if(c>='0'&&c<='9')x+=c-'0';else if(c>='a'&&c<='f')x+=c-'a'+10;else throw runtime_error("invalid hex");}if(x>>121)throw runtime_error("out of bounds");return x;}
vector<int> pts(U b){vector<int>v;for(int i=0;i<121;i++)if((b>>i)&1)v.push_back(i);return v;}
long long det4(int a,int b,int c,int d){auto vec=[&](int p){long long x=p%11,y=p/11,dx=d%11,dy=d/11;return array<long long,3>{x-dx,y-dy,x*x+y*y-dx*dx-dy*dy};};auto A=vec(a),B=vec(b),C=vec(c);return A[0]*(B[1]*C[2]-B[2]*C[1])-A[1]*(B[0]*C[2]-B[2]*C[0])+A[2]*(B[0]*C[1]-B[1]*C[0]);}
bool safe_append(const vector<int>&v,int p){for(size_t i=0;i<v.size();i++)for(size_t j=i+1;j<v.size();j++)for(size_t k=j+1;k<v.size();k++)if(!det4(v[i],v[j],v[k],p))return false;return true;}
bool safe(U b){auto p=pts(b);for(size_t i=0;i<p.size();i++){auto q=p;q.erase(q.begin()+i);if(!safe_append(q,p[i]))return false;}return true;}
U canonical(U b){U best=~U(0);for(int t=0;t<8;t++){U v=0;for(int p:pts(b)){int x=p%11,y=p/11,xx=0,yy=0;switch(t){case 0:xx=x;yy=y;break;case 1:xx=10-y;yy=x;break;case 2:xx=10-x;yy=10-y;break;case 3:xx=y;yy=10-x;break;case 4:xx=10-x;yy=y;break;case 5:xx=10-y;yy=10-x;break;case 6:xx=x;yy=10-y;break;case 7:xx=y;yy=x;break;}v|=U(1)<<(11*yy+xx);}best=min(best,v);}return best;}
vector<U> children(U b){auto p=pts(b);set<U>c;for(int i=0;i<121;i++)if(!((b>>i)&1)&&safe_append(p,i))c.insert(canonical(b|(U(1)<<i)));return {c.begin(),c.end()};}
struct R{bool win;size_t states;int moves;};
R solve10(U b){auto base=pts(b);if(base.size()!=10||!safe(b))throw runtime_error("bad s10");vector<int>can;for(int p=0;p<121;p++)if(!((b>>p)&1)&&safe_append(base,p))can.push_back(p);if(can.size()>63)throw runtime_error("too many moves");unordered_map<uint64_t,bool>memo;memo.reserve(4096);auto current=base;auto dfs=[&](auto&&self,uint64_t mask)->bool{auto it=memo.find(mask);if(it!=memo.end())return it->second;for(size_t i=0;i<can.size();i++){uint64_t bit=uint64_t(1)<<i;if(mask&bit)continue;if(!safe_append(current,can[i]))continue;current.push_back(can[i]);bool w=self(self,mask|bit);current.pop_back();if(!w)return memo[mask]=true;}return memo[mask]=false;};bool w=dfs(dfs,0);return {w,memo.size(),(int)can.size()};}
map<U,R> memo10;
map<U,pair<bool,vector<U>>>memo9;
map<U,pair<bool,vector<U>>>memo8;
long long calls10=0;
R get10(U b){auto it=memo10.find(b);if(it!=memo10.end())return it->second;R r=solve10(b);memo10[b]=r;calls10++;return r;}
// At odd S9, first-player WIN iff ALL S10 children WIN.
pair<bool,vector<U>> get9(U b){auto it=memo9.find(b);if(it!=memo9.end())return it->second;vector<U>ch=children(b);vector<U>proof;for(U c:ch){bool w=get10(c).win;proof.push_back(c);if(!w){return memo9[b]={false,{c}};}}return memo9[b]={true,proof};}
// At even S8, first-player WIN iff ANY S9 child WIN.
pair<bool,vector<U>> get8(U b){auto it=memo8.find(b);if(it!=memo8.end())return it->second;vector<U>ch=children(b);sort(ch.begin(),ch.end(),[](U a,U b){return children(a).size()<children(b).size();});vector<U>proof;for(U c:ch){bool w=get9(c).first;proof.push_back(c);if(w)return memo8[b]={true,{c}};}return memo8[b]={false,proof};}
int main(int argc,char**argv){if(argc!=3){cerr<<"usage: solve_s7 missing.txt prefix\n";return 2;}ifstream in(argv[1]);string s;vector<U>roots;while(in>>s){U b=parse(s);if(pts(b).size()!=7||!safe(b)||canonical(b)!=b)throw runtime_error("bad s7");roots.push_back(b);}string prefix=argv[2];ofstream result(prefix+".results.tsv");for(U b:roots){auto ch=children(b);vector<U> proof;bool win=true;for(U c:ch){bool w=get8(c).first;proof.push_back(c);if(!w){win=false;proof={c};break;}}result<<hx(b)<<'\t'<<(win?"WIN":"LOSS")<<'\t'<<ch.size()<<'\t'<<proof.size()<<'\n';cerr<<hx(b)<<" "<<(win?"WIN":"LOSS")<<" s8checked="<<proof.size()<<" s10="<<memo10.size()<<"\n";}
ofstream f10(prefix+".s10.tsv"),f9(prefix+".s9.tsv"),f8(prefix+".s8.tsv");for(auto [b,r]:memo10)f10<<hx(b)<<'\t'<<(r.win?"WIN":"LOSS")<<'\t'<<r.states<<'\t'<<r.moves<<'\n';for(auto [b,r]:memo9){f9<<hx(b)<<'\t'<<(r.first?"WIN":"LOSS");for(U c:r.second)f9<<'\t'<<hx(c);f9<<'\n';}for(auto [b,r]:memo8){f8<<hx(b)<<'\t'<<(r.first?"WIN":"LOSS");for(U c:r.second)f8<<'\t'<<hx(c);f8<<'\n';}cerr<<"DONE S8="<<memo8.size()<<" S9="<<memo9.size()<<" S10="<<memo10.size()<<" direct calls="<<calls10<<"\n";
}
