// Verify fixed 734-leaf schedule using C++ exact 4x4 integer determinants.
#define main unused_adaptive52_main
#include "../n11-four-s8-shared-tt-20261023/adaptive52.cpp"
#undef main
using Weights=array<long long,4>;
const vector<Weights> menu={
 {100000,1000,0,-1},{100000,1000,0,1},{100000,1000,0,-10},{100000,1000,0,10},
 {100000,1000,1,-1},{100000,1000,-1,-1},{100000,100,0,-1},{100000,10000,0,-1},
 {24,8,-31,9},{100000,0,0,0},{100000,1000,0,-100},{100000,1000,0,100},
 {100000,1000,10,-1},{100000,1000,-10,-1},{100000,1000,0,0},{100000,1000,0,-3},
 {100000,1000,0,3},{100000,1000,0,-30},{100000,1000,0,30},{100000,1000,0,-300}
};
int main(int argc,char**argv){try{
 need(argc==3,"usage: verify_schedule734 S10_KEYS COMPACT_SCHEDULE");init_d4();
 ifstream f(argv[1]);need(f.good(),"keys missing");vector<U> keys;string h;
 while(f>>h){U b=parse(h);need(points(b).size()==10&&safe(b)&&canon(b)==b,"bad S10");keys.push_back(b);}
 need(keys.size()==734&&set<U>(keys.begin(),keys.end()).size()==734,"wrong leaf set");
 need(is_sorted(keys.begin(),keys.end()),"keys not sorted");reverse(keys.begin(),keys.end());
 ifstream g(argv[2]);need(g.good(),"schedule missing");string schedule,chunk;
 while(g>>chunk)schedule+=chunk;
 need(schedule.size()==1468,"wrong schedule length");
 for(char c:schedule)need((c>='0'&&c<='9')||(c>='a'&&c<='f'),"bad schedule digit");
 Solver solver;solver.mode=1;solver.memo.reserve(100000);
 for(size_t i=0;i<734;i++){
  auto nib=[](char c){return c<='9'?c-'0':c-'a'+10;};
  int j=16*nib(schedule[2*i])+nib(schedule[2*i+1]);need(j<(int)menu.size(),"bad schedule index");
  for(int k=0;k<4;k++)W[k]=menu[j][k];
  Root root=prepare(keys[i],10);need(solver.dfs(root,0,keys[i]),"LOSS leaf");
 }
 cout<<"PASS S10=734 WIN=734 states="<<solver.memo.size()<<" lookups="<<solver.lookups<<" hits="<<solver.hits<<" edges="<<solver.children<<" empty=UNKNOWN\n";
 need(solver.memo.size()==48794&&solver.lookups==81853&&solver.hits==33059&&solver.children==81119,"metrics mismatch");
 return 0;
}catch(exception&e){cerr<<"ERROR: "<<e.what()<<'\n';return 1;}}
