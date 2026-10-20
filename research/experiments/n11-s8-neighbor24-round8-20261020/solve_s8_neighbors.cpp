#define main old_main
#include "verify_s10_direct.cpp"
#undef main
#include <algorithm>
#include <iomanip>
#include <sstream>
#include <unordered_set>
#include <chrono>

string hex128(U128 v){string s(32,'0');for(int i=31;i>=0;i--){s[i]="0123456789abcdef"[(int)(v&15)];v>>=4;}return s;}
U128 canon(U128 v){auto ps=occupied(v);U128 best=~U128(0);for(int t=0;t<8;t++){U128 z=0;for(int p:ps){int x=p%11,y=p/11,xx,yy;switch(t){case 0:xx=x;yy=y;break;case 1:xx=10-y;yy=x;break;case 2:xx=10-x;yy=10-y;break;case 3:xx=y;yy=10-x;break;case 4:xx=10-x;yy=y;break;case 5:xx=10-y;yy=10-x;break;case 6:xx=x;yy=10-y;break;default:xx=y;yy=x;}z|=U128(1)<<(11*yy+xx);}best=min(best,z);}return best;}
struct Hash{size_t operator()(U128 a)const noexcept{return (uint64_t)a^((uint64_t)(a>>64)*0x9e3779b97f4a7c15ULL);}};
struct Leaf{U128 pos;bool win;int states;};
int main(int argc,char**argv){if(argc!=3){cerr<<"usage: INPUT OUTPUT\n";return 2;}ifstream in(argv[1]);ofstream out(argv[2]);unordered_map<U128,Result,Hash> cache;cache.reserve(20000);int total=0;string h;while(in>>h){U128 root=parse(h);if(occupied(root).size()!=8||canon(root)!=root)throw runtime_error("bad S8 root");auto b=occupied(root);for(int p:b){auto c=b;c.erase(find(c.begin(),c.end(),p));if(!safe_append(c,p))throw runtime_error("unsafe S8");}vector<int> moves9;for(int p=0;p<121;p++)if(!((root>>p)&1)&&safe_append(b,p))moves9.push_back(p);bool rootwin=false;vector<pair<U128,U128>> loss_witnesses;vector<U128> win_children;U128 win_s9=0;size_t calculated_before=cache.size();for(int p:moves9){U128 s9=root|(U128(1)<<p);auto b9=b;b9.push_back(p);bool s9loss=true;vector<U128> local_wins;U128 loss10=0;for(int q=0;q<121;q++)if(!((s9>>q)&1)&&safe_append(b9,q)){U128 s10=canon(s9|(U128(1)<<q));auto it=cache.find(s10);if(it==cache.end()){auto res=solve(s10);it=cache.emplace(s10,res).first;}if(!it->second.first_wins){s9loss=false;loss10=s10;break;}local_wins.push_back(s10);}if(s9loss){rootwin=true;win_s9=canon(s9);win_children=local_wins;break;}loss_witnesses.emplace_back(canon(s9),loss10);}
 out<<"ROOT\t"<<h<<"\t"<<(rootwin?"WIN":"LOSS")<<"\t"<<moves9.size()<<"\t"<<(cache.size()-calculated_before)<<"\n";
 if(rootwin){out<<"S9_LOSS\t"<<hex128(win_s9)<<"\n";for(U128 x:win_children)out<<"S10_WIN\t"<<hex128(x)<<"\n";}else for(auto [x,y]:loss_witnesses)out<<"S9_WIN\t"<<hex128(x)<<"\t"<<hex128(y)<<"\n";
 cerr<<"root "<<++total<<" "<<h<<" "<<(rootwin?"WIN":"LOSS")<<" s9="<<moves9.size()<<" new_s10="<<cache.size()-calculated_before<<" total_s10="<<cache.size()<<endl;
 }
 size_t states=0,w=0;for(auto [k,v]:cache){states+=v.states;w+=v.first_wins;}cerr<<"TOTAL roots="<<total<<" s10="<<cache.size()<<" WIN="<<w<<" LOSS="<<cache.size()-w<<" states="<<states<<endl;
}
