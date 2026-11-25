// Independent C++17 terminal checker for eighty canonical 9-stone WIN witnesses (20 distinct S10 children each).
// Only the fixed witness list is an input. No cached verdicts, no JS geometry.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;
using U128 = unsigned __int128;
using U32 = uint32_t;
struct Hash128 { size_t operator()(U128 x) const {return (uint64_t)x ^ (uint64_t)(x>>64)*0x9e3779b97f4a7c15ULL;} };
struct Pt {int64_t x,y,z;};
Pt p[121];
void check(bool b, const string& m){if(!b)throw runtime_error(m);}
U128 parse(const string& s){check(s.size()==32,"key width");U128 v=0;for(char c:s){int n=c>='0'&&c<='9'?c-'0':c>='a'&&c<='f'?c-'a'+10:-1;check(n>=0,"key hex");v=(v<<4)|n;}return v;}
vector<int> pts(U128 b){vector<int> out;for(int i=0;i<121;i++)if((b>>i)&1)out.push_back(i);return out;}
U128 canonical(U128 b){auto a=pts(b);U128 best=~(U128)0;for(int t=0;t<8;t++){U128 r=0;for(int i:a){int x=i%11,y=i/11,nx,ny;switch(t){case 0:nx=x;ny=y;break;case 1:nx=10-y;ny=x;break;case 2:nx=10-x;ny=10-y;break;case 3:nx=y;ny=10-x;break;case 4:nx=10-x;ny=y;break;case 5:nx=10-y;ny=10-x;break;case 6:nx=x;ny=10-y;break;default:nx=y;ny=x;}r|=(U128)1<<(ny*11+nx);}best=min(best,r);}return best;}
int64_t det3(const array<array<int64_t,3>,3>& m){return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]);}
bool forbidden(int a,int b,int c,int d){
 int ids[4]={a,b,c,d};array<array<int64_t,4>,4> m{};
 for(int i=0;i<4;i++){auto q=p[ids[i]];m[i]={q.x,q.y,q.z,1};}
 int64_t det=0;for(int j=0;j<4;j++){
  array<array<int64_t,3>,3> sub{};
  for(int i=1;i<4;i++){int k=0;for(int col=0;col<4;col++)if(col!=j)sub[i-1][k++]=m[i][col];}
  det+=(j%2?-1:1)*m[0][j]*det3(sub);
 }
 return det==0;
}
bool safe(U128 b){auto a=pts(b);for(int i=0;i<(int)a.size();i++)for(int j=i+1;j<(int)a.size();j++)for(int k=j+1;k<(int)a.size();k++)for(int l=k+1;l<(int)a.size();l++)if(forbidden(a[i],a[j],a[k],a[l]))return false;return true;}
vector<int> legal(U128 b){auto a=pts(b);vector<array<int,3>> tri;
 for(int i=0;i<(int)a.size();i++)for(int j=i+1;j<(int)a.size();j++)for(int k=j+1;k<(int)a.size();k++)tri.push_back({a[i],a[j],a[k]});
 vector<int> out;for(int q=0;q<121;q++){if((b>>q)&1)continue;bool ok=true;for(auto t:tri)if(forbidden(t[0],t[1],t[2],q)){ok=false;break;}if(ok)out.push_back(q);}return out;
}
struct Result {bool win;int states,legal;};
Result solve10(U128 b){auto base=pts(b);check(base.size()==10,"not ten stones");auto moves=legal(b);int n=moves.size();check(n<=30,"mask overflow");
 vector<U32> bad;
 auto has_sub=[&](U32 mask){for(U32 x:bad)if((mask&x)==x)return true;return false;};
 for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){
  bool fail=false;for(int a=0;a<10&&!fail;a++)for(int c=a+1;c<10;c++)if(forbidden(base[a],base[c],moves[i],moves[j])){fail=true;break;}
  if(fail)bad.push_back((1u<<i)|(1u<<j));
 }
 for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++){
  U32 mask=(1u<<i)|(1u<<j)|(1u<<k);if(has_sub(mask))continue;
  bool fail=false;for(int a:base)if(forbidden(a,moves[i],moves[j],moves[k])){fail=true;break;}
  if(fail)bad.push_back(mask);
 }
 for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++)for(int l=k+1;l<n;l++){
  U32 mask=(1u<<i)|(1u<<j)|(1u<<k)|(1u<<l);
  if(!has_sub(mask)&&forbidden(moves[i],moves[j],moves[k],moves[l]))bad.push_back(mask);
 }
 vector<vector<U32>> bans(n);for(U32 mask:bad)for(int i=0;i<n;i++)if(mask&(1u<<i))bans[i].push_back(mask^(1u<<i));
 unordered_map<U32,bool> memo;
 auto rec=[&](auto&& self,U32 state)->bool{
  auto it=memo.find(state);if(it!=memo.end())return it->second;
  for(int i=0;i<n;i++){U32 bit=1u<<i;if(state&bit)continue;
   bool fail=false;for(U32 x:bans[i])if((state&x)==x){fail=true;break;}
   if(!fail&&!self(self,state|bit)){memo.emplace(state,true);return true;}
  }
  memo.emplace(state,false);return false;
 };
 bool win=rec(rec,0);return {win,(int)memo.size(),n};
}
int main(int argc,char** argv){try{
 check(argc==2,"usage: independent_terminal CERTIFICATE.tsv");
 for(int i=0;i<121;i++){int x=i%11,y=i/11;p[i]={x,y,x*x+y*y};}
 ifstream in(argv[1]);check(in.good(),"cannot open certificate");
 const vector<string> headers={
  "# n11-s9-n20-terminal-v1",
  "# board=11 perspective=original-first-player",
  "# empty_board=UNKNOWN",
  "# s9_win canonical_s10_children terminal_states_per_geometry"};
 string line;for(auto h:headers){check((bool)getline(in,line)&&line==h,"certificate header mismatch");}
 vector<pair<string,int>> roots;unordered_set<U128,Hash128> rootKeys;
 while(getline(in,line)){
  check(!line.empty(),"empty certificate row");
  istringstream ss(line);string key,extra;int leaves=0,states=0;
  check((bool)(ss>>key>>leaves>>states)&&!(ss>>extra),"invalid certificate row");
  check(leaves==20&&states>0,"invalid certificate counts");
  U128 b=parse(key);check(rootKeys.insert(b).second,"duplicate S9 witness");
  roots.push_back({key,states});
 }
 check(roots.size()==80,"wrong S9 witness count");
 unordered_set<U128,Hash128> unique10,parents8;int totalStates=0,totalEdges=0;
 for(auto [key,expected]:roots){U128 b=parse(key);check(pts(b).size()==9&&canonical(b)==b,"invalid canonical S9 root");
  check(safe(b),"unsafe S9 root");
  for(int occupied:pts(b)){
   U128 parent=canonical(b^((U128)1<<occupied));
   bool incidence=false;
   for(int q:legal(parent))if(canonical(parent|((U128)1<<q))==b){incidence=true;break;}
   check(incidence,"illegal S8 to S9 witness incidence");parents8.insert(parent);
  }
  auto children=legal(b);unordered_set<U128,Hash128> childKeys;int subtotal=0;
  for(int q:children){U128 c=canonical(b|((U128)1<<q));childKeys.insert(c);
   auto r=solve10(c);check(r.win,"S10 non-WIN leaf");subtotal+=r.states;unique10.insert(c);totalEdges++;
  }
  check(childKeys.size()==20&&children.size()==20,"incorrect S9 boundary");
  check(subtotal==expected,"S9 terminal states mismatch");totalStates+=subtotal;
 }
 check(totalEdges==1600&&unique10.size()==1573&&totalStates==157557&&parents8.size()==689,"total witness census mismatch");
 cout<<"PASS independent C++ terminal replay: 80 S9 WIN, 689 S8 WIN parents, 1600 S10 edges, 1573 distinct leaves, 157557 states; empty board UNKNOWN\n";
 }catch(const exception& e){cerr<<"FAIL "<<e.what()<<'\n';return 1;}}
