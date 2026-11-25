// Shared/canonical terminal minimax across 734 independently proven S10 WIN leaves.
// Modes 0..3 isolate table-sharing and D4 symmetry; priority 1 is natural order.
#define main original_adaptive52_main
#include "../n11-four-s8-shared-tt-20261023/adaptive52.cpp"
#undef main
int main(int argc,char**argv){try{
 need(argc==5,"usage: shared734 S10_KEYS ORDER_MODE PRIORITY_MODE TABLE_MODE");
 init_d4();ifstream f(argv[1]);need(f.good(),"input not found");
 vector<U> keys;string h;while(f>>h){U b=parse(h);need(points(b).size()==10&&safe(b)&&canon(b)==b,"invalid canonical S10");keys.push_back(b);}
 need(keys.size()==734&&set<U>(keys.begin(),keys.end()).size()==734,"expected 734 distinct leaves");
 int order=stoi(argv[2]),priority=stoi(argv[3]),table=stoi(argv[4]);
 need(order==0||order==1,"bad order");need(priority>=1&&priority<=10,"bad priority");need(table>=0&&table<=3,"bad table mode");
 if(order==1)reverse(keys.begin(),keys.end());
 Solver s;s.mode=(table%2);s.memo.reserve(400000);
 uint64_t states=0,lookups=0,hits=0,edges=0;
 for(U key:keys){
  Root r=prepare(key,priority);
  if(table<2){Solver local;local.mode=table;local.memo.reserve(2048);need(local.dfs(r,0,key),"LOSS leaf: "+hx(key));states+=local.memo.size();lookups+=local.lookups;hits+=local.hits;edges+=local.children;}
  else need(s.dfs(r,0,key),"LOSS leaf: "+hx(key));
 }
 if(table>=2){states=s.memo.size();lookups=s.lookups;hits=s.hits;edges=s.children;}
 cout<<"PASS leaves=734 WIN=734 states="<<states<<" lookups="<<lookups<<" hits="<<hits<<" edges="<<edges<<" order="<<order<<" priority="<<priority<<" table="<<table<<"\n";
 return 0;
}catch(exception&e){cerr<<"ERROR: "<<e.what()<<"\n";return 1;}}
